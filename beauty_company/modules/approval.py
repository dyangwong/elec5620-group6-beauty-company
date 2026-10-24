"""AP-M-01: exact-scope decision/request/audit commit, then separate delivery.

A decision intent is a durable, identifiable *proposal* to decide. It is not a
committed decision: it grants no authority, delivers nothing and dispatches no
business work. Recording it before the commit is what makes a failed commit
recoverable from storage alone (AP-T-05 / AP-AC-05 E3).
"""
import json

from ..contracts import DECISIONS, DECISION_STATES, DomainError, require_role, revision_value, text_value
from ..store import Store, encode, new_id, now
from .coordination import Coordination

# A decision intent may be proposed, committed, or left failed after a recording
# error. Only COMMITTED carries a decision id; the others grant no authority.
INTENT_STATES = {"PROPOSED", "COMMITTED", "RECORDING_FAILED"}
# An approval request may additionally be left failed after a recording error.
RECORDING_FAILED = "RECORDING_FAILED"


class Approval:
    @staticmethod
    def submit(db, role, origin_id, revision, action, evidence, action_ref=None, predecessor=None):
        if role not in {"CS", "MC"} or not action or not evidence:
            raise DomainError("Review requires a supported origin, exact action and evidence.")
        existing = db.execute("SELECT id FROM approvals WHERE origin_role=? AND origin_id=? AND revision=?",
                              (role, origin_id, revision)).fetchone()
        if existing:
            return existing["id"]
        rid = new_id("AP")
        db.execute("""INSERT INTO approvals
            (id,origin_role,origin_id,revision,action_ref,action,evidence,status,delivery,created,predecessor)
            VALUES(?,?,?,?,?,?,?,'PENDING','NOT_READY',?,?)""",
                   (rid, role, origin_id, revision, action_ref, encode(action), encode(evidence), now(), predecessor))
        Store.event(db, rid, "AP", "REVIEW_REQUEST_PERSISTED", {"originId": origin_id, "contextRevision": revision})
        return rid

    @staticmethod
    def get(db, rid):
        row = db.execute("SELECT * FROM approvals WHERE id=?", (rid,)).fetchone()
        if not row:
            raise DomainError("Review request not found.", 404, "NOT_FOUND")
        result = dict(row)
        result["action"] = json.loads(result["action"])
        result["evidence"] = json.loads(result["evidence"])
        return result

    @staticmethod
    def _decode_intent(row):
        result = dict(row)
        result["action"] = json.loads(result["action"])
        result["evidence"] = json.loads(result["evidence"])
        return result

    @staticmethod
    def intent(db, rid):
        """Read the stored decision intent for a review request, if one exists."""
        row = db.execute("SELECT * FROM approval_intents WHERE approval_id=?", (rid,)).fetchone()
        return Approval._decode_intent(row) if row else None

    @staticmethod
    def intent_by_id(db, intent_id):
        """Read the stored decision intent by its own identifier."""
        row = db.execute("SELECT * FROM approval_intents WHERE id=?", (intent_id,)).fetchone()
        return Approval._decode_intent(row) if row else None

    def prepare_intent(self, db, actor, rid, data):
        """Validate the request and persist an identifiable decision intent.

        The intent records the Founder, the exact scope, the kind and the reason.
        It is written in its own committed transaction so a later commit failure
        leaves it recoverable from storage. An existing intent is never silently
        replaced: a conflicting kind or reason is rejected.
        """
        require_role(actor, "FOUNDER")
        kind = data.get("decision")
        if not isinstance(kind, str) or kind not in DECISIONS:
            raise DomainError("Choose APPROVE, REJECT or REQUEST_REVISION.")
        reason = text_value(data.get("reason"), "Decision reason", 1000)
        revision = revision_value(data.get("contextRevision"))
        review = self.get(db, rid)
        existing = self.intent(db, rid)
        if review["decision_id"]:
            if review["decision"] == kind and review["reason"] == reason:
                # Already committed. Keep the authoritative envelope and its intent.
                if existing:
                    return existing
                return self._backfill_intent(db, review, actor, kind, reason)
            raise DomainError("A committed decision cannot be overwritten.", 409, "DECISION_CONFLICT")
        if review["status"] not in {"PENDING", RECORDING_FAILED}:
            raise DomainError("This request is not open for a decision.", 409, "REVIEW_CLOSED")
        origin = Store.get(db, review["origin_id"], review["origin_role"])
        if revision != review["revision"] or origin["revision"] != revision or origin["payload"].get("approvalId") != rid:
            raise DomainError("This action or context revision has changed. Fresh review is required.", 409, "STALE_SCOPE")
        if existing:
            if existing["kind"] != kind or existing["reason"] != reason:
                raise DomainError("A recorded decision intent cannot be replaced by a different decision.", 409, "DECISION_CONFLICT")
            if existing["founder_id"] != actor.id:
                raise DomainError("This decision intent belongs to another authorised decision maker.", 403, "FORBIDDEN")
            return existing
        intent_id = new_id("INT")
        db.execute("""INSERT INTO approval_intents
            (id,approval_id,founder_id,kind,reason,origin_role,origin_id,revision,action_ref,action,evidence,status,created,updated)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,'PROPOSED',?,?)""",
                   (intent_id, rid, actor.id, kind, reason, review["origin_role"], review["origin_id"],
                    review["revision"], review["action_ref"], encode(review["action"]), encode(review["evidence"]),
                    now(), now()))
        Store.event(db, rid, "AP", "DECISION_INTENT_RECORDED",
                    {"intentId": intent_id, "decision": kind, "reason": reason, "founderId": actor.id,
                     "contextRevision": review["revision"], "actionRef": review["action_ref"],
                     "committed": False, "authority": False})
        return self.intent(db, rid)

    @staticmethod
    def _backfill_intent(db, review, actor, kind, reason):
        """Give a pre-existing committed decision the same durable intent record."""
        intent_id = new_id("INT")
        db.execute("""INSERT INTO approval_intents
            (id,approval_id,founder_id,kind,reason,origin_role,origin_id,revision,action_ref,action,evidence,status,decision_id,created,updated)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,'COMMITTED',?,?,?)""",
                   (intent_id, review["id"], review["founder_id"] or actor.id, kind, reason,
                    review["origin_role"], review["origin_id"], review["revision"], review["action_ref"],
                    encode(review["action"]), encode(review["evidence"]), review["decision_id"], now(), now()))
        return Approval.intent(db, review["id"])

    def commit_intent(self, db, intent_id, actor):
        """Atomically commit decision, request state and audit for a stored intent.

        Returns the committed review, or None when the injected recording fault
        fired and the decision was not recorded. A failed commit never leaves a
        decision id, a delivered approval or a business effect behind.
        """
        intent = self.intent_by_id(db, intent_id)
        if not intent:
            raise DomainError("No stored decision intent was found.", 404, "NOT_FOUND")
        if intent["status"] not in INTENT_STATES:
            raise DomainError("The stored decision intent has an unknown state.", 409, "INVALID_STATE")
        require_role(actor, "FOUNDER")
        if intent["founder_id"] != actor.id:
            raise DomainError("This decision intent belongs to another authorised decision maker.", 403, "FORBIDDEN")
        review = self.get(db, intent["approval_id"])
        if review["decision_id"]:
            if review["decision"] == intent["kind"] and review["reason"] == intent["reason"]:
                # One authoritative decision per request. A repeated commit is not a second decision.
                return review
            raise DomainError("A committed decision cannot be overwritten.", 409, "DECISION_CONFLICT")
        if review["status"] not in {"PENDING", RECORDING_FAILED}:
            raise DomainError("This request is not open for a decision.", 409, "REVIEW_CLOSED")
        # Recovery revalidates the current scope; a stale action or revision is never substituted.
        origin = Store.get(db, intent["origin_id"], intent["origin_role"])
        if (review["revision"] != intent["revision"] or origin["revision"] != intent["revision"]
                or origin["payload"].get("approvalId") != review["id"]
                or review["action"] != intent["action"] or review["action_ref"] != intent["action_ref"]):
            raise DomainError("This action or context revision has changed. Fresh review is required.", 409, "STALE_SCOPE")
        if Store.fault(db, "approval_recording"):
            # The decision is not recorded. Expose the failure without any committed envelope.
            self.mark_recording_failed(db, intent, {"reason": "Injected decision recording failure."})
            return None
        decision_id = new_id("DEC")
        db.execute("""UPDATE approvals SET status=?,decision_id=?,decision=?,reason=?,founder_id=?,delivery='PENDING'
                      WHERE id=?""", (DECISION_STATES[intent["kind"]], decision_id, intent["kind"], intent["reason"],
                                      intent["founder_id"], review["id"]))
        db.execute("UPDATE approval_intents SET status='COMMITTED',decision_id=?,updated=? WHERE id=?",
                   (decision_id, now(), intent["id"]))
        # This append and the two authoritative decision fields share one SQLite transaction.
        Store.event(db, review["id"], "AP", "DECISION_COMMITTED", {"decisionId": decision_id, "decision": intent["kind"],
                    "reason": intent["reason"], "founderId": intent["founder_id"], "contextRevision": intent["revision"],
                    "actionRef": review["action_ref"], "intentId": intent["id"]})
        return self.get(db, review["id"])

    def mark_recording_failed(self, db, intent, detail=None):
        """Expose RECORDING_FAILED for a decision that was not recorded.

        The request keeps no decision id, decision, reason or founder, so it grants
        no authority. The stored intent keeps the intended identity for recovery.
        """
        rid = intent["approval_id"]
        review = self.get(db, rid)
        if review["decision_id"]:
            # A committed decision is never downgraded by a later recording error.
            return review
        db.execute("UPDATE approvals SET status=? WHERE id=?", (RECORDING_FAILED, rid))
        db.execute("UPDATE approval_intents SET status='RECORDING_FAILED',updated=? WHERE id=?", (now(), intent["id"]))
        event = {"intentId": intent["id"], "decision": intent["kind"], "reason": intent["reason"],
                 "founderId": intent["founder_id"], "contextRevision": intent["revision"],
                 "actionRef": intent["action_ref"], "committed": False, "authority": False,
                 "recoverable": True, **(detail or {})}
        # The failure audit is best effort; the state above must survive an audit outage.
        db.execute("SAVEPOINT recording_failure_audit")
        try:
            Store.event(db, rid, "AP", "DECISION_RECORDING_FAILED", event)
        except Exception:
            db.execute("ROLLBACK TO recording_failure_audit")
        db.execute("RELEASE recording_failure_audit")
        return self.get(db, rid)

    def deliver(self, db, rid):
        review = self.get(db, rid)
        if not review["decision_id"]:
            raise DomainError("A receipt is not a committed decision.", 409, "NO_DECISION")
        origin = Store.get(db, review["origin_id"], review["origin_role"])
        if origin["revision"] != review["revision"] or origin["payload"].get("approvalId") != rid:
            db.execute("UPDATE approvals SET delivery='STALE' WHERE id=?", (rid,))
            return self.get(db, rid)
        if origin["payload"].get("decisionId") == review["decision_id"]:
            return review
        if Store.fault(db, "approval_delivery"):
            db.execute("UPDATE approvals SET delivery='FAILED' WHERE id=?", (rid,))
            Store.event(db, rid, "AP", "DELIVERY_FAILED", {"decisionId": review["decision_id"], "committedDecisionPreserved": True})
            return self.get(db, rid)
        origin["payload"]["decisionId"] = review["decision_id"]
        origin["payload"]["decision"] = review["decision"]
        if review["origin_role"] == "CS":
            origin["status"] = {"APPROVE": "AWAITING_CONFIRMATION", "REJECT": "REJECTED", "REQUEST_REVISION": "NEEDS_INFORMATION"}[review["decision"]]
            origin["payload"]["note"] = {"APPROVE": "Exact-scope approval recorded. The Customer must confirm again; current eligibility and stock will be rechecked.", "REJECT": "The Founder rejected this proposal. No business action was executed.", "REQUEST_REVISION": "The Founder requested corrected needs and a fresh proposal/review."}[review["decision"]]
            coordination_state = {"APPROVE": "PENDING_VALIDATION", "REJECT": "CANCELLED", "REQUEST_REVISION": "CLARIFICATION_REQUIRED"}[review["decision"]]
            Coordination.state(db, origin["payload"]["coordinationId"], coordination_state,
                               "RECORDED_REVIEW_OBSERVED", {"decisionId": review["decision_id"], "decision": review["decision"]})
        else:
            origin["status"] = {"APPROVE": "APPROVED", "REJECT": "REJECTED", "REQUEST_REVISION": "REVISION_REQUIRED"}[review["decision"]]
        Store.save(db, origin)
        db.execute("UPDATE approvals SET delivery='DELIVERED' WHERE id=?", (rid,))
        Store.event(db, origin["id"], review["origin_role"], "RECORDED_DECISION_RECEIVED",
                    {"decisionId": review["decision_id"], "decision": review["decision"], "businessExecution": False})
        return self.get(db, rid)

    @staticmethod
    def supersede(db, rid):
        if rid:
            db.execute("UPDATE approvals SET status='SUPERSEDED' WHERE id=?", (rid,))
            Store.event(db, rid, "AP", "SCOPE_SUPERSEDED", {"freshReviewRequired": True})
