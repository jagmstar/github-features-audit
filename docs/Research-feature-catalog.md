# Research Feature Catalog: Free GitHub Features

Issue: #10  
Repository: `jagmstar/github-features-audit`  
Prepared for: JAGM IT Company  
Date: 2026-07-23

## Scope and method

This catalog covers GitHub-native features that are free on GitHub.com, either because they are included in GitHub Free or because GitHub exposes them as free-by-default surfaces on public repositories. It focuses on features with real operational value: collaboration, planning, publishing, automation, security, developer tooling, and APIs.

Usage status is repo-level:

- **USED** = there is visible evidence of the feature in this repository or its workflow history.
- **NOT USED** = there is no visible evidence of the feature in this repository yet.

Public-repo-only features are called out explicitly because GitHub Free often keeps the feature itself free but limits it to public repositories.

## Quick free-tier allowances

| Area | Free allowance | Notes |
|---|---|---|
| GitHub Actions | 2,000 minutes/month; 500 MB artifact storage; 10 GB cache storage per repository; 20 concurrent standard runner jobs; 5 concurrent macOS jobs | Standard GitHub-hosted runners are free for public repositories and Dependabot |
| GitHub Packages | 500 MB storage | Shared with Actions artifact storage |
| GitHub Codespaces | 120 core hours/month and 15 GB storage for GitHub Free personal accounts | Organization plans do not get this personal free quota |
| GitHub API | 60 unauthenticated requests/hour; 5,000 authenticated requests/hour; 1,000 `GITHUB_TOKEN` requests/hour per repository | Rate-limited, not separately billed |
| GitHub Pages | One Pages site per account or repository | Static hosting from a repository |
| GitHub Wiki | Soft limit of 5,000 total files | Wiki is repository-scoped |
| GitHub Copilot | Up to 2,000 completions/month | Free add-on quota |

## Catalog

### Core repository and collaboration

- **Unlimited repositories** — GitHub Free includes unlimited public and private repositories. Activation is just creating the repository. **Status: USED.**
- **Collaborators** — Public and private repositories can have unlimited collaborators on GitHub Free. Activate by inviting people or teams in repository settings. **Status: NOT OBSERVED.**
- **Issues** — Free work tracking for bugs, tasks, sub-issues, dependencies, labels, milestones, mentions, templates, and notifications. Issues can be created in the web UI, via GitHub CLI, via the API, or from GitHub Mobile. **Status: USED.**
- **Pull requests and code review** — Free collaboration surface for proposing and reviewing changes. Includes draft pull requests, multiple reviewers, multiple assignees, automatic code review assignment, scheduled reminders, merge checks, and the Conversation / Commits / Checks / Files changed views. Some advanced controls are public-repo-only on Free. Activate by opening a PR from a branch or fork. **Status: NOT USED.**
- **Projects** — Free tables, boards, roadmaps, custom fields, views, templates, charts, and automation. Projects can use up to 50 fields, including built-in metadata and custom fields. Activate from the Projects tab. **Status: NOT OBSERVED.**
- **Milestones** — Free way to group issues and pull requests around a target release or theme. Activate from an issue or milestone page. **Status: NOT OBSERVED.**
- **Discussions** — Free forum-style conversations for Q&A, ideas, announcements, and polls. Enable in repository Settings → Features → Discussions, or at the organization level if needed. **Status: NOT USED.**
- **Templates** — Issue templates/forms, pull request templates, and template repositories are free. Activate by adding files under `.github/` or by marking a repository as a template. **Status: NOT USED.**
- **Core repository mechanics** — Branches, tags, commits/history, forks, stars, watches, notifications, search, compare, blame, releases, and archive downloads are free by default because they are part of normal GitHub repository use. **Status: USED for repository hosting, branches, commits, and docs; otherwise NOT OBSERVED.**

### Documentation and publishing

- **GitHub Pages** — Free static website hosting from a repository. One Pages site per account and one Pages site per repository are the key structural limits; custom domains are supported. Activate in repository Settings → Pages. **Status: NOT USED.**
- **GitHub Wiki** — Free repository wiki for longer-form documentation. Wikis have a 5,000-file soft limit and are enabled per repository. Activate in repository Settings → Features → Wikis. **Status: NOT USED.**
- **Markdown rendering and diagrams** — Markdown, fenced code blocks, Mermaid, GeoJSON, TopoJSON, and ASCII STL render for free across GitHub surfaces. Use normal Markdown in repository files, issues, pull requests, and wikis. **Status: USED for repository docs.**
- **Gists** — Free code-snippet sharing with public and secret gists. Secret gists are unlisted, not private. Gists can be created in the web UI or with GitHub CLI. **Status: NOT USED.**

### Automation and delivery

- **GitHub Actions** — Free CI/CD automation with 2,000 minutes/month on GitHub Free, free execution in public repositories, 500 MB artifact storage, 10 GB cache per repository, and a 20-job concurrency limit on standard runners. Linux, Windows, and macOS runners consume minutes at different rates, with macOS being the most expensive. Activate by adding workflows in `.github/workflows/`. **Status: USED.**
- **Actions artifacts and cache** — Artifacts are part of the Actions allowance; cache storage is separate and capped at 10 GB per repository on Free. Cache uploads are rate-limited. **Status: USED for workflows, but artifact/cache features are not separately exercised.**
- **GitHub Packages / GHCR** — Free package storage is 500 MB on GitHub Free, shared with Actions artifacts. Public repositories can use Packages for free. Activate by publishing packages or container images from Actions or the CLI. **Status: NOT USED.**
- **GitHub Codespaces** — Free dev environments for personal accounts only: 120 core hours/month and 15 GB storage on GitHub Free; 180 hours/20 GB on GitHub Pro. Organization plans do not receive the personal free quota. Compute scales by machine size: 2-core $0.18/hour, 4-core $0.36, 8-core $0.72, 16-core $1.44, 32-core $2.88; storage is $0.07/GB-month. Activate by clicking Code → Codespaces or via `gh codespace`. **Status: NOT USED.**

### Security and supply chain

- **Dependabot alerts** — Included in GitHub Free for dependency-graph-backed vulnerability alerts. Alerts show vulnerable dependencies on the Security tab and dependency graph. Activate by enabling the dependency graph and Dependabot alerts. **Status: NOT USED.**
- **Dependabot security updates** — Free automated pull requests that fix vulnerable dependencies raised by Dependabot alerts. Activate with repository security settings and, optionally, `.github/dependabot.yml`. **Status: NOT USED.**
- **Dependabot version updates** — Free automated pull requests that keep dependencies up to date even when no vulnerability exists. Activate with `.github/dependabot.yml`. **Status: NOT USED.**
- **Secret scanning** — Free on public repositories; scans git history, issues, pull requests, Discussions, wikis, and secret gists for exposed credentials. Activate in Security → Code security and analysis. **Status: NOT USED.**
- **Push protection** — Free on public repositories; blocks secrets before they enter the repository. Activate with secret scanning / push protection settings. **Status: NOT USED.**
- **Code scanning with CodeQL** — Free on public repositories; uses GitHub Actions to scan code for vulnerabilities and errors. Activate via Security → Code scanning → Set up CodeQL. **Status: NOT USED.**
- **CODEOWNERS** — Free file-based ownership and automatic review requests. A code owner can be required to approve when branch protection or rulesets demand it. Activate by creating `.github/CODEOWNERS` (or the repo-root/docs equivalent). **Status: NOT USED.**
- **Branch protection, rulesets, and status checks** — Free policy controls for blocking force pushes, requiring reviews, requiring code owner review, and requiring CI checks before merge. GitHub’s newer ruleset model is more plan-sensitive than basic branch protection, so the safe free baseline for a private repo is branch protection plus required status checks. **Status: NOT USED.**
- **Repository security advisories** — Free private disclosure and public publication workflow for vulnerabilities in public repositories. Activate in Security → Advisories. **Status: NOT USED.**
- **Dependency graph, SBOMs, and artifact attestations** — Dependency graph powers Dependabot; SBOM export and artifact attestations are free on public repositories and improve supply-chain visibility. Activate from the repository security and dependency graph settings. **Status: NOT USED.**

### Tooling, APIs, and mobile access

- **GitHub API** — Free platform access, but rate-limited: 60 requests/hour unauthenticated, 5,000 requests/hour authenticated, and 1,000 requests/hour for `GITHUB_TOKEN` per repository. Activate by using REST or GraphQL with a token. **Status: NOT USED.**
- **GitHub CLI** — Free, open-source command-line client for repositories, issues, pull requests, workflows, releases, gists, codespaces, and API access. Activate by installing `gh` and signing in. **Status: NOT USED.**
- **GitHub Mobile** — Free iOS/Android app for notifications, issues, pull requests, file edits, repo browsing, code search, and 2FA. Activate by installing the app and signing in. **Status: NOT USED.**
- **GitHub Copilot free tier** — GitHub’s pricing page includes a free quota of up to 2,000 completions per month. This is an add-on free tier rather than part of the base repository feature set. Activate by enrolling in Copilot from the pricing/account flow. **Status: NOT USED.**
- **GitHub Apps and Marketplace integrations** — GitHub Apps can be installed without GitHub charging a separate app fee; the app itself may still have its own pricing. Activate by installing an app from the Marketplace or an app owner. **Status: NOT OBSERVED.**

### Lesser-known free collaboration features

- **Multiple issue assignees** — Free on public repositories; lets multiple people own the same issue. **Status: NOT USED.**
- **Multiple pull request assignees** — Free on public repositories; lets multiple people track a pull request. **Status: NOT USED.**
- **Draft pull requests** — Free on public repositories; useful for work-in-progress collaboration before formal review. **Status: NOT USED.**
- **Repository insights** — Free on public repositories; exposes activity and contribution trends for the repository. **Status: NOT USED.**
- **Scheduled reminders** — Free on public repositories; sends scheduled reminders for open pull requests. **Status: NOT USED.**
- **Automatic code review assignment** — Free on public repositories; assigns reviewers automatically based on built-in algorithms. **Status: NOT USED.**
- **Environment protection rules and deployment branches/secrets** — Free on public repositories; lets workflow jobs wait for approvals and use branch-scoped deployment secrets. **Status: NOT USED.**

## Current adoption snapshot for JAGM IT Company

- **USED today:** GitHub repository hosting, GitHub Issues, and GitHub Actions.
- **Visible but not yet used here:** Pages, Wiki, Discussions, Projects, Packages, Codespaces, security automation, CLI/mobile workflows, GitHub Gists, and the newer free AI quota.
- **Public-repo-only features:** currently not adopted in this private repository, so they remain potential future options rather than present usage.

## Sources

- https://github.com/pricing
- https://docs.github.com/en/actions/reference/limits
- https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions
- https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces
- https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues
- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects
- https://docs.github.com/en/discussions/quickstart
- https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages
- https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis
- https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning
- https://docs.github.com/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql
- https://docs.github.com/code-security/dependabot/dependabot-alerts/about-dependabot-alerts
- https://docs.github.com/code-security/dependabot/dependabot-security-updates/about-dependabot-security-updates
- https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates
- https://docs.github.com/en/code-security/concepts/supply-chain-security/about-the-dependabot-yml-file
- https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- https://docs.github.com/code-security/security-advisories/repository-security-advisories/about-repository-security-advisories
- https://docs.github.com/en/github-cli/github-cli/about-github-cli
- https://docs.github.com/en/get-started/using-github/github-mobile
- https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists
