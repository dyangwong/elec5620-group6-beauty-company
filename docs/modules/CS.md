# CS handoff

English is the maintained primary version. [中文阅读副本](../zh-CN/modules/CS.md).

Default Stage 2 continuation: Siyuan Lei, at Danny's request; no shared claim is
inferred. Begin with [CS-START-01](../tasks/CS-START-01.md) and
[START_HERE](../../START_HERE.md). Complete only its declared slice first.

Stage 1 owner: Siyuan Lei. CS-M-01 / CS-UC-01 / CS-F-01..03.
Code: `beauty_company/modules/customer_service.py`,
`beauty_company/adapters/after_sales.py`; new tests in `tests/test_cs.py`;
existing tests `test_cs_t_*`,
`test_gr_t_*`. Preserve actual request states declared in source section 8.2.2.

Initial slice: owning Customer exchange request, explicit policy fixture, Founder
starts BA handoff through CO, Customer confirms exact revision, AP reviews, then
Customer reconfirms and service executes once. The effect commits before local
receipt saving. Query actionRef after uncertainty; storage recovery never executes.
Approval cannot create eligibility or stock. Every outcome is simulated and lists
remaining physical obligations. One active/completed exchange per demo order.

Remaining: routine return/refund paths, full policy conflict/clarification,
cancellation, optional authorised notification, all persistence/provider failures,
real commerce contracts and complete model consistency. No real financial service
may be connected without an explicit approved scope and appropriate controls.
