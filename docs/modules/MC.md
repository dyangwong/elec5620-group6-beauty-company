# MC handoff

English is the maintained primary version. [中文阅读副本](../zh-CN/modules/MC.md).

## Advert-template polish · 30 October 2026

Danny's KAN-9 visual increment replaces the optional renderer's plain text cards
with original fictional packaging/studio artwork, subtle motion and timed grounded
captions. It preserves MC ownership, text/model/evidence checks, 15s silent format,
hash-bound AP and same-artifact recovery. No audio, video model or public posting.
PNGs ship in source; no new app dependency. See beauty_company/assets/advert/README.md
and current VERIFICATION for actual Mac playback/download, three-style/three-product
renders and failed-save/restart recovery. 283 tests passed; Windows/live-model/final
ZIP/Canvas and general creative/visual quality remain pending.


## MC generation recovery checkpoint · 29 October 2026

Danny explicitly authorised MC generation persistence/recovery/cancellation under
KAN-15, preserving Zhengdu Wei's original work and claims. New module-local
mc_generation.py orchestrates the existing Marketing validation/review; AP business
rules, schema, BA/CS/CO and model transport/config remain unchanged. Shared facade,
HTTP and UI changes are recorded in SHARED_FILES.md; affected-owner review pending.

GENERATING -> durable server outcome -> independent current evidence/file recheck
-> atomic draft/REVIEW_PENDING receipt. Final failure is RECORDING_FAILED when
recordable. Recovery resumes this same saved generation without text/render calls;
no saved outcome requires explicit retry/new revision. Current review/decision is
never inherited or replaced by generation retry. Cancel advances revision and
suppresses late output; it does not promise physical GPU/render abort. No publication.

210 full tests passed, including 57 MC tests; actual mock SQLite failure/
restart/recovery/no-draft retry/cancel and real MC model-off restart/same-MP4 recovery
passed. All browser reviews remained pending or superseded, with zero effects and
unchanged stock. See VERIFICATION.md, CONTRACTS.md and WINDOWS_LLM.md for exact
evidence/commands. Earlier below “no MC recovery UI” statements are historical.

**MC-T-06 remains PARTIAL.** This is generation-save recovery, not every possible
MC local decision-save/approval-delivery recovery. No partial generation/render
checkpointing, orphan cleanup, unrestricted prose, AI scenes/audio, wider media
quality, current-source ZIP/other-machine/venue or complete MC/Stage 2 acceptance.


## MC template MP4 checkpoint · 29 October 2026

This Danny-authorised KAN-15 increment adds MC-F-02 template media, preserving
Zhengdu Wei's original module work/ownership. Current pipeline: validated mock or
real text -> optional CPU template MP4 -> metadata/full decode/hash checks -> save
current draft -> existing AP bound to exact file/script hash -> internal preview.
Default MockMedia is unchanged. No second model, scene generation, photography,
audio, publishing, optional MC-F-03 variants, general quality evaluator or full
recovery/cancellation is implemented. Camera directions are displayed as text,
not executed. Visual sampling covers the current fictional catalogue only.

MC-T-04/05/06 remain PARTIAL: actual Windows file/playback/download and exact-scope
review, unavailable tools, timeout/process/format failures and artifact tampering
are covered to the documented extent. Missing artifact access fails safely;
generation/final-save recovery and wider media/semantic/quality acceptance remain.
Files from stale or failed work may remain ignored; they cannot be downloaded via
a current record URL. Failed final DB save can retain DRAFTING without review.
Reviewers must assess both text and the actual preview, not just presence of a hash.
See WINDOWS_LLM.md for setup; VERIFICATION.md for new and historical evidence.


## MC bounded live-text checkpoint · 29 October 2026

Danny explicitly authorised this shared-model increment; original Zhengdu Wei
KAN-12 service work and task ownership are retained. It adds no video or new AP
business rules. Shared-file changes are recorded in SHARED_FILES.md; review pending.

Founder brief + authorised product -> real shared-model bounded plan -> independently
grounded catalogue-literal script/three-shot storyboard -> mock media placeholder
-> saved current revision -> existing AP review. The model chooses fact selection/
order, featured caption and CALM/ENERGETIC/INFORMATIVE style. It does not generate
unrestricted marketing prose; style relevance still needs Founder judgement.
Default mock and BA-only Strata remain unchanged; enable live MC explicitly.

Actual Windows browser calm -> REQUEST_REVISION -> energetic new script -> fresh
APPROVE passed. Original review became SUPERSEDED. Model-off new creation retained
GENERATION_FAILED/LLM_UNAVAILABLE with no output/review/fallback. 181 full tests
(28 MC tests) passed, including timeout/invalid output, actual-field tampering,
independent evidence, current catalogue, concurrent revisions and final-save rollback.
See VERIFICATION.md for concrete records/environment and reproduction.

Stop here for this increment. **Storyboard is not video.** Media output and quality,
full failure/recovery/cancellation lifecycle, broader brief interpretation and all
Stage 1 MC acceptance conditions remain open. If final generation-save fails,
DRAFTING may remain without output/review; no MC recovery UI is claimed. Existing
AP decision recovery is a separate capability. English live examples alone do not
establish multilingual/creative/medical safety or complete MC acceptance.

The following earlier mock-only handoff/progress sections are historical.



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

## Danny-authorised repair and integration · 27 October 2026

The original KAN-12 implementation by Zhengdu Wei is retained. At Danny's explicit request, the original PR #11 was brought up to main dc1b60b (merged AP #12) and repaired with AI assistance. This does not reassign the starter or claim the teammate's endorsement.

Failed revisions now render as failed records in Content studio, with their permitted reason, no fabricated product/media/approval, and a corrected-draft form using productId. The review queue also handles failed current payloads and shows that a superseded review cannot approve a different current revision. Existing HTTP creation still calls submit; submit_draft remains a service entry point. No live model or video generation is added.

Model evidence and media inputs are deep copies; media frames are checked against an independent verified storyboard snapshot, rather than a mutable alias. Shot/duration metadata and the mock-media label are bounded to the declared fixture. A mutating adapter cannot introduce unsupported captions or alter the saved script/claims by changing its input. This remains deterministic mock validation, not unrestricted prose grounding.

The full integrated suite passed 112 tests, including the original 11 MC tests and five new regressions for adapter/evidence mutation, metadata and the actual failed HTTP revision contract. Actual browser creation followed by a whitespace-only revision saved INCOMPLETE/revision 2; both Content studio and the old SUPERSEDED review rendered without crashing. Initial revision history and old review are retained. Remote CI and actual review/merge are recorded on PR #11 separately.
