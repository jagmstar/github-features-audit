# TechWriter Documentation Strategy: GitHub Wiki, Discussions, Pages, and Repository Docs

Issue: #13  
Repository: `jagmstar/github-features-audit`  
Prepared for: JAGM IT Company

## Executive summary

GitHub should be treated as a documentation system, not only a code host. For JAGM IT Company, the best documentation strategy is a layered model:

- **README.md** as the first entry point and project summary
- **CONTRIBUTING.md** as the contributor workflow guide
- **CODE_OF_CONDUCT.md** as the collaboration policy baseline
- **Issue and pull request templates** as quality controls for inbound work
- **GitHub Discussions** as the community and Q&A layer
- **GitHub Wiki** as lightweight operational knowledge storage when needed
- **GitHub Pages** as the public-facing documentation and knowledge portal
- **GitHub Actions** as the automation layer that keeps docs current, validated, and published
- **MkDocs or Jekyll** as the site generator layer for richer documentation sites published through Pages

The strategic goal is to make documentation easy to find, easy to maintain, and hard to let drift. GitHub already provides the surfaces we need; the main job is to assign each surface a clear purpose and avoid duplication.

## Core documentation principles

1. **One clear home for each kind of information**  
   Do not place the same policy in five different locations. Each document should have a primary owner and a primary purpose.

2. **Public-proof, private-core**  
   Public repositories should show enough process, structure, and quality to build trust. Private project details can stay private, but the public-facing docs should still look complete.

3. **Documentation should be near the work**  
   If people need to follow a process while contributing, the process should live in the repository, not in a separate forgotten site.

4. **Keep the front door short**  
   The README should answer: what is this, why does it matter, how do I use it, and where do I go next.

5. **Use GitHub features for governance**  
   Templates, discussions, workflows, and pages should enforce good habits rather than relying on memory.

6. **Automate validation and publishing**  
   Docs that can break should be tested, linked, and published automatically.

## Recommended documentation architecture

### Layer 1: Repository front door
This layer should always exist in every active repository.

#### README.md
Use the README as the top-level summary and navigation hub.
It should include:
- project purpose
- who it is for
- quick start or usage steps
- link to full documentation
- link to issues/discussions
- maintenance or ownership note

**README standards**
- keep the first screen scannable
- use one H1 only
- keep paragraphs short
- use bullets and tables for scanability
- include screenshots or diagrams only when they add meaning
- write in plain language

#### CONTRIBUTING.md
Use CONTRIBUTING.md to define how to work with the repository.
It should include:
- setup steps
- branch and pull request process
- code or docs style rules
- testing/validation expectations
- where to ask questions
- release or review expectations if relevant

Best practice: place CONTRIBUTING.md at the repository root so GitHub can surface it automatically.

#### CODE_OF_CONDUCT.md
Use a standard code of conduct to define collaboration norms.
It should include:
- expected behavior
- unacceptable behavior
- reporting process
- enforcement responsibility
- contact point for escalation

Best practice: keep the file short, adopt a recognized template, and point people to the reporting path immediately.

#### Issue and pull request templates
Templates should reduce ambiguity and improve submission quality.
Use them for:
- bug reports
- feature requests
- documentation gaps
- change requests
- pull request summaries

Recommended location:
- `.github/ISSUE_TEMPLATE/`
- `.github/pull_request_template.md`

Prefer **YAML issue forms** when you want structured input, and **Markdown templates** when a lightweight narrative format is enough.

### Layer 2: Operational knowledge
This layer is for contributor guidance and community conversation.

#### GitHub Discussions
Use Discussions for questions, ideas, announcements, and community collaboration.
It is a better fit than issues when the conversation is open-ended or not tied to a specific work item.

Recommended discussion categories for JAGM IT:

| Category | Format | Purpose |
|---|---|---|
| Announcements | Announcement | Official updates, release notes, and policy notices |
| General | Open-ended | Broad community discussion and repository questions |
| Ideas | Open-ended | Suggestions for improvements and future work |
| Q&A | Question and Answer | Support questions and solution sharing |
| Show and tell | Open-ended | Demos, examples, and proof-of-work |
| Polls | Polls | Lightweight preference gathering |

**Category governance rules**
- keep categories purposeful, not decorative
- use clear naming and consistent emoji only if they help recognition
- avoid creating too many categories just because GitHub allows it
- review category usefulness periodically and archive low-value categories
- remember that GitHub allows up to **25 categories** per repository or organization discussion space

**When to use Discussions instead of Issues**
- use Discussions for questions without a fixed task
- use Issues for work items that need completion tracking
- use Discussions for community input before defining a task
- use Issues once the work becomes actionable

#### GitHub Wiki
Use the Wiki for lightweight internal or semi-structured knowledge that does not belong in the main repository history.
It is best for:
- meeting notes
- reference pages
- operational runbooks
- migration notes
- temporary knowledge that may not need a full code review cycle

**Wiki guidance**
- do not use the Wiki as the primary source of truth for policy docs that must travel with the code
- keep core policies in the repository, not only in the Wiki
- use the Wiki when the information is useful but not part of the release artifact
- if the repository needs more than a small knowledge base, consider GitHub Pages or a docs site instead

**Known constraint**
- GitHub Wikis have a soft limit of **5,000 files**

### Layer 3: Public documentation portal
This layer is for polished, navigable documentation and external-facing knowledge.

#### GitHub Pages
Use GitHub Pages for any documentation that needs a public URL, a structured site, or a client-facing presentation layer.
Good use cases include:
- project documentation sites
- service landing pages
- knowledge portals
- demo hubs
- onboarding guides
- release and change logs

**Pages strategy**
- use Pages for polished, navigable documentation
- use the repository for source files and governance documents
- publish generated docs to Pages from a docs branch or workflow artifact
- keep the site simple enough to maintain consistently

**Site types**
- **user/organization site**: `<owner>.github.io`
- **project site**: `<owner>.github.io/<repository>`

#### Generator choice: MkDocs vs Jekyll
Both can work well on GitHub Pages; the best choice depends on the docs shape.

**Use Jekyll when:**
- the site is simple
- the team wants minimal setup
- you want native GitHub Pages compatibility with less tooling overhead
- the docs are mostly static pages and simple navigation

**Use MkDocs when:**
- the docs are content-heavy
- you want better navigation for technical documentation
- the site should feel like a documentation portal rather than a blog
- you want a clean docs-first structure with strong markdown support

**Practical recommendation**
- Start with **MkDocs** for a documentation-centric portal if the repo grows beyond a few pages.
- Use **Jekyll** for small, simple Pages sites where the maintenance overhead must stay very low.

## Documentation governance model

### Ownership
Every documentation surface should have a named owner.

Suggested ownership model:
- **README.md** — repository maintainer
- **CONTRIBUTING.md** — technical lead or maintainer
- **CODE_OF_CONDUCT.md** — company operations or leadership contact
- **Templates** — repository maintainer plus quality owner
- **Discussions** — community manager or designated maintainer
- **Wiki** — documentation owner or project lead
- **Pages site** — documentation owner plus technical maintainer

### Update rules
- update documentation in the same pull request as the feature or process change whenever possible
- review docs during release and milestone closeout
- treat broken documentation as a quality issue, not a cosmetic one
- archive outdated pages instead of leaving them misleadingly live

### Review rules
- docs changes should be reviewed like code changes
- templates and contributing guidance should be checked for clarity and correctness
- public-facing docs should be reviewed for tone, accuracy, and brand consistency

## Suggested content standards by document type

### README.md standards
A good README should answer four questions in the first part of the file:
1. What is this?
2. Why does it matter?
3. How do I start?
4. Where do I ask for help?

Recommended sections:
- Project title
- One-sentence summary
- Why this matters
- Key features or scope
- Quick start
- Usage or examples
- Documentation links
- Support or contact
- License or policy note if needed

### CONTRIBUTING.md standards
A good contributing guide should answer:
1. How do I set up the project?
2. How do I make changes?
3. How do I submit them?
4. How are they reviewed?
5. How do I get help?

Recommended sections:
- repository setup
- branch naming
- commit message expectations
- pull request expectations
- issue linkage expectations
- testing and docs checks
- review and merge process

### CODE_OF_CONDUCT.md standards
A good code of conduct should be:
- short
- respectful
- readable
- easy to enforce

Recommended sections:
- standards of behavior
- unacceptable behavior
- reporting process
- enforcement responsibilities
- scope and applicability

### Template standards
Templates should help contributors submit useful information the first time.

For issue forms, prefer fields such as:
- problem description
- expected behavior
- actual behavior
- reproduction steps
- screenshots or links
- environment or repository context
- priority or impact

For pull requests, prefer fields such as:
- summary of change
- linked issue
- testing performed
- docs updated
- screenshots or evidence when relevant

## GitHub Actions for docs automation

GitHub Actions should be the enforcement and publishing engine for documentation quality.

### Recommended workflows
1. **docs-lint.yml**  
   Validate markdown formatting, headings, links, and file naming.

2. **docs-preview.yml**  
   Build and preview the site on pull requests.

3. **docs-publish.yml**  
   Publish the built docs to GitHub Pages after merge or release.

4. **template-check.yml**  
   Verify required issue and pull request template files exist and are current.

5. **link-check.yml**  
   Catch broken internal and external links.

### Automation checks to include
- markdown linting
- broken link validation
- heading hierarchy checks
- front matter validation if the generator uses it
- Pages build validation
- docs ownership or stale-doc detection where practical

### Recommended policy
- documentation changes should not be merged if the docs build fails
- published docs should be regenerated automatically from source
- workflow files should live with the repository so they are versioned and reviewable

## Recommended GitHub Discussions structure

### Category usage model
Use the following rules to keep Discussions useful:

- **Announcements** for official news only
- **Q&A** for support and troubleshooting
- **Ideas** for early-stage suggestions
- **General** for broad conversation
- **Show and tell** for examples, demos, and proof-of-work
- **Polls** for quick preference checks

### Moderation model
- assign at least one maintainer to oversee discussion hygiene
- convert actionable discussion items into issues
- close duplicate or off-topic threads politely
- keep announcement categories tightly controlled to avoid noise

### Escalation path
- if a discussion becomes a task, move it to an issue
- if a discussion becomes a support problem, document the answer in README, FAQ, or Pages
- if a discussion reveals a policy gap, update the relevant governance document

## Recommended GitHub Wiki usage

Use the Wiki only when it provides value that the repository docs do not.
Good examples:
- quick internal reference pages
- temporary operational notes
- brainstorming or rough notes that may later be promoted into the repository

Do not use the Wiki for:
- authoritative contributor rules
- release-critical policies
- documents that must be versioned with code and reviewed in pull requests

## Recommended Pages information architecture

A GitHub Pages documentation site for JAGM IT should follow this order:

1. **Home**
2. **Getting started**
3. **Documentation or product overview**
4. **Guides / tutorials**
5. **Reference material**
6. **FAQ or support**
7. **Changelog or updates**

If the site is public-facing, keep the navigation shallow and the value proposition obvious.
If the site is internal-facing, prioritize searchability and clear section labels.

## Implementation roadmap

### Phase 1: Establish the documentation baseline
- standardize README structure
- add CONTRIBUTING.md
- add CODE_OF_CONDUCT.md
- add issue and PR templates
- define the main documentation owner

### Phase 2: Add community and knowledge surfaces
- enable and organize Discussions
- define the discussion category model
- document when to use Discussions vs Issues vs Wiki
- create or clean up Wiki pages if the repo needs a lightweight knowledge base

### Phase 3: Publish a documentation site
- choose MkDocs or Jekyll
- create the Pages source structure
- add navigation and landing page content
- wire deployment through GitHub Actions

### Phase 4: Automate quality control
- add docs linting
- add link checking
- publish previews for pull requests
- require docs validation before merge

### Phase 5: Sustain and improve
- review doc analytics or usage signals where available
- remove stale pages
- update templates and guidance based on actual contributor questions
- keep the doc system aligned with project growth

## Success criteria

The documentation strategy is working if:

- new contributors can understand the repository within minutes
- people know where to ask questions and where to file work
- docs changes are reviewed and published consistently
- discussion threads are not being used as a substitute for structured issue tracking
- the Pages site stays current with repository changes
- templates reduce back-and-forth and improve issue quality
- the Wiki remains a secondary knowledge store, not a neglected source of truth

## Recommendation

For JAGM IT Company, the recommended documentation model is:

- **README** for the front door
- **CONTRIBUTING + CODE_OF_CONDUCT + templates** for governance
- **Discussions** for community Q&A and idea gathering
- **Wiki** for lightweight auxiliary knowledge
- **Pages** for the polished documentation site
- **Actions** for validation and publishing automation

This gives the company a GitHub-native documentation stack that scales from small repositories to public-facing knowledge portals without creating unnecessary process overhead.
