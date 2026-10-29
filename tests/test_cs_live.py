"""KAN-15: CS intent + staged read-only CO/BA; controlled live doubles, not real-model proof."""
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
import json
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from beauty_company.application import Company
from beauty_company.adapters.mock import MockLlm
from beauty_company.adapters.cs_intent import mock_intent, validate_intent
from beauty_company.adapters.llm import LlmConfig, ModelError, StrataLlm
from beauty_company.contracts import Actor, DomainError
from beauty_company.http import Router
from beauty_company.store import Store

C=Actor('customer','CUSTOMER','Fictional Customer')
F=Actor('founder','FOUNDER','Fictional Founder')
OTHER=Actor('customer-2','CUSTOMER','Fictional Other')
MESSAGE='Please exchange my item for fragrance-free hydration cream for dry skin, budget AUD 60.'


class Target(MockLlm):
    simulated=False
    def __init__(self):self.intents=0;self.advice=0;self.intent_hook=None;self.advice_hook=None;self.bad_intent=None;self.intent_error=None;self.advice_error=None
    def interpret_service_request(self,message):
        self.intents+=1
        if self.intent_hook:self.intent_hook()
        if self.intent_error:raise self.intent_error
        return deepcopy(self.bad_intent) if self.bad_intent is not None else mock_intent(message)
    def propose(self,context,evidence):
        self.advice+=1
        if self.advice_hook:self.advice_hook()
        if self.advice_error:raise self.advice_error
        return super().propose(context,evidence)


class CsLiveTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'isolated.sqlite3';self.llm=Target();self.company=Company(self.path,self.llm)
        self.flow=self.company.cs_flow
    def start(self,message=MESSAGE):return self.flow.start(C,{'orderId':'ORD-1001','message':message})
    def handoff(self,r):return self.flow.coordinate(F,r['id'],{'contextRevision':r['revision']})
    def revise(self,r,message=MESSAGE+' Please use the corrected request.'):
        return self.flow.start(C,{'contextRevision':r['revision'],'message':message},r['id'])
    def record(self,r):
        with self.company.store.read() as db:return Store.get(db,r['id'])
    def counts(self):
        with self.company.store.read() as db:
            return [db.execute('SELECT count(*) FROM '+t).fetchone()[0] for t in ('approvals','effects')]
    def co(self,r):
        with self.company.store.read() as db:return Store.get(db,r['payload']['coordinationId'])
    def assert_code(self,code,call):
        with self.assertRaises(DomainError) as caught:call()
        self.assertEqual(caught.exception.code,code)

    def test_cs_t_01_live_intent_then_co_ba_keeps_modes_scope_and_confirmation(self):
        r=self.start();self.assertEqual(r['status'],'ASSESSING');n=r['payload']['naturalIntent']
        self.assertEqual(n['stage'],'READY');self.assertFalse(n['simulated']);self.assertEqual(r['payload']['needs']['budget'],6000)
        r=self.handoff(r);self.assertEqual(r['status'],'AWAITING_CONFIRMATION');self.assertFalse(r['payload']['advice']['simulated'])
        self.assertEqual(r['payload']['advice']['product']['id'],'P-101');self.assertEqual(self.counts(),[0,0])
        h=self.co(r)['payload']['handoffs'][0];self.assertEqual(h['status'],'COMPLETED');self.assertEqual(h['contextRevision'],1)
        self.assertEqual(set(h['authorisedContext']),{'message','concern','budget','fragranceFree'})
        self.assertEqual((self.llm.intents,self.llm.advice),(1,1))

    def test_gr_t_02_exact_approval_then_one_simulated_effect(self):
        r=self.handoff(self.start());r=self.company.cs.confirm(C,r['id'],{'contextRevision':1})
        self.assertEqual(r['status'],'REVIEW_PENDING');self.assertEqual(self.counts(),[1,0])
        review=self.company.decide(F,r['payload']['approvalId'],{'contextRevision':1,'decision':'APPROVE','reason':'Authorised synthetic test; exact exchange scope.'})
        self.assertEqual(review['decision'],'APPROVE');self.assertEqual(self.counts(),[1,0])
        for _ in range(3):r=self.company.cs.confirm(C,r['id'],{'contextRevision':1})
        self.assertEqual(r['status'],'RESOLVED');self.assertEqual(self.counts(),[1,1])
        with self.company.store.read() as db:self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-101'").fetchone()[0],11)
        self.assertEqual(self.co(r)['status'],'COMPLETED')

    def test_cs_t_02_missing_ambiguous_unsupported_and_negated_do_not_handoff(self):
        for text in ['Please help me.','Please exchange my item.','Refund my item, budget AUD60.',"I do not want to exchange my item, fragrance-free hydration budget AUD60."]:
            with self.subTest(text=text):
                # Each order gets a separate disposable DB, never duplicate business records.
                self.company=Company(Path(self.temp.name)/(str(len(text))+'.sqlite3'),Target());self.flow=self.company.cs_flow
                r=self.start(text);self.assertIn(r['status'],{'NEEDS_INFORMATION','UNRESOLVED'})
                self.assertNotIn('actionRef',r['payload']);self.assertEqual(self.counts(),[0,0]);self.assertNotEqual(r['payload']['naturalIntent']['stage'],'READY')

    def test_cs_t_01_identity_order_and_policy_checked_before_model(self):
        self.assert_code('ORDER_NOT_FOUND',lambda:self.flow.start(OTHER,{'orderId':'ORD-1001','message':MESSAGE}))
        self.assertEqual(self.llm.intents,0)
        with self.company.store.transaction() as db:db.execute("UPDATE orders SET policy='{}' WHERE id='ORD-1001'")
        r=self.start();self.assertEqual(r['status'],'NEEDS_INFORMATION');self.assertEqual(self.llm.intents,0)
        self.assertEqual(self.counts(),[0,0])

    def test_cs_t_04_intent_failure_retains_actual_mode_without_fallback(self):
        for code in ['LLM_UNAVAILABLE','LLM_TIMEOUT','LLM_HTTP','LLM_INVALID_OUTPUT']:
            with self.subTest(code=code):
                self.llm.intent_error=ModelError('SYNTHETIC-PRIVATE',502,code)
                r=self.start() if code=='LLM_UNAVAILABLE' else self.revise(r,MESSAGE+' '+code)
                self.assertEqual(r['status'],'UNRESOLVED');n=r['payload']['naturalIntent']
                self.assertEqual(n['errorCode'],code);self.assertFalse(n['simulated']);self.assertNotIn('SYNTHETIC-PRIVATE',json.dumps(r))
        self.assertEqual(self.llm.advice,0);self.assertEqual(self.counts(),[0,0])

    def test_cs_t_04_invalid_or_authority_bearing_intent_is_withheld(self):
        good=mock_intent(MESSAGE)
        for i,bad in enumerate([{},[],{**good,'approve':True},{**good,'intentSource':'not in the message'},
                {**good,'needs':{**good['needs'],'budget':999}}, {**good,'intent':'EXECUTE'}]):
            self.llm.bad_intent=bad;r=self.start() if i==0 else self.revise(r,MESSAGE+' '+str(i))
            self.assertEqual(r['payload']['naturalIntent']['errorCode'],'LLM_INVALID_OUTPUT');self.assertEqual(self.counts(),[0,0])

    def test_cs_t_04_missing_capability_is_not_mock_success(self):
        self.llm.interpret_service_request=None
        r=self.start();self.assertEqual(r['payload']['naturalIntent']['errorCode'],'LLM_CAPABILITY_UNAVAILABLE')
        self.assertFalse(r['payload']['naturalIntent']['simulated']);self.assertEqual(self.company.mode()['csIntent'],'NOT_CONNECTED')

    def test_cs_t_04_both_inferences_release_write_lock_and_all_connections(self):
        def write():
            with self.company.store.transaction() as db:db.execute("UPDATE products SET tone='test' WHERE id='P-102'")
        self.llm.intent_hook=write;self.llm.advice_hook=write
        r=self.handoff(self.start());self.assertEqual(r['status'],'AWAITING_CONFIRMATION')

    def test_cs_t_04_changed_stock_during_advice_withholds_result(self):
        def change():
            with self.company.store.transaction() as db:db.execute("UPDATE products SET stock=0,version=version+1 WHERE id='P-101'")
        self.llm.advice_hook=change;r=self.handoff(self.start())
        self.assertEqual(r['status'],'UNRESOLVED');self.assertNotIn('actionRef',r['payload']);self.assertEqual(self.counts(),[0,0])

    def test_cs_t_02_policy_change_during_intent_is_retained_not_guessed(self):
        def change():
            with self.company.store.transaction() as db:db.execute("UPDATE orders SET policy='{}' WHERE id='ORD-1001'")
        self.llm.intent_hook=change;r=self.start();self.assertEqual(r['status'],'NEEDS_INFORMATION')
        self.assertEqual(r['payload']['naturalIntent']['stage'],'BLOCKED');self.assertEqual(self.counts(),[0,0])

    def test_cs_t_04_policy_or_order_change_during_advice_blocks_old_scope(self):
        def change():
            with self.company.store.transaction() as db:db.execute("UPDATE orders SET customer_id='customer-2' WHERE id='ORD-1001'")
        self.llm.advice_hook=change;r=self.handoff(self.start());self.assertEqual(r['status'],'UNRESOLVED')
        self.assertNotIn('advice',r['payload']);self.assertEqual(self.counts(),[0,0])

    def test_cs_t_04_old_intent_response_cannot_overwrite_new_revision(self):
        def revise_during():
            self.llm.intent_hook=None
            with self.company.store.read() as db:old=Store.get(db,db.execute("SELECT id FROM records WHERE kind='CS'").fetchone()[0])
            self.new=self.revise(old)
        self.llm.intent_hook=revise_during
        self.assert_code('STALE_SCOPE',self.start);r=self.record(self.new)
        self.assertEqual(r['revision'],2);self.assertEqual(r['payload']['naturalIntent']['stage'],'READY')

    def test_co_t_01_old_advice_response_and_confirmation_cannot_cross_revision(self):
        old=self.start()
        def revise_during():self.llm.advice_hook=None;self.new=self.revise(old)
        self.llm.advice_hook=revise_during
        self.assert_code('STALE_SCOPE',lambda:self.handoff(old));r=self.record(self.new)
        self.assertEqual(r['revision'],2);self.assertNotIn('advice',r['payload'])
        self.assert_code('STALE_SCOPE',lambda:self.company.cs.confirm(C,r['id'],{'contextRevision':1}))
        self.assertEqual(self.counts(),[0,0])

    def test_co_t_01_concurrent_duplicate_handoff_dispatches_once(self):
        r=self.start();entered=threading.Event();release=threading.Event()
        def wait():entered.set();self.assertTrue(release.wait(5))
        self.llm.advice_hook=wait
        with ThreadPoolExecutor(max_workers=2) as pool:
            future=pool.submit(self.handoff,r);self.assertTrue(entered.wait(5))
            try:
                duplicate=self.handoff(r);self.assertEqual(duplicate['status'],'ASSESSING')
            finally:release.set()
            done=future.result(timeout=5)
        self.assertEqual(done['status'],'AWAITING_CONFIRMATION');self.assertEqual(self.llm.advice,1)
        self.handoff(done);self.assertEqual(self.llm.advice,1)
        self.assertEqual(len(self.co(done)['payload']['handoffs']),1)

    def test_cs_t_01_duplicate_intake_reuses_record_without_inference(self):
        r=self.start();again=self.start();self.assertEqual(r['id'],again['id']);self.assertEqual(self.llm.intents,1)
        self.assert_code('DUPLICATE_REQUEST',lambda:self.start(MESSAGE+' changed'))

    def test_co_t_04_ba_failure_preserves_live_mode_no_review_or_execution(self):
        self.llm.advice_error=ModelError('SYNTHETIC-PRIVATE',503,'LLM_UNAVAILABLE')
        r=self.handoff(self.start());self.assertEqual(r['status'],'UNRESOLVED')
        self.assertFalse(r['payload']['advice']['simulated']);self.assertNotIn('SYNTHETIC-PRIVATE',json.dumps(r))
        self.assertEqual(self.co(r)['payload']['handoffs'][0]['failure']['upstreamCode'],'LLM_UNAVAILABLE')
        self.handoff(r);self.assertEqual(self.llm.advice,1);self.assertEqual(self.counts(),[0,0])

    def test_cs_t_06_final_storage_error_retains_pending_intent_not_success(self):
        def trigger():
            with self.company.store.transaction() as db:db.execute("CREATE TRIGGER fail_intent BEFORE INSERT ON events WHEN NEW.event='INTENT_RECORDED' BEGIN SELECT RAISE(ABORT,'test'); END")
        self.llm.intent_hook=trigger
        self.assert_code('CS_STORAGE_UNAVAILABLE',self.start)
        with self.company.store.read() as db:r=Store.get(db,db.execute("SELECT id FROM records WHERE kind='CS'").fetchone()[0])
        self.assertEqual(r['payload']['naturalIntent']['stage'],'INTERPRETING');self.assertEqual(self.counts(),[0,0])

    def test_co_t_08_result_save_failure_keeps_committed_sent_and_no_redispatch(self):
        r=self.start()
        with self.company.store.transaction() as db:db.execute("CREATE TRIGGER fail_result BEFORE INSERT ON events WHEN NEW.event='ADVICE_RESULT_RECORDED' BEGIN SELECT RAISE(ABORT,'test'); END")
        self.assert_code('CS_STORAGE_UNAVAILABLE',lambda:self.handoff(r))
        self.assertEqual(self.record(r)['status'],'ASSESSING');self.assertEqual(self.co(r)['payload']['handoffs'][0]['status'],'SENT')
        self.handoff(r);self.assertEqual(self.llm.advice,1);self.assertEqual(self.counts(),[0,0])

    def test_cs_t_01_http_session_csrf_and_expiry_rechecked_after_intent(self):
        router=Router(self.company);base={'Host':'127.0.0.1:5620','Content-Type':'application/json'}
        token,csrf,_=self.company.login('customer','customer-demo');headers={**base,'Cookie':'beauty_session='+token,'X-CSRF-Token':csrf}
        body=json.dumps({'orderId':'ORD-1001','message':MESSAGE}).encode()
        denied=router.handle('POST','/api/after-sales/intake',base,body);self.assertEqual(denied.status,401)
        denied=router.handle('POST','/api/after-sales/intake',{**headers,'X-CSRF-Token':'bad'},body);self.assertEqual(denied.status,403)
        def expire():
            with self.company.store.transaction() as db:db.execute('UPDATE sessions SET expires=0')
        self.llm.intent_hook=expire
        denied=router.handle('POST','/api/after-sales/intake',headers,body);self.assertEqual(denied.status,401)
        self.assertEqual(self.counts(),[0,0])

    def test_cs_t_01_founder_identity_rechecked_before_advice_save(self):
        r=self.start()
        def revoke():
            with self.company.store.transaction() as db:db.execute("UPDATE users SET role='CUSTOMER' WHERE id='founder'")
        self.llm.advice_hook=revoke
        self.assert_code('FORBIDDEN',lambda:self.handoff(r));self.assertNotIn('advice',self.record(r)['payload'])
        self.assertEqual(self.counts(),[0,0])

    def test_cs_t_01_shared_transport_uses_only_message_and_rejects_extra_authority(self):
        llm=StrataLlm(LlmConfig('http://127.0.0.1:8080/v1','test'))
        with patch.object(llm,'_complete',return_value=mock_intent(MESSAGE)) as call:
            self.assertEqual(llm.interpret_service_request(MESSAGE)['intent'],'EXCHANGE')
            self.assertEqual(call.call_args.args[1],{'message':MESSAGE})
        with patch.object(llm,'_complete',return_value={**mock_intent(MESSAGE),'policy':'approved'}):
            self.assert_code('LLM_INVALID_OUTPUT',lambda:llm.interpret_service_request(MESSAGE))

    def test_cs_t_01_default_mock_and_structured_exchange_remain_available(self):
        company=Company(Path(self.temp.name)/'default.sqlite3')
        self.assertEqual(company.mode()['csIntent'],'MOCK')
        r=company.cs_flow.start(C,{'orderId':'ORD-1001','message':MESSAGE})
        self.assertTrue(r['payload']['naturalIntent']['simulated'])
        r=company.cs_flow.coordinate(F,r['id'],{})
        self.assertTrue(r['payload']['advice']['simulated']);self.assertEqual(r['status'],'AWAITING_CONFIRMATION')

    def test_cs_t_02_semantic_constraint_mismatch_and_conflicts_cannot_guess(self):
        good=mock_intent(MESSAGE)
        for bad in [
            {**good,'needs':{**good['needs'],'fragranceFree':False}},
            {**good,'needs':{**good['needs'],'concern':'CLEANSING'}},
        ]:
            with self.assertRaises(ValueError):validate_intent(bad,MESSAGE)
        for message,field in [(MESSAGE+' Also cleansing.','concern'),(MESSAGE+' Or budget AUD 80.','budget')]:
            self.assertIsNone(mock_intent(message)['needs'][field])

    def test_cs_t_01_concurrent_duplicate_intake_does_not_call_model_again(self):
        entered=threading.Event();release=threading.Event()
        def wait():entered.set();self.assertTrue(release.wait(5))
        self.llm.intent_hook=wait
        with ThreadPoolExecutor(max_workers=2) as pool:
            future=pool.submit(self.start);self.assertTrue(entered.wait(5))
            try:
                current=self.start();self.assertEqual(current['payload']['naturalIntent']['stage'],'INTERPRETING')
            finally:release.set()
            saved=future.result(timeout=5)
        self.assertEqual(current['id'],saved['id']);self.assertEqual(self.llm.intents,1)

    def test_co_t_01_legacy_live_service_cannot_infer_inside_write_transaction(self):
        r=self.start()
        def legacy():
            with self.company.store.transaction() as db:self.company.cs.coordinate(db,F,r['id'])
        self.assert_code('CS_STAGED_HANDOFF_REQUIRED',legacy)
        self.assertEqual(self.llm.advice,0)

    def test_cs_t_04_correction_supersedes_pending_exact_review(self):
        r=self.handoff(self.start());r=self.company.cs.confirm(C,r['id'],{'contextRevision':1});review_id=r['payload']['approvalId']
        revised=self.revise(r)
        self.assertEqual(revised['revision'],2);self.assertNotIn('approvalId',revised['payload'])
        with self.company.store.read() as db:self.assertEqual(self.company.ap.get(db,review_id)['status'],'SUPERSEDED')
        with self.assertRaises(DomainError):self.company.decide(F,review_id,{'contextRevision':1,'decision':'APPROVE','reason':'Old scope cannot apply.'})
        self.assertEqual(self.counts(),[1,0])

    def test_co_t_08_initial_staged_audit_failure_prevents_model_dispatch(self):
        r=self.start()
        with self.company.store.transaction() as db:db.execute("CREATE TRIGGER fail_sent BEFORE INSERT ON events WHEN NEW.event='HANDOFF_SENT' BEGIN SELECT RAISE(ABORT,'test'); END")
        self.assert_code('CS_STORAGE_UNAVAILABLE',lambda:self.handoff(r))
        self.assertEqual(self.llm.advice,0);self.assertEqual(self.co(r)['payload']['handoffs'],[])
        self.assertEqual(self.record(r)['status'],'ASSESSING');self.assertEqual(self.counts(),[0,0])
