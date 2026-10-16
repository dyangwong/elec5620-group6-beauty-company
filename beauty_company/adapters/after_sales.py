"""A simulated external service with an actionRef lookup and once-only effects."""
import json

from ..contracts import DomainError
from ..store import Store, encode, new_id


class MockAfterSales:
    def __init__(self, store):
        self.store = store

    def execute_resolution(self, request_id, action_ref, revision, product_id):
        with self.store.transaction() as db:
            previous = db.execute("SELECT * FROM effects WHERE action_ref=?", (action_ref,)).fetchone()
            if previous:
                if previous["request_id"] != request_id or previous["revision"] != revision or previous["product_id"] != product_id:
                    raise DomainError("An action reference cannot be reused for a different action.", 409, "ACTION_CONFLICT")
                return json.loads(previous["result"])
            request = Store.get(db, request_id, "CS")
            if request["revision"] != revision or request["status"] != "EXECUTING":
                raise DomainError("The request is no longer executable.", 409, "STALE_SCOPE")
            # Conditional update prevents a check-then-write oversell race.
            changed = db.execute("UPDATE products SET stock=stock-1 WHERE id=? AND stock>0", (product_id,)).rowcount
            if changed != 1:
                raise DomainError("The replacement is unavailable or its stock is unknown.", 409, "STOCK_UNAVAILABLE")
            result = {"serviceRef": new_id("SIM"), "actionRef": action_ref, "productId": product_id,
                      "outcome": "SIMULATED_EXCHANGE_REQUEST_ACCEPTED", "simulated": True,
                      "remainingSteps": "No shipment or payment has occurred. Physical return and replacement are outside this simulation."}
            db.execute("INSERT INTO effects VALUES(?,?,?,?,?)", (action_ref, request_id, revision, product_id, encode(result)))
            db.execute("UPDATE orders SET status='EXCHANGE_REQUEST_ACCEPTED' WHERE id=?", (request["payload"]["orderId"],))
            return result

    def lookup_outcome(self, action_ref):
        with self.store.read() as db:
            row = db.execute("SELECT result FROM effects WHERE action_ref=?", (action_ref,)).fetchone()
            return json.loads(row["result"]) if row else None
