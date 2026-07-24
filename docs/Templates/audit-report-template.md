# Client-Facing Audit Report Template

> Prepared for: [Client Name]  
> Repository: [Repository Name]  
> Audit date: [YYYY-MM-DD]  
> Prepared by: JAGM IT Company

## 1. Executive Summary

[Write one short paragraph in plain language. Include the overall health score, the most important finding, and why it matters to the client’s business. Keep this section easy to read in under 30 seconds.]

**Overall health score:** [0-100]/100  
**Bottom line:** [One-sentence summary of the audit outcome]

## 2. Security Score

**Security score:** [0-100]/100

| Area | Weight | Score | What this means |
|---|---:|---:|---|
| Secrets handling | [x] | [x] | [Short note about exposed secrets, secret scanning, and credential storage] |
| Access and branch controls | [x] | [x] | [Short note about branch protection, review rules, and merge safety] |
| Dependency hygiene | [x] | [x] | [Short note about dependency freshness and known vulnerabilities] |
| CI/CD safeguards | [x] | [x] | [Short note about automated checks and release gates] |
| Recovery and monitoring | [x] | [x] | [Short note about alerting, logging, and incident readiness] |

**Plain-English interpretation:** [Explain the score in simple terms and mention whether the risk level is low, medium, or high.]

## 3. Critical Findings

> These are the issues that must be fixed immediately because they create direct risk.

1. **[Critical finding title]**
   - **Why it matters:** [Explain the impact in business terms]
   - **Evidence:** [Reference the file, workflow, or control that triggered the finding]
   - **Recommended fix:** [Describe the immediate remediation]
   - **Priority:** Critical

2. **[Critical finding title, if needed]**
   - **Why it matters:** [Explain the impact in business terms]
   - **Evidence:** [Reference the file, workflow, or control that triggered the finding]
   - **Recommended fix:** [Describe the immediate remediation]
   - **Priority:** Critical

If no critical findings were identified, write: **No critical findings were identified in this audit run.**

## 4. Warnings

> These issues are not as urgent as critical findings, but they should be addressed soon.

1. **[Warning title]**
   - **Why it matters:** [Explain the risk in plain language]
   - **Recommended fix:** [What should happen next]
   - **Priority:** Warning

2. **[Warning title, if needed]**
   - **Why it matters:** [Explain the risk in plain language]
   - **Recommended fix:** [What should happen next]
   - **Priority:** Warning

If no warnings were identified, write: **No warning-level issues were identified in this audit run.**

## 5. Recommendations

> These are best-practice improvements that will raise quality, reduce risk, and make future work easier.

- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]
- [Recommendation 4, if needed]

## 6. Next Steps

> If the client wants help, these are the two service paths we offer.

### Audit+Fix Sprint — $1K-$3K
Best for teams that want the highest-priority audit findings fixed quickly.

**Includes:**
- Focused remediation of the most important issues
- Fast implementation of agreed quick wins
- Lightweight validation after fixes are applied
- A short follow-up summary of completed work

### AI Ops Retainer — $1K-$5K/mo
Best for teams that want ongoing improvement, automation, and support after the first fix cycle.

**Includes:**
- Monthly repository health review
- Continuous improvement recommendations
- Workflow, automation, and documentation support
- Priority handling for new issues and improvement requests

**Suggested client message:** [Add one clear sentence inviting the client to choose the next step.]
