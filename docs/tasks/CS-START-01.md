# CS-START-01 · Eligibility and truthful read-failure outcomes

English is the maintained primary version. [中文阅读副本](../zh-CN/tasks/CS-START-01.md).

Owner: M2 / Siyuan Lei. Prepared and unclaimed. CS-M-01 / CS-UC-01;
CS-F-01 and the evidence/failure part of CS-F-02.

## Source and reading

CS-AC-01/02/04/06; CS-NFR-01/02/03. Acceptance subsets CS-T-01/02/04/06.
Read reference PDF pages 7–8, 15–16, 19, 24, 28–30, 34, 37–38, 43–45,
49–50 and 57. Inspect CS-CL/ACT/SEQ/STM and the stated identity-before-disclosure
and current policy/stock guards. Read current CS code, simulated after-sales port,
module guide and existing CS/GR integration tests.

## Current gap

Intake accepts one always-review eligibility fixture. Missing policy/identity
conditions often exit through an exception before an observable request outcome
is retained. The complete conflicting-policy/read-failure paths are absent.

## Implement this slice

Keep identity/order verification before protected disclosure. Separate sufficient,
missing, conflicting and unavailable policy/evidence results using declared
fixtures. For an already authorised request, record a truthful unresolved or
needs-information outcome and permitted reason when storage works. An identity
mismatch remains generic; do not attach a different Customer's protected order
to the request or its model/review context.

Preserve evidence references and recheck before action. UNKNOWN and unavailable
replacement stock cannot become a successful exchange or an unconfirmed substitute.
Do not invent a return window, risk threshold or policy. Read failure causes no
execution; an uncertain write remains a different condition handled by actionRef
lookup. Use injectable module-local evidence fixtures without changing shared
provider signatures or the existing public success path.

## Scope

Own `beauty_company/modules/customer_service.py`,
`beauty_company/adapters/after_sales.py`, new `tests/test_cs.py` and
`docs/modules/CS.md`. Keep the adapter's unique actionRef and conditional stock
update. Add module-local helpers if needed. Shared schema/AP/CO/HTTP/UI changes
are not part of this first task; document required integration instead.

## Observable completion conditions

- Correct association allows permitted intake; mismatched identity discloses no
  protected order information and causes zero service effects.
- Sufficient policy retains its reference; missing/conflicting/unavailable policy
  never fabricates eligibility and has an observable safe outcome.
- Failed required reads cause no execution. AVAILABLE, UNAVAILABLE and UNKNOWN
  stock have distinct handling, and substitutions require Customer selection.
- Prior approval cannot override changed policy or stock. Current confirmation,
  exact-scope approval and actionRef behaviour remain intact.
- The existing exchange success, duplicate/concurrent confirmation, timeout lookup
  and storage-recovery regressions continue to pass unchanged.

Record the precise tested subsets in CS traceability rows and a shared integration
note if response views must expand. Do not claim full return/refund support,
notification or all CS-T-06 conditions. Those remain backlog work.

LLM handoff: read [LLM_INTEGRATION.md](../LLM_INTEGRATION.md). Danyang Wang owns
shared integration; preserve the existing module seam and supply the relevant
injected fixtures/examples. Do not deploy or build a separate provider client.
