# Proposed collaboration workflow

English is the maintained primary version. [中文阅读副本](zh-CN/COLLABORATION.md).

Prepared for onboarding at Danny's request, using the Stage 1 ownership map. This
is not evidence all members have adopted it. No Jira project, remote repository,
issue, review, sprint or human contribution was created here. START_HERE.md,
team.json, tasks.json, task briefs and SHARED_FILES.md define the entry process.

## Trace one unit of work

An actual Jira task links the Stage 1 requirement/feature, use case, model/guard
and acceptance case. Its branch/PR links that task and records implementation,
tests, observed results, feedback and remaining limitations. Use the actual Jira
key once available; a placeholder is not a task. Jira tracks work/iterations;
GitHub owns code/review/CI. Avoid competing copies of requirements in both tools.

Use one integration branch (`main`) and short task branches. Prefer vertical
changes that include domain behaviour, relevant UI and evidence over isolated
pages. The Stage 1 BA/CS/MC/AP/CO chain owners are the starting responsibility
map now prepared as the default Stage 2 continuation. Each member explicitly
declares their identity and checks the actual task claim before starting; do not
silently claim their work. The starter helper only prepares a local packet.

The maintainer publishes one common initial commit before teammates clone. A
downloaded source folder and a local repository with no HEAD are not a common
branch baseline. Check branch and dirty state, preserve unrelated work and use
the selected task branch. No initial commit or remote was made by onboarding.

If Jira is not connected, an authorised person may claim/update it manually.
Until shared tracking exists, member-local work may proceed on isolated task
branches, with the missing shared claim recorded honestly; before shared PR
integration link the actual work item and reconcile duplicate claims. Do not
fabricate IDs or retroactively invent iteration history.

## Shared-change rules

- A task states its allowed module/files and the explicit requirement revision.
- Contract changes update caller, receiver, persistence, fixtures, tests and docs.
- AP/CO and database schema changes identify affected chains for review.
- Preserve another member's work. Reconcile current branch changes before merging.
- Authors may self-check and merge their PRs after required checks pass; no outside
  approval is mandatory. Seek affected teammates' review for shared contracts,
  schema or authority changes. AI generation alone is not review or contribution.
- Changes need tests appropriate to the risk, not tests that merely repeat code.

## Definition of done for a task

1. Stated acceptance conditions have observable evidence, with mock/live identified.
2. Relevant failure, scope and duplicate-effect checks pass; baseline tests pass.
3. Startup and changed API/UI behaviour are documented and verified.
4. Traceability differentiates full case coverage from a tested subset.
5. PR explains behaviour, evidence, deviations and remaining risk. Actual review
   and Jira updates are recorded once performed; neither is invented locally.

## Iteration and assessment evidence

Retain real planning decisions, iteration goals, demonstrable increments, tutor/
teammate feedback and resulting changes/retrospectives as they happen. Jira should
show this process, not a last-minute list marked Done. No fixed sprint schedule is
created in this scaffold. The team selects cadence based on its availability.

The contribution form reports each member's specific work and percentages per
assessment criterion, each row totalling 100%. AI assistance, integration,
testing, review and documentation can be described accurately; commit count alone
does not establish contribution. No member percentages are supplied here.

## Source delivery

Prepare a clean source archive at an identified revision, excluding var/, .git,
credentials and machine-specific state. Download the actual Canvas submission and
rehearse startup from a fresh directory. A hosted demo or GitHub checkout is not
that verification. Determine the on-site Python/install/network rules with the
teaching team; original files, external model availability and cached services
must not be hidden runtime dependencies.

The current Git policy is [GIT_WORKFLOW.md](GIT_WORKFLOW.md): required PR/checks, zero mandatory outside approvals, no direct/force pushes to main. Earlier onboarding statements above describe preparation, not current hosting evidence.
