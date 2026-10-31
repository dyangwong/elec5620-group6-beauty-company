"""Server-owned, bounded AP action registry. No model/caller risk classification."""
import re

from ..contracts import DomainError
from ..store import Store
from .cs_evidence import ExchangeEvidence, read_order, require_policy, require_same_policy


def classify(role, origin_id, revision, action, evidence, action_ref):
    """Return a registered review class, or fail closed before creating a receipt.

    Every registered class requires Founder review. Unknown actions/extra routing
    fields (including caller-supplied risk) cannot select a lower-authority path.
    """
    valid = (type(revision) is int and revision > 0 and isinstance(origin_id, str)
             and bool(origin_id.strip()) and isinstance(action, dict)
             and isinstance(evidence, dict) and bool(evidence))
    risk_class = None
    if valid and role == "BA":
        needs = evidence.get("needs")
        valid = (action == {"type": "REASSESS_ADVICE", "consultationId": origin_id,
                            "contextRevision": revision} and type(action.get("contextRevision")) is int
                 and action_ref is None
                 and set(evidence) == {"needs", "issue", "outcomeCode", "adviceSimulated"}
                 and isinstance(needs, dict) and set(needs) == {"concern", "budget", "fragranceFree"}
                 and needs.get("concern") in ("HYDRATION", "CLEANSING")
                 and type(needs.get("budget")) is int and 0 < needs["budget"] <= 1000000
                 and type(needs.get("fragranceFree")) is bool
                 and isinstance(evidence.get("issue"), str) and 0 < len(evidence["issue"].strip()) <= 1000
                 and type(evidence.get("adviceSimulated")) is bool
                 and evidence.get("outcomeCode") in ("NO_VALIDATED_MATCH", "LLM_UNAVAILABLE", "LLM_TIMEOUT",
                     "LLM_INVALID_OUTPUT", "LLM_STALE_EVIDENCE", "LLM_CAPABILITY_UNAVAILABLE",
                     "LLM_HTTP_ERROR", "LLM_MODEL_MISMATCH"))
        risk_class = "CONSENTED_REASSESSMENT"
    elif valid and role == "CS":
        valid = (set(action) == {"kind", "orderId", "productId"}
                 and action.get("kind") == "SIMULATED_EXCHANGE"
                 and all(isinstance(action.get(key), str) and action[key].strip()
                         for key in ("orderId", "productId"))
                 and isinstance(action_ref, str) and bool(action_ref.strip())
                 and set(evidence) == {"policyRef", "productEvidence"})
        risk_class = "DISPUTED_EXCHANGE"
    elif valid and role == "MC":
        base = {"kind", "draftId", "draftRevision"}
        kind = action.get("kind")
        live = kind == "REVIEW_TEXT_DRAFT"
        video = action.get("mediaKind") == "TEMPLATE_VIDEO"
        keys = base | ({"textMode", "mediaKind"} if live or video else set())
        if video:
            keys |= {"mediaSha256", "scriptSha256"}
        valid = (kind in ("REVIEW_MOCK_DRAFT", "REVIEW_TEXT_DRAFT")
                 and set(action) == keys and action.get("draftId") == origin_id
                 and type(action.get("draftRevision")) is int
                 and action["draftRevision"] == revision and action_ref is None
                 and set(evidence) == {"catalogueRef", "facts"}
                 and isinstance(evidence.get("catalogueRef"), str) and bool(evidence["catalogueRef"].strip())
                 and isinstance(evidence.get("facts"), list) and bool(evidence["facts"])
                 and all(isinstance(fact, str) and fact.strip() for fact in evidence["facts"]))
        if live or video:
            valid = (valid and action.get("textMode") == ("LIVE" if live else "MOCK")
                     and action.get("mediaKind") == ("TEMPLATE_VIDEO" if video else "MOCK_STORYBOARD"))
        if video:
            valid = valid and all(isinstance(action.get(key), str)
                                  and re.fullmatch(r"[0-9a-f]{64}", action[key])
                                  for key in ("mediaSha256", "scriptSha256"))
        risk_class = "CONTENT_REVIEW"
    else:
        valid = False
    if not valid:
        raise DomainError("Action or review policy is not registered. Correct the request; no authority was granted.",
                          409, "AP_ACTION_UNSUPPORTED")
    return risk_class


def validate(db, role, origin_id, revision, action, evidence, action_ref):
    risk_class = classify(role, origin_id, revision, action, evidence, action_ref)
    origin = Store.get(db, origin_id, role)
    if origin["revision"] != revision:
        raise DomainError("The registered action revision changed.", 409, "STALE_SCOPE")
    if role == "CS":
        payload = origin["payload"]
        advice = payload.get("advice", {})
        if (action != {"kind": "SIMULATED_EXCHANGE", "orderId": payload.get("orderId"),
                       "productId": advice.get("product", {}).get("id")}
                or action_ref != payload.get("actionRef")
                or evidence != {"policyRef": payload.get("policy", {}).get("id"),
                                "productEvidence": advice.get("evidence")}):
            raise DomainError("The exchange action/evidence scope changed.", 409, "STALE_SCOPE")
        # The order source, not a client risk label, determines the current policy.
        order = read_order(ExchangeEvidence(), db, origin["owner_id"], action["orderId"])
        policy = require_policy(ExchangeEvidence.policy(order))
        require_same_policy(policy, payload["policy"])
    return risk_class


def validate_review(db, review):
    return validate(db, review["origin_role"], review["origin_id"], review["revision"],
                    review["action"], review["evidence"], review["action_ref"])
