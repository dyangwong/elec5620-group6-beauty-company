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
        with patch.object(Store, 'save', side_effect=fail_completed), self.assertRaises(DomainError) as caught:
            self.confirm(record)
        self.assertEqual(caught.exception.code, 'BA_STORAGE_UNAVAILABLE')
        self.assertNotIn('PRIVATE_DATABASE_PATH', str(caught.exception))
        saved = self.saved(record['id'])
        self.assertEqual(saved['status'], 'INCOMPLETE')
        self.assertEqual(saved['payload']['pendingOutcome']['kind'], 'ADVICE')
        self.assertNotIn('result', saved['payload'])
        with patch.object(self.company.llm, 'propose', side_effect=AssertionError('Recovery must not infer')):
            recovered = self.intake.recover(CUSTOMER, record['id'], {'contextRevision': saved['revision']})
        self.assertEqual(recovered['status'], 'COMPLETED')
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

    def fail_advice_recording(self, message=FULL):
        self.company.set_fault(FOUNDER, 'ba_recording')
        record = self.start(message)
        with self.assertRaises(DomainError) as caught:
            self.confirm(record)
        self.assertEqual(caught.exception.code, 'BA_RECORDING_FAILED')
        return self.saved(record['id'])

    def test_ba_t_07_completed_revision_preserves_history_and_replaces_scope(self):
        final = self.confirm(self.start())
        revised = self.intake.revise(CUSTOMER, final['id'], {'contextRevision': final['revision'],
                                                             'message': 'Gentle cleansing.'})
        self.assertEqual((revised['id'], revised['revision'], revised['status']), (final['id'], 3, 'CLARIFYING'))
        self.assertIsNone(revised['payload']['proposedNeeds']['budget'])
        self.assertNotIn('needsConfirmed', revised['payload'])
        self.assertNotIn('result', revised['payload'])
        self.assertEqual(revised['payload']['messages'], ['Gentle cleansing.'])
        old = revised['payload']['history'][-1]
        self.assertEqual(old['status'], 'COMPLETED')
        self.assertEqual(old['result']['product']['id'], 'P-101')
        self.assertEqual(old['needs']['budget'], 6000)
        ready = self.intake.clarify(CUSTOMER, final['id'], {'contextRevision': 3,
                                        'message': 'Budget AUD 40. Fragrance-free required.'})
        new = self.confirm(ready, concern='CLEANSING', budget=40)
        self.assertEqual(new['payload']['result']['product']['id'], 'P-102')
        self.no_effects()

    def test_ba_t_07_cancel_persists_is_idempotent_and_requires_fresh_session(self):
        record = self.start('Dry skin.')
        cancelled = self.intake.cancel(CUSTOMER, record['id'], {'contextRevision': 1})
        self.assertEqual((cancelled['status'], cancelled['revision']), ('CANCELLED', 2))
        self.company = Company(self.path); self.intake = self.company.ba_intake
        self.assertEqual(self.intake.cancel(CUSTOMER, record['id'], {'contextRevision': 2})['revision'], 2)
        for operation, data in [('clarify', {'message': FULL}), ('revise', {'message': FULL}),
                                ('retry', {}), ('recover', {}), ('confirm', CONFIRM)]:
            with self.subTest(operation=operation), self.assertRaises(DomainError):
                getattr(self.intake, operation)(CUSTOMER, record['id'], {'contextRevision': 2, **data})
        with self.assertRaises(DomainError) as caught:
            self.intake.cancel(CUSTOMER, record['id'], {'contextRevision': 1})
        self.assertEqual(caught.exception.code, 'STALE_SCOPE')
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE event='CONSULTATION_CANCELLED'").fetchone()[0], 1)
        self.assertNotEqual(self.start()['id'], record['id'])
        self.no_effects()

    def test_ba_t_07_completed_advice_cannot_be_retroactively_cancelled(self):
        final = self.confirm(self.start())
        with self.assertRaises(DomainError) as caught:
            self.intake.cancel(CUSTOMER, final['id'], {'contextRevision': final['revision']})
        self.assertEqual(caught.exception.code, 'INVALID_STATE')
        self.assertEqual(self.saved(final['id'])['payload']['result'], final['payload']['result'])

    def test_ba_t_07_cancel_suppresses_delayed_extraction(self):
        record = self.start('Dry skin.')
        entered, release = threading.Event(), threading.Event()
        def delayed(messages):
            entered.set(); self.assertTrue(release.wait(10))
            return mock_extract(messages)
        with patch.object(self.company.llm, 'extract_needs', side_effect=delayed), ThreadPoolExecutor(1) as pool:
            future = pool.submit(self.intake.clarify, CUSTOMER, record['id'],
                                 {'contextRevision': 1, 'message': 'Budget AUD 60. Fragrance-free required.'})
            try:
                self.assertTrue(entered.wait(5))
                cancelled = self.intake.cancel(CUSTOMER, record['id'], {'contextRevision': 2})
                self.assertEqual(cancelled['status'], 'CANCELLED')
            finally: release.set()
            with self.assertRaises(DomainError) as caught: future.result(5)
            self.assertEqual(caught.exception.code, 'STALE_SCOPE')
        saved = self.saved(record['id'])
        self.assertEqual(saved['status'], 'CANCELLED')
        self.assertNotIn('result', saved['payload'])
        self.assertNotIn('pendingOutcome', saved['payload'])
        self.no_effects()

    def test_ba_t_07_cancel_suppresses_delayed_recommendation(self):
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
                self.intake.cancel(CUSTOMER, record['id'], {'contextRevision': 2})
            finally: release.set()
            with self.assertRaises(DomainError) as caught: future.result(5)
            self.assertEqual(caught.exception.code, 'STALE_SCOPE')
        self.assertEqual(self.saved(record['id'])['status'], 'CANCELLED')
        self.assertNotIn('result', self.saved(record['id'])['payload'])
        self.no_effects()

    def test_ba_t_07_revision_supersedes_inflight_advice(self):
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
                current = self.intake.revise(CUSTOMER, record['id'], {'contextRevision': 2,
                    'message': 'Gentle cleansing. Budget AUD 40. Fragrance-free required.'})
            finally: release.set()
            with self.assertRaises(DomainError) as caught: future.result(5)
            self.assertEqual(caught.exception.code, 'STALE_SCOPE')
        self.assertEqual(self.saved(record['id'])['revision'], current['revision'])
        self.assertNotIn('result', current['payload'])
        self.assertEqual(current['payload']['proposedNeeds']['concern'], 'CLEANSING')

    def test_ba_t_07_new_operations_enforce_owner_and_exact_inputs(self):
        record = self.fail_advice_recording()
        for operation in ('revise', 'cancel', 'recover', 'retry'):
            data = {'contextRevision': record['revision'], **({'message': FULL} if operation == 'revise' else {})}
            for actor, status in ((OTHER, 404), (FOUNDER, 403)):
                with self.subTest(operation=operation, actor=actor.id), self.assertRaises(DomainError) as caught:
                    getattr(self.intake, operation)(actor, record['id'], data)
                self.assertEqual(caught.exception.status, status)
            for bad in ({**data, 'contextRevision': True}, {**data, 'result': {'productId': 'FORGED'}},
                        {**data, 'contextRevision': record['revision']-1}):
                with self.subTest(operation=operation, bad=bad), self.assertRaises(DomainError):
                    getattr(self.intake, operation)(CUSTOMER, record['id'], bad)
        self.assertEqual(self.saved(record['id'])['status'], 'INCOMPLETE')

    def test_ba_t_07_recovery_survives_restart_and_never_repeats_inference(self):
        record = self.fail_advice_recording()
        self.assertNotIn('result', record['payload'])
        self.company = Company(self.path); self.intake = self.company.ba_intake
        with patch.object(self.company.llm, 'propose', side_effect=AssertionError('No inference')), \
                patch.object(self.company.llm, 'extract_needs', side_effect=AssertionError('No extraction')):
            for _ in range(3):
                recovered = self.intake.recover(CUSTOMER, record['id'], {'contextRevision': record['revision']})
                self.assertEqual(recovered['status'], 'COMPLETED')
                self.assertEqual(recovered['revision'], record['revision'])
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE entity_id=? AND event='CONFIRMED_ADVICE_RECORDED'", (record['id'],)).fetchone()[0], 1)
        self.no_effects()

    def test_ba_t_07_snapshot_hides_uncommitted_advice_draft_for_both_roles(self):
        record = self.fail_advice_recording()
        self.assertIn('product', record['payload']['pendingOutcome']['value'])
        for actor in (CUSTOMER, FOUNDER):
            visible = next(r for r in self.company.snapshot(actor)['records'] if r['id'] == record['id'])
            self.assertEqual(set(visible['payload']['pendingOutcome']), {'kind', 'revision', 'simulated'})
            self.assertNotIn('result', visible['payload'])
            self.assertNotIn('Daily Hydration Cream', json.dumps(visible))

    def test_ba_t_07_recovered_live_label_survives_mock_restart(self):
        self.company.llm.ba_simulated = False  # Explicit fake capability; this is not actual model evidence.
        record = self.fail_advice_recording()
        self.company = Company(self.path); self.intake = self.company.ba_intake
        result = self.intake.recover(CUSTOMER, record['id'], {'contextRevision': record['revision']})
        self.assertFalse(result['payload']['simulated'])
        self.assertFalse(result['payload']['result']['simulated'])
        revised = self.intake.revise(CUSTOMER, result['id'], {'contextRevision': result['revision'], 'message': FULL})
        self.assertTrue(revised['payload']['simulated'])

    def test_ba_t_03_recovery_rechecks_current_stock_without_new_model_call(self):
        record = self.fail_advice_recording()
        with self.company.store.transaction() as db:
            db.execute("UPDATE products SET stock=0,version=2 WHERE id='P-101'")
        with patch.object(self.company.llm, 'propose', side_effect=AssertionError('No inference')):
            result = self.intake.recover(CUSTOMER, record['id'], {'contextRevision': record['revision']})
        self.assertEqual(result['status'], 'INCOMPLETE')
        self.assertEqual(result['payload']['result']['errorCode'], 'LLM_STALE_EVIDENCE')
        self.assertNotIn('product', result['payload']['result'])
        self.assertNotIn('pendingOutcome', result['payload'])

    def test_ba_t_07_old_draft_cannot_be_recovered_after_revision_or_cancellation(self):
        for operation in ('revise', 'cancel'):
            record = self.fail_advice_recording()
            data = {'contextRevision': record['revision'], **({'message': 'Cleansing.'} if operation == 'revise' else {})}
            current = getattr(self.intake, operation)(CUSTOMER, record['id'], data)
            with self.assertRaises(DomainError) as caught:
                self.intake.recover(CUSTOMER, record['id'], {'contextRevision': record['revision']})
            self.assertEqual(caught.exception.code, 'STALE_SCOPE')
            self.assertNotIn('pendingOutcome', current['payload'])
            self.assertNotIn('result', current['payload'])

    def test_ba_t_07_concurrent_recovery_records_one_advice_event(self):
        record = self.fail_advice_recording()
        with ThreadPoolExecutor(2) as pool:
            futures = [pool.submit(self.intake.recover, CUSTOMER, record['id'],
                                   {'contextRevision': record['revision']}) for _ in range(2)]
            self.assertTrue(all(future.result(10)['status'] == 'COMPLETED' for future in futures))
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE entity_id=? AND event='CONFIRMED_ADVICE_RECORDED'", (record['id'],)).fetchone()[0], 1)
        self.no_effects()

    def test_ba_t_07_missing_durable_draft_requires_explicit_retry(self):
        record = self.start(); original = Store.save
        def fail_stage(db, item):
            if item['payload'].get('pendingOutcome'):
                raise sqlite3.OperationalError('PRIVATE_STAGE_PATH')
            return original(db, item)
        with patch.object(Store, 'save', side_effect=fail_stage), self.assertRaises(DomainError) as caught:
            self.confirm(record)
        self.assertEqual(caught.exception.code, 'BA_STORAGE_UNAVAILABLE')
        saved = self.saved(record['id'])
        self.assertEqual(saved['status'], 'ACTIVE')
        self.assertNotIn('pendingOutcome', saved['payload'])
        with self.assertRaises(DomainError) as caught:
            self.intake.recover(CUSTOMER, record['id'], {'contextRevision': saved['revision']})
        self.assertEqual(caught.exception.code, 'NO_PENDING_RESULT')
        with patch.object(self.company.llm, 'propose', side_effect=AssertionError('Confirmation required')):
            retried = self.intake.retry(CUSTOMER, record['id'], {'contextRevision': saved['revision']})
        self.assertEqual(retried['status'], 'CLARIFYING')
        self.assertNotIn('needsConfirmed', retried['payload'])

    def test_ba_t_07_final_and_failure_writes_both_unavailable_preserve_active_draft(self):
        record = self.start(); original = Store.save; staged = False
        def unavailable(db, item):
            nonlocal staged
            if staged: raise sqlite3.OperationalError('DISK_UNAVAILABLE')
            result = original(db, item)
            if item['payload'].get('pendingOutcome'): staged = True
            return result
        with patch.object(Store, 'save', side_effect=unavailable), self.assertRaises(DomainError) as caught:
            self.confirm(record)
        self.assertEqual(caught.exception.code, 'BA_STORAGE_UNAVAILABLE')
        saved = self.saved(record['id'])
        self.assertEqual(saved['status'], 'ACTIVE')
        self.assertIn('pendingOutcome', saved['payload'])
        self.assertNotIn('result', saved['payload'])
        self.company = Company(self.path); self.intake = self.company.ba_intake
        self.assertEqual(self.intake.recover(CUSTOMER, saved['id'], {'contextRevision': saved['revision']})['status'], 'COMPLETED')

    def test_ba_t_07_failed_interpretation_save_recovers_only_questions_not_advice(self):
        original = Store.save
        def fail_clarifying(db, item):
            if item['status'] == 'CLARIFYING': raise sqlite3.OperationalError('WRITE_FAILED')
            return original(db, item)
        with patch.object(Store, 'save', side_effect=fail_clarifying), self.assertRaises(DomainError):
            self.start()
        with self.company.store.read() as db:
            rid = db.execute("SELECT id FROM records WHERE kind='BA'").fetchone()[0]
        with patch.object(self.company.llm, 'propose', side_effect=AssertionError('Needs not confirmed')):
            result = self.intake.recover(CUSTOMER, rid, {'contextRevision': 1})
        self.assertEqual(result['status'], 'CLARIFYING')
        self.assertTrue(result['payload']['needsReady'])
        self.assertNotIn('result', result['payload'])

    def test_ba_t_07_failed_cancel_is_not_reported_as_cancelled(self):
        record = self.start('Dry skin.'); original = Store.save
        def fail_cancel(db, item):
            if item['status'] == 'CANCELLED': raise sqlite3.OperationalError('PRIVATE_CANCEL_PATH')
            return original(db, item)
        with patch.object(Store, 'save', side_effect=fail_cancel), self.assertRaises(DomainError) as caught:
            self.intake.cancel(CUSTOMER, record['id'], {'contextRevision': 1})
        self.assertEqual(caught.exception.code, 'BA_CANCELLATION_NOT_RECORDED')
        self.assertNotIn('PRIVATE_CANCEL_PATH', str(caught.exception))
        self.assertEqual((self.saved(record['id'])['status'], self.saved(record['id'])['revision']), ('CLARIFYING', 1))

    def test_ba_t_07_actual_sqlite_audit_failure_rolls_back_result_and_recovers_once(self):
        record = self.start()
        with self.company.store.transaction() as db:
            db.execute("""CREATE TRIGGER reject_ba_final_audit BEFORE INSERT ON events
                          WHEN NEW.event='CONFIRMED_ADVICE_RECORDED'
                          BEGIN SELECT RAISE(ABORT,'PRIVATE_AUDIT_STORAGE_FAILURE'); END""")
        with self.assertRaises(DomainError) as caught:
            self.confirm(record)
        self.assertEqual(caught.exception.code, 'BA_STORAGE_UNAVAILABLE')
        self.assertNotIn('PRIVATE_AUDIT_STORAGE_FAILURE', str(caught.exception))
        saved = self.saved(record['id'])
        self.assertEqual(saved['status'], 'INCOMPLETE')
        self.assertNotIn('result', saved['payload'])
        self.assertEqual(saved['payload']['pendingOutcome']['kind'], 'ADVICE')
        with self.company.store.transaction() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE event='CONFIRMED_ADVICE_RECORDED'").fetchone()[0], 0)
            db.execute('DROP TRIGGER reject_ba_final_audit')  # Only this test's isolated temporary database.
        with patch.object(self.company.llm, 'propose', side_effect=AssertionError('No repeat model call')):
            result = self.intake.recover(CUSTOMER, saved['id'], {'contextRevision': saved['revision']})
        self.assertEqual(result['status'], 'COMPLETED')
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE event='CONFIRMED_ADVICE_RECORDED'").fetchone()[0], 1)
        self.no_effects()

    def test_ba_t_03_retry_is_explicit_and_refuses_saved_draft(self):
        with patch.object(self.company.llm, 'extract_needs', side_effect=ModelError('Unavailable', 503, 'LLM_UNAVAILABLE')):
            record = self.start()
        ready = self.intake.retry(CUSTOMER, record['id'], {'contextRevision': 1})
        self.assertEqual((ready['id'], ready['revision'], ready['status']), (record['id'], 2, 'CLARIFYING'))
        failed = self.fail_advice_recording()
        with self.assertRaises(DomainError) as caught:
            self.intake.retry(CUSTOMER, failed['id'], {'contextRevision': failed['revision']})
        self.assertEqual(caught.exception.code, 'RECOVERY_AVAILABLE')

    def test_ba_t_04_invalid_saved_draft_never_becomes_success(self):
        for mutate in (lambda p: p.update(revision=True), lambda p: p.update(value=[]),
                       lambda p: p.update(kind='APPROVE'), lambda p: p.update(simulated='false')):
            record = self.fail_advice_recording()
            with self.company.store.transaction() as db:
                saved = Store.get(db, record['id']); mutate(saved['payload']['pendingOutcome']); Store.save(db, saved)
            with self.assertRaises(DomainError) as caught:
                self.intake.recover(CUSTOMER, record['id'], {'contextRevision': record['revision']})
            self.assertEqual(caught.exception.code, 'INVALID_SAVED_RESULT')
            self.assertNotIn('result', self.saved(record['id'])['payload'])

    def test_ba_t_04_recovery_independently_withholds_unsupported_saved_facts(self):
        record = self.fail_advice_recording()
        with self.company.store.transaction() as db:
            saved = Store.get(db, record['id'])
            saved['payload']['pendingOutcome']['value']['reasons'] = ['Invented medical cure']
            Store.save(db, saved)
        result = self.intake.recover(CUSTOMER, record['id'], {'contextRevision': record['revision']})
        self.assertEqual(result['status'], 'INCOMPLETE')
        self.assertNotIn('product', result['payload']['result'])

    def test_ba_t_07_lifecycle_http_routes_require_session_csrf_and_customer(self):
        record = self.start('Dry skin.'); router = Router(self.company)
        token, csrf, _ = self.company.login('customer', 'customer-demo')
        base = {'Host': '127.0.0.1:5620', 'Content-Type': 'application/json'}
        for operation in ('revise', 'cancel', 'recover', 'retry'):
            route = '/api/consultations/'+record['id']+'/'+operation
            data = {'contextRevision': 1, **({'message': FULL} if operation == 'revise' else {})}
            body = json.dumps(data).encode()
            self.assertEqual(router.handle('POST', route, base, body).status, 401)
            self.assertEqual(router.handle('POST', route, {**base, 'Cookie': 'beauty_session='+token}, body).status, 403)
        response = router.handle('POST', '/api/consultations/'+record['id']+'/cancel',
            {**base, 'Cookie': 'beauty_session='+token, 'X-CSRF-Token': csrf}, json.dumps({'contextRevision': 1}).encode())
        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(response.body)['status'], 'CANCELLED')

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



class BaConditionalReviewTests(unittest.TestCase):
    # Reuse fixture helpers, not inherited tests (loader below uses an independent class).
    def unresolved(self):
        record = self.start()
        with patch.object(self.company.llm, 'propose', return_value={'productId': 'invented'}):
            return self.confirm(record)

    def request_review(self, record, **changes):
        return self.company.ba_review.request(CUSTOMER, record['id'], {
            'contextRevision': record['revision'], 'consent': True,
            'issue': 'Please review the unresolved product match.', **changes})

    def decision(self, record, kind='APPROVE'):
        return self.company.decide(FOUNDER, record['payload']['approvalId'], {
            'contextRevision': record['revision'], 'decision': kind, 'reason': 'Synthetic scope-only test.'})

    def assert_no_commerce(self):
        with self.company.store.read() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM effects').fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-101'").fetchone()[0], 12)
            self.assertEqual(db.execute("SELECT product_id FROM orders WHERE id='ORD-1001'").fetchone()[0], 'P-103')

    def test_review_routine_advice_never_needs_ap(self):
        record = self.confirm(self.start())
        self.assertEqual(record['status'], 'COMPLETED')
        with self.assertRaises(DomainError) as caught:
            self.request_review(record)
        self.assertEqual(caught.exception.code, 'REVIEW_NOT_AVAILABLE')
        self.no_effects()

    def test_review_consent_scope_owner_and_input_are_enforced(self):
        record = self.unresolved()
        for consent in (False, None, 1, 'true'):
            with self.subTest(consent=consent), self.assertRaises(DomainError) as caught:
                self.request_review(record, consent=consent)
            self.assertEqual(caught.exception.code, 'CONSENT_REQUIRED')
        for actor in (OTHER, FOUNDER):
            with self.assertRaises(DomainError):
                self.company.ba_review.request(actor, record['id'], {
                    'contextRevision':record['revision'],'consent':True,'issue':'Product question'})
        with self.assertRaises(DomainError):
            self.request_review(record, approvalId='injected')
        with self.assertRaises(DomainError):
            self.request_review(record, contextRevision=1)
        self.no_effects()

    def test_review_receipt_is_minimal_pending_and_replay_once(self):
        record = self.unresolved()
        with patch.object(self.company.llm, 'propose') as model:
            pending = self.request_review(record)
            again = self.request_review(pending)
            self.assertEqual(again['payload']['approvalId'], pending['payload']['approvalId'])
            model.assert_not_called()
        self.assertEqual(pending['status'], 'REVIEW_PENDING')
        with self.company.store.read() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0], 1)
            review = self.company.ap.get(db, pending['payload']['approvalId'])
            self.assertEqual(set(review['evidence']), {'needs','issue','outcomeCode','adviceSimulated'})
            self.assertNotIn('invented', json.dumps(review))
            self.assertNotIn(FULL, json.dumps(review))
            self.assertIsNone(review['decision_id'])
        with self.assertRaises(DomainError):
            self.confirm(pending)
        self.assert_no_commerce()

    def test_review_missing_needs_draft_and_medical_cannot_escalate(self):
        missing = self.start('Hydration please.')
        with self.assertRaises(DomainError):
            self.request_review(missing)
        medical = self.start('Diagnose my skin. Budget AUD 60, fragrance-free.')
        with self.assertRaises(DomainError) as caught:
            self.request_review(medical)
        self.assertEqual(caught.exception.code, 'MEDICAL_SCOPE')
        record=self.unresolved()
        with self.assertRaises(DomainError) as caught:
            self.request_review(record, issue='Please diagnose my skin')
        self.assertEqual(caught.exception.code,'MEDICAL_SCOPE')
        with self.company.store.transaction() as db:
            item=Store.get(db, record['id']); item['payload']['pendingOutcome']={'kind':'ADVICE'}; Store.save(db,item)
        with self.assertRaises(DomainError):
            self.request_review(item)
        self.no_effects()

    def test_review_unavailable_has_no_receipt_or_pending_state(self):
        record=self.unresolved()
        with patch.object(self.company.ap, 'submit', side_effect=OSError('private service failure')):
            with self.assertRaises(DomainError) as caught:
                self.request_review(record)
        self.assertEqual(caught.exception.code, 'BA_REVIEW_UNAVAILABLE')
        self.assertNotIn('private',str(caught.exception))
        self.assertEqual(self.saved(record['id'])['status'],'INCOMPLETE')
        self.no_effects()

    def test_review_receipt_and_origin_save_are_atomic(self):
        record=self.unresolved()
        with self.company.store.transaction() as db:
            db.execute("CREATE TRIGGER fail_review_audit BEFORE INSERT ON events WHEN NEW.event='REVIEW_ACKNOWLEDGED' BEGIN SELECT RAISE(ABORT,'test write failure'); END")
        with self.assertRaises(DomainError) as caught:
            self.request_review(record)
        self.assertEqual(caught.exception.code,'BA_REVIEW_UNAVAILABLE')
        self.assertNotIn('approvalId',self.saved(record['id'])['payload'])
        self.no_effects()

    def test_review_approve_only_reopens_confirmation_fresh_model_and_stock(self):
        record=self.request_review(self.unresolved())
        with patch.object(self.company.llm,'propose',wraps=self.company.llm.propose) as model:
            self.decision(record)
            self.assertEqual(model.call_count,0)
            approved=self.saved(record['id'])
            self.assertEqual(approved['status'],'CLARIFYING')
            self.assertEqual(approved['payload']['result']['status'],'INCOMPLETE')
            final=self.confirm(approved)
            self.assertEqual(final['status'],'COMPLETED')
            self.assertEqual(model.call_count,1)
        self.assertGreater(final['revision'],record['revision'])
        self.assertNotIn('approvalId',final['payload'])
        self.assertEqual(final['payload']['history'][-1]['decision'],'APPROVE')
        self.assert_no_commerce()

    def test_review_approval_cannot_override_no_stock_or_invalid_output(self):
        record=self.request_review(self.unresolved()); self.decision(record)
        with self.company.store.transaction() as db:
            db.execute("UPDATE products SET stock=0 WHERE id='P-101'")
        final=self.confirm(self.saved(record['id']))
        self.assertEqual(final['status'],'INCOMPLETE')
        self.assertNotIn('product',final['payload']['result'])
        again=self.request_review(final); self.decision(again)
        with patch.object(self.company.llm,'propose',return_value={'productId':'invented','factRefs':['cures disease']}):
            final=self.confirm(self.saved(record['id']))
        self.assertEqual(final['status'],'INCOMPLETE')
        self.assertNotIn('product',final['payload']['result'])

    def test_review_approved_model_unavailable_retains_live_failure(self):
        record=self.request_review(self.unresolved()); self.decision(record)
        self.company.llm.ba_simulated=False
        with patch.object(self.company.llm,'propose',side_effect=ModelError('Unavailable',503,'LLM_UNAVAILABLE')):
            final=self.confirm(self.saved(record['id']))
        self.assertEqual(final['status'],'INCOMPLETE')
        self.assertEqual(final['payload']['result']['errorCode'],'LLM_UNAVAILABLE')
        self.assertIs(final['payload']['result']['simulated'],False)
        self.assert_no_commerce()

    def test_review_reject_and_request_revision_never_enable_confirmation(self):
        for decision in ('REJECT','REQUEST_REVISION'):
            with self.subTest(decision=decision):
                record=self.request_review(self.unresolved()); self.decision(record,decision)
                current=self.saved(record['id'])
                self.assertEqual(current['status'],'INCOMPLETE' if decision=='REJECT' else 'CLARIFYING')
                with self.assertRaises(DomainError): self.confirm(current)
                revised=self.intake.revise(CUSTOMER,record['id'],{'contextRevision':record['revision'],'message':FULL})
                self.assertNotIn('approvalId',revised['payload'])
                self.assertEqual(self.confirm(revised)['status'],'COMPLETED')
        self.assert_no_commerce()

    def test_review_revoked_or_same_revision_source_change_refuses_decision(self):
        record=self.request_review(self.unresolved())
        with self.company.store.transaction() as db:
            current=Store.get(db,record['id']); current['payload']['needs']['budget']=1; Store.save(db,current)
        with self.assertRaises(DomainError) as caught: self.decision(record)
        self.assertEqual(caught.exception.code,'STALE_SCOPE')
        with self.company.store.read() as db:
            self.assertIsNone(self.company.ap.get(db,record['payload']['approvalId'])['decision_id'])
        self.assert_no_commerce()

    def test_review_cancel_or_revision_suppresses_old_delivery_and_recovery(self):
        for operation in ('cancel','revise'):
            with self.subTest(operation=operation):
                record=self.request_review(self.unresolved()); self.company.set_fault(FOUNDER,'approval_delivery')
                review=self.decision(record); self.assertEqual(review['delivery'],'FAILED')
                data={'contextRevision':record['revision']}
                if operation=='revise': data['message']=FULL
                current=getattr(self.intake,operation)(CUSTOMER,record['id'],data)
                old=self.company.redeliver(FOUNDER,review['id']); self.assertEqual(old['delivery'],'STALE')
                self.assertNotIn('decisionId',self.saved(record['id'])['payload'])
                self.assertNotEqual(current['status'],'COMPLETED')
        self.assert_no_commerce()

    def test_review_recording_recovery_delivery_and_duplicates_reuse_ap(self):
        record=self.request_review(self.unresolved()); self.company.set_fault(FOUNDER,'approval_recording')
        with self.assertRaises(DomainError) as caught: self.decision(record)
        self.assertEqual(caught.exception.code,'RECORDING_FAILED')
        self.assertEqual(self.saved(record['id'])['status'],'REVIEW_PENDING')
        self.company=Company(self.path); self.intake=self.company.ba_intake
        rid=record['payload']['approvalId']
        review=self.company.recover_decision(FOUNDER,rid,{'contextRevision':record['revision']})
        self.assertEqual(review['delivery'],'DELIVERED')
        for _ in range(3):
            self.assertEqual(self.company.redeliver(FOUNDER,rid)['decision_id'],review['decision_id'])
            self.assertEqual(self.company.recover_decision(FOUNDER,rid,{'contextRevision':record['revision']})['decision_id'],review['decision_id'])
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE event='DECISION_COMMITTED'").fetchone()[0],1)
        self.assert_no_commerce()

    def test_review_stale_failed_recording_intent_cannot_recover(self):
        record=self.request_review(self.unresolved()); self.company.set_fault(FOUNDER,'approval_recording')
        with self.assertRaises(DomainError): self.decision(record)
        self.intake.cancel(CUSTOMER,record['id'],{'contextRevision':record['revision']})
        with self.assertRaises(DomainError):
            self.company.recover_decision(FOUNDER,record['payload']['approvalId'],{'contextRevision':record['revision']})
        self.assert_no_commerce()

    def test_review_concurrent_requests_persist_one_receipt(self):
        record=self.unresolved()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(lambda _:self.request_review(record),range(2)))
        self.assertEqual(results[0]['payload']['approvalId'],results[1]['payload']['approvalId'])
        with self.company.store.read() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0],1)

    def test_review_reassessment_closes_db_during_model_and_rechecks_identity(self):
        from contextlib import contextmanager
        record=self.request_review(self.unresolved()); self.decision(record)
        original=self.company.store.read
        opened=[]
        @contextmanager
        def monitored():
            with original() as db:
                opened.append(True)
                try: yield db
                finally: opened.pop()
        def model(context,evidence):
            self.assertFalse(opened)
            with self.company.store.transaction() as db:
                db.execute("UPDATE users SET role='FOUNDER' WHERE id='customer'")
            return {'productId':'P-101','factRefs':['Fragrance-free']}
        with patch.object(self.company.store,'read',monitored),patch.object(self.company.llm,'propose',side_effect=model):
            with self.assertRaises(DomainError) as caught: self.confirm(self.saved(record['id']))
        self.assertEqual(caught.exception.code,'FORBIDDEN')
        self.assertEqual(self.saved(record['id'])['status'],'ACTIVE')
        self.assertNotIn('pendingOutcome',self.saved(record['id'])['payload'])
        self.assert_no_commerce()

    def test_review_http_session_csrf_scope_and_snapshot(self):
        record=self.unresolved(); router=Router(self.company)
        token,csrf,_=self.company.login('customer','customer-demo')
        headers={'Host':'127.0.0.1:5770','Content-Type':'application/json','Cookie':f'beauty_session={token}'}
        path=f"/api/consultations/{record['id']}/request-review"
        payload=json.dumps({'contextRevision':record['revision'],'consent':True,'issue':'Product question'}).encode()
        self.assertEqual(router.handle('POST',path,headers,payload).status,403)
        headers['X-CSRF-Token']=csrf
        response=router.handle('POST',path,headers,payload)
        self.assertEqual(response.status,200)
        self.assertEqual(json.loads(response.body)['status'],'REVIEW_PENDING')
        with self.company.store.transaction() as db: db.execute('DELETE FROM sessions')
        self.assertEqual(router.handle('POST',path,headers,payload).status,401)


for _helper in ('setUp','start','confirm','saved','no_effects'):
    setattr(BaConditionalReviewTests, _helper, getattr(BaNeedsTests, _helper))


class BaStructuredLifecycleTests(unittest.TestCase):
    """KAN-10 legacy explicit-field parity; all providers/data are isolated fakes."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'structured.sqlite3'
        self.company = Company(self.path)
        self.fields = {'message': 'Hydration please', **CONFIRM}

    def saved(self, rid):
        with self.company.store.read() as db:
            return Store.get(db, rid, 'BA')

    def assert_no_effects(self):
        with self.company.store.read() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM effects').fetchone()[0], 0)
            self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0], 0)
            self.assertEqual([r[0] for r in db.execute('SELECT stock FROM products ORDER BY id')], [12, 8, 0])

    def test_ba_t_01_structured_resume_same_id_after_restart_rechecks_evidence(self):
        with patch.object(self.company.llm, 'propose') as provider:
            record = self.company.consult(CUSTOMER, {'message': 'Hydration please', 'concern': 'HYDRATION'})
            provider.assert_not_called()
        self.assertEqual(record['status'], 'CLARIFYING')
        self.assertNotIn('needs', record['payload'])
        self.company = Company(self.path)
        with self.company.store.transaction() as db:
            db.execute("UPDATE products SET stock=0,version=version+1 WHERE id='P-101'")
        final = self.company.consult(CUSTOMER, {'contextRevision': 1, 'budget': 60, 'fragranceFree': True}, record['id'])
        self.assertEqual((final['id'], final['revision'], final['status']), (record['id'], 2, 'INCOMPLETE'))
        self.assertNotIn('product', final['payload']['result'])
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM records WHERE kind='BA'").fetchone()[0], 1)

    def test_ba_t_07_structured_replacement_invalidates_advice_and_never_inherits_constraints(self):
        first = self.company.consult(CUSTOMER, self.fields)
        revised = self.company.revise_consultation(CUSTOMER, first['id'], {'contextRevision': 1, 'message': 'Cleansing please'})
        self.assertEqual((revised['revision'], revised['status']), (2, 'CLARIFYING'))
        self.assertNotIn('result', revised['payload'])
        self.assertNotIn('needs', revised['payload'])
        self.assertEqual(revised['payload']['history'][0]['result'], first['payload']['result'])
        final = self.company.consult(CUSTOMER, {'contextRevision': 2, 'concern': 'CLEANSING', 'budget': 40, 'fragranceFree': False}, first['id'])
        self.assertEqual((final['id'], final['revision'], final['status']), (first['id'], 3, 'COMPLETED'))
        self.assertEqual(final['payload']['result']['product']['id'], 'P-102')
        self.assert_no_effects()

    def test_ba_t_07_structured_low_level_submit_resume_revise_cancel_compatibility(self):
        with self.company.store.transaction() as db:
            first = self.company.ba.submit(db, CUSTOMER, {'message': 'Hydration please', 'concern': 'HYDRATION'})
            final = self.company.ba.resume(db, CUSTOMER, first['id'], {'contextRevision': 1, 'budget': 60, 'fragranceFree': True})
            self.assertEqual((final['id'], final['revision'], final['status']), (first['id'], 2, 'COMPLETED'))
            changed = self.company.ba.revise(db, CUSTOMER, first['id'], {'contextRevision': 2, 'message': 'Something else'})
            cancelled = self.company.ba.cancel(db, CUSTOMER, first['id'], {'contextRevision': changed['revision']})
        self.assertEqual(cancelled['status'], 'CANCELLED')
        self.assert_no_effects()

    def test_ba_t_07_structured_cancel_persists_and_requires_new_consultation(self):
        record = self.company.consult(CUSTOMER, {'message': 'Hydration please'})
        result = self.company.cancel_consultation(CUSTOMER, record['id'], {'contextRevision': 1})
        self.company = Company(self.path)
        repeat = self.company.cancel_consultation(CUSTOMER, record['id'], {'contextRevision': 2})
        self.assertEqual(repeat, result)
        for operation in (self.company.consult,):
            with self.assertRaises(DomainError):
                operation(CUSTOMER, {'contextRevision': 2, **self.fields}, record['id'])
        with self.assertRaises(DomainError):
            self.company.revise_consultation(CUSTOMER, record['id'], {'contextRevision': 2, **self.fields})
        self.assertNotEqual(self.company.consult(CUSTOMER, self.fields)['id'], record['id'])
        self.assert_no_effects()

    def test_ba_t_07_structured_owner_revision_role_and_exact_input_guards(self):
        record = self.company.consult(CUSTOMER, {'message': 'Hydration please'})
        for actor in (OTHER, FOUNDER):
            for op in (self.company.revise_consultation, self.company.cancel_consultation, self.company.recover_consultation):
                with self.subTest(actor=actor.id, operation=op.__name__), self.assertRaises(DomainError):
                    op(actor, record['id'], {'contextRevision': 1})
        for data in ({'contextRevision': True}, {'contextRevision': 0}, {'contextRevision': 9},
                     {'contextRevision': 1, 'result': {'status': 'COMPLETED'}}, {'contextRevision': 1, 'password': 'unrelated'}):
            with self.subTest(data=data), self.assertRaises(DomainError):
                self.company.consult(CUSTOMER, data, record['id'])
        with self.assertRaises(DomainError):
            self.company.consult(FOUNDER, self.fields)
        self.assertEqual(self.saved(record['id']), record)
        self.assert_no_effects()

    def test_ba_t_07_structured_late_output_after_cancel_or_revision_is_discarded(self):
        for action in ('cancel', 'revise'):
            with self.subTest(action=action):
                record = self.company.consult(CUSTOMER, {'message': 'Hydration please'})
                entered, release = threading.Event(), threading.Event()
                propose = self.company.llm.propose
                def delayed(needs, products):
                    entered.set()
                    self.assertTrue(release.wait(10))
                    return propose(needs, products)
                with patch.object(self.company.llm, 'propose', side_effect=delayed), ThreadPoolExecutor(1) as pool:
                    future = pool.submit(self.company.consult, CUSTOMER,
                        {'contextRevision': 1, **CONFIRM}, record['id'])
                    try:
                        self.assertTrue(entered.wait(5))
                        if action == 'cancel':
                            self.company.cancel_consultation(CUSTOMER, record['id'], {'contextRevision': 2})
                        else:
                            self.company.revise_consultation(CUSTOMER, record['id'], {'contextRevision': 2, 'message': 'Cleansing instead'})
                    finally:
                        release.set()
                    with self.assertRaises(DomainError) as caught:
                        future.result(10)
                self.assertEqual(caught.exception.code, 'STALE_SCOPE')
                current = self.saved(record['id'])
                self.assertEqual(current['revision'], 3)
                self.assertEqual(current['status'], 'CANCELLED' if action == 'cancel' else 'CLARIFYING')
                self.assertNotIn('result', current['payload'])
        self.assert_no_effects()

    def test_ba_t_07_structured_failed_save_recovery_after_restart_is_same_result_once(self):
        self.company.set_fault(FOUNDER, 'ba_recording')
        with self.assertRaises(DomainError) as caught:
            self.company.consult(CUSTOMER, self.fields)
        self.assertEqual(caught.exception.code, 'BA_RECORDING_FAILED')
        snapshot = self.company.snapshot(CUSTOMER)
        record = snapshot['records'][0]
        self.assertEqual(record['status'], 'INCOMPLETE')
        self.assertNotIn('result', record['payload'])
        self.assertNotIn('value', record['payload']['pendingOutcome'])
        self.assertNotIn('value', self.company.snapshot(FOUNDER)['records'][0]['payload']['pendingOutcome'])
        self.company = Company(self.path)
        with patch.object(self.company.llm, 'propose') as provider:
            one = self.company.recover_consultation(CUSTOMER, record['id'], {'contextRevision': 1})
            two = self.company.recover_consultation(CUSTOMER, record['id'], {'contextRevision': 1})
            provider.assert_not_called()
        self.assertEqual((one['id'], one['revision'], one['status'], one['payload']),
                         (two['id'], two['revision'], two['status'], two['payload']))
        self.assertEqual(one['status'], 'COMPLETED')
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE entity_id=? AND event='CONFIRMED_ADVICE_RECORDED'", (record['id'],)).fetchone()[0], 1)
        self.assert_no_effects()

    def test_ba_t_03_structured_recovery_rechecks_stock_and_has_no_model_fallback(self):
        self.company.set_fault(FOUNDER, 'ba_recording')
        with self.assertRaises(DomainError):
            self.company.consult(CUSTOMER, self.fields)
        record = self.company.snapshot(CUSTOMER)['records'][0]
        with self.company.store.transaction() as db:
            db.execute("UPDATE products SET stock=NULL,version=version+1 WHERE id='P-101'")
        with patch.object(self.company.llm, 'propose') as provider:
            result = self.company.recover_consultation(CUSTOMER, record['id'], {'contextRevision': 1})
            provider.assert_not_called()
        self.assertEqual(result['status'], 'INCOMPLETE')
        self.assertEqual(result['payload']['result']['errorCode'], 'LLM_STALE_EVIDENCE')
        self.assertNotIn('product', result['payload']['result'])

    def test_ba_t_07_structured_actual_audit_failure_rolls_back_completion_then_recovers(self):
        with self.company.store.transaction() as db:
            db.execute("""CREATE TRIGGER fail_structured_audit BEFORE INSERT ON events
                WHEN NEW.event='CONFIRMED_ADVICE_RECORDED' BEGIN SELECT RAISE(ABORT,'test disk failure'); END""")
        with self.assertRaises(DomainError) as caught:
            self.company.consult(CUSTOMER, self.fields)
        self.assertEqual(caught.exception.code, 'BA_STORAGE_UNAVAILABLE')
        record = self.company.snapshot(CUSTOMER)['records'][0]
        self.assertNotEqual(record['status'], 'COMPLETED')
        self.assertNotIn('result', record['payload'])
        with self.company.store.transaction() as db:
            db.execute('DROP TRIGGER fail_structured_audit')
        with patch.object(self.company.llm, 'propose') as provider:
            final = self.company.recover_consultation(CUSTOMER, record['id'], {'contextRevision': 1})
            provider.assert_not_called()
        self.assertEqual(final['status'], 'COMPLETED')
        self.assert_no_effects()

    def test_ba_t_07_structured_no_draft_or_failed_cancel_never_claims_success(self):
        save = Store.save
        def fail_stage(db, item):
            if item['payload'].get('pendingOutcome'):
                raise sqlite3.OperationalError('test disk failure')
            return save(db, item)
        with patch.object(Store, 'save', side_effect=fail_stage), self.assertRaises(DomainError):
            self.company.consult(CUSTOMER, self.fields)
        record = self.company.snapshot(CUSTOMER)['records'][0]
        self.assertEqual(record['status'], 'ACTIVE')
        with self.assertRaises(DomainError) as caught:
            self.company.recover_consultation(CUSTOMER, record['id'], {'contextRevision': 1})
        self.assertEqual(caught.exception.code, 'NO_PENDING_RESULT')
        with patch.object(Store, 'save', side_effect=sqlite3.OperationalError('test disk failure')), self.assertRaises(DomainError) as caught:
            self.company.cancel_consultation(CUSTOMER, record['id'], {'contextRevision': 1})
        self.assertEqual(caught.exception.code, 'BA_CANCELLATION_NOT_RECORDED')
        self.assertEqual(self.saved(record['id'])['status'], 'ACTIVE')
        final = self.company.revise_consultation(CUSTOMER, record['id'], {'contextRevision': 1, **self.fields})
        self.assertEqual((final['revision'], final['status']), (2, 'COMPLETED'))

    def test_ba_t_07_structured_rechecks_current_identity_after_model_and_payload_is_minimal(self):
        propose = self.company.llm.propose
        def revoked(needs, products):
            self.assertEqual(set(needs), {'message', 'concern', 'budget', 'fragranceFree'})
            self.assertNotIn('customer', json.dumps([needs, products]))
            with self.company.store.transaction() as db:
                db.execute("UPDATE users SET role='FOUNDER' WHERE id='customer'")
            return propose(needs, products)
        with patch.object(self.company.llm, 'propose', side_effect=revoked), self.assertRaises(DomainError) as caught:
            self.company.consult(CUSTOMER, self.fields)
        self.assertEqual(caught.exception.code, 'FORBIDDEN')
        record = self.company.snapshot(CUSTOMER)['records'][0]
        self.assertEqual(record['status'], 'ACTIVE')
        self.assertNotIn('result', record['payload'])
        self.assert_no_effects()

    def test_ba_t_07_structured_http_session_revoked_during_inference_withholds_advice(self):
        token, csrf, _ = self.company.login('customer', 'customer-demo')
        propose = self.company.llm.propose
        def logout(needs, products):
            with self.company.store.transaction() as db:
                db.execute('DELETE FROM sessions')
            return propose(needs, products)
        headers = {'host': '127.0.0.1', 'content-type': 'application/json',
                   'cookie': 'beauty_session='+token, 'x-csrf-token': csrf}
        with patch.object(self.company.llm, 'propose', side_effect=logout):
            response = Router(self.company).handle('POST', '/api/consultations', headers, json.dumps(self.fields).encode())
        self.assertEqual(response.status, 401)
        record = self.company.snapshot(CUSTOMER)['records'][0]
        self.assertEqual(record['status'], 'ACTIVE')
        self.assertNotIn('result', record['payload'])
        self.assert_no_effects()

    def test_ba_t_07_structured_cancel_invalidates_saved_draft_and_old_recovery(self):
        self.company.set_fault(FOUNDER, 'ba_recording')
        with self.assertRaises(DomainError):
            self.company.consult(CUSTOMER, self.fields)
        record = self.company.snapshot(CUSTOMER)['records'][0]
        cancelled = self.company.cancel_consultation(CUSTOMER, record['id'], {'contextRevision': 1})
        self.assertNotIn('pendingOutcome', cancelled['payload'])
        self.assertNotIn('result', cancelled['payload'])
        for revision in (1, 2):
            with self.assertRaises(DomainError):
                self.company.recover_consultation(CUSTOMER, record['id'], {'contextRevision': revision})
        self.assert_no_effects()

    def test_ba_t_07_pre_marker_structured_record_resume_preserves_budget_units(self):
        with self.company.store.transaction() as db:
            rid = Store.create(db, 'BA', CUSTOMER.id, 'INCOMPLETE', {
                'needs': {'message': 'Hydration please', 'concern': 'HYDRATION', 'budget': 6000, 'fragranceFree': True},
                'result': {'status': 'INCOMPLETE', 'message': 'Earlier failure', 'simulated': True}, 'simulated': True}, 'BA')
        record = self.company.consult(CUSTOMER, {'contextRevision': 1}, rid)
        self.assertEqual((record['id'], record['revision'], record['status']), (rid, 2, 'COMPLETED'))
        self.assertEqual(record['payload']['needs']['budget'], 6000)
        self.assertEqual(record['payload']['structuredInput']['budget'], 60)
        self.assertEqual(record['payload']['history'][0]['status'], 'INCOMPLETE')
        self.assert_no_effects()

    def test_ba_t_07_structured_concurrent_recovery_is_single_recording(self):
        self.company.set_fault(FOUNDER, 'ba_recording')
        with self.assertRaises(DomainError):
            self.company.consult(CUSTOMER, self.fields)
        record = self.company.snapshot(CUSTOMER)['records'][0]
        with patch.object(self.company.llm, 'propose') as provider, ThreadPoolExecutor(3) as pool:
            results = list(pool.map(lambda _: self.company.recover_consultation(
                CUSTOMER, record['id'], {'contextRevision': 1}), range(3)))
            provider.assert_not_called()
        self.assertTrue(all(result['status'] == 'COMPLETED' for result in results))
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE entity_id=? AND event='CONFIRMED_ADVICE_RECORDED'", (record['id'],)).fetchone()[0], 1)
        self.assert_no_effects()

    def test_ba_t_07_saved_response_matches_storage_across_distinct_write_times(self):
        # Every persistence operation gets a distinct instant; no wall-clock luck or sleep.
        counter = iter(range(1, 100))
        def ticking():
            return f'2026-10-31T00:00:00.{next(counter):03d}+00:00'
        with patch('beauty_company.store.now', side_effect=ticking):
            record = self.company.consult(CUSTOMER, {'message': 'Hydration please'})
            self.assertEqual(record, self.saved(record['id']))
            final = self.company.consult(CUSTOMER, {'contextRevision': 1, **CONFIRM}, record['id'])
            self.assertEqual(final, self.saved(record['id']))
            changed = self.company.revise_consultation(CUSTOMER, record['id'], {'contextRevision': 2, 'message': 'Cleansing please'})
            self.assertEqual(changed, self.saved(record['id']))
            cancelled = self.company.cancel_consultation(CUSTOMER, record['id'], {'contextRevision': 3})
            self.assertEqual(cancelled, self.saved(record['id']))
            with self.company.store.transaction() as db:
                low_level = self.company.ba.submit(db, CUSTOMER, self.fields)
                self.assertEqual(low_level, Store.get(db, low_level['id'], 'BA'))
        self.assert_no_effects()
