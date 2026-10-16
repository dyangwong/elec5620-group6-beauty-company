"""CO-M-01: traceable handoff; acknowledgement is not business completion."""
from ..store import Store


class Coordination:
    @staticmethod
    def create(db, customer_id, cs_id):
        return Store.create(db, "CO", customer_id, "PENDING_VALIDATION",
                            {"originId": cs_id, "handoffs": [], "simulated": True}, "CO")

    @staticmethod
    def state(db, rid, status, event, detail):
        record = Store.get(db, rid, "CO")
        record["status"] = status
        Store.save(db, record)
        Store.event(db, rid, "CO", event, detail)

    @staticmethod
    def advice_handoff(db, rid, needs, advisor):
        record = Store.get(db, rid, "CO")
        # No order details, identity credentials or unrelated profile fields reach BA.
        context = {key: needs[key] for key in ("message", "concern", "budget", "fragranceFree")}
        handoff = {"fromRole": "CS", "toRole": "BA", "authorisedContext": context, "status": "SENT"}
        record["payload"]["handoffs"].append(handoff)
        record["status"] = "HANDOFF_SENT"
        Store.save(db, record)
        Store.event(db, rid, "CO", "HANDOFF_SENT", handoff)
        result = advisor.recommend(db, context)
        handoff["status"] = "COMPLETED" if result["status"] == "COMPLETED" else "FAILED"
        handoff["result"] = result
        record["status"] = "PENDING_VALIDATION" if result["status"] == "COMPLETED" else "ESCALATED"
        Store.save(db, record)
        Store.event(db, rid, "CO", "ADVICE_RESULT_RECORDED", {"status": handoff["status"], "businessExecution": False})
        return result
