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

Remaining: generic BA/CS/MC role adapters, target unavailability, fuller saved
context/revision correlation, every failure/cancellation/escalation path and
optional bounded retry. No blind retry after uncertain execution; a read-only
lookup never grants new authority. Model types/records are partially realised;
the complete UML participant/receiver audit has not been performed.
