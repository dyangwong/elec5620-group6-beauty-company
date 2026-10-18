# MC-START-01 · Persist mock-generation failure and revision states

English is the maintained primary version. [中文阅读副本](../zh-CN/tasks/MC-START-01.md).

Owner: M3 / Zhengdu Wei. Prepared and unclaimed. MC-M-01 / MC-UC-01;
MC-F-01/02, not the optional variant feature.

## Source and reading

MC-AC-02/04/05/06; MC-NFR-01/02/03/04. Acceptance subsets MC-T-02..06.
Read reference PDF pages 8, 12, 16–17, 25, 28–30, 35, 39, 45–46, 51–52
and 57–58. Inspect MC-STM-01 and its transition table, not just the state names.
Read the MC guide, current marketing service and mock-provider contracts/tests.

## Current gap

Most invalid input/output is rejected before a durable campaign/failure outcome
exists. Successful mocks produce only storyboard placeholders; the full
INCOMPLETE/CONTENT_REJECTED/GENERATION_FAILED/revision lifecycle is missing.

## Implement this slice

At service level, retain an authorised campaign identity and source revision;
distinguish missing/conflicting source information, malformed/unsupported model
output, failed content checks and unavailable/failed mock media. Persist the actual
safe state/reason/evidence when storage works, without implying generation or
review succeeded. Only a saved current draft that passes the declared checks may
be submitted to AP. Withhold failed output; a model's list of its own claims is
not sufficient verification of arbitrary script/storyboard content.

Add controlled fake providers in the new MC test file (or module-local helpers),
preserving the current successful adapter signatures. Authorised correction creates
the correct new revision and repeats evidence/checks before fresh review; keep
old evidence/decisions historically, without inheriting approval. Tests may use
simple bounded evidence-linked content; do not claim general semantic validation
or introduce an unagreed numerical quality threshold.

## Scope

Own `beauty_company/modules/marketing.py`, new `tests/test_mc.py` and
`docs/modules/MC.md`. Do not edit shared `adapters/mock.py`, AP decisions,
schema, HTTP or the shared frontend in this first task. Keep normal success
responses compatible. Record explicit shared follow-up before exposing new failure
payloads to the existing browser renderer, which assumes a saved product/media.

## Observable completion conditions

- Missing/contradictory required facts cannot produce an approval-ready draft.
- Malformed output, invented product facts and failed content checks are visibly
  withheld with the corresponding retained failure/revision state where possible.
- Media unavailability/failure never becomes real generation success. Any fallback
  is explicitly simulated; no actual video file is claimed by this task.
- No failed draft creates an AP approval-ready success. Corrected input repeats
  the relevant checks and receives fresh exact-revision review.
- Existing successful mock drafting, approval and fresh-revision regressions pass.
- Service-only tests and pending HTTP/UI integration are reported separately.

Leave real model/media deployment, actual video generation, optional variants and
full review-decision-save recovery in the backlog. No external model download,
credentials, posting or payment is part of this task.

LLM handoff: read [LLM_INTEGRATION.md](../LLM_INTEGRATION.md). Danyang Wang owns
shared integration; preserve the existing module seam and supply the relevant
injected fixtures/examples. Do not deploy or build a separate provider client.
