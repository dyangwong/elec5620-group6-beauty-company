# CO handoff

English is the maintained primary version. [中文阅读副本](../zh-CN/modules/CO.md).

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
transaction, not a durable queue/staged recovery framework. Real CS intent/handoff
remains unconnected/blocked. CO-T-02/03 now PARTIAL; all relevant case groups retain
unverified breadth. Full UML participant/receiver and Stage 2 acceptance remain
open. Guiyu Liu attribution/task claims unchanged; affected-owner review pending.
