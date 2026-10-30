"""CO-T-01/02/03/04/08 bounded handoff contracts; controlled targets, no real model."""
from copy import deepcopy
import json
import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from beauty_company.application import Company
from beauty_company.contracts import Actor, DomainError
from beauty_company.http import Router
from beauty_company.store import Store

CUSTOMER = Actor('customer', 'CUSTOMER', 'Fictional Customer')
FOUNDER = Actor('founder', 'FOUNDER', 'Fictional Founder')
INPUT = {'orderId':'ORD-1001','message':'Fragrance-free hydration advice','concern':'HYDRATION',
         'budget':60,'fragranceFree':True}


class CoordinationHandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.index=0;self.fresh()

    def fresh(self):
        self.index+=1;self.company=Company(Path(self.temp.name)/f'co-{self.index}.sqlite3')
        with self.company.store.transaction() as db:self.request=self.company.cs.assess(db,CUSTOMER,INPUT)
        self.rid=self.request['payload']['coordinationId'];self.needs=self.request['payload']['needs']

    def saved(self,rid=None):
        with self.company.store.read() as db:return Store.get(db,rid or self.rid)

    def handoff(self,needs=None,target=None):
        with self.company.store.transaction() as db:
            return self.company.co.advice_handoff(db,self.rid,self.needs if needs is None else needs,
                self.company.ba if target is None else target)

    def coordinate(self):
        with self.company.store.transaction() as db:
            return self.company.cs.coordinate(db,FOUNDER,self.request['id'])

    def no_effects(self):
        with self.company.store.read() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM effects').fetchone()[0],0)
            self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0],0)
            self.assertEqual([r[0] for r in db.execute('SELECT stock FROM products ORDER BY id')],[12,8,0])

    def test_co_t_01_valid_handoff_retains_only_minimal_context_and_distinct_success(self):
        needs={**self.needs,'password':'SYNTHETIC-PRIVATE','orderId':'DO-NOT-FORWARD'}
        result=self.handoff(needs)
        record=self.saved();handoff=record['payload']['handoffs'][0]
        self.assertEqual(result['status'],'COMPLETED');self.assertEqual(record['status'],'PENDING_VALIDATION')
        self.assertEqual(set(handoff['authorisedContext']),{'message','concern','budget','fragranceFree'})
        self.assertEqual(handoff['originId'],self.request['id']);self.assertEqual(handoff['contextRevision'],1)
        self.assertEqual(handoff['operation'],'READ_ONLY_ADVICE');self.assertTrue(handoff['handoffId'])
        self.assertNotIn('SYNTHETIC-PRIVATE',json.dumps(record));self.no_effects()

    def test_co_t_02_invalid_context_fields_do_not_dispatch_or_forward_raw_values(self):
        bad=[{},{'message':''},{'message':None},{'message':'x'*2001},{'concern':None},{'concern':[]},
             {'concern':'UNKNOWN'},{'budget':True},{'budget':0},{'budget':-1},{'budget':60.0},
             {'budget':1000001},{'fragranceFree':1},{'fragranceFree':None}]
        for change in bad:
            with self.subTest(change=change):
                self.fresh();needs={**self.needs,**change} if change else {'message':'SYNTHETIC-PRIVATE'}
                target=SimpleNamespace(simulated=True,recommend=Mock())
                result=self.handoff(needs,target)
                target.recommend.assert_not_called();self.assertEqual(result['errorCode'],'CO_INVALID_CONTEXT')
                saved=self.saved();self.assertEqual(saved['status'],'CLARIFICATION_REQUIRED')
                self.assertEqual(saved['payload']['handoffs'][0]['authorisedContext'],{})
                self.assertNotIn('SYNTHETIC-PRIVATE',json.dumps(saved));self.no_effects()

    def test_co_t_02_non_object_context_is_retained_as_failure_without_dispatch(self):
        for value in (None,False,[],42,'SYNTHETIC-PRIVATE'):
            self.fresh();target=SimpleNamespace(simulated=True,recommend=Mock())
            with self.company.store.transaction() as db:
                result=self.company.co.advice_handoff(db,self.rid,value,target)
            self.assertEqual(result['status'],'INCOMPLETE');target.recommend.assert_not_called()
            self.assertEqual(self.saved()['status'],'CLARIFICATION_REQUIRED')

    def test_co_t_02_budget_remains_integer_cents_without_second_conversion(self):
        self.assertEqual(self.needs['budget'],6000)
        result=self.handoff();self.assertEqual(result['product']['price'],4800)
        self.assertEqual(result['evidence']['constraints']['budget'],6000)

    def test_co_t_03_unavailable_target_is_recorded_without_dispatch(self):
        for target in (None,object(),SimpleNamespace(simulated=True,recommend=False)):
            self.fresh()
            with self.company.store.transaction() as db:
                result=self.company.co.advice_handoff(db,self.rid,self.needs,target)
            self.assertEqual(result['errorCode'],'CO_TARGET_UNAVAILABLE')
            record=self.saved();self.assertEqual(record['status'],'ESCALATED')
            self.assertFalse(record['payload']['handoffs'][0]['dispatched']);self.no_effects()

    def test_co_t_03_timeout_and_unavailable_results_keep_permitted_reason_only(self):
        for error,code in ((TimeoutError('SYNTHETIC-PRIVATE'),'CO_TARGET_TIMEOUT'),
                           (ConnectionError('SYNTHETIC-PRIVATE'),'CO_TARGET_UNAVAILABLE'),
                           (RuntimeError('SYNTHETIC-PRIVATE'),'CO_TARGET_FAILED'),
                           (sqlite3.OperationalError('SYNTHETIC-PRIVATE'),'CO_TARGET_UNAVAILABLE')):
            self.fresh();target=SimpleNamespace(simulated=True,recommend=Mock(side_effect=error))
            result=self.handoff(target=target)
            self.assertEqual(result['errorCode'],code);self.assertEqual(self.saved()['status'],'ESCALATED')
            self.assertNotIn('SYNTHETIC-PRIVATE',json.dumps(self.saved()));self.no_effects()

    def test_co_t_03_safe_upstream_code_and_original_mode_retained_without_fallback(self):
        target=SimpleNamespace(simulated=False,recommend=Mock(side_effect=DomainError('SYNTHETIC-PRIVATE',503,'LLM_UNAVAILABLE')))
        result=self.handoff(target=target)
        self.assertFalse(result['simulated']);self.assertEqual(result['status'],'INCOMPLETE')
        failure=self.saved()['payload']['handoffs'][0]['failure'];self.assertEqual(failure['upstreamCode'],'LLM_UNAVAILABLE')
        self.assertNotIn('SYNTHETIC-PRIVATE',json.dumps(self.saved()));self.no_effects()

    def test_co_t_04_malformed_success_or_unrecognised_status_never_completes(self):
        for value in (None,[],{'status':'COMPLETED'},{'status':'SENT'},{'status':'INCOMPLETE'},
                      {'status':'INCOMPLETE','message':'SYNTHETIC-PRIVATE','simulated':True,'product':{}}):
            self.fresh();target=SimpleNamespace(simulated=True,recommend=Mock(return_value=value))
            result=self.handoff(target=target)
            self.assertEqual(result['errorCode'],'CO_INVALID_RESULT')
            self.assertEqual(self.saved()['payload']['handoffs'][0]['status'],'FAILED');self.no_effects()

    def test_co_t_04_actual_product_claim_and_evidence_are_independently_checked(self):
        for field in ('id','price','version','claim','stock','constraints','observation','extra'):
            self.fresh()
            with self.company.store.read() as db:result=self.company.ba.recommend(db,self.needs)
            if field=='id':result['product']['id']='INVENTED'
            elif field=='price':result['product']['price']=1
            elif field=='version':result['product']['version']=True
            elif field=='claim':result['reasons']=['Unsupported cure']
            elif field=='stock':result['product']['stock']=None
            elif field=='constraints':result['evidence']['constraints']['budget']=999999
            elif field=='observation':result['evidence']['inventoryObservation']='not-an-observation'
            else:result['approvalId']='SYNTHETIC-PRIVATE'
            target=SimpleNamespace(simulated=True,recommend=Mock(return_value=result))
            checked=self.handoff(target=target)
            self.assertEqual(checked['errorCode'],'CO_INVALID_RESULT',field)
            self.assertNotIn('product',checked);self.assertNotIn('SYNTHETIC-PRIVATE',json.dumps(self.saved()))

    def test_co_t_04_unavailable_product_or_unsupported_need_cannot_be_invented(self):
        with self.company.store.read() as db:result=self.company.ba.recommend(db,self.needs)
        with self.company.store.transaction() as db:db.execute("UPDATE products SET stock=0 WHERE id='P-101'")
        checked=self.handoff(target=SimpleNamespace(simulated=True,recommend=Mock(return_value=result)))
        self.assertEqual(checked['errorCode'],'CO_INVALID_RESULT')
        self.assertEqual(self.saved()['status'],'ESCALATED')

    def test_co_t_04_mutating_receiver_cannot_rewrite_the_scope_it_is_verified_against(self):
        original=self.company.ba.recommend
        def mutate(db,context):
            context.update(concern='CLEANSING',budget=999999)
            return original(db,context)
        with patch.object(self.company.ba,'recommend',side_effect=mutate):result=self.handoff()
        self.assertEqual(result['errorCode'],'CO_INVALID_RESULT')
        self.assertEqual(self.saved()['payload']['handoffs'][0]['authorisedContext'],self.needs)

    def test_co_t_04_late_mutation_of_returned_value_does_not_change_saved_result(self):
        result=self.handoff();result['product']['name']='CHANGED';result['reasons'].clear()
        saved=self.saved()['payload']['handoffs'][0]['result']
        self.assertEqual(saved['product']['name'],'Daily Hydration Cream');self.assertTrue(saved['reasons'])

    def test_co_t_04_incomplete_result_drops_untrusted_explanation_and_keeps_failure(self):
        target=SimpleNamespace(simulated=False,recommend=Mock(return_value={'status':'INCOMPLETE',
            'message':'SYNTHETIC-PRIVATE','simulated':False,'errorCode':'LLM_TIMEOUT'}))
        result=self.handoff(target=target);self.assertEqual(result['errorCode'],'CO_ADVICE_INCOMPLETE')
        self.assertFalse(result['simulated']);self.assertNotIn('SYNTHETIC-PRIVATE',json.dumps(self.saved()))
        self.assertEqual(self.saved()['payload']['handoffs'][0]['failure']['upstreamCode'],'LLM_TIMEOUT')

    def test_co_t_01_duplicate_success_reuses_the_same_handoff_without_target_or_new_events(self):
        with patch.object(self.company.ba,'recommend',wraps=self.company.ba.recommend) as target:
            first=self.handoff();second=self.handoff()
        self.assertEqual(target.call_count,1);self.assertEqual(first,second)
        self.assertEqual(len(self.saved()['payload']['handoffs']),1)
        with self.company.store.read() as db:self.assertEqual(db.execute('SELECT count(*) FROM events WHERE entity_id=?',(self.rid,)).fetchone()[0],2)

    def test_co_t_03_duplicate_failure_does_not_automatically_retry(self):
        target=SimpleNamespace(simulated=True,recommend=Mock(side_effect=TimeoutError()))
        first=self.handoff(target=target);second=self.handoff(target=target)
        self.assertEqual(first,second);self.assertEqual(target.recommend.call_count,1)
        self.assertEqual(len(self.saved()['payload']['handoffs']),1);self.no_effects()

    def test_co_t_01_corrected_cs_revision_records_new_handoff_and_preserves_failure_history(self):
        self.company.cs.advisor=SimpleNamespace(simulated=True,recommend=Mock(side_effect=TimeoutError()))
        self.assertEqual(self.coordinate()['status'],'UNRESOLVED')
        self.company.cs.advisor=self.company.ba
        with self.company.store.transaction() as db:
            revised=self.company.cs.revise(db,CUSTOMER,self.request['id'],{**INPUT,'contextRevision':1})
            result=self.company.cs.coordinate(db,FOUNDER,self.request['id'])
        self.assertEqual(revised['revision'],2);self.assertEqual(result['status'],'AWAITING_CONFIRMATION')
        handoffs=self.saved()['payload']['handoffs'];self.assertEqual([h['contextRevision'] for h in handoffs],[1,2])
        self.assertEqual([h['status'] for h in handoffs],['FAILED','COMPLETED'])
        self.assertNotEqual(handoffs[0]['handoffId'],handoffs[1]['handoffId']);self.no_effects()

    def test_co_t_02_stale_needs_cannot_replace_current_scope_or_dispatch(self):
        target=SimpleNamespace(simulated=True,recommend=Mock())
        with self.assertRaises(DomainError) as caught:self.handoff({**self.needs,'budget':10000},target)
        self.assertEqual(caught.exception.code,'STALE_SCOPE');target.recommend.assert_not_called()
        self.assertEqual(self.saved()['payload']['handoffs'],[])

    def test_co_t_02_origin_link_and_owner_must_match(self):
        for field,value in (('owner_id','customer-2'),('coordinationId','CO-wrong')):
            self.fresh()
            with self.company.store.transaction() as db:
                origin=Store.get(db,self.request['id'])
                if field=='owner_id':origin[field]=value;db.execute('UPDATE records SET owner_id=? WHERE id=?',(value,origin['id']))
                else:origin['payload'][field]=value;Store.save(db,origin)
            with self.assertRaises(DomainError) as caught:self.handoff()
            self.assertEqual(caught.exception.code,'STALE_SCOPE');self.assertEqual(self.saved()['payload']['handoffs'],[])

    def test_co_t_03_existing_cs_caller_commits_failure_note_without_confirmation_or_review(self):
        self.company.cs.advisor=SimpleNamespace(simulated=True,recommend=Mock(side_effect=TimeoutError('SYNTHETIC-PRIVATE')))
        result=self.coordinate();self.assertEqual(result['status'],'UNRESOLVED')
        self.assertEqual(result['payload']['advice']['status'],'INCOMPLETE')
        self.assertNotIn('actionRef',result['payload']);self.assertNotIn('approvalId',result['payload'])
        self.assertNotIn('SYNTHETIC-PRIVATE',json.dumps(self.company.snapshot(FOUNDER)));self.no_effects()

    def test_co_t_03_http_founder_csrf_and_duplicate_failure_contract(self):
        router=Router(self.company);path='/api/after-sales/'+self.request['id']+'/coordinate'
        headers={'Host':'127.0.0.1:5750','Content-Type':'application/json'}
        self.assertEqual(router.handle('POST',path,headers,b'{}').status,401)
        for user in ('customer','founder'):
            token,csrf,_=self.company.login(user,user+'-demo')
            authenticated={**headers,'Cookie':'beauty_session='+token,'X-CSRF-Token':csrf}
            self.assertEqual(router.handle('POST',path,{**authenticated,'X-CSRF-Token':''},b'{}').status,403)
            self.company.cs.advisor=SimpleNamespace(simulated=True,recommend=Mock(side_effect=TimeoutError()))
            response=router.handle('POST',path,authenticated,b'{}')
            self.assertEqual(response.status,403 if user=='customer' else 200)
        self.assertEqual(json.loads(response.body)['status'],'UNRESOLVED')
        repeat=router.handle('POST',path,authenticated,b'{}');self.assertEqual(json.loads(repeat.body)['status'],'UNRESOLVED')
        self.assertEqual(len(self.saved()['payload']['handoffs']),1);self.no_effects()

    def test_co_t_08_intent_audit_failure_prevents_dispatch_and_claims_no_saved_trace(self):
        with self.company.store.transaction() as db:
            db.execute("CREATE TRIGGER fail_co BEFORE INSERT ON events WHEN NEW.event='HANDOFF_SENT' BEGIN SELECT RAISE(ABORT,'SYNTHETIC-PRIVATE'); END")
        target=SimpleNamespace(simulated=True,recommend=Mock())
        with self.assertRaises(DomainError) as caught:self.handoff(target=target)
        self.assertEqual(caught.exception.code,'CO_STORAGE_UNAVAILABLE');self.assertEqual(caught.exception.status,503)
        self.assertNotIn('SYNTHETIC-PRIVATE',str(caught.exception));target.recommend.assert_not_called()
        self.assertEqual(self.saved()['payload']['handoffs'],[]);self.no_effects()

    def test_co_t_08_result_or_failure_audit_abort_rolls_back_handoff_and_cs_outcome(self):
        for event,failed in (('ADVICE_RESULT_RECORDED',False),('HANDOFF_FAILED',True)):
            self.fresh()
            if failed:self.company.cs.advisor=SimpleNamespace(simulated=True,recommend=Mock(side_effect=TimeoutError()))
            with self.company.store.transaction() as db:
                db.execute(f"CREATE TRIGGER fail_co BEFORE INSERT ON events WHEN NEW.event='{event}' BEGIN SELECT RAISE(ABORT,'audit outage'); END")
            with self.assertRaises(DomainError) as caught:self.coordinate()
            self.assertEqual(caught.exception.code,'CO_STORAGE_UNAVAILABLE')
            self.assertEqual(self.saved()['payload']['handoffs'],[])
            self.assertEqual(self.saved(self.request['id'])['status'],'ASSESSING');self.no_effects()

    def test_co_t_08_read_only_storage_cannot_claim_saved_failure_or_dispatch(self):
        target=SimpleNamespace(simulated=True,recommend=Mock())
        with self.assertRaises(DomainError) as caught:
            with self.company.store.transaction() as db:
                db.execute('PRAGMA query_only=ON')
                self.company.co.advice_handoff(db,self.rid,self.needs,target)
        self.assertEqual(caught.exception.code,'CO_STORAGE_UNAVAILABLE');target.recommend.assert_not_called()
        self.assertEqual(self.saved()['payload']['handoffs'],[])

    def test_co_t_01_concurrent_cs_calls_dispatch_once_and_never_execute(self):
        for failed in (False,True):
            self.fresh();target=Mock(wraps=self.company.ba.recommend)
            if failed:target=Mock(side_effect=TimeoutError())
            self.company.cs.advisor=SimpleNamespace(simulated=True,recommend=target)
            with ThreadPoolExecutor(3) as pool:results=list(pool.map(lambda _:self.coordinate(),range(3)))
            self.assertEqual(target.call_count,1);self.assertEqual(len(self.saved()['payload']['handoffs']),1)
            self.assertEqual({r['status'] for r in results},{'UNRESOLVED' if failed else 'AWAITING_CONFIRMATION'})
            self.no_effects()

    def test_co_t_02_invalid_replay_cannot_reuse_prior_success(self):
        self.handoff()
        with self.assertRaises(DomainError) as caught:self.handoff({'message':'missing constraints'})
        self.assertEqual(caught.exception.code,'STALE_SCOPE')
        self.assertEqual(len(self.saved()['payload']['handoffs']),1)

    def test_co_t_03_invalid_mode_or_failing_adapter_lookup_never_dispatches(self):
        class Broken:
            simulated=True
            @property
            def recommend(self):raise RuntimeError('SYNTHETIC-PRIVATE')
        target=SimpleNamespace(simulated='invalid mode',recommend=Mock())
        for adapter in (target,Broken()):
            self.fresh();result=self.handoff(target=adapter)
            self.assertEqual(result['errorCode'],'CO_TARGET_UNAVAILABLE')
            self.assertFalse(self.saved()['payload']['handoffs'][0]['dispatched'])
            self.assertNotIn('SYNTHETIC-PRIVATE',json.dumps(self.saved()))
        target.recommend.assert_not_called()

    def test_co_t_04_untrusted_success_prose_cannot_add_saved_authority_or_private_data(self):
        with self.company.store.read() as db:result=self.company.ba.recommend(db,self.needs)
        result['message']='SYNTHETIC-PRIVATE: the exchange is already approved'
        checked=self.handoff(target=SimpleNamespace(simulated=True,recommend=Mock(return_value=result)))
        self.assertEqual(checked['status'],'COMPLETED')
        self.assertNotIn('SYNTHETIC-PRIVATE',json.dumps(self.saved()));self.no_effects()

    def test_co_t_02_non_assessing_origin_cannot_start_a_new_handoff(self):
        for status in ('CANCELLED', 'RESOLVED', 'UNRESOLVED', 'AWAITING_CONFIRMATION'):
            with self.subTest(status=status):
                self.fresh()
                with self.company.store.transaction() as db:
                    origin = Store.get(db, self.request['id'])
                    origin['status'] = status
                    Store.save(db, origin)
                target = SimpleNamespace(simulated=True, recommend=Mock())
                with self.assertRaises(DomainError) as caught:
                    self.handoff(target=target)
                self.assertEqual(caught.exception.code, 'INVALID_STATE')
                target.recommend.assert_not_called()
                self.assertEqual(self.saved()['payload']['handoffs'], [])
                self.no_effects()

    def test_co_t_02_invalid_saved_needs_cannot_be_replaced_by_valid_caller_context(self):
        with self.company.store.transaction() as db:
            origin = Store.get(db, self.request['id'])
            origin['payload']['needs'] = None
            Store.save(db, origin)
        target = SimpleNamespace(simulated=True, recommend=Mock())
        result = self.handoff(target=target)
        self.assertEqual(result['errorCode'], 'CO_INVALID_CONTEXT')
        target.recommend.assert_not_called()
        record = self.saved()
        self.assertEqual(record['status'], 'CLARIFICATION_REQUIRED')
        self.assertFalse(record['payload']['handoffs'][0]['dispatched'])
        self.no_effects()

    def test_co_t_04_unknown_current_stock_rejects_previously_valid_advice(self):
        with self.company.store.read() as db:
            advice = self.company.ba.recommend(db, self.needs)
        with self.company.store.transaction() as db:
            db.execute('UPDATE products SET stock=NULL WHERE id=?', (advice['product']['id'],))
        target = SimpleNamespace(simulated=True, recommend=Mock(return_value=advice))
        result = self.handoff(target=target)
        self.assertEqual(result['errorCode'], 'CO_INVALID_RESULT')
        self.assertNotIn('product', result)
        record = self.saved()
        self.assertEqual(record['status'], 'ESCALATED')
        self.assertEqual(record['payload']['handoffs'][0]['status'], 'FAILED')
        with self.company.store.read() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM effects').fetchone()[0], 0)
            self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0], 0)
            self.assertIsNone(db.execute('SELECT stock FROM products WHERE id=?',
                                        (advice['product']['id'],)).fetchone()[0])
