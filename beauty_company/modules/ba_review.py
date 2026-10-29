"""BA-UC-01 E4: consented unresolved-product review, never advice authority."""
import sqlite3

from ..contracts import DomainError, require_role, revision_value, text_value
from ..store import Store


def medical_scope(payload, issue=""):
    return payload.get("errorCode") == "MEDICAL_SCOPE" or any(
        word in text.lower() for text in [*payload.get("messages", []), issue]
        for word in ("diagnose", "diagnosis", "treat eczema", "诊断", "治疗"))


def current_customer(db, actor, authenticate=None):
    if authenticate and authenticate() != actor:
        raise DomainError("The current identity changed. Sign in again.", 401, "UNAUTHENTICATED")
    require_role(actor, "CUSTOMER")
    user = db.execute("SELECT role FROM users WHERE id=?", (actor.id,)).fetchone()
    if not user or user["role"] != "CUSTOMER":
        raise DomainError("Customer access changed.", 403, "FORBIDDEN")


def review_action(record):
    return {"type": "REASSESS_ADVICE", "consultationId": record["id"],
            "contextRevision": record["revision"]}


def check_review_scope(record, review):
    p = record["payload"]
    context = p.get("reviewContext")
    if (record["kind"] != "BA" or not p.get("naturalNeeds")
            or record["status"] in {"CANCELLED", "COMPLETED"}
            or p.get("approvalId") != review["id"] or record["revision"] != review["revision"]
            or review["origin_id"] != record["id"] or review["origin_role"] != "BA"
            or review["action_ref"] is not None or review["action"] != review_action(record)
            or not isinstance(context, dict) or context != review["evidence"]
            or context.get("needs") != {key: p.get("needs", {}).get(key)
                                        for key in ("concern", "budget", "fragranceFree")}
            or p.get("reviewConsent") != {"revision": record["revision"], "consent": True}
            or medical_scope(p, context.get("issue", ""))):
        raise DomainError("The consented BA review scope changed. Fresh review is required.",
                          409, "STALE_SCOPE")


def receive_review(record, review):
    """Deliver a committed decision; no model, product release or commerce call."""
    check_review_scope(record, review)
    p = record["payload"]
    p.update(decisionId=review["decision_id"], decision=review["decision"],
             reviewReason=review["reason"], needsReady=False)
    if review["decision"] == "APPROVE":
        record["status"] = "CLARIFYING"
        p.update(needsReady=True, proposedNeeds={"concern": p["needs"]["concern"],
                 "budget": p["needs"]["budget"]/100, "fragranceFree": p["needs"]["fragranceFree"],
                 "sources": {}}, message="Founder review permits fresh assessment only. "
                 "Confirm the needs again; catalogue, stock and model output will be checked anew.")
    elif review["decision"] == "REQUEST_REVISION":
        record["status"] = "CLARIFYING"
        p.update(message="The Founder requested corrected needs. Replace or clarify the request; "
                 "no advice or approval carries to the new revision.")
    else:
        record["status"] = "INCOMPLETE"
        p.update(message="The Founder rejected this review. No advice was approved. "
                 "You may explicitly correct the request or end the consultation.")


class BaReview:
    def __init__(self, store, intake, approval):
        self.store, self.intake, self.approval = store, intake, approval

    def request(self, actor, rid, data, authenticate=None):
        require_role(actor, "CUSTOMER")
        self.intake._input(data, ("contextRevision", "consent", "issue"))
        revision = revision_value(data["contextRevision"])
        if data["consent"] is not True:
            raise DomainError("Explicit Customer consent is required before sharing review context.",
                              400, "CONSENT_REQUIRED")
        issue = text_value(data["issue"], "Unresolved product question", 1000)
        try:
            with self.store.transaction() as db:
                current_customer(db, actor, authenticate)
                record = self.intake._owned(db, actor, rid, revision)
                p = record["payload"]
                if medical_scope(p, issue):
                    raise DomainError("Review cannot override the medical scope stop.", 409, "MEDICAL_SCOPE")
                if p.get("approvalId"):
                    review = self.approval.get(db, p["approvalId"])
                    check_review_scope(record, review)
                    if p["reviewContext"]["issue"] != issue:
                        raise DomainError("Correct the request as a new revision before changing review scope.",
                                          409, "STALE_SCOPE")
                    return record  # Same consent/scope returns the durable receipt, never resubmits.
                if (record["status"] != "INCOMPLETE" or not p.get("needsConfirmed")
                        or p.get("pendingOutcome") or p.get("result", {}).get("status") != "INCOMPLETE"):
                    raise DomainError("Review is offered only for an unresolved, recorded product assessment. "
                                      "Clarify missing needs or recover a saved draft first.", 409, "REVIEW_NOT_AVAILABLE")
                needs = p["needs"]
                code = p["result"].get("errorCode")
                if code not in {"LLM_UNAVAILABLE", "LLM_TIMEOUT", "LLM_INVALID_OUTPUT", "LLM_STALE_EVIDENCE",
                                "LLM_CAPABILITY_UNAVAILABLE", "LLM_HTTP_ERROR", "LLM_MODEL_MISMATCH"}:
                    code = "NO_VALIDATED_MATCH"
                context = {"needs": {key: needs[key] for key in ("concern", "budget", "fragranceFree")},
                           "issue": issue, "outcomeCode": code, "adviceSimulated": p["simulated"]}
                try:
                    rid_ap = self.approval.submit(db, "BA", rid, revision, review_action(record), context)
                    review = self.approval.get(db, rid_ap)
                except DomainError:
                    raise DomainError("Review service did not acknowledge this request. It is not submitted.",
                                      503, "BA_REVIEW_UNAVAILABLE") from None
                if (review["status"] != "PENDING" or review["origin_role"] != "BA" or review["origin_id"] != rid
                        or review["revision"] != revision or review["action"] != review_action(record)
                        or review["evidence"] != context or review["action_ref"] is not None):
                    raise DomainError("Review service did not acknowledge this exact request.", 503, "BA_REVIEW_UNAVAILABLE")
                p.update(approvalId=rid_ap, reviewContext=context,
                         reviewConsent={"revision": revision, "consent": True},
                         message="Review request acknowledged. No decision or successful advice is implied.")
                p.pop("reviewError", None)
                record["status"] = "REVIEW_PENDING"
                Store.save(db, record)
                Store.event(db, rid, "BA", "REVIEW_ACKNOWLEDGED", {"approvalId": rid_ap,
                            "contextRevision": revision, "consent": True, "adviceCompleted": False})
                return record
        except (sqlite3.Error, OSError):
            raise DomainError("Review could not be recorded or acknowledged. It is not submitted; "
                              "refresh before retrying. No completion is claimed.", 503, "BA_REVIEW_UNAVAILABLE") from None
