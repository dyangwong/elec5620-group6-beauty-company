
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from beauty_company.application import Company
from beauty_company.contracts import Actor, DomainError
from beauty_company.http import Router
from beauty_company.store import Store

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
