# CS handoff

English is the maintained primary version. [中文阅读副本](../zh-CN/modules/CS.md).

Stage 1 owner: Siyuan Lei (M2). CS-M-01 / CS-UC-01 / CS-F-01..03.
Task: [CS-START-01](../tasks/CS-START-01.md) / KAN-11.
Implementation prepared with Codex assistance on 18 October 2026; review, merge
and Jira acceptance remain separate. Jira was observed assigned to Siyuan Lei,
To Do; no Jira transition or shared claim was applied by this implementation.

Code: `beauty_company/modules/customer_service.py`, module-local
`beauty_company/modules/cs_evidence.py`, `beauty_company/adapters/after_sales.py`.
Tests: `tests/test_cs.py`; existing `test_cs_t_*`, `test_gr_t_*` and recovery
regressions in `tests/test_workflows.py` remain unchanged.

## Implemented service slice

The original success path remains: owning Customer exchange intake, explicit
synthetic policy, Founder starts BA through CO, Customer confirms the exact
revision, AP reviews, then Customer reconfirms and execution occurs once.
An approval does not create eligibility or stock. Effects commit independently
before receipt storage; uncertain effects use the existing actionRef lookup.
All business responses remain mocks. No payment, refund, shipment or publication.

`CustomerService.assess(db, actor, data)` is the new service-level intake entry
for retained evidence failures. The caller commits its transaction on returned
NEEDS_INFORMATION/UNRESOLVED results. Initial identity/order mismatch or unavailable
verification still raises a generic DomainError, creates no request and performs
no policy/model/review read. Once association is verified, assessment retains:

| Evidence | Request outcome | Guard/effect |
|---|---|---|
| SUFFICIENT | ASSESSING | Keep the exact policy and reference; permit Founder handoff |
| MISSING | NEEDS_INFORMATION | Save permitted reason/references; no inferred return window |
| CONFLICTING / UNSUPPORTED | UNRESOLVED | Save reason/references; no eligibility or review/execution |
| UNAVAILABLE policy read | UNRESOLVED | Save safe reason; withhold provider diagnostics |

These are subsets of CS-CL-01, CS-ACT-01, CS-SEQ-01 and CS-STM-01, visually
inspected on physical report pages 24, 37-38, 43-45 and 50. Existing declared
NEEDS_INFORMATION/UNRESOLVED states are reused; no new RequestState is invented.

`ExchangeEvidence` is injectable only within CS/its simulated after-sales adapter.
Its default order read uses both customer and order IDs before policy evaluation.
The seeded policy is unchanged. Controlled evidence fixtures may omit required
fields, set `missingFields: ["returnWindow"]`, or supply `conflictingRefs` with
conflicting authorised policy references. Malformed JSON is conflicting evidence;
false eligibility or an unsupported order state stops automation. None of these
fixtures establishes a real return window, threshold or replacement policy.
Inject read errors via the reader's order/policy/stock methods, not request JSON.
SQLite read errors, timeouts and connection failures become safe unavailable
outcomes; storage-write errors propagate and cannot claim a retained result.

Handoff, revision and confirmation recheck association and policy. Confirmation
records AVAILABLE/UNAVAILABLE/UNKNOWN stock distinctly. A required read failure,
changed policy or non-available stock saves the safe outcome, clears confirmation,
supersedes/detaches the old review and prevents late delivery reopening that scope.
Confirmation commits this result before raising its DomainError. Revisions require
new Founder handoff, actionRef, Customer confirmation and exact-scope AP review.
No automatic substitute is selected or executed: supported changes go through
Customer revision/selection and fresh review; a general alternatives UI is pending.
The adapter rechecks association, policy, selected scope and stock inside its
effect transaction, retaining the unique actionRef and conditional stock decrement.
A replay of an existing effect returns the same receipt without another decrement.

## Shared integration handoff and compatibility

At the human's explicit instruction, **all shared regression tests are unchanged**.
The legacy `submit(db, actor, data)` entry and current HTTP intake preserve their
policy-failure DomainError/rollback contract. They share the same validation and
success implementation with assess, but do not retain failed initial intake.
This distinction is deliberate and tested; it is not a claim that the browser
already exposes the new assessment workflow.

A later bounded HTTP/UI integration must route intake to assess, render failed
records without assuming `payload.policy` or advice exists, and offer corrected
needs/reassessment rather than showing success. Confirm errors require a snapshot
refresh to show the already-saved status. Review affected callers/tests together
with the shared integration owner before switching the default entry. No schema,
AP/CO implementation, shared provider signature, HTTP or UI changes are included.

## Verification and remaining scope

`python -m unittest discover -s tests -v` covers the original 38 regressions plus
22 CS tests: association before disclosure, sufficient/missing/conflicting/invalid
policy, safe policy/order/stock read failures, corrected-evidence revision, changed
policy after approval, late review delivery, all three stock observations,
post-intent evidence races, replay conflicts and failed outcome writes.
Existing success, concurrent/duplicate confirmation, post-write timeout and
storage-only recovery regressions run unchanged. Use docs/traceability.csv for
partial CS-T-01/02/04/06 coverage; full cases are not marked passed.

Remaining: default HTTP/UI retained intake integration, routine returns/refunds,
full policy/verification-service matrices, general alternatives, cancellation,
optional authorised notifications, every persistence/audit/provider failure,
real provider idempotency and complete model consistency. Model deployment is
reserved to Danyang Wang under [LLM_INTEGRATION](../LLM_INTEGRATION.md).
For future CS intent: “exchange my item” needs an order reference and verified
association; missing policy requires clarification; “use another customer's order”
must yield generic correction/support. Intent output cannot supply trusted identity,
approval, stock or execution authority. No independent CS model client was added.

## Shared HTTP/UI integration · GR-INT-01 · 27 October 2026

Danny explicitly authorised switching the HTTP receiver to assess and adding safe
failure rendering/reassessment. This supersedes the earlier current-HTTP rollback
handoff above; service submit itself and all member tests remain unchanged.
Missing policy is saved as NEEDS_INFORMATION; conflicting/unsupported/unavailable
policy is saved as UNRESOLVED after identity association. The view shows safe
reason/reference and no old advice/current confirmation when evidence is blocked.
It directs the Customer to reassess the existing request after authorised evidence
refresh, preserving history and requiring fresh handoff/confirmation/review.
No new policy editor, fixture endpoint, service signature, model or schema change.

Eleven new HTTP/session/SQLite tests cover retained outcomes/restart/ownership,
initial verification denial, policy read failure sanitisation, forged policy,
evidence refresh/still-blocked reassessment, saved confirmation error and storage
rollback. The complete branch passes 107 offline tests, plus source/JS checks.
Actual Customer browser intake persisted NEEDS_INFORMATION; server fixture refresh
then browser reassessment produced revision 2/ASSESSING. A controlled existing
Founder service handoff followed by another missing-policy fixture caused actual
browser confirmation HTTP 409 and immediately displayed the saved blocked result.
Independent readback found one CS record, no approvals/effects and stock 12.
All are mock policy/business fixtures. CS-T-01/02/06 stay PARTIAL; routine refunds,
full cancellation, real CS intent and the wider failure matrix remain open.
Remote CI/review/merge and current Jira progress are recorded on the integration PR.
