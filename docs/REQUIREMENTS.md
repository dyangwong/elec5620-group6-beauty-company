# Implementation baseline

English is the maintained primary version. [中文阅读副本](zh-CN/REQUIREMENTS.md).

Authority: final local Stage 1 report, verified in `source-manifest.json`.
Its design status is PROPOSED; no formal approval is inferred. The initial local
implementation is authorised, but policy/technology choices here remain provisional.
Source excerpts preserve the original requirement/use-case/acceptance context.

## Five owned chains, exactly three business roles

| Chain | Stage 1 owner / default Stage 2 continuation | Core features | Optional |
|---|---|---|---|
| BA-M-01 / BA-UC-01 | Danyang Wang | BA-F-01 need clarification; BA-F-02 explainable recommendation | BA-F-03 verified alternatives |
| CS-M-01 / CS-UC-01 | Siyuan Lei | CS-F-01 identity/intake/eligibility; CS-F-02 routine resolution/escalation | CS-F-03 status notification |
| MC-M-01 / MC-UC-01 | Zhengdu Wei | MC-F-01 brief/script/storyboard; MC-F-02 draft media and Founder review | MC-F-03 approved-concept variants requiring fresh review |
| AP-M-01 / AP-UC-01 | Jiaxuan Ren | AP-F-01 risk-based routing; AP-F-02 decision/audit | AP-F-03 assisted linked resubmission |
| CO-M-01 / CO-UC-01 | Guiyu Liu | CO-F-01 authorised handoff; CO-F-02 status/failure/recovery | CO-F-03 controlled automatic retry |

AP/CO are controls, not fourth/fifth AI business agents. At Danny's request, the
report ownership above is the default Stage 2 handoff mapping in team.json. It is
not proof of individual acceptance, Stage 2 completion or a shared task claim.
All fifteen features remain in scope tracking. Optional OFF cannot remove core
rejection, revision, escalation, reconciliation or safe incomplete outcomes.

## System requirements

- GR-C-01: one accountable Founder; BA/CS/MC differentiated; AP/CO shared.
- GR-C-02: facts require authorised evidence; expose missing/conflicting facts.
- GR-C-03: authority, Customer confirmation, approval and execution are distinct.
- GR-C-04: minimal authorised handoff context with origin/revision correlation.
- GR-C-05: expose uncertain effects and reconcile before duplicate execution.
- GR-C-06: labelled mocks, optional independence, no production settlement/posting.

All twenty role NFRs and detailed ACs remain in the source excerpts. Do not replace
them with an invented latency, confidence, return window, risk threshold or expiry.

## Integrated scenarios

GR-S-01: Customer exchange/advice intent; Founder initiates CO; CS verifies order
and policy; CO transfers minimal needs to BA; BA returns grounded advice; CS
rechecks eligibility/stock and obtains Customer confirmation; consequential action
receives AP exact-scope review; CS rechecks, saves intent/actionRef, executes only
permitted PoC work, reconciles uncertainty and records the actual result.

MC has its own Founder campaign path with shared AP control, rather than an
artificial handoff merely to include all three business roles in one sequence.

## Assessment obligations

Stage 2: Stage 1 implementation/design 7; agent capabilities 4; Agile experience 4;
effective advanced technology 5. The rubric explicitly says every group **should
use Jira**. Code management/CI on GitHub does not replace that instruction.
Record actual iteration, feedback and collaboration; do not backfill fake history.

The supplied rubric states source-code submission on **1 November 2026, 11:59 PM**
and downloading source directly from Canvas for on-site Week 13 deployment.
Current Canvas settings and on-site machine/network constraints remain unverified.
Contribution percentages are per assessment row, each totalling 100%; do not infer
them from commits or generated code. The source includes the contribution form.
