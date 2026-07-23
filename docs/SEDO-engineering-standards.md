# SEDO Engineering Standards: How GitHub Free Features Enforce Quality

## Executive summary
GitHub Free features can enforce a strong engineering standard without extra tooling or paid security products. The most effective pattern is:

1. Use a **template repository** to seed every new project with the same guardrails.
2. Protect the default branch with **branch protection rules** or **rulesets**.
3. Route ownership through **CODEOWNERS** so the right people must review the right files.
4. Make **GitHub Actions** the enforcement engine for linting, formatting, testing, and commit/PR convention checks.
5. Treat **status checks** as merge gates, not as informational signals.
6. Lock down repository settings so the default branch and release flow stay stable.

> Important constraint: GitHub's native commit-metadata restrictions are described in the ruleset docs as **GitHub Enterprise-only**. For the free baseline, enforce commit conventions with GitHub Actions and required status checks instead of relying on metadata rules.

---

## 1) Standard operating model

### Non-negotiable rules
- `main` is the protected integration branch.
- All changes land through a pull request.
- At least one approval is required before merge.
- CODEOWNERS approval is required for sensitive paths.
- CI checks must pass before merge.
- Force pushes to `main` are blocked.
- Merge history should stay readable and predictable.
- Head branches are deleted after merge.

### Why this works
This is a cheap but effective control stack:
- **Pull requests** create review and traceability.
- **CODEOWNERS** ensures the right reviewers are pulled in automatically.
- **Required status checks** stop broken code at the gate.
- **Actions** automate the checks rather than depending on manual discipline.
- **Repository settings** reduce accidental drift and destructive changes.

---

## 2) Template repository design

A template repo is the fastest way to make standards repeatable for every new project. The template should contain the policies, automation, and documentation that every repo needs from day one.

### Recommended template contents
```text
.
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CODEOWNERS
├── .editorconfig
├── .gitignore
├── .github/
│   ├── pull_request_template.md
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
│       ├── ci.yml
│       ├── lint.yml
│       └── commit-convention.yml
├── docs/
│   └── engineering-standards.md
└── language/tooling configs
    ├── formatter config
    ├── linter config
    └── test config
```

### What each file does
- **README.md**: explains purpose, setup, run, test, and release flow.
- **CONTRIBUTING.md**: defines branch naming, PR expectations, review rules, and merge policy.
- **SECURITY.md**: gives a security contact path.
- **CODEOWNERS**: defines ownership by area.
- **pull_request_template.md**: standardizes PR descriptions and checklists.
- **workflows/**: runs the enforcement checks on every PR.
- **formatter/linter/test configs**: keep local and CI behavior aligned.

### Template rule
Every new repository should be created from the template, not assembled manually. That keeps standards consistent and removes setup ambiguity.

---

## 3) Branch protection and rulesets

### Baseline recommendation
Use a rule on `main` that requires the pull request workflow to succeed before merge.

If rulesets are available in the repo plan, prefer a **ruleset** because it is easier to discover and can enforce policies consistently across matching branches. If not, use classic **branch protection rules** on `main`.

### Minimum protection set for `main`
- Require a pull request before merging.
- Require at least 1 approving review.
- Require code owner review when files under owned paths change.
- Require these checks to pass:
  - formatting
  - linting
  - tests
  - commit/PR convention validation
- Block force pushes.
- Dismiss stale approvals when new commits change the diff.
- Restrict merges to the allowed merge method.

### Recommended merge method
Use **squash merge** as the default.

Why:
- It keeps `main` history concise.
- It makes convention enforcement easier because you can validate the **PR title** and use that as the squash commit message.
- It reduces noise from exploratory commits and WIP commits.

### Ruleset vs branch protection
- **Ruleset**: better for reusable policy and multiple targets.
- **Branch protection**: the simplest guaranteed control for a single default branch.

### Free-feature guidance
The free baseline should rely on the standard merge gates above. Avoid designing a policy that depends on enterprise-only metadata restrictions.

---

## 4) Required pull request reviews

### Standard review policy
- One approving review required for routine changes.
- Two approvals for high-risk areas if the repo is small or sensitive.
- Code owner approval required when the PR touches code owned by a protected area.
- Reviews are dismissed if the PR changes materially after approval.

### Review expectations for authors
Every PR should answer these questions:
- What changed?
- Why did it change?
- How was it tested?
- What risk does it introduce?
- Is there a linked issue or ticket?

### Review expectations for reviewers
Reviewers should check:
- correctness
- readability
- test coverage
- naming and formatting
- security or data-handling impact
- whether the change belongs in the current PR

---

## 5) CODEOWNERS structure

CODEOWNERS is the most direct way to route review responsibility.

### Placement
Put the file in one of these locations, in this order of precedence:
1. `.github/CODEOWNERS`
2. `CODEOWNERS` at repo root
3. `docs/CODEOWNERS`

### Recommended ownership model
```text
# Default owners for the repository
* @company/platform-leads

# Workflow and release automation
.github/workflows/ @company/devops

# Documentation and standards
/docs/ @company/tech-writing
*.md @company/tech-writing

# Security-sensitive files
SECURITY.md @company/security
.github/CODEOWNERS @company/platform-leads
```

### Rules to follow
- Owners must have **write** access.
- Keep the file small and readable.
- Put the repository owner or platform team in charge of the CODEOWNERS file itself.
- Use branch protection/rulesets to require code owner review.

### Why this matters
CODEOWNERS turns tribal knowledge into an enforceable review path. It prevents a security or platform change from being merged without the right reviewer.

---

## 6) Commit message conventions

### Policy recommendation
Use **Conventional Commits** for human-authored commits and PR titles.

Examples:
- `feat: add onboarding checklist`
- `fix: handle empty config file`
- `docs: clarify review policy`
- `chore: update workflow permissions`

### Enforcement strategy on GitHub Free
Because GitHub's native commit-metadata restrictions are Enterprise-only, enforce conventions like this:
1. Make the PR title follow the convention.
2. Use **squash merge** so the final commit message inherits the PR title.
3. Add a GitHub Actions job that validates the PR title and/or commit messages.
4. Make that job a required status check.

### Good convention checks
- PR title matches the Conventional Commits pattern.
- Commit messages do not contain disallowed prefixes.
- Merge commits are not used on protected branches.
- The final squash commit message follows the same pattern as the PR title.

### Why this is the right free-tier approach
It keeps the standard enforceable without depending on plan-gated repository metadata rules.

---

## 7) GitHub Actions for linting and formatting

GitHub Actions is the automation layer that makes standards real. Each repository should run the same commands locally and in CI.

### Required CI jobs
- **format**: verify formatting is clean
- **lint**: run static analysis
- **test**: run unit/integration tests
- **convention**: validate commit/PR title format

### Workflow pattern
- Trigger on `pull_request` and `push` to protected branches.
- Use `actions/checkout`.
- Install the project runtime.
- Install dependencies.
- Run format/lint/test commands.
- Publish the result as a required check.

### Example workflow shape
```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Set up runtime
        run: <install runtime>
      - name: Install dependencies
        run: <install deps>
      - name: Check formatting
        run: <format check>
      - name: Run linter
        run: <lint command>
      - name: Run tests
        run: <test command>
```

### CI rules
- CI must fail if formatting fails.
- CI must fail if lint fails.
- CI must fail if tests fail.
- CI must fail if the PR title or commit message format is invalid.

### Why this matters
GitHub Actions turns quality standards into a merge gate. Reviewers should not have to manually police formatting or basic correctness.

---

## 8) Status checks as merge gates

Status checks should be the final authority before merge.

### Required status checks
At minimum, require:
- formatting check
- lint check
- test suite
- commit/PR convention check

### Optional status checks
- docs build
- type-checking
- package/dependency audit
- security-oriented checks if available in the repo's normal workflow

### Enforcement principle
If a check is required, it must be red/green deterministic and visible in the PR. No informal checks should be required for merge.

### Recommended policy
- No merge when checks are pending.
- No merge when checks are failing.
- No bypass unless an admin explicitly approves an exception path.

---

## 9) Repository settings best practices

These settings keep the repo stable and reduce the chance of accidental damage.

### Default branch
- Use `main` as the default branch.
- Make sure protected settings target `main`.

### Branch deletion and history
- Auto-delete head branches after merge.
- Block force pushes to protected branches.
- Prefer squash merges for protected integration branches.

### Visibility and forks
- Use the least permissive visibility that fits the project.
- For internal code, keep repositories private or internal as appropriate.
- Restrict forking when the repository contains sensitive data.

### Ownership and access
- Limit who can change repo settings.
- Keep maintainers or platform owners in charge of branch protection, rulesets, and CODEOWNERS.
- Review repository access regularly.

### Why these settings matter
Engineering standards fail if the repo itself is easy to mutate outside the review process. Settings should support the policy, not undermine it.

---

## 10) Recommended rollout sequence

1. Create the template repository.
2. Add README, CONTRIBUTING, SECURITY, CODEOWNERS, PR template, and CI workflows.
3. Set the default branch to `main`.
4. Protect `main` with required reviews and required checks.
5. Add CODEOWNERS paths for security, docs, and workflow files.
6. Make the CI workflow required.
7. Make squash merge the default.
8. Validate commit/PR conventions in GitHub Actions.
9. Document the policy in the repo and in the template.

---

## 11) Final standards statement

**If a change is not reviewed, not owned, not tested, and not traceable, it does not merge.**

That is the engineering standard this GitHub Free feature set should enforce.

---

## Sources used
- GitHub Docs: Creating a repository from a template — https://docs.github.com/en/enterprise-server@3.21/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template
- GitHub Docs: Managing and standardizing pull requests — https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/managing-and-standardizing-pull-requests
- GitHub Docs: About code owners — https://docs.github.com/en/enterprise-server@3.18/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- GitHub Docs: Available rules for rulesets — https://docs.github.com/en/enterprise-server@3.18/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- GitHub Docs: About repositories / repository management best practices — https://docs.github.com/en/enterprise-server@3.18/repositories/creating-and-managing-repositories/about-repositories
- GitHub Docs: Enforcing repository management policies in your enterprise — https://docs.github.com/en/enterprise-server@3.19/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-repository-management-policies-in-your-enterprise
- GitHub Docs: Creating an example workflow — https://docs.github.com/en/actions/tutorials/create-an-example-workflow
- GitHub Docs: GitHub Advanced Security overview — https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security
