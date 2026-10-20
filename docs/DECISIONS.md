# Provisional implementation decisions

English is the maintained primary version. [中文阅读副本](zh-CN/DECISIONS.md).

16 October 2026. Local implementation was authorised by Danny. These technical
choices do not assert team/tutor approval of the original PROPOSED design.

| Decision | Rationale and limit |
|---|---|
| New isolated project; legacy reference only | Keeps credentials/data and unrelated commercial scope outside the repository. No legacy files were copied. |
| One modular application, one local database | Keeps the five chain boundaries while reducing initial integration/setup cost. Logical modules are not five deployable microservices. |
| Buildless HTML/CSS/JS and Python standard library | Existing Python 3.9 can run offline immediately, without installing dependencies. This is an initial local delivery choice, not a claim to the advanced-technology marks. Framework migration stays open. |
| Browser Customer/Founder workspaces | Makes human review and cross-role evidence visible. Stage 1 leaves physical hosting open; WeChat-specific delivery is not implemented. Team acceptance is pending. |
| Server-side demo sessions and ownership guards | Avoids legacy client-supplied user/administrator identity. Shared local passwords and loopback HTTP are not production identity. |
| Deterministic mock model/media/commerce adapters | Permits reproducible initial wiring and failure injection. Does not establish live LLM/agent capabilities or a video-generation result. |
| Separate commit for AP decision versus delivery | Failed delivery cannot erase a committed decision; duplicate delivery does not execute business work. |
| Separate commit for simulated external effect versus CS outcome | Exercises write-timeout/storage-recovery boundaries. Real external-service semantics remain unverified. |
| Optional features not implemented/OFF | Initial focus is core integration/safety. All five optional IDs remain tracked; they have not been removed from scope. |
| Stage 1 ownership is the default onboarding map | Danny requested that members continue their Stage 1 parts. Five member-specific starter briefs are prepared; no individual claim/acceptance or completion is inferred. |
| Public privacy derivative of the complete report | Supersedes the original byte-identical packaging choice for public publication. All 63 pages/models remain; student IDs and PDF metadata are removed. Original PDF stays unchanged locally/ignored. Original and derivative hashes are recorded separately. |
| Defer real/local model setup | Danny asked not to rush that work. Starter tasks use deterministic injected fixtures; no model download, provider choice, key or hardware setup is required. |

English is the maintained documentation primary at Danny's request. Root
`*.zh-CN.md` and `docs/zh-CN/` provide corresponding Chinese reading copies;
update both together. IDs, task/status data and original evidence remain shared.

## Decisions still needing the team or additional evidence

- Adoption/revision of the final Stage 1 baseline and acceptance of affected owners.
- Individual acceptance/claims of the default Stage 1 ownership map, actual GitHub
  accounts, Jira setup and tool-specific instruction loading. Public GitHub
  visibility was subsequently selected by Danny.
- Whether to retain this initial web stack, add a frontend/backend framework, or
  retain WeChat delivery. Record costs to existing APIs/models before migration.
- Live LLM provider, tools, funding/keys and guard/claim-validation approach.
- Actual video/media approach and permitted labelled fallback; storyboard cards
  alone must not be reported as a completed generated-video feature.
- Explicit PoC policy/risk/freshness/expiry/quality criteria and their approval.
- Production identity/retention and any hosted demo; neither is in initial scope.
- Remaining requirements, all optional ON behaviour, complete acceptance, genuine
  Agile evidence and clean Canvas package/on-site deployment rehearsal.

No policy return window, confidence cutoff, monetary risk threshold or review expiry
has been inferred from the old prototype. Catalogue values and eligibility are
synthetic fixture inputs.

## Public Git collaboration · 16 October 2026

Danny explicitly requested a public GitHub repository without Pro and a relaxed
review policy. Require PRs and passing CI for main, with zero mandatory outside
approvals; authors can self-check and merge. Shared contract/schema/authority
changes should seek relevant teammate review. Do not infer a review from a
self-merge. No open-source licence is assigned merely by making the repo public.
Original student identifiers and local credentials/runtime data are excluded.

## Jira setup · 17 October 2026

Danny requested configuration of the existing team-managed KAN space and repository
mapping. Keep one board/backlog and six epics, retain bounded starters, add Bug,
use Verification for self-check/testing without a mandatory outside Approve.
Default assignment follows verified displayed report names; unmatched AP/CO remain
unassigned. Assignment is not a personal claim. Do not start a sprint or invent
iterations/estimates/deadlines. Actual work/status remains in Jira; repository JSON
is a mapping/snapshot. GitHub for Jira does not grant coding-agent API access.

## Shared LLM reservation · 18 October 2026

Danny explicitly reserved GR-INT-02 / KAN-15 shared LLM deployment and integration
for himself. Preserve existing injected v1 BA/MC calls; CS intent extraction needs
a later coordinated interface. Members implement scoped business slices/fakes,
not independent providers. LLM_INTEGRATION.md defines the contract and gaming-
laptop handoff. This supersedes unassigned future LLM ownership, while keeping
actual deployment/provider choice deferred and BA-START-01 separate. It is not
a claim of implementation, teammate endorsement or completion.

## Teammate PR approval · 18 October 2026

Danny now requires teammate PRs to have non-author Approve, superseding the earlier
zero-external-review policy for teammates. Add active ruleset 25333272 on main:
at least one approval, dismiss stale approval, resolve review threads; only user
dyangwong has a PR-only review-layer exception, intended for his own PRs. Base
classic PR/CI/admin/no-force/no-delete protections remain enforced unchanged.
The exception is actor-based technically; agents must not use it on unapproved
teammate PRs. CODEOWNERS requests dyangwong by default, not exclusively.
The actual collaborator readback now shows slei0644 and ZhengduWei with write
access; this does not establish identity/claims/contribution or who invited them.

## KAN-15 Windows BA slice · 21 October 2026

Danny explicitly authorised local deployment/shared integration, separate from
BA-START-01. Use the standard library OpenAI-compatible HTTP boundary instead of
adding an SDK/framework. Default mock is unchanged; only standalone BA is opt-in
live. Preserve v1 signatures, keep MC explicitly mock and block live HTTP CS
handoffs until owner coordination. Select Strata v0.2.1 / Gyro-S / 8K / int8 KV /
single request / no vision or MTP for the measured 32 GB RAM, 12 GB VRAM laptop;
quality/fit/speed need real validation. The restricted install failed and no live
success or team approval is inferred. WINDOWS_LLM.md records budgets, errors,
scope, actual checks and next actions. No source/model diagram baseline changed.

## Runtime ACL repair and real BA · 21 October 2026

Supersedes the earlier blocked-install/real-success-pending snapshot. Migration
left runtime permissions inherited from D; the official owner-private ACL check
now passes after a backed-up repair. Windows scripts support RepairModel and
resume the installed saved profile, without duplicate download/start or config
overwrite. Strata 0.1.46 CUDA 13 / Gyro-S is running at 8192 context, one request,
MTP/vision off, VRAM reserve 1536 MiB. Exact model ID and actual evidence are in
[WINDOWS_LLM_RUNTIME.md](WINDOWS_LLM_RUNTIME.md). Actual authenticated BA HTTP
consultation passed (6.804 s, COMPLETED, simulated:false, grounded P-101 facts),
then passed again; zero effects/approvals. All 45 offline tests, repository/JS
checks and diff checks passed. Repeat repair preserved config/profile hashes;
repeat StartModel/InstallModel retained the same engine process. MC remains mock,
CS intent/live handoffs unconnected, broader acceptance/review pending. No Jira,
commit, push, PR or merge action occurred.
