# AP-START-01 · Durable decision intent and storage-only recovery

English is the maintained primary version. [中文阅读副本](../zh-CN/tasks/AP-START-01.md).

Owner: M4 / Jiaxuan Ren. Prepared and unclaimed. AP-M-01 / AP-UC-01 / AP-F-02.
AP is a governance control. It never performs the requesting role's action.

## Source and reading

AP-AC-02/03/04/05/06; AP-NFR-01/02/03/04. Primary target AP-T-05, with
AP-T-02/03/04/06 regressions. Read reference PDF pages 8–9, 17–18, 20, 26,
28–30, 40, 46–47, 52–53 and 58. Inspect AP-STM-01 and the sequence distinction
between commit failure and committed-decision delivery failure.

Read the current approval module, Company decision/delivery facade, record schema,
AP tests, module guide and shared-file rules.

## Current gap

Atomic audit failure currently rolls the transaction back to PENDING. There is no
durable same-decision-intent retry path or RECORDING_FAILED state machine. The
existing same-committed-decision delivery recovery solves a different problem.

## Implement this slice

Create/retain an identifiable decision intent with Founder, exact scope, kind and
reason. It is not a committed decision and cannot grant authority. A commit failure
must expose RECORDING_FAILED without delivering approval or dispatching business
work. Storage-only recovery retries the same intended decision identity/content,
revalidates Founder/current scope, and atomically commits decision/request/audit
before any delivery. Restart recovery must not depend only on an in-memory object.

Distinguish a proposed attempt from the authoritative committed envelope. A second
conflicting decision or stale revision must not overwrite the first intent/commit.
Delivery recovery continues to use the same committed decisionId and never repeats
execution. Do not invent expiry, money or risk thresholds.

## Scope and prepared shared exceptions

- Primary: `beauty_company/modules/approval.py`, new `tests/test_ap.py`, AP guide.
- `beauty_company/store.py`: additive AP decision-intent storage/migration only.
  Existing local databases must remain usable; do not alter other chain tables,
  demo users, policy fixtures or service effects.
- `beauty_company/application.py`: AP decision/recovery facade only. Failed or
  uncommitted recording cannot enter the committed-decision delivery path.
- `tests/test_workflows.py`: only the existing AP atomic-audit-failure regression
  may be adapted to assert the improved state/intended identity without weakening
  atomic rollback, no authority or no effect checks.

These narrow shared edits are included in the prepared task scope. List them in
the PR and seek relevant teammate review for integration; no external approval
is a mandatory GitHub merge gate; do not repeatedly ask permission for ordinary
local edits already covered here. New HTTP recovery controls/UI remain GR-INT-01;
do not rewrite all shared transport or web files as part of this service task.

## Observable completion conditions

- Inject failed decision recording: no committed envelope, no delivered approval,
  no business effect; RECORDING_FAILED and intended scope/identity are recoverable.
- Recreate the service/process from the same database; storage-only recovery
  commits the same intended decision, with exactly one authoritative decision/audit
  result and no duplicate business dispatch.
- Conflicting kind/reason or stale action/revision cannot be silently substituted
  during recovery. Missing current Founder authority grants no permission.
- Failed delivery preserves the already committed decision; repeated redelivery
  reuses its ID. Request receipt and pending intent remain distinct from approval.
- Existing CS/MC approval, rejection, revision, stock and duplicate-effect tests pass.

Report the tested AP-T-05 conditions and remaining queue/expiry/risk/HTTP/UI gaps.
The optional assisted-resubmission feature and actual human contribution approval
are not implemented or established by this task.
