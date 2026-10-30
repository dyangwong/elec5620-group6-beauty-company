"""BA-M-01: read-only commerce advice, independently checked against evidence."""
import json
import math
from copy import deepcopy

from ..contracts import DomainError, require_role, revision_value, text_value
from ..adapters.llm import ModelError
from ..store import Store, now


def catalogue(db):
    result = []
    for row in db.execute("SELECT * FROM products ORDER BY id"):
        item = dict(row)
        item["facts"] = json.loads(item["facts"])
        item["fragrance_free"] = bool(item["fragrance_free"])
        item["availability"] = "UNKNOWN" if item["stock"] is None else ("AVAILABLE" if item["stock"] > 0 else "UNAVAILABLE")
        result.append(item)
    return result


def validated_needs(data):
    message = text_value(data.get("message"), "Consultation request")
    if not isinstance(data.get("concern"), str) or data["concern"] not in {"HYDRATION", "CLEANSING"}:
        raise DomainError("Choose an explicit product need: hydration or cleansing.")
    budget = data.get("budget")
    if type(budget) not in (int, float) or not math.isfinite(budget) or budget <= 0 or budget > 10000:
        raise DomainError("Supply a positive budget up to AUD 10,000.")
    if type(data.get("fragranceFree")) is not bool:
        raise DomainError("Explicitly state whether fragrance-free is required.")
    return {"message": message, "concern": data["concern"], "budget": round(budget * 100),
            "fragranceFree": data["fragranceFree"]}


def retain_revision(record):
    """Invalidate current advice while retaining the prior owned context."""
    payload = record["payload"]
    prior = {"revision": record["revision"], "status": record["status"]}
    for key in ("messages", "proposedNeeds", "needs", "needsConfirmed", "result", "errorCode", "simulated",
                "approvalId", "decisionId", "decision", "reviewContext", "reviewConsent", "reviewReason",
                "structuredInput"):
        if key in payload:
            prior[key] = deepcopy(payload[key])
    payload.setdefault("history", []).append(prior)
    for key in ("result", "proposedNeeds", "questions", "needsReady", "needs", "needsConfirmed", "errorCode", "message",
                "pendingOutcome", "recordedRevision", "approvalId", "reviewContext", "reviewConsent",
                "decisionId", "decision", "reviewReason", "reviewError"):
        payload.pop(key, None)
    record["revision"] += 1
    record["status"] = "ACTIVE"


def checked_advice(db, needs, value, simulated):
    """Revalidate saved advice using current evidence, without another model call."""
    value = deepcopy(value)
    value["simulated"] = simulated
    if value.get("status") not in {"COMPLETED", "INCOMPLETE"}:
        raise DomainError("The saved advice has no confirmed scope.", 409, "INVALID_SAVED_RESULT")
    if value["status"] != "COMPLETED":
        return value
    supplied = value.get("product")
    if not isinstance(supplied, dict) or not isinstance(value.get("evidence"), dict):
        raise DomainError("The saved advice evidence is invalid.", 409, "INVALID_SAVED_RESULT")
    product = next((item for item in catalogue(db) if item["id"] == supplied.get("id")), None)
    fact = "Moisturises dry skin" if needs["concern"] == "HYDRATION" else "Cleanses the skin"
    if (not product or product != supplied or product["availability"] != "AVAILABLE"
            or product["price"] > needs["budget"] or fact not in product["facts"]
            or (needs["fragranceFree"] and not product["fragrance_free"])
            or not isinstance(value.get("reasons"), list) or not value["reasons"]
            or any(reason not in product["facts"] for reason in value["reasons"])
            or value["evidence"].get("catalogueRef") != f"catalogue:{product['id']}:v{product['version']}"
            or value["evidence"].get("constraints") != {key: needs[key] for key in ("concern", "budget", "fragranceFree")}):
        return {"status": "INCOMPLETE", "errorCode": "LLM_STALE_EVIDENCE",
                "message": "Catalogue or stock changed. Retry with fresh evidence.", "simulated": simulated}
    value["evidence"].update(inventoryObservation=now(), availability=product["availability"])
    return value


class BeautyAdvisor:
    def __init__(self, llm):
        self.llm = llm

    @property
    def simulated(self):
        return getattr(self.llm, "ba_simulated", getattr(self.llm, "simulated", True))

    def recommend(self, db, needs):
        return self.recommend_from_catalogue(needs, catalogue(db))

    def recommend_from_catalogue(self, needs, products):
        """Read-only snapshot input: no DB handle is needed during inference."""
        if any(word in needs["message"].lower() for word in ("diagnose", "diagnosis", "treat eczema", "诊断", "治疗")):
            return {"status": "INCOMPLETE", "message": "This consultation cannot provide medical diagnosis or treatment.", "simulated": self.simulated}
        required_fact = "Moisturises dry skin" if needs["concern"] == "HYDRATION" else "Cleanses the skin"
        candidates = [p for p in products if p["availability"] == "AVAILABLE"
                      and p["price"] <= needs["budget"] and required_fact in p["facts"]
                      and (not needs["fragranceFree"] or p["fragrance_free"])]
        try:
            proposal = self.llm.propose(needs, candidates)
        except ModelError as error:
            return {"status": "INCOMPLETE", "message": str(error), "errorCode": error.code,
                    "simulated": self.simulated}
        if not isinstance(proposal, dict):
            return {"status": "INCOMPLETE", "message": "The model returned malformed output; the proposal was withheld.", "simulated": self.simulated}
        selected = next((p for p in candidates if p["id"] == proposal.get("productId")), None)
        if not selected:
            return {"status": "INCOMPLETE", "message": "No reliable available match can be offered for these constraints.", "simulated": self.simulated}
        claims = proposal.get("factRefs")
        if not isinstance(claims, list) or not claims or any(c not in selected["facts"] for c in claims):
            return {"status": "INCOMPLETE", "message": "The proposed claims could not be verified; the output was withheld.", "simulated": self.simulated}
        return {"status": "COMPLETED", "product": selected, "reasons": claims,
                "evidence": {"catalogueRef": f"catalogue:{selected['id']}:v{selected['version']}",
                             "inventoryObservation": now(), "availability": selected["availability"],
                             "constraints": {k: v for k, v in needs.items() if k != "message"}},
                "message": "Matched against the explicit need, budget and fragrance constraint. Selection does not authorise a purchase.",
                "simulated": self.simulated}

    @staticmethod
    def owned_structured(db, actor, rid, revision):
        require_role(actor, "CUSTOMER")
        record = Store.get(db, rid, "BA")
        if record["owner_id"] != actor.id or record["payload"].get("naturalNeeds"):
            raise DomainError("Consultation not found.", 404, "NOT_FOUND")
        if record["revision"] != revision:
            raise DomainError("The consultation changed. Refresh before continuing.", 409, "STALE_SCOPE")
        return record

    def begin_structured(self, db, actor, data, rid=None, replace=False):
        require_role(actor, "CUSTOMER")
        fields = {"message", "concern", "budget", "fragranceFree"}
        if (not isinstance(data, dict) or set(data) - fields - ({"contextRevision"} if rid else set())):
            raise DomainError("Supply only the structured consultation fields.")
        supplied = {key: deepcopy(value) for key, value in data.items() if key in fields}
        if rid:
            record = self.owned_structured(db, actor, rid, revision_value(data.get("contextRevision")))
            if record["status"] == "CANCELLED":
                raise DomainError("A cancelled consultation requires a new consultation.", 409, "INVALID_STATE")
            if record["status"] not in {"ACTIVE", "CLARIFYING", "INCOMPLETE", "COMPLETED"}:
                raise DomainError("This consultation cannot be continued.", 409, "INVALID_STATE")
            if not replace and record["status"] not in {"CLARIFYING", "INCOMPLETE"}:
                raise DomainError("Use an explicit revision to replace current advice.", 409, "INVALID_STATE")
            previous = record["payload"].get("structuredInput")
            # Earlier structured records predate the input marker; budgets were stored in cents.
            if previous is None:
                previous = deepcopy(record["payload"].get("needs", {}))
                if "budget" in previous:
                    previous["budget"] /= 100
            supplied = supplied if replace else {**previous, **supplied}
            retain_revision(record)
            record["payload"].update(structuredNeeds=True, structuredInput=supplied, simulated=self.simulated)
        else:
            record = self._record(db, actor, "ACTIVE", {"structuredNeeds": True,
                "structuredInput": supplied, "history": [], "simulated": self.simulated})
        try:
            needs = validated_needs(supplied)
        except DomainError as error:
            record["status"] = "CLARIFYING"
            record["payload"].update(message=str(error), needsConfirmed=False)
        else:
            record["payload"].update(needs=needs, needsConfirmed=True)
        Store.save(db, record)
        Store.event(db, record["id"], "BA", "STRUCTURED_NEEDS_RECORDED", {"revision": record["revision"], "status": record["status"]})
        return record

    def submit(self, db, actor, data, rid=None, replace=False):
        """Caller-owned transaction compatibility; Company.consult stages durable recovery."""
        record = self.begin_structured(db, actor, data, rid, replace)
        if record["status"] != "ACTIVE":
            return record
        result = self.recommend(db, deepcopy(record["payload"]["needs"]))
        current = self.owned_structured(db, actor, record["id"], record["revision"])
        if current["status"] != "ACTIVE" or current["payload"] != record["payload"]:
            raise DomainError("The advice scope changed. Old output was discarded.", 409, "STALE_SCOPE")
        result = checked_advice(db, record["payload"]["needs"], result, record["payload"]["simulated"])
        current["status"] = result["status"]
        current["payload"].update(result=result, simulated=result["simulated"], recordedRevision=current["revision"])
        Store.save(db, current)
        Store.event(db, current["id"], "BA", "CONFIRMED_ADVICE_RECORDED", {"revision": current["revision"], "status": current["status"]})
        return current

    def resume(self, db, actor, rid, data):
        return self.submit(db, actor, data, rid)

    def revise(self, db, actor, rid, data):
        return self.submit(db, actor, data, rid, replace=True)

    def cancel(self, db, actor, rid, data):
        if not isinstance(data, dict) or set(data) != {"contextRevision"}:
            raise DomainError("Cancellation accepts only contextRevision.")
        record = self.owned_structured(db, actor, rid, revision_value(data["contextRevision"]))
        if record["status"] == "CANCELLED":
            return record
        if record["status"] not in {"ACTIVE", "CLARIFYING", "INCOMPLETE"}:
            raise DomainError("Completed advice may be revised, not cancelled retroactively.", 409, "INVALID_STATE")
        retain_revision(record)
        record["status"] = "CANCELLED"
        record["payload"].update(needsConfirmed=False, message="Consultation cancelled. Start a new consultation to continue.")
        Store.save(db, record)
        Store.event(db, rid, "BA", "CONSULTATION_CANCELLED", {"revision": record["revision"]})
        return Store.get(db, rid, "BA")

    @staticmethod
    def _record(db, actor, status, payload):
        rid = Store.create(db, "BA", actor.id, status, payload, "BA")
        Store.event(db, rid, "BA", "CONSULTATION_RECORDED", {"status": status, "simulated": payload["simulated"]})
        return Store.get(db, rid)
