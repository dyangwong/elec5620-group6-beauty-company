
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
        with patch.object(Store,'save',side_effect=fail), self.assertRaises(sqlite3.OperationalError):
            self.company.campaign(FOUNDER,self.data)
        with self.company.store.read() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0],0)
            saved=Store.get(db,db.execute("SELECT id FROM records WHERE kind='MC'").fetchone()[0])
        self.assertEqual(saved['status'],'DRAFTING'); self.assertNotIn('script',saved['payload'])

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
