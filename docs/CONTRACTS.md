# Shared contracts and implementation map

English is the maintained primary version. [中文阅读副本](zh-CN/CONTRACTS.md).

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
| POST `/api/after-sales` | Customer | orderId plus explicit consultation constraints |
| POST `/api/after-sales/{id}/coordinate` | Founder | Initiate the authorised GR-S-01 advice handoff |
| POST `/api/after-sales/{id}/confirm` | Owning Customer | Current contextRevision; first confirmation submits review, later current confirmation may execute |
| POST `/api/after-sales/{id}/revise` | Owning Customer | Current revision plus corrected needs; invalidate former scope |
| POST `/api/after-sales/{id}/reconcile` | Owning Customer | Read same actionRef effect and recover outcome, never repeat execution |
| POST `/api/approvals/{id}/decide` | Founder | decision, reason, contextRevision |
| POST `/api/approvals/{id}/deliver` | Founder | Redeliver same committed decision |
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

- BA: CLARIFYING, COMPLETED, INCOMPLETE. Full lifecycle remains pending.
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
LLM integration is reserved to Danyang Wang; current runtime remains mock-only.
CS intent extraction is a future coordinated interface, not an implemented port.
