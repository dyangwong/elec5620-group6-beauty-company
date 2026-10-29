# AP handoff

English is the maintained primary version. [中文阅读副本](../zh-CN/modules/AP.md).

Default Stage 2 continuation: Jiaxuan Ren, at Danny's request; no shared claim is
inferred. Begin with [AP-START-01](../tasks/AP-START-01.md), including its narrow
shared-file exceptions, and [START_HERE](../../START_HERE.md).

Stage 1 owner: Jiaxuan Ren. AP-M-01 / AP-UC-01 / AP-F-01..03.
Code: `beauty_company/modules/approval.py`, `beauty_company/application.py`
decision/delivery boundary; new tests in `tests/test_ap.py` and existing tests
`test_ap_t_*`. AP is a shared control, not an AI business agent.

Initial slice: CS/MC exact action/revision evidence; persisted PENDING receipt;
Founder-only APPROVE/REJECT/REQUEST_REVISION with reason; decision/request/audit
one commit; delivery separate. Duplicate delivery retains one decisionId. Stale
scope cannot alter current work. Receiving services retain independent checks.

## BA conditional review checkpoint · 30 October 2026

Danny authorised this KAN-15 shared exception, preserving Jiaxuan Ren / M4 AP
attribution and KAN-13/starter ownership. AP accepts the new BA REASSESS_ADVICE
origin using existing tables/intent/decide/recover/deliver. A module-local BA receiver
checks current consented exact scope/evidence; it never calls a model or business
effect. Approved BA returns for Customer confirmation/fresh validation, rejection
stays incomplete and revision requests require correction. Existing CS/MC mapping
and AP decision-save recovery remain; full 281-test regression passed. Affected-owner
human review remains pending, not inferred from this authorised integration/CI.
See CONTRACTS/VERIFICATION and BA guide. Unknown-risk classification/expiry/queue/
notifications and full AP acceptance remain separate.

## Recording failure and recovery · KAN-13 / AP-START-01 · 24 October 2026

A **decision intent** is a durable, identifiable proposal to decide. It holds the
Founder, the exact scope (origin, revision, action, actionRef), the kind and the
reason. It is not a committed decision: it grants no authority, delivers nothing
and dispatches no business work. It is written in its own committed transaction
before the decision commit, so a failed commit leaves it recoverable from storage.

- **Failed commit → `RECORDING_FAILED`.** The approval keeps no decision id,
  decision, reason or founder, so it is not an approval. Nothing is delivered and
  no business work is dispatched. The intended identity stays in the intent.
- **Storage-only recovery.** `Company.recover_decision` reads the intent from the
  database, revalidates the Founder and the current scope, then commits
  decision/request/audit atomically before any delivery. A restarted process over
  the same database recovers the same intended decision exactly once.
- **One authoritative decision per request.** A second conflicting kind or reason
  is refused (`DECISION_CONFLICT`) and never replaces the first intent or commit.
  A stale action, revision or superseded request is refused (`STALE_SCOPE` /
  `REVIEW_CLOSED`) and is never silently substituted during recovery.
- **Receipt, intent and approval stay distinct.** A `PENDING` receipt, a proposed
  intent and a committed approval are three different things; only the committed
  envelope has a decisionId.

Shared-file exceptions used by this slice: an additive `approval_intents` table
in `beauty_company/store.py`, the decision/recovery facade and the intent field in
`beauty_company/application.py`, and the existing AP atomic-audit-failure
regression in `tests/test_workflows.py`.

Remaining: full risk/authority classification, BA/CO local adapter mappings,
unknown risk, expiry, notification, cancellation, queue failure and the optional
linked resubmission. The original service slice left HTTP/UI recovery to GR-INT-01; the bounded
26 October integration below closes that transport/view gap. Recording failure
remains an injected local fixture, not a real provider outage.
Never execute an exchange, settlement or publication from approval code.

## HTTP/UI recording recovery · KAN-9 / GR-INT-01 · 26 October 2026

Danny authorised this shared integration separately from Jiaxuan's AP starter.
`POST /api/approvals/{id}/recover` takes only the displayed contextRevision,
rechecks current scope and calls the existing storage-only recovery facade.
Original Founder/session/CSRF checks apply; decision, reason, identity and action
are never accepted from this request. The optional facade data argument preserves
existing two-argument service callers. No schema or approval-module change.

The failed review card now names the actual recording failure, displays the saved
kind/reason as an intention without authority, and offers Recover saved decision
only to its original Founder for a current linked origin. Failed decide/recover
refreshes saved state, so the card appears immediately. The Founder simulation
menu includes approval_recording. After recovery, show the actual committed ID and
delivery status; a failed delivery retains the existing separate redelivery button.
No exchange, settlement or publication is dispatched by recovery.

Twelve new Router/session/SQLite tests in tests/test_ap_http.py cover authority,
CSRF, input tampering, current/stale/action scope, repeated recording failure,
restart, all three saved decision kinds, once-only commit and separate delivery.
Actual browser save-failure/recovery passed; independent DB readback found one
committed audit, zero effects and unchanged stock. See VERIFICATION.md.
AP-T-05 stays PARTIAL: queue/notification, expiry, full risk routing and real
storage-outage acceptance remain open. Publication, affected-owner review and
Jira progress update are pending; this is not full AP or epic acceptance.
