"""CO-M-01: bounded read-only CS-to-BA handoff with retained, correlated failures."""
from copy import deepcopy
from datetime import datetime
import sqlite3

from ..contracts import DomainError
from ..store import Store, new_id, now
from .beauty_advisor import catalogue


FIELDS = {"message", "concern", "budget", "fragranceFree"}
FAILURES = {
    "CO_INVALID_CONTEXT": ("The advice handoff needs complete, valid product needs. Correct the request before a new handoff.", "CORRECT_CONTEXT"),
    "CO_TARGET_UNAVAILABLE": ("The advice service is unavailable. The Founder must review the failed handoff; no exchange was executed.", "FOUNDER_INTERVENTION"),
    "CO_TARGET_TIMEOUT": ("The read-only advice request timed out. No advice or exchange completion is claimed. The Founder must review the failure.", "FOUNDER_INTERVENTION"),
    "CO_TARGET_FAILED": ("The advice service failed. No supported advice was saved; the Founder must review the failure.", "FOUNDER_INTERVENTION"),
    "CO_INVALID_RESULT": ("The advice result could not be independently verified. Correct the request or seek Founder intervention.", "CORRECT_OR_ESCALATE"),
    "CO_ADVICE_INCOMPLETE": ("No supported advice is available for these needs. Correct the request or seek Founder intervention.", "CORRECT_OR_ESCALATE"),
}


class Coordination:
    @staticmethod
    def create(db, customer_id, cs_id):
        return Store.create(db, "CO", customer_id, "PENDING_VALIDATION",
                            {"originId": cs_id, "handoffs": [], "simulated": True}, "CO")

    @staticmethod
    def state(db, rid, status, event, detail):
        record = Store.get(db, rid, "CO")
        record["status"] = status
        Store.save(db, record)
        Store.event(db, rid, "CO", event, detail)

    @staticmethod
    def _context(needs):
        if (not isinstance(needs, dict) or not FIELDS <= set(needs)
                or not isinstance(needs["message"], str) or not needs["message"].strip()
                or len(needs["message"]) > 2000 or needs["concern"] not in ("HYDRATION", "CLEANSING")
                or type(needs["budget"]) is not int or not 0 < needs["budget"] <= 1000000
                or type(needs["fragranceFree"]) is not bool):
            return None
        # Budget is already canonical integer AUD cents from CS, never convert it twice.
        return {key: deepcopy(needs[key]) for key in FIELDS}

    @staticmethod
    def _verified_success(db, result, context, simulated):
        if (not isinstance(result, dict) or set(result) != {"status", "product", "reasons", "evidence", "message", "simulated"}
                or result["status"] != "COMPLETED" or result["simulated"] is not simulated
                or not isinstance(result["product"], dict) or not isinstance(result["evidence"], dict)
                or any(type(result["product"].get(key)) is not int for key in ("price", "version", "stock"))
                or type(result["product"].get("fragrance_free")) is not bool
                or not isinstance(result["message"], str) or not result["message"].strip() or len(result["message"]) > 2000):
            return False
        product = next((p for p in catalogue(db) if p["id"] == result["product"].get("id")), None)
        fact = "Moisturises dry skin" if context["concern"] == "HYDRATION" else "Cleanses the skin"
        if (not product or product != result["product"] or product["availability"] != "AVAILABLE"
                or product["price"] > context["budget"] or fact not in product["facts"]
                or (context["fragranceFree"] and not product["fragrance_free"])
                or not isinstance(result["reasons"], list) or not result["reasons"]
                or any(not isinstance(reason, str) or reason not in product["facts"] for reason in result["reasons"])):
            return False
        evidence = result["evidence"]
        if (set(evidence) != {"catalogueRef", "inventoryObservation", "availability", "constraints"}
                or evidence["catalogueRef"] != f"catalogue:{product['id']}:v{product['version']}"
                or evidence["availability"] != "AVAILABLE"
                or evidence["constraints"] != {k: v for k, v in context.items() if k != "message"}
                or not isinstance(evidence["inventoryObservation"], str)):
            return False
        try:
            return datetime.fromisoformat(evidence["inventoryObservation"]).tzinfo is not None
        except ValueError:
            return False

    @staticmethod
    def _failure(record, handoff, code, simulated, upstream=None):
        reason, recovery = FAILURES[code]
        result = {"status": "INCOMPLETE", "message": reason, "errorCode": code, "simulated": simulated}
        handoff.update(status="FAILED", result=result, failure={"code": code, "reason": reason,
                       "recovery": recovery, "businessExecution": False})
        if isinstance(upstream, str) and upstream in {"LLM_UNAVAILABLE", "LLM_TIMEOUT", "LLM_INVALID_OUTPUT", "LLM_CAPABILITY_UNAVAILABLE", "MEDICAL_SCOPE"}:
            handoff["failure"]["upstreamCode"] = upstream
        record["status"] = "CLARIFICATION_REQUIRED" if code == "CO_INVALID_CONTEXT" else "ESCALATED"
        return result

    @staticmethod
    def advice_handoff(db, rid, needs, advisor):
        """Caller owns/commits the transaction; failures are returned to be saved, never raised after a successful save."""
        try:
            return Coordination._advice_handoff(db, rid, needs, advisor)
        except sqlite3.Error:
            # Raising forces the existing CS/HTTP transaction to roll back. No durable trace is claimed.
            raise DomainError("The handoff could not be recorded. No saved result or completed handoff is claimed. "
                              "Refresh the request before any further action.", 503, "CO_STORAGE_UNAVAILABLE") from None

    @staticmethod
    def _advice_handoff(db, rid, needs, advisor):
        record = Store.get(db, rid, "CO")
        origin = Store.get(db, record["payload"]["originId"], "CS")
        if origin["owner_id"] != record["owner_id"] or origin["payload"].get("coordinationId") != rid:
            raise DomainError("The handoff origin no longer matches this work request.", 409, "STALE_SCOPE")
        revision = origin["revision"]
        context = Coordination._context(needs)
        current_context = Coordination._context(origin["payload"].get("needs"))
        if context is not None and current_context is not None and context != current_context:
            raise DomainError("The Customer needs changed. Use the current request revision.", 409, "STALE_SCOPE")
        # Same-origin/revision replay is read-only. A deliberate CS revision is required for new dispatch.
        for prior in reversed(record["payload"]["handoffs"]):
            if prior.get("originId") == origin["id"] and prior.get("contextRevision") == revision:
                if ((context is not None and current_context == context and prior["authorisedContext"] == context)
                        or (context is None and prior.get("failure", {}).get("code") == "CO_INVALID_CONTEXT")):
                    return deepcopy(prior["result"])
                raise DomainError("The supplied scope does not match the saved handoff. Revise the request explicitly.",
                                  409, "STALE_SCOPE")
        if origin["status"] != "ASSESSING":
            raise DomainError("This request is not awaiting a new handoff.", 409, "INVALID_STATE")
        try:
            simulated = getattr(advisor, "simulated", True)
            receiver = getattr(advisor, "recommend", None)
            mode_valid = type(simulated) is bool
        except Exception:
            simulated, receiver, mode_valid = True, None, False
        if not mode_valid:
            simulated = True  # Synthetic failure metadata only; this target will not be called.
        handoff = {"handoffId": new_id("HO"), "fromRole": "CS", "toRole": "BA", "originId": origin["id"],
                   "contextRevision": revision, "handoffTime": now(), "operation": "READ_ONLY_ADVICE",
                   "authorisedContext": context or {}, "status": "SENT", "dispatched": False}
        record["revision"] = revision
        record["payload"]["originRevision"] = revision
        record["payload"]["handoffs"].append(handoff)
        if context is None or current_context is None:
            result = Coordination._failure(record, handoff, "CO_INVALID_CONTEXT", simulated)
        elif not mode_valid or not callable(receiver):
            result = Coordination._failure(record, handoff, "CO_TARGET_UNAVAILABLE", simulated)
        else:
            record["status"] = "HANDOFF_SENT"
            Store.save(db, record)
            Store.event(db, rid, "CO", "HANDOFF_SENT", {**deepcopy(handoff), "dispatched": True})
            handoff["dispatched"] = True
            try:
                # A receiver cannot mutate the scope against which its result will be checked.
                result = deepcopy(receiver(db, deepcopy(context)))
                if isinstance(result, dict) and result.get("status") == "COMPLETED":
                    valid = Coordination._verified_success(db, result, context, simulated)
                    if valid:
                        # Product/facts/evidence are checked; arbitrary receiver prose grants no authority.
                        result["message"] = "Supported read-only advice was checked. Customer confirmation and any required review still apply."
                        handoff.update(status="COMPLETED", result=result)
                        record["status"] = "PENDING_VALIDATION"
                    else:
                        result = Coordination._failure(record, handoff, "CO_INVALID_RESULT", simulated)
                elif (isinstance(result, dict) and result.get("status") == "INCOMPLETE"
                      and set(result) <= {"status", "message", "simulated", "errorCode"}
                      and result.get("simulated") is simulated and isinstance(result.get("message"), str)
                      and bool(result["message"].strip()) and len(result["message"]) <= 2000):
                    result = Coordination._failure(record, handoff, "CO_ADVICE_INCOMPLETE", simulated, result.get("errorCode"))
                else:
                    result = Coordination._failure(record, handoff, "CO_INVALID_RESULT", simulated)
            except Exception as error:
                # This boundary is only read-only BA advice, not an unknown commerce-effect retry.
                code = ("CO_TARGET_TIMEOUT" if isinstance(error, TimeoutError) else
                        "CO_TARGET_UNAVAILABLE" if isinstance(error, (ConnectionError, sqlite3.Error)) else "CO_TARGET_FAILED")
                result = Coordination._failure(record, handoff, code, simulated,
                                               error.code if isinstance(error, DomainError) else None)
        Store.save(db, record)
        Store.event(db, rid, "CO", "HANDOFF_FAILED" if handoff["status"] == "FAILED" else "ADVICE_RESULT_RECORDED",
                    {"handoffId": handoff["handoffId"], "originId": origin["id"], "contextRevision": revision,
                     "status": handoff["status"], "businessExecution": False,
                     **({"failure": deepcopy(handoff["failure"])} if handoff.get("failure") else {})})
        return deepcopy(result)
