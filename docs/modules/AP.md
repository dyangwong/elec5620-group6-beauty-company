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

Remaining: full risk/authority classification, BA/CO local adapter mappings,
unknown risk, expiry, notification, cancellation, RECORDING_FAILED lifecycle and
durable same-decision storage-intent retry, optional linked resubmission. The local
atomic rollback test covers only part of recording failure, not all AP-T-05.
Never execute an exchange, settlement or publication from approval code.
