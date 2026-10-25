# MC handoff

English is the maintained primary version. [中文阅读副本](../zh-CN/modules/MC.md).

Default Stage 2 continuation: Zhengdu Wei, at Danny's request; no shared claim is
inferred. Begin with [MC-START-01](../tasks/MC-START-01.md) and
[START_HERE](../../START_HERE.md). Complete only its declared slice first.

Stage 1 owner: Zhengdu Wei. MC-M-01 / MC-UC-01 / MC-F-01..03.
Code: `beauty_company/modules/marketing.py`, `beauty_company/adapters/mock.py`;
new tests in `tests/test_mc.py`; existing tests `test_mc_t_*`.

Initial slice: Founder brief and authorised product; deterministic facts-only mock
script plus storyboard; labelled placeholder media; saved exact revision before
review receipt; committed/delivered decision establishes the local reviewed status.
Changed draft creates fresh review and preserves history. Nothing publishes.

Remaining: real brief interpretation, complete output-claim checking, generated
video/labelled fallback assets, media failure/quality lifecycle, failed-save
recovery, cancellation/stale callbacks and optional variants. A three-card
storyboard placeholder must not be reported as generated video. An approval here
is scoped to the current mock draft, not permission to post it externally.


## MC-START-01 / KAN-12 Implementation Progress

### Implemented Service-Level Features

- Added controlled failure classification for incomplete inputs, rejected content and failed mock generation.
- Added `submit_draft()` to retain failed campaign drafts without submitting them for approval.
- Added revision handling that preserves previous draft states and failure information.
- Prevented stale revisions from overwriting current campaign records.
- Superseded previous approval requests when a new draft revision was created.
- Added deterministic validation of mock scripts, storyboard content and returned media frames.
- Restricted campaign creation and revision to authorised Founder operations.

### Verification

The local Python unittest suite passed 49 tests, including 11 MC-specific tests.

The tested scenarios include failed draft persistence, media failures, failed revisions, stale revision protection, approval supersession, unsupported promotional claims, storyboard validation, media frame consistency and role enforcement.

### Known Limitations

- The content checks use deterministic mock templates and do not provide general natural-language claim verification.
- `submit_draft()` is a service-level entry point and has not been integrated into the existing HTTP/UI workflow.
- Real video generation and external media deployment are not implemented.
- Database recording failures and complete recovery procedures remain outside the verified scope.
- Full Stage 1 acceptance and production readiness are not claimed.

### Remaining Integration Work

- Coordinate the service-level failure results with the shared application and HTTP interfaces.
- Complete wider recovery and failure-path verification.
- Review the MC changes against the shared LLM integration contract.
- Confirm the final task acceptance conditions before marking KAN-12 Done.
