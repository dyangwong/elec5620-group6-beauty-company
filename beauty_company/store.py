"""Small transaction boundary; business effects are committed separately from receipts."""
from __future__ import annotations

import hashlib
import json
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def new_id(prefix: str) -> str:
    return f"{prefix}-{secrets.token_hex(6)}"


def encode(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def password_hash(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120000).hex()


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.transaction() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY, role TEXT NOT NULL, name TEXT NOT NULL,
                    salt TEXT NOT NULL, password_hash TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS sessions (
                    token_hash TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id),
                    csrf TEXT NOT NULL, expires REAL NOT NULL);
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY, name TEXT NOT NULL, price INTEGER NOT NULL,
                    fragrance_free INTEGER NOT NULL, facts TEXT NOT NULL,
                    version INTEGER NOT NULL, stock INTEGER, tone TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY, customer_id TEXT NOT NULL REFERENCES users(id),
                    product_id TEXT NOT NULL REFERENCES products(id), status TEXT NOT NULL,
                    policy TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS records (
                    id TEXT PRIMARY KEY, kind TEXT NOT NULL, owner_id TEXT NOT NULL,
                    revision INTEGER NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL,
                    created TEXT NOT NULL, updated TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS approvals (
                    id TEXT PRIMARY KEY, origin_role TEXT NOT NULL, origin_id TEXT NOT NULL,
                    revision INTEGER NOT NULL, action_ref TEXT, action TEXT NOT NULL,
                    evidence TEXT NOT NULL, status TEXT NOT NULL, decision_id TEXT UNIQUE,
                    decision TEXT, reason TEXT, founder_id TEXT, delivery TEXT NOT NULL,
                    created TEXT NOT NULL, predecessor TEXT,
                    UNIQUE(origin_role, origin_id, revision));
                CREATE TABLE IF NOT EXISTS approval_intents (
                    id TEXT PRIMARY KEY, approval_id TEXT NOT NULL UNIQUE REFERENCES approvals(id),
                    founder_id TEXT NOT NULL, kind TEXT NOT NULL, reason TEXT NOT NULL,
                    origin_role TEXT NOT NULL, origin_id TEXT NOT NULL, revision INTEGER NOT NULL,
                    action_ref TEXT, action TEXT NOT NULL, evidence TEXT NOT NULL,
                    status TEXT NOT NULL, decision_id TEXT,
                    created TEXT NOT NULL, updated TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS effects (
                    action_ref TEXT PRIMARY KEY, request_id TEXT NOT NULL,
                    revision INTEGER NOT NULL, product_id TEXT NOT NULL, result TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS events (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT, entity_id TEXT NOT NULL,
                    role TEXT NOT NULL, event TEXT NOT NULL, detail TEXT NOT NULL,
                    created TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS faults (name TEXT PRIMARY KEY);
            """)
            self._seed(db)

    def connect(self):
        db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA busy_timeout=10000")
        return db

    @contextmanager
    def transaction(self):
        db = self.connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    @contextmanager
    def read(self):
        db = self.connect()
        try:
            yield db
        finally:
            db.close()

    def _seed(self, db):
        for uid, role, name, password in [
            ("customer", "CUSTOMER", "Alex · Demo Customer", "customer-demo"),
            ("customer-2", "CUSTOMER", "Sam · Demo Customer", "customer-demo"),
            ("founder", "FOUNDER", "Human Founder / Operator", "founder-demo"),
        ]:
            if not db.execute("SELECT 1 FROM users WHERE id=?", (uid,)).fetchone():
                salt = secrets.token_hex(16)
                db.execute("INSERT INTO users VALUES(?,?,?,?,?)", (uid, role, name, salt, password_hash(password, salt)))
        products = [
            ("P-101", "Daily Hydration Cream", 4800, 1, ["Moisturises dry skin", "Fragrance-free", "50 ml"], 1, 12, "peach"),
            ("P-102", "Gentle Daily Cleanser", 3200, 1, ["Cleanses the skin", "Fragrance-free", "150 ml"], 1, 8, "sage"),
            ("P-103", "Rich Moisture Cream", 6200, 0, ["Moisturises dry skin", "Contains fragrance", "50 ml"], 1, 0, "lilac"),
        ]
        for pid, name, price, fragrance, facts, version, stock, tone in products:
            db.execute("INSERT OR IGNORE INTO products VALUES(?,?,?,?,?,?,?,?)",
                       (pid, name, price, fragrance, encode(facts), version, stock, tone))
        # Declared fixture eligibility, not an invented real return window.
        policy = encode({"id": "POLICY-DEMO-EXCHANGE-v1", "eligible": True,
                         "requiresApproval": True, "simulated": True,
                         "reason": "Declared disputed-exchange fixture; no monetary threshold is inferred."})
        db.execute("INSERT OR IGNORE INTO orders VALUES(?,?,?,?,?)", ("ORD-1001", "customer", "P-103", "DELIVERED", policy))
        db.execute("INSERT OR IGNORE INTO orders VALUES(?,?,?,?,?)", ("ORD-2001", "customer-2", "P-102", "DELIVERED", policy))

    @staticmethod
    def event(db, entity_id, role, event, detail):
        db.execute("INSERT INTO events(entity_id,role,event,detail,created) VALUES(?,?,?,?,?)",
                   (entity_id, role, event, encode(detail), now()))

    @staticmethod
    def create(db, kind, owner_id, status, payload, prefix, revision=1):
        rid = new_id(prefix)
        stamp = now()
        db.execute("INSERT INTO records VALUES(?,?,?,?,?,?,?,?)",
                   (rid, kind, owner_id, revision, status, encode(payload), stamp, stamp))
        return rid

    @staticmethod
    def get(db, rid, kind=None):
        row = db.execute("SELECT * FROM records WHERE id=?", (rid,)).fetchone()
        if not row or (kind and row["kind"] != kind):
            from .contracts import DomainError
            raise DomainError("Record not found.", 404, "NOT_FOUND")
        item = dict(row)
        item["payload"] = json.loads(item["payload"])
        return item

    @staticmethod
    def save(db, record):
        db.execute("UPDATE records SET revision=?,status=?,payload=?,updated=? WHERE id=?",
                   (record["revision"], record["status"], encode(record["payload"]), now(), record["id"]))

    @staticmethod
    def fault(db, name):
        return db.execute("DELETE FROM faults WHERE name=?", (name,)).rowcount == 1
