# AI-Engineer Analysis: Free GitHub AI-Powered Features

Issue: #14  
Repository: `jagmstar/github-features-audit`  
Prepared by: AI-Engineer track for JAGM IT Company

## 1) Executive summary

GitHub has a small but useful set of AI-adjacent features that can be used at no direct cost, but the free value is uneven.

For JAGM IT Company, the most dependable zero-cost wins are:

- **Dependabot** for dependency alerts and security updates
- **GitHub Actions** for orchestration and lightweight AI workflows within free minutes
- **GitHub Models** for prototyping prompts and internal experiments within rate limits
- **GitHub Copilot Free** for individual contributor productivity
- **CodeQL** only when we can place the work in public repositories or accept a paid private-repo upgrade path
- **Copilot code review** only as an opportunistic helper, not as the foundation of a free operating model

The key decision is this: if we want maximum free value, we should separate our architecture into:

1. **Private core repo** for company work
2. **Public demo/sandbox repos** for security scanning and AI experimentation

That split lets us keep the private repository lean while still using public repositories to unlock free CodeQL and free public-repo Actions runs.

## 2) Scope and assumptions

### Scope
This analysis covers the GitHub features named in issue #14:

- GitHub Copilot Free
- CodeQL / code scanning
- GitHub Actions AI features
- Dependabot
- Copilot code review in pull requests
- GitHub Models
- GitHub API-based automation / code generation workflows

### Assumptions
- The main JAGM IT Company repository is **private**.
- The organization is on **GitHub Free** unless otherwise noted.
- Developers may use personal GitHub accounts with free Copilot access where available.
- We are optimizing for **no direct spend** or **minimum possible spend**, not for maximum throughput.

## 3) Feature-by-feature analysis

### 3.1 GitHub Copilot Free

**What it is**  
A free Copilot plan for individual developers. It is not a shared organizational seat model.

**What is free**
- Inline code suggestions with a limited monthly allowance
- Limited chat usage and limited agent-style assistance
- Access through supported IDE and GitHub experiences for eligible users

**Notable limits**
- Inline completions are capped at **2,000 completions per month**
- Model choice is **auto-selected** rather than fully user-controlled
- It is not a substitute for a paid team plan when multiple people need predictable usage

**Best use cases for JAGM IT Company**
- Drafting boilerplate code, YAML, Markdown, and small scripts
- Accelerating README and documentation edits
- Generating test scaffolding and repetitive refactors
- Helping a developer move faster without creating a new tool budget

**Verdict**  
Useful and genuinely free for individuals, but not a complete team-wide AI strategy. Treat it as a productivity multiplier for contributors, not as a company-owned platform capability.

---

### 3.2 GitHub Models

**What it is**  
GitHub’s model playground and API access layer for experimenting with AI models inside the GitHub ecosystem.

**What is free**
- Public preview access with free, rate-limited usage
- Prompt prototyping and experimentation without standing up a separate model platform
- A practical way to compare prompts, model behavior, and output quality

**Notable limits**
- Rate limits vary by plan and can be quite low for free usage
- Free access is best for experiments, not production workloads
- Usage is constrained by tokens and request caps, so large batch jobs are not a fit

**Best use cases for JAGM IT Company**
- Drafting issue summaries and release-note drafts
- Experimenting with support bot prompts
- Building proof-of-concept automations for triage or classification
- Testing prompt templates before we invest in a paid model provider

**Verdict**  
This is the best true “AI feature” for free experimentation. It is excellent for prototyping and internal R&D, but should not be relied on for production-scale automation without a paid plan or a different model provider.

---

### 3.3 CodeQL / code scanning

**What it is**  
GitHub’s static analysis and code scanning platform. It is security-oriented analysis rather than generative AI, but it is often grouped with AI-assisted code intelligence because it automates deep code inspection.

**What is free**
- Code scanning for **public repositories**
- CodeQL CLI for public-repo use
- Strong baseline security feedback with no direct license cost for open repositories

**Notable limits**
- Private repositories generally require a **GitHub Code Security** license or equivalent paid security entitlement
- The free path is best suited to public codebases or public demo repos

**Best use cases for JAGM IT Company**
- Public demo repos that we want to keep safe by default
- Open proof-of-concept work that should not carry security blind spots
- Security validation in PRs for public-facing examples

**Verdict**  
Excellent on public repositories, but not a free private-repo security baseline. If we want free CodeQL, we should publish sanitized demo repos publicly.

---

### 3.4 Dependabot

**What it is**  
GitHub’s dependency monitoring and automated update system.

**What is free**
- Security alerts
- Security update pull requests
- Dependency version update pull requests
- Available by default across repositories

**Notable limits**
- The cost is not financial, but there is still maintenance overhead from review and merge work
- Update noise can be high if dependency hygiene is poor

**Best use cases for JAGM IT Company**
- Keeping library risk visible without manual scanning
- Auto-opening update PRs for routine package maintenance
- Reducing security drift in long-lived repositories
- Supporting a lightweight compliance story for client-facing repos

**Verdict**  
This is one of the strongest free features in the entire GitHub ecosystem. It should be enabled everywhere.

---

### 3.5 Copilot code review in pull requests

**What it is**  
An AI-assisted review experience for PRs.

**What is free**
- Limited free access exists for some GitHub.com users on the Free plan
- The feature can help surface obvious problems and suggest changes

**Notable limits**
- Full access is tied to higher Copilot plans
- Free usage can be constrained by AI credit behavior and plan rules
- It should not be treated as deterministic, always-on review coverage

**Best use cases for JAGM IT Company**
- Extra review assist on routine PRs
- Fast feedback on documentation, formatting, and low-risk code changes
- Helping small teams catch easy mistakes before human review

**Verdict**  
Helpful when available, but not reliable enough to be the backbone of a free plan. Use it as a bonus layer, not a control point.

---

### 3.6 GitHub Actions as an AI orchestration layer

**What it is**  
GitHub Actions is not an AI model feature by itself. Its free value comes from orchestrating AI-related workflows and automating the steps around them.

**What is free**
- Public repositories: standard runner usage is free within GitHub’s policy
- Private repositories on GitHub Free: **2,000 minutes per month** are included
- Workflow automation itself is the platform, even when the AI call happens elsewhere

**What to use it for**
- Scheduled prompt jobs against GitHub Models
- Automated issue classification and label suggestions
- AI-assisted release-note generation
- Security scans, docs validation, and repo hygiene checks that feed AI workflows
- Triggering internal webhooks when AI-generated artifacts are ready for review

**Notable limits**
- Actions minutes can be consumed quickly by large jobs
- If a workflow calls an external AI API, that API has its own pricing and limits
- “AI features” in Actions are mostly about integration, not free intelligence built into the runner

**Verdict**  
Actions is the correct automation layer for the company, but it is not an AI engine. Use it to schedule, gate, and publish AI outputs rather than to host large model workloads.

---

### 3.7 GitHub API-based code generation and automation

**What it is**  
Using GitHub REST or GraphQL APIs to automate repository operations such as opening issues, creating PRs, labeling work, posting comments, or syncing metadata.

**What is free**
- Normal API usage is free within GitHub rate limits
- No separate AI license is required for the API itself

**Notable limits**
- The API does not generate code on its own
- AI generation still requires Copilot, GitHub Models, or an external model provider
- Rate limits and authentication rules still apply

**Best use cases for JAGM IT Company**
- Automated issue triage
- PR labeling and routing
- Generating structured repository metadata
- Posting machine-generated summaries for human review

**Verdict**  
The API is the control plane for AI workflows, not the model. It is valuable because it lets us operationalize AI results cleanly and cheaply.

## 4) Availability matrix

| Feature | Free availability | Key limits | Best fit for JAGM IT Company |
|---|---|---|---|
| GitHub Copilot Free | Yes, for eligible individual accounts | 2,000 inline completions/month; limited chat/agent usage; auto model selection | Day-to-day developer productivity |
| GitHub Models | Yes, rate-limited preview access | Low usage caps; not for production-scale workloads | Prompt prototyping and internal experiments |
| CodeQL | Yes on public repos | Private repos need paid security entitlement | Public demo repos and open POCs |
| Dependabot | Yes across repos | Review noise; merge overhead | Dependency risk reduction everywhere |
| Copilot code review | Limited free access on GitHub.com | Full access requires paid Copilot plans | Bonus PR review assist |
| GitHub Actions | Yes within plan minutes | 2,000 private minutes/month on GitHub Free; external AI calls may cost more | Workflow automation and AI orchestration |
| GitHub API automation | Yes within rate limits | Not an AI engine by itself | Triage, routing, and repo automation |

## 5) Recommended use cases for JAGM IT Company

### Immediate wins
1. **Enable Dependabot everywhere**
   - Lowest friction, highest reliability
   - Helps keep the private repo healthy without adding process overhead

2. **Use Copilot Free for individual contributors**
   - Good for markdown, YAML, scripts, and routine refactors
   - Useful for the docs-heavy nature of this project

3. **Use GitHub Models for prompt experiments**
   - Prototype issue summarizers, release-note generators, and triage helpers
   - Keep experiments in a sandbox repo or branch

4. **Use Actions to automate AI outputs**
   - Human review still happens in the PR
   - Automate the boring glue around the model calls

### Medium-term wins
5. **Create public demo repos where possible**
   - This unlocks free CodeQL and free public-repo Actions usage
   - Good for safe, sanitized examples and showcase repositories

6. **Use Copilot code review opportunistically**
   - Helpful, but not critical
   - Treat it as a convenience feature for low-risk changes

### Upgrade-path items
7. **Private-repo CodeQL**
   - Upgrade only when private-repo security coverage is worth the license cost

8. **Higher Copilot plans**
   - Worth it if the team wants shared, predictable review and broader AI usage

## 6) Integration plan

### Phase 1: Zero-cost baseline
- Turn on Dependabot alerts and security updates for every repo
- Keep AI experiments in a dedicated sandbox or demo repository
- Document prompt-review rules so generated content always gets human approval
- Create simple Actions workflows for docs validation and AI experiment gating

### Phase 2: Controlled AI adoption
- Ask individual developers to use Copilot Free where available
- Build a GitHub Models prototype for:
  - issue summarization
  - release-note drafting
  - triage suggestions
- Use Actions to run scheduled or event-driven model jobs
- Save all outputs as draft artifacts, not production truth

### Phase 3: Security and scale
- Publish sanitized public demo repos to take advantage of free CodeQL
- Measure how many Actions minutes the AI workflows actually consume
- Decide whether private-repo CodeQL or a paid Copilot plan is justified by business value
- Introduce a review policy for model-generated content

## 7) Guardrails

If we adopt AI tools broadly, we should enforce the following rules:

- Never send secrets, tokens, or customer data to a model prompt
- Treat every model output as untrusted until reviewed by a human
- Log prompt templates and workflow versions
- Use repo templates so generated output stays consistent
- Avoid depending on free model rate limits for production-critical flows

## 8) Conclusion

The most useful free GitHub AI stack for JAGM IT Company is not a single feature. It is a combination of:

- **Dependabot** for always-on dependency safety
- **GitHub Models** for experimentation
- **GitHub Copilot Free** for individual productivity
- **GitHub Actions** for orchestration
- **Public demo repositories** for free CodeQL coverage

That combination gives us a practical zero-cost path to explore AI-enabled engineering without turning the company into a paid AI platform customer too early.

## 9) References

Official GitHub documentation reviewed for this analysis includes:

- GitHub Copilot plans and features: `https://docs.github.com/en/copilot/get-started/plans`
- GitHub Models billing and free preview access: `https://docs.github.com/billing/managing-billing-for-your-products/about-billing-for-github-models`
- GitHub Models overview: `https://docs.github.com/github-models/prototyping-with-ai-models`
- Copilot code review: `https://docs.github.com/en/copilot/concepts/agents/code-review`
- Code scanning / CodeQL: `https://docs.github.com/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning`
- GitHub security features and Dependabot overview: `https://docs.github.com/code-security/getting-started/github-security-features`
