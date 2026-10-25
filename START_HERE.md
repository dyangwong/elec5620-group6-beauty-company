# Teammate and coding-agent onboarding

English is the maintained primary version. [中文阅读副本](START_HERE.zh-CN.md).

This handoff follows the five member responsibility chains in the final local
Stage 1 report. Danny requested this default Stage 2 continuation; it does not
mean other members have claimed tasks, completed work or approved the full design.
Business-model replies and media remain mocks. Coding agents can first implement
isolated service behaviour, states and tests. Real LLM/local-model deployment and
video-provider selection are deferred, not prerequisites for the starter tasks.

## 1. Explicitly identify yourself

Use your full report name, member ID or module code. Do not ask the agent to guess,
and do not use a Founder/Customer application demo account as contributor identity.

| Member | Report name | Default module | Starter task |
|---|---|---|---|
| M1 | Danyang Wang | BA · Beauty Advisor | [BA-START-01](docs/tasks/BA-START-01.md) |
| M2 | Siyuan Lei | CS · Customer Service and Order | [CS-START-01](docs/tasks/CS-START-01.md) |
| M3 | Zhengdu Wei | MC · Marketing Content | [MC-START-01](docs/tasks/MC-START-01.md) |
| M4 | Jiaxuan Ren | AP · Approval and Governance | [AP-START-01](docs/tasks/AP-START-01.md) |
| M5 | Guiyu Liu | CO · Coordination and Recovery | [CO-START-01](docs/tasks/CO-START-01.md) |

BA, CS and MC are the three business agents; AP and CO are shared controls.
GitHub usernames remain unset. Git author, system login, account names and current
web-app roles do not establish contributor identity. The machine-readable map is
[team.json](docs/team.json); prepared task status is in [tasks.json](docs/tasks.json).

## 2. Give your coding agent a clear instruction

### What the agent obtains from the human

Read the mapping/brief and inspect the checkout first. Reuse information already
given in this conversation; do not turn onboarding into a questionnaire.

| Information | Agent behaviour |
|---|---|
| Declared contributor | Ask once for a report name, M1–M5 or the module the human explicitly owns, only if missing/ambiguous. Show the matched name/module/task. A Git login or ticket number alone is not contributor identity. |
| Work intent | Use that member's mapped starter when asked to start. Ask only if it is unclear whether to resume existing work, review, implement or switch tasks. A completed/claimed/conflicting ticket requires reconciliation, not automatic reuse. |
| Existing work / overlap | Inspect branch, main baseline, dirty files, task/PR state where accessible. Ask about known unfinished work or another active agent only if it cannot be established and affects this task; preserve it. |
| Action boundary | Reuse explicit authorisation for local work, Jira updates, branch push, PR creation and merge. Do not infer remote writes from local implementation. Clarify missing authorisation when the dependent action is needed; continue independent authorised work. |
| Access needed | Inspect available tools without assuming access. Ask for a non-secret account identifier only when needed to match an account; missing access can use a human handoff. Never ask for passwords, tokens, student IDs or model keys to start a service task. Ask about OS/setup only when an actual setup problem cannot be resolved by inspection. |

If only identity is missing, a suitable question is: "Which Stage 1 member are
you? Please give your report name, member ID or module; I will resolve the task
and read its scope from the repository." Once answered, do not ask again unless
the declaration conflicts or the human explicitly changes role/task.

The agent derives requirement IDs, model pages, acceptance conditions, allowed
files, branch suggestion and completion boundary from the repository. Humans do
not need to supply these again. A fresh agent/session still needs an explicit
identity declaration if it has no trustworthy conversation context; an ignored
saved profile is not a substitute.

### What the agent makes visible

Before edits, give a short start note: resolved member/module/task/Jira key;
claim/status checked or unverified; current branch/baseline and relevant existing
changes; acceptance target and allowed/shared file scope; immediate next action
and any missing access. A clear existing instruction is not another approval gate.

During work, report meaningful behaviour changes, discoveries affecting scope,
test failures, dependencies and conflicts. Explain the affected requirement and
people before proposing a shared change. Do not stream every command or repeatedly
ask permission for routine in-scope edits. Keep Jira current at the checkpoints
in [JIRA.md](docs/JIRA.md), using explicit pending instructions when unavailable.

At handoff, report the task/key, changed files and behaviour, actual test/scenario
results, acceptance conditions covered and still unverified, remaining integration
gaps, branch/PR/commit references when created, and actual/pending Jira actions
with the next responsible person/action. Report self-check and teammate review
separately; record AI assistance without inventing human contribution.

### How to keep parallel work on topic

1. Tie planned edits to this task's requirement/acceptance conditions. Follow the
   source authority order; do not replace Stage 1 with a new personal product idea.
2. Check actual claims and current main, then use one scoped task branch. Respect
   [file ownership](docs/SHARED_FILES.md); do not run two agents on the same task
   or shared checkout without an explicit division of work.
3. Treat other modules, new features, shared UI/contract/schema changes, framework
   migration and model deployment as scope changes unless explicitly covered by
   the brief. State the proposed change, reason, affected owners/files/conditions
   and integration need; obtain a bounded human instruction for out-of-scope edits.
   Record authorised deviations and seek affected-owner review. Continue safe
   in-scope work instead of blocking the whole task on an unrelated improvement.
4. Before PR/merge, reconcile current main and inspect the full diff for unrelated
   files, changed contracts and acceptance gaps. Resolve conflicts purposefully;
   do not overwrite teammate code/tests/claims or silently relax acceptance tests.
5. A finished service slice may still need shared HTTP/UI integration. Record it
   rather than expanding the task or marking the whole module/epic Done.

For example, the CS member can paste:

> I am Siyuan Lei, responsible for CS in Stage 1. Start with AGENTS.md and
> START_HERE.md. Resolve my default task CS-START-01 and read its module guide,
> task brief and relevant models in the final report. Briefly state the resolved
> identity, task scope and current gaps, then complete the authorised local
> implementation, tests and handoff notes within that scope. Do not stop at a plan.
> Preserve teammates' work; do not repeatedly request approval for routine
> reversible changes. Do not install or connect a real model, create or change
> external repositories, Jira or publishing services, or edit the final report.

Other members substitute their full name, module and task ID. Clarify unknown or
conflicting identity first; when the match is explicit, proceed with the task brief.
Read-only assessments, repository maintenance and integration handoffs do not
automatically start a member's feature task.

A human can explicitly ask any coding tool to read this entry. Automatic AGENTS.md
loading depends on the tool. This handoff does not assume a particular tool is
installed, connected or running in the background.

## 3. Prepare the current task packet

Run any of these from the repository root, or ask the agent to read the same files:

```sh
python3 scripts/start_work.py --list
python3 scripts/start_work.py --member "Siyuan Lei"
python3 scripts/start_work.py --member CS --task CS-START-01 --json
```

Python 3.9 or newer is required. On Windows, replace `python3` with `python` or
`py -3` if needed; keep the other arguments. No third-party package, model service
or network connection is required.

The packet includes the report fingerprint, reading order, starter task, primary
and shared edit scope, suggested branch, acceptance IDs and completion boundary.
`--save` optionally writes ignored `var/work-session.json` for this machine only.
It does not change shared task records, claim a Jira issue, verify real identity
or prove implementation has started.

## 4. Read and implement in order

1. Read AGENTS, STATUS, REQUIREMENTS, CONTRACTS and COLLABORATION.
2. Read your module guide, starter brief and its specified physical PDF pages.
3. Inspect relevant code/tests and run baseline checks; retain evidence of existing
   failures rather than hiding them.
4. Implement and verify on your task branch, updating your module records. Starters
   focus on service logic and tests. Coordinate shared UI, HTTP and global contracts
   under the [shared-file rules](docs/SHARED_FILES.md).
5. Before submitting, check the task conditions, affected modules and remaining
   gaps. A completed task does not mean its entire requirement or the group is done.

The complete privacy-redacted reading reference is
[stage1-report-public.pdf](docs/reference/stage1-report-public.pdf). Text excerpts do
not replace diagrams. Only student IDs/PDF metadata are redacted; all 63 pages
and model diagrams are retained. The unredacted local original remains authoritative;
the manifest records both original and derivative hashes. Brief page numbers are physical PDF-reader pages, starting
at 1, not printed report footers. Document the source and impact of design changes;
do not silently change requirements to simplify implementation. If the tool cannot
inspect a diagram, record that as unverified and continue independent work that
does not depend on it. Reading excerpts does not prove full-model verification.

## 5. Collaborate through GitHub and Jira

Use the published common repository baseline and create your own task branch.
Do not create an independent root commit. Jira setup/claims remain separate and
must be recorded honestly. See [Git workflow](docs/GIT_WORKFLOW.md).

Check actual Jira claims and branch state before implementing. Members without a
Jira connector can verify and update tasks manually. If access is unavailable,
record the missing shared claim and give precise pending updates for the human;
reconcile the actual claim before shared integration. A local READY record does
not prove Jira synchronisation and must not overwrite another person's claim.

Use the PR template with actual task IDs, requirement/case IDs, executed tests,
and model/UI impacts. Required checks must pass. Teammate PRs require at least
one actual non-author Approve from a write-access reviewer, normally dyangwong;
new commits dismiss stale approvals. Agents wait for review rather than self-merge
unapproved teammate work. Only dyangwong retains the own-PR exception described
in GIT_WORKFLOW. Seek affected teammates' review
for shared contracts/schema/authority changes. An agent's completion statement alone
does not justify replacing main. Real LLM
setup can happen later. See [BACKLOG.md](docs/BACKLOG.md) for remaining work.

## Current Jira entry

Read [JIRA.md](docs/JIRA.md). BA/CS/MC/AP/CO starters map to KAN-10/11/12/13/14.
Use the actual key in branch/commit/PR names, retaining the internal START ID.
The helper prints the versioned mapping and suggested branch, not live Jira state.
Three verified members are assigned; AP/CO remain unassigned pending real accounts.
Check actual claims before work. Sprint planning and model deployment are separate.

Before work, at PR handoff and after merge, follow the [progress checkpoints](docs/JIRA.md#required-progress-checkpoints).
Keep Jira current and include implementation/evidence changes in the same PR. The
example prompt above authorises local work only: give the human the exact Jira
transition/progress text/links when external updates are outside authorisation or
access is unavailable. Label them `Jira update pending`, never already applied.

## Shared LLM ownership and gaming-laptop handoff

[LLM_INTEGRATION.md](docs/LLM_INTEGRATION.md) reserves GR-INT-02 to Danyang Wang,
separate from BA-START-01. Other members keep provider-neutral injected seams and
deterministic fixtures; no duplicate model installs, SDKs or direct clients.
Read the exact existing BA/MC signatures, the still-missing CS intent seam and
per-module handoff requirements there. KAN-15 local adapter work has now begun;
the local model and one actual BA path now pass. See [runtime evidence](docs/WINDOWS_LLM_RUNTIME.md).
Danny's next-machine agent must explicitly select shared GR-INT-02 rather than
relying on the member helper's default BA starter.
