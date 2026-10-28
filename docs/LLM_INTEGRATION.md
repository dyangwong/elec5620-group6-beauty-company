# Shared LLM ownership and module contract

English primary. [中文阅读副本](zh-CN/LLM_INTEGRATION.md).

## BA lifecycle checkpoint · 29 October 2026

Round 2 adds natural BA revision/cancellation and persistence recovery around the
existing extraction/propose calls; it adds no provider dependency, prompt, key,
model download or live CS/MC capability. Full replacement input starts a fresh
interpretation scope and requires Customer confirmation. Cancelled/stale outputs
are discarded before staging/final save. A model request may still consume GPU
time after cancellation; no physical provider-abort guarantee is claimed.

Recovery accepts only the displayed revision and reads a saved server draft. It
never invokes extract_needs/propose, rechecks current authoritative evidence and
retains the draft's originating mode. With no saved draft, **retry** is a separate,
explicit new model attempt with a new revision and fresh needs confirmation.
Raw drafts are withheld from HTTP snapshots. Actual live recovery was verified
after model shutdown and application restart; a separate new consultation still
failed truthfully with LLM_UNAVAILABLE. Evidence and limits: VERIFICATION.md.
CS intent remains NOT_CONNECTED, MC MOCK, and the live CS handoff guard remains.

## Earlier round 1 · BA needs checkpoint · 29 October 2026

Danny authorised a bounded KAN-15 standalone BA perception/clarification slice.
It does not claim BA-START-01 or connect CS/MC. The additive optional capability
`extract_needs(messages: list[str]) -> dict` reuses `StrataLlm._complete`, the same
loopback configuration, strict JSON/envelope checks, timeout and no-redirect
transport as `propose`. No new client, dependency, URL or key is introduced.
Existing injected objects implementing only the v1 propose/script methods still
work with their old callers. Natural intake with a missing extraction method
saves INCOMPLETE / LLM_CAPABILITY_UNAVAILABLE; it never substitutes MockLlm.
Health adds `capabilities.baNeeds=LIVE|MOCK|NOT_CONNECTED`; configuration is not
model readiness. MC remains MOCK, csIntent NOT_CONNECTED and the live CS handoff
guard is unchanged.

Extraction v1.1 has exactly concern (HYDRATION/CLEANSING/null), budget (positive
AUD dollars, at most two decimal places and 10,000, or null), fragranceFree
(boolean/null), sources (exactly those three keys, literal user quotation/null).
Every non-null value requires a short source (at most 600 characters) found in
the saved original messages; budget also needs an explicit budget/currency cue
and matching literal amount; other currencies/conversion are refused. No user
identity, credentials, order, policy, product or database handle enters extraction.
Nulls generate fixed focused questions. English/Chinese mock grammar is a small,
labelled fixture; unsupported/ambiguous input requires clarification or safe stop.
Quotations and schema checks do not prove unrestricted semantic correctness or
medical safety. Customer confirmation is mandatory; recommendation then independently
checks authorised product ID, literal facts, price, constraints and current stock.

Natural intake uses only the Customer-reviewed three fields and original first
message for recommendation; the conversation stays stored separately. No general
multi-turn model memory, arbitrary generated prose grounding, live CS intent or
real MC/media is claimed. Actual Windows model and failure evidence is in
VERIFICATION.md; the 28 October source ZIP predates this feature and is historical.

[KAN-15 / GR-INT-02](https://uni-team6-elec5620.atlassian.net/browse/KAN-15) · owner: Danyang Wang · local model deployed; one actual BA path verified, broader integration pending.

## Owner and present boundary

On 18 October 2026, Danyang Wang (Danny / M1) explicitly reserved shared LLM
integration for himself. GR-INT-02 is separate from his BA-START-01 task. Other
members and their agents implement their own business slices and deterministic
fixtures; do not independently deploy models, choose providers, install SDKs,
create direct provider clients or redesign the shared model boundary. Request
interface changes through the shared task, with affected-owner review recommended.
This reserves responsibility, not permission to overwrite others' module work.

The 18 October reservation prepared ownership/seams only. On 21 October Danny
authorised gaming-laptop deployment and shared integration. Default mode stays
mock; an opt-in standalone BA adapter, capability labels and Windows scripts now
exist. After the initial restricted install failed, the model was installed and
the migrated runtime ACL repaired. One actual BA HTTP path now passes; see
[runtime evidence](WINDOWS_LLM_RUNTIME.md) and [machine/setup history](WINDOWS_LLM.md).
MC stays mock and CS intent is unconnected.

## Existing callable boundary (v1, preserve compatibility)

The application already accepts an injected object: `Company(path, llm=None)`
uses `MockLlm` by default and shares the supplied object with BA and MC. BA and
MC constructors accept that object. These are Python calls, not HTTP endpoints;
only the future shared adapter may translate them to a model service protocol.

| Call | Input | Result shape |
|---|---|---|
| `llm.propose(context, evidence)` | Validated needs: message, concern, budget in integer AUD cents, fragranceFree; a list of candidate catalogue records | dict with productId (candidate ID or null), factRefs (list of literal supplied product facts), simulated (bool) |
| `llm.generate_script(brief, evidence)` | Brief string and one authorised catalogue record | dict with script (string), claims (list of supplied facts), storyboard (list of shot/duration/caption/direction objects), simulated (bool) |

Catalogue records currently include id, name, facts, price in cents, version,
fragrance_free and availability/stock observations. Build minimal permitted
evidence; do not send database handles, sessions, credentials or unrelated orders.
Keep field names and units stable. Empty/invalid results are not successful advice
or a saved draft. These shapes describe the existing fixture-compatible boundary,
not proof of complete runtime schema validation or natural-language understanding.

Business modules consume structured results. Do not put provider URLs, model names,
SDK imports, transport requests, provider prompts or provider-specific response
parsing in business modules or browser code. Integration-owned adapter code will
own configuration, role-specific prompts, provider parsing, time limits and mode
selection. Members may document domain prompt requirements and examples, without
building separate provider pipelines. Test doubles stay injectable in module tests.

CS currently takes structured intake and reaches BA through CO; it has no separate
LLM intent-extraction port. Keep identity/order/policy/stock checks independent of
language interpretation. For now, retain the structured service boundary and
provide sanitised input, expected intent/clarification examples and failure cases
in the CS handoff. Danny will introduce and version the missing intent boundary
with the CS owner before real CS perception is claimed. Do not invent a no-op port
and describe it as integrated. AP/CO retain deterministic authority/state controls;
LLM output cannot approve, confirm, change stock or execute commerce/publication.

## What each member delivers for later connection

- BA: preserve the injected propose call; validate candidate identity and supplied
  facts independently; retain current revision/cancellation checks around results.
- CS: preserve the structured intake and authoritative evidence guards; supply the
  future intent examples above, without making a direct model connection.
- MC: preserve injected generate_script and separate media boundary. Validate the
  actual script/captions as well as structured fields; a model's own claims list
  does not prove its text is grounded. A storyboard is not a generated video.
- AP/CO: preserve revision/actionRef correlation and exact-scope authority. Document
  how unavailable/invalid/late advice enters the existing safe states.
- In each module PR, show a valid fixture, malformed/unsupported output, provider
  failure and (where relevant) stale/cancelled result handling. Use injected fakes;
  no running model/network is needed for the baseline tests. Map to the task's
  actual acceptance subset and name any cases not yet covered. Do not broaden a
  starter to implement every future live-model condition.

Timeout, unavailable service, malformed output and unsupported claims must never
be treated as live success. This document does not create new error codes or claim
all failure paths already exist: current domain errors/outcome states and gaps
remain in the module briefs. Danny must agree any normalised provider error mapping
with affected callers before wiring a real adapter. Late outputs must be checked
against saved current scope; the model must not supply trusted identity/revision.

## Danny's later integration acceptance

1. One shared adapter/configuration path preserves v1 callers and default offline
   mock tests. Add role-specific behaviour through the common boundary rather than
   separate services per teammate. Version incompatible changes with callers,
   fixtures and docs in the same PR; no silent signature changes.
2. Explicit mock/live selection and trustworthy per-capability mode reporting.
   UI/facade now expose configured BA/MC/CS-intent/media/commerce modes; app
   health does not prove model readiness. Each advice record retains its own mode. A live text model does not make media/commerce live. No silent mock
   fallback labelled as a real model result.
3. First verify one bounded BA path end to end, including independent evidence
   checks, malformed output, unavailable/timeout behaviour and safe non-success.
   Then integrate MC and the agreed CS intent port as separate reviewed slices.
   A BA demo alone does not complete GR-INT-02 or full Stage 1 acceptance.
4. Supply reproducible model/runtime/configuration instructions, observed machine
   constraints, actual model/version, redacted request/result evidence and limits.
   Record provider-specific budgets/timeouts as explicit choices, not course facts.
   Moving network calls outside current database write transactions and rechecking
   scope before persistence may require a bounded shared integration change.
5. Keep model weights under ignored `var/models/`, local configuration under ignored
   var/ or .env, and publish only safe examples. No fixed laptop IP or secret belongs
   in module code. Decide the authorised inter-machine network setup later; the
   app's current loopback binding is unchanged by this reservation.

## Continue on another machine

Push unfinished work to its task branch before switching; on the other machine,
clone/fetch the same repository and branch. Avoid concurrent edits to that branch.
Declare: "I am Danyang Wang; continue GR-INT-02 shared LLM integration, not my
default BA starter. Read AGENTS, this guide, CONTRACTS, STATUS, BACKLOG and the
actual Jira task before work." The starter helper still selects BA by default;
this separate guide is the shared-task entry and does not claim BA-START-01.

At each handoff record the branch/commit, actual Jira state, files changed, checks,
remaining work and setup prerequisites in Jira/PR and versioned relevant docs.
Never rely on chat memory or a local saved identity as shared progress. Weights,
secrets and local databases are not synchronised through the public repository.

## Current local slice · 21 October 2026

See WINDOWS_LLM.md for exact error mapping, standalone BA transaction/recheck,
HTTP CS handoff guard, budgets, signatures, tests and pending Jira text. Shared
review is pending; no teammate module or starter claim was changed. Preserved v1
calls do not establish live MC/CS capability or full GR-INT-02 acceptance.
