"""GR-INT-01: retained CS assessments through authenticated HTTP, no live model."""
import io
import json
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from beauty_company.application import Company
from beauty_company.http import Router
from beauty_company.store import Store


NEEDS = {"orderId": "ORD-1001", "message": "A fragrance-free moisturiser.",
         "concern": "HYDRATION", "budget": 60, "fragranceFree": True}
MISSING = {"id": "POLICY-INCOMPLETE", "missingFields": ["returnWindow"]}
SUFFICIENT = {"id": "POLICY-DEMO-EXCHANGE-v1", "eligible": True, "requiresApproval": True}


class CustomerServiceHttpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "cs-web.sqlite3"
        self.company = Company(self.path)
        self.router = Router(self.company)
        self.base = {"Host": "127.0.0.1:5620", "Content-Type": "application/json"}
        self.customer = self.login("customer", "customer-demo")
        self.other = self.login("customer-2", "customer-demo")
        self.founder = self.login("founder", "founder-demo")

    def login(self, user, password):
        response = self.router.handle("POST", "/api/login", self.base,
                                      json.dumps({"username": user, "password": password}).encode())
        self.assertEqual(response.status, 200)
        return {**self.base, "Cookie": response.headers["Set-Cookie"].split(";")[0],
                "X-CSRF-Token": json.loads(response.body)["csrf"]}

    def post(self, path="/api/after-sales", data=None, headers=None, status=201):
        response = self.router.handle("POST", path, self.customer if headers is None else headers,
                                      json.dumps(NEEDS if data is None else data).encode())
        result = json.loads(response.body)
        self.assertEqual(response.status, status, result)
        return result

    def policy(self, value):
        with self.company.store.transaction() as db:
            db.execute("UPDATE orders SET policy=? WHERE id='ORD-1001'", (json.dumps(value),))

    def snapshot(self, headers=None):
        response = self.router.handle("GET", "/api/snapshot", headers or self.customer)
        self.assertEqual(response.status, 200)
        return json.loads(response.body)

    def assert_no_authority_or_effect(self):
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM effects").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM approvals WHERE decision_id IS NOT NULL").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-101'").fetchone()[0], 12)

    def test_cs_t_02_http_missing_policy_is_retained_and_survives_restart(self):
        self.policy(MISSING)
        result = self.post()
        self.assertEqual(result["status"], "NEEDS_INFORMATION")
        self.assertNotIn("policy", result["payload"])
        self.assertEqual(result["payload"]["evidenceOutcome"]["policyRefs"], ["POLICY-INCOMPLETE"])
        self.company = Company(self.path)
        self.router = Router(self.company)
        saved = next(r for r in self.snapshot()["records"] if r["kind"] == "CS")
        self.assertEqual(saved["payload"], result["payload"])
        self.assertEqual(self.snapshot(self.other)["records"], [])
        self.assertEqual(self.snapshot()["approvals"], [])
        self.assert_no_authority_or_effect()

    def test_cs_t_02_http_conflicting_policy_is_retained_without_eligibility(self):
        self.policy({**SUFFICIENT, "id": "POLICY-A", "conflictingRefs": ["POLICY-B"]})
        result = self.post()
        self.assertEqual(result["status"], "UNRESOLVED")
        self.assertEqual(result["payload"]["evidenceOutcome"]["policyRefs"], ["POLICY-A", "POLICY-B"])
        self.assertNotIn("advice", result["payload"])
        self.assert_no_authority_or_effect()

    def test_cs_t_06_http_policy_read_failure_is_saved_without_private_diagnostic(self):
        with patch.object(self.company.cs.evidence, "policy", side_effect=TimeoutError("PRIVATE_PROVIDER_PATH")):
            result = self.post()
        self.assertEqual(result["status"], "UNRESOLVED")
        self.assertEqual(result["payload"]["evidenceOutcome"]["code"], "POLICY_UNAVAILABLE")
        self.assertNotIn("PRIVATE_PROVIDER_PATH", json.dumps(self.snapshot()))
        self.assert_no_authority_or_effect()

    def test_cs_t_01_http_association_failure_reads_no_policy_and_saves_no_record(self):
        with patch.object(self.company.cs.evidence, "policy") as policy:
            self.post(headers=self.other, status=404)
            policy.assert_not_called()
        self.assertEqual(self.snapshot(self.founder)["records"], [])
        self.assert_no_authority_or_effect()

    def test_cs_t_01_http_initial_verification_unavailable_saves_no_protected_context(self):
        with patch.object(self.company.cs.evidence, "order", side_effect=TimeoutError("PRIVATE_ORDER_PATH")):
            result = self.post(status=409)
        self.assertEqual(result["error"]["code"], "ORDER_READ_UNAVAILABLE")
        self.assertNotIn("PRIVATE_ORDER_PATH", json.dumps(result))
        self.assertEqual(self.snapshot()["records"], [])
        self.assert_no_authority_or_effect()

    def test_cs_t_01_http_assessment_requires_customer_session_and_csrf(self):
        self.post(headers=self.base, status=401)
        self.post(headers=self.founder, status=403)
        self.post(headers={**self.customer, "X-CSRF-Token": "bad"}, status=403)
        self.assertEqual(self.snapshot()["records"], [])

    def test_cs_t_02_http_customer_policy_fields_cannot_supply_eligibility(self):
        self.policy(MISSING)
        result = self.post(data={**NEEDS, "policy": SUFFICIENT, "eligible": True, "role": "FOUNDER"})
        self.assertEqual(result["status"], "NEEDS_INFORMATION")
        self.assertEqual(result["payload"]["evidenceOutcome"]["code"], "POLICY_MISSING")
        self.assert_no_authority_or_effect()

    def test_cs_t_02_http_reassessment_after_authoritative_evidence_refresh_requires_new_handoff(self):
        self.policy(MISSING)
        original = self.post()
        self.policy(SUFFICIENT)
        revised = self.post(f"/api/after-sales/{original['id']}/revise", {**NEEDS, "contextRevision": 1}, status=200)
        self.assertEqual((revised["id"], revised["revision"], revised["status"]), (original["id"], 2, "ASSESSING"))
        self.assertNotIn("evidenceOutcome", revised["payload"])
        self.assertNotIn("approvalId", revised["payload"])
        self.assertNotIn("actionRef", revised["payload"])
        self.assertEqual(revised["payload"]["history"][0]["status"], "NEEDS_INFORMATION")
        self.post(f"/api/after-sales/{original['id']}/confirm", {"contextRevision": 1}, status=409)
        self.assert_no_authority_or_effect()

    def test_cs_t_02_http_still_missing_reassessment_does_not_fabricate_a_new_proposal(self):
        self.policy(MISSING)
        result = self.post()
        repeated = self.post(f"/api/after-sales/{result['id']}/revise", {**NEEDS, "contextRevision": 1}, status=200)
        self.assertEqual((repeated["id"], repeated["revision"], repeated["status"]),
                         (result["id"], 1, "NEEDS_INFORMATION"))
        self.assertEqual(len([r for r in self.snapshot()["records"] if r["kind"] == "CS"]), 1)
        self.assert_no_authority_or_effect()

    def test_cs_t_06_http_confirm_error_keeps_saved_blocked_status_for_refresh(self):
        result = self.post()
        self.post(f"/api/after-sales/{result['id']}/coordinate", {}, self.founder, 200)
        self.policy(MISSING)
        error = self.post(f"/api/after-sales/{result['id']}/confirm", {"contextRevision": 1}, status=409)
        self.assertEqual(error["error"]["code"], "POLICY_MISSING")
        saved = next(r for r in self.snapshot()["records"] if r["kind"] == "CS")
        self.assertEqual(saved["status"], "NEEDS_INFORMATION")
        self.assertNotIn("approvalId", saved["payload"])
        self.assert_no_authority_or_effect()

    def test_cs_t_06_http_storage_failure_cannot_claim_the_assessment_was_retained(self):
        self.policy(MISSING)
        with patch.object(Store, "save", side_effect=sqlite3.OperationalError("PRIVATE_DATABASE_PATH")), redirect_stderr(io.StringIO()):
            error = self.post(status=500)
        self.assertEqual(error["error"]["code"], "INTERNAL_ERROR")
        self.assertNotIn("PRIVATE_DATABASE_PATH", json.dumps(error))
        self.assertEqual(self.snapshot()["records"], [])
        self.assert_no_authority_or_effect()
