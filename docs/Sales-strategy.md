# Sales Strategy: Using GitHub Free Features for Client Delivery

## Executive summary
GitHub’s free and public-facing features give JAGM IT a practical sales engine:

- **Public repositories** turn past work into a visible portfolio.
- **GitHub Pages** turns a repository into a live demo or landing page.
- **GitHub Releases** turn delivery into a versioned client artifact.
- **GitHub Discussions** create a lightweight support channel.
- **Issue templates** standardize intake and onboarding.
- **GitHub Projects** provide visibility into status, scope, and priorities.
- **Organization profiles** act as a polished storefront for credibility.

This workflow lets us sell confidence, not just code: prospects can see proof, clients can track progress, and delivery stays organized without needing a separate paid tooling stack for every engagement.

## What GitHub free features do for the sales process

### 1) Public repos as portfolio pieces
Public repositories are our proof-of-work. They let prospects inspect code quality, README quality, commit discipline, release hygiene, and documentation depth.

**Sales value:**
- Reduces trust friction in first conversations.
- Shows technical maturity before the first call.
- Lets us highlight repeatable patterns: setup, testing, deployment, and release practices.

**Portfolio curation rules:**
- Keep 3–5 flagship repos pinned on the organization profile.
- Each repo should include: clear README, screenshots, live demo link, release notes, and a short case study.
- Prefer small, polished repositories over large unfinished ones.
- Use public repos for sanitized examples, accelerators, templates, and demo implementations.

### 2) GitHub Releases for client artifacts
Releases package software with release notes and binary files. That makes them ideal for handing over client builds, installers, exports, PDFs, or demo assets.

**Sales value:**
- Makes delivery feel professional and versioned.
- Gives clients a stable place to download exactly what was agreed.
- Supports handoff conversations with changelogs and known-issues notes.

**Recommended release format:**
- Tag: `v1.0.0-clientname`
- Title: `Client delivery v1.0.0`
- Release notes sections:
  - What’s included
  - Setup / install steps
  - Known limitations
  - Next steps
- Attach assets:
  - build zip
  - installer
  - PDF brief
  - data export if applicable

### 3) GitHub Pages for demos
GitHub Pages hosts a website directly from a repository. We should use it for lightweight demos, service landing pages, and client showcase pages.

**Sales value:**
- Gives prospects a live URL instead of a static slide deck.
- Makes services easier to explain with screenshots, short copy, and CTAs.
- Lets us show a solution before we ask for the sale.

**Demo page pattern:**
- Hero section: problem + outcome
- 3 benefits
- 1 architecture diagram
- 1 short walkthrough video or GIF
- CTA: book a discovery call / request a proposal

### 4) GitHub Discussions for client support
Discussions work as a community-style support forum. They are best for Q&A, announcements, and open-ended project communication.

**Sales value:**
- Reduces support noise in email threads.
- Creates searchable answers for recurring questions.
- Makes the relationship feel active and transparent.

**Best use:**
- Public projects: general support and FAQ.
- Client-specific repos: product questions, release announcements, and roadmap updates.
- Convert recurring support questions into docs or FAQs.

### 5) Issue templates for onboarding
Issue templates standardize intake. For onboarding, they should capture business context before work starts.

**Sales value:**
- Improves lead-to-project conversion by making the first action easy.
- Reduces back-and-forth during discovery.
- Sets expectations early about scope, environment, and decision makers.

**Template types we should use:**
- New client onboarding
- Bug report / defect report
- Feature request
- Support request
- Access / environment request

**Why this matters:**
Research on GitHub issue templates shows they are widely adopted and can reduce resolution time, reopenings, and comment volume, especially when the template is structured.

### 6) GitHub Projects for visibility
Projects provide boards, tables, roadmaps, custom fields, charts, templates, and status updates.

**Sales value:**
- Gives clients real-time visibility into work.
- Helps us show scope, status, blockers, and deadlines.
- Supports a professional delivery rhythm without separate PM software.

**Recommended project views:**
- Board for execution
- Table for detail tracking
- Roadmap for milestones and client deadlines

**Suggested custom fields:**
- Priority
- Client impact
- Target date
- Owner
- Risk level
- Approval status

### 7) Organization profile as a sales tool
An organization profile can show a README and pinned repositories for public users. This is our storefront on GitHub.

**Sales value:**
- Makes the brand look active and organized.
- Lets prospects quickly understand what we do.
- Turns the profile page into a curated lead-conversion surface.

**Profile checklist:**
- Strong one-line value proposition
- 3–6 pinned repos
- Link to website and contact method
- Short “How we work” section
- Links to case studies and demos

## Client delivery workflow

### Stage 1: Discovery
- Create a project in GitHub Projects.
- Open an onboarding issue using a template.
- Capture goals, constraints, stakeholders, timeline, and acceptance criteria.

### Stage 2: Proposal and proof
- Share the organization profile and 1–2 matching portfolio repos.
- Point the client to a live GitHub Pages demo.
- If needed, create a short release or tagged prototype.

### Stage 3: Delivery
- Track work in a project board.
- Use issues for milestones, bugs, and approvals.
- Ship deliverables through Releases.
- Post progress updates in Discussions or project status notes.

### Stage 4: Handoff and support
- Publish a final Release with assets and release notes.
- Convert common support questions into Discussions or FAQ docs.
- Keep the project open for follow-up issues and enhancements.

## Portfolio curation plan

We should treat the portfolio like a sales asset, not just a code archive.

### What to publish
- Client-safe demos
- Reusable accelerators
- Internal tooling examples that have been sanitized
- Before/after transformation stories
- Small utilities that solve a clear business problem

### What every flagship repo needs
- README with business problem and outcome
- Screenshot or GIF
- Setup instructions
- Architecture overview
- Release section
- Link to live demo or demo video
- Contact / next-step CTA

### What to avoid
- Raw experimental code with no context
- Unexplained monorepos
- Repos with no README or no visible outcome
- Sensitive client data or secrets

## Demo template

Use the same structure for every Pages demo site so prospects learn it once and trust it quickly.

### Suggested sections
1. **Headline**: What problem we solve.
2. **Business outcome**: Cost saved, time reduced, risk reduced.
3. **Screenshots**: 2–4 visuals.
4. **Process**: How the solution works.
5. **Proof**: Link to release, repo, or case study.
6. **Call to action**: Contact us or request a walkthrough.

### Demo repo structure
```text
/demo-project
  /docs
  /assets
  /screenshots
  README.md
  release-notes.md
  index.md
```

## Onboarding guide

### Intake questions
- What is the business goal?
- Who is the decision maker?
- What does success look like?
- What systems must integrate?
- What is the deadline?
- What access or assets are needed?

### Onboarding workflow
1. Client submits the onboarding issue.
2. We triage the request in Projects.
3. We confirm scope and risks.
4. We assign owners and dates.
5. We publish the first delivery milestone.

### Onboarding output
- Confirmed scope
- Project board link
- Initial delivery timeline
- Communication channel
- First milestone release plan

## Case study structure using GitHub features

Every case study should be built from the same evidence trail:

- **Repository**: source code and README
- **GitHub Pages**: live demo and storytelling page
- **Release**: versioned deliverable or client artifact
- **Projects**: timeline and delivery visibility
- **Discussions**: support and client Q&A
- **Organization profile**: discovery surface for prospects

### Case study template
- Client challenge
- Our approach
- GitHub tools used
- Delivery timeline
- Measurable result
- Link to demo / release / repo

## Sales positioning

Our message to prospects should be:

> We don’t just build software. We deliver it in a way that is visible, versioned, documented, and easy to support.

That positioning matters because it frames GitHub as part of the value proposition:
- lower delivery friction
- faster onboarding
- clearer status reporting
- easier client trust-building
- better long-term support

## Evidence and references
- GitHub Free plan includes unlimited public/private repositories and Issues & Projects: https://github.com/pricing
- GitHub Pages can host a website for an organization or project directly from a repository: https://docs.github.com/en/pages/getting-started-with-github-pages
- GitHub Discussions is a collaborative communication forum for questions, announcements, and project conversations: https://docs.github.com/en/discussions
- GitHub Projects supports tables, boards, roadmaps, custom fields, automation, charts, and status updates: https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects
- Organization profiles can show READMEs and pinned repositories for public users: https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile
- Releases package software with release notes and binary files: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
- Issue templates are widely used and associated with better issue quality and lower resolution overhead: https://doi.org/10.1145/3643673
