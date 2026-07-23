# QAO Quality Strategy: GitHub QA and Testing

Prepared for GitHub issue #7 for JAGM IT Company.

## Executive summary

GitHub has enough free-quality features to build a strong, policy-driven QA system around pull requests and protected branches. The core model for JAGM IT Company should be:

1. Validate every change in GitHub Actions.
2. Run tests across a matrix of runtime / OS combinations.
3. Scan code automatically with CodeQL.
4. Keep dependencies current with Dependabot.
5. Require passing status checks before merge.
6. Use a merge queue so the branch is always tested as it will actually be merged.

The goal is to make quality enforcement automatic, repeatable, and visible in GitHub rather than dependent on manual review alone.

## Scope and assumptions

- Assumption: this repository is used as a GitHub feature audit and may expand later into code-enabled projects.
- Assumption: the primary branch is `main`.
- Assumption: the company wants a template that works for public repositories first, with a path to private-repo hardening later.
- Assumption: workflow names and job names should be stable so they can be reused as required status checks.

## Research summary: GitHub features that matter for QA

### 1) GitHub Actions CI
GitHub Actions is the execution layer for validation, build, and deployment automation. It supports reusable workflows, job outputs, environments, and matrix builds. This makes it a good fit for repeatable QA gates.

Key observations:
- Use `pull_request` for validation of proposed changes.
- Use `push` on `main` for post-merge validation and release prep.
- Use `merge_group` when merge queues are enabled so queued PRs still receive checks.
- Keep workflow permissions minimal, especially for validation jobs.

### 2) Matrix testing
Matrix jobs let us run the same test suite across multiple operating systems, language versions, or package-manager variants.

Key observations:
- GitHub Actions exposes `matrix` and `strategy` contexts for matrix execution.
- `exclude` lets us avoid invalid combinations.
- `fail-fast: false` is useful when we want a full picture of failures instead of stopping on the first broken axis.
- Matrix testing should be kept intentionally small at first and expanded only where risk justifies the cost.

### 3) CodeQL code scanning
CodeQL is GitHub’s code-analysis engine for code scanning. It can run on pushes, pull requests, and schedules, and it can be configured to analyze multiple languages via a matrix.

Key observations:
- Default scans on `push` and `pull_request` are the right baseline.
- A scheduled weekly scan catches issues introduced by dependency drift or newly published queries.
- The `security-and-quality` suite is a strong default for higher-value repositories because it includes both security and maintainability queries.
- CodeQL results can be turned into merge protection so high-severity alerts block merge.

### 4) Dependabot
Dependabot keeps dependencies current and can open PRs for both version updates and security updates.

Key observations:
- Add `dependabot.yml` for languages plus `github-actions` dependency updates.
- Use weekly updates by default, daily for high-change ecosystems if needed.
- Grouping reduces PR noise and makes review manageable.
- Dependabot PRs should go through the same CI, coverage, and security gates as human-authored PRs.

### 5) Required status checks
Status checks are the enforcement mechanism that prevents broken or unscanned changes from merging.

Key observations:
- Required checks must pass on the latest commit SHA.
- Do not rely on workflow skipping as a way to bypass quality gates.
- If a workflow is required, it must always produce a result for the branch policy.
- Strict status checks are safer when the branch must always be current with `main`.

### 6) Merge queues
Merge queues reduce the risk of “green on branch, red after merge” by testing the exact batch of queued changes together.

Key observations:
- Workflows must listen to `merge_group` or queue checks will not run.
- Merge queue settings can require every queue entry to pass required checks.
- Build concurrency can be capped so queued items do not overwhelm CI.
- Merge queue is the right final gate once required checks are stable.

## CI/CD template designs

### Template A: Pull request validation workflow
**File:** `.github/workflows/ci.yml`

**Purpose:** fast feedback for every pull request.

**Trigger design:**
- `pull_request` on `main`
- `merge_group` for queue validation
- optional `push` on `main` for post-merge verification

**Jobs:**
- lint
- unit tests
- coverage check
- artifact upload for reports

**Design principles:**
- Minimal `GITHUB_TOKEN` permissions.
- Fail fast on lint, but keep tests and coverage visible.
- Publish test and coverage reports as artifacts.
- Name checks consistently so they can be required by branch protections.

**Suggested check names:**
- `ci / lint`
- `ci / unit-tests`
- `ci / coverage`

```yaml
on:
  pull_request:
    branches: [main]
  merge_group:
    branches: [main]

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps: []

  unit-tests:
    runs-on: ubuntu-latest
    steps: []

  coverage:
    runs-on: ubuntu-latest
    steps: []
```

### Template B: Matrix test workflow
**File:** `.github/workflows/test-matrix.yml`

**Purpose:** validate supported runtime and OS combinations.

**Recommended matrix model:**
- Linux on every PR
- Windows only when the stack needs it
- macOS only when the stack needs it
- multiple language/runtime versions where compatibility risk exists

**Recommended matrix rules:**
- `fail-fast: false`
- exclude unsupported combinations
- keep the matrix focused on combinations that users actually run in production

**Suggested check names:**
- `matrix / linux`
- `matrix / windows`
- `matrix / macos`

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
        runtime: ['current', 'previous']
        exclude:
          - os: windows-latest
            runtime: previous
    runs-on: ${{ matrix.os }}
    steps: []
```

### Template C: CodeQL workflow
**File:** `.github/workflows/codeql.yml`

**Purpose:** prevent vulnerable code from merging.

**Trigger design:**
- `pull_request` to `main`
- `push` to `main`
- scheduled weekly scan
- `merge_group` so merge-queue candidates are scanned too

**Recommended analysis strategy:**
- use the default language detection or a language matrix if the repo becomes multi-language
- prefer `security-and-quality` for mature repositories
- keep the workflow on the default branch

**Suggested check name:**
- `codeql / analyze`

```yaml
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  schedule:
    - cron: '20 14 * * 1'
  merge_group:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps: []
```

### Template D: Dependabot configuration
**File:** `.github/dependabot.yml`

**Purpose:** keep ecosystem and GitHub Actions dependencies fresh.

**Recommended cadence:**
- weekly for most ecosystems
- daily only for high-risk, fast-moving, or security-sensitive components

**Recommended pattern:**
- one block per ecosystem
- group low-risk updates where it reduces PR noise
- keep version updates and security updates on the same enforcement path

**Suggested ecosystems to monitor when present:**
- `github-actions`
- language package managers in use by the repo

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

### Template E: Release gate workflow
**File:** `.github/workflows/release.yml`

**Purpose:** ensure only fully validated changes can be promoted.

**Trigger design:**
- tag push, or manual dispatch, after required checks pass on `main`

**Jobs:**
- package/build
- verify release artifact
- deploy to staging or publish preview
- production promotion only after environment approval

**Design principle:**
- release jobs should depend on the same quality gates used by pull requests, not a separate shortcut path.

## Test automation plan

### 1) Unit tests
Run on every pull request and merge queue event.

Goals:
- verify business logic
- verify branch-specific behavior
- keep test execution fast enough to run on every change

Policy:
- any new feature or bug fix must include tests
- tests should be deterministic and isolated

### 2) Integration tests
Run on pull requests for high-risk flows and on `main` after merge.

Goals:
- verify components working together
- catch environment assumptions
- validate external API integrations where appropriate

Policy:
- integration tests should be tagged so they can be included selectively
- use test fixtures and service containers where needed

### 3) Smoke tests
Run after deployment to staging or preview environments.

Goals:
- confirm the release is actually usable
- detect configuration or deployment regressions
- validate critical paths before production promotion

Policy:
- smoke tests should be short and high-signal
- failing smoke tests should block promotion

### 4) Regression tests
Run nightly or on a scheduled cadence for broad coverage.

Goals:
- protect against issues not covered by PR-level tests
- catch drift from dependency updates or environment changes

Policy:
- prioritize the most business-critical paths
- keep results visible and actionable

### 5) Flaky test management
Goals:
- isolate flaky tests from stable gates
- prevent noisy failures from eroding trust in CI

Policy:
- flaky tests must be tracked as defects
- do not leave important gates flaky for long periods
- quarantine only as a temporary measure

## Coverage targets

### Changed-code coverage target
**Target:** at least **90% coverage for changed code** on every merged pull request.

This is the primary quality metric because it measures the code being introduced or modified, not just the historical coverage of the whole repository.

### Coverage policy
- PRs must not merge if changed-code coverage drops below 90%.
- Whole-repo coverage should be tracked as a health metric, but changed-code coverage is the enforcement gate.
- Coverage reports should be published as workflow artifacts so reviewers can inspect the diff impact.
- If a change touches untested legacy code, the author must either add tests or document the risk with an explicit exception.

### Recommended reporting
- line coverage
- branch coverage where the tooling supports it
- per-package or per-module coverage for large repositories

## Security scanning

### CodeQL
- Run on PRs, pushes to `main`, and a weekly schedule.
- Keep scan results visible in the repository security tab.
- Treat high-severity alerts as merge blockers.
- If the repo becomes multi-language, use a matrix so each language is scanned in parallel.

### Dependabot alerts and updates
- Enable Dependabot alerts.
- Enable Dependabot security updates.
- Use version updates to reduce future vulnerability accumulation.
- Review dependency PRs with the same quality checks as human-authored PRs.

### Secret prevention
- Enable secret scanning where available.
- Treat any secret alert as an incident, not just a cleanup task.
- Rotate any exposed secret immediately.

### Optional reinforcement
- Add dependency review if the repo later introduces third-party dependency churn at scale.
- Use commit signature rules and tag protection for release integrity.

## Enforcement gates

The following gates should be required before merge into `main`:

1. **Lint gate** — no formatting, style, or static-analysis errors.
2. **Unit test gate** — all unit tests pass.
3. **Matrix gate** — supported runtime/OS combinations pass.
4. **Coverage gate** — changed code coverage is at least 90%.
5. **CodeQL gate** — no blocking code-scanning alerts.
6. **Dependabot gate** — dependency updates run through the same validation path.
7. **Merge queue gate** — queue candidates must pass `merge_group` checks.
8. **Branch protection gate** — no direct merge without the required checks.

### Enforcement recommendations
- Require pull requests for `main`.
- Require the repository to be up to date before merge if the branch has frequent conflicts.
- Require the named checks above as required status checks.
- Require merge queue once CI is stable enough to support it.
- Block force pushes on protected branches.
- Use review requirements for high-risk changes.

## Recommended rollout sequence

1. Add the CI workflow and required status checks.
2. Add the test matrix.
3. Add coverage publishing and the 90% changed-code rule.
4. Add CodeQL scanning.
5. Add Dependabot configuration.
6. Enable protected-branch or ruleset enforcement.
7. Turn on merge queue after the required checks are stable.

## Evidence consulted

Official GitHub documentation used for this strategy:

- GitHub Actions contexts and matrix execution: https://docs.github.com/enterprise-cloud@latest/actions/reference/workflows-and-actions/contexts
- GitHub Actions matrix examples: https://docs.github.com/en/enterprise-server@3.19/actions/tutorials/build-and-test-code/python
- Code scanning overview: https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning
- CodeQL workflow configuration options: https://docs.github.com/en/enterprise-server@3.20/code-security/reference/code-scanning/workflow-configuration-options
- Dependabot configuration reference: https://docs.github.com/en/enterprise-cloud@latest/code-security/reference/supply-chain-security/dependabot-options-reference
- Required status checks and merge queue behavior: https://docs.github.com/en/enterprise-server@3.18/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- Required status checks troubleshooting and merge_group trigger guidance: https://docs.github.com/en/enterprise-server@3.17/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks
- Pull request standardization and rulesets overview: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/managing-and-standardizing-pull-requests

## Conclusion

A good QA system on GitHub is not just “run tests.” It is a chain of controls: matrix validation, coverage thresholds, security scanning, dependency automation, and merge enforcement. If JAGM IT Company applies those controls consistently, quality becomes a default property of the delivery process instead of a manual afterthought.