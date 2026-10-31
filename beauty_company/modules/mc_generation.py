"""MC generation persistence: explicit retry, storage-only recovery and cancellation."""
from copy import deepcopy
import sqlite3

from ..contracts import DomainError, require_role, revision_value, text_value
from ..store import Store


class McGeneration:
    def __init__(self, store, marketing):
        self.store, self.mc = store, marketing

    @staticmethod
    def _input(data, fields):
        if not isinstance(data, dict) or set(data) != set(fields):
            raise DomainError("Supply only the displayed campaign fields.")

    def _owned(self, db, actor, rid, revision):
        record = Store.get(db, rid, "MC")
        if record["owner_id"] != actor.id:
            raise DomainError("Only the campaign owner may change this draft.", 403, "FORBIDDEN")
        if record["revision"] != revision:
            raise DomainError("The campaign changed. Refresh the current revision.", 409, "STALE_SCOPE")
        return record

    @staticmethod
    def public_record(record):
        """Uncommitted generated content never becomes a browser preview/history."""
        result = deepcopy(record)

        def project(payload):
            pending = payload.get("pendingGeneration")
            if pending is not None:
                payload["pendingGeneration"] = ({key: pending[key] for key in
                    ("revision", "status", "textSimulated", "mediaSimulated") if key in pending}
                    if isinstance(pending, dict) else {"invalid": True})
            for prior in payload.get("history", []):
                project(prior.get("payload", {}))
        project(result["payload"])
        return result

    @staticmethod
    def _history(record):
        payload = record["payload"]
        return deepcopy(payload.get("history", [])) + [{"revision": record["revision"],
            "status": record["status"], "payload": deepcopy({k: v for k, v in payload.items() if k != "history"})}]

    @staticmethod
    def _storage_error():
        return DomainError("Generation could not be recorded. No review-ready result is claimed. "
                           "Refresh; recover a saved draft if offered, otherwise retry explicitly.",
                           503, "MC_STORAGE_UNAVAILABLE")

    def start(self, actor, data, rid=None):
        require_role(actor, "FOUNDER")
        self._input(data, {"brief", "productId"} | ({"contextRevision"} if rid else set()))
        if not isinstance(data["brief"], str) or len(data["brief"]) > 2000:
            raise DomainError("Campaign brief must be text of at most 2000 characters.")
        brief = data["brief"].strip()  # An empty correction is retained as an INCOMPLETE revision.
        product_id = text_value(data["productId"], "Product ID", 100)
        with self.store.transaction() as db:
            history = []
            if rid:
                record = self._owned(db, actor, rid, revision_value(data["contextRevision"]))
                if record["status"] == "CANCELLED":
                    raise DomainError("A cancelled campaign requires a new campaign.", 409, "INVALID_STATE")
                history = self._history(record)
                self.mc.ap.supersede(db, record["payload"].get("approvalId"))
                record["revision"] += 1
            else:
                rid = Store.create(db, "MC", actor.id, "DRAFTING", {}, "MC")
                record = Store.get(db, rid, "MC")
            self._begin(db, record, brief, product_id, history)
        return self._generate(record)

    def _begin(self, db, record, brief, product_id, history):
        record["status"] = "GENERATING"
        record["payload"] = {"brief": brief, "productId": product_id, "generationLifecycle": True,
            "simulated": self.mc.simulated, "textSimulated": self.mc.simulated,
            "mediaSimulated": not self.mc.template_video, "history": history}
        Store.save(db, record)
        Store.event(db, record["id"], "MC", "TEXT_GENERATION_STARTED",
                    {"revision": record["revision"], "simulated": self.mc.simulated})

    def _generate(self, record):
        scope = record["payload"]
        try:
            with self.store.read() as db:
                payload = self.mc.generate(db, {"brief": scope["brief"], "productId": scope["productId"]})
        except DomainError as error:
            payload = {"failure": {"code": error.code, "reason": str(error)}}
            status = "INCOMPLETE" if error.code in {"INVALID_REQUEST", "SOURCE_CONFLICT"} else error.code if error.code in {"INCOMPLETE", "CONTENT_REJECTED", "GENERATION_FAILED"} else (
                "CONTENT_REJECTED" if error.code == "LLM_INVALID_OUTPUT" else "GENERATION_FAILED")
        else:
            status = "READY"
        try:
            with self.store.transaction() as db:
                current = Store.get(db, record["id"], "MC")
                if current["revision"] != record["revision"] or current["status"] != "GENERATING":
                    raise DomainError("A newer or cancelled revision exists. Late output was discarded.", 409, "STALE_SCOPE")
                current["payload"]["pendingGeneration"] = {"revision": record["revision"], "status": status,
                    "payload": deepcopy(payload), "textSimulated": scope["textSimulated"],
                    "mediaSimulated": scope["mediaSimulated"]}
                Store.save(db, current)
        except sqlite3.Error:
            # Staging did not commit: no saved result is invented and a retry needs a new revision.
            raise self._storage_error() from None
        return self._finish(record["id"], record["revision"])

    def recover(self, actor, rid, data):
        require_role(actor, "FOUNDER")
        self._input(data, {"contextRevision"})
        revision = revision_value(data["contextRevision"])
        with self.store.read() as db:
            self._owned(db, actor, rid, revision)
        return self._finish(rid, revision, actor)

    def _finish(self, rid, revision, actor=None):
        try:
            fixture = False
            with self.store.transaction() as db:
                current = self._owned(db, actor, rid, revision) if actor else Store.get(db, rid, "MC")
                if current["revision"] != revision or current["status"] == "CANCELLED":
                    raise DomainError("The generated draft is stale or cancelled.", 409, "STALE_SCOPE")
                scope = current["payload"]
                pending = scope.get("pendingGeneration")
                if not pending and scope.get("generationRecordedRevision") == revision:
                    return self.public_record(current)
                if current["status"] not in {"GENERATING", "RECORDING_FAILED"} or not pending:
                    raise DomainError("No saved generation is available. Retry interrupted work explicitly.",
                                      409, "NO_PENDING_RESULT")
                if (not isinstance(pending, dict) or set(pending) != {
                        "revision", "status", "payload", "textSimulated", "mediaSimulated"}
                        or type(pending["revision"]) is not int or pending["revision"] != revision
                        or type(pending["textSimulated"]) is not bool or type(pending["mediaSimulated"]) is not bool
                        or pending["textSimulated"] is not scope.get("textSimulated")
                        or pending["mediaSimulated"] is not scope.get("mediaSimulated")
                        or pending["status"] not in {"READY", "INCOMPLETE", "CONTENT_REJECTED", "GENERATION_FAILED"}
                        or not isinstance(pending["payload"], dict)):
                    raise DomainError("The saved generation is invalid. Revise the request.", 409, "INVALID_SAVED_RESULT")
                if Store.fault(db, "mc_recording"):
                    current["status"] = "RECORDING_FAILED"
                    scope["failure"] = {"code": "MC_RECORDING_FAILED", "reason":
                        "Final save failed. A generation draft is saved; recover without generating again."}
                    Store.save(db, current)
                    Store.event(db, rid, "MC", "GENERATION_RECORDING_FAILED",
                                {"revision": revision, "simulatedFixture": True})
                    fixture = True
                else:
                    payload = deepcopy(pending["payload"])
                    status = pending["status"]
                    if status == "READY":
                        try:
                            self.mc.validate_saved(db, payload, scope)
                        except DomainError as error:
                            if error.code == "MC_MEDIA_RECOVERY_UNAVAILABLE":
                                raise  # Preserve the draft until its original artifact configuration is restored.
                            payload = {"failure": {"code": error.code, "reason": str(error)}}
                            status = "INCOMPLETE" if error.code == "MC_STALE_EVIDENCE" else "CONTENT_REJECTED"
                        except (ValueError, TypeError, KeyError, IndexError):
                            payload = {"failure": {"code": "INVALID_SAVED_RESULT", "reason":
                                       "Saved generation failed independent validation. Revise the request."}}
                            status = "CONTENT_REJECTED"
                    elif (set(payload) != {"failure"} or not isinstance(payload["failure"], dict)
                          or set(payload["failure"]) != {"code", "reason"}
                          or any(not isinstance(payload["failure"][key], str) for key in ("code", "reason"))):
                        raise DomainError("The saved failure is invalid.", 409, "INVALID_SAVED_RESULT")
                    original = {key: deepcopy(value) for key, value in scope.items()
                                if key not in {"pendingGeneration", "failure"}}
                    current["payload"] = {**original, **payload, "generationRecordedRevision": revision}
                    if status == "READY":
                        self.mc._review(db, current)
                    else:
                        current["status"] = status
                        Store.save(db, current)
                        Store.event(db, rid, "MC", "TEXT_GENERATION_FAILED", {
                            "revision": revision, "code": payload["failure"]["code"]})
                    Store.event(db, rid, "MC", "GENERATION_RECORDED", {
                        "revision": revision, "recovered": actor is not None,
                        "textSimulated": pending["textSimulated"], "mediaSimulated": pending["mediaSimulated"]})
            if fixture:
                raise DomainError("Final generation save failed. Refresh and recover the saved draft; no review is ready.",
                                  503, "MC_RECORDING_FAILED")
            return self.public_record(current)
        except sqlite3.Error:
            try:
                with self.store.transaction() as db:
                    current = Store.get(db, rid, "MC")
                    if (current["revision"] == revision and current["status"] in {"GENERATING", "RECORDING_FAILED"}
                            and current["payload"].get("pendingGeneration")):
                        current["status"] = "RECORDING_FAILED"
                        current["payload"]["failure"] = {"code": "MC_RECORDING_FAILED", "reason":
                            "Generation save failed. Recover the saved draft without repeating generation."}
                        Store.save(db, current)
                        Store.event(db, rid, "MC", "GENERATION_RECORDING_FAILED", {"revision": revision,
                                    "simulatedFixture": False, "savedDraftRetained": True})
            except sqlite3.Error:
                pass  # A total write outage can leave GENERATING with a pending draft; never claim failure was saved.
            raise self._storage_error() from None

    def retry(self, actor, rid, data):
        require_role(actor, "FOUNDER")
        self._input(data, {"contextRevision"})
        revision = revision_value(data["contextRevision"])
        with self.store.transaction() as db:
            record = self._owned(db, actor, rid, revision)
            if record["status"] not in {"DRAFTING", "GENERATING", "RECORDING_FAILED", "GENERATION_FAILED", "INCOMPLETE"}:
                raise DomainError("Only interrupted or failed generation can be retried.", 409, "INVALID_STATE")
            if record["payload"].get("pendingGeneration"):
                raise DomainError("A saved generation is available. Recover it or explicitly revise.", 409, "RECOVERY_AVAILABLE")
            if record["payload"].get("approvalId") or record["payload"].get("decisionId"):
                raise DomainError("This draft already has review authority. Use its decision recovery or revise explicitly.",
                                  409, "INVALID_STATE")
            p = record["payload"]
            brief = text_value(p.get("brief"), "Campaign brief")
            product_id = text_value(p.get("productId"), "Product ID", 100)
            history = self._history(record)
            record["revision"] += 1
            self._begin(db, record, brief, product_id, history)
            Store.event(db, rid, "MC", "GENERATION_RETRY_REQUESTED", {"revision": record["revision"]})
        return self._generate(record)

    def cancel(self, actor, rid, data):
        require_role(actor, "FOUNDER")
        self._input(data, {"contextRevision"})
        revision = revision_value(data["contextRevision"])
        try:
            with self.store.transaction() as db:
                record = self._owned(db, actor, rid, revision)
                if record["status"] == "CANCELLED":
                    return self.public_record(record)
                if record["status"] not in {"DRAFTING", "GENERATING", "RECORDING_FAILED", "GENERATION_FAILED",
                                            "INCOMPLETE", "CONTENT_REJECTED", "REVIEW_PENDING", "REVISION_REQUIRED"}:
                    raise DomainError("A decided draft cannot be cancelled retroactively. Revise it instead.",
                                      409, "INVALID_STATE")
                history = self._history(record)
                p = record["payload"]
                self.mc.ap.supersede(db, p.get("approvalId"))
                record["revision"] += 1
                record["status"] = "CANCELLED"
                record["payload"] = {key: deepcopy(p[key]) for key in
                    ("brief", "productId", "simulated", "textSimulated", "mediaSimulated", "generationLifecycle") if key in p}
                record["payload"]["history"] = history
                Store.save(db, record)
                Store.event(db, rid, "MC", "CAMPAIGN_CANCELLED", {"revision": record["revision"],
                    "lateOutputSuppressed": True, "providerAbortGuaranteed": False})
            return self.public_record(record)
        except sqlite3.Error:
            raise DomainError("Cancellation could not be recorded. It is not confirmed; refresh before retrying.",
                              503, "MC_CANCELLATION_NOT_RECORDED") from None
