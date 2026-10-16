"""MC-M-01: grounded mock script/storyboard with exact-revision review."""
from ..contracts import DomainError, require_role, revision_value, text_value
from ..store import Store
from .beauty_advisor import catalogue


class Marketing:
    def __init__(self, llm, media, approval):
        self.llm, self.media, self.ap = llm, media, approval

    def generate(self, db, data):
        brief = text_value(data.get("brief"), "Campaign brief")
        product = next((p for p in catalogue(db) if p["id"] == data.get("productId")), None)
        if not product:
            raise DomainError("Choose an authorised catalogue product.")
        script = self.llm.generate_script(brief, product)
        if not isinstance(script, dict):
            raise DomainError("Malformed generated output was withheld.", 409, "CONTENT_REJECTED")
        claims = script.get("claims")
        # Initial deterministic mock validation. General live generated-text checking remains unimplemented.
        if not isinstance(claims, list) or not claims or any(c not in product["facts"] for c in claims):
            raise DomainError("Unsupported generated claims were withheld.", 409, "CONTENT_REJECTED")
        return {"brief": brief, "product": product, "script": script["script"],
                "claims": claims, "media": self.media.generate(script), "simulated": True,
                "evidence": {"catalogueRef": f"catalogue:{product['id']}:v{product['version']}", "facts": product["facts"]}}

    def submit(self, db, actor, data):
        require_role(actor, "FOUNDER")
        payload = self.generate(db, data)
        rid = Store.create(db, "MC", actor.id, "DRAFTING", payload, "MC")
        record = Store.get(db, rid)
        self._review(db, record)
        return record

    def _review(self, db, record):
        record["payload"]["approvalId"] = self.ap.submit(db, "MC", record["id"], record["revision"],
            {"kind": "REVIEW_MOCK_DRAFT", "draftId": record["id"], "draftRevision": record["revision"]}, record["payload"]["evidence"])
        record["status"] = "REVIEW_PENDING"
        Store.save(db, record)
        Store.event(db, record["id"], "MC", "MOCK_DRAFT_SAVED_AND_SUBMITTED", {"contextRevision": record["revision"], "simulated": True, "videoGenerated": False})

    def revise(self, db, actor, rid, data):
        require_role(actor, "FOUNDER")
        record = Store.get(db, rid, "MC")
        if revision_value(data.get("contextRevision")) != record["revision"]:
            raise DomainError("The draft revision changed.", 409, "STALE_SCOPE")
        payload = self.generate(db, data)
        self.ap.supersede(db, record["payload"].get("approvalId"))
        payload["history"] = record["payload"].get("history", []) + [{"revision": record["revision"], "status": record["status"], "payload": {k: v for k, v in record["payload"].items() if k != "history"}}]
        record["revision"] += 1
        record["payload"] = payload
        self._review(db, record)
        return record
