"""GR-INT-01: authenticated AP recording recovery through the HTTP boundary.

Use real sessions, SQLite and the existing mock CS/AP flow. No model or external
commerce service is required. Browser acceptance is recorded separately.
"""
import json
import tempfile
import unittest
from pathlib import Path

from beauty_company.application import Company
from beauty_company.http import Router


NEEDS = {"message": "I need a fragrance-free moisturiser.", "concern": "HYDRATION",
         "budget": 60, "fragranceFree": True}
REASON = "Checked the current exchange and catalogue evidence."


class ApprovalRecoveryHttpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "http.sqlite3"
        self.company = Company(self.path)
        self.router = Router(self.company)
        self.base = {"Host": "127.0.0.1:5620", "Content-Type": "application/json"}
        self.founder = self.login("founder", "founder-demo")
        self.customer = self.login("customer", "customer-demo")

    def post(self, path, data, headers=None, status=200):
        response = self.router.handle("POST", path, headers or self.base, json.dumps(data).encode())
        body = json.loads(response.body)
        self.assertEqual(response.status, status, body)
        return body

    def login(self, username, password):
        response = self.router.handle("POST", "/api/login", self.base,
                                      json.dumps({"username": username, "password": password}).encode())
        self.assertEqual(response.status, 200)
        return {**self.base, "Cookie": response.headers["Set-Cookie"].split(";")[0],
                "X-CSRF-Token": json.loads(response.body)["csrf"]}

    def pending(self):
        request = self.post("/api/after-sales", {**NEEDS, "orderId": "ORD-1001"}, self.customer, 201)
        self.post(f"/api/after-sales/{request['id']}/coordinate", {}, self.founder)
        request = self.post(f"/api/after-sales/{request['id']}/confirm", {"contextRevision": 1}, self.customer)
        return request["id"], request["payload"]["approvalId"]

    def failed(self, kind="APPROVE"):
        request_id, approval_id = self.pending()
        self.post("/api/demo/fault", {"fault": "approval_recording"}, self.founder)
        failure = self.post(f"/api/approvals/{approval_id}/decide",
                            {"contextRevision": 1, "decision": kind, "reason": REASON}, self.founder, 409)
        self.assertEqual(failure["error"]["code"], "RECORDING_FAILED")
        return request_id, approval_id

    def recover(self, approval_id, status=200, headers=None, data=None):
        return self.post(f"/api/approvals/{approval_id}/recover",
                         {"contextRevision": 1} if data is None else data,
                         self.founder if headers is None else headers, status)

    def counts(self):
        with self.company.store.read() as db:
            return (db.execute("SELECT COUNT(*) FROM events WHERE event='DECISION_COMMITTED'").fetchone()[0],
                    db.execute("SELECT COUNT(*) FROM effects").fetchone()[0],
                    db.execute("SELECT stock FROM products WHERE id='P-101'").fetchone()[0])

    def test_ap_t_05_http_recovery_after_restart_is_once_only_and_does_not_execute(self):
        request_id, approval_id = self.failed()
        self.assertEqual(self.counts(), (0, 0, 12))
        self.company = Company(self.path)
        self.router = Router(self.company)
        recovered = self.recover(approval_id)
        self.assertEqual((recovered["status"], recovered["delivery"], recovered["decision"], recovered["reason"]),
                         ("APPROVED", "DELIVERED", "APPROVE", REASON))
        for _ in range(3):
            self.assertEqual(self.recover(approval_id)["decision_id"], recovered["decision_id"])
        self.assertEqual(self.counts(), (1, 0, 12))
        # Only a later current Customer confirmation can cause the mock effect.
        for _ in range(3):
            self.post(f"/api/after-sales/{request_id}/confirm", {"contextRevision": 1}, self.customer)
        self.assertEqual(self.counts(), (1, 1, 11))
        self.recover(approval_id)
        self.assertEqual(self.counts(), (1, 1, 11))

    def test_ap_t_05_http_recovery_preserves_saved_rejection(self):
        _, approval_id = self.failed("REJECT")
        self.assertEqual(self.recover(approval_id)["status"], "REJECTED")
        self.assertEqual(self.counts(), (1, 0, 12))

    def test_ap_t_05_http_recovery_preserves_saved_revision_request(self):
        _, approval_id = self.failed("REQUEST_REVISION")
        self.assertEqual(self.recover(approval_id)["status"], "REVISION_REQUESTED")
        self.assertEqual(self.counts(), (1, 0, 12))

    def test_ap_t_05_http_recovery_requires_session_csrf_and_founder(self):
        _, approval_id = self.failed()
        self.assertEqual(self.recover(approval_id, 401, self.base)["error"]["code"], "UNAUTHENTICATED")
        bad_csrf = {**self.founder, "X-CSRF-Token": "invalid"}
        self.assertEqual(self.recover(approval_id, 403, bad_csrf)["error"]["code"], "INVALID_CSRF")
        self.assertEqual(self.recover(approval_id, 403, self.customer)["error"]["code"], "FORBIDDEN")
        self.assertEqual(self.counts(), (0, 0, 12))

    def test_ap_t_05_http_recovery_refuses_a_different_founder(self):
        _, approval_id = self.failed()
        with self.company.store.transaction() as db:
            db.execute("INSERT INTO users SELECT 'other-founder',role,'Other Founder',salt,password_hash "
                       "FROM users WHERE id='founder'")
        other = self.login("other-founder", "founder-demo")
        self.assertEqual(self.recover(approval_id, 403, other)["error"]["code"], "FORBIDDEN")
        self.assertEqual(self.counts(), (0, 0, 12))

    def test_ap_t_05_http_recovery_accepts_only_a_positive_integer_displayed_revision(self):
        _, approval_id = self.failed()
        for data in ({}, {"contextRevision": True}, {"contextRevision": "1"}, {"contextRevision": 0},
                     {"contextRevision": 1, "decision": "REJECT"},
                     {"contextRevision": 1, "reason": "A replacement reason"},
                     {"contextRevision": 1, "action": {"productId": "P-102"}},
                     {"contextRevision": 1, "founder_id": "founder"}):
            with self.subTest(data=data):
                self.recover(approval_id, 400, data=data)
        self.assertEqual(self.recover(approval_id, 409, data={"contextRevision": 2})["error"]["code"], "STALE_SCOPE")
        self.assertEqual(self.counts(), (0, 0, 12))
        self.assertEqual(self.recover(approval_id)["reason"], REASON)

    def test_ap_t_05_http_recovery_refuses_superseded_scope(self):
        request_id, approval_id = self.failed()
        self.post(f"/api/after-sales/{request_id}/revise", {**NEEDS, "contextRevision": 1}, self.customer)
        self.assertEqual(self.recover(approval_id, 409)["error"]["code"], "STALE_SCOPE")
        self.assertEqual(self.counts(), (0, 0, 12))

    def test_ap_t_05_http_repeated_recovery_checks_scope_even_after_commit(self):
        request_id, approval_id = self.failed()
        self.recover(approval_id)
        self.post(f"/api/after-sales/{request_id}/revise", {**NEEDS, "contextRevision": 1}, self.customer)
        self.assertEqual(self.recover(approval_id, 409)["error"]["code"], "STALE_SCOPE")
        self.assertEqual(self.counts(), (1, 0, 12))

    def test_ap_t_05_http_recovery_refuses_changed_action_scope(self):
        _, approval_id = self.failed()
        with self.company.store.transaction() as db:
            db.execute("UPDATE approvals SET action_ref='changed-scope' WHERE id=?", (approval_id,))
        self.assertEqual(self.recover(approval_id, 409)["error"]["code"], "STALE_SCOPE")
        self.assertEqual(self.counts(), (0, 0, 12))

    def test_ap_t_05_http_recovery_requires_an_existing_saved_intent(self):
        _, approval_id = self.pending()
        self.assertEqual(self.recover(approval_id, 409)["error"]["code"], "NO_INTENT")
        self.assertEqual(self.recover("missing-review", 404)["error"]["code"], "NOT_FOUND")
        self.assertEqual(self.counts(), (0, 0, 12))

    def test_ap_t_05_http_recovery_failure_remains_failed_and_can_be_retried(self):
        _, approval_id = self.failed()
        self.post("/api/demo/fault", {"fault": "approval_recording"}, self.founder)
        self.assertEqual(self.recover(approval_id, 409)["error"]["code"], "RECORDING_FAILED")
        self.assertEqual(self.counts(), (0, 0, 12))
        self.assertEqual(self.recover(approval_id)["delivery"], "DELIVERED")
        self.assertEqual(self.counts(), (1, 0, 12))

    def test_ap_t_05_http_failed_delivery_preserves_decision_for_explicit_redelivery(self):
        _, approval_id = self.failed()
        self.post("/api/demo/fault", {"fault": "approval_delivery"}, self.founder)
        recovered = self.recover(approval_id)
        self.assertEqual(recovered["delivery"], "FAILED")
        repeated = self.recover(approval_id)
        self.assertEqual((repeated["decision_id"], repeated["delivery"]), (recovered["decision_id"], "FAILED"))
        delivered = self.post(f"/api/approvals/{approval_id}/deliver", {}, self.founder)
        self.assertEqual((delivered["decision_id"], delivered["delivery"]), (recovered["decision_id"], "DELIVERED"))
        self.assertEqual(self.counts(), (1, 0, 12))
