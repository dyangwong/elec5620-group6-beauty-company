"""Use-case facade and local demo identity; no caller-supplied business identity."""
import hashlib
import hmac
import json
import secrets
import time
from http.cookies import CookieError, SimpleCookie

from .adapters.after_sales import MockAfterSales
from .adapters.mock import MockLlm, MockMedia
from .contracts import Actor, DomainError, require_role
from .modules.approval import Approval
from .modules.beauty_advisor import BeautyAdvisor, catalogue
from .modules.coordination import Coordination
from .modules.customer_service import CustomerService
from .modules.marketing import Marketing
from .store import Store, password_hash


class Company:
    def __init__(self, path, llm=None):
        self.store = Store(path)
        self.llm = llm or MockLlm()
        self.ba = BeautyAdvisor(self.llm)
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
            approval_ids = [r["id"] for r in db.execute("SELECT id,origin_id FROM approvals ORDER BY created DESC") if actor.role == "FOUNDER" or r["origin_id"] in ids]
            approvals = [self.ap.get(db, rid) for rid in approval_ids]
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
                    "mode": {"simulated": True, "model": "Deterministic mock", "media": "Storyboard placeholder",
                             "optionalFeatures": {"BA-F-03": False, "CS-F-03": False, "MC-F-03": False, "AP-F-03": False, "CO-F-03": False}}}

    def decide(self, actor, rid, data):
        with self.store.transaction() as db:
            review = self.ap.decide(db, actor, rid, data)
        # A delivery failure cannot roll back the committed decision above.
        with self.store.transaction() as db:
            return self.ap.deliver(db, review["id"])

    def redeliver(self, actor, rid):
        require_role(actor, "FOUNDER")
        with self.store.transaction() as db:
            return self.ap.deliver(db, rid)

    def set_fault(self, actor, fault):
        require_role(actor, "FOUNDER")
        if not isinstance(fault, str) or fault not in {"after_sales_timeout", "outcome_recording", "approval_delivery", "none"}:
            raise DomainError("Unsupported simulation fixture.")
        with self.store.transaction() as db:
            db.execute("DELETE FROM faults")
            if fault != "none":
                db.execute("INSERT INTO faults VALUES(?)", (fault,))
        return {"armed": fault}
