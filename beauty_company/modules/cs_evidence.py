"""CS-local, injectable reads of the declared exchange fixture; no policy inference."""
import json
import sqlite3

from ..contracts import DomainError


class ExchangeEvidence:
    @staticmethod
    def order(db, customer_id, order_id):
        # Verify association before loading or interpreting protected policy evidence.
        try:
            row = db.execute("SELECT * FROM orders WHERE id=? AND customer_id=?",
                             (order_id, customer_id)).fetchone()
        except sqlite3.Error:
            raise DomainError("Order verification is unavailable. No action was authorised.",
                              409, "ORDER_READ_UNAVAILABLE") from None
        if not row:
            raise DomainError("No accessible order matches that reference.", 404, "ORDER_NOT_FOUND")
        return dict(row)

    @staticmethod
    def policy(order):
        try:
            policy = json.loads(order["policy"])
        except (ValueError, TypeError):
            return {"state": "CONFLICTING", "refs": []}
        if not isinstance(policy, dict):
            return {"state": "MISSING", "refs": []}
        ref = policy.get("id")
        refs = [ref] if isinstance(ref, str) and ref.strip() else []
        conflicts = policy.get("conflictingRefs", [])
        if conflicts:
            if isinstance(conflicts, list):
                refs += [r for r in conflicts if isinstance(r, str) and r.strip()]
            return {"state": "CONFLICTING", "refs": refs}
        if policy.get("eligible") is False or order["status"] != "DELIVERED":
            return {"state": "UNSUPPORTED", "refs": refs}
        if (not refs or policy.get("eligible") is not True
                or policy.get("requiresApproval") is not True or policy.get("missingFields")):
            return {"state": "MISSING", "refs": refs}
        return {"state": "SUFFICIENT", "refs": refs, "policy": policy}

    @staticmethod
    def stock(db, product_id):
        try:
            row = db.execute("SELECT stock FROM products WHERE id=?", (product_id,)).fetchone()
        except sqlite3.Error:
            raise DomainError("Replacement availability could not be read. No action was authorised.",
                              409, "STOCK_READ_UNAVAILABLE") from None
        if not row or row["stock"] is None:
            return "UNKNOWN"
        return "AVAILABLE" if row["stock"] > 0 else "UNAVAILABLE"


def policy_evidence(reader, order):
    try:
        result = reader.policy(order)
    except (sqlite3.Error, TimeoutError, ConnectionError):
        result = {"state": "UNAVAILABLE", "refs": []}
    return result


def require_policy(result):
    state = result["state"]
    if state != "SUFFICIENT":
        messages = {
            "MISSING": "Required policy evidence is missing. Correct the evidence before a fresh assessment.",
            "CONFLICTING": "Policy evidence conflicts. Authorised clarification is required.",
            "UNAVAILABLE": "Policy evidence could not be read. No action was authorised.",
            "UNSUPPORTED": "Current order/policy evidence does not support this exchange fixture.",
        }
        error = DomainError(messages[state], 409, "POLICY_" + state)
        error.evidence = {"state": state, "refs": result["refs"]}
        raise error
    return result["policy"]


def read_order(reader, db, customer_id, order_id):
    try:
        return reader.order(db, customer_id, order_id)
    except (sqlite3.Error, TimeoutError, ConnectionError):
        raise DomainError("Order verification is unavailable. No action was authorised.",
                          409, "ORDER_READ_UNAVAILABLE") from None


def read_stock(reader, db, product_id):
    try:
        return reader.stock(db, product_id)
    except (sqlite3.Error, TimeoutError, ConnectionError):
        raise DomainError("Replacement availability could not be read. No action was authorised.",
                          409, "STOCK_READ_UNAVAILABLE") from None


def require_same_policy(current, previous):
    if current != previous:
        error = DomainError("Policy evidence changed. A revised proposal is required.", 409, "STALE_POLICY")
        error.evidence = {"state": "CHANGED", "refs": list(dict.fromkeys([previous["id"], current["id"]]))}
        raise error
