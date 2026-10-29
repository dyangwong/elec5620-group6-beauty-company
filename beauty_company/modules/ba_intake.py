"""Owned standalone BA conversation, revision/cancellation and storage-only recovery."""
from copy import deepcopy
import sqlite3

from ..adapters.llm import ModelError
from ..adapters.needs import FIELDS, validate_extraction
from ..contracts import DomainError, require_role, revision_value, text_value
from ..store import Store, now
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
        prior = {"revision": record["revision"], "status": record["status"]}
        for key in ("messages", "proposedNeeds", "needs", "needsConfirmed", "result", "errorCode", "simulated", "approvalId", "decisionId", "decision",
                    "reviewContext", "reviewConsent", "reviewReason"):
            if key in payload:
                prior[key] = deepcopy(payload[key])
        payload.setdefault("history", []).append(prior)
        for key in ("result", "proposedNeeds", "questions", "needsReady", "needs", "needsConfirmed", "errorCode", "message",
                    "pendingOutcome", "recordedRevision", "approvalId", "reviewContext", "reviewConsent",
                    "decisionId", "decision", "reviewReason", "reviewError"):
            payload.pop(key, None)
        record["revision"] += 1
        record["status"] = "ACTIVE"

    @staticmethod
    def _invalidate_review(db, record):
        from .approval import Approval
        Approval.supersede(db, record["payload"].get("approvalId"))

    def _begin(self, record, db):
        self._invalidate_review(db, record)
        self._history(record)
        record["payload"].update(needsReady=False, simulated=self.advisor.simulated)

    @staticmethod
    def public_record(record):
        """Uncommitted advice drafts are persistence data, never snapshot output."""
        record = deepcopy(record)
        pending = record["payload"].get("pendingOutcome")
        if pending:
            record["payload"]["pendingOutcome"] = ({key: pending[key]
                for key in ("kind", "revision", "simulated") if key in pending}
                if isinstance(pending, dict) else {"invalid": True})
        return record

    @staticmethod
    def _storage_error():
        return DomainError("The result could not be recorded. No completion is claimed. "
                           "Refresh; recover a saved draft if offered, otherwise retry the attempt.",
                           503, "BA_STORAGE_UNAVAILABLE")

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
            self._begin(record, db)
            messages.append(message)
            Store.save(db, record)
        return self._extract(record)

    def revise(self, actor, rid, data):
        require_role(actor, "CUSTOMER")
        self._input(data, ("message", "contextRevision"))
        revision = revision_value(data["contextRevision"])
        message = text_value(data["message"], "Your replacement request")
        with self.store.transaction() as db:
            record = self._owned(db, actor, rid, revision)
            if record["status"] not in {"ACTIVE", "CLARIFYING", "INCOMPLETE", "COMPLETED", "REVIEW_PENDING"}:
                raise DomainError("A cancelled consultation requires a new consultation.", 409, "INVALID_STATE")
            self._begin(record, db)
            # A replacement is a new scope, not an implicit inheritance of old constraints.
            record["payload"]["messages"] = [message]
            Store.save(db, record)
            Store.event(db, rid, "BA", "CONSULTATION_REVISED", {"revision": record["revision"]})
        return self._extract(record)

    def cancel(self, actor, rid, data):
        require_role(actor, "CUSTOMER")
        self._input(data, ("contextRevision",))
        revision = revision_value(data["contextRevision"])
        try:
            with self.store.transaction() as db:
                record = self._owned(db, actor, rid, revision)
                if record["status"] == "CANCELLED":
                    return record
                if record["status"] not in {"ACTIVE", "CLARIFYING", "INCOMPLETE", "REVIEW_PENDING"}:
                    raise DomainError("Completed advice may be revised; it cannot be cancelled retroactively.",
                                      409, "INVALID_STATE")
                self._invalidate_review(db, record)
                self._history(record)
                record["status"] = "CANCELLED"
                record["payload"].update(needsReady=False, message="Consultation cancelled. Late results are suppressed. "
                                       "Start a new consultation to continue.")
                Store.save(db, record)
                Store.event(db, rid, "BA", "CONSULTATION_CANCELLED", {"revision": record["revision"]})
                return record
        except sqlite3.Error:
            raise DomainError("Cancellation could not be recorded. It is not confirmed; refresh before retrying.",
                              503, "BA_CANCELLATION_NOT_RECORDED") from None

    def retry(self, actor, rid, data):
        require_role(actor, "CUSTOMER")
        self._input(data, ("contextRevision",))
        revision = revision_value(data["contextRevision"])
        with self.store.transaction() as db:
            record = self._owned(db, actor, rid, revision)
            if record["status"] not in {"ACTIVE", "INCOMPLETE"}:
                raise DomainError("Only an interrupted or incomplete attempt can be retried.", 409, "INVALID_STATE")
            if record["payload"].get("pendingOutcome"):
                raise DomainError("A saved result is available. Recover it or explicitly revise the request.",
                                  409, "RECOVERY_AVAILABLE")
            self._begin(record, db)
            Store.save(db, record)
            Store.event(db, rid, "BA", "CONSULTATION_RETRY_REQUESTED", {"revision": record["revision"]})
        # Explicit new read-only inference, not storage recovery or an automatic retry.
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
        value = {"errorCode": error.code, "message": str(error)} if error else {"extracted": result}
        return self._stage(record, "NEEDS", value)

    def confirm(self, actor, rid, data, authenticate=None):
        require_role(actor, "CUSTOMER")
        self._input(data, ("contextRevision", *FIELDS))
        revision = revision_value(data["contextRevision"])
        from .ba_review import current_customer, check_review_scope
        with self.store.transaction() as db:
            current_customer(db, actor, authenticate)
            record = self._owned(db, actor, rid, revision)
            if record["payload"].get("approvalId"):
                from .approval import Approval
                review = Approval.get(db, record["payload"]["approvalId"])
                check_review_scope(record, review)
                if (review["decision"] != "APPROVE" or not review["decision_id"]
                        or review["delivery"] != "DELIVERED"
                        or record["payload"].get("decisionId") != review["decision_id"]):
                    raise DomainError("A current delivered decision permitting reassessment is required.",
                                      409, "REVIEW_NOT_APPROVED")
            if record["status"] != "CLARIFYING" or not record["payload"].get("needsReady"):
                raise DomainError("Answer the missing questions before confirming needs.", 409, "NEEDS_NOT_READY")
            # These are explicit Customer-reviewed fields, not trusted model authority.
            needs = validated_needs({"message": record["payload"]["messages"][0],
                                     **{key: data[key] for key in FIELDS}})
            self._begin(record, db)
            record["payload"].update(needs=needs, needsConfirmed=True, needsReady=False)
            Store.save(db, record)
            Store.event(db, rid, "BA", "CUSTOMER_NEEDS_CONFIRMED", {"revision": record["revision"]})
        with self.store.read() as db:
            products = catalogue(db)
        result = self.advisor.recommend_from_catalogue(needs, products)
        return self._stage(record, "ADVICE", result, actor, authenticate)

    def _stage(self, record, kind, value, actor=None, authenticate=None):
        """Persist a non-authoritative draft before attempting its final recording."""
        try:
            with self.store.transaction() as db:
                current = Store.get(db, record["id"], "BA")
                if actor:
                    from .ba_review import current_customer
                    current_customer(db, actor, authenticate)
                    if current["owner_id"] != actor.id or current["payload"] != record["payload"]:
                        raise DomainError("The current advice source changed. Old output was discarded.", 409, "STALE_SCOPE")
                if current["revision"] != record["revision"] or current["status"] != "ACTIVE":
                    raise DomainError("A newer or cancelled revision exists. Old output was discarded.", 409, "STALE_SCOPE")
                current["payload"]["pendingOutcome"] = {
                    "kind": kind, "revision": record["revision"], "value": value,
                    "simulated": record["payload"]["simulated"]}
                Store.save(db, current)
        except sqlite3.Error:
            # There may be no durable draft. Do not invent one or return the model output.
            raise self._storage_error() from None
        return self._finish(record["id"], record["revision"])

    def recover(self, actor, rid, data):
        require_role(actor, "CUSTOMER")
        self._input(data, ("contextRevision",))
        revision = revision_value(data["contextRevision"])
        with self.store.read() as db:
            self._owned(db, actor, rid, revision)
        # No model call, supplied result or change to Customer-confirmed scope.
        return self._finish(rid, revision, actor)

    def _finish(self, rid, revision, actor=None):
        try:
            with self.store.transaction() as db:
                current = self._owned(db, actor, rid, revision) if actor else Store.get(db, rid, "BA")
                if current["revision"] != revision or current["status"] == "CANCELLED":
                    raise DomainError("This output belongs to a stale or cancelled revision.", 409, "STALE_SCOPE")
                p = current["payload"]
                if p.get("recordedRevision") == revision and not p.get("pendingOutcome"):
                    return current  # Idempotent same-revision recovery; no repeat audit/inference.
                pending = p.get("pendingOutcome")
                if current["status"] not in {"ACTIVE", "INCOMPLETE"} or not pending:
                    raise DomainError("No saved draft is available. Retry interrupted work explicitly.", 409, "NO_PENDING_RESULT")
                if (not isinstance(pending, dict) or set(pending) != {"kind", "revision", "value", "simulated"}
                        or type(pending["revision"]) is not int or pending["revision"] != revision
                        or type(pending["simulated"]) is not bool or pending["kind"] not in ("NEEDS", "ADVICE")
                        or not isinstance(pending["value"], dict)):
                    raise DomainError("The saved draft is invalid. Revise the request instead.", 409, "INVALID_SAVED_RESULT")
                # Explicit simulation of a final-write failure, retaining the durable draft.
                if pending["kind"] == "ADVICE" and Store.fault(db, "ba_recording"):
                    p.update(errorCode="BA_RECORDING_FAILED", message="The final advice save failed. "
                             "A draft is saved; recover it without calling the model again.")
                    current["status"] = "INCOMPLETE"
                    Store.save(db, current)
                    Store.event(db, rid, "BA", "ADVICE_RECORDING_FAILED", {"revision": revision, "simulatedFixture": True})
                    fixture = True
                else:
                    fixture = False
                    value = deepcopy(pending["value"])
                    p.pop("message", None); p.pop("errorCode", None)
                    if pending["kind"] == "NEEDS":
                        if set(value) == {"extracted"}:
                            try:
                                extracted = validate_extraction(value["extracted"], p["messages"])
                            except (ValueError, TypeError, KeyError):
                                raise DomainError("The saved interpretation is invalid. Revise the request.", 409, "INVALID_SAVED_RESULT") from None
                            missing = [key for key in FIELDS if extracted[key] is None]
                            current["status"] = "CLARIFYING"
                            p.update(proposedNeeds=extracted, needsReady=not missing,
                                     questions=[QUESTIONS[key] for key in missing],
                                     message="Please answer the missing needs." if missing else
                                     "Review and explicitly confirm these interpreted needs before advice.")
                        elif set(value) == {"errorCode", "message"}:
                            current["status"] = "INCOMPLETE"
                            p.update(value, needsReady=False)
                        else:
                            raise DomainError("The saved interpretation is invalid.", 409, "INVALID_SAVED_RESULT")
                        event = "NEEDS_INTERPRETATION_RECORDED"
                    else:
                        if not p.get("needsConfirmed") or value.get("status") not in {"COMPLETED", "INCOMPLETE"}:
                            raise DomainError("The saved advice has no confirmed scope.", 409, "INVALID_SAVED_RESULT")
                        if value["status"] == "COMPLETED":
                            supplied = value.get("product")
                            if not isinstance(supplied, dict) or not isinstance(value.get("evidence"), dict):
                                raise DomainError("The saved advice evidence is invalid.", 409, "INVALID_SAVED_RESULT")
                            product = next((item for item in catalogue(db) if item["id"] == supplied.get("id")), None)
                            needs = p["needs"]
                            fact = "Moisturises dry skin" if needs["concern"] == "HYDRATION" else "Cleanses the skin"
                            if (not product or product != supplied or product["availability"] != "AVAILABLE"
                                    or product["price"] > needs["budget"] or fact not in product["facts"]
                                    or (needs["fragranceFree"] and not product["fragrance_free"])
                                    or not isinstance(value.get("reasons"), list) or not value["reasons"]
                                    or any(reason not in product["facts"] for reason in value["reasons"])
                                    or value["evidence"].get("catalogueRef") != f"catalogue:{product['id']}:v{product['version']}"
                                    or value["evidence"].get("constraints") != {key: needs[key] for key in FIELDS}):
                                value = {"status": "INCOMPLETE", "errorCode": "LLM_STALE_EVIDENCE",
                                         "message": "Catalogue or stock changed. Retry with fresh evidence.",
                                         "simulated": pending["simulated"]}
                            else:
                                value["evidence"].update(inventoryObservation=now(), availability=product["availability"])
                        current["status"] = value["status"]
                        value["simulated"] = pending["simulated"]
                        p.update(result=value)
                        event = "CONFIRMED_ADVICE_RECORDED"
                    p.update(simulated=pending["simulated"], recordedRevision=revision)
                    p.pop("pendingOutcome")
                    Store.save(db, current)
                    Store.event(db, rid, "BA", event, {"status": current["status"], "revision": revision,
                                "simulated": p["simulated"], "recovered": actor is not None})
            if fixture:
                raise DomainError("The final advice save failed. Refresh and recover the saved draft; no completion is claimed.",
                                  503, "BA_RECORDING_FAILED")
            return current
        except sqlite3.Error:
            # Final write rolled back. Its durable draft remains non-authoritative.
            try:
                with self.store.transaction() as db:
                    current = Store.get(db, rid, "BA")
                    if current["revision"] == revision and current["status"] == "ACTIVE" and current["payload"].get("pendingOutcome"):
                        current["status"] = "INCOMPLETE"
                        current["payload"].update(errorCode="BA_RECORDING_FAILED", message="The result save failed. "
                                                  "Recover the saved draft without repeating inference.")
                        Store.save(db, current)
            except sqlite3.Error:
                pass  # Even the failure cannot be stored; disclose without a false saved state.
            raise self._storage_error() from None
