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
            raise DomainError("Choose an authorised catalogue product.", 409, "INCOMPLETE")

        try:
            script = self.llm.generate_script(brief, product)
        except (RuntimeError, TimeoutError, ConnectionError):
            raise DomainError("Marketing text generation is unavailable.", 409, "GENERATION_FAILED")

        if not isinstance(script, dict) or not isinstance(script.get("script"), str) or not script["script"].strip():
            raise DomainError("Malformed generated output was withheld.", 409, "CONTENT_REJECTED")

        claims = script.get("claims")
        if not isinstance(claims, list) or not claims or any(not isinstance(c, str) or c not in product["facts"] for c in claims):
            raise DomainError("Unsupported generated claims were withheld.", 409, "CONTENT_REJECTED")
        expected_script = f"Meet {product['name']}. " + ". ".join(product["facts"]) + "."
        if script["script"] != expected_script or claims != product["facts"]:
            raise DomainError("Generated script does not match authorised catalogue evidence.", 409, "CONTENT_REJECTED")

        storyboard = script.get("storyboard")
        if not isinstance(storyboard, list) or not storyboard or any(not isinstance(frame, dict) for frame in storyboard):
            raise DomainError("Malformed storyboard was withheld.", 409, "CONTENT_REJECTED")
        expected_captions = [product["name"], product["facts"][0], "Explore the product details"]
        if len(storyboard) != 3 or any(frame.get("caption") != caption for frame, caption in zip(storyboard, expected_captions)):
            raise DomainError("Storyboard contains unsupported content.", 409, "CONTENT_REJECTED")
        if any(frame.get("direction") != direction for frame, direction in zip(storyboard, ["Product introduction", "Catalogue-supported benefit", "Draft closing card"])):
            raise DomainError("Storyboard directions are not supported.", 409, "CONTENT_REJECTED")

        try:
            media = self.media.generate(script)
        except (RuntimeError, TimeoutError, ConnectionError):
            raise DomainError("Mock media generation failed.", 409, "GENERATION_FAILED")

        if not isinstance(media, dict) or media.get("kind") != "MOCK_STORYBOARD" or media.get("simulated") is not True:
            raise DomainError("Mock media result is invalid.", 409, "GENERATION_FAILED")
        if media.get("frames") != storyboard:
            raise DomainError("Mock media frames do not match the verified storyboard.", 409, "GENERATION_FAILED")

        return {"brief": brief, "product": product, "script": script["script"],
                "claims": claims, "media": media, "simulated": True,
                "evidence": {"catalogueRef": f"catalogue:{product['id']}:v{product['version']}", "facts": product["facts"]}}

    def submit(self, db, actor, data):
        require_role(actor, "FOUNDER")
        payload = self.generate(db, data)
        rid = Store.create(db, "MC", actor.id, "DRAFTING", payload, "MC")
        record = Store.get(db, rid)
        self._review(db, record)
        return record
    def submit_draft(self, db, actor, data):
        require_role(actor, "FOUNDER")
        rid = Store.create(db, "MC", actor.id, "DRAFTING", {"brief": data.get("brief"), "productId": data.get("productId"), "simulated": True}, "MC")
        record = Store.get(db, rid)
        try:
            payload = self.generate(db, data)
        except DomainError as error:
            record["status"] = error.code if error.code in {"INCOMPLETE", "CONTENT_REJECTED", "GENERATION_FAILED"} else "INCOMPLETE"
            record["payload"]["failure"] = {"code": error.code, "reason": str(error)}
            Store.save(db, record)
            Store.event(db, rid, "MC", "DRAFT_GENERATION_FAILED", {"status": record["status"], "code": error.code})
            return record
        record["payload"] = payload
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
        if record["owner_id"] != actor.id:
            raise DomainError("Only the campaign owner may revise this draft.", 403, "FORBIDDEN")
        if revision_value(data.get("contextRevision")) != record["revision"]:
            raise DomainError("The draft revision changed.", 409, "STALE_SCOPE")
        previous = {"revision": record["revision"], "status": record["status"], "payload": {k: v for k, v in record["payload"].items() if k != "history"}}
        history = record["payload"].get("history", []) + [previous]
        try:
            payload = self.generate(db, data)
        except DomainError as error:
            payload = {"brief": data.get("brief"), "productId": data.get("productId"), "simulated": True,
                       "failure": {"code": error.code, "reason": str(error)}}
            status = error.code if error.code in {"INCOMPLETE", "CONTENT_REJECTED", "GENERATION_FAILED"} else "INCOMPLETE"
        else:
            status = "DRAFTING"
        self.ap.supersede(db, record["payload"].get("approvalId"))
        record["revision"] += 1
        payload["history"] = history
        record["payload"] = payload
        if status == "DRAFTING":
            self._review(db, record)
        else:
            record["status"] = status
            Store.save(db, record)
            Store.event(db, rid, "MC", "DRAFT_REVISION_FAILED", {"contextRevision": record["revision"], "status": status})
        return record