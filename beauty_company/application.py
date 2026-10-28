"""Use-case facade and local demo identity; no caller-supplied business identity."""
import hashlib
import hmac
import json
import secrets
import time
from copy import deepcopy
from http.cookies import CookieError, SimpleCookie

from .adapters.after_sales import MockAfterSales
from .adapters.mock import MockLlm, MockMedia
from .contracts import Actor, DomainError, require_role, revision_value, text_value
from .modules.approval import Approval
from .modules.beauty_advisor import BeautyAdvisor, catalogue, validated_needs
from .modules.ba_intake import BaIntake
from .modules.coordination import Coordination
from .modules.customer_service import CustomerService
from .modules.marketing import Marketing
from .store import Store, password_hash

RECORDING_FAILED_MESSAGE = ("The decision could not be recorded. No approval was delivered and no business work "
                            "was dispatched. The intended decision is stored and can be recovered from storage.")


class Company:
    def __init__(self, path, llm=None):
        self.store = Store(path)
        self.llm = llm or MockLlm()
        self.ba = BeautyAdvisor(self.llm)
        self.ba_intake = BaIntake(self.store, self.ba)
        self.ap = Approval()
        self.co = Coordination()
        self.cs = CustomerService(self.store, self.ba, self.co, self.ap, MockAfterSales(self.store))
        self.mc = Marketing(self.llm, MockMedia(), self.ap)

    def login(self, username, password):
        if not isinstance(username, str) or not isinstance(password, str) or len(password) > 200:
            raise DomainError("Invalid demo credentials.", 401, "UNAUTHENTICATED")
        with self.store.transaction() as db:
            row = db.execute("SELECT * FROM users WHERE id=?", (username,)).fetchone()
            if not row or not hmac.compare_digest(row["password_hash"], password_hash(password, row["salt"])):
                raise DomainError("Invalid demo credentials.", 401, "UNAUTHENTICATED")
            token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
            db.execute("DELETE FROM sessions WHERE expires<?", (time.time(),))
            # Eight hours is a declared local session fixture, not approval validity.
            db.execute("INSERT INTO sessions VALUES(?,?,?,?)", (hashlib.sha256(token.encode()).hexdigest(), username, csrf, time.time() + 28800))
            return token, csrf, Actor(row["id"], row["role"], row["name"])

    def mode(self):
        live = not self.ba.simulated
        mc_live = not self.mc.simulated
        return {"simulated": not (live or mc_live), "model": "Local shared model" if live or mc_live else "Deterministic mock",
                "ba": "LIVE" if live else "MOCK", "mc": "LIVE" if mc_live else "MOCK", "csIntent": "NOT_CONNECTED",
                "baNeeds": ("LIVE" if live else "MOCK") if callable(getattr(self.llm, "extract_needs", None)) else "NOT_CONNECTED",
                "media": "Storyboard placeholder", "commerce": "SIMULATED",
                "optionalFeatures": {"BA-F-03": False, "CS-F-03": False, "MC-F-03": False,
                                     "AP-F-03": False, "CO-F-03": False}}

    def campaign(self, actor, data, rid=None):
        """Opt-in MC HTTP path: persist scope, infer without a write lock, revalidate/save/review."""
        require_role(actor, "FOUNDER")
        expected = {"brief", "productId", *({"contextRevision"} if rid else set())}
        if not isinstance(data, dict) or set(data) != expected:
            raise DomainError("Supply only the displayed campaign fields.")
        brief = text_value(data["brief"], "Campaign brief")
        product_id = text_value(data["productId"], "Product ID", 100)
        with self.store.transaction() as db:
            history = []
            if rid:
                record = Store.get(db, rid, "MC")
                if record["owner_id"] != actor.id:
                    raise DomainError("Only the campaign owner may revise this draft.", 403, "FORBIDDEN")
                if revision_value(data["contextRevision"]) != record["revision"]:
                    raise DomainError("The draft revision changed.", 409, "STALE_SCOPE")
                history = deepcopy(record["payload"].get("history", []))
                history.append({"revision": record["revision"], "status": record["status"],
                                "payload": deepcopy({k: v for k, v in record["payload"].items() if k != "history"})})
                self.ap.supersede(db, record["payload"].get("approvalId"))
                record["revision"] += 1
            else:
                rid = Store.create(db, "MC", actor.id, "DRAFTING", {}, "MC")
                record = Store.get(db, rid, "MC")
            record["status"] = "DRAFTING"
            record["payload"] = {"brief": brief, "productId": product_id, "simulated": self.mc.simulated,
                                 "textSimulated": self.mc.simulated, "mediaSimulated": True, "history": history}
            Store.save(db, record)
            Store.event(db, rid, "MC", "TEXT_GENERATION_STARTED", {"revision": record["revision"], "simulated": self.mc.simulated})
        try:
            with self.store.read() as db:
                payload = self.mc.generate(db, {"brief": brief, "productId": product_id})
        except DomainError as error:
            payload = {**record["payload"], "failure": {"code": error.code, "reason": str(error)}}
            status = error.code if error.code in {"INCOMPLETE", "CONTENT_REJECTED", "GENERATION_FAILED"} else (
                "CONTENT_REJECTED" if error.code == "LLM_INVALID_OUTPUT" else "GENERATION_FAILED")
        else:
            status = "DRAFTING"
        with self.store.transaction() as db:
            current = Store.get(db, rid, "MC")
            if current["revision"] != record["revision"] or current["status"] != "DRAFTING":
                raise DomainError("This generated draft is stale. Output was discarded.", 409, "STALE_SCOPE")
            if status == "DRAFTING":
                product = next((p for p in catalogue(db) if p["id"] == product_id), None)
                if product != payload["product"]:
                    payload = {**record["payload"], "failure": {"code": "MC_STALE_EVIDENCE",
                               "reason": "Catalogue changed during generation. Revise with fresh evidence."}}
                    status = "INCOMPLETE"
            payload["history"] = history
            current["payload"] = payload
            if status == "DRAFTING":
                self.mc._review(db, current)
            else:
                current["status"] = status
                Store.save(db, current)
                Store.event(db, rid, "MC", "TEXT_GENERATION_FAILED", {"revision": current["revision"], "code": payload["failure"]["code"]})
            return current

    def consult(self, actor, data):
        """BA first live slice: no write lock during inference; recheck before save."""
        require_role(actor, "CUSTOMER")
        try:
            needs = validated_needs(data)
        except DomainError as error:
            with self.store.transaction() as db:
                return self.ba._record(db, actor, "CLARIFYING", {"message": str(error), "simulated": True})
        with self.store.read() as db:
            result = self.ba.recommend(db, needs)
        with self.store.transaction() as db:
            if result["status"] == "COMPLETED":
                current = next((p for p in catalogue(db) if p["id"] == result["product"]["id"]), None)
                if current != result["product"]:
                    result = {"status": "INCOMPLETE", "message": "Catalogue or stock changed during advice. Submit a fresh consultation.",
                              "errorCode": "LLM_STALE_EVIDENCE", "simulated": self.ba.simulated}
            return self.ba._record(db, actor, result["status"],
                                   {"needs": needs, "result": result, "simulated": result["simulated"]})

    def session(self, cookie):
        jar = SimpleCookie()
        try:
            jar.load(cookie or "")
            token = jar["beauty_session"].value
        except (KeyError, ValueError, CookieError):
            raise DomainError("Sign in to a demo workspace.", 401, "UNAUTHENTICATED")
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        with self.store.read() as db:
            row = db.execute("""SELECT users.*,sessions.csrf FROM sessions JOIN users ON users.id=sessions.user_id
                                WHERE token_hash=? AND expires>?""", (token_hash, time.time())).fetchone()
            if not row:
                raise DomainError("Your demo session expired. Sign in again.", 401, "UNAUTHENTICATED")
            return Actor(row["id"], row["role"], row["name"]), row["csrf"], token_hash

    def snapshot(self, actor):
        with self.store.read() as db:
            query = "SELECT id FROM records" + (" WHERE owner_id=?" if actor.role != "FOUNDER" else "") + " ORDER BY created DESC,id"
            ids = [r["id"] for r in db.execute(query, (actor.id,) if actor.role != "FOUNDER" else ())]
            records = [Store.get(db, rid) for rid in ids]
            records = [self.ba_intake.public_record(record) if record["kind"] == "BA"
                       and record["payload"].get("naturalNeeds") else record for record in records]
            approval_ids = [r["id"] for r in db.execute("SELECT id,origin_id FROM approvals ORDER BY created DESC") if actor.role == "FOUNDER" or r["origin_id"] in ids]
            approvals = []
            for rid in approval_ids:
                review = self.ap.get(db, rid)
                # A pending intent is not an approval. It is exposed so the intended
                # scope of a failed recording stays visible and recoverable.
                review["intent"] = self.ap.intent(db, rid)
                approvals.append(review)
            visible = set(ids + approval_ids)
            events = []
            for r in db.execute("SELECT * FROM events ORDER BY seq DESC LIMIT 1000"):
                if r["entity_id"] in visible:
                    item = dict(r)
                    item["detail"] = json.loads(item["detail"])
                    events.append(item)
            orders = []
            order_query = "SELECT * FROM orders" + (" WHERE customer_id=?" if actor.role == "CUSTOMER" else "")
            for row in db.execute(order_query, (actor.id,) if actor.role == "CUSTOMER" else ()):
                order = dict(row)
                order["policy"] = json.loads(order["policy"])
                orders.append(order)
            faults = [r["name"] for r in db.execute("SELECT name FROM faults")] if actor.role == "FOUNDER" else []
            return {"actor": actor.__dict__, "products": catalogue(db), "orders": orders,
                    "records": records, "approvals": approvals, "events": events[:150], "faults": faults,
                    "mode": self.mode()}

    def decide(self, actor, rid, data):
        # The intent is persisted in its own committed transaction, so a failed
        # decision commit leaves the intended decision recoverable from storage.
        with self.store.transaction() as db:
            intent = self.ap.prepare_intent(db, actor, rid, data)
        review = self._commit_intent(actor, rid, intent)
        # A delivery failure cannot roll back the committed decision above.
        with self.store.transaction() as db:
            return self.ap.deliver(db, review["id"])

    def _commit_intent(self, actor, rid, intent):
        try:
            with self.store.transaction() as db:
                review = self.ap.commit_intent(db, intent["id"], actor)
        except DomainError:
            raise
        except Exception as error:
            # The commit rolled back. Expose RECORDING_FAILED without a decision id.
            with self.store.transaction() as db:
                self.ap.mark_recording_failed(db, intent, {"error": type(error).__name__})
            raise DomainError(RECORDING_FAILED_MESSAGE, 409, "RECORDING_FAILED") from error
        if review is None:
            raise DomainError(RECORDING_FAILED_MESSAGE, 409, "RECORDING_FAILED")
        return review

    def recover_decision(self, actor, rid, data=None):
        """Recover a decision whose recording failed, using the stored intent only.

        The Founder, kind, reason and exact scope come from durable storage, never
        from the caller. Scope and authority are revalidated before the commit.
        """
        require_role(actor, "FOUNDER")
        if data is not None:
            if set(data) != {"contextRevision"}:
                raise DomainError("Recovery accepts only contextRevision. The decision and reason come from storage.")
            revision = revision_value(data["contextRevision"])
        with self.store.read() as db:
            if data is not None:
                review = self.ap.get(db, rid)
                origin = Store.get(db, review["origin_id"], review["origin_role"])
                if (revision != review["revision"] or origin["revision"] != revision
                        or origin["payload"].get("approvalId") != rid):
                    raise DomainError("This action or context revision has changed. Fresh review is required.",
                                      409, "STALE_SCOPE")
            intent = self.ap.intent(db, rid)
        if not intent:
            raise DomainError("There is no stored decision intent to recover.", 409, "NO_INTENT")
        if intent["founder_id"] != actor.id:
            raise DomainError("This decision intent belongs to another authorised decision maker.", 403, "FORBIDDEN")
        if intent["status"] == "COMMITTED":
            # The decision is already authoritative. Recovery never commits a second one.
            with self.store.read() as db:
                return self.ap.get(db, rid)
        review = self._commit_intent(actor, rid, intent)
        with self.store.transaction() as db:
            return self.ap.deliver(db, review["id"])

    def redeliver(self, actor, rid):
        require_role(actor, "FOUNDER")
        with self.store.transaction() as db:
            return self.ap.deliver(db, rid)

    def set_fault(self, actor, fault):
        require_role(actor, "FOUNDER")
        if not isinstance(fault, str) or fault not in {"after_sales_timeout", "outcome_recording", "approval_delivery", "approval_recording", "ba_recording", "none"}:
            raise DomainError("Unsupported simulation fixture.")
        with self.store.transaction() as db:
            db.execute("DELETE FROM faults")
            if fault != "none":
                db.execute("INSERT INTO faults VALUES(?)", (fault,))
        return {"armed": fault}
