# BA-START-01 · Consultation revision and cancellation

English is the maintained primary version. [中文阅读副本](../zh-CN/tasks/BA-START-01.md).

Owner: M1 / Danyang Wang. Prepared and unclaimed; no work or approval is inferred.
This is the first bounded task, not an instruction to implement the entire BA chain.

## Source and reading

BA-M-01; BA-F-01/02; BA-UC-01 A1/A4/E3/E5; BA-AC-01/04/06;
BA-NFR-02/03/04. Acceptance subsets: BA-T-01, BA-T-04, BA-T-07.
Read the reference PDF pages 7, 13–15, 23, 28–30, 36, 42–43, 48–49, 56–57.
Inspect BA-CL-01, BA-ACT-01, BA-SEQ-01 and BA-STM-01, including its
event/guard/effect panel. Page numbers refer to the complete PDF in this repo.

Read AGENTS, current status/contracts, `docs/modules/BA.md`, current BA code and
the existing `test_ba_t_*` conditions in `tests/test_workflows.py`.

## Current gap

Each submit currently creates a new record. CLARIFYING has no proper resumption;
there are no BA revise/cancel operations or protection against a result from an
older consultation revision. Invalid model output has selected mock checks only.

## Implement this slice

Add explicit service-level resumption/revision/cancellation using the same owned
consultation identity and the Stage 1 vocabulary. Retain revision/evidence history;
corrections invalidate the former applicable advice. An asynchronous result or
delayed test fixture must prove it belongs to the current uncancelled revision
before being saved/delivered. A cancelled session requires a fresh session.

Do not turn a stale or failed-save result into COMPLETED. Preserve the actual
failure when storage is unavailable. Do not execute any commerce action. Use
deterministic fixtures for delayed/invalid/failed output; no real model is needed.
Document service signatures and the existing submit/recommend compatibility.

## Scope

Own files: `beauty_company/modules/beauty_advisor.py`, new `tests/test_ba.py`,
`docs/modules/BA.md`. Use existing generic record persistence. Do not modify the
shared LlmPort, shared mock adapter, catalogue consumers, schema, HTTP or web files
in this first task. Record any additional integration surface in the PR rather
than silently altering the other chains. Only BA rows of traceability are yours.

## Observable completion conditions

- A missing required need stays CLARIFYING without a guessed value; an authorised
  answer resumes the same consultation and rechecks evidence.
- A correction increments the context revision; the former recommendation is
  retained historically but cannot be returned as the current recommendation.
- A late old-revision output is ignored, and cancellation suppresses later output.
- Cancellation and result-save failure cannot claim successful advice delivery.
- Another Customer cannot revise/cancel the consultation; minimum model/review
  payloads exclude unrelated Customer data and credentials.
- Existing grounded-advice and integrated exchange tests still pass; no order,
  stock, payment, refund or publication effect is introduced.

Run the full existing suite and the new BA tests. Update exact tested conditions,
remaining BA-T-07 branches and pending HTTP/UI wiring. Do not mark an entire case
passed for a service-only subset. BA review and optional alternatives remain later
work. Shared UI integration is GR-INT-01 in the backlog.
