# CISO Security Audit: Free GitHub Security Features

Prepared for GitHub issue #5 for JAGM IT Company.

## Executive summary

GitHub provides a useful free security baseline even before any paid add-ons are purchased. For public repositories, that baseline includes code scanning, secret scanning, Dependabot alerts and security updates, protected branches, tag protection, commit signature verification, and repository security advisories. In addition, some core supply-chain controls such as the dependency graph and Dependabot alerts are included in all plans.

The biggest security gap is not the absence of tools, but the absence of consistent rollout. This repository currently does not track the main security configuration artifacts that would prove adoption, such as a CodeQL workflow, Dependabot configuration, a security policy, or repository protection policy documentation.

## Scope and assumptions

- Scope: GitHub.com free security capabilities that can reduce risk for JAGM IT Company.
- Assumption: the company uses public repositories or wants its public-facing repositories hardened first.
- Assumption: repository-level settings are managed in GitHub, while this document records the audit and rollout plan.
- This document does **not** claim that any feature is already enabled in the live GitHub repository settings.

## Free GitHub security feature inventory

| Feature | Free availability | Why it matters | Notes for JAGM IT Company |
|---|---|---|---|
| Dependency graph | Included in GitHub plans and enabled by default | Creates the dependency inventory that powers downstream security features | Treat as foundational; without it, Dependabot visibility is reduced |
| Dependabot alerts | Included in all plans | Detects vulnerable and malicious dependencies using the GitHub Advisory Database | Enable and triage regularly |
| Dependabot security updates | Included without extra GHAS purchase | Opens PRs to remediate vulnerable dependencies automatically | Best low-effort supply-chain control |
| Dependabot version updates | Free | Keeps dependencies current and reduces future vulnerability accumulation | Operational hygiene, not purely security, but strongly recommended |
| Code scanning with CodeQL | Free for public repositories | Finds code vulnerabilities and security mistakes before merge | Private/internal repositories require paid GitHub Code Security |
| Secret scanning | Free for public repositories | Detects committed secrets and credentials | Private/internal repositories require paid GitHub Secret Protection |
| Repository security advisories | Free for public repositories | Supports private disclosure and coordinated vulnerability publication | Pair with a SECURITY.md policy |
| Security policy / private vulnerability reporting | Free for public repositories | Gives external reporters a safe path to disclose issues | Important for open-source or public-facing projects |
| Branch protection rules | Available for public repositories on GitHub Free | Enforces reviews, status checks, signed commits, and merge restrictions | This is the core merge-control layer |
| Required status checks | Free when used through branch protection | Prevents merging when CI checks fail | Works best with the existing CI workflow |
| Commit signature verification | Free feature | Verifies authorship/provenance through GPG, SSH, or S/MIME signatures | Strengthens trust in release and merge history |
| Tag protection rules | Available for public repositories on GitHub Free | Prevents accidental or malicious creation, deletion, or changes to protected tags | Important for release integrity |
| Security risk assessment | Free for GitHub Team and Enterprise organizations | Measures exposure to leaked secrets and code vulnerabilities | Optional extra assessment if the org is on Team/Enterprise |

## Current gaps observed in this repository

Based on the tracked files in this repository, the following security artifacts are missing or not yet documented:

| Gap | Current state in repo | Risk created |
|---|---|---|
| CodeQL workflow | No CodeQL workflow file is tracked | Vulnerabilities can move through pull requests without code-scanning coverage |
| Dependabot config | No `.github/dependabot.yml` is tracked | Vulnerable dependencies may linger longer than necessary |
| Security policy | No `SECURITY.md` is tracked | Reporters may not know how to disclose vulnerabilities privately |
| Protected branch policy documentation | Not documented in repo | Merge safety depends on manual enforcement instead of policy |
| Tag protection process | Not documented in repo | Release tags may be changed without a clear control process |
| Signed-commit requirement | Not documented in repo | Commit provenance is weaker than it should be |

## Recommended implementation plan

1. **Add a security policy**
   - Create `SECURITY.md` with private disclosure instructions.
   - Link the policy from the repository home and issue templates if used.

2. **Enable dependency monitoring**
   - Turn on Dependabot alerts.
   - Add `dependabot.yml` for version updates and automated security updates.
   - Review alerts on a weekly cadence until backlog is stable.

3. **Add code scanning**
   - Add a CodeQL workflow for the main languages used in the repository.
   - Require the CodeQL check before merge on protected branches.

4. **Harden merge controls**
   - Protect `main` with required reviews, required status checks, and linear history where practical.
   - Require signed commits for maintainers.
   - Block force-pushes and branch deletion on protected branches.

5. **Protect release tags**
   - Add tag protection rules for release tags such as `v*` or `release-*`.
   - Limit who can create or rewrite release tags.

6. **Operationalize secret prevention**
   - Enable secret scanning on public repositories.
   - Treat secret alerts as incident tickets, not just cleanup tasks.
   - Rotate any exposed credential immediately.

7. **Measure adoption**
   - Track open Dependabot alerts, code-scanning alerts, and secret-scanning alerts.
   - Review the metrics monthly and report trend lines to leadership.

## Risk reduction matrix

| Control | Primary risk reduced | Expected impact | Effort | Priority |
|---|---|---|---|---|
| Secret scanning | Credential leakage | Very high | Low | P1 |
| Dependabot alerts | Known vulnerable dependencies | Very high | Low | P1 |
| Dependabot security updates | Slow remediation of dependency CVEs | High | Low | P1 |
| CodeQL code scanning | Application logic and insecure-code defects | High | Medium | P1 |
| Branch protection with required status checks | Unsafe merges and broken builds | High | Low | P1 |
| Signed commits | Impersonation and tampered history | Medium-high | Medium | P2 |
| Tag protection | Release tampering | Medium-high | Low | P2 |
| Security policy and private reporting | Delayed disclosure and noisy public reporting | Medium | Low | P2 |
| Dependency graph | Blind spots in dependency inventory | Medium | Low | P2 |
| Security risk assessment | Unmeasured exposure across the org | Medium | Low | P3 |

## Evidence consulted

Official GitHub documentation used for this audit:

- About GitHub Advanced Security: https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security
- Supply chain security overview: https://docs.github.com/en/code-security/concepts/supply-chain-security/supply-chain-security
- Dependabot alerts: https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts
- Dependabot security updates and pull requests: https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-pull-requests
- Secret scanning: https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning
- Enable secret scanning: https://docs.github.com/en/code-security/how-tos/secure-your-secrets/detect-secret-leaks/enable-secret-scanning
- Repository security advisories: https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories
- Protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- Commit signature verification: https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification

## Conclusion

GitHub’s free security features are strong enough to build a meaningful baseline, especially on public repositories. For JAGM IT Company, the immediate win is to combine secret scanning, Dependabot, CodeQL, and branch protection so that security is enforced automatically rather than by convention.

The repository should treat these controls as standard delivery requirements, not optional extras.