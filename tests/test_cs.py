"""KAN-11 / CS-START-01: bounded offline evidence/failure acceptance subsets."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from beauty_company.application import Company
from beauty_company.contracts import Actor, DomainError
from beauty_company.store import Store, encode


CUSTOMER = Actor("customer", "CUSTOMER", "Alex")
OTHER = Actor("customer-2", "CUSTOMER", "Sam")
FOUNDER = Actor("founder", "FOUNDER", "Founder")
NEEDS = {"orderId": "ORD-1001", "message": "A fragrance-free moisturiser.",
         "concern": "HYDRATION", "budget": 60, "fragranceFree": True}


class CustomerServiceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.company = Company(Path(self.temp.name) / "cs.sqlite3")
        self.cs = self.company.cs

    def intake(self, actor=CUSTOMER, data=None):
        with self.company.store.transaction() as db:
            return self.cs.assess(db, actor, data or NEEDS)

    def record(self, rid):
        with self.company.store.read() as db:
            return Store.get(db, rid)

    def policy(self, value):
        with self.company.store.transaction() as db:
            db.execute("UPDATE orders SET policy=? WHERE id='ORD-1001'", (encode(value),))

    def no_effects(self):
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM effects").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-101'").fetchone()[0], 12)

    def approved(self):
        request = self.intake()
        with self.company.store.transaction() as db:
            self.cs.coordinate(db, FOUNDER, request["id"])
        pending = self.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})
        self.company.decide(FOUNDER, pending["payload"]["approvalId"], {
            "decision": "APPROVE", "contextRevision": 1, "reason": "Checked fixture scope."})
        return self.record(request["id"])

    def test_cs_t_01_association_precedes_policy_and_model_reads(self):
        for actor, data in [(OTHER, NEEDS), (CUSTOMER, {**NEEDS, "orderId": "ABSENT"})]:
            with patch.object(self.cs.evidence, "policy") as policy, patch.object(self.company.llm, "propose") as model:
                with self.assertRaises(DomainError) as caught:
                    self.intake(actor, data)
                self.assertEqual(caught.exception.code, "ORDER_NOT_FOUND")
                self.assertEqual(str(caught.exception), "No accessible order matches that reference.")
                policy.assert_not_called()
                model.assert_not_called()
        self.assertEqual(self.company.snapshot(OTHER)["records"], [])
        self.no_effects()

    def test_cs_t_01_initial_verification_unavailable_discloses_no_context(self):
        with patch.object(self.cs.evidence, "order", side_effect=TimeoutError("private diagnostic")):
            with self.assertRaises(DomainError) as caught:
                self.intake()
        self.assertEqual(caught.exception.code, "ORDER_READ_UNAVAILABLE")
        self.assertNotIn("private diagnostic", str(caught.exception))
        self.assertEqual(self.company.snapshot(CUSTOMER)["records"], [])
        self.no_effects()

    def test_cs_t_02_sufficient_policy_retains_reference(self):
        record = self.intake()
        self.assertEqual(record["status"], "ASSESSING")
        self.assertEqual(record["payload"]["policy"]["id"], "POLICY-DEMO-EXCHANGE-v1")
        self.assertEqual(self.record(record["id"])["payload"], record["payload"])
        self.no_effects()

    def test_cs_t_02_missing_evidence_retains_clarification_without_rule(self):
        self.policy({"id": "POLICY-INCOMPLETE", "eligible": None, "missingFields": ["returnWindow"]})
        record = self.intake()
        self.assertEqual(record["status"], "NEEDS_INFORMATION")
        self.assertNotIn("policy", record["payload"])
        self.assertEqual(record["payload"]["evidenceOutcome"]["policyRefs"], ["POLICY-INCOMPLETE"])
        self.assertEqual(self.record(record["id"])["status"], "NEEDS_INFORMATION")
        self.assertEqual(self.record(record["payload"]["coordinationId"])["status"], "CLARIFICATION_REQUIRED")
        self.assertEqual(self.company.snapshot(CUSTOMER)["approvals"], [])
        self.no_effects()

    def test_cs_t_02_conflicting_policy_retains_refs_without_eligibility(self):
        self.policy({"id": "POLICY-A", "eligible": True, "requiresApproval": True,
                     "conflictingRefs": ["POLICY-B"]})
        record = self.intake()
        self.assertEqual(record["status"], "UNRESOLVED")
        self.assertEqual(record["payload"]["evidenceOutcome"]["policyRefs"], ["POLICY-A", "POLICY-B"])
        self.assertNotIn("policy", record["payload"])
        self.assertEqual(self.company.snapshot(CUSTOMER)["approvals"], [])
        self.no_effects()

    def test_cs_t_02_malformed_policy_cannot_become_eligibility(self):
        with self.company.store.transaction() as db:
            db.execute("UPDATE orders SET policy='invalid json' WHERE id='ORD-1001'")
        record = self.intake()
        self.assertEqual(record["status"], "UNRESOLVED")
        self.assertEqual(record["payload"]["evidenceOutcome"]["code"], "POLICY_CONFLICTING")
        self.no_effects()

    def test_cs_t_02_ineligible_policy_has_safe_outcome(self):
        self.policy({"id": "POLICY-INELIGIBLE", "eligible": False, "requiresApproval": True})
        record = self.intake()
        self.assertEqual(record["payload"]["evidenceOutcome"]["code"], "POLICY_UNSUPPORTED")
        self.assertEqual(record["status"], "UNRESOLVED")
        self.no_effects()

    def test_cs_t_06_policy_read_failure_is_retained_without_raw_diagnostic(self):
        with patch.object(self.cs.evidence, "policy", side_effect=sqlite3.OperationalError("private diagnostic")):
            record = self.intake()
        self.assertEqual(record["status"], "UNRESOLVED")
        self.assertEqual(record["payload"]["evidenceOutcome"]["code"], "POLICY_UNAVAILABLE")
        self.assertNotIn("private diagnostic", encode(self.record(record["id"])))
        self.assertEqual(self.record(record["payload"]["coordinationId"])["status"], "ESCALATED")
        self.no_effects()

    def test_cs_t_06_changed_policy_before_handoff_blocks_model(self):
        record = self.intake()
        self.policy({"id": "POLICY-MISSING", "eligible": None})
        with patch.object(self.company.llm, "propose") as model:
            with self.company.store.transaction() as db:
                result = self.cs.coordinate(db, FOUNDER, record["id"])
            model.assert_not_called()
        self.assertEqual(result["status"], "NEEDS_INFORMATION")
        self.assertEqual(result["payload"]["evidenceOutcome"]["policyRefs"], ["POLICY-MISSING"])
        self.no_effects()

    def test_cs_t_02_corrected_evidence_requires_new_revision_confirmation_review(self):
        self.policy({"eligible": None})
        record = self.intake()
        self.policy({"id": "POLICY-CORRECTED", "eligible": True, "requiresApproval": True})
        with self.company.store.transaction() as db:
            revised = self.cs.revise(db, CUSTOMER, record["id"], {**NEEDS, "contextRevision": 1})
            proposed = self.cs.coordinate(db, FOUNDER, record["id"])
        self.assertEqual(revised["revision"], 2)
        self.assertNotIn("approvalId", revised["payload"])
        self.assertNotIn("confirmation", revised["payload"])
        with self.assertRaises(DomainError):
            self.cs.confirm(CUSTOMER, record["id"], {"contextRevision": 1})
        pending = self.cs.confirm(CUSTOMER, proposed["id"], {"contextRevision": 2})
        self.assertEqual(pending["status"], "REVIEW_PENDING")
        self.no_effects()

    def test_cs_t_04_available_exchange_executes_only_selected_product(self):
        record = self.approved()
        result = self.cs.confirm(CUSTOMER, record["id"], {"contextRevision": 1})
        self.assertEqual(result["status"], "RESOLVED")
        self.assertEqual(result["payload"]["stockObservation"]["availability"], "AVAILABLE")
        self.assertEqual(result["payload"]["result"]["productId"], "P-101")
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM effects").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-102'").fetchone()[0], 8)

    def test_cs_t_04_unknown_and_unavailable_never_substitute(self):
        record = self.approved()
        for stock, expected in [(None, "UNKNOWN"), (0, "UNAVAILABLE")]:
            with self.subTest(availability=expected):
                with self.company.store.transaction() as db:
                    db.execute("UPDATE products SET stock=? WHERE id='P-101'", (stock,))
                    # A deliberate new revision is required after each blocked attempt.
                    current = Store.get(db, record["id"])
                    if current["status"] == "UNRESOLVED":
                        db.execute("UPDATE products SET stock=12 WHERE id='P-101'")
                        self.cs.revise(db, CUSTOMER, record["id"], {**NEEDS, "contextRevision": 1})
                        self.cs.coordinate(db, FOUNDER, record["id"])
                        db.execute("UPDATE products SET stock=? WHERE id='P-101'", (stock,))
                revision = self.record(record["id"])["revision"]
                with self.assertRaises(DomainError) as caught:
                    self.cs.confirm(CUSTOMER, record["id"], {"contextRevision": revision})
                self.assertEqual(caught.exception.code, "STOCK_" + expected)
                saved = self.record(record["id"])
                self.assertEqual(saved["status"], "UNRESOLVED")
                self.assertEqual(saved["payload"]["stockObservation"]["availability"], expected)
                self.assertNotIn("confirmation", saved["payload"])
                with self.company.store.read() as db:
                    self.assertEqual(db.execute("SELECT COUNT(*) FROM effects").fetchone()[0], 0)
                    self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-102'").fetchone()[0], 8)

    def test_cs_t_06_confirm_read_failure_commits_before_error_and_invalidates_review(self):
        record = self.approved()
        old_approval = record["payload"]["approvalId"]
        with patch.object(self.cs.evidence, "stock", side_effect=TimeoutError("private diagnostic")):
            with self.assertRaises(DomainError) as caught:
                self.cs.confirm(CUSTOMER, record["id"], {"contextRevision": 1})
        self.assertEqual(caught.exception.code, "STOCK_READ_UNAVAILABLE")
        saved = self.record(record["id"])
        self.assertEqual(saved["status"], "UNRESOLVED")
        self.assertNotIn("approvalId", saved["payload"])
        self.assertNotIn("private diagnostic", encode(saved))
        self.company.redeliver(FOUNDER, old_approval)
        self.assertEqual(self.record(record["id"])["status"], "UNRESOLVED")
        self.no_effects()

    def test_cs_t_02_post_approval_policy_change_retained_and_old_delivery_stale(self):
        record = self.approved()
        approval_id = record["payload"]["approvalId"]
        self.policy({"id": "POLICY-NEW", "eligible": True, "requiresApproval": True})
        with self.assertRaises(DomainError) as caught:
            self.cs.confirm(CUSTOMER, record["id"], {"contextRevision": 1})
        self.assertEqual(caught.exception.code, "STALE_POLICY")
        self.assertEqual(self.record(record["id"])["status"], "UNRESOLVED")
        self.company.redeliver(FOUNDER, approval_id)
        self.assertEqual(self.record(record["id"])["status"], "UNRESOLVED")
        self.no_effects()

    def test_cs_t_01_reassigned_order_never_enters_policy_or_review_context(self):
        record = self.approved()
        with self.company.store.transaction() as db:
            db.execute("UPDATE orders SET customer_id='customer-2',policy=? WHERE id='ORD-1001'",
                       (encode({"id": "FOREIGN-PRIVATE-POLICY"}),))
        with patch.object(self.cs.evidence, "policy") as policy:
            with self.assertRaises(DomainError) as caught:
                self.cs.confirm(CUSTOMER, record["id"], {"contextRevision": 1})
            policy.assert_not_called()
        self.assertEqual(caught.exception.code, "ORDER_NOT_FOUND")
        self.assertNotIn("FOREIGN-PRIVATE-POLICY", encode(self.record(record["id"])))
        self.no_effects()

    def test_cs_t_06_adapter_rechecks_policy_between_intent_and_effect(self):
        record = self.approved()
        execute = self.cs.port.execute_resolution

        def changed(*args):
            self.policy({"id": "POLICY-CHANGED-AFTER-INTENT", "eligible": True, "requiresApproval": True})
            return execute(*args)

        with patch.object(self.cs.port, "execute_resolution", side_effect=changed):
            with self.assertRaises(DomainError) as caught:
                self.cs.confirm(CUSTOMER, record["id"], {"contextRevision": 1})
        self.assertEqual(caught.exception.code, "STALE_POLICY")
        self.assertEqual(self.record(record["id"])["status"], "UNRESOLVED")
        self.no_effects()

    def test_cs_t_06_adapter_read_failure_after_intent_has_no_effect(self):
        record = self.approved()
        with patch.object(self.cs.port.evidence, "policy", side_effect=ConnectionError("private diagnostic")):
            with self.assertRaises(DomainError) as caught:
                self.cs.confirm(CUSTOMER, record["id"], {"contextRevision": 1})
        self.assertEqual(caught.exception.code, "POLICY_UNAVAILABLE")
        self.assertEqual(self.record(record["id"])["status"], "UNRESOLVED")
        self.no_effects()

    def test_cs_t_04_adapter_rechecks_unknown_or_unavailable_stock_after_intent(self):
        for stock, availability in [(None, "UNKNOWN"), (0, "UNAVAILABLE")]:
            with self.subTest(availability=availability):
                with self.company.store.transaction() as db:
                    db.execute("UPDATE products SET stock=12 WHERE id='P-101'")
                record = self.approved()
                execute = self.cs.port.execute_resolution

                def change_stock(*args):
                    with self.company.store.transaction() as db:
                        db.execute("UPDATE products SET stock=? WHERE id='P-101'", (stock,))
                    return execute(*args)

                with patch.object(self.cs.port, "execute_resolution", side_effect=change_stock):
                    with self.assertRaises(DomainError) as caught:
                        self.cs.confirm(CUSTOMER, record["id"], {"contextRevision": 1})
                self.assertEqual(caught.exception.code, "STOCK_" + availability)
                self.assertEqual(self.record(record["id"])["status"], "UNRESOLVED")
                with self.company.store.read() as db:
                    self.assertEqual(db.execute("SELECT COUNT(*) FROM effects").fetchone()[0], 0)
                    self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-102'").fetchone()[0], 8)

    def test_cs_t_06_authorised_order_read_failure_is_retained(self):
        record = self.approved()
        with patch.object(self.cs.evidence, "order", side_effect=ConnectionError("private diagnostic")):
            with self.assertRaises(DomainError) as caught:
                self.cs.confirm(CUSTOMER, record["id"], {"contextRevision": 1})
        self.assertEqual(caught.exception.code, "ORDER_READ_UNAVAILABLE")
        self.assertEqual(self.record(record["id"])["status"], "UNRESOLVED")
        self.no_effects()

    def test_cs_t_06_revision_policy_failure_retains_safe_outcome(self):
        record = self.approved()
        with patch.object(self.cs.evidence, "policy", side_effect=TimeoutError("private diagnostic")):
            with self.company.store.transaction() as db:
                result = self.cs.revise(db, CUSTOMER, record["id"], {**NEEDS, "contextRevision": 1})
        self.assertEqual(result["status"], "UNRESOLVED")
        self.assertNotIn("confirmation", result["payload"])
        self.assertEqual(result["revision"], 1)
        self.no_effects()

    def test_cs_t_04_adapter_replay_returns_same_receipt_without_rechecking_or_effect(self):
        record = self.approved()
        result = self.cs.confirm(CUSTOMER, record["id"], {"contextRevision": 1})
        action_ref = result["payload"]["actionRef"]
        with patch.object(self.cs.port.evidence, "order") as read:
            replay = self.cs.port.execute_resolution(record["id"], action_ref, 1, "P-101")
            read.assert_not_called()
        self.assertEqual(replay, result["payload"]["result"])
        with self.assertRaises(DomainError) as caught:
            self.cs.port.execute_resolution(record["id"], action_ref, 1, "P-102")
        self.assertEqual(caught.exception.code, "ACTION_CONFLICT")
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM effects").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-101'").fetchone()[0], 11)

    def test_cs_t_06_failed_outcome_storage_cannot_claim_retention(self):
        self.policy({"eligible": None})
        with patch.object(Store, "save", side_effect=sqlite3.OperationalError("injected write failure")):
            with self.assertRaises(sqlite3.OperationalError):
                self.intake()
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM records").fetchone()[0], 0)
        self.no_effects()


if __name__ == "__main__":
    unittest.main()
