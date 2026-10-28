# Shared contracts and implementation map

English is the maintained primary version. [中文阅读副本](zh-CN/CONTRACTS.md).

## MC bounded live-text checkpoint · 29 October 2026

Additive, explicitly opted-in MC live route; default mock callers retain their
existing paths. Founder session/CSRF and owner guards apply.

| POST | Exact body | Result |
|---|---|---|
| `/api/campaigns` | `brief`, `productId` | 201 with persisted MC draft/failure record |
| `/api/campaigns/{id}/revise` | `brief`, `productId`, positive integer `contextRevision` | 200, same ID/new revision; old review superseded, history preserved; stale scope 409 |

No caller-supplied mode, result or approval fields. Success payload includes
script/claims/product/evidence, textPlan, simulated=false, textSimulated=false,
mediaSimulated=true and labelled mock media. Exact three-shot composition is
described in LLM_INTEGRATION.md. Current catalogue and revision/status are checked
before save/review. Live review action is REVIEW_TEXT_DRAFT with draftId,
draftRevision, textMode=LIVE, mediaKind=MOCK_STORYBOARD. Pending review is not approval;
approved text/mock preview is not video generation or permission to publish.

Known provider failures produce persisted GENERATION_FAILED or CONTENT_REJECTED;
missing/changed evidence can produce INCOMPLETE. No output/review is invented on
failure. Whole-result final transaction rollback leaves earlier DRAFTING scope,
not successful content or approval; generic HTTP 500 requires refreshing the saved
record. No cancellation, durable result staging/recovery or automatic retry is
provided here. Default mock may keep its older failure contract. Mode belongs to
each saved record; current capability flags alone never relabel historical results.


## BA lifecycle checkpoint · 29 October 2026

Additive operations on the owning Customer's **natural-needs** BA records;
Customer session, CSRF and exact positive-integer contextRevision remain required.
Legacy structured consultations and CS/CO callers retain their contracts.

| POST `/api/consultations/{id}/…` | Exact JSON body | Guard and result |
|---|---|---|
| `revise` | `contextRevision`, `message` | ACTIVE/CLARIFYING/INCOMPLETE/COMPLETED; same ID, revision +1, replace the full current message scope, re-extract and require new confirmation |
| `cancel` | `contextRevision` | ACTIVE/CLARIFYING/INCOMPLETE only; revision +1, CANCELLED; repeat at the cancelled current revision returns unchanged |
| `recover` | `contextRevision` | Current durable draft in ACTIVE/INCOMPLETE; storage-only finalisation, no inference; already recorded current revision returns unchanged |
| `retry` | `contextRevision` | ACTIVE/INCOMPLETE with no draft; new revision and explicit new extraction, then Customer confirmation; pending draft returns 409 RECOVERY_AVAILABLE |

This follows BA-STM-01 panel B (PDF page 49): COMPLETED is resumable by revision,
but not cancellable; CANCELLED requires a fresh consultation. Cancellation suppresses
late output; it does not abort an already running GPU request or undo earlier delivery.
Replacing the request never silently inherits old constraints. History retains old
input, confirmed needs, applicable result and mode, clearly labelled historical.
Old/cancelled revisions return 409 and cannot stage or deliver a result.

Inference finishes outside write transactions. A server-owned `pendingOutcome`
draft is first committed in the existing payload; final result and audit commit
together only after current revision/status/confirmed scope/catalogue/fact/stock
checks. This adds no schema or model interface. Snapshot projection exposes only
draft kind/revision/mode, never its uncommitted advice value. Caller-supplied result,
mode or extra fields are refused. Recovery preserves the original mock/live label
even after configuration changes, and refreshes the inventory observation once.
Repeated recovery returns the saved outcome/observation, not a new availability check.

If final persistence fails, return 503 BA_STORAGE_UNAVAILABLE and save INCOMPLETE /
BA_RECORDING_FAILED when possible; if even failure recording is unavailable, ACTIVE
with a draft may remain. If draft staging also failed, no draft is invented: recovery
returns NO_PENDING_RESULT; explicit retry makes a new inference attempt. An ACTIVE
record is not proof of a crashed process; retry explicitly supersedes possible
ongoing work. Failed cancellation returns 503 BA_CANCELLATION_NOT_RECORDED and does
not claim the request stopped. No automatic retry or commerce effect is introduced.

Founder-only `ba_recording` is a declared one-shot final-advice-save simulation,
retaining a recoverable draft. It does not damage storage or affect AP/CS operations.
Web refresh/cancel remain usable during inference; response sequencing prevents an
older snapshot from replacing a later refresh. Shared review remains pending.

## Earlier round 1 · BA needs checkpoint · 29 October 2026

Additive standalone BA intake (Customer session + CSRF, same owner). The existing
structured `/api/consultations` route and CS/CO callers retain their contracts.

| POST path | Exact JSON body | Saved behaviour |
|---|---|---|
| `/api/consultations/intake` | `message` | 201 record; ACTIVE during inference, then CLARIFYING or INCOMPLETE |
| `/api/consultations/{id}/clarify` | `message`, `contextRevision` | Same ID, revision increment, old result invalidated, re-extract |
| `/api/consultations/{id}/confirm-needs` | `contextRevision`, `concern`, `budget`, `fragranceFree` | Explicit Customer review/correction, revision increment, then independently validated advice |

Messages are 1–2,000 characters, at most eight messages / 8,000 characters total.
Only ACTIVE/CLARIFYING/INCOMPLETE natural-needs records accept clarification.
Confirmation requires CLARIFYING and `needsReady=true`; a complete extraction
alone never recommends. `contextRevision` is a positive integer, not a boolean.
Stale revisions return 409 STALE_SCOPE; another Customer receives 404, Founder 403.
Unsupported/extra body fields are rejected. Completed records require a new
consultation; no cancel or completed-record revision API is supplied in this slice.

`payload.messages` retains original text; `proposedNeeds` includes bounded literal
sources and remains an unconfirmed hypothesis. UI shows fixed missing-field
questions, then editable confirmation fields. Confirmation stores `needsConfirmed`
and authoritative Customer-reviewed `needs` before recommendation. Request and
extraction budgets use AUD dollars; saved confirmed needs/catalogue use cents.
Provider work is outside write transactions. Revision/status and current catalogue
are rechecked before saving; stale inference cannot overwrite the current revision.
Unavailable/timeout/invalid output saves INCOMPLETE with no successful recommendation
or mock fallback. If the final database write fails, its transaction rolls back:
the saved record can remain ACTIVE, never falsely COMPLETED. Automatic storage
recovery and a dedicated recovery button are not implemented for this new BA path.
See VERIFICATION.md for actual checks; this does not complete all BA cases.

Read Stage 1 section 8.2 and the original state vocabularies in
`reference/stage1-baseline.txt`. Python uses snake_case at the code boundary;
JSON uses camelCase where an explicit contract field is needed. This is a partial
implementation of the class/port design, not a one-to-one implementation of every
model participant. Domain objects are persisted records in this initial version.

| Stage 1 receiver | Current receiver | Boundary |
|---|---|---|
| BeautyAdvisorService.submit; LlmPort.propose | `BeautyAdvisor.submit`; `MockLlm.propose` | Catalogue/stock reads; consultation writes only |
| CustomerServiceAgent.submitRequest/confirmResolution | `CustomerService.submit/confirm` | Customer-owned order, current evidence, confirmation and AP |
| AfterSalesPort.executeResolution/lookupOutcome | `MockAfterSales.execute_resolution/lookup_outcome` | Unique actionRef and separately committed simulated effect |
| CoordinationService.handoff/recordResult/reconcile | `Coordination.advice_handoff/state`; CS reconcile | Founder-started CS→BA slice, not generic dispatch |
| FounderApprovalService.receiveRequest/processDecision | `Approval.submit/decide` | Persist receipt; exact-scope decision/audit commit |
| ReviewGateway.routeRecordedDecision | `Approval.deliver` | Separate delivery; no business execution |
| MarketingContentService.submitCampaign/requestRevision | `Marketing.submit/revise` | Mock script/storyboard; new revision, new review |

## Identity and request rules

HTTP binds only to 127.0.0.1. There is no CORS. Host/origin checks reject cross-site
and non-loopback hosts. Mutations require JSON and, after login, a CSRF token.
An opaque HttpOnly SameSite=Strict session cookie maps to a server-side user;
no `Authorization: userId`, supplied `role` or customerId selects authority.
Shared seeded demo passwords are PBKDF2-hashed, but are not production credentials.
Session responses contain actor and CSRF token, never password/session hashes.

Errors use the appropriate 400/401/403/404/409/413/415 status and
`{"error":{"code":"...","message":"..."}}`. Other customers' order/record references
produce generic inaccessible/not-found responses. No customer sees all records.
Inputs and database evidence are escaped before insertion into browser markup.

## Initial same-origin JSON endpoints

| Method/path | Actor | Meaning |
|---|---|---|
| GET `/api/health` | Public | Simulation status only |
| POST `/api/login` | Public | username/password → server session and CSRF |
| GET `/api/session` | Session | Current actor/CSRF |
| POST `/api/logout` | Session + CSRF | Invalidate this server session |
| GET `/api/snapshot` | Session | Role/ownership-filtered workspace |
| POST `/api/consultations` | Customer | message, concern, budget (AUD), fragranceFree |
| POST `/api/after-sales` | Customer | orderId/needs → stored assessment; 201 may be ASSESSING, NEEDS_INFORMATION or UNRESOLVED, not exchange success |
| POST `/api/after-sales/{id}/coordinate` | Founder | Initiate the authorised GR-S-01 advice handoff |
| POST `/api/after-sales/{id}/confirm` | Owning Customer | Current contextRevision; first confirmation submits review, later current confirmation may execute |
| POST `/api/after-sales/{id}/revise` | Owning Customer | Current revision plus corrected needs; invalidate former scope |
| POST `/api/after-sales/{id}/reconcile` | Owning Customer | Read same actionRef effect and recover outcome, never repeat execution |
| POST `/api/approvals/{id}/decide` | Founder | decision, reason, contextRevision |
| POST `/api/approvals/{id}/deliver` | Founder | Redeliver same committed decision |
| POST `/api/approvals/{id}/recover` | Original Founder | Only contextRevision; recover the saved decision intent for the displayed current scope |
| POST `/api/campaigns` | Founder | brief and authorised productId → mock draft/review |
| POST `/api/campaigns/{id}/revise` | Founder | Current revision, brief, productId → new exact-scope review |
| POST `/api/demo/fault` | Founder | One declared next-operation failure fixture |

## Evidence, review and execution correlation

Review submission retains origin_role/origin_id, exact action, revision, evidence
and action_ref where applicable. PENDING is a request state, not DecisionKind.
DecisionKind is APPROVE, REJECT or REQUEST_REVISION. Committed decisions retain
decision_id, actor, reason and exact scope; decision/request/audit update together.
Delivery is a separate transaction and status. Repeated delivery is idempotent;
stale scope cannot change the current origin. Approval itself performs no effect.

Recording recovery requires the authenticated original Founder, CSRF and exactly
`{"contextRevision": <positive integer>}`. The displayed revision must still match
the review and current origin/approval link; the stored intent's exact action and
actionRef are revalidated before commit. Caller-supplied decision, reason, actor
or action fields are rejected. Recovery reuses the durable kind/reason, commits
once and attempts separate delivery; it never executes commerce or publication.
Repeating recovery after commit returns the same decision without redelivery;
use `/deliver` for failed delivery. Stale scope is refused even on this repeat.
The failed card displays the saved intention as non-authoritative and offers
recovery only for the original Founder and a current linked origin. Decision and
recovery errors refresh the saved state before showing the error. The
`approval_recording` fixture is available under Founder simulation controls.

CS rechecks order association, current policy evidence, replacement stock, current
confirmation, exact action/ref/revision and delivered committed approval. It saves
EXECUTING/intent first. The simulated external adapter atomically conditionally
decrements stock and inserts the unique actionRef effect in another transaction.
CS then saves the confirmed outcome and CO completion. A response timeout yields
RECONCILING; an injected result-save failure yields RECORDING_FAILED. Recovery
queries the effect table and saves the same receipt, without calling execute.

This is a local transactional simulation of an external service contract; real
provider lookup/idempotency guarantees remain unverified. A process crash with an
EXECUTING request can be queried; an unresolved lookup escalates without retry.

## Implemented state subsets

- BA: ACTIVE → CLARIFYING (missing questions or explicit-confirmation gate) → ACTIVE → COMPLETED/INCOMPLETE for natural intake; full lifecycle remains pending.
- CS: ASSESSING → AWAITING_CONFIRMATION → REVIEW_PENDING → current approval →
  AWAITING_CONFIRMATION → EXECUTING → RESOLVED; failure states RECONCILING,
  RECORDING_FAILED, UNRESOLVED; review REJECTED/NEEDS_INFORMATION.
- AP: PENDING → APPROVED/REJECTED/REVISION_REQUESTED; old scope SUPERSEDED.
  No receipt is approval, and failed delivery preserves the committed state.
  A decision that could not be recorded becomes RECORDING_FAILED: no decision id,
  no delivery and no business effect. A separate durable decision intent
  (PROPOSED → COMMITTED, or RECORDING_FAILED) holds the intended Founder, kind,
  reason and exact scope; it grants no authority and is the only input to
  storage-only recovery. One request has at most one committed decision.
- MC: DRAFTING → REVIEW_PENDING → APPROVED/REJECTED/REVISION_REQUIRED;
  revision creates new payload/history and review; former scope is superseded.
- CO: PENDING_VALIDATION, HANDOFF_SENT, AWAITING_APPROVAL, EXECUTING,
  RECONCILING, RECORDING_FAILED, CLARIFICATION_REQUIRED, ESCALATED,
  CANCELLED, COMPLETED. The persisted handoff is a narrow synchronous slice.

Do not add a new state casually: document its event/guard/effect and update callers,
tests and the model deviation record. Live generated script/storyboard checking
must inspect the actual output, not trust a model-provided list of its own claims.

## Shared LLM seam and ownership

See [LLM_INTEGRATION.md](LLM_INTEGRATION.md) for the preserved v1 Python calls,
field units, module fixtures, error/mode gaps and later live acceptance. Shared
LLM integration is reserved to Danyang Wang; default runtime remains mock.
Opt-in standalone BA transport and precise mode/error reporting are documented in
[WINDOWS_LLM.md](WINDOWS_LLM.md). One actual BA model path is now verified; see
[WINDOWS_LLM_RUNTIME.md](WINDOWS_LLM_RUNTIME.md).
CS intent extraction is a future coordinated interface, not an implemented port.

## Retained CS HTTP assessment · 27 October 2026

HTTP intake now explicitly calls CustomerService.assess in the existing transaction.
The legacy service submit call remains unchanged. Initial inaccessible/unverifiable
order association raises a generic error with no record or protected context.
After verified association, missing/conflicting/unsupported/unavailable policy
may create NEEDS_INFORMATION/UNRESOLVED with permitted reasons/references, no advice
or approval/effect. A write failure does not claim a retained result. Client-supplied
policy/identity fields cannot replace server evidence or the session actor.

The request card renders evidenceOutcome without assuming policy/advice exists,
hides earlier advice when evidence is blocked, and offers the existing revision
path for reassessment. Corrected authoritative evidence plus current needs yields
a new ASSESSING revision requiring a fresh Founder handoff, Customer confirmation
and exact-scope review. Evidence is never editable through this form. If it is still
missing, the same blocked record remains, without a fabricated new proposal.
Coordinate/revise/confirm errors refresh the persisted snapshot, including saved
blocked outcomes returned through an HTTP error. Non-success receipts use truthful
assessment wording. Existing live-CS handoff/revise guard and effect reconciliation
remain unchanged. No new policy fixture endpoint or real CS model is introduced.
