# CFO Cost Savings Analysis: What We Pay For vs What GitHub Gives Free

## Executive summary
GitHub can replace a meaningful share of our current tool stack at very low platform cost. For JAGM IT Company, the financial case is strongest in three areas:

1. **CI/CD** — GitHub Actions can replace a standalone CI vendor for many workloads.
2. **Hosting and documentation** — GitHub Pages can replace lightweight static hosting for public demos and docs.
3. **Project management** — GitHub Issues, Projects, and Milestones can replace a basic task-tracking subscription for internal delivery.

For an organization-sized account, the best default tier is **GitHub Team** at **$4/user/month**. It preserves the business features we actually need while still keeping the platform spend far below a separate CI + hosting + PM stack.

## Scope and assumptions
Because the issue did not provide headcount or current vendor contracts, I used a conservative planning model:

- **Team size modeled:** 5 users
- **Blended labor rate for productivity value:** $75/hour
- **Current tools modeled:**
  - CircleCI Performance for CI/CD
  - Netlify Pro for static hosting / deploy previews
  - A Jira/Asana/Linear-equivalent PM tool for work tracking
- **GitHub tier comparison:** Free vs Team vs Enterprise for company use

This is a decision memo, not an invoice audit. Numbers below are estimates meant to show order of magnitude and ROI direction.

## What GitHub gives us for free or near-free
### GitHub Free
Official GitHub Free includes, among other features:
- Unlimited public/private repositories
- **2,000 CI/CD minutes/month** with GitHub Actions for private usage
- Free Actions usage for public repositories
- **500 MB Packages storage**
- Issues and Projects
- Dependabot security and version updates
- Community support

### GitHub Team
Official GitHub Team adds the features most relevant to a business account:
- **$4/user/month**
- **3,000 CI/CD minutes/month**
- Repository rules
- Multiple reviewers
- Draft pull requests
- Code owners
- Required reviewers
- Pages and Wikis
- Environment deployment branches and secrets
- 2 GB Packages storage

### GitHub Enterprise
Official GitHub Enterprise starts at **$21/user/month** and adds enterprise controls such as:
- Data residency
- Enterprise Managed Users
- SSO / SCIM
- Advanced auditing
- Higher CI/CD and storage limits

## Current cost breakdown: what we are likely paying today
| Tool / capability | Assumed monthly cost | What GitHub can replace | Notes |
|---|---:|---|---|
| CI/CD (CircleCI Performance) | $15 | GitHub Actions | GitHub Team includes 3,000 minutes/month; Free includes 2,000 minutes/month |
| Static hosting / deploy previews (Netlify Pro) | $20 | GitHub Pages | Best for docs, demos, and lightweight marketing sites |
| Project management (Jira/PM equivalent) | $50 | GitHub Issues + Projects + Milestones | Good for basic delivery flow and visibility |
| **Total current baseline** | **$85/month** |  |  |

## Savings from moving to GitHub-native workflows
### Direct hard-dollar savings
If we move CI/CD, hosting, and basic PM into GitHub and use **GitHub Team** for the organization:

- Current baseline: **$85/month**
- GitHub Team cost for 5 users: **$20/month**
- **Net hard-dollar savings: $65/month**
- **Annual hard-dollar savings: $780/year**

If we can run a **public-first** model and stay entirely on **GitHub Free**, then the monthly platform cost could drop to **$0**, which would increase the hard-dollar savings to the full **$85/month** baseline.

### Capability mapping
| Need | Current tool class | GitHub replacement | Cost effect |
|---|---|---|---|
| Build/test/deploy automation | CI vendor | GitHub Actions | Eliminates a separate CI subscription for many repos |
| Public demo / docs hosting | Static hosting platform | GitHub Pages | Eliminates a lightweight hosting bill |
| Backlog / sprint / issue tracking | PM SaaS | GitHub Issues + Projects + Milestones | Eliminates a separate PM seat cost for core delivery work |
| Dependency hygiene | Separate security tooling | Dependabot | Reduces need for extra dependency-update tooling |

## ROI projection
I split ROI into two parts: **hard-dollar savings** and **capacity value**.

### 1) Hard-dollar savings
- Current baseline: $85/month
- GitHub Team: $20/month
- **Savings: $65/month**
- **Savings per year: $780**

### 2) Capacity value from automation and fewer tool hops
Estimated monthly time saved:
- CI/CD maintenance and re-runs: **2 hours**
- Hosting / deploy-preview admin: **1 hour**
- PM tool switching, status chasing, and manual updates: **3 hours**
- **Total: 6 hours/month**

At a blended labor rate of **$75/hour**:
- **6 x $75 = $450/month** of capacity value
- **$5,400/year** of capacity value

### 3) Combined economic impact
- Hard-dollar savings: **$65/month**
- Capacity value: **$450/month**
- **Total monthly economic impact: $515/month**
- **Total annual economic impact: $6,180/year**

### 4) ROI against GitHub Team spend
- GitHub Team annual cost for 5 users: **$240/year**
- Net benefit after platform cost: **$5,940/year**
- **ROI: 2,475%**
- Payback period: **well under 1 month**

## Recommended tier
### Recommendation: GitHub Team
GitHub Team is the best fit for JAGM IT Company because it gives us:
- Organization-friendly collaboration
- Repository rules and review controls
- Pages and Wikis
- A higher Actions allowance than Free
- A cost structure that is still extremely small relative to the value it replaces

### Why not GitHub Pro?
GitHub Pro is primarily a personal-account plan. It is not the right default tier for a company that needs organization-level collaboration and branch governance.

### Why not GitHub Enterprise?
GitHub Enterprise is only justified if we need compliance, SSO/SCIM, advanced auditing, data residency, or other enterprise controls. It is **not** the cost-saving choice.

### Why not stay on GitHub Free only?
GitHub Free can work for a public-first proof engine, but Team is the safer business default if we want:
- Company-owned organization workflows
- Stronger branch and review rules
- More predictable collaboration across the team
- More CI/CD headroom

## Budget impact summary
| Scenario | Annual platform spend | Annual value recovered | Net annual impact |
|---|---:|---:|---:|
| Current standalone stack | $1,020 | $0 | $1,020 spent |
| GitHub Free public-first | $0 | $1,020 | $1,020 avoided |
| GitHub Team default | $240 | $6,180 | $5,940 net benefit |
| GitHub Enterprise | $1,260 | depends on compliance need | Usually not cost-justified for this use case |

## Bottom line
Adopting GitHub-native features can eliminate a separate CI/CD subscription, a lightweight hosting bill, and a basic PM subscription. On a conservative 5-user model, the company can reduce direct platform spend from about **$85/month** to **$20/month** with GitHub Team, while also recovering roughly **6 hours of team capacity per month**.

**Decision:** choose **GitHub Team** for the organization, and use GitHub Free patterns where public repos make sense for demos and proof-of-work.

## Sources
- GitHub pricing: https://github.com/pricing
- CircleCI pricing: https://circleci.com/pricing
- Netlify pricing: https://www.netlify.com/pricing/
- Atlassian Jira pricing reference: https://www.atlassian.com/software/jira/pricing
