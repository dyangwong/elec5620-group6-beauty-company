"""Executable slices of Stage 1 cases; see docs/traceability.csv for limits."""
import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from beauty_company.application import Company
from beauty_company.contracts import Actor, DomainError
from beauty_company.http import Router
from beauty_company.store import Store, encode


CUSTOMER = Actor("customer", "CUSTOMER", "Alex")
OTHER = Actor("customer-2", "CUSTOMER", "Sam")
FOUNDER = Actor("founder", "FOUNDER", "Founder")
NEEDS = {"message": "I need a fragrance-free moisturiser.", "concern": "HYDRATION", "budget": 60, "fragranceFree": True}


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.company = Company(Path(self.temp.name) / "test.sqlite3")

    def request(self):
        with self.company.store.transaction() as db:
            return self.company.cs.submit(db, CUSTOMER, {**NEEDS, "orderId": "ORD-1001"})

    def proposed(self):
        request = self.request()
        with self.company.store.transaction() as db:
            return self.company.cs.coordinate(db, FOUNDER, request["id"])

    def pending(self):
        request = self.proposed()
        return self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})

    def approved(self):
        request = self.pending()
        self.decision(request["payload"]["approvalId"])
        return request

    def decision(self, rid, kind="APPROVE", revision=1, reason="Checked this exact simulated action."):
        return self.company.decide(FOUNDER, rid, {"decision": kind, "contextRevision": revision, "reason": reason})

    def record(self, rid):
        with self.company.store.read() as db:
            return Store.get(db, rid)

    def effects(self):
        with self.company.store.read() as db:
            return db.execute("SELECT COUNT(*) FROM effects").fetchone()[0]

    def test_ba_t_01_missing_constraint_requests_clarification(self):
        with self.company.store.transaction() as db:
            result = self.company.ba.submit(db, CUSTOMER, {"message": "Something for my skin"})
        self.assertEqual(result["status"], "CLARIFYING")
        self.assertEqual(self.effects(), 0)

    def test_ba_t_02_grounded_advice_has_no_commerce_effect(self):
        with self.company.store.transaction() as db:
            result = self.company.ba.submit(db, CUSTOMER, NEEDS)
        advice = result["payload"]["result"]
        self.assertEqual(advice["product"]["id"], "P-101")
        self.assertEqual(advice["evidence"]["availability"], "AVAILABLE")
        self.assertTrue(set(advice["reasons"]).issubset(advice["product"]["facts"]))
        self.assertEqual(self.effects(), 0)

    def test_ba_t_03_unknown_stock_never_becomes_available(self):
        with self.company.store.transaction() as db:
            db.execute("UPDATE products SET stock=NULL WHERE id='P-101'")
            result = self.company.ba.submit(db, CUSTOMER, NEEDS)
        self.assertEqual(result["status"], "INCOMPLETE")

    def test_ba_t_04_unsupported_mock_claim_is_withheld(self):
        for output in [{"productId": "P-101", "factRefs": ["Cures eczema"]}, None,
                       {"productId": "INVENTED-PRODUCT", "factRefs": ["Fragrance-free"]}]:
            with patch.object(self.company.llm, "propose", return_value=output):
                with self.company.store.transaction() as db:
                    result = self.company.ba.submit(db, CUSTOMER, NEEDS)
            self.assertEqual(result["status"], "INCOMPLETE")

    def test_ba_t_05_diagnosis_request_stops(self):
        with self.company.store.transaction() as db:
            result = self.company.ba.submit(db, CUSTOMER, {**NEEDS, "message": "Please diagnose my skin."})
        self.assertEqual(result["status"], "INCOMPLETE")

    def test_cs_t_01_identity_mismatch_discloses_no_order(self):
        with self.assertRaises(DomainError) as caught:
            with self.company.store.transaction() as db:
                self.company.cs.submit(db, OTHER, {**NEEDS, "orderId": "ORD-1001"})
        self.assertEqual(caught.exception.status, 404)
        self.assertEqual(self.company.snapshot(OTHER)["records"], [])

    def test_cs_t_02_unknown_policy_blocks_intake(self):
        with self.company.store.transaction() as db:
            db.execute("UPDATE orders SET policy=? WHERE id='ORD-1001'", (encode({"eligible": None}),))
        with self.assertRaises(DomainError):
            self.request()

    def test_duplicate_intake_cannot_create_two_active_exchanges(self):
        self.request()
        with self.assertRaises(DomainError) as caught:
            self.request()
        self.assertEqual(caught.exception.code, "DUPLICATE_REQUEST")

    def test_changed_policy_requires_revised_scope_and_fresh_review(self):
        request = self.approved()
        with self.company.store.transaction() as db:
            row = db.execute("SELECT policy FROM orders WHERE id='ORD-1001'").fetchone()
            policy = json.loads(row["policy"])
            policy["id"] = "POLICY-DEMO-EXCHANGE-v2"
            db.execute("UPDATE orders SET policy=? WHERE id='ORD-1001'", (encode(policy),))
        with self.assertRaises(DomainError) as caught:
            self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})
        self.assertEqual(caught.exception.code, "STALE_POLICY")
        with self.company.store.transaction() as db:
            revised = self.company.cs.revise(db, CUSTOMER, request["id"], {**NEEDS, "contextRevision": 1})
        self.assertEqual(revised["payload"]["policy"]["id"], policy["id"])
        self.assertNotIn("approvalId", revised["payload"])
        self.assertEqual(self.effects(), 0)

    def test_co_t_01_founder_initiates_minimal_handoff(self):
        request = self.request()
        with self.assertRaises(DomainError):
            with self.company.store.transaction() as db:
                self.company.cs.coordinate(db, CUSTOMER, request["id"])
        with self.company.store.transaction() as db:
            request = self.company.cs.coordinate(db, FOUNDER, request["id"])
        coordination = self.record(request["payload"]["coordinationId"])
        context = coordination["payload"]["handoffs"][0]["authorisedContext"]
        self.assertEqual(set(context), {"message", "concern", "budget", "fragranceFree"})
        self.assertNotEqual(coordination["status"], "COMPLETED")

    def test_ap_t_02_pending_approval_grants_no_execution(self):
        request = self.pending()
        self.assertEqual(request["status"], "REVIEW_PENDING")
        self.assertEqual(self.effects(), 0)
        with self.assertRaises(DomainError):
            self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})

    def test_ap_t_02_customer_cannot_decide(self):
        request = self.pending()
        with self.assertRaises(DomainError) as caught:
            self.company.decide(CUSTOMER, request["payload"]["approvalId"], {"decision": "APPROVE", "reason": "Self approval", "contextRevision": 1})
        self.assertEqual(caught.exception.status, 403)

    def test_gr_t_02_approval_and_execution_remain_distinct(self):
        request = self.approved()
        self.assertEqual(self.effects(), 0)
        self.assertEqual(self.record(request["id"])["status"], "AWAITING_CONFIRMATION")
        result = self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})
        self.assertEqual(result["status"], "RESOLVED")
        self.assertTrue(result["payload"]["result"]["simulated"])
        self.assertEqual(self.effects(), 1)
        self.assertEqual(self.record(request["payload"]["coordinationId"])["status"], "COMPLETED")

    def test_gr_t_03_repeated_confirmation_never_duplicates_effect(self):
        request = self.approved()
        for _ in range(3):
            self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})
        self.assertEqual(self.effects(), 1)
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-101'").fetchone()[0], 11)

    def test_concurrent_confirmations_never_duplicate_stock_effect(self):
        request = self.approved()

        def confirm():
            try:
                return self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})["status"]
            except DomainError as error:
                return error.code

        with ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(lambda _: confirm(), range(3)))
        self.assertIn("RESOLVED", results)
        self.assertTrue(set(results).issubset({"RESOLVED", "RECONCILIATION_REQUIRED"}))
        self.assertEqual(self.effects(), 1)
        self.assertEqual(self.record(request["id"])["status"], "RESOLVED")

    def test_cs_t_06_post_write_timeout_requires_read_only_reconciliation(self):
        request = self.approved()
        self.company.set_fault(FOUNDER, "after_sales_timeout")
        result = self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})
        self.assertEqual(result["status"], "RECONCILING")
        self.assertEqual(self.effects(), 1)
        with self.assertRaises(DomainError):
            self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})
        result = self.company.cs.reconcile(CUSTOMER, request["id"])
        self.assertEqual(result["status"], "RESOLVED")
        self.assertEqual(self.effects(), 1)

    def test_co_t_08_failed_outcome_recording_recovers_without_execution(self):
        request = self.approved()
        self.company.set_fault(FOUNDER, "outcome_recording")
        result = self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})
        self.assertEqual(result["status"], "RECORDING_FAILED")
        self.company.cs.reconcile(CUSTOMER, request["id"])
        self.assertEqual(self.effects(), 1)

    def test_ap_t_06_failed_delivery_preserves_same_committed_decision(self):
        request = self.pending()
        self.company.set_fault(FOUNDER, "approval_delivery")
        review = self.decision(request["payload"]["approvalId"])
        self.assertEqual(review["status"], "APPROVED")
        self.assertEqual(review["delivery"], "FAILED")
        self.assertEqual(self.record(request["id"])["status"], "REVIEW_PENDING")
        recovered = self.company.redeliver(FOUNDER, review["id"])
        duplicate = self.company.redeliver(FOUNDER, review["id"])
        self.assertEqual(recovered["decision_id"], review["decision_id"])
        self.assertEqual(duplicate["decision_id"], review["decision_id"])
        self.assertEqual(self.effects(), 0)

    def test_ap_t_03_decision_and_audit_roll_back_together(self):
        request = self.pending()
        rid = request["payload"]["approvalId"]
        real_event = Store.event

        def fail_commit_audit(db, entity_id, role, event, detail):
            # Only the authoritative decision audit fails; the intent is recorded first.
            if event == "DECISION_COMMITTED":
                raise RuntimeError("injected audit write failure")
            return real_event(db, entity_id, role, event, detail)

        with patch.object(Store, "event", side_effect=fail_commit_audit):
            with self.assertRaises(DomainError) as caught:
                self.decision(rid)
        # The commit rolled back, so no committed decision and no authority exist.
        self.assertEqual(caught.exception.code, "RECORDING_FAILED")
        self.assertIsInstance(caught.exception.__cause__, RuntimeError)
        with self.company.store.read() as db:
            review = self.company.ap.get(db, rid)
            intent = self.company.ap.intent(db, rid)
            events = [row["event"] for row in db.execute("SELECT event FROM events WHERE entity_id=?", (rid,))]
        self.assertEqual(review["status"], "RECORDING_FAILED")
        self.assertIsNone(review["decision_id"])
        self.assertNotIn("DECISION_COMMITTED", events)
        self.assertEqual(self.effects(), 0)
        # The intended decision identity stays recoverable from storage.
        self.assertIsNotNone(intent)
        self.assertEqual(intent["kind"], "APPROVE")
        self.assertEqual(intent["status"], "RECORDING_FAILED")

    def test_ap_t_07_approval_cannot_create_stock(self):
        request = self.approved()
        with self.company.store.transaction() as db:
            db.execute("UPDATE products SET stock=0 WHERE id='P-101'")
        with self.assertRaises(DomainError):
            self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})
        self.assertEqual(self.effects(), 0)

    def test_ap_t_04_revised_action_never_inherits_approval(self):
        request = self.approved()
        old_approval = request["payload"]["approvalId"]
        with self.company.store.transaction() as db:
            revised = self.company.cs.revise(db, CUSTOMER, request["id"], {**NEEDS, "contextRevision": 1})
        self.assertEqual(revised["revision"], 2)
        self.assertNotIn("decisionId", revised["payload"])
        self.company.redeliver(FOUNDER, old_approval)
        self.assertEqual(self.record(request["id"])["status"], "ASSESSING")
        with self.assertRaises(DomainError):
            self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})

    def test_ap_rejection_and_revision_do_not_execute(self):
        for kind, expected in [("REJECT", "REJECTED"), ("REQUEST_REVISION", "NEEDS_INFORMATION")]:
            request = self.pending()
            self.decision(request["payload"]["approvalId"], kind)
            self.assertEqual(self.record(request["id"])["status"], expected)
        self.assertEqual(self.effects(), 0)

    def test_mc_t_01_and_06_mock_draft_needs_own_review(self):
        with self.company.store.transaction() as db:
            campaign = self.company.mc.submit(db, FOUNDER, {"brief": "A calm introduction to daily hydration.", "productId": "P-101"})
        self.assertEqual(campaign["status"], "REVIEW_PENDING")
        self.assertEqual(campaign["payload"]["media"]["kind"], "MOCK_STORYBOARD")
        self.decision(campaign["payload"]["approvalId"])
        self.assertEqual(self.record(campaign["id"])["status"], "APPROVED")
        with self.company.store.transaction() as db:
            revised = self.company.mc.revise(db, FOUNDER, campaign["id"], {"brief": "A revised campaign brief.", "productId": "P-101", "contextRevision": 1})
        self.assertEqual(revised["status"], "REVIEW_PENDING")
        self.assertNotEqual(revised["payload"]["approvalId"], campaign["payload"]["approvalId"])
        self.assertNotIn("decisionId", revised["payload"])

    def test_mc_t_03_unsupported_claim_blocks_review(self):
        with patch.object(self.company.llm, "generate_script", return_value={"claims": ["Guaranteed cure"]}):
            with self.assertRaises(DomainError):
                with self.company.store.transaction() as db:
                    self.company.mc.submit(db, FOUNDER, {"brief": "A brief", "productId": "P-101"})
        self.assertEqual(self.company.snapshot(FOUNDER)["approvals"], [])

    def test_customer_snapshot_never_exposes_other_customer_records(self):
        self.request()
        snapshot = self.company.snapshot(OTHER)
        self.assertEqual(snapshot["records"], [])
        self.assertEqual(snapshot["approvals"], [])
        self.assertEqual([o["id"] for o in snapshot["orders"]], ["ORD-2001"])


class HttpBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.company = Company(Path(self.temp.name) / "http.sqlite3")
        self.router = Router(self.company)
        self.headers = {"Host": "127.0.0.1:5620", "Content-Type": "application/json"}

    def post(self, path, data, headers=None):
        return self.router.handle("POST", path, headers or self.headers, json.dumps(data).encode())

    def test_user_id_header_does_not_authenticate(self):
        response = self.router.handle("GET", "/api/snapshot", {**self.headers, "Authorization": "founder"})
        self.assertEqual(response.status, 401)

    def test_csrf_and_role_are_enforced(self):
        login = self.post("/api/login", {"username": "customer", "password": "customer-demo", "role": "FOUNDER"})
        data = json.loads(login.body)
        self.assertEqual(data["actor"]["role"], "CUSTOMER")
        headers = {**self.headers, "Cookie": login.headers["Set-Cookie"].split(";")[0]}
        self.assertEqual(self.post("/api/demo/fault", {"fault": "after_sales_timeout"}, headers).status, 403)
        headers["X-CSRF-Token"] = data["csrf"]
        self.assertEqual(self.post("/api/demo/fault", {"fault": "after_sales_timeout"}, headers).status, 403)

    def test_cross_origin_and_dns_rebinding_hosts_are_rejected(self):
        self.assertEqual(self.post("/api/login", {}, {**self.headers, "Origin": "https://example.com"}).status, 403)
        self.assertEqual(self.router.handle("GET", "/", {"Host": "example.com"}).status, 403)

    def test_invalid_json_does_not_mutate_state(self):
        response = self.router.handle("POST", "/api/login", self.headers, b"{")
        self.assertEqual(response.status, 400)


if __name__ == "__main__":
    unittest.main()
