# Shared contracts and implementation map

## Registered review policy and MC source conflicts · 31 October 2026

Danny-authorised KAN-9 bounded repair; see [evidence index](EVIDENCE_INDEX.md).
MC rejects known fragrance-fact/metadata contradictions before generation and on
saved-result validation: SOURCE_CONFLICT, retained INCOMPLETE on creation/revision,
no generators or new AP. Saved corrupt/legacy output is withheld as CONTENT_REJECTED.
Vocabulary is limited to fragrance-free/fragrance free versus contains fragrance/
contains added fragrance (case/space/nonbreaking-hyphen normalised), not general prose.

AP-REGISTERED-v1 admits only BA REASSESS_ADVICE, CS SIMULATED_EXCHANGE and MC
REVIEW_MOCK_DRAFT/REVIEW_TEXT_DRAFT, with exact origin/revision/actionRef and the
declared mock/live/template hash envelopes. Extra action fields/caller risk,
unknown roles/actions and malformed scopes return AP_ACTION_UNSUPPORTED before
receipt. The server-derived CONTENT_REVIEW/CONSENTED_REASSESSMENT/DISPUTED_EXCHANGE
class and requiresFounderReview=true are audited, not caller options. All three
classes require Founder review. No routine no-review CS path or monetary risk
threshold is added. Missing/conflicting/changed authoritative CS policy blocks
receipt, new intent, uncommitted commit/recovery and delivery. Unknown/stale
requests grant no authority. Identical existing receipts remain idempotent;
changed action/evidence/ref returns STALE_SCOPE. Recovery binds evidence and both
origin fields as well as action/revision/ref. Failed delivery preserves its commit.
The legacy MC revision caller saves the new origin inside the same transaction
before AP validates it. No schema/provider/HTTP contract or execution change.

English is the maintained primary version. [中文阅读副本](zh-CN/CONTRACTS.md).

## BA/MC bounded failure repair · 31 October 2026

KAN-10: explicit structured consultation fields are message/concern/budget (AUD)/
fragranceFree. New structured resumption accepts their supplied subset plus required
positive integer contextRevision; explicit replacement drops omitted old constraints.
Same owned ID / revision+1 / historical old result; cancellation suppresses late
output and requires a new session afterwards. Company.consult remains creation-
compatible and adds optional rid for resume; Company.revise_consultation,
cancel_consultation and recover_consultation are service-only. Low-level
BeautyAdvisor submit/resume/revise/cancel remain caller-transaction operations.
Company uses existing BaIntake durable ADVICE save/recovery and shared independent
evidence checks; all BA snapshots withhold pendingOutcome.value. Existing structured
HTTP creation rechecks the trusted session callback after inference. No new routes,
structured UI controls or structured AP review are added.

KAN-12: required catalogue facts must be a nonempty list of nonblank strings.
Invalid/missing facts raise DomainError INCOMPLETE before provider calls. Existing
retaining draft/revision and Company generation paths persist that safe outcome
where storage works; saved-result validation applies the same guard. No schema,
provider signature, media format or AP authority contract changes.

## Advert-template rendering · 30 October 2026

The optional renderer uses source-bundled PNG illustrations (editable SVG sources),
fixed studio composition, bounded CALM/ENERGETIC/INFORMATIVE motion/accent and
validated caption textfiles. Captions remain data, not filter expressions; packaging
is explicitly fictional. No user-selected asset path/URL, new provider, audio or
claim is accepted. Missing artwork -> MEDIA_UNAVAILABLE without fallback/review.
Format, label, kind, metadata schema, file/script hashes and AP scope are unchanged;
old saved artifacts remain readable/recoverable using their original bytes. Asset
changes only affect new renders; recovery never substitutes a freshly rendered file.


## BA conditional review checkpoint · 30 October 2026

Additive natural-route BA-UC-01 E4 contract; no schema/provider change:

`POST /api/consultations/{id}/request-review` accepts exactly
`{contextRevision: positive integer, consent: true, issue: nonempty product question <=1000 chars}`.
Session Customer/CSRF/record ownership/current stored Customer role are required.
Natural confirmed-needs INCOMPLETE advice only, no pending draft or medical stop.
Duplicate identical scope returns its receipt; changed issue requires a new revision.
No arbitrary review ID, role, result, action, evidence, authority or decision accepted.

Server action is `{type: REASSESS_ADVICE, consultationId, contextRevision}` with
null actionRef. Evidence is exactly `{needs:{concern,budget,fragranceFree}, issue,
outcomeCode, adviceSimulated}`; budget uses integer cents. Outcome codes are bounded
server classifications, not raw provider exceptions. Raw chat/invalid proposals,
orders, profiles, credentials and session fields are excluded. Consent is recorded
for this revision. AP receipt, BA REVIEW_PENDING and acknowledgement audit commit
atomically; unavailable/unacknowledged/storage failure is BA_REVIEW_UNAVAILABLE,
not success or claimed submission. This local SQLite ReviewPort is not a new remote service.

AP now accepts BA alongside CS/MC. Existing Founder decision intent/atomic commit/
storage recovery/delivery are reused; BA validates current action/revision/consent/
confirmed constraints and stored evidence, including intent evidence on recovery.
APPROVE delivery makes BA CLARIFYING/needsReady, with failed advice still incomplete;
Customer uses existing confirm-needs route for a new revision and fresh assessment.
REJECT ->INCOMPLETE; REQUEST_REVISION ->CLARIFYING/needsReady:false. Neither allows
direct confirm. Ordinary valid advice requires no review. Medical scope and invalid
product/fact/stock cannot be overridden by a decision. Approval does not execute
anything or itself invoke a model. No automatic inference/retry on delivery.

Natural confirm-needs optionally receives a trusted session-recheck callback from
Router; snapshots close before inference, then current Customer/session, owner,
source payload and revision are checked before staging; existing final evidence
validation and draft recovery remain. Correction/retry/confirmation/cancellation
supersede prior review and retain decision/history; old delivery/recovery cannot
grant new-revision authority. Legacy structured consult signature remains unchanged
and has no conditional review endpoint in this slice.

## CS intent v1 and staged live handoff · 29 October 2026

The additive shared `interpret_service_request(message: str) -> dict` reuses
StrataLlm._complete/config/errors. Exact fields: intent=EXCHANGE|CLARIFY|UNSUPPORTED,
intentSource=literal quotation|null, needs={concern,budget,fragranceFree,sources};
needs uses the existing extraction schema (AUD dollars, explicit nulls, exact
per-field user quotations). No trusted identity/order/policy/stock/product/authority
is sent or accepted. Independent bounded cue checks corroborate concern/fragrance,
withhold mixed concerns/budgets and reject authority fields. Negated/mixed/refund/
return/cancel/medical requests clarify/escalate; this is not a universal semantic verifier.

POST /api/after-sales/intake takes exactly orderId/message (Customer, 201).
POST /api/after-sales/{id}/revise-intent takes exactly message/contextRevision (owner).
Both verify association/policy first; save INTERPRETING metadata, release the DB
connection for inference, then recheck current session/role/source/owner/revision/
policy before retaining READY, CLARIFICATION_REQUIRED, UNSUPPORTED or FAILED.
CS states remain ASSESSING/NEEDS_INFORMATION/UNRESOLVED. READY is a hypothesis,
not approval: interpreted constraints are visible for Customer review/correction.
Exact duplicate intake reuses its record; changed messages require explicit revision.

Founder POST /api/after-sales/{id}/coordinate accepts only contextRevision, required
for live. Legacy mock empty-body callers remain compatible. Live requires current
READY intent and policy. CO.prepare_external commits one SENT read-only attempt;
the application releases the connection and calls BA.recommend_from_catalogue
with a snapshot, then rechecks session/role/source/owner/revision/policy and current
catalogue/facts/stock before CO.finish_external and CS outcome save atomically.
SENT is pending dispatch evidence, never an accepted result or effect. Repeated SENT/
terminal attempts never redispatch. New Customer revision supersedes old pending
handoffs and exact reviews; old responses/confirmations cannot reopen them.
Legacy CustomerService.coordinate rejects live with CS_STAGED_HANDOFF_REQUIRED.

No schema/new dependency/provider/client/config or AP/effect contract changed.
Default structured/mock paths remain. CS capability mode is LIVE/MOCK/NOT_CONNECTED;
intent.simulated and advice.simulated track their own origin; payload.simulated
still describes simulated commerce. Model unavailable/timeout/invalid is retained
without fallback. SQLite write errors return503 CS_STORAGE_UNAVAILABLE, never a
false saved trace. Interrupted/final-save-failed scope stays INTERPRETING/SENT and
needs explicit new-revision correction; no generic automatic/storage-only CO
recovery is implied. Confirmation→exact AP→Customer reconfirmation→one simulated
effect still uses the original CS/AP/after-sales services. Historical guards below
are superseded only for this newly tested path.

## CO read-only advice failure boundary · 29 October 2026

`Coordination.advice_handoff(db, rid, needs, advisor)` retains its signature and
caller-owned transaction. It requires the linked, same-owner current CS origin;
new dispatch requires ASSESSING. Only message/concern/budget/fragranceFree pass,
with budget already integer AUD cents. Different valid saved scope returns 409
STALE_SCOPE. Same origin/revision reuses its saved result without target/events;
an explicit CS revision is required for another attempt. No HTTP/schema changes.

Each payload.handoffs entry retains handoffId/fromRole/toRole/originId/
contextRevision/handoffTime/operation/authorisedContext/status/dispatched/result;
payload.originRevision and CO revision follow CS. Operation is READ_ONLY_ADVICE.
Invalid context returns safe INCOMPLETE/CO_INVALID_CONTEXT and CO
CLARIFICATION_REQUIRED, dispatched=false. Missing/invalid receiver, timeout,
unavailable/unexpected failure or unverifiable/incomplete result returns safe
INCOMPLETE, FAILED handoff and CO ESCALATED with allowlisted reason/recovery,
businessExecution=false. Only safe upstream codes are retained; no raw exception
or untrusted result prose. CS existing caller saves UNRESOLVED, without actionRef,
Customer confirmation or AP review. Valid originating mode is retained, no fallback.

Success requires current catalogue product equality, available stock, explicit
needs/budget/fact support, correct evidence reference/constraints and timezone-aware
observation. Receiver prose becomes a safe CO control message. Only the read-only
handoff is COMPLETED; CO PENDING_VALIDATION still awaits downstream CS outcome.
HANDOFF_SENT precedes target call; HANDOFF_FAILED/ADVICE_RESULT_RECORDED saves its
outcome. These writes commit with existing CS transaction, not an independent
external-effect journal. SQLite persistence failure returns 503
CO_STORAGE_UNAVAILABLE, rolls back and claims no saved trace. No durable staged
CO recovery/new dispatcher/automatic retry is implied. See VERIFICATION.md.

## MC generation recovery checkpoint · 29 October 2026

MC-ACT-01 / MC-STM-01 (public PDF pages 39, 51–52), MC-T-06, Danny-authorised
shared exception. All HTTP modes, including default mock, now use the same staged
Company.campaign orchestration; legacy injected MC submit/submit_draft/revise service
methods remain compatible and do not independently acquire durable HTTP recovery.

| POST `/api/campaigns/{id}/…` | Exact body | Behaviour |
|---|---|---|
| recover | positive integer contextRevision | Same saved outcome/revision, no generator calls; validates current catalogue, actual text/frames, original modes and exact template artifact/manifest/hash before resuming one pending review. Already recorded generation returns current state, preserving later decisions. |
| retry | positive integer contextRevision | Interrupted/failed generation with no pending result/review/decision; same ID, revision +1, explicit new generation using current configuration. Saved result returns 409 RECOVERY_AVAILABLE; existing review authority cannot be replaced by generation retry. |
| cancel | positive integer contextRevision | Active draft only; revision +1, CANCELLED, prior history retained, old review superseded. Current-revision repetition is idempotent. Decided terminal drafts cannot be cancelled retroactively. Cancelled campaigns require a new campaign. |

Founder session, owner and CSRF checks apply. Extra caller-supplied results/modes
or malformed revision are rejected. Revise still takes brief/productId/contextRevision;
it replaces scope and starts fresh review, refusing cancelled records. Default mock
retains blank-revision INCOMPLETE behaviour; provider failures retain originating mode.

GENERATING records the scope before inference outside the write lock. A
server-owned payload.pendingGeneration stores revision/status/outcome/modes in the
existing JSON payload; no schema migration. Snapshot/controls expose only its
metadata, including in history, never uncommitted text/media or approval. The final
validated draft, review receipt and audit save atomically. Failed final transaction
returns 503 MC_STORAGE_UNAVAILABLE and records RECORDING_FAILED when possible;
total write outage can leave GENERATING with a saved draft. Failed staging leaves
no draft and does not invent one. Initial scope-write failure may leave no new record.
GENERATION_FAILED, CONTENT_REJECTED and INCOMPLETE remain distinct failed outcomes.

Founder-only one-shot mc_recording is an explicit local final-save fixture: 503
MC_RECORDING_FAILED with durable pending outcome and no review. It is separate from
real SQLite failure tests. Failed cancellation returns 503 MC_CANCELLATION_NOT_RECORDED.
Missing original template-media configuration returns 503 MC_MEDIA_RECOVERY_UNAVAILABLE,
preserving pending data. Invalid/currently changed evidence or artifact is withheld,
never reviewed; use a fresh correction. Recover never approves, publishes or executes.

Generation recovery is separate from AP decision persistence/delivery recovery.
No physical provider abort, partial model/render resume, orphan cleanup, full MC
decision/local-save recovery, automatic retry or general semantic verifier is added.


## MC template MP4 checkpoint · 29 October 2026

Optional Company(path, llm=None, media=None) injection preserves MockMedia default.
Template mode (even with mock text) uses Company.campaign outside the write lock;
text-only Strata/default mock paths remain compatible. Media adds kind=TEMPLATE_VIDEO,
simulated=false, modelGenerated=false, exact frames, opaque artifactId, bytes/MIME,
sha256, scriptSha256 and fixed template metadata. textSimulated/mediaSimulated are
separate; legacy record simulated refers to text. Configured media capability is
TEMPLATE_VIDEO; health TEXT_WITH_TEMPLATE_VIDEO proves configuration, not rendering.

Existing review action additionally binds mediaKind=TEMPLATE_VIDEO, textMode,
mediaSha256 and scriptSha256, alongside draft ID/revision. AP logic is unchanged.
Only a fully validated file and manifest can enter the saved payload/review transaction.
Failed render/timeout/format results retain GENERATION_FAILED with an explicit MEDIA_*
code, without output or review. No fallback or automatic retry is introduced.

GET /api/campaigns/{id}/media/{revision} requires the owning Founder session, current
revision and a saved template artifact; current drafts can be previewed before a
decision. It serves video/mp4 with session-protected/no-store responses and single byte-range
support (200/206/416). Authentication failure 401, wrong role/owner 403, stale URL
409, missing record/media 404, unavailable/modified artifact 503. Path/URL inputs
cannot select filesystem paths. Downloads recheck manifest/size/hash, and never
substitute a new file for an old revision. Preview/download is not publication.
Files for superseded, failed or uncommitted work may remain ignored for diagnosis;
there is no orphan cleanup, historical download API or durable media-save recovery.
Missing artifacts are refused; this does not retroactively erase historical decisions.


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
