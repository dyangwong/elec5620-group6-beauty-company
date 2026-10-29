
import json
import io
import sqlite3
import threading
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from beauty_company.application import Company
from beauty_company.contracts import Actor, DomainError
from beauty_company.http import Router
from beauty_company.store import Store
from beauty_company.adapters.mock import MockLlm
from beauty_company.adapters.llm import LlmConfig, ModelError, StrataLlm, create_llm
from beauty_company.adapters.mc_text import compose

FOUNDER = Actor("founder", "FOUNDER", "Founder")


class MarketingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.company = Company(Path(self.temp.name) / "test.sqlite3")

    def test_failed_generation_retains_record(self):
        with patch.object(self.company.llm, "generate_script", return_value={"script": "Invalid claim", "claims": ["Cures eczema"]}):
            with self.company.store.transaction() as db:
                result = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Promote skincare", "productId": "P-101"})

        self.assertEqual(result["status"], "CONTENT_REJECTED")
        self.assertEqual(result["payload"]["failure"]["code"], "CONTENT_REJECTED")
        self.assertNotIn("approvalId", result["payload"])

        with self.company.store.read() as db:
            saved = Store.get(db, result["id"], "MC")
            approvals = db.execute("SELECT COUNT(*) FROM approvals WHERE origin_id=?", (result["id"],)).fetchone()[0]

        self.assertEqual(saved["status"], "CONTENT_REJECTED")
        self.assertEqual(approvals, 0)

    def test_mc_t_03_mutating_media_input_cannot_validate_its_own_changed_frames(self):
        generate = self.company.mc.media.generate

        def mutate(script):
            script["storyboard"][0]["caption"] = "Guaranteed cure for eczema"
            return generate(script)

        with patch.object(self.company.mc.media, "generate", side_effect=mutate):
            with self.company.store.transaction() as db:
                result = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Promote skincare", "productId": "P-101"})
        self.assertEqual(result["status"], "GENERATION_FAILED")
        self.assertNotIn("approvalId", result["payload"])
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM approvals").fetchone()[0], 0)

    def test_mc_t_03_model_cannot_rewrite_the_evidence_it_is_checked_against(self):
        generate = self.company.llm.generate_script

        def mutate(brief, evidence):
            evidence["facts"][0] = "Guaranteed cure for eczema"
            return generate(brief, evidence)

        with patch.object(self.company.llm, "generate_script", side_effect=mutate):
            with self.company.store.transaction() as db:
                result = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Promote skincare", "productId": "P-101"})
        self.assertEqual(result["status"], "CONTENT_REJECTED")
        with self.company.store.read() as db:
            self.assertNotIn("Guaranteed cure", db.execute("SELECT facts FROM products WHERE id='P-101'").fetchone()[0])
            self.assertEqual(db.execute("SELECT COUNT(*) FROM approvals").fetchone()[0], 0)

    def test_mc_t_03_media_input_text_mutation_cannot_replace_the_saved_script(self):
        generate = self.company.mc.media.generate

        def mutate(script):
            script["script"] = "Guaranteed cure for eczema"
            script["claims"].append("Guaranteed cure for eczema")
            return generate(script)

        with patch.object(self.company.mc.media, "generate", side_effect=mutate):
            with self.company.store.transaction() as db:
                result = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Promote skincare", "productId": "P-101"})
        self.assertEqual(result["status"], "REVIEW_PENDING")
        self.assertNotIn("Guaranteed cure", result["payload"]["script"])
        self.assertNotIn("Guaranteed cure for eczema", result["payload"]["claims"])

    def test_mc_t_03_unsupported_storyboard_metadata_is_withheld(self):
        generate = self.company.llm.generate_script

        def mutate(brief, evidence):
            script = generate(brief, evidence)
            script["storyboard"][0]["duration"] = "Guaranteed cure for eczema"
            return script

        with patch.object(self.company.llm, "generate_script", side_effect=mutate):
            with self.company.store.transaction() as db:
                result = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Promote skincare", "productId": "P-101"})
        self.assertEqual(result["status"], "CONTENT_REJECTED")
        self.assertNotIn("approvalId", result["payload"])

    def test_mc_t_06_failed_http_revision_remains_a_visible_failed_contract(self):
        router = Router(self.company)
        headers = {"Host": "127.0.0.1:5620", "Content-Type": "application/json"}
        login = router.handle("POST", "/api/login", headers,
                              json.dumps({"username": "founder", "password": "founder-demo"}).encode())
        headers.update({"Cookie": login.headers["Set-Cookie"].split(";")[0],
                        "X-CSRF-Token": json.loads(login.body)["csrf"]})
        response = router.handle("POST", "/api/campaigns", headers,
                                 json.dumps({"brief": "A valid campaign", "productId": "P-101"}).encode())
        self.assertEqual(response.status, 201)
        original = json.loads(response.body)
        response = router.handle("POST", f"/api/campaigns/{original['id']}/revise", headers,
                                 json.dumps({"brief": "   ", "productId": "P-101", "contextRevision": 1}).encode())
        self.assertEqual(response.status, 200)
        revised = json.loads(response.body)
        self.assertEqual((revised["status"], revised["revision"]), ("INCOMPLETE", 2))
        self.assertIn("failure", revised["payload"])
        self.assertNotIn("approvalId", revised["payload"])
        snapshot = json.loads(router.handle("GET", "/api/snapshot", headers).body)
        self.assertEqual(snapshot["records"][0]["payload"]["history"][0]["revision"], 1)
        self.assertEqual(snapshot["approvals"][0]["status"], "SUPERSEDED")
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM approvals").fetchone()[0], 1)

    def test_media_generation_failure(self):
        with patch.object(self.company.mc.media, "generate", side_effect=RuntimeError("Media service unavailable")):
            with self.assertRaises(DomainError) as caught:
                with self.company.store.transaction() as db:
                    self.company.mc.submit(db, FOUNDER, {"brief": "Promote skincare", "productId": "P-101"})
        self.assertEqual(caught.exception.code, "GENERATION_FAILED")
        with self.company.store.read() as db:
            approvals = db.execute("SELECT COUNT(*) FROM approvals WHERE origin_role='MC'").fetchone()[0]
        self.assertEqual(approvals, 0)

    def test_failed_draft_can_be_revised(self):
        with patch.object(self.company.llm, "generate_script", return_value={"script": "Invalid", "claims": ["Guaranteed cure"]}):
            with self.company.store.transaction() as db:
                failed = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Promote skincare", "productId": "P-101"})

        self.assertEqual(failed["status"], "CONTENT_REJECTED")
        self.assertEqual(failed["revision"], 1)

        with self.company.store.transaction() as db:
            revised = self.company.mc.revise(db, FOUNDER, failed["id"], {"contextRevision": 1, "brief": "Promote gentle skincare", "productId": "P-101"})

        self.assertEqual(revised["revision"], 2)
        self.assertEqual(revised["status"], "REVIEW_PENDING")
        self.assertEqual(revised["payload"]["history"][0]["revision"], 1)
        self.assertEqual(revised["payload"]["history"][0]["status"], "CONTENT_REJECTED")
        self.assertNotIn("approvalId", revised["payload"]["history"][0]["payload"])
        self.assertIn("approvalId", revised["payload"])

    def test_failed_revision_retains_history(self):
        with self.company.store.transaction() as db:
            original = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Promote skincare", "productId": "P-101"})

        with patch.object(self.company.llm, "generate_script", return_value={"script": "Invalid", "claims": ["Guaranteed cure"]}):
            with self.company.store.transaction() as db:
                revised = self.company.mc.revise(db, FOUNDER, original["id"], {"contextRevision": 1, "brief": "Revised promotion", "productId": "P-101"})

        self.assertEqual(revised["revision"], 2)
        self.assertEqual(revised["status"], "CONTENT_REJECTED")
        self.assertEqual(revised["payload"]["history"][0]["revision"], 1)
        self.assertNotIn("approvalId", revised["payload"])
        with self.company.store.read() as db:
            saved = Store.get(db, original["id"], "MC")
            self.assertEqual(saved["revision"], 2)
            self.assertEqual(saved["status"], "CONTENT_REJECTED")

    def test_stale_revision_cannot_overwrite_current_draft(self):
        with self.company.store.transaction() as db:
            original = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Original campaign", "productId": "P-101"})
        with self.company.store.transaction() as db:
            revised = self.company.mc.revise(db, FOUNDER, original["id"], {"contextRevision": 1, "brief": "Updated campaign", "productId": "P-101"})
        self.assertEqual(revised["revision"], 2)

        with self.assertRaises(DomainError) as caught:
            with self.company.store.transaction() as db:
                self.company.mc.revise(db, FOUNDER, original["id"], {"contextRevision": 1, "brief": "Outdated campaign", "productId": "P-101"})

        self.assertEqual(caught.exception.code, "STALE_SCOPE")

        with self.company.store.read() as db:
            saved = Store.get(db, original["id"], "MC")

        self.assertEqual(saved["revision"], 2)
        self.assertEqual(saved["payload"]["brief"], "Updated campaign")

    def test_unsupported_script_content_blocks_review(self):
        fake = {"script": "Daily Hydration Cream guarantees a cure for eczema.", "claims": ["Fragrance-free"], "storyboard": [{"shot": 1, "duration": "0-5 s", "caption": "Fragrance-free", "direction": "Product introduction"}], "simulated": True}
        with patch.object(self.company.llm, "generate_script", return_value=fake):
            with self.company.store.transaction() as db:
                result = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Promote skincare", "productId": "P-101"})
        self.assertEqual(result["status"], "CONTENT_REJECTED")
        self.assertNotIn("approvalId", result["payload"])
        with self.company.store.read() as db:
            saved = Store.get(db, result["id"], "MC")
            approvals = db.execute("SELECT COUNT(*) FROM approvals WHERE origin_id=?", (result["id"],)).fetchone()[0]
        self.assertEqual(saved["status"], "CONTENT_REJECTED")
        self.assertEqual(approvals, 0)
    def test_unsupported_storyboard_content_blocks_review(self):
        fake = {"script": "Meet Daily Hydration Cream. Moisturises dry skin. Fragrance-free. 50 ml.", "claims": ["Moisturises dry skin", "Fragrance-free", "50 ml"], "storyboard": [{"shot": 1, "duration": "0–5 s", "caption": "Daily Hydration Cream", "direction": "Product introduction"}, {"shot": 2, "duration": "5–10 s", "caption": "Guaranteed cure for eczema", "direction": "Catalogue-supported benefit"}, {"shot": 3, "duration": "10–15 s", "caption": "Explore the product details", "direction": "Draft closing card"}], "simulated": True}
        with patch.object(self.company.llm, "generate_script", return_value=fake):
            with self.company.store.transaction() as db:
                result = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Promote skincare", "productId": "P-101"})
        self.assertEqual(result["status"], "CONTENT_REJECTED")
        self.assertNotIn("approvalId", result["payload"])
        with self.company.store.read() as db:
            approvals = db.execute("SELECT COUNT(*) FROM approvals WHERE origin_id=?", (result["id"],)).fetchone()[0]
        self.assertEqual(approvals, 0)
    def test_modified_media_output_blocks_review(self):
        fake_media = {"kind": "MOCK_STORYBOARD", "simulated": True, "label": "Storyboard placeholder; no video file has been generated.", "frames": [{"shot": 1, "caption": "Guaranteed cure for eczema"}]}
        with patch.object(self.company.mc.media, "generate", return_value=fake_media):
            with self.company.store.transaction() as db:
                result = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Promote skincare", "productId": "P-101"})
        self.assertEqual(result["status"], "GENERATION_FAILED")
        self.assertNotIn("approvalId", result["payload"])
        with self.company.store.read() as db:
            saved = Store.get(db, result["id"], "MC")
            approvals = db.execute("SELECT COUNT(*) FROM approvals WHERE origin_id=?", (result["id"],)).fetchone()[0]
        self.assertEqual(saved["status"], "GENERATION_FAILED")
        self.assertEqual(approvals, 0)
    def test_revision_supersedes_previous_approval(self):
        with self.company.store.transaction() as db:
            original = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Original campaign", "productId": "P-101"})
        old_approval = original["payload"]["approvalId"]
        with patch.object(self.company.llm, "generate_script", return_value={"script": "Invalid", "claims": ["Guaranteed cure"]}):
            with self.company.store.transaction() as db:
                revised = self.company.mc.revise(db, FOUNDER, original["id"], {"contextRevision": 1, "brief": "Revised campaign", "productId": "P-101"})

        self.assertEqual(revised["revision"], 2)
        self.assertEqual(revised["status"], "CONTENT_REJECTED")
        self.assertNotIn("approvalId", revised["payload"])

        with self.company.store.read() as db:
            approval = self.company.ap.get(db, old_approval)
            saved = Store.get(db, original["id"], "MC")

        self.assertEqual(approval["status"], "SUPERSEDED")
        self.assertEqual(saved["payload"]["history"][0]["payload"]["approvalId"], old_approval)
    def test_customer_cannot_create_or_revise_campaign(self):
        customer = Actor("customer", "CUSTOMER", "Customer")
        with self.assertRaises(DomainError) as caught:
            with self.company.store.transaction() as db:
                self.company.mc.submit_draft(db, customer, {"brief": "Unauthorised campaign", "productId": "P-101"})
        self.assertEqual(caught.exception.code, "FORBIDDEN")
        with self.company.store.transaction() as db:
            original = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Authorised campaign", "productId": "P-101"})
        with self.assertRaises(DomainError) as caught:
            with self.company.store.transaction() as db:
                self.company.mc.revise(db, customer, original["id"], {"contextRevision": 1, "brief": "Unauthorised revision", "productId": "P-101"})
        self.assertEqual(caught.exception.code, "FORBIDDEN")
        with self.company.store.read() as db:
            saved = Store.get(db, original["id"], "MC")
            count = db.execute("SELECT COUNT(*) FROM records WHERE kind='MC'").fetchone()[0]
        self.assertEqual(saved["revision"], 1)
        self.assertEqual(count, 1)
    def test_missing_product_retains_incomplete_record(self):
        with self.company.store.transaction() as db:
            result = self.company.mc.submit_draft(db, FOUNDER, {"brief": "Promote skincare", "productId": "UNKNOWN"})

        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertNotIn("approvalId", result["payload"])

        with self.company.store.read() as db:
            saved = Store.get(db, result["id"], "MC")
            approvals = db.execute("SELECT COUNT(*) FROM approvals WHERE origin_id=?", (result["id"],)).fetchone()[0]

        self.assertEqual(saved["status"], "INCOMPLETE")
        self.assertEqual(approvals, 0)


class LivePlanFixture(MockLlm):
    """Offline test double only; actual model evidence is recorded separately."""
    mc_simulated = False

    def generate_script(self, brief, evidence):
        calm = 'calm' in brief.lower()
        fact = evidence['facts'][1 if calm else -1]
        return compose({'productId': evidence['id'], 'style': 'CALM' if calm else 'ENERGETIC',
                        'briefRef': brief, 'factRefs': [fact], 'featureFact': fact}, brief, evidence)


class LiveMarketingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)/'live-mc.sqlite3'
        self.company = Company(self.path, llm=LivePlanFixture())
        self.brief = 'A calm introduction focused on Fragrance-free.'
        self.data = {'brief': self.brief, 'productId': 'P-101'}

    def saved(self, rid):
        with self.company.store.read() as db: return Store.get(db, rid, 'MC')

    def no_effects(self):
        with self.company.store.read() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM effects').fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-101'").fetchone()[0], 12)

    def test_mc_t_01_opt_in_is_separate_and_default_mc_remains_mock(self):
        with self.assertRaises(ValueError): create_llm('mock', mc_live=True)
        llm = StrataLlm(LlmConfig('http://127.0.0.1:8080/v1', 'test-model'))
        with patch.object(llm, '_complete', side_effect=AssertionError('Explicit opt-in required')):
            result = llm.generate_script(self.brief, {'name': 'Demo', 'facts': ['Fact']})
        self.assertTrue(result['simulated']); self.assertTrue(llm.mc_simulated)
        self.assertEqual(self.company.mode()['mc'], 'LIVE')
        self.assertEqual(self.company.mode()['ba'], 'MOCK')
        self.assertEqual(self.company.mode()['csIntent'], 'NOT_CONNECTED')

    def test_mc_t_01_actual_shared_transport_receives_only_brief_and_product_evidence(self):
        with self.company.store.read() as db:
            from beauty_company.modules.beauty_advisor import catalogue
            product = catalogue(db)[0]
        plan = {'productId': 'P-101', 'style': 'CALM', 'briefRef': 'calm',
                'factRefs': ['Fragrance-free'], 'featureFact': 'Fragrance-free'}
        llm = StrataLlm(LlmConfig('http://127.0.0.1:8080/v1', 'test-model'), mc_live=True)
        response = io.BytesIO(json.dumps({'model': 'test-model', 'choices': [
            {'finish_reason': 'stop', 'message': {'content': json.dumps(plan)}}]}).encode())
        response.status = 200
        with patch.object(llm.opener, 'open', return_value=response) as opened:
            script = llm.generate_script(self.brief, product)
        sent = json.loads(opened.call_args.args[0].data)
        value = json.loads(sent['messages'][1]['content'])
        self.assertEqual(set(value), {'brief', 'product'})
        self.assertEqual(set(value['product']), {'id', 'name', 'facts', 'version'})
        self.assertFalse(script['simulated'])
        self.assertEqual(script['claims'], ['Fragrance-free'])
        self.assertIn('Fragrance-free', script['script'])
        self.assertNotIn('Moisturises dry skin', script['script'])

    def test_mc_t_03_invalid_live_plan_cannot_fall_back_to_mock(self):
        product = {'id': 'P-101', 'name': 'Demo', 'facts': ['Fragrance-free'], 'version': 1}
        good = {'productId': 'P-101', 'style': 'CALM', 'briefRef': 'calm',
                'factRefs': ['Fragrance-free'], 'featureFact': 'Fragrance-free'}
        llm = StrataLlm(LlmConfig('http://127.0.0.1:8080/v1', 'test-model'), mc_live=True)
        for bad in (None, {**good, 'script': 'Invented prose'}, {**good, 'productId': 'FORGED'},
                    {**good, 'style': 'CURES_ECZEMA'}, {**good, 'briefRef': 'Not in brief'},
                    {**good, 'factRefs': ['Invented benefit']}, {**good, 'featureFact': 'Invented caption'}):
            with self.subTest(bad=bad), patch.object(llm, '_complete', return_value=bad), \
                    patch.object(MockLlm, 'generate_script', side_effect=AssertionError('No fallback')):
                with self.assertRaises(ModelError) as caught: llm.generate_script(self.brief, product)
                self.assertEqual(caught.exception.code, 'LLM_INVALID_OUTPUT')

    def test_mc_t_01_live_draft_uses_existing_exact_scope_approval(self):
        record = self.company.campaign(FOUNDER, self.data)
        self.assertEqual(record['status'], 'REVIEW_PENDING')
        p = record['payload']; self.assertFalse(p['simulated']); self.assertFalse(p['textSimulated'])
        self.assertTrue(p['media']['simulated']); self.assertEqual(p['media']['kind'], 'MOCK_STORYBOARD')
        self.assertEqual(p['claims'], ['Fragrance-free'])
        with self.company.store.read() as db:
            review = self.company.ap.get(db, p['approvalId'])
            self.assertEqual(review['action'], {'kind': 'REVIEW_TEXT_DRAFT', 'draftId': record['id'],
                'draftRevision': 1, 'textMode': 'LIVE', 'mediaKind': 'MOCK_STORYBOARD'})
        self.company.decide(FOUNDER, p['approvalId'], {'decision': 'APPROVE', 'reason': 'Checked this text and mock media.', 'contextRevision': 1})
        current = self.saved(record['id']); self.assertEqual(current['status'], 'APPROVED')
        self.assertIn('decisionId', current['payload']); self.no_effects()

    def test_mc_t_06_live_revision_has_new_content_and_no_inherited_approval(self):
        first = self.company.campaign(FOUNDER, self.data); old = first['payload']['approvalId']
        current = self.company.campaign(FOUNDER, {'brief': 'An energetic focus on 50 ml.', 'productId': 'P-101',
                                                'contextRevision': 1}, first['id'])
        self.assertEqual(current['revision'], 2)
        self.assertEqual(current['payload']['textPlan']['style'], 'ENERGETIC')
        self.assertNotEqual(current['payload']['script'], first['payload']['script'])
        self.assertNotEqual(current['payload']['approvalId'], old)
        with self.company.store.read() as db: self.assertEqual(self.company.ap.get(db, old)['status'], 'SUPERSEDED')
        with self.assertRaises(DomainError):
            self.company.decide(FOUNDER, old, {'decision': 'APPROVE', 'reason': 'Old scope', 'contextRevision': 1})
        self.assertEqual(self.saved(first['id'])['status'], 'REVIEW_PENDING')
        self.no_effects()

    def test_mc_t_03_provider_failure_is_saved_without_text_media_or_review(self):
        for code in ('LLM_UNAVAILABLE', 'LLM_TIMEOUT', 'LLM_INVALID_OUTPUT'):
            with patch.object(self.company.llm, 'generate_script', side_effect=ModelError('Safe model failure', 503, code)):
                record = self.company.campaign(FOUNDER, self.data)
            self.assertEqual(record['status'], 'CONTENT_REJECTED' if code=='LLM_INVALID_OUTPUT' else 'GENERATION_FAILED')
            self.assertFalse(record['payload']['simulated'])
            self.assertEqual(record['payload']['failure']['code'], code)
            for field in ('script', 'media', 'approvalId'): self.assertNotIn(field, record['payload'])
        with self.company.store.read() as db: self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0], 0)

    def test_mc_t_03_actual_script_and_captions_are_checked_not_just_claims(self):
        original = self.company.llm.generate_script
        for target in ('script', 'caption', 'direction', 'duration'):
            def tamper(brief, evidence):
                value = original(brief, evidence)
                if target == 'script': value['script'] += ' Guaranteed cure.'
                else: value['storyboard'][1][target] = 'Unsupported claim'
                return value
            with self.subTest(target=target), patch.object(self.company.llm, 'generate_script', side_effect=tamper):
                record = self.company.campaign(FOUNDER, self.data)
                self.assertEqual(record['status'], 'CONTENT_REJECTED')
                self.assertNotIn('approvalId', record['payload'])

    def test_mc_t_03_model_cannot_mutate_its_own_catalogue_evidence(self):
        original = self.company.llm.generate_script
        def mutate(brief, product):
            product['facts'][1] = 'Guaranteed cure'
            return original(brief, product)
        with patch.object(self.company.llm, 'generate_script', side_effect=mutate):
            record = self.company.campaign(FOUNDER, self.data)
        self.assertEqual(record['status'], 'CONTENT_REJECTED'); self.assertNotIn('approvalId', record['payload'])

    def test_mc_t_06_inference_releases_write_lock_and_old_revision_is_discarded(self):
        original = self.company.llm.generate_script; entered=threading.Event(); release=threading.Event()
        def delayed(brief, product):
            if 'calm' in brief:
                entered.set(); self.assertTrue(release.wait(10))
            return original(brief, product)
        with patch.object(self.company.llm, 'generate_script', side_effect=delayed), ThreadPoolExecutor(1) as pool:
            future = pool.submit(self.company.campaign, FOUNDER, self.data)
            try:
                self.assertTrue(entered.wait(5))
                with self.company.store.read() as db: rid=db.execute("SELECT id FROM records WHERE kind='MC'").fetchone()[0]
                current=self.company.campaign(FOUNDER, {'brief':'An energetic focus on 50 ml.', 'productId':'P-101','contextRevision':1},rid)
            finally: release.set()
            with self.assertRaises(DomainError) as caught: future.result(5)
            self.assertEqual(caught.exception.code,'STALE_SCOPE')
        self.assertEqual(self.saved(rid)['revision'],current['revision'])
        with self.company.store.read() as db: self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0],1)

    def test_mc_t_03_current_catalogue_is_rechecked_before_review(self):
        original = self.company.llm.generate_script
        def change(brief, product):
            with self.company.store.transaction() as db: db.execute("UPDATE products SET version=2 WHERE id='P-101'")
            return original(brief, product)
        with patch.object(self.company.llm, 'generate_script', side_effect=change):
            record = self.company.campaign(FOUNDER,self.data)
        self.assertEqual(record['status'],'INCOMPLETE')
        self.assertEqual(record['payload']['failure']['code'],'MC_STALE_EVIDENCE')
        self.assertNotIn('approvalId',record['payload'])

    def test_mc_t_06_failed_final_save_cannot_leave_approval_or_success(self):
        original=Store.save
        def fail(db,item):
            if item['status']=='REVIEW_PENDING': raise sqlite3.OperationalError('Private database detail')
            return original(db,item)
        with patch.object(Store,'save',side_effect=fail), self.assertRaises(DomainError) as caught:
            self.company.campaign(FOUNDER,self.data)
        with self.company.store.read() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0],0)
            saved=Store.get(db,db.execute("SELECT id FROM records WHERE kind='MC'").fetchone()[0])
        self.assertEqual(caught.exception.code,'MC_STORAGE_UNAVAILABLE')
        self.assertEqual(saved['status'],'RECORDING_FAILED'); self.assertNotIn('script',saved['payload'])
        self.assertIn('pendingGeneration',saved['payload'])

    def test_mc_t_01_http_live_route_requires_founder_csrf_and_exact_fields(self):
        router=Router(self.company); base={'Host':'127.0.0.1:5711','Content-Type':'application/json'}
        body=json.dumps(self.data).encode()
        self.assertEqual(router.handle('POST','/api/campaigns',base,body).status,401)
        for user,expected in (('customer',403),('founder',201)):
            token,csrf,_=self.company.login(user,user+'-demo')
            headers={**base,'Cookie':'beauty_session='+token,'X-CSRF-Token':csrf}
            self.assertEqual(router.handle('POST','/api/campaigns',{**headers,'X-CSRF-Token':''},body).status,403)
            response=router.handle('POST','/api/campaigns',headers,body)
            self.assertEqual(response.status,expected)
        response=router.handle('POST','/api/campaigns',headers,json.dumps({**self.data,'approved':True}).encode())
        self.assertEqual(response.status,400)


class TemplateVideoTests(unittest.TestCase):
    """Offline media boundaries. Stub bytes are never presented as playback evidence."""
    def setUp(self):
        from beauty_company.adapters.template_video import TemplateVideo, VideoConfig
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = VideoConfig('missing-ffmpeg', 'missing-ffprobe', 'missing-font', str(self.root/'artifacts'))
        self.media = TemplateVideo(self.config)
        self.company = Company(self.root/'test.sqlite3', llm=LivePlanFixture(), media=self.media)
        self.data = {'brief':'A calm Fragrance-free introduction.', 'productId':'P-101'}

    def artifact(self, script):
        from beauty_company.adapters.template_video import LABEL, digest, script_digest
        raw=b'OFFLINE STUB - NOT A PLAYABLE VIDEO'
        aid='a'*32; job=self.media.root/aid; job.mkdir(parents=True,exist_ok=False)
        (job/'draft.mp4').write_bytes(raw)
        value={'kind':'TEMPLATE_VIDEO','simulated':False,'modelGenerated':False,'label':LABEL,
               'frames':script['storyboard'],'artifactId':aid,'sha256':digest(raw),'scriptSha256':script_digest(script),
               'bytes':len(raw),'mime':'video/mp4','durationSeconds':15,'width':720,'height':1280,'fps':24,'audio':False}
        (job/'manifest.json').write_text(json.dumps(value),encoding='utf-8')
        return value

    def draft(self):
        with patch.object(self.media,'generate',side_effect=self.artifact):
            return self.company.campaign(FOUNDER,self.data)

    def test_mc_t_04_template_hash_is_bound_to_existing_review(self):
        record=self.draft(); value=record['payload']; self.assertFalse(value['mediaSimulated'])
        self.assertEqual(record['status'],'REVIEW_PENDING'); self.assertFalse(value['media']['modelGenerated'])
        with self.company.store.read() as db:
            review=self.company.ap.get(db,value['approvalId'])
        self.assertEqual(review['action']['mediaSha256'],value['media']['sha256'])
        self.assertEqual(review['action']['scriptSha256'],value['media']['scriptSha256'])
        self.assertEqual(review['action']['mediaKind'],'TEMPLATE_VIDEO')
        self.company.decide(FOUNDER,review['id'],{'contextRevision':1,'decision':'APPROVE','reason':'Review offline stub scope only.'})
        with self.company.store.read() as db:
            saved=Store.get(db,record['id']); self.assertEqual(saved['status'],'APPROVED')
            self.assertEqual(db.execute('SELECT count(*) FROM effects').fetchone()[0],0)

    def test_mc_t_04_unavailable_timeout_and_encoder_failure_have_no_fallback_or_review(self):
        from beauty_company.adapters.template_video import failed
        record=self.company.campaign(FOUNDER,self.data)
        self.assertEqual(record['payload']['failure']['code'],'MEDIA_UNAVAILABLE')
        for code in ('MEDIA_TIMEOUT','MEDIA_GENERATION_FAILED','MEDIA_CONTENT_REJECTED'):
            with self.subTest(code=code), patch.object(self.media,'generate',side_effect=failed(code)):
                record=self.company.campaign(FOUNDER,self.data)
            self.assertEqual(record['status'],'GENERATION_FAILED')
            self.assertEqual(record['payload']['failure']['code'],code)
            self.assertNotIn('media',record['payload']);self.assertNotIn('approvalId',record['payload'])

    def test_mc_t_05_modified_file_or_manifest_cannot_be_downloaded(self):
        record=self.draft(); value=record['payload']['media']; job=self.media.root/value['artifactId']
        (job/'draft.mp4').write_bytes(b'MODIFIED')
        with self.assertRaises(DomainError): self.company.campaign_media(FOUNDER,record['id'],1)
        for identifier in ('../escape','a/b','A'*32):
            with self.subTest(identifier=identifier),self.assertRaises(DomainError):
                self.media.read({**value,'artifactId':identifier})

    def test_mc_t_05_wrong_frames_or_script_hash_blocks_review(self):
        original=self.artifact
        def altered(script):
            result=original(script);result['frames'][1]['caption']='Invented cure';return result
        with patch.object(self.media,'generate',side_effect=altered):
            record=self.company.campaign(FOUNDER,self.data)
        self.assertEqual(record['status'],'GENERATION_FAILED');self.assertNotIn('approvalId',record['payload'])

    def test_mc_t_06_stale_media_url_cannot_serve_previous_or_replacement_video(self):
        record=self.draft()
        with patch.object(self.media,'generate',side_effect=DomainError('Unavailable',503,'MEDIA_UNAVAILABLE')):
            changed=self.company.campaign(FOUNDER,{**self.data,'contextRevision':1},record['id'])
        self.assertEqual(changed['revision'],2)
        with self.assertRaises(DomainError) as caught: self.company.campaign_media(FOUNDER,record['id'],1)
        self.assertEqual(caught.exception.code,'STALE_SCOPE')
        with self.assertRaises(DomainError): self.company.campaign_media(FOUNDER,record['id'],2)

    def test_mc_t_04_authenticated_http_ranges_and_role_guards(self):
        from beauty_company.http import Router
        record=self.draft(); router=Router(self.company); token,csrf,_=self.company.login('founder','founder-demo')
        path=f"/api/campaigns/{record['id']}/media/1"
        headers={'Host':'127.0.0.1:5720','Cookie':'beauty_session='+token}
        self.assertEqual(router.handle('GET',path,{'Host':'127.0.0.1:5720'}).status,401)
        for requested,expected,length in [('bytes=0-9',206,10),('bytes=-5',206,5),('bytes=9999-',416,0),('bytes=0-1,2-3',416,0)]:
            response=router.handle('GET',path,{**headers,'Range':requested})
            self.assertEqual(response.status,expected);self.assertEqual(len(response.body),length)
        raw=router.handle('GET',path,headers);self.assertEqual(raw.status,200)
        self.assertEqual(raw.headers['Content-Type'],'video/mp4')
        with self.assertRaises(DomainError): self.company.campaign_media(Actor("alex", "CUSTOMER", "Alex"),record['id'],1)

    def test_mc_t_04_config_relative_paths_and_timeouts_are_explicit(self):
        from beauty_company.adapters.template_video import VideoConfig
        path=self.root/'local.json'; values={'ffmpeg':'bin/ffmpeg','ffprobe':'bin/ffprobe','font':'font.ttf','output_dir':'output'}
        path.write_text(json.dumps(values)); config=VideoConfig.load(path)
        self.assertEqual(Path(config.output_dir),self.root/'output')
        for timeout in (True,0,301):
            path.write_text(json.dumps({**values,'timeout_seconds':timeout}))
            with self.assertRaises(ValueError): VideoConfig.load(path)

    def test_mc_t_04_encoder_timeout_and_process_failure_are_retained(self):
        import subprocess
        for name in ('ffmpeg','ffprobe','font'): (self.root/name).touch()
        from beauty_company.adapters.template_video import TemplateVideo,VideoConfig
        adapter=TemplateVideo(VideoConfig(*(str(self.root/x) for x in ('ffmpeg','ffprobe','font')),str(self.root/'render')))
        for failure in (subprocess.TimeoutExpired('ffmpeg',1),subprocess.CalledProcessError(1,'ffmpeg')):
            with self.subTest(failure=type(failure).__name__), patch.object(adapter,'run',side_effect=failure):
                self.company.mc.media=adapter
                record=self.company.campaign(FOUNDER,self.data)
            self.assertEqual(record['status'],'GENERATION_FAILED');self.assertNotIn('approvalId',record['payload'])

        for text_file in adapter.root.rglob('*.txt'):
            self.assertNotIn(b'\r', text_file.read_bytes())

    def test_mc_t_04_mock_text_can_explicitly_render_without_a_live_model(self):
        self.company=Company(self.root/'mock.sqlite3',media=self.media)
        record=self.draft(); self.assertTrue(record['payload']['textSimulated'])
        self.assertFalse(record['payload']['mediaSimulated'])
        self.assertEqual(record['payload']['media']['kind'],'TEMPLATE_VIDEO')


    def test_mc_t_05_wrong_probe_format_cannot_create_review(self):
        import subprocess
        from beauty_company.adapters.template_video import TemplateVideo, VideoConfig
        for name in ('ffmpeg','ffprobe','font'): (self.root/name).touch()
        adapter=TemplateVideo(VideoConfig(*(str(self.root/x) for x in ('ffmpeg','ffprobe','font')),str(self.root/'render')))
        self.company.mc.media=adapter
        bad={'streams':[{'codec_type':'video','codec_name':'h264','width':320,'height':240,'pix_fmt':'yuv420p','nb_frames':'360'}],
             'format':{'duration':'15'}}
        with patch.object(adapter,'run',side_effect=[subprocess.CompletedProcess([],0,b'',b''),
                    subprocess.CompletedProcess([],0,json.dumps(bad).encode(),b'')]):
            record=self.company.campaign(FOUNDER,self.data)
        self.assertEqual(record['status'],'GENERATION_FAILED')
        self.assertEqual(record['payload']['failure']['code'],'MEDIA_CONTENT_REJECTED')
        self.assertNotIn('approvalId',record['payload'])

    def test_mc_t_06_template_recovery_uses_same_artifact_after_restart_without_render(self):
        self.company.set_fault(FOUNDER,'mc_recording')
        with patch.object(self.media,'generate',side_effect=self.artifact):
            with self.assertRaises(DomainError): self.company.campaign(FOUNDER,self.data)
        with self.company.store.read() as db:
            rid=db.execute("SELECT id FROM records WHERE kind='MC'").fetchone()[0]
            pending=Store.get(db,rid)['payload']['pendingGeneration']['payload']['media']
        restarted=Company(self.root/'test.sqlite3',media=self.media)
        with patch.object(restarted.llm,'generate_script',side_effect=AssertionError('No model')), \
                patch.object(self.media,'generate',side_effect=AssertionError('No renderer')):
            result=restarted.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.assertFalse(result['payload']['textSimulated']); self.assertFalse(result['payload']['mediaSimulated'])
        self.assertEqual(result['payload']['media'],pending)
        with self.company.store.read() as db:
            review=self.company.ap.get(db,result['payload']['approvalId'])
        self.assertEqual(review['action']['mediaSha256'],pending['sha256'])
        restarted.mc_generation.cancel(FOUNDER,rid,{'contextRevision':1})
        with self.assertRaises(DomainError): restarted.campaign_media(FOUNDER,rid,1)

    def test_mc_t_06_template_recovery_requires_original_config_and_untampered_artifact(self):
        self.company.set_fault(FOUNDER,'mc_recording')
        with patch.object(self.media,'generate',side_effect=self.artifact):
            with self.assertRaises(DomainError): self.company.campaign(FOUNDER,self.data)
        with self.company.store.read() as db: rid=db.execute("SELECT id FROM records WHERE kind='MC'").fetchone()[0]
        with self.assertRaises(DomainError) as caught:
            Company(self.root/'test.sqlite3').mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(caught.exception.code,'MC_MEDIA_RECOVERY_UNAVAILABLE')
        with self.company.store.read() as db: self.assertIn('pendingGeneration',Store.get(db,rid)['payload'])
        (self.media.root/('a'*32)/'draft.mp4').write_bytes(b'MODIFIED')
        result=self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(result['status'],'CONTENT_REJECTED'); self.assertNotIn('media',result['payload'])
        with self.company.store.read() as db: self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0],0)


class McRecoveryTests(unittest.TestCase):
    """Durable generation recovery, real SQLite rollback and exact-revision controls."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)/'recovery.sqlite3'
        self.company = Company(self.path, llm=LivePlanFixture())
        self.data = {'brief': 'A calm Fragrance-free introduction.', 'productId': 'P-101'}

    def saved(self, rid):
        with self.company.store.read() as db: return Store.get(db, rid, 'MC')

    def pending(self):
        self.company.set_fault(FOUNDER, 'mc_recording')
        with self.assertRaises(DomainError) as caught: self.company.campaign(FOUNDER, self.data)
        self.assertEqual(caught.exception.code, 'MC_RECORDING_FAILED')
        with self.company.store.read() as db:
            rid=db.execute("SELECT id FROM records WHERE kind='MC' ORDER BY rowid DESC").fetchone()[0]
        self.assertEqual(self.saved(rid)['status'], 'RECORDING_FAILED')
        self.assertNotIn('approvalId', self.saved(rid)['payload'])
        return rid

    def counts(self, rid):
        with self.company.store.read() as db:
            return (db.execute('SELECT count(*) FROM approvals WHERE origin_id=?',(rid,)).fetchone()[0],
                    db.execute('SELECT count(*) FROM effects').fetchone()[0])

    def test_mc_t_06_restart_recovery_keeps_live_mode_with_mock_configuration_and_no_generation(self):
        rid=self.pending(); self.company=Company(self.path)
        with patch.object(self.company.llm,'generate_script',side_effect=AssertionError('No inference')), \
                patch.object(self.company.mc.media,'generate',side_effect=AssertionError('No render')):
            result=self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(result['status'],'REVIEW_PENDING')
        self.assertFalse(result['payload']['textSimulated']); self.assertTrue(result['payload']['mediaSimulated'])
        self.assertEqual(self.counts(rid),(1,0))

    def test_mc_t_06_real_audit_abort_rolls_back_review_and_recovers_once(self):
        with self.company.store.transaction() as db:
            db.execute("CREATE TRIGGER fail_mc BEFORE INSERT ON events WHEN NEW.event='GENERATION_RECORDED' BEGIN SELECT RAISE(ABORT,'private storage detail'); END")
        with self.assertRaises(DomainError) as caught: self.company.campaign(FOUNDER,self.data)
        self.assertEqual(caught.exception.code,'MC_STORAGE_UNAVAILABLE'); self.assertNotIn('private',str(caught.exception))
        with self.company.store.transaction() as db:
            rid=db.execute("SELECT id FROM records WHERE kind='MC'").fetchone()[0]
            db.execute('DROP TRIGGER fail_mc')
        self.assertEqual(self.saved(rid)['status'],'RECORDING_FAILED'); self.assertEqual(self.counts(rid),(0,0))
        self.assertIn('pendingGeneration',self.saved(rid)['payload'])
        recovered=Company(self.path).mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        repeated=self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(recovered['payload']['approvalId'],repeated['payload']['approvalId'])
        self.assertEqual(self.counts(rid),(1,0))

    def test_mc_t_06_stage_failure_has_no_draft_and_explicit_retry_is_new_revision(self):
        original=Store.save
        def fail(db,record):
            if record['payload'].get('pendingGeneration'): raise sqlite3.OperationalError('staging outage')
            return original(db,record)
        with patch.object(Store,'save',side_effect=fail), self.assertRaises(DomainError):
            self.company.campaign(FOUNDER,self.data)
        with self.company.store.read() as db: rid=db.execute("SELECT id FROM records WHERE kind='MC'").fetchone()[0]
        self.assertNotIn('pendingGeneration',self.saved(rid)['payload']); self.assertEqual(self.counts(rid),(0,0))
        with self.assertRaises(DomainError) as caught:
            self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(caught.exception.code,'NO_PENDING_RESULT')
        with patch.object(self.company.llm,'generate_script',wraps=self.company.llm.generate_script) as model:
            result=self.company.mc_generation.retry(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(model.call_count,1); self.assertEqual(result['revision'],2)
        with self.assertRaises(DomainError): self.company.mc_generation.retry(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(self.counts(rid),(1,0))

    def test_mc_t_06_total_final_write_outage_leaves_pending_generating_without_false_save_claim(self):
        with self.company.store.transaction() as db:
            db.execute("CREATE TRIGGER fail_final BEFORE INSERT ON events WHEN NEW.event='GENERATION_RECORDED' BEGIN SELECT RAISE(ABORT,'outage'); END")
            db.execute("CREATE TRIGGER fail_mark BEFORE UPDATE ON records WHEN NEW.status='RECORDING_FAILED' BEGIN SELECT RAISE(ABORT,'outage'); END")
        with self.assertRaises(DomainError): self.company.campaign(FOUNDER,self.data)
        with self.company.store.transaction() as db:
            rid=db.execute("SELECT id FROM records WHERE kind='MC'").fetchone()[0]
            db.execute('DROP TRIGGER fail_final'); db.execute('DROP TRIGGER fail_mark')
        self.assertEqual(self.saved(rid)['status'],'GENERATING'); self.assertEqual(self.counts(rid),(0,0))
        self.assertEqual(self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})['status'],'REVIEW_PENDING')

    def test_mc_t_06_concurrent_recovery_is_one_review_one_recording_event(self):
        rid=self.pending()
        with ThreadPoolExecutor(3) as pool:
            results=list(pool.map(lambda _:self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1}),range(3)))
        self.assertEqual(len({r['payload']['approvalId'] for r in results}),1)
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE entity_id=? AND event='GENERATION_RECORDED'",(rid,)).fetchone()[0],1)
        self.assertEqual(self.counts(rid),(1,0))

    def test_mc_t_06_cancel_running_request_suppresses_late_result_and_is_idempotent(self):
        entered=threading.Event(); release=threading.Event(); original=self.company.llm.generate_script
        def delayed(brief,product):
            entered.set(); self.assertTrue(release.wait(10)); return original(brief,product)
        with patch.object(self.company.llm,'generate_script',side_effect=delayed), ThreadPoolExecutor(1) as pool:
            future=pool.submit(self.company.campaign,FOUNDER,self.data)
            try:
                self.assertTrue(entered.wait(5))
                with self.company.store.read() as db: rid=db.execute("SELECT id FROM records WHERE kind='MC'").fetchone()[0]
                cancelled=self.company.mc_generation.cancel(FOUNDER,rid,{'contextRevision':1})
                again=self.company.mc_generation.cancel(FOUNDER,rid,{'contextRevision':2})
            finally: release.set()
            with self.assertRaises(DomainError) as caught: future.result(5)
        self.assertEqual(caught.exception.code,'STALE_SCOPE'); self.assertEqual(cancelled['revision'],again['revision'])
        self.assertEqual(self.saved(rid)['status'],'CANCELLED'); self.assertEqual(self.counts(rid),(0,0))
        for op in (self.company.mc_generation.retry,self.company.mc_generation.recover):
            with self.assertRaises(DomainError): op(FOUNDER,rid,{'contextRevision':2})
        with self.assertRaises(DomainError): self.company.campaign(FOUNDER,{**self.data,'contextRevision':2},rid)

    def test_mc_t_06_pending_result_cannot_be_retried_or_recovered_at_old_revision(self):
        rid=self.pending()
        with self.assertRaises(DomainError) as caught: self.company.mc_generation.retry(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(caught.exception.code,'RECOVERY_AVAILABLE')
        result=self.company.campaign(FOUNDER,{**self.data,'contextRevision':1,'brief':'An energetic focus on 50 ml.'},rid)
        self.assertEqual(result['revision'],2)
        with self.assertRaises(DomainError) as caught: self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(caught.exception.code,'STALE_SCOPE'); self.assertEqual(self.counts(rid),(1,0))

    def test_mc_t_03_recovery_revalidates_saved_text_actual_fields_and_mode(self):
        for field in ('script','frames','mode','envelope'):
            rid=self.pending()
            with self.company.store.transaction() as db:
                current=Store.get(db,rid); pending=current['payload']['pendingGeneration']; value=pending['payload']
                if field=='script': value['script']+=' Unsupported cure.'
                elif field=='frames': value['media']['frames'][0]['caption']='Unsupported cure'
                elif field=='mode': value['textSimulated']=True
                else: pending['textSimulated']=True
                Store.save(db,current)
            if field=='envelope':
                with self.assertRaises(DomainError): self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
            else:
                result=self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
                self.assertEqual(result['status'],'CONTENT_REJECTED'); self.assertNotIn('script',result['payload'])
            self.assertEqual(self.counts(rid),(0,0))

    def test_mc_t_03_recovery_rechecks_current_catalogue(self):
        rid=self.pending()
        with self.company.store.transaction() as db: db.execute("UPDATE products SET version=2 WHERE id='P-101'")
        result=self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(result['status'],'INCOMPLETE'); self.assertEqual(result['payload']['failure']['code'],'MC_STALE_EVIDENCE')
        self.assertNotIn('script',result['payload']); self.assertEqual(self.counts(rid),(0,0))

    def test_mc_t_06_snapshot_and_history_withhold_uncommitted_content(self):
        rid=self.pending()
        before=self.company.snapshot(FOUNDER)['records'][0]
        self.assertNotIn('payload',before['payload']['pendingGeneration']); self.assertNotIn('script',before['payload'])
        self.company.mc_generation.cancel(FOUNDER,rid,{'contextRevision':1})
        after=self.company.snapshot(FOUNDER)['records'][0]
        self.assertNotIn('payload',after['payload']['history'][0]['payload']['pendingGeneration'])
        self.assertEqual(self.counts(rid),(0,0))

    def test_mc_t_06_failed_generation_recovery_keeps_failure_live_label_without_fallback(self):
        self.company.set_fault(FOUNDER,'mc_recording')
        with patch.object(self.company.llm,'generate_script',side_effect=ModelError('Unavailable',503,'LLM_UNAVAILABLE')):
            with self.assertRaises(DomainError): self.company.campaign(FOUNDER,self.data)
        with self.company.store.read() as db: rid=db.execute("SELECT id FROM records WHERE kind='MC'").fetchone()[0]
        self.company=Company(self.path)
        with patch.object(self.company.llm,'generate_script',side_effect=AssertionError('No fallback')):
            result=self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(result['status'],'GENERATION_FAILED'); self.assertFalse(result['payload']['simulated'])
        self.assertEqual(result['payload']['failure']['code'],'LLM_UNAVAILABLE'); self.assertEqual(self.counts(rid),(0,0))

    def test_mc_t_06_mock_http_uses_same_durable_recovery(self):
        self.company=Company(self.path); rid=self.pending()
        result=self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.assertTrue(result['payload']['textSimulated']); self.assertTrue(result['payload']['mediaSimulated'])
        self.assertEqual(self.counts(rid),(1,0))

    def test_mc_t_06_pending_review_cancel_supersedes_authority_and_old_media_scope(self):
        result=self.company.campaign(FOUNDER,self.data); rid=result['id']; review=result['payload']['approvalId']
        self.company.mc_generation.cancel(FOUNDER,rid,{'contextRevision':1})
        with self.assertRaises(DomainError):
            self.company.decide(FOUNDER,review,{'contextRevision':1,'decision':'APPROVE','reason':'Stale'})
        with self.company.store.read() as db: self.assertEqual(self.company.ap.get(db,review)['status'],'SUPERSEDED')
        self.assertEqual(self.saved(rid)['status'],'CANCELLED')

    def test_mc_t_06_recovery_after_committed_decision_does_not_restore_pending_or_duplicate(self):
        rid=self.pending(); result=self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.company.decide(FOUNDER,result['payload']['approvalId'],{'contextRevision':1,'decision':'APPROVE','reason':'Unit test scope'})
        after=self.company.mc_generation.recover(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(after['status'],'APPROVED'); self.assertEqual(self.counts(rid),(1,0))
        with self.assertRaises(DomainError): self.company.mc_generation.cancel(FOUNDER,rid,{'contextRevision':1})

    def test_mc_t_06_failed_cancellation_does_not_claim_cancelled(self):
        rid=self.pending()
        with patch.object(Store,'save',side_effect=sqlite3.OperationalError('Outage')):
            with self.assertRaises(DomainError) as caught: self.company.mc_generation.cancel(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(caught.exception.code,'MC_CANCELLATION_NOT_RECORDED')
        self.assertEqual(self.saved(rid)['status'],'RECORDING_FAILED'); self.assertEqual(self.saved(rid)['revision'],1)

    def test_mc_t_06_http_controls_require_session_csrf_owner_revision_and_exact_fields(self):
        rid=self.pending(); router=Router(self.company); base={'Host':'127.0.0.1:5740','Content-Type':'application/json'}
        for op in ('recover','retry','cancel'):
            path=f'/api/campaigns/{rid}/{op}'; body=json.dumps({'contextRevision':1}).encode()
            self.assertEqual(router.handle('POST',path,base,body).status,401)
            token,csrf,_=self.company.login('customer','customer-demo')
            headers={**base,'Cookie':'beauty_session='+token,'X-CSRF-Token':csrf}
            self.assertEqual(router.handle('POST',path,headers,body).status,403)
            token,csrf,_=self.company.login('founder','founder-demo')
            headers={**base,'Cookie':'beauty_session='+token,'X-CSRF-Token':csrf}
            self.assertEqual(router.handle('POST',path,{**headers,'X-CSRF-Token':''},body).status,403)
            for bad in ({},{'contextRevision':True},{'contextRevision':1,'result':{}},{'contextRevision':1,'simulated':True}):
                self.assertEqual(router.handle('POST',path,headers,json.dumps(bad).encode()).status,400)
            with self.assertRaises(DomainError) as caught:
                getattr(self.company.mc_generation,op)(Actor('other','FOUNDER','Other'),rid,{'contextRevision':1})
            self.assertEqual(caught.exception.status,403)
        response=router.handle('POST',f'/api/campaigns/{rid}/recover',headers,json.dumps({'contextRevision':1}).encode())
        self.assertEqual(response.status,200); self.assertEqual(self.counts(rid),(1,0))

    def test_mc_t_06_generation_retry_cannot_replace_a_saved_decision_or_review(self):
        record=self.company.campaign(FOUNDER,self.data); rid=record['id']
        with self.company.store.transaction() as db:
            current=Store.get(db,rid); current['status']='RECORDING_FAILED'
            current['payload']['decisionId']='retained-decision-envelope'
            Store.save(db,current)
        with patch.object(self.company.llm,'generate_script',side_effect=AssertionError('No re-generation')):
            with self.assertRaises(DomainError) as caught:
                self.company.mc_generation.retry(FOUNDER,rid,{'contextRevision':1})
        self.assertEqual(caught.exception.code,'INVALID_STATE')
        self.assertEqual(self.saved(rid)['revision'],1)
        self.assertEqual(self.saved(rid)['payload']['approvalId'],record['payload']['approvalId'])
