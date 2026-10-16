"""Application values derived from Stage 1 section 8.2; HTTP is an adapter."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class DomainError(Exception):
    def __init__(self, message: str, status: int = 400, code: str = "INVALID_REQUEST"):
        super().__init__(message)
        self.status = status
        self.code = code


@dataclass(frozen=True)
class Actor:
    id: str
    role: str
    name: str


class LlmPort(Protocol):
    simulated: bool

    def propose(self, context: dict, evidence: list[dict]) -> dict: ...

    def generate_script(self, brief: str, evidence: dict) -> dict: ...


DECISIONS = {"APPROVE", "REJECT", "REQUEST_REVISION"}
DECISION_STATES = {
    "APPROVE": "APPROVED", "REJECT": "REJECTED",
    "REQUEST_REVISION": "REVISION_REQUESTED",
}


def require_role(actor: Actor, role: str) -> None:
    if actor.role != role:
        raise DomainError("This action is not permitted for this role.", 403, "FORBIDDEN")


def text_value(value: Any, label: str, maximum: int = 2000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise DomainError(f"{label} must contain 1–{maximum} characters.")
    return value.strip()


def revision_value(value: Any) -> int:
    if type(value) is not int or value < 1:
        raise DomainError("An explicit positive contextRevision is required.")
    return value
