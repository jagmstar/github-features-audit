# PMO Project Management Plan: GitHub Features for Team Coordination

## Executive summary
GitHub Projects v2, issue and pull request templates, milestones, and workflow automation can give JAGM IT Company a lightweight PMO operating model without adding another planning tool.

The recommended approach is:
- use **Projects v2** as the source of truth for portfolio, program, and sprint coordination
- use **issue forms** to standardize intake and reduce back-and-forth
- use **PR templates** to make delivery reviews consistent
- use **milestones** to track time-bound delivery goals
- use **built-in project automations** and a small amount of GitHub Actions support to keep the board current

This plan assumes the repository stays on GitHub and that we want a process that works for both documentation work and future code delivery.

## Operating principles
1. **One source of truth** — the Project board is the current state of work.
2. **Structured intake** — every new request starts as a template-driven issue.
3. **Visible status** — work should be easy to find, group, and filter.
4. **Automation first** — humans should not have to move items manually for routine transitions.
5. **Milestone discipline** — every meaningful delivery should roll up to a milestone.
6. **Low ceremony, high consistency** — the process should be simple enough that the team actually uses it.

## 1) Projects v2 board setup guide

### 1.1 Recommended project structure
Create one primary PMO project and, if needed later, a separate delivery project for each major program.

**Suggested project name:**
- `JAGM PMO Delivery Board`

**Suggested views:**
- **Board** — daily execution and status movement
- **Table** — backlog grooming and reporting
- **Roadmap** — timeline planning across milestones and iterations
- **Intake** — filtered view for new requests and triage items

### 1.2 Core fields to create
Use a small set of fields that support planning, prioritization, and reporting.

| Field | Type | Purpose |
|---|---|---|
| `Status` | Single select | Work state across the board |
| `Priority` | Single select | PMO prioritization |
| `Iteration` | Iteration | Sprint or weekly planning |
| `Owner` | Assignee / people field | Person accountable for the item |
| `Team` | Single select | Function or squad ownership |
| `Effort` | Number or single select | Relative sizing |
| `Risk` | Single select | Low / Medium / High |
| `Target date` | Date | Delivery deadline |
| `Milestone` | Milestone-linked or tracked via repo milestone | Delivery checkpoint |
| `Type` | Single select | Bug / Task / Feature / Ops / Risk / Decision |

If the team wants to keep the board lean, start with:
- `Status`
- `Priority`
- `Owner`
- `Iteration`
- `Target date`

### 1.3 Recommended status model
Use a status model that matches real PMO behavior.

**Suggested statuses:**
- `Intake`
- `Triage`
- `Planned`
- `In Progress`
- `Blocked`
- `In Review`
- `Ready to Close`
- `Done`
- `Archived`

Board rule:
- keep only active work on the default board
- move finished work to `Done`
- archive old work rather than leaving it in active columns

### 1.4 Recommended board layout
Set the main board to group by `Status`.

Why:
- it matches the normal PMO flow from intake to completion
- it is easy for leadership to read
- it works well with GitHub Projects board layout, which is designed for kanban-style workflow tracking

Optional secondary grouping for table view:
- group by `Owner`
- sort by `Priority`, then `Target date`

Optional roadmap setup:
- use `Iteration` and `Target date` fields on the roadmap
- add milestone markers so leadership can see delivery windows on one timeline

### 1.5 Board setup steps
1. Create a new **Projects v2** project.
2. Add the fields above.
3. Create the default views: Board, Table, Roadmap.
4. Set the board column field to `Status`.
5. Add filters for active work, such as open items, current iteration, or key labels.
6. Hide fields that are not useful for day-to-day execution.
7. Save a leadership-friendly roadmap view.
8. Enable built-in workflows so new items are added and normalized automatically.

### 1.6 Board governance
Assign clear ownership for the board.

**PMO owner responsibilities:**
- maintain field definitions
- review board hygiene weekly
- enforce naming conventions
- keep milestone dates current
- archive stale completed items

**Team responsibilities:**
- open issues using templates
- update item status when work starts or is blocked
- link pull requests to issues
- keep milestone assignments current

### 1.7 Reporting rules
The project should answer these questions quickly:
- What is in intake right now?
- What is at risk?
- What is blocked?
- What is due this iteration or milestone?
- What is done but not yet archived?

A good PMO board should allow leadership to see those answers without opening individual issues.

## 2) Issue template designs

GitHub issue templates should standardize intake and make requests actionable from the start. Use issue forms for structured requests and Markdown templates for lightweight requests.

### 2.1 Template set recommendation
Create these templates in `.github/ISSUE_TEMPLATE/`:

- `01-project-intake.yml`
- `02-task-request.yml`
- `03-risk-or-blocker.yml`
- `04-decision-request.yml`
- `config.yml`

Keep the first two as issue forms and the rest as shorter forms or Markdown templates depending on team preference.

### 2.2 Project intake form design
Best for new work that needs PMO review.

**Recommended fields:**
- Request title
- Requestor
- Business objective
- Problem statement
- Desired outcome
- Deadline or target date
- Priority
- Related project / milestone
- Attachments or reference links
- Risk / dependency notes

**Example structure:**
```yaml
name: Project Intake
about: Submit a new work request for PMO review
labels: ["pmo-intake"]
body:
  - type: input
    id: requestor
    attributes:
      label: Requestor
      placeholder: Name and team
    validations:
      required: true
  - type: textarea
    id: problem
    attributes:
      label: Problem statement
      description: What needs to change and why?
    validations:
      required: true
  - type: textarea
    id: outcome
    attributes:
      label: Desired outcome
      description: What does success look like?
    validations:
      required: true
  - type: input
    id: target-date
    attributes:
      label: Target date
      placeholder: YYYY-MM-DD
```

### 2.3 Task request form design
Best for smaller delivery items.

**Recommended fields:**
- Task summary
- Scope
- Definition of done
- Owner
- Target iteration
- Dependencies
- Acceptance criteria

This template keeps delivery requests short but still actionable.

### 2.4 Risk or blocker form design
Best for anything that could delay a milestone.

**Recommended fields:**
- Risk description
- Impact
- Likelihood
- Owner
- Escalation need
- Mitigation plan
- Due date for mitigation

This should automatically add labels such as:
- `risk`
- `blocker`
- `needs-triage`

### 2.5 Decision request form design
Best for approvals, tradeoffs, and leadership decisions.

**Recommended fields:**
- Decision needed
- Options considered
- Recommendation
- Deadline
- Approver
- Consequences of delay

### 2.6 Template chooser configuration
Use `.github/ISSUE_TEMPLATE/config.yml` to reduce noise.

Recommended settings:
- disable blank issues for most contributors
- keep a small number of high-quality templates
- route maintainers to a short triage path

Suggested configuration:
```yaml
blank_issues_enabled: false
contact_links:
  - name: PMO help
    url: https://github.com/jagmstar/github-features-audit/issues/new
    about: Use this for PMO-related requests and delivery coordination.
```

### 2.7 Template usage rules
- Put templates on the repository default branch.
- Keep file names numbered so the chooser appears in a predictable order.
- Use issue forms when you need required fields.
- Use Markdown templates when a simple guided prompt is enough.
- Add labels automatically where possible so project automation can catch the item.

## 3) PR template designs

Pull request templates should make review faster and reduce merge risk.

### 3.1 Recommended PR template files
Create:
- `.github/pull_request_template.md`
- optionally `.github/PULL_REQUEST_TEMPLATE/` for specialized templates

Suggested specialized PR templates:
- `docs-change.md`
- `workflow-change.md`
- `hotfix.md`

### 3.2 Standard PR template
The default PR template should ask for:
- linked issue
- summary of change
- reason for change
- testing completed
- rollout or rollback notes
- screenshots or evidence when relevant
- reviewer checklist

**Recommended template body:**
```md
## Related issue
- Closes #

## Summary
- What changed?
- Why was this needed?

## Validation
- [ ] I reviewed the change locally
- [ ] I verified the expected behavior
- [ ] I updated docs or notes if needed

## Risk / rollback
- Risk level:
- Rollback plan:

## Notes for reviewers
- Any special context?
```

### 3.3 Docs-only PR template
Use this for documentation and process changes.

Include:
- source of truth or issue reference
- files changed
- impact on workflow or policy
- whether screenshots are needed

### 3.4 Workflow-change PR template
Use this for GitHub Actions, Projects automation, and governance changes.

Include:
- risk of broken automation
- affected labels, fields, or boards
- whether the change can affect issue intake or status updates
- test plan with sample issue or dry-run evidence

## 4) Automation rules

Automation should reduce manual PMO administration without becoming brittle.

### 4.1 Built-in Projects workflows to enable
1. **Auto-add to project**
   - Add items automatically when they match a label or repository filter.
   - Recommended filters:
     - `label:pmo-intake`
     - `label:project-request`
     - `label:blocker`
     - `label:risk`

2. **Item added to project**
   - Set `Status` to `Intake` or `Todo` when a new item enters the project.
   - This prevents new work from landing in random states.

3. **Auto-archive items**
   - Archive finished items after they are closed and no longer active.
   - Use this for old completed work so the active board stays readable.

### 4.2 Recommended status transition rules
Use a combination of built-in workflows and lightweight Actions logic where needed.

**Rules:**
- New issue with `pmo-intake` label → auto-add to project
- Project item added → set status to `Intake`
- PMO triage complete → set status to `Planned`
- Work started → set status to `In Progress`
- Issue/PR blocked → set status to `Blocked`
- Review started → set status to `In Review`
- Item completed → set status to `Done`
- Closed and aged work → archive

### 4.3 Recommended Actions support
If more control is needed than the built-in workflows provide, use a small Actions workflow to synchronize project fields.

Use Actions for:
- syncing issue labels to project fields
- moving status when an issue is closed or a PR is merged
- posting reminders on overdue items
- creating weekly PMO summaries

### 4.4 Label conventions for automation
Use a small, stable label taxonomy.

**Suggested labels:**
- `pmo-intake`
- `project-request`
- `task`
- `risk`
- `blocker`
- `needs-triage`
- `needs-review`
- `done-ready`

Avoid label sprawl. Too many labels will weaken automation quality.

### 4.5 Automation control rules
- Automations should be deterministic and transparent.
- A change in automation should be documented in the PR.
- Avoid workflows that silently skip required work.
- Keep one owner responsible for project automation health.
- Review automation metrics monthly: stale items, mislabeled items, and manual overrides.

## 5) Milestone tracking

Milestones are the PMO layer that sit above the board.

### 5.1 Milestone model
Use milestones for time-bounded deliveries such as:
- monthly release
- quarterly objective
- client delivery package
- governance initiative

**Recommended milestone naming:**
- `2026-Q3 PMO Launch`
- `2026-08 Process Standardization`
- `Issue #6 Delivery`

### 5.2 Milestone fields and content
Each milestone should include:
- description
- target date
- linked issues and PRs
- completion percentage
- count of open and closed items
- key risks or dependencies

### 5.3 Milestone workflow
1. Create the milestone before work starts.
2. Assign every relevant issue and PR to that milestone.
3. Track progress weekly from the milestone page.
4. Reorder work inside the milestone to keep priority visible.
5. Close the milestone when deliverables are complete.
6. Archive completed project items after the milestone is stabilized.

### 5.4 Roadmap and milestone markers
Use the roadmap view to show milestone markers and delivery windows.

Recommended use:
- show target dates for each milestone
- add vertical markers for important release dates
- use roadmap to spot schedule collisions early

### 5.5 Milestone governance
- Every active project should have a current milestone.
- No issue should remain unassigned if it is part of a delivery.
- PMO should review milestone progress weekly.
- If a milestone slips, update the target date immediately and record the reason.

## 6) Rollout schedule

### Phase 1 — Foundation setup
**Timing:** Week 1

**Deliverables:**
- create the Projects v2 board
- define fields and statuses
- create milestone naming convention
- create the initial issue and PR templates
- document ownership rules

### Phase 2 — Intake standardization
**Timing:** Week 2

**Deliverables:**
- enable issue forms
- turn off or minimize blank issues
- train the team on using templates
- map labels to project fields
- start routing new requests through the PMO board

### Phase 3 — Automation enablement
**Timing:** Week 3

**Deliverables:**
- enable auto-add workflows
- set item-added status automation
- configure archiving rules
- test status transitions on sample issues and PRs
- validate that the board updates without manual intervention

### Phase 4 — Milestone discipline
**Timing:** Week 4

**Deliverables:**
- assign all active delivery work to milestones
- publish the first roadmap view
- begin weekly milestone review meetings
- collect feedback on board usability

### Phase 5 — Stabilization and optimization
**Timing:** Weeks 5-6

**Deliverables:**
- remove unused labels and fields
- refine templates based on actual usage
- add additional workflow automation only if it removes repeated manual work
- review reporting quality with leadership

## 7) Success metrics
Track these monthly:
- percentage of issues created from templates
- percentage of PRs using the PR template
- number of items with current owner and status
- average time from intake to planning
- average time from in progress to done
- number of overdue milestones
- number of stale or archived items
- number of manual project edits required per week

## 8) Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Too many board fields | Medium | Keep the first version lean and only add fields that are actively used |
| Templates are ignored | High | Disable blank issues where possible and make templates the easiest path |
| Automation becomes noisy | Medium | Automate only high-value transitions and review monthly |
| Milestones slip silently | High | Review milestone dates weekly and surface blockers immediately |
| Board becomes cluttered | Medium | Archive completed work on a regular schedule |

## 9) Recommended next steps
1. Create the PMO Projects v2 board.
2. Add the standard status, priority, owner, and milestone fields.
3. Publish the issue and PR templates in `.github/`.
4. Enable auto-add and item-added workflows.
5. Start weekly milestone reviews.
6. Measure template adoption and board hygiene after the first month.

## 10) Research basis
Official GitHub documentation reviewed for this plan:
- GitHub Projects quickstart and automation: https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects
- Adding items automatically to Projects: https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically
- Projects layouts, board, and roadmap: https://docs.github.com/en/enterprise-server@3.18/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/changing-the-layout-of-a-view
- Issue and pull request templates: https://docs.github.com/en/enterprise-server@3.20/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates
- Configuring issue templates: https://docs.github.com/en/enterprise-server@3.17/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
- Creating a pull request template: https://docs.github.com/en/enterprise-server@3.17/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
- Milestones overview: https://docs.github.com/en/enterprise-server@3.19/issues/using-labels-and-milestones-to-track-work/about-milestones
