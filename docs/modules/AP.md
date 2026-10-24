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
linked resubmission. The HTTP/UI recovery control and demo fixture for the
recording failure are GR-INT-01 shared integration, not part of this slice.
Observed pending items for that integration: the backend accepts the
`approval_recording` fault but the demo dropdown does not offer it yet; the
review card has no recovery control for a `RECORDING_FAILED` request; and its
non-PENDING fallback text ("This review was superseded by a changed context.")
is inaccurate for a failed recording, although the card still reports
"No applicable committed decision" and renders the failed badge. The recording
failure is an injected local fixture, not a real provider outage.
Never execute an exchange, settlement or publication from approval code.
