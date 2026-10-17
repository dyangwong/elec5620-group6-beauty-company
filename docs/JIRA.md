# Jira work and GitHub linkage

English is the maintained primary version. [中文阅读副本](zh-CN/JIRA.md).

The human created elec5620_team6 and connected GitHub for Jira. On 17 October 2026,
AI-assisted configuration established the following real work-item mapping. This
is a setup snapshot; use Jira for current assignment, claims and workflow state.

[Board](https://uni-team6-elec5620.atlassian.net/jira/software/projects/KAN/boards/2) ·
[Backlog](https://uni-team6-elec5620.atlassian.net/jira/software/projects/KAN/boards/2/backlog).
One team-managed software space, key KAN. No site access, billing or account
permissions are changed by this setup. Existing KAN-1/2 are preserved.

| Chain | Epic | Starter task | Planned owner / verified assignment at setup |
|---|---|---|---|
| BA | KAN-4 | [KAN-10 / BA-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-10) | Danyang Wang / assigned |
| CS | KAN-5 | [KAN-11 / CS-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-11) | Siyuan Lei / assigned |
| MC | KAN-6 | [KAN-12 / MC-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-12) | Zhengdu Wei (Jira display ZHENGDU WEI) / assigned |
| AP | KAN-7 | [KAN-13 / AP-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-13) | Jiaxuan Ren / unassigned, account not matched |
| CO | KAN-8 | [KAN-14 / CO-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-14) | Guiyu Liu / unassigned, account not matched |
| Shared | [KAN-9](https://uni-team6-elec5620.atlassian.net/browse/KAN-9) | Integration & Verification; later child tasks scoped separately | Per concrete task |

All five starters were created To Do, Medium priority, labelled starter and linked
to the correct epic. Ticket descriptions contain source/acceptance IDs, bounded
files, observable conditions, English/Chinese brief links and completion limits.
Assignment is planned responsibility, not a personal work claim, implementation,
review or contribution. No guessed invitation was sent. Real/local model setup
remains deferred. Six epics are not six business agents; BA/CS/MC remain the three.

## Work sequence

1. Identify the member and read START_HERE, the module/brief and source models.
2. Check the actual Jira task, assignment/claim, blockers and current repository.
   The helper prints a local mapping only. No connection means a human must verify
   shared state; do not pretend the integration gave the agent access to Jira.
3. Use the real key in branch, commit and PR title. For CS, for example:

   ```text
   Branch: KAN-11-cs-start-01
   Commit: KAN-11 Handle policy evidence failures
   PR:     KAN-11 [CS-START-01] Preserve truthful eligibility outcomes
   ```

   The registry supplies a Jira-prefixed suggested branch for every starter.
4. To Do → In Progress when actual work starts; Verification for self-check, tests,
   PR and any relevant teammate review. The GitHub policy allows self-merge after
   required checks and does not require an outside Approve.
5. Mark Done only when this task's declared conditions have evidence, the PR is
   merged, and module docs/traceability record the exact tested subset and remaining
   integration gaps. One service slice does not complete a module or acceptance group.
   Failed/unmerged PRs and receipts are not completion. Do not auto-Done on merge.

Backlog is enabled. The five starters were moved into Board, retaining To Do.
The setup snapshot has seven board items (including preserved KAN-1/2) and an
empty backlog; future work can be planned in Backlog. Sprint dates/goals and work commitment require actual team
planning; no sprint is started and no new due date, recurring reminder or work log
is fabricated. Bug is available for discovered defects; existing Story/Subtask
work types remain. Blocked work needs a clear flag/reason, not a false success.

## Keep one work tracker

### Required progress checkpoints

The person doing the work owns these updates. An authorised coding agent may
perform them; otherwise the person records them manually. Check the current ticket
at each checkpoint instead of trusting a local snapshot.

| Checkpoint | Jira update | Repository / PR evidence |
|---|---|---|
| Before implementation | Verify identity, assignee, existing claim, scope and blockers. Record an explicit claim and move to In Progress when work actually starts. | Start from current main on the task-key branch. Record any evidenced claim in the task's own registry row; a local edit alone does not reserve shared work. |
| Ready for verification | Move to Verification once the scoped work is ready for checks/review; link the PR and state what remains. | Update the affected module guide, relevant traceability rows and changed implementation gaps in STATUS; fill the PR template with actual tests, limitations and the observed Jira state. |
| After merge and acceptance | Link the merged PR and acceptance evidence, then move to Done only if every condition of this task is met. Otherwise keep Verification or return to In Progress with a reason. | The merged change must contain accurate implementation/evidence records. A merge alone does not complete a module, full acceptance group or parent epic. |
| Blocked, paused or reopened | Record the reason, dependency and next action; flag blocked work. Use In Progress for resumed implementation and explain reopening. | Preserve previous evidence, record the remaining gap and link any follow-up task/PR. Do not erase failed checks or expand the task silently. |

Each progress update states the actual task key, date, actor, work completed,
test/evidence or PR link, blockers and next action. Update at these checkpoints
and when a material blocker/scope change occurs; no recurring schedule is required.
For changed scope or ownership, reconcile Jira and the versioned brief/registry
in the same work cycle, preserving the Stage 1 source and recording deviations.

### File responsibilities and stale-state handling

- Jira: live assignee, claim, workflow, blockers, planning and links to evidence.
- docs/tasks.json: stable task/member/source/file mapping; claim_state, claimed_by
  and pr_url are versioned receipts only. Update only the relevant row with real
  evidence. READY is brief readiness, not workflow; jira_status_at_setup and the
  setup assignee/date remain historical, not fields to rewrite for every move.
- docs/jira.json: configuration/setup receipt. Do not edit it on each status move
  or treat its verified_date as the date every ticket was last checked.
- Module guides, docs/traceability.csv and docs/STATUS.md: implemented behaviour,
  tested conditions and remaining technical gaps at a repository revision. Update
  the affected records in the implementation PR; do not copy the whole live board.
- PR template and Jira progress notes: connect the task, exact change and evidence.
  Record Jira's observed status/date and distinguish applied updates from pending
  instructions. Later checkpoints belong in Jira or the PR, without a new commit
  merely to mirror a workflow move.

If Jira is inaccessible, state "Jira update pending" and provide the exact task,
requested transition, progress text and PR/evidence links for the human to apply.
Never report a requested update as applied. Before shared integration, reconcile
the actual claim and current status through an authorised person. Offline status
or an old repository snapshot must not overwrite a newer Jira record. If Jira says
Done but evidence is incomplete, flag the discrepancy and reconcile the ticket;
do not manufacture tests or change Stage 1 requirements to make it look complete.

These are checkpoint-based human/agent updates, not automatic two-way sync.
GitHub CI checks repository behaviour and structure; it does not verify the live
Jira workflow. No Jira credentials belong in the public repository.

Jira owns current workflow. docs/tasks.json owns the versioned member/requirement/
file-scope/Jira-key mapping, not a competing live board. Preserve others' records.
Explicit personal claiming may update claim_state/claimed_by with evidence; planned
Jira assignment alone leaves local UNCLAIMED intact. Update stale setup snapshots
honestly rather than inventing a live sync. Do not make duplicate GitHub issues for
routine Jira tasks. GitHub for Jira links development data only when real work keys
are included; it does not implement or validate the feature.

The KAN-9 repository-maintenance [PR #2](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/2)
appeared in KAN-9 Development with its repository, branch and main target; actual
results are recorded in VERIFICATION. Keys mentioned by maintenance work may also
show development links; that does not mean their feature has started or passed. The integration epic remains broader work,
not complete merely because this configuration PR merges.
