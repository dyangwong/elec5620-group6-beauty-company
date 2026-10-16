"""AP-M-01: exact-scope decision/request/audit commit, then separate delivery."""
import json

from ..contracts import DECISIONS, DECISION_STATES, DomainError, require_role, revision_value, text_value
from ..store import Store, encode, new_id, now
from .coordination import Coordination


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

    def decide(self, db, actor, rid, data):
        require_role(actor, "FOUNDER")
        kind = data.get("decision")
        if not isinstance(kind, str) or kind not in DECISIONS:
            raise DomainError("Choose APPROVE, REJECT or REQUEST_REVISION.")
        reason = text_value(data.get("reason"), "Decision reason", 1000)
        revision = revision_value(data.get("contextRevision"))
        review = self.get(db, rid)
        origin = Store.get(db, review["origin_id"], review["origin_role"])
        if revision != review["revision"] or origin["revision"] != revision or origin["payload"].get("approvalId") != rid:
            raise DomainError("This action or context revision has changed. Fresh review is required.", 409, "STALE_SCOPE")
        if review["decision_id"]:
            if review["decision"] == kind and review["reason"] == reason:
                return review
            raise DomainError("A committed decision cannot be overwritten.", 409, "DECISION_CONFLICT")
        if review["status"] != "PENDING":
            raise DomainError("This request is not open for a decision.", 409, "REVIEW_CLOSED")
        decision_id = new_id("DEC")
        db.execute("""UPDATE approvals SET status=?,decision_id=?,decision=?,reason=?,founder_id=?,delivery='PENDING'
                      WHERE id=?""", (DECISION_STATES[kind], decision_id, kind, reason, actor.id, rid))
        # This append and the two authoritative decision fields share one SQLite transaction.
        Store.event(db, rid, "AP", "DECISION_COMMITTED", {"decisionId": decision_id, "decision": kind,
                    "reason": reason, "founderId": actor.id, "contextRevision": revision, "actionRef": review["action_ref"]})
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
