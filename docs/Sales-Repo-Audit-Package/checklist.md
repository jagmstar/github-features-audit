# Internal Checklist — AI-SDLC Repo Audit

## 1. Intake and access
- [ ] Confirm repository URL
- [ ] Confirm client contact details
- [ ] Confirm read access has been granted
- [ ] Note any special concerns from the client

## 2. Clone and setup
- [ ] Clone the repository locally
- [ ] Confirm the correct branch is available
- [ ] Review repository structure
- [ ] Identify primary app, service, and test directories

## 3. Baseline review
- [ ] Read the README and main docs
- [ ] Identify build/test commands
- [ ] Identify framework, package manager, and CI tools
- [ ] Check for obvious repository hygiene issues

## 4. Code quality review
- [ ] Scan for large files and overly complex modules
- [ ] Look for duplication and inconsistent patterns
- [ ] Review naming, structure, and maintainability
- [ ] Note refactor opportunities

## 5. Security review
- [ ] Check for exposed secrets or suspicious files
- [ ] Review dependency vulnerabilities
- [ ] Review lockfiles and dependency pinning
- [ ] Check branch protection and security settings

## 6. CI/CD review
- [ ] Inspect GitHub Actions or other pipeline configs
- [ ] Confirm lint/test/build jobs exist
- [ ] Check release flow and deployment automation
- [ ] Note any missing quality gates

## 7. Test coverage review
- [ ] Identify test frameworks in use
- [ ] Review unit, integration, and E2E coverage
- [ ] Confirm coverage thresholds if present
- [ ] Note the most important missing tests

## 8. Documentation review
- [ ] Review setup instructions
- [ ] Review architecture and contribution docs
- [ ] Check for deployment and troubleshooting guidance
- [ ] Note missing onboarding material

## 9. GitHub feature usage review
- [ ] Check issues, PR flow, and branch strategy
- [ ] Review use of templates, CODEOWNERS, and labels
- [ ] Check Dependabot or update automation
- [ ] Review security alerts and repo governance features

## 10. Synthesis and scoring
- [ ] Write executive summary
- [ ] Assign code quality score
- [ ] Summarize security findings
- [ ] Assess CI/CD maturity
- [ ] Summarize test coverage and documentation
- [ ] Prioritize recommendations
- [ ] Draft action plan

## 11. Quality check
- [ ] Ensure findings are clear and evidence-based
- [ ] Keep language client-ready and non-technical where needed
- [ ] Confirm priorities are ordered by risk and impact
- [ ] Remove any unclear or duplicated notes

## 12. Delivery
- [ ] Save report in the agreed handoff format
- [ ] Send report to Roman
- [ ] Confirm Roman received the package
- [ ] Be available for follow-up questions
