"""BA-M-01: read-only commerce advice, independently checked against evidence."""
import json
import math

from ..contracts import DomainError, text_value
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


class BeautyAdvisor:
    def __init__(self, llm):
        self.llm = llm

    def recommend(self, db, needs):
        if any(word in needs["message"].lower() for word in ("diagnose", "diagnosis", "treat eczema", "诊断", "治疗")):
            return {"status": "INCOMPLETE", "message": "This consultation cannot provide medical diagnosis or treatment.", "simulated": True}
        required_fact = "Moisturises dry skin" if needs["concern"] == "HYDRATION" else "Cleanses the skin"
        candidates = [p for p in catalogue(db) if p["availability"] == "AVAILABLE"
                      and p["price"] <= needs["budget"] and required_fact in p["facts"]
                      and (not needs["fragranceFree"] or p["fragrance_free"])]
        proposal = self.llm.propose(needs, candidates)
        if not isinstance(proposal, dict):
            return {"status": "INCOMPLETE", "message": "The model returned malformed output; the proposal was withheld.", "simulated": True}
        selected = next((p for p in candidates if p["id"] == proposal.get("productId")), None)
        if not selected:
            return {"status": "INCOMPLETE", "message": "No reliable available match can be offered for these constraints.", "simulated": True}
        claims = proposal.get("factRefs")
        if not isinstance(claims, list) or not claims or any(c not in selected["facts"] for c in claims):
            return {"status": "INCOMPLETE", "message": "The proposed claims could not be verified; the output was withheld.", "simulated": True}
        return {"status": "COMPLETED", "product": selected, "reasons": claims,
                "evidence": {"catalogueRef": f"catalogue:{selected['id']}:v{selected['version']}",
                             "inventoryObservation": now(), "availability": selected["availability"],
                             "constraints": {k: v for k, v in needs.items() if k != "message"}},
                "message": "Matched against the explicit need, budget and fragrance constraint. Selection does not authorise a purchase.",
                "simulated": True}

    def submit(self, db, actor, data):
        # A missing decision-relevant field is an explicit clarification, not an inferred default.
        try:
            needs = validated_needs(data)
        except DomainError as error:
            return self._record(db, actor, "CLARIFYING", {"message": str(error), "simulated": True})
        result = self.recommend(db, needs)
        return self._record(db, actor, result["status"], {"needs": needs, "result": result, "simulated": True})

    @staticmethod
    def _record(db, actor, status, payload):
        rid = Store.create(db, "BA", actor.id, status, payload, "BA")
        Store.event(db, rid, "BA", "CONSULTATION_RECORDED", {"status": status, "simulated": True})
        return Store.get(db, rid)
