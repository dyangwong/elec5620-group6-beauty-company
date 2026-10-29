"""MC-M-01: grounded text and optional template media with exact-revision review."""
from copy import deepcopy

from ..contracts import DomainError, require_role, revision_value, text_value
from ..adapters.mc_text import validate_live_script
from ..store import Store
from .beauty_advisor import catalogue


class Marketing:
    def __init__(self, llm, media, approval):
        self.llm, self.media, self.ap = llm, media, approval

    @property
    def simulated(self):
        return getattr(self.llm, "mc_simulated", True)

    @property
    def template_video(self):
        return getattr(self.media, "template_video", False) is True

    def generate(self, db, data):
        brief = text_value(data.get("brief"), "Campaign brief")
        product = next((p for p in catalogue(db) if p["id"] == data.get("productId")), None)
        if not product:
            raise DomainError("Choose an authorised catalogue product.", 409, "INCOMPLETE")

        try:
            script = self.llm.generate_script(brief, deepcopy(product))
        except (RuntimeError, TimeoutError, ConnectionError):
            raise DomainError("Marketing text generation is unavailable.", 409, "GENERATION_FAILED")

        self.validate_script(script, brief, product, self.simulated)
        storyboard = script["storyboard"]
        verified_storyboard = deepcopy(storyboard)

        try:
            # An adapter may mutate its input; it must not alter our validated text
            # or the independent snapshot used to check its actual output.
            media = self.media.generate(deepcopy(script))
        except (RuntimeError, TimeoutError, ConnectionError):
            raise DomainError("Mock media generation failed.", 409, "GENERATION_FAILED")

        if self.template_video:
            self.media.validate(media, script)
        elif not isinstance(media, dict) or media.get("kind") != "MOCK_STORYBOARD" or media.get("simulated") is not True:
            raise DomainError("Mock media result is invalid.", 409, "GENERATION_FAILED")
        if (media.get("frames") != verified_storyboard or (not self.template_video
                and media.get("label") != "Storyboard placeholder; no video file has been generated.")):
            raise DomainError("Mock media frames do not match the verified storyboard.", 409, "GENERATION_FAILED")

        return {"brief": brief, "product": product, "script": script["script"],
                "claims": script["claims"], "media": deepcopy(media), "simulated": self.simulated,
                "textSimulated": self.simulated, "mediaSimulated": not self.template_video,
                **({"textPlan": deepcopy(script["textPlan"])} if not self.simulated else {}),
                "evidence": {"catalogueRef": f"catalogue:{product['id']}:v{product['version']}", "facts": product["facts"]}}

    @staticmethod
    def validate_script(script, brief, product, simulated):
        if not simulated:
            try:
                validate_live_script(script, brief, product)
            except (ValueError, TypeError, KeyError):
                raise DomainError("Generated marketing text/captions could not be independently verified.",
                                  409, "CONTENT_REJECTED") from None

        if not isinstance(script, dict) or not isinstance(script.get("script"), str) or not script["script"].strip():
            raise DomainError("Malformed generated output was withheld.", 409, "CONTENT_REJECTED")

        claims = script.get("claims")
        if not isinstance(claims, list) or not claims or any(not isinstance(c, str) or c not in product["facts"] for c in claims):
            raise DomainError("Unsupported generated claims were withheld.", 409, "CONTENT_REJECTED")
        expected_script = f"Meet {product['name']}. " + ". ".join(product["facts"]) + "."
        if simulated and (script["script"] != expected_script or claims != product["facts"]):
            raise DomainError("Generated script does not match authorised catalogue evidence.", 409, "CONTENT_REJECTED")

        storyboard = script.get("storyboard")
        if not isinstance(storyboard, list) or not storyboard or any(not isinstance(frame, dict) for frame in storyboard):
            raise DomainError("Malformed storyboard was withheld.", 409, "CONTENT_REJECTED")
        expected_captions = [product["name"], product["facts"][0], "Explore the product details"]
        if simulated and (len(storyboard) != 3 or any(frame.get("caption") != caption for frame, caption in zip(storyboard, expected_captions))):
            raise DomainError("Storyboard contains unsupported content.", 409, "CONTENT_REJECTED")
        if simulated and any(frame.get("direction") != direction for frame, direction in zip(storyboard, ["Product introduction", "Catalogue-supported benefit", "Draft closing card"])):
            raise DomainError("Storyboard directions are not supported.", 409, "CONTENT_REJECTED")

        if simulated and any(set(frame) != {"shot", "duration", "caption", "direction"}
               or type(frame["shot"]) is not int or frame["shot"] != index
               or frame["duration"] != duration
               for index, (frame, duration) in enumerate(zip(storyboard, ["0–5 s", "5–10 s", "10–15 s"]), 1)):
            raise DomainError("Storyboard metadata is not supported by this mock fixture.", 409, "CONTENT_REJECTED")

    def validate_saved(self, db, payload, scope):
        """Recheck staged bytes/evidence without invoking either generator."""
        simulated = scope["textSimulated"]
        video = not scope["mediaSimulated"]
        expected = {"brief", "product", "script", "claims", "media", "simulated",
                    "textSimulated", "mediaSimulated", "evidence"} | ({"textPlan"} if not simulated else set())
        if (not isinstance(payload, dict) or set(payload) != expected or payload["brief"] != scope["brief"]
                or payload["simulated"] is not simulated or payload["textSimulated"] is not simulated
                or payload["mediaSimulated"] is not scope["mediaSimulated"]):
            raise DomainError("Saved generation scope or mode is invalid. Revise the draft.", 409, "INVALID_SAVED_RESULT")
        product = next((p for p in catalogue(db) if p["id"] == scope["productId"]), None)
        if (not product or product != payload["product"] or payload["evidence"] != {
                "catalogueRef": f"catalogue:{product['id']}:v{product['version']}", "facts": product["facts"]}):
            raise DomainError("Catalogue changed. Revise using current evidence.", 409, "MC_STALE_EVIDENCE")
        media = payload["media"]
        if not isinstance(media, dict):
            raise DomainError("Saved media is invalid.", 409, "INVALID_SAVED_RESULT")
        script = {"script": payload["script"], "claims": payload["claims"], "storyboard": media.get("frames"),
                  "simulated": simulated, **({"textPlan": payload["textPlan"]} if not simulated else {})}
        self.validate_script(script, scope["brief"], product, simulated)
        if video:
            if not self.template_video:
                raise DomainError("Restore the original template media configuration before recovery.",
                                  503, "MC_MEDIA_RECOVERY_UNAVAILABLE")
            self.media.validate(media, script)
        elif (media.get("kind") != "MOCK_STORYBOARD" or media.get("simulated") is not True
                or media.get("label") != "Storyboard placeholder; no video file has been generated."):
            raise DomainError("Saved mock media is invalid.", 409, "INVALID_SAVED_RESULT")

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
        live = record["payload"].get("textSimulated") is False
        video = record["payload"].get("media", {}).get("kind") == "TEMPLATE_VIDEO"
        record["payload"]["approvalId"] = self.ap.submit(db, "MC", record["id"], record["revision"],
            {"kind": "REVIEW_TEXT_DRAFT" if live else "REVIEW_MOCK_DRAFT", "draftId": record["id"],
             "draftRevision": record["revision"], **({"textMode": "LIVE", "mediaKind": "MOCK_STORYBOARD"} if live else {}),
             **({"textMode": "LIVE" if live else "MOCK", "mediaKind": "TEMPLATE_VIDEO", "mediaSha256": record["payload"]["media"]["sha256"],
                 "scriptSha256": record["payload"]["media"]["scriptSha256"]} if video else {})}, record["payload"]["evidence"])
        record["status"] = "REVIEW_PENDING"
        Store.save(db, record)
        Store.event(db, record["id"], "MC", "TEMPLATE_VIDEO_DRAFT_SAVED_AND_SUBMITTED" if video else "TEXT_DRAFT_SAVED_AND_SUBMITTED" if live else "MOCK_DRAFT_SAVED_AND_SUBMITTED",
                    {"contextRevision": record["revision"], "simulated": not live, "videoGenerated": video, "videoModelUsed": False})

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
