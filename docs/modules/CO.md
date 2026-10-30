# CO handoff

English is the maintained primary version. [中文阅读副本](../zh-CN/modules/CO.md).

## Maintainer review closeout · 30 October 2026

Danny explicitly authorised small fixes and reviewed integration of Guiyu Liu's
PR #17. It adds three regression tests, not new coordination implementation;
KAN-15's original work and authorship remain. Current main1ad1101 is incorporated,
the Chinese reading copy is restored, and the non-ASSESSING test uses the actual
CS terminal name RESOLVED without calling every non-ASSESSING state terminal.
The authorised Jira browser observed KAN-14 Verification / GuiyuLiu on 30 October;
retain that owner/state until the complete starter acceptance is reconciled.
Fresh tests, CI, exact-head review and merge receipts belong on PR #17; an earlier
approval is not evidence for the repaired head. No production, schema or API change.

## Current staged live read-only handoff · 29 October 2026

Danny-authorised KAN-15 exception, preserving Guiyu Liu / M5 attribution. The
existing bounded failure helpers now also serve prepare_external/finish_external:
commit one correlated SENT intent, release DB for snapshot BA inference, then
revalidate source/owner/revision/policy/current catalogue and atomically save CO
and CS outcomes. SENT is not a completion/receiver receipt. Replays do not dispatch;
new Customer revision supersedes old pending attempts; stale replies cannot apply.
The original synchronous mock advice_handoff contract remains. Live CS must use
CsFlow, not the legacy service call inside a write transaction. Audit/write failures
are explicit; interrupted SENT needs deliberate new-revision correction, no general
CO staging-recovery/queue/retry/cancellation framework. Actual live browser once-only
exchange, model-off failures and264 tests are evidenced in VERIFICATION. CO stays
PARTIAL; old generic/lifecycle gaps remain. Owner review pending, no task claim.

Default Stage 2 continuation: Guiyu Liu, at Danny's request; no shared claim is
inferred. Begin with [CO-START-01](../tasks/CO-START-01.md) and
[START_HERE](../../START_HERE.md). Complete only its declared slice first.

Stage 1 owner: Guiyu Liu. CO-M-01 / CO-UC-01 / CO-F-01..03.
Code: `beauty_company/modules/coordination.py` and CS result/reconcile integration;
new tests in `tests/test_co.py`; existing tests `test_co_t_*`, `test_gr_t_*`.
CO is a control, not an AI business agent.

Initial slice: Founder explicitly initiates CS→BA advice handoff, saved minimal
context and handoff result; coordination waits for the CS outcome. AP commitment
does not complete work. Unknown response triggers same-action lookup, failed
result saving has storage-only recovery, final completion requires saved outcome.

Current bounded failure slice (29 October 2026, Danny-authorised KAN-15,
AI-assisted): invalid context, target unavailable/timeout/failure, malformed and
independently unverifiable result now retain safe failed attempts. Minimal scope
correlates saved CS origin/current revision; same-revision replay never redispatches.
Customer correction creates a new revision; prior failed attempts remain. Valid
read-only advice does not complete the workflow. SQLite intent/result/audit failures
return truthful storage errors with caller-transaction rollback. See CONTRACTS.md
and VERIFICATION.md for 27 new CO tests / 237 full tests and actual mock browser
failure -> restart -> correction -> pending review evidence. No model needed.

Remaining: generic BA/CS/MC role adapters, independent durable external dispatch,
every cancellation/escalation/intervention/result-save recovery path and optional
bounded retry. No blind retry after uncertain execution; a read-only lookup never
grants new authority. This call remains synchronous inside the existing caller
transaction, not a durable queue/staged recovery framework. The staged path above
now supports bounded live CS intent/handoff. CO-T-02/03 stay PARTIAL; case groups retain
unverified breadth. Full UML participant/receiver and Stage 2 acceptance remain
open. Guiyu Liu attribution/task claims unchanged; affected-owner review pending.

## KAN-14 / CO-START-01 verification increment · 30 October 2026

M5 / Guiyu Liu requested this AI-assisted task continuation from main `7c86234`.
The original brief's failure-handling gap was already implemented through KAN-15;
this increment preserves that implementation and all other members' code. Added
three CO regression tests: non-ASSESSING origins cannot dispatch (CO-T-02), invalid
saved source needs cannot be overridden by valid caller needs (CO-T-02), and stock
becoming UNKNOWN invalidates previously valid advice (CO-T-04). The tests check
saved failure/no-dispatch boundaries and absence of approval or commerce effects.
All 30 CO tests pass. The initial unchanged baseline passed all 281 tests,
repository checks and JavaScript syntax checks. Actual loopback HTTP mock intake,
Founder handoff and duplicate replay returned AWAITING_CONFIRMATION, not completion.

Traceability remains PARTIAL: test_co_t_02 and test_co_t_04 include these new cases;
CO-T-01/03/08 retain their existing tests. No shared schema, module implementation,
UI, HTTP, provider, optional retry or task-claim changes are included. This is
verification of the bounded starter, not full CO/model-diagram/Stage 2 acceptance.
The original author reported Jira HTTP403 and an instruction to leave the PR
unmerged. These are historical receipts; Danny's later explicit repair/review/merge
instruction and the current observed Jira state are recorded above. Keep full
starter acceptance separate and do not automatically mark Done. Publication/CI/
exact-head review/merge must be reported separately from local checks.

Original author validation: all 284 tests passed on Python 3.12.14; repository
checks, JavaScript syntax and git diff whitespace checks also passed.
