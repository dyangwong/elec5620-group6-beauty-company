"""AP-T-05: durable decision intent and storage-only recording recovery.

These tests cover the recorded-decision-failure slice of AP-START-01. They use
the real SQLite store and the ordinary service facade, so a restart is a new
Company instance over the same database file.
"""
import tempfile
import unittest
import json
from copy import deepcopy
from pathlib import Path

from beauty_company.application import Company
from beauty_company.contracts import Actor, DomainError
from beauty_company.store import Store, encode

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


class RegisteredActionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.company = Company(Path(self.temp.name) / 'registry.sqlite3')

    pending_approval = RecordingFailureTests.pending_approval

    def assert_no_authority(self, approval_count=0):
        with self.company.store.read() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM approvals').fetchone()[0], approval_count)
            self.assertEqual(db.execute('SELECT count(*) FROM approvals WHERE decision_id IS NOT NULL').fetchone()[0], 0)
            self.assertEqual(db.execute('SELECT count(*) FROM effects').fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-101'").fetchone()[0], 12)

    def test_ap_t_01_unknown_or_malformed_actions_cannot_obtain_a_receipt(self):
        with self.company.store.transaction() as db:
            origin = Store.create(db, 'MC', FOUNDER.id, 'DRAFTING', {}, 'MC')
        valid = {'kind': 'REVIEW_MOCK_DRAFT', 'draftId': origin, 'draftRevision': 1}
        evidence = {'catalogueRef': 'catalogue:P-101:v1', 'facts': ['Fragrance-free']}
        cases = [('MC', {'kind': 'UNREGISTERED_ACTION', 'risk': 'UNKNOWN'}, evidence, None, 1),
                 ('MC', {**valid, 'risk': 'LOW'}, evidence, None, 1),
                 ('MC', {**valid, 'kind': []}, evidence, None, 1),
                 ('MC', {**valid, 'draftRevision': True}, evidence, None, 1),
                 ('MC', valid, evidence, None, True),
                 ('MC', valid, evidence, 'unregistered-ref', 1),
                 ('MC', valid, {}, None, 1), ('MC', [], evidence, None, 1),
                 ('CO', valid, evidence, None, 1), ('CS', valid, evidence, None, 1),
                 ('BA', {'type': 'REASSESS_ADVICE', 'consultationId': origin,
                         'contextRevision': 1}, {'needs': 'unknown'}, None, 1)]
        for role, action, facts, ref, revision in cases:
            with self.subTest(role=role, action=action, revision=revision):
                with self.assertRaises(DomainError) as caught, self.company.store.transaction() as db:
                    self.company.ap.submit(db, role, origin, revision, action, facts, ref)
                self.assertEqual(caught.exception.code, 'AP_ACTION_UNSUPPORTED')
                self.assert_no_authority()
        with self.company.store.read() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE event='REVIEW_REQUEST_PERSISTED'").fetchone()[0], 0)

    def test_ap_t_01_registered_routes_record_server_owned_review_classes(self):
        _, cs_id = self.pending_approval()
        mc = self.company.campaign(FOUNDER, {'brief': 'Product introduction', 'productId': 'P-101'})
        for rid, expected in ((cs_id, 'DISPUTED_EXCHANGE'), (mc['payload']['approvalId'], 'CONTENT_REVIEW')):
            with self.company.store.read() as db:
                row = db.execute("SELECT detail FROM events WHERE entity_id=? AND event='REVIEW_REQUEST_PERSISTED'", (rid,)).fetchone()
                detail = json.loads(row['detail'])
                self.assertEqual(detail['riskClass'], expected)
                self.assertTrue(detail['requiresFounderReview'])
                self.assertFalse(detail['businessExecution'])
                self.assertEqual(detail['policyVersion'], 'AP-REGISTERED-v1')
        self.assert_no_authority(2)

    def test_ap_t_01_existing_receipt_only_acknowledges_identical_scope(self):
        record = self.company.campaign(FOUNDER, {'brief': 'Product introduction', 'productId': 'P-101'})
        with self.company.store.transaction() as db:
            rid = record['payload']['approvalId']
            review = self.company.ap.get(db, rid)
            self.assertEqual(self.company.ap.submit(db, 'MC', record['id'], 1,
                review['action'], review['evidence']), rid)
        changed = deepcopy(review['evidence']); changed['facts'] = ['50 ml']
        with self.assertRaises(DomainError) as caught, self.company.store.transaction() as db:
            self.company.ap.submit(db, 'MC', record['id'], 1, review['action'], changed)
        self.assertEqual(caught.exception.code, 'STALE_SCOPE')
        self.assert_no_authority(1)

    def test_ap_t_01_registered_exchange_rejects_forged_target_before_receipt(self):
        record, rid = self.pending_approval()
        with self.company.store.read() as db:
            review = self.company.ap.get(db, rid)
        for action, evidence, ref in (({**review['action'], 'productId': 'P-102'}, review['evidence'], review['action_ref']),
                (review['action'], {**review['evidence'], 'policyRef': 'invented'}, review['action_ref']),
                (review['action'], review['evidence'], 'different-ref')):
            with self.subTest(action=action, evidence=evidence, ref=ref):
                with self.assertRaises(DomainError) as caught, self.company.store.transaction() as db:
                    self.company.ap.submit(db, 'CS', record, 1, action, evidence, ref)
                self.assertEqual(caught.exception.code, 'STALE_SCOPE')
        self.assert_no_authority(1)

    def test_ap_t_01_unknown_stored_action_cannot_prepare_or_recover_a_decision(self):
        _, rid = self.pending_approval()
        with self.company.store.read() as db:
            original = self.company.ap.get(db, rid)
        unknown = encode({'kind': 'UNREGISTERED_ACTION', 'risk': 'UNKNOWN'})
        with self.company.store.transaction() as db:
            db.execute('UPDATE approvals SET action=? WHERE id=?', (unknown, rid))
        with self.assertRaises(DomainError) as caught:
            self.company.decide(FOUNDER, rid, {'decision': 'APPROVE', 'reason': REASON, 'contextRevision': 1})
        self.assertEqual(caught.exception.code, 'AP_ACTION_UNSUPPORTED')
        with self.company.store.read() as db:
            self.assertIsNone(self.company.ap.intent(db, rid))
        self.assert_no_authority(1)
        with self.company.store.transaction() as db:
            db.execute('UPDATE approvals SET action=? WHERE id=?', (encode(original['action']), rid))
            self.company.ap.prepare_intent(db, FOUNDER, rid,
                {'decision': 'APPROVE', 'reason': REASON, 'contextRevision': 1})
        # Even a mutually matching but unregistered stored action is not authority.
        with self.company.store.transaction() as db:
            db.execute('UPDATE approvals SET action=? WHERE id=?', (unknown, rid))
            db.execute('UPDATE approval_intents SET action=? WHERE approval_id=?', (unknown, rid))
        with self.assertRaises(DomainError) as caught:
            Company(self.company.store.path).recover_decision(FOUNDER, rid)
        self.assertEqual(caught.exception.code, 'AP_ACTION_UNSUPPORTED')
        self.assert_no_authority(1)

    def test_ap_t_01_current_policy_must_support_review_before_founder_intent(self):
        _, rid = self.pending_approval()
        with self.company.store.read() as db:
            original = json.loads(db.execute("SELECT policy FROM orders WHERE id='ORD-1001'").fetchone()[0])
        cases = [({**original, 'requiresApproval': False}, 'POLICY_MISSING'),
                 ({**original, 'conflictingRefs': ['OTHER']}, 'POLICY_CONFLICTING'),
                 ({**original, 'id': 'NEW-POLICY'}, 'STALE_POLICY')]
        for policy, code in cases:
            with self.subTest(policy=policy):
                with self.company.store.transaction() as db:
                    db.execute("UPDATE orders SET policy=? WHERE id='ORD-1001'", (encode(policy),))
                with self.assertRaises(DomainError) as caught:
                    self.company.decide(FOUNDER, rid, {'decision': 'APPROVE', 'reason': REASON, 'contextRevision': 1})
                self.assertEqual(caught.exception.code, code)
                with self.company.store.read() as db:
                    self.assertIsNone(self.company.ap.intent(db, rid))
                self.assert_no_authority(1)

    def test_ap_t_01_recovery_rechecks_policy_and_refuses_changed_evidence(self):
        _, rid = self.pending_approval()
        self.company.set_fault(FOUNDER, 'approval_recording')
        with self.assertRaises(DomainError):
            self.company.decide(FOUNDER, rid, {'decision': 'APPROVE', 'reason': REASON, 'contextRevision': 1})
        self.company.set_fault(FOUNDER, 'none')
        with self.company.store.transaction() as db:
            original = self.company.ap.get(db, rid)
            changed = {**original['evidence'], 'policyRef': 'changed'}
            db.execute('UPDATE approvals SET evidence=? WHERE id=?', (encode(changed), rid))
        with self.assertRaises(DomainError) as caught:
            Company(self.company.store.path).recover_decision(FOUNDER, rid)
        self.assertEqual(caught.exception.code, 'STALE_SCOPE')
        with self.company.store.transaction() as db:
            db.execute('UPDATE approvals SET evidence=? WHERE id=?', (encode(original['evidence']), rid))
            policy = json.loads(db.execute("SELECT policy FROM orders WHERE id='ORD-1001'").fetchone()[0])
            policy['requiresApproval'] = False
            db.execute("UPDATE orders SET policy=? WHERE id='ORD-1001'", (encode(policy),))
        with self.assertRaises(DomainError) as caught:
            Company(self.company.store.path).recover_decision(FOUNDER, rid)
        self.assertEqual(caught.exception.code, 'POLICY_MISSING')
        self.assert_no_authority(1)

    def test_ap_t_01_delivery_rechecks_policy_preserving_committed_decision(self):
        _, rid = self.pending_approval()
        self.company.set_fault(FOUNDER, 'approval_delivery')
        committed = self.company.decide(FOUNDER, rid, {'decision': 'APPROVE', 'reason': REASON, 'contextRevision': 1})
        self.assertEqual(committed['delivery'], 'FAILED')
        self.company.set_fault(FOUNDER, 'none')
        with self.company.store.transaction() as db:
            policy = json.loads(db.execute("SELECT policy FROM orders WHERE id='ORD-1001'").fetchone()[0])
            policy['requiresApproval'] = False
            db.execute("UPDATE orders SET policy=? WHERE id='ORD-1001'", (encode(policy),))
        with self.assertRaises(DomainError) as caught:
            self.company.redeliver(FOUNDER, rid)
        self.assertEqual(caught.exception.code, 'POLICY_MISSING')
        with self.company.store.read() as db:
            current = self.company.ap.get(db, rid)
            self.assertEqual(current['decision_id'], committed['decision_id'])
            self.assertEqual(current['delivery'], 'FAILED')
            self.assertEqual(db.execute('SELECT count(*) FROM effects').fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT stock FROM products WHERE id='P-101'").fetchone()[0], 12)


if __name__ == "__main__":
    unittest.main()
