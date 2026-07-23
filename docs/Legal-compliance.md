# Legal Compliance Guide: GitHub Free Features for JAGM IT Company

Issue: #15  
Repository: `jagmstar/github-features-audit`  
Prepared by: Legal track for JAGM IT Company

## Executive summary

GitHub's free features can support a strong legal and compliance posture if they are configured intentionally. The most important legal controls for JAGM IT Company are:

- clear licensing for every public repository
- a published security policy for responsible disclosure
- automated dependency vulnerability monitoring
- account and billing practices that comply with GitHub's terms
- a documented data residency and privacy posture
- license compliance controls for open source usage
- a visible code of conduct for community-facing work

The practical conclusion is that legal compliance on GitHub is not a single setting. It is a set of repeatable repository, organization, and account practices that reduce ambiguity for contributors, customers, and auditors.

## Scope and assumptions

This guide focuses on the GitHub features that are most relevant to legal, licensing, privacy, and compliance work for a small company using GitHub Free or otherwise relying on free GitHub features wherever possible.

Assumptions:

- JAGM IT Company uses GitHub for both internal work and public-facing repositories.
- Public repositories are likely to be the main venue for free features.
- Legal review is handled internally, but the company wants practical controls that engineering teams can follow.
- This document is a policy guide, not a substitute for jurisdiction-specific legal advice.

## 1) LICENSE files: make ownership and reuse terms explicit

### What GitHub does

GitHub detects repository licenses by looking for a license file in the repository root. GitHub documents that license detection uses the Licensee library, and it can recognize common file names such as `LICENSE`, `LICENSE.txt`, `LICENSE.md`, or similar variants.

GitHub also helps users filter repositories by license, which makes licensing a discoverability and trust issue, not just a legal one.

### Why it matters legally

If a repository has no explicit license, the default legal position is often “all rights reserved.” That creates uncertainty for customers, contributors, and downstream users. For JAGM IT Company, that ambiguity can block reuse, slow collaboration, and create avoidable compliance questions.

### Recommendation

- Add a license file to every public repository.
- Make the license choice intentional and consistent with the business purpose of the repo.
- For company-owned code, ensure the license matches the intended distribution model.
- For documentation or demo repos, choose a license that clearly defines reuse rights.

### Operational checklist

- [ ] Place the license file in the repository root
- [ ] Use a standard SPDX-compatible license text when possible
- [ ] Confirm GitHub recognizes the license badge or license metadata
- [ ] Review whether the repo should be permissive, restrictive, or source-available

## 2) Security advisories and private vulnerability reporting

### What GitHub does

GitHub supports coordinated vulnerability disclosure through security advisories and private reporting workflows. When configured correctly, maintainers can receive vulnerability reports privately rather than through public issues.

### Why it matters legally

A public vulnerability report can expose users to unnecessary risk and can also create reputational harm if handled poorly. A private reporting path helps the company receive, triage, and remediate security issues before disclosure.

### Recommendation

- Use GitHub security advisories for repositories that may receive external security reports.
- Avoid relying on public issue tracking for vulnerability intake.
- Establish an internal process for triage, ownership, remediation, and disclosure decisions.
- Coordinate with engineering and management before publishing any advisory.

### Operational checklist

- [ ] Enable private vulnerability reporting where available
- [ ] Assign a responsible security contact or team
- [ ] Define triage SLAs for incoming reports
- [ ] Document disclosure timelines and approval steps
- [ ] Keep an audit trail of the remediation workflow

## 3) SECURITY.md: publish the reporting policy

### What GitHub does

GitHub supports a `SECURITY.md` file in a repository, usually in the root, `.github/`, or `docs/` directory. This file tells researchers and users how to report vulnerabilities, which versions are supported, and what information to include.

### Why it matters legally

A security policy reduces confusion and helps show due diligence. It also discourages public disclosure through the wrong channel and gives the company a standard response pattern.

### Recommendation

Every public-facing repository should have a `SECURITY.md` file if the code could reasonably be targeted or reported on.

The file should include:

- a reporting email or form
- supported versions
- what not to report publicly
- expected response time
- basic safe disclosure guidance

### Operational checklist

- [ ] Add `SECURITY.md` to the repo
- [ ] Keep contact details current
- [ ] Specify supported branches or releases
- [ ] State whether GitHub private reporting is accepted
- [ ] Review the policy at least quarterly

## 4) Dependabot security updates: automate dependency risk reduction

### What GitHub does

Dependabot security updates can automatically open pull requests when GitHub detects vulnerable dependencies. GitHub can also surface dependency alerts, including transitive dependency issues, so teams are notified when a package pulls in a vulnerable component indirectly.

### Why it matters legally

Dependency vulnerabilities are a supply-chain risk. If the company ships code with known vulnerable dependencies, that can create negligence, breach, or incident-response issues depending on the situation and jurisdiction.

### Recommendation

- Enable Dependabot security updates for active repositories.
- Treat Dependabot alerts as part of the official remediation workflow.
- Require review for security update pull requests.
- Use configuration files to control update cadence and package ecosystems.

### Operational checklist

- [ ] Enable Dependabot for supported ecosystems
- [ ] Review alert volume and assign owners
- [ ] Track fixes to closure, not just alert creation
- [ ] Test updates before merging into protected branches
- [ ] Keep dependency update policy documented in the repo

## 5) GitHub Terms of Service and the free tier

### What GitHub requires

GitHub's terms govern account creation, acceptable use, payments, and the use of platform features. For the free tier, the key compliance points include:

- accounts must be created by a human and meet the minimum age requirement
- one free account per person is the intended model
- paid services are billed in advance where applicable
- cancellations, refunds, and downgrade handling follow GitHub's terms
- free-tier features and usage limits should be understood before relying on them operationally

### Why it matters legally

This is both a legal and governance issue. If the company creates accounts in a way that violates platform rules, it can lose access or create contractual problems. Billing and account ownership should also be tracked internally so the company knows which individual or business function controls each account.

### Recommendation

- Use company-managed accounts and documented ownership.
- Do not create duplicate free accounts to bypass limits.
- Review paid feature usage before relying on them in a production workflow.
- Make sure team members understand acceptable use and account integrity rules.

### Operational checklist

- [ ] Track account ownership internally
- [ ] Confirm every account follows GitHub's age and identity rules
- [ ] Review free-tier limits before planning operational dependencies
- [ ] Keep billing responsibility clear for any paid add-ons or upgrades
- [ ] Retain the latest terms and policy references in the compliance archive

## 6) Data residency and privacy

### What GitHub does

GitHub documents regional data residency options for enterprise customers, including storage locations such as the EU, Australia, the US, and Japan. GitHub also documents privacy and data processing practices, including the handling of personal data, lawful bases for processing, and international transfers.

### Why it matters legally

Data residency affects contractual commitments, cross-border transfer analysis, and privacy disclosures. If JAGM IT Company handles client-sensitive or regulated information, the company must know where data may be stored and processed.

### Recommendation

- Treat data residency as a design decision, not a later compliance add-on.
- Identify whether any repositories contain personal data, customer data, or regulated information.
- Avoid storing unnecessary personal data in issues, pull requests, or comments.
- Review whether the GitHub plan and product mix support the company’s privacy commitments.

### Operational checklist

- [ ] Classify the types of data stored in GitHub
- [ ] Minimize personal data in repository content and metadata
- [ ] Review whether regional storage is required for any business unit
- [ ] Maintain a privacy notice and internal retention policy
- [ ] Confirm any external transfer obligations with counsel

## 7) Open source license compliance tools

### What GitHub does

GitHub supports enterprise-style open source license compliance controls using SPDX identifiers and policy enforcement. GitHub can be configured to evaluate or actively enforce license requirements through pull request checks and rulesets, and it can support exception workflows for approved cases.

### Why it matters legally

License compliance is not just about using a permissive license. It is about making sure third-party code is tracked, approved, and distributed under the right terms. Missing this step can create downstream disclosure or redistribution problems.

### Recommendation

- Define an internal approved-license policy using SPDX identifiers.
- Use policy checks to flag unapproved licenses before merge.
- Route exceptions through a documented approval process.
- Keep a record of third-party components and their license obligations.

### Operational checklist

- [ ] Create an approved license list
- [ ] Map licenses to SPDX identifiers
- [ ] Set ruleset or PR checks for license enforcement
- [ ] Define an exception approval process
- [ ] Review license exceptions regularly

## 8) Code of conduct templates and community standards

### What GitHub does

GitHub offers code of conduct templates that can be added to repositories. A code of conduct is typically stored in the root, `docs/`, or `.github/` directory, and GitHub can surface community standards in project metadata.

### Why it matters legally

A code of conduct is not only a community feature. It is also a governance tool that helps the company set behavioral expectations, respond consistently to misconduct, and reduce moderation ambiguity.

### Recommendation

- Add a code of conduct to public or community-facing repositories.
- Use a recognized template when appropriate, then adapt it to company needs.
- Pair the code of conduct with a reporting and enforcement path.
- Ensure moderators or maintainers know how to respond consistently.

### Operational checklist

- [ ] Select a code of conduct template
- [ ] Add reporting contacts or escalation routes
- [ ] Publish moderation expectations where contributors can find them
- [ ] Align enforcement with company policy
- [ ] Review the policy when community scope changes

## Practical compliance checklist for JAGM IT Company

### Repository-level controls

- [ ] Every public repo has a license file
- [ ] Every public repo has a `SECURITY.md` file when security reports are possible
- [ ] Dependabot is enabled where supported
- [ ] A code of conduct is present where community interaction is expected
- [ ] Third-party dependencies are reviewed for license and vulnerability risk

### Organization-level controls

- [ ] Account ownership is documented
- [ ] Terms of Service compliance is reviewed periodically
- [ ] Data residency requirements are understood before storing sensitive data
- [ ] Privacy obligations are mapped to GitHub usage patterns
- [ ] License approval and exception handling are centralized

### Process controls

- [ ] Security reports are triaged privately
- [ ] Vulnerability fixes are tracked to completion
- [ ] License exceptions require approval
- [ ] Contributors know where to report misconduct or security issues
- [ ] Compliance artifacts are reviewed on a schedule

## Risk summary

| Risk | Impact | Likelihood | Mitigation |
| --- | --- | --- | --- |
| Missing or unclear license | High | Medium | Add a root license file to every public repo |
| Public vulnerability disclosure without process | High | Medium | Use `SECURITY.md` and private reporting workflows |
| Vulnerable dependencies shipped accidentally | High | Medium | Enable Dependabot and review alerts promptly |
| Terms of Service or account misuse | Medium | Low to medium | Track account ownership and comply with free-tier rules |
| Unclear data residency or privacy posture | High | Medium | Minimize personal data and document storage expectations |
| Third-party code used under incompatible terms | High | Medium | Apply license policy checks and review exceptions |
| Community conflicts handled inconsistently | Medium | Medium | Publish a code of conduct and enforcement process |

## Conclusion

GitHub gives JAGM IT Company enough free and built-in controls to support a credible baseline legal/compliance posture, provided the company uses them consistently. The strongest pattern is simple:

1. publish the legal rules in the repository
2. automate the checks GitHub can enforce
3. document the exception process for everything else

If JAGM IT Company follows that pattern, GitHub becomes not just a development platform but a controlled compliance surface.

## References consulted

Official GitHub documentation reviewed for this guide:

- Licensing a repository: https://docs.github.com/articles/licensing-a-repository
- Adding a security policy to your repository: https://docs.github.com/code-security/getting-started/adding-a-security-policy-to-your-repository
- Dependabot security updates: https://docs.github.com/code-security/concepts/supply-chain-security/dependabot-security-updates
- GitHub Terms of Service: https://docs.github.com/site-policy/github-terms/github-terms-of-service
- GitHub Privacy Statement: https://docs.github.com/site-policy/privacy-policies/github-privacy-statement
- Open source license compliance: https://docs.github.com/code-security/concepts/supply-chain-security/open-source-license-compliance
- Configure license policies: https://docs.github.com/code-security/getting-started/configure-license-policies
- Adding a code of conduct to your project: https://docs.github.com/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project
- Data residency documentation: https://docs.github.com/enterprise-cloud@latest/admin/data-residency/
