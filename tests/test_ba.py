"""Danny-authorised BA needs/clarification slice; legacy CS/MC remain unchanged."""
import io
import json
import sqlite3
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from beauty_company.application import Company
from beauty_company.adapters.llm import StrataLlm, LlmConfig, ModelError
from beauty_company.adapters.mock import MockLlm
from beauty_company.adapters.needs import mock_extract, validate_extraction
from beauty_company.contracts import Actor, DomainError
from beauty_company.http import Router
from beauty_company.store import Store

CUSTOMER = Actor('customer', 'CUSTOMER', 'Demo')
OTHER = Actor('customer-2', 'CUSTOMER', 'Other')
FOUNDER = Actor('founder', 'FOUNDER', 'Founder')
FULL = 'A moisturiser for dry skin. Budget AUD 60. Fragrance-free required.'
CONFIRM = {'concern': 'HYDRATION', 'budget': 60, 'fragranceFree': True}


class BaNeedsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)/'ba.sqlite3'
        self.company = Company(self.path)
        self.intake = self.company.ba_intake

    def start(self, message=FULL):
        return self.intake.start(CUSTOMER, {'message': message})

    def confirm(self, record, **edits):
        return self.intake.confirm(CUSTOMER, record['id'],
                                   {'contextRevision': record['revision'], **CONFIRM, **edits})

    def saved(self, rid):
        with self.company.store.read() as db:
            return Store.get(db, rid)

    def no_effects(self):
        with self.company.store.read() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM effects').fetchone()[0], 0)
            self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-101'").fetchone()[0], 12)

    def test_ba_t_01_missing_conditions_are_questions_not_defaults(self):
        with patch.object(self.company.llm, 'propose') as recommend:
            record = self.start('A moisturiser for dry skin.')
            self.assertEqual(record['status'], 'CLARIFYING')
            p = record['payload']
            self.assertIsNone(p['proposedNeeds']['budget'])
            self.assertIsNone(p['proposedNeeds']['fragranceFree'])
            self.assertEqual(len(p['questions']), 2)
            self.assertFalse(p['needsReady'])
            self.assertNotIn('result', p)
            recommend.assert_not_called()
        self.no_effects()

    def test_ba_t_01_same_consultation_resumes_after_restart_and_requires_confirmation(self):
        record = self.start('A moisturiser for dry skin.')
        self.company = Company(self.path); self.intake = self.company.ba_intake
        with patch.object(self.company.llm, 'propose', wraps=self.company.llm.propose) as propose:
            reply = self.intake.clarify(CUSTOMER, record['id'], {'contextRevision': 1,
                'message': 'My budget is AUD 60 and fragrance-free is required.'})
            self.assertEqual((reply['id'], reply['revision'], reply['status']), (record['id'], 2, 'CLARIFYING'))
            self.assertTrue(reply['payload']['needsReady'])
            propose.assert_not_called()
            final = self.confirm(reply)
            self.assertEqual((final['id'], final['revision'], final['status']), (record['id'], 3, 'COMPLETED'))
            self.assertEqual(final['payload']['result']['product']['id'], 'P-101')
            self.assertTrue(final['payload']['simulated'])
            self.assertEqual(propose.call_count, 1)
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM records WHERE kind='BA'").fetchone()[0], 1)
        self.no_effects()

    def test_ba_t_01_sufficient_message_is_still_only_an_unconfirmed_hypothesis(self):
        record = self.start()
        self.assertEqual(record['status'], 'CLARIFYING')
        self.assertTrue(record['payload']['needsReady'])
        self.assertNotIn('result', record['payload'])
        self.assertNotIn('needsConfirmed', record['payload'])
        self.no_effects()

    def test_ba_t_01_explicit_optional_fragrance_and_chinese_fixture(self):
        for message, expected in [('Gentle cleansing, budget AUD 40, fragrance is fine.', False),
                                  ('需要保湿，预算60澳元，必须无香。', True)]:
            with self.subTest(message=message):
                record = self.start(message)
                self.assertTrue(record['payload']['needsReady'])
                self.assertIs(record['payload']['proposedNeeds']['fragranceFree'], expected)

    def test_ba_t_01_customer_can_correct_interpreted_fields_before_advice(self):
        record = self.start()
        result = self.confirm(record, concern='CLEANSING', budget=40)
        self.assertEqual(result['status'], 'COMPLETED')
        self.assertEqual(result['payload']['needs']['budget'], 4000)
        self.assertEqual(result['payload']['result']['product']['id'], 'P-102')
        self.no_effects()

    def test_ba_t_01_ambiguous_mock_budget_is_asked_again(self):
        record = self.start('Hydration, budget AUD 40 or AUD 60, fragrance-free.')
        self.assertIsNone(record['payload']['proposedNeeds']['budget'])
        self.assertEqual(record['payload']['questions'], ['What is your maximum budget in AUD?'])
        self.assertNotIn('result', record['payload'])

    def test_ba_t_04_quoted_budget_allows_sentence_punctuation_but_not_partial_decimal(self):
        extracted = mock_extract([FULL])
        extracted['sources']['budget'] = 'Budget AUD 60.'
        self.assertEqual(validate_extraction(extracted, [FULL])['budget'], 60)
        extracted['sources']['budget'] = 'Budget AUD 60.123'
        with self.assertRaises(ValueError):
            validate_extraction(extracted, ['Budget AUD 60.123', FULL])

    def test_ba_t_01_missing_needs_cannot_be_bypassed_by_direct_confirmation(self):
        record = self.start('Something for my skin.')
        with self.assertRaises(DomainError) as caught:
            self.confirm(record)
        self.assertEqual(caught.exception.code, 'NEEDS_NOT_READY')
        self.assertEqual(self.saved(record['id'])['revision'], 1)

    def test_ba_t_04_old_interpretation_does_not_overwrite_a_newer_answer(self):
        record = self.start('A moisturiser for dry skin.')
        entered, release = threading.Event(), threading.Event()
        def delayed(messages):
            if len(messages) == 2:
                entered.set()
                self.assertTrue(release.wait(10))
            return mock_extract(messages)
        with patch.object(self.company.llm, 'extract_needs', side_effect=delayed), ThreadPoolExecutor(1) as pool:
            future = pool.submit(self.intake.clarify, CUSTOMER, record['id'],
                                 {'contextRevision': 1, 'message': 'Budget AUD 60. Fragrance-free required.'})
            try:
                self.assertTrue(entered.wait(5))
                latest = self.intake.clarify(CUSTOMER, record['id'],
                    {'contextRevision': 2, 'message': 'Correction: budget AUD 40.'})
                self.assertEqual(latest['payload']['proposedNeeds']['budget'], 40)
            finally:
                release.set()
            with self.assertRaises(DomainError) as caught:
                future.result(5)
            self.assertEqual(caught.exception.code, 'STALE_SCOPE')
        current = self.saved(record['id'])
        self.assertEqual(current['revision'], 3)
        self.assertEqual(current['payload']['proposedNeeds']['budget'], 40)
        self.assertNotIn('result', current['payload'])

    def test_ba_t_04_new_answer_invalidates_an_inflight_recommendation(self):
        record = self.start()
        entered, release = threading.Event(), threading.Event()
        original = self.company.llm.propose
        def delayed(needs, evidence):
            entered.set(); self.assertTrue(release.wait(10))
            return original(needs, evidence)
        with patch.object(self.company.llm, 'propose', side_effect=delayed), ThreadPoolExecutor(1) as pool:
            future = pool.submit(self.confirm, record)
            try:
                self.assertTrue(entered.wait(5))
                latest = self.intake.clarify(CUSTOMER, record['id'],
                    {'contextRevision': 2, 'message': 'Correction: budget AUD 40.'})
                self.assertFalse(latest['payload'].get('needsConfirmed', False))
            finally:
                release.set()
            with self.assertRaises(DomainError) as caught:
                future.result(5)
            self.assertEqual(caught.exception.code, 'STALE_SCOPE')
        self.assertNotIn('result', self.saved(record['id'])['payload'])
        self.no_effects()

    def test_ba_t_03_confirmation_rechecks_catalogue_after_actual_provider_work(self):
        record = self.start()
        original = self.company.llm.propose
        def changed(needs, evidence):
            with self.company.store.transaction() as db:
                db.execute("UPDATE products SET stock=0,version=2 WHERE id='P-101'")
            return original(needs, evidence)
        with patch.object(self.company.llm, 'propose', side_effect=changed):
            result = self.confirm(record)
        self.assertEqual(result['status'], 'INCOMPLETE')
        self.assertEqual(result['payload']['result']['errorCode'], 'LLM_STALE_EVIDENCE')
        self.assertNotIn('product', result['payload']['result'])

    def test_ba_t_07_other_customer_and_founder_cannot_continue_or_confirm(self):
        record = self.start()
        for actor, code in ((OTHER, 'NOT_FOUND'), (FOUNDER, 'FORBIDDEN')):
            for operation, data in ((self.intake.clarify, {'message': 'Budget AUD 50', 'contextRevision': 1}),
                                    (self.intake.confirm, {**CONFIRM, 'contextRevision': 1})):
                with self.subTest(actor=actor.id, operation=operation.__name__), self.assertRaises(DomainError) as caught:
                    operation(actor, record['id'], data)
                self.assertEqual(caught.exception.code, code)
        self.assertEqual(self.saved(record['id'])['revision'], 1)

    def test_ba_t_07_old_revision_duplicate_confirmation_and_completed_resume_refused(self):
        record = self.start(); completed = self.confirm(record)
        with patch.object(self.company.llm, 'propose') as propose:
            for rev in (1, completed['revision']):
                with self.assertRaises(DomainError):
                    self.intake.confirm(CUSTOMER, record['id'], {**CONFIRM, 'contextRevision': rev})
            propose.assert_not_called()
        with self.assertRaises(DomainError):
            self.intake.clarify(CUSTOMER, record['id'], {'message': 'Budget AUD 50', 'contextRevision': completed['revision']})

    def test_ba_t_05_medical_stop_calls_no_provider(self):
        with patch.object(self.company.llm, 'extract_needs') as extract, patch.object(self.company.llm, 'propose') as propose:
            record = self.start('Please diagnose and treat eczema.')
            self.assertEqual(record['status'], 'INCOMPLETE')
            self.assertEqual(record['payload']['errorCode'], 'MEDICAL_SCOPE')
            extract.assert_not_called(); propose.assert_not_called()

    def test_ba_t_04_hallucinated_fields_sources_and_invalid_schema_withheld(self):
        valid = mock_extract([FULL])
        for bad in (None, [], {**valid, 'approve': True}, {**valid, 'budget': 99},
                    {**valid, 'fragranceFree': 'false'}, {**valid, 'concern': 'MEDICAL'},
                    {**valid, 'sources': {**valid['sources'], 'budget': 'Budget AUD 99'}},
                    {**valid, 'budget': True}, {**valid, 'budget': float('nan')}):
            with self.subTest(bad=bad), patch.object(self.company.llm, 'extract_needs', return_value=bad):
                record = self.start()
                self.assertEqual(record['status'], 'INCOMPLETE')
                self.assertEqual(record['payload']['errorCode'], 'LLM_INVALID_OUTPUT')
                self.assertNotIn('result', record['payload'])
        self.no_effects()

    def test_ba_t_04_provider_cannot_forge_sources_by_mutating_its_message_list(self):
        def mutate(messages):
            messages.append(FULL)
            return mock_extract([FULL])
        with patch.object(self.company.llm, 'extract_needs', side_effect=mutate):
            record = self.start('Something for my skin.')
        self.assertEqual(record['status'], 'INCOMPLETE')
        self.assertEqual(record['payload']['messages'], ['Something for my skin.'])

    def test_ba_t_03_live_failure_is_retained_without_a_mock_fallback(self):
        self.company.llm.ba_simulated = False
        with patch.object(self.company.llm, 'extract_needs', side_effect=ModelError('Unavailable', 503, 'LLM_UNAVAILABLE')):
            record = self.start()
        self.assertEqual(record['status'], 'INCOMPLETE')
        self.assertFalse(record['payload']['simulated'])
        self.assertEqual(self.saved(record['id'])['payload']['errorCode'], 'LLM_UNAVAILABLE')
        reply = self.intake.clarify(CUSTOMER, record['id'], {'message': 'Budget AUD 60', 'contextRevision': 1})
        self.assertEqual(reply['id'], record['id'])
        self.assertEqual(reply['status'], 'CLARIFYING')

    def test_ba_t_03_missing_optional_extraction_capability_is_not_silently_mocked(self):
        class Legacy:
            simulated = False
            def propose(self, needs, evidence):
                raise AssertionError('No recommendation before interpretation')
        self.company.ba.llm = Legacy()
        record = self.start()
        self.assertEqual(record['payload']['errorCode'], 'LLM_CAPABILITY_UNAVAILABLE')
        self.assertFalse(record['payload']['simulated'])

    def test_ba_t_07_result_save_failure_cannot_report_completed(self):
        record = self.start(); original = Store.save
        def fail_completed(db, item):
            if item['status'] == 'COMPLETED':
                raise sqlite3.OperationalError('PRIVATE_DATABASE_PATH')
            return original(db, item)
        with patch.object(Store, 'save', side_effect=fail_completed), self.assertRaises(sqlite3.OperationalError):
            self.confirm(record)
        saved = self.saved(record['id'])
        self.assertEqual(saved['status'], 'ACTIVE')
        self.assertNotIn('result', saved['payload'])
        self.no_effects()

    def test_ba_t_07_message_limits_invalid_inputs_and_unknown_fields_preserve_record(self):
        record = self.start('Something for my skin.')
        for data in ({'contextRevision': True, 'message': 'Budget AUD 60'},
                     {'contextRevision': 1, 'message': ''}, {'contextRevision': 1, 'message': 'x'*2001},
                     {'contextRevision': 1, 'message': 'Budget AUD 60', 'owner_id': 'customer-2'}):
            with self.subTest(data=data), self.assertRaises(DomainError):
                self.intake.clarify(CUSTOMER, record['id'], data)
        self.assertEqual(self.saved(record['id'])['revision'], 1)
        for _ in range(7):
            record=self.intake.clarify(CUSTOMER, record['id'], {'contextRevision': record['revision'], 'message': 'Please clarify.'})
        with self.assertRaises(DomainError) as caught:
            self.intake.clarify(CUSTOMER, record['id'], {'contextRevision': record['revision'], 'message': 'One more.'})
        self.assertEqual(caught.exception.code, 'CONVERSATION_LIMIT')

    def test_ba_t_01_actual_router_requires_session_csrf_and_customer(self):
        router=Router(self.company)
        base={'Host':'127.0.0.1:5620','Content-Type':'application/json'}
        body=json.dumps({'message':FULL}).encode()
        self.assertEqual(router.handle('POST','/api/consultations/intake',base,body).status,401)
        for username, expected in (('founder',403),('customer',201)):
            token,csrf,_=self.company.login(username,username+'-demo')
            headers={**base,'Cookie':'beauty_session='+token,'X-CSRF-Token':csrf}
            result=router.handle('POST','/api/consultations/intake',headers,body)
            self.assertEqual(result.status,expected)
            self.assertEqual(router.handle('POST','/api/consultations/intake',
                                          {**headers,'X-CSRF-Token':'wrong'},body).status,403)
            if expected==201:
                record=json.loads(result.body)
                response=router.handle('POST',f"/api/consultations/{record['id']}/confirm-needs",headers,
                                       json.dumps({'contextRevision':1,**CONFIRM}).encode())
                self.assertEqual(json.loads(response.body)['status'],'COMPLETED')


class BaExtractionTransportTests(unittest.TestCase):
    def setUp(self):
        self.llm=StrataLlm(LlmConfig('http://127.0.0.1:8080/v1','test-model'))

    def response(self,value):
        data={'model':'test-model','choices':[{'finish_reason':'stop','message':{'content':json.dumps(value)}}]}
        stream=io.BytesIO(json.dumps(data).encode()); stream.status=200
        return stream

    def test_ba_t_01_extraction_uses_shared_transport_with_only_customer_messages(self):
        reply=mock_extract([FULL])
        with patch.object(self.llm.opener,'open',return_value=self.response(reply)) as send:
            result=self.llm.extract_needs([FULL])
        self.assertEqual(result['budget'],60)
        body=json.loads(send.call_args[0][0].data)
        self.assertEqual(json.loads(body['messages'][1]['content']),{'messages':[FULL]})
        self.assertIn('Customer must',body['messages'][0]['content'])
        self.assertFalse(body['chat_template_kwargs']['enable_thinking'])

    def test_ba_t_04_transport_rejects_invalid_needs_or_unsupported_currency(self):
        source='Dry skin. Budget USD 60. Fragrance-free.'
        valid=mock_extract([FULL])
        bad={**valid,'sources':{'concern':'Dry skin','budget':'Budget USD 60','fragranceFree':'Fragrance-free'}}
        for value,messages in (({'productId':'P-101','factRefs':[]},[FULL]),(bad,[source])):
            with self.subTest(value=value), patch.object(self.llm.opener,'open',return_value=self.response(value)), self.assertRaises(ModelError) as caught:
                self.llm.extract_needs(messages)
            self.assertEqual(caught.exception.code,'LLM_INVALID_OUTPUT')

    def test_ba_t_04_no_value_can_exist_without_its_literal_customer_source(self):
        value=mock_extract([FULL])
        for key in ('concern','budget','fragranceFree'):
            bad={**value,'sources':{**value['sources'],key:None}}
            with self.subTest(key=key),self.assertRaises(ValueError):
                validate_extraction(bad,[FULL])
