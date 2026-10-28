"""Standalone BA needs conversation; extract -> clarify -> Customer confirm -> advise."""
from ..adapters.llm import ModelError
from ..adapters.needs import FIELDS, validate_extraction
from ..contracts import DomainError, require_role, revision_value, text_value
from ..store import Store
from .beauty_advisor import catalogue, validated_needs

QUESTIONS = {
    "concern": "Are you looking for hydration for dry skin, or a cleanser?",
    "budget": "What is your maximum budget in AUD?",
    "fragranceFree": "Is fragrance-free required, or is fragrance acceptable?",
}


class BaIntake:
    def __init__(self, store, advisor):
        self.store, self.advisor = store, advisor

    @staticmethod
    def _input(data, expected):
        if not isinstance(data, dict) or set(data) != set(expected):
            raise DomainError("Supply only the displayed consultation fields.")

    def _owned(self, db, actor, rid, revision):
        record = Store.get(db, rid, "BA")
        if record["owner_id"] != actor.id or not record["payload"].get("naturalNeeds"):
            raise DomainError("Consultation not found.", 404, "NOT_FOUND")
        if record["revision"] != revision:
            raise DomainError("The consultation changed. Refresh its current questions.", 409, "STALE_SCOPE")
        return record

    @staticmethod
    def _history(record):
        payload = record["payload"]
        payload.setdefault("history", []).append({"revision": record["revision"], "status": record["status"],
            "proposedNeeds": payload.get("proposedNeeds"), "errorCode": payload.get("errorCode")})
        for key in ("result", "proposedNeeds", "questions", "needsReady", "needs", "needsConfirmed", "errorCode", "message"):
            payload.pop(key, None)
        record["revision"] += 1
        record["status"] = "ACTIVE"

    def start(self, actor, data):
        require_role(actor, "CUSTOMER")
        self._input(data, ("message",))
        message = text_value(data["message"], "Your needs")
        with self.store.transaction() as db:
            record = self.advisor._record(db, actor, "ACTIVE", {
                "naturalNeeds": True, "messages": [message], "simulated": self.advisor.simulated,
                "history": [], "needsReady": False})
        return self._extract(record)

    def clarify(self, actor, rid, data):
        require_role(actor, "CUSTOMER")
        self._input(data, ("message", "contextRevision"))
        revision = revision_value(data["contextRevision"])
        message = text_value(data["message"], "Your clarification")
        with self.store.transaction() as db:
            record = self._owned(db, actor, rid, revision)
            if record["status"] not in {"ACTIVE", "CLARIFYING", "INCOMPLETE"}:
                raise DomainError("Start a new consultation for a completed request.", 409, "INVALID_STATE")
            messages = record["payload"]["messages"]
            if len(messages) >= 8 or sum(map(len, messages)) + len(message) > 8000:
                raise DomainError("This bounded consultation is full. Start a new consultation.", 409, "CONVERSATION_LIMIT")
            self._history(record)
            messages.append(message)
            record["payload"]["needsReady"] = False
            Store.save(db, record)
        return self._extract(record)

    def _extract(self, record):
        messages = tuple(record["payload"]["messages"])
        result, error = None, None
        if any(word in text.lower() for text in messages
               for word in ("diagnose", "diagnosis", "treat eczema", "诊断", "治疗")):
            error = ModelError("This consultation cannot provide medical diagnosis or treatment.", 400, "MEDICAL_SCOPE")
        else:
            try:
                extract = getattr(self.advisor.llm, "extract_needs", None)
                if not callable(extract):
                    raise ModelError("Needs interpretation is not connected. No recommendation was made.",
                                     503, "LLM_CAPABILITY_UNAVAILABLE")
                result = validate_extraction(extract(list(messages)), messages)
            except ModelError as caught:
                error = caught
            except (ValueError, TypeError, KeyError):
                error = ModelError("The extracted needs could not be verified. No recommendation was made.",
                                   502, "LLM_INVALID_OUTPUT")
        # Inference has finished: re-read the saved revision before applying it.
        with self.store.transaction() as db:
            current = Store.get(db, record["id"], "BA")
            if current["revision"] != record["revision"] or current["status"] != "ACTIVE":
                raise DomainError("A newer consultation revision exists. Old interpretation was discarded.", 409, "STALE_SCOPE")
            payload = current["payload"]
            if error:
                current["status"] = "INCOMPLETE"
                payload.update(errorCode=error.code, message=str(error), needsReady=False)
            else:
                missing = [key for key in FIELDS if result[key] is None]
                current["status"] = "CLARIFYING"
                payload.update(proposedNeeds=result, needsReady=not missing,
                               questions=[QUESTIONS[key] for key in missing],
                               message="Please answer the missing needs." if missing else
                               "Review and explicitly confirm these interpreted needs before advice.")
            Store.save(db, current)
            Store.event(db, current["id"], "BA", "NEEDS_INTERPRETATION_RECORDED",
                        {"status": current["status"], "revision": current["revision"],
                         "simulated": payload["simulated"], "needsReady": payload["needsReady"]})
            return current

    def confirm(self, actor, rid, data):
        require_role(actor, "CUSTOMER")
        self._input(data, ("contextRevision", *FIELDS))
        revision = revision_value(data["contextRevision"])
        with self.store.transaction() as db:
            record = self._owned(db, actor, rid, revision)
            if record["status"] != "CLARIFYING" or not record["payload"].get("needsReady"):
                raise DomainError("Answer the missing questions before confirming needs.", 409, "NEEDS_NOT_READY")
            # These are explicit Customer-reviewed fields, not trusted model authority.
            needs = validated_needs({"message": record["payload"]["messages"][0],
                                     **{key: data[key] for key in FIELDS}})
            self._history(record)
            record["payload"].update(needs=needs, needsConfirmed=True, needsReady=False)
            Store.save(db, record)
            Store.event(db, rid, "BA", "CUSTOMER_NEEDS_CONFIRMED", {"revision": record["revision"]})
        with self.store.read() as db:
            result = self.advisor.recommend(db, needs)
        with self.store.transaction() as db:
            current = self._owned(db, actor, rid, record["revision"])
            if current["status"] != "ACTIVE":
                raise DomainError("This result is no longer applicable.", 409, "STALE_SCOPE")
            if result["status"] == "COMPLETED":
                product = next((p for p in catalogue(db) if p["id"] == result["product"]["id"]), None)
                if product != result["product"]:
                    result = {"status": "INCOMPLETE", "errorCode": "LLM_STALE_EVIDENCE",
                              "message": "Catalogue or stock changed. Start a fresh consultation.",
                              "simulated": self.advisor.simulated}
            current["status"] = result["status"]
            current["payload"].update(result=result, simulated=result["simulated"])
            Store.save(db, current)
            Store.event(db, rid, "BA", "CONFIRMED_ADVICE_RECORDED", {"status": current["status"],
                        "revision": current["revision"], "simulated": result["simulated"]})
            return current
