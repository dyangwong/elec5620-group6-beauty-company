"""CS-M-01: initial exchange slice; return/refund paths remain in the backlog."""
import json

from ..contracts import DomainError, require_role, revision_value, text_value
from ..store import Store, new_id
from .beauty_advisor import validated_needs
from .cs_evidence import ExchangeEvidence, policy_evidence, read_order, read_stock, require_policy, require_same_policy


class CustomerService:
    def __init__(self, store, advisor, coordination, approval, after_sales, evidence=None):
        self.store, self.advisor, self.co, self.ap, self.port = store, advisor, coordination, approval, after_sales
        self.evidence = evidence or ExchangeEvidence()

    @staticmethod
    def owned(db, actor, rid):
        require_role(actor, "CUSTOMER")
        record = Store.get(db, rid, "CS")
        if record["owner_id"] != actor.id:
            raise DomainError("Record not found.", 404, "NOT_FOUND")
        return record

    def eligible_order(self, db, customer_id, order_id):
        order = read_order(self.evidence, db, customer_id, order_id)
        return order, require_policy(policy_evidence(self.evidence, order))

    def _blocked(self, db, record, error, evidence=None):
        """Persist only permitted reasons, never provider exceptions or foreign order data."""
        record["status"] = "NEEDS_INFORMATION" if error.code == "POLICY_MISSING" else "UNRESOLVED"
        detail = {"code": error.code, "reason": str(error), "executionOccurred": False,
                  "contextRevision": record["revision"]}
        evidence = evidence or getattr(error, "evidence", None)
        if evidence:
            detail["policyState"] = evidence["state"]
            detail["policyRefs"] = evidence["refs"]
        record["payload"]["evidenceOutcome"] = detail
        record["payload"]["note"] = str(error)
        record["payload"].pop("confirmation", None)
        # Invalidate a pending/approved scope so late AP delivery cannot reopen it.
        self.ap.supersede(db, record["payload"].pop("approvalId", None))
        record["payload"].pop("decisionId", None)
        record["payload"].pop("decision", None)
        Store.save(db, record)
        Store.event(db, record["id"], "CS", "EVIDENCE_BLOCKED", detail)
        self.co.state(db, record["payload"]["coordinationId"],
                      "CLARIFICATION_REQUIRED" if record["status"] == "NEEDS_INFORMATION" else "ESCALATED",
                      "EVIDENCE_BLOCKED", detail)
        return record

    def submit(self, db, actor, data):
        # Legacy HTTP failure contract rolls back on DomainError. Shared integration
        # must opt into assess() before it can expose retained failed intake views.
        return self._intake(db, actor, data, retain_failure=False)

    def assess(self, db, actor, data):
        """Service-level intake with a durable safe outcome in the caller's transaction."""
        return self._intake(db, actor, data, retain_failure=True)

    def _intake(self, db, actor, data, retain_failure):
        require_role(actor, "CUSTOMER")
        order_id = text_value(data.get("orderId"), "Order reference", 100)
        order = read_order(self.evidence, db, actor.id, order_id)
        evidence = policy_evidence(self.evidence, order)
        if not retain_failure:
            require_policy(evidence)
        needs = validated_needs(data)
        for row in db.execute("SELECT payload,status FROM records WHERE kind='CS' AND owner_id=?", (actor.id,)):
            if json.loads(row["payload"]).get("orderId") == order_id and row["status"] not in {"REJECTED", "CANCELLED", "UNRESOLVED"}:
                raise DomainError("An active or completed exchange already exists for this demo order. Open or revise that request.", 409, "DUPLICATE_REQUEST")
        payload = {"orderId": order_id, "needs": needs, "simulated": True,
                   "note": "Waiting for the Founder to initiate the authorised advice handoff."}
        rid = Store.create(db, "CS", actor.id, "ASSESSING", payload, "CS")
        co_id = self.co.create(db, actor.id, rid)
        record = Store.get(db, rid)
        record["payload"]["coordinationId"] = co_id
        try:
            policy = require_policy(evidence)
        except DomainError as error:
            return self._blocked(db, record, error, evidence)
        record["payload"]["policy"] = policy
        Store.save(db, record)
        Store.event(db, rid, "CS", "ORDER_AND_POLICY_VERIFIED", {"policyRef": policy["id"], "contextRevision": 1})
        return record

    def coordinate(self, db, actor, rid):
        require_role(actor, "FOUNDER")
        record = Store.get(db, rid, "CS")
        if record["status"] != "ASSESSING":
            return record
        try:
            _, policy = self.eligible_order(db, record["owner_id"], record["payload"]["orderId"])
            require_same_policy(policy, record["payload"]["policy"])
        except DomainError as error:
            return self._blocked(db, record, error)
        advice = self.co.advice_handoff(db, record["payload"]["coordinationId"], record["payload"]["needs"], self.advisor)
        record["payload"]["advice"] = advice
        record["status"] = "AWAITING_CONFIRMATION" if advice["status"] == "COMPLETED" else "UNRESOLVED"
        record["payload"]["note"] = "Advice handoff recorded. Awaiting current Customer confirmation." if advice["status"] == "COMPLETED" else advice["message"]
        if advice["status"] == "COMPLETED":
            record["payload"]["actionRef"] = new_id("ACT")
        Store.save(db, record)
        Store.event(db, rid, "CS", "ADVICE_RECEIVED", {"status": record["status"], "executionOccurred": False})
        return record

    def confirm(self, actor, rid, data):
        revision = revision_value(data.get("contextRevision"))
        with self.store.transaction() as db:
            record = self.owned(db, actor, rid)
            payload = record["payload"]
            if record["revision"] != revision:
                raise DomainError("The proposal changed. Review the current revision before confirming.", 409, "STALE_SCOPE")
            if record["status"] == "RESOLVED":
                return record
            if record["status"] in {"RECONCILING", "RECORDING_FAILED", "EXECUTING"}:
                raise DomainError("Query the existing action outcome; do not execute it again.", 409, "RECONCILIATION_REQUIRED")
            if record["status"] != "AWAITING_CONFIRMATION":
                raise DomainError("This request is not awaiting Customer confirmation.", 409, "INVALID_STATE")
            try:
                _, policy = self.eligible_order(db, actor.id, payload["orderId"])
                require_same_policy(policy, payload["policy"])
                product_id = payload["advice"]["product"]["id"]
                stock = read_stock(self.evidence, db, product_id)
                payload["stockObservation"] = {"productId": product_id, "availability": stock}
                if stock != "AVAILABLE":
                    raise DomainError("Replacement stock is " + stock.lower() +
                                      ". Select a supported proposal through fresh confirmation/review; no substitute was executed.",
                                      409, "STOCK_" + stock)
            except DomainError as error:
                self._blocked(db, record, error)
                blocked = error
            else:
                blocked = None
            if blocked is None:
                action = {"kind": "SIMULATED_EXCHANGE", "orderId": payload["orderId"], "productId": product_id}
                payload["confirmation"] = {"customerId": actor.id, "contextRevision": revision, "actionRef": payload["actionRef"]}
                if not payload.get("approvalId"):
                    payload["approvalId"] = self.ap.submit(db, "CS", rid, revision, action,
                        {"policyRef": policy["id"], "productEvidence": payload["advice"]["evidence"]}, payload["actionRef"])
                    record["status"] = "REVIEW_PENDING"
                    payload["note"] = "The exact proposal is awaiting a Founder decision. No business action has executed."
                    Store.save(db, record)
                    self.co.state(db, payload["coordinationId"], "AWAITING_APPROVAL", "REVIEW_PENDING", {"approvalId": payload["approvalId"]})
                    return record
                review = self.ap.get(db, payload["approvalId"])
                if not (review["decision"] == "APPROVE" and review["decision_id"]
                        and review["delivery"] == "DELIVERED" and review["revision"] == revision
                        and review["action"] == action and review["action_ref"] == payload["actionRef"]
                        and payload.get("decisionId") == review["decision_id"]):
                    raise DomainError("A committed, delivered approval for this exact action is required.", 409, "APPROVAL_REQUIRED")
                record["status"] = "EXECUTING"
                Store.save(db, record)
                Store.event(db, rid, "CS", "ACTION_INTENT_PERSISTED", {"actionRef": payload["actionRef"], "contextRevision": revision})
                self.co.state(db, payload["coordinationId"], "EXECUTING", "ACTION_DISPATCHED", {"actionRef": payload["actionRef"]})

        if blocked is not None:
            raise blocked

        # Simulated external effect commits independently; never assume a later failure rolls it back.
        try:
            result = self.port.execute_resolution(rid, payload["actionRef"], revision, product_id)
        except DomainError as error:
            with self.store.transaction() as db:
                record = Store.get(db, rid)
                self._blocked(db, record, error)
            raise
        with self.store.transaction() as db:
            record = Store.get(db, rid)
            if record["status"] == "RESOLVED":
                return record
            if Store.fault(db, "after_sales_timeout"):
                record["status"] = "RECONCILING"
                record["payload"]["note"] = "The service response timed out. The effect is unknown to CS; query the same actionRef."
                Store.save(db, record)
                self.co.state(db, payload["coordinationId"], "RECONCILING", "EXECUTION_UNCERTAIN", {"actionRef": payload["actionRef"]})
                return record
            if Store.fault(db, "outcome_recording"):
                record["status"] = "RECORDING_FAILED"
                record["payload"]["note"] = "The service returned a result, but the required outcome record failed. Recover storage without executing again."
                Store.save(db, record)
                self.co.state(db, payload["coordinationId"], "RECORDING_FAILED", "OUTCOME_SAVE_FAILED", {"actionRef": payload["actionRef"]})
                return record
            return self._record_result(db, record, result)

    def reconcile(self, actor, rid):
        with self.store.read() as db:
            record = self.owned(db, actor, rid)
            if record["status"] == "RESOLVED":
                return record
            if record["status"] not in {"RECONCILING", "RECORDING_FAILED", "EXECUTING"}:
                raise DomainError("There is no uncertain action to query.", 409, "INVALID_STATE")
            action_ref = record["payload"]["actionRef"]
        result = self.port.lookup_outcome(action_ref)
        with self.store.transaction() as db:
            record = self.owned(db, actor, rid)
            if record["status"] == "RESOLVED":
                return record
            Store.event(db, rid, "CS", "READ_ONLY_OUTCOME_LOOKUP", {"actionRef": action_ref, "found": result is not None})
            if result:
                return self._record_result(db, record, result)
            record["status"] = "UNRESOLVED"
            record["payload"]["note"] = "No confirmed service outcome was found. Escalated; no repeat execution was attempted."
            Store.save(db, record)
            self.co.state(db, record["payload"]["coordinationId"], "ESCALATED", "OUTCOME_UNRESOLVED", {"actionRef": action_ref})
            return record

    def _record_result(self, db, record, result):
        record["payload"]["result"] = result
        record["payload"]["note"] = result["remainingSteps"]
        record["status"] = "RESOLVED"
        Store.save(db, record)
        Store.event(db, record["id"], "CS", "CONFIRMED_SIMULATED_RESULT_SAVED", result)
        self.co.state(db, record["payload"]["coordinationId"], "COMPLETED", "REQUIRED_OUTCOME_SAVED", {"actionRef": result["actionRef"]})
        return record

    def revise(self, db, actor, rid, data):
        record = self.owned(db, actor, rid)
        revision = revision_value(data.get("contextRevision"))
        if revision != record["revision"]:
            raise DomainError("The proposal revision changed.", 409, "STALE_SCOPE")
        if record["status"] in {"EXECUTING", "RECONCILING", "RECORDING_FAILED", "RESOLVED", "CANCELLED"}:
            raise DomainError("This request cannot be revised before its existing effect is reconciled or after completion.", 409, "INVALID_STATE")
        needs = validated_needs(data)
        try:
            _, policy = self.eligible_order(db, actor.id, record["payload"]["orderId"])
        except DomainError as error:
            return self._blocked(db, record, error)
        self.ap.supersede(db, record["payload"].get("approvalId"))
        history = record["payload"].get("history", []) + [{"contextRevision": record["revision"], "status": record["status"], "payload": {k: v for k, v in record["payload"].items() if k != "history"}}]
        record["revision"] += 1
        record["status"] = "ASSESSING"
        record["payload"] = {"orderId": record["payload"]["orderId"], "policy": policy,
                             "coordinationId": record["payload"]["coordinationId"], "needs": needs,
                             "history": history, "simulated": True, "note": "Revised context needs a new Founder-initiated handoff and fresh review."}
        Store.save(db, record)
        self.co.state(db, record["payload"]["coordinationId"], "PENDING_VALIDATION", "CONTEXT_REVISED", {"contextRevision": record["revision"]})
        return record
