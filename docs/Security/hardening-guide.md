# Security Hardening Guide for Client Repositories

Prepared by JAGM IT Company
Owner: CISO
Applies to: client repositories managed or maintained by JAGM IT Company

## Purpose

This guide defines the minimum GitHub security baseline for client repositories. The goal is to reduce the chance of unauthorized changes, leaked secrets, vulnerable dependencies, and unreviewed or unverified code entering protected branches.

These controls should be treated as standard delivery requirements, not optional extras.

## Baseline security standard

Every client repository should, at minimum, implement the following controls:

1. Branch protection rules on the default branch
2. Secret scanning enabled
3. CodeQL code scanning enabled
4. A repository-level `SECURITY.md`
5. Dependabot configuration in `.github/dependabot.yml`
6. Signed commits required for protected branches

If a repository is public, these controls are generally available in GitHub Free. If a repository is private, some features may require additional GitHub security licensing. Even when licensing is needed, the control objective remains the same.

## 1) Branch protection rules

Protect the default branch, typically `main`.

### Required settings

At a minimum, configure the protected branch or ruleset to:

- **Require a pull request before merging**
- **Require at least one approving review** before merge
- **Require status checks to pass before merging**
- Block direct pushes to the protected branch
- Block force pushes
- Block branch deletion

### Recommended review settings

Use the following review rules where supported:

- Require code owner review for sensitive repositories
- Dismiss stale reviews when new commits are pushed
- Require conversation resolution before merging
- Require linear history if the team can support squash or rebase merges consistently

### Required status checks

Only require checks that are stable and meaningful. Common required checks include:

- unit tests
- linting
- build validation
- CodeQL analysis
- dependency or policy validation if applicable

### Why this matters

Branch protection ensures that changes are reviewed, validated, and merged through a controlled process. This is the foundation that prevents accidental breakage and reduces the risk of malicious changes reaching production branches.

## 2) Secret scanning enablement

Enable secret scanning for every repository that supports it.

### Required actions

- Turn on secret scanning alerts
- Enable push protection where available
- Review and triage alerts promptly
- Rotate any exposed secret immediately
- Treat leaked credentials as security incidents, not cleanup tasks

### Operational expectations

When a secret alert appears:

1. Confirm whether the secret is real or a false positive
2. If real, revoke or rotate the credential immediately
3. Remove the secret from the repository history where appropriate
4. Record the incident and remediation steps
5. Review the root cause to prevent recurrence

### Why this matters

Secrets committed to source control can be copied instantly and reused outside the organization. Secret scanning is one of the fastest ways to reduce that risk.

## 3) CodeQL enablement

Enable CodeQL code scanning for supported languages in the repository.

### Recommended setup

- Add a CodeQL workflow under `.github/workflows/codeql.yml`
- Run CodeQL on pull requests and on a schedule
- Analyze the primary languages used in the repository
- Require the CodeQL check before merge on protected branches

### Suggested workflow behavior

A strong default configuration includes:

- `pull_request` trigger for merge review
- `schedule` trigger, at least weekly
- language matrix for the repository’s main stack
- upload of results to GitHub code scanning

### Why this matters

CodeQL identifies insecure coding patterns and vulnerability classes before they become production issues. Required CodeQL checks turn security review into a merge gate instead of an after-the-fact activity.

## 4) SECURITY.md template

Every client repository should include a repository-level `SECURITY.md` file at the root of the repository.

### Minimum content requirements

The security policy should include:

- where to report vulnerabilities privately
- what not to disclose publicly
- expected response time
- supported versions or supported branches
- who owns security intake for the repository

### Recommended policy language

Keep the file short, clear, and easy to follow. The policy should direct reporters to a private disclosure path such as a security email address or GitHub Security Advisory workflow.

### Why this matters

A security policy gives external reporters a safe, predictable way to disclose vulnerabilities without public escalation.

## 5) Dependabot configuration

Add Dependabot configuration at `.github/dependabot.yml`.

### Minimum recommended configuration

Configure Dependabot to:

- monitor the dependency ecosystems used by the repository
- run on a regular schedule
- create version update pull requests
- create security update pull requests where supported
- group updates when it improves review quality

### Suggested schedule

For most client repositories:

- **version updates:** weekly
- **security updates:** automatic when vulnerabilities are detected

### Practical guidance

- Keep update PRs small and reviewable
- Use grouping carefully; do not combine unrelated high-risk changes into a single update PR
- Require the same CI checks on Dependabot PRs as on human PRs
- Review dependency updates even when they are automated

### Why this matters

Dependabot reduces exposure to known vulnerabilities and prevents dependency drift from building up over time.

## 6) Signed commits requirement

Require signed commits on protected branches.

### Required actions

- Enable **Require signed commits** for the protected branch or ruleset
- Ensure maintainers use supported signing methods
- Accept commit signatures from GPG, SSH, or S/MIME where appropriate

### Operational guidance

- Verify that GitHub shows commits as verified before enabling strict enforcement broadly
- Educate maintainers on how to sign commits in their normal workflow
- Use signed commits together with pull requests and code review, not as a replacement for them

### Why this matters

Signed commits improve provenance and make it harder for unauthorized actors to impersonate a trusted contributor or tamper with history.

## Recommended implementation order

1. Protect the default branch
2. Require pull requests and review
3. Require status checks
4. Require signed commits
5. Enable secret scanning
6. Add CodeQL scanning
7. Add Dependabot configuration
8. Publish `SECURITY.md`

## Repository owner checklist

Before a client repository is considered hardened, confirm the following:

- [ ] Default branch is protected
- [ ] Pull requests are required for merges
- [ ] Review approval is required
- [ ] Required status checks are enforced
- [ ] Secret scanning is enabled
- [ ] CodeQL is enabled and required
- [ ] `SECURITY.md` exists at the repository root
- [ ] Dependabot configuration exists in `.github/dependabot.yml`
- [ ] Signed commits are required
- [ ] Force pushes and branch deletion are blocked

## Final note

These controls work best as a package. Branch protection without scanning leaves security gaps. Scanning without branch protection leaves unsafe merge paths. Signed commits without review do not stop flawed code. For client repositories, the security baseline should be complete, enforced, and visible to every contributor.