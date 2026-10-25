"""AP-T-05: durable decision intent and storage-only recording recovery.

These tests cover the recorded-decision-failure slice of AP-START-01. They use
the real SQLite store and the ordinary service facade, so a restart is a new
Company instance over the same database file.
"""
import tempfile
import unittest
from pathlib import Path

from beauty_company.application import Company
from beauty_company.contracts import Actor, DomainError

CUSTOMER = Actor("customer", "CUSTOMER", "Alex")
FOUNDER = Actor("founder", "FOUNDER", "Founder")
OTHER_FOUNDER = Actor("founder-2", "FOUNDER", "Second Founder")
NEEDS = {"message": "I need a fragrance-free moisturiser.", "concern": "HYDRATION", "budget": 60, "fragranceFree": True}
REASON = "Checked this exact simulated action."


class RecordingFailureTests(unittest.TestCase):
    """A decision whose recording failed must stay unapproved and stay recoverable."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "ap.sqlite3"
        self.company = Company(self.path)

    def pending_approval(self):
        """Drive a customer request to a PENDING review and return its approval id."""
        with self.company.store.transaction() as db:
            request = self.company.cs.submit(db, CUSTOMER, {**NEEDS, "orderId": "ORD-1001"})
        with self.company.store.transaction() as db:
            request = self.company.cs.coordinate(db, FOUNDER, request["id"])
        request = self.company.cs.confirm(CUSTOMER, request["id"], {"contextRevision": 1})
        return request["id"], request["payload"]["approvalId"]

    def arm_recording_failure(self):
        with self.company.store.transaction() as db:
            db.execute("INSERT OR REPLACE INTO faults VALUES('approval_recording')")

    def review(self, rid, company=None):
        company = company or self.company
        with company.store.read() as db:
            return company.ap.get(db, rid)

    def intent(self, rid, company=None):
        company = company or self.company
        with company.store.read() as db:
            return company.ap.intent(db, rid)

    def events(self, rid, company=None):
        company = company or self.company
        with company.store.read() as db:
            rows = db.execute("SELECT event FROM events WHERE entity_id=?", (rid,)).fetchall()
        return [row["event"] for row in rows]

    def effects(self, company=None):
        company = company or self.company
        with company.store.read() as db:
            return db.execute("SELECT COUNT(*) FROM effects").fetchone()[0]

    def decide(self, rid, kind="APPROVE", reason=REASON, actor=FOUNDER, company=None):
        company = company or self.company
        return company.decide(actor, rid, {"decision": kind, "contextRevision": 1, "reason": reason})

    def failed_decision(self):
        """Return the approval id of a request whose decision recording failed."""
        request_id, approval_id = self.pending_approval()
        self.arm_recording_failure()
        with self.assertRaises(DomainError) as caught:
            self.decide(approval_id)
        self.assertEqual(caught.exception.code, "RECORDING_FAILED")
        return request_id, approval_id

    def test_ap_t_05_failed_recording_exposes_recording_failed_without_any_authority(self):
        request_id, approval_id = self.failed_decision()
        review = self.review(approval_id)
        self.assertEqual(review["status"], "RECORDING_FAILED")
        # No committed envelope: nothing may be read back as an approval.
        self.assertIsNone(review["decision_id"])
        self.assertIsNone(review["decision"])
        self.assertIsNone(review["reason"])
        self.assertIsNone(review["founder_id"])
        self.assertEqual(review["delivery"], "NOT_READY")
        # No delivered approval and no business effect.
        with self.company.store.read() as db:
            origin = self.company.store.get(db, request_id)
        self.assertEqual(origin["status"], "REVIEW_PENDING")
        self.assertNotIn("decisionId", origin["payload"])
        self.assertEqual(self.effects(), 0)
        # The commit itself produced no authoritative decision audit.
        self.assertNotIn("DECISION_COMMITTED", self.events(approval_id))

    def test_ap_t_05_failed_recording_keeps_the_intended_scope_recoverable(self):
        request_id, approval_id = self.failed_decision()
        intent = self.intent(approval_id)
        self.assertIsNotNone(intent)
        self.assertEqual(intent["status"], "RECORDING_FAILED")
        self.assertEqual(intent["kind"], "APPROVE")
        self.assertEqual(intent["reason"], REASON)
        self.assertEqual(intent["founder_id"], FOUNDER.id)
        self.assertEqual(intent["revision"], 1)
        self.assertEqual(intent["origin_id"], request_id)
        self.assertEqual(intent["action"]["kind"], "SIMULATED_EXCHANGE")
        self.assertIsNone(intent["decision_id"])
        # A receipt and a pending intent are not an approval.
        self.assertIsNone(self.review(approval_id)["decision_id"])

    def test_ap_t_05_failed_recording_is_visible_in_the_snapshot(self):
        _, approval_id = self.failed_decision()
        snapshot = self.company.snapshot(FOUNDER)
        review = next(item for item in snapshot["approvals"] if item["id"] == approval_id)
        self.assertEqual(review["status"], "RECORDING_FAILED")
        self.assertEqual(review["intent"]["status"], "RECORDING_FAILED")
        self.assertEqual(review["intent"]["kind"], "APPROVE")

    def test_ap_t_05_storage_only_recovery_commits_the_same_intended_decision(self):
        request_id, approval_id = self.failed_decision()
        # A new process over the same database finds the intent in storage alone.
        restarted = Company(self.path)
        recovered = restarted.recover_decision(FOUNDER, approval_id)
        self.assertEqual(recovered["status"], "APPROVED")
        self.assertIsNotNone(recovered["decision_id"])
        self.assertEqual(recovered["decision"], "APPROVE")
        self.assertEqual(recovered["reason"], REASON)
        self.assertEqual(recovered["delivery"], "DELIVERED")
        # Exactly one authoritative decision and one decision audit.
        self.assertEqual(self.events(approval_id, restarted).count("DECISION_COMMITTED"), 1)
        # The same intended identity was committed, and nothing was dispatched twice.
        intent = self.intent(approval_id, restarted)
        self.assertEqual(intent["status"], "COMMITTED")
        self.assertEqual(intent["decision_id"], recovered["decision_id"])
        with restarted.store.read() as db:
            origin = restarted.store.get(db, request_id)
        self.assertEqual(origin["status"], "AWAITING_CONFIRMATION")
        self.assertEqual(origin["payload"]["decisionId"], recovered["decision_id"])
        self.assertEqual(self.effects(restarted), 0)

    def test_ap_t_05_recovery_never_commits_a_second_decision(self):
        _, approval_id = self.failed_decision()
        first = self.company.recover_decision(FOUNDER, approval_id)
        second = self.company.recover_decision(FOUNDER, approval_id)
        self.assertEqual(first["decision_id"], second["decision_id"])
        self.assertEqual(self.events(approval_id).count("DECISION_COMMITTED"), 1)
        self.assertEqual(self.events(approval_id).count("RECORDED_DECISION_RECEIVED"), 0)
        self.assertEqual(self.effects(), 0)

    def test_ap_t_05_recovery_never_repeats_business_execution(self):
        request_id, approval_id = self.failed_decision()
        self.company.recover_decision(FOUNDER, approval_id)
        self.company.recover_decision(FOUNDER, approval_id)
        for _ in range(3):
            self.company.cs.confirm(CUSTOMER, request_id, {"contextRevision": 1})
        self.assertEqual(self.effects(), 1)

    def test_ap_t_05_conflicting_kind_cannot_replace_the_recorded_intent(self):
        _, approval_id = self.failed_decision()
        with self.assertRaises(DomainError) as caught:
            self.decide(approval_id, kind="REJECT", reason="Changed my mind entirely.")
        self.assertEqual(caught.exception.code, "DECISION_CONFLICT")
        intent = self.intent(approval_id)
        self.assertEqual(intent["kind"], "APPROVE")
        self.assertEqual(intent["reason"], REASON)
        self.assertEqual(self.review(approval_id)["status"], "RECORDING_FAILED")
        self.assertIsNone(self.review(approval_id)["decision_id"])

    def test_ap_t_05_conflicting_reason_cannot_replace_the_recorded_intent(self):
        _, approval_id = self.failed_decision()
        with self.assertRaises(DomainError) as caught:
            self.decide(approval_id, reason="A different reason for the same action.")
        self.assertEqual(caught.exception.code, "DECISION_CONFLICT")
        self.assertEqual(self.intent(approval_id)["reason"], REASON)

    def test_ap_t_05_recovery_rejects_a_stale_context_revision(self):
        request_id, approval_id = self.failed_decision()
        # The proposal moved on while the decision was failing to record.
        with self.company.store.transaction() as db:
            db.execute("UPDATE records SET revision=2 WHERE id=?", (request_id,))
        with self.assertRaises(DomainError) as caught:
            self.company.recover_decision(FOUNDER, approval_id)
        self.assertEqual(caught.exception.code, "STALE_SCOPE")
        self.assertIsNone(self.review(approval_id)["decision_id"])
        self.assertNotIn("DECISION_COMMITTED", self.events(approval_id))
        self.assertEqual(self.effects(), 0)

    def test_ap_t_05_recovery_rejects_a_superseded_request(self):
        request_id, approval_id = self.failed_decision()
        with self.company.store.transaction() as db:
            self.company.cs.revise(db, CUSTOMER, request_id, {**NEEDS, "contextRevision": 1})
        with self.assertRaises(DomainError) as caught:
            self.company.recover_decision(FOUNDER, approval_id)
        self.assertEqual(caught.exception.code, "REVIEW_CLOSED")
        self.assertIsNone(self.review(approval_id)["decision_id"])
        self.assertNotIn("DECISION_COMMITTED", self.events(approval_id))
        self.assertEqual(self.effects(), 0)

    def test_ap_t_05_recovery_requires_the_current_founder_authority(self):
        _, approval_id = self.failed_decision()
        with self.assertRaises(DomainError) as caught:
            self.company.recover_decision(CUSTOMER, approval_id)
        self.assertEqual(caught.exception.status, 403)
        with self.assertRaises(DomainError) as caught:
            self.company.recover_decision(OTHER_FOUNDER, approval_id)
        self.assertEqual(caught.exception.status, 403)
        self.assertIsNone(self.review(approval_id)["decision_id"])
        self.assertEqual(self.review(approval_id)["status"], "RECORDING_FAILED")

    def test_ap_t_05_a_failed_recording_grants_no_execution(self):
        request_id, approval_id = self.failed_decision()
        with self.assertRaises(DomainError):
            self.company.cs.confirm(CUSTOMER, request_id, {"contextRevision": 1})
        self.assertEqual(self.effects(), 0)
        with self.assertRaises(DomainError) as caught:
            self.company.redeliver(FOUNDER, approval_id)
        self.assertEqual(caught.exception.code, "NO_DECISION")
        self.assertEqual(self.review(approval_id)["delivery"], "NOT_READY")

    def test_ap_t_05_recovery_without_a_stored_intent_is_refused(self):
        _, approval_id = self.pending_approval()
        with self.assertRaises(DomainError) as caught:
            self.company.recover_decision(FOUNDER, approval_id)
        self.assertEqual(caught.exception.code, "NO_INTENT")
        self.assertEqual(self.review(approval_id)["status"], "PENDING")
        self.assertIsNone(self.review(approval_id)["decision_id"])

    def test_ap_t_05_the_same_decision_can_be_retried_without_recovery(self):
        _, approval_id = self.failed_decision()
        retried = self.decide(approval_id)
        self.assertEqual(retried["status"], "APPROVED")
        self.assertEqual(retried["decision"], "APPROVE")
        self.assertEqual(self.events(approval_id).count("DECISION_COMMITTED"), 1)
        self.assertEqual(self.effects(), 0)

    def test_ap_t_05_failed_delivery_after_recovery_preserves_the_committed_decision(self):
        request_id, approval_id = self.failed_decision()
        # The recovery commits the decision; its delivery then fails.
        with self.company.store.transaction() as db:
            db.execute("INSERT OR REPLACE INTO faults VALUES('approval_delivery')")
        recovered = self.company.recover_decision(FOUNDER, approval_id)
        self.assertEqual(recovered["status"], "APPROVED")
        self.assertEqual(recovered["delivery"], "FAILED")
        self.assertIsNotNone(recovered["decision_id"])
        with self.company.store.read() as db:
            origin = self.company.store.get(db, request_id)
        self.assertNotIn("decisionId", origin["payload"])
        self.assertEqual(self.effects(), 0)
        # Redelivery reuses the committed decision id and never repeats execution.
        again = self.company.redeliver(FOUNDER, approval_id)
        self.assertEqual(again["delivery"], "DELIVERED")
        self.assertEqual(again["decision_id"], recovered["decision_id"])
        self.assertEqual(self.events(approval_id).count("DECISION_COMMITTED"), 1)
        self.assertEqual(self.effects(), 0)


if __name__ == "__main__":
    unittest.main()
