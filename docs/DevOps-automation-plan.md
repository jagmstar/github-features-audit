# DevOps Automation Plan: GitHub Infrastructure Features for JAGM IT Company

## Executive summary
JAGM IT Company can build a low-maintenance DevOps platform on top of GitHub by combining:

- **GitHub-hosted runners** for standard CI/CD jobs
- **Self-hosted runners** only where we need private network access, static IPs, specialized hardware, or custom tooling
- **GitHub Packages** and **GitHub Container Registry (GHCR)** for versioned package and image distribution
- **GitHub Environments** for staging/production separation and controlled deployments
- **Secrets, variables, and OIDC** to reduce long-lived credentials
- **Caching, reusable workflows, and Marketplace actions** to keep pipelines fast, consistent, and secure

The guiding principle is to keep the default path simple and fully managed by GitHub, while reserving self-managed infrastructure for exceptions that genuinely need it.

## Assumptions
- The repository is intended to remain public or at least use the free tier as much as possible.
- The main goal is DevOps automation for application delivery, package publishing, and deployment governance.
- We want a design that minimizes operational overhead while still supporting secure production releases.

## Target operating model

### 1) Default execution model: GitHub-hosted runners
Use GitHub-hosted runners for:
- linting
- unit tests
- build verification
- dependency checks
- package publishing jobs that do not require internal network access
- container image builds and pushes to GHCR

Why this is the default:
- GitHub manages the runner VM lifecycle and updates
- each job gets a clean environment
- public repositories can use standard GitHub-hosted runners free and unlimited
- the operational burden is lower than maintaining our own runner fleet

Recommended baseline labels:
- `ubuntu-latest` for most CI/CD jobs
- `windows-latest` only when a Windows toolchain is required
- `macos-latest` only for Apple/macOS-specific builds

### 2) Exception model: self-hosted runners
Use self-hosted runners only when we need:
- access to private on-prem resources
- static or allowlisted IPs
- custom hardware or large memory/CPU allocations
- non-public software already installed internally
- specialized deployment targets in a protected network

Operational rule:
- **Do not use self-hosted runners for untrusted public pull requests**
- Keep self-hosted runners behind runner groups and labels
- Treat self-hosted runners as higher-risk infrastructure because jobs may see credentials and local environment state

Recommended use cases:
- deployment jobs to internal infrastructure
- integrations with on-prem databases or secret managers
- heavy build workloads that exceed standard hosted runner capacity

## Runner strategy

| Runner type | Best use | Pros | Tradeoffs |
|---|---|---|---|
| GitHub-hosted runner | Default CI/CD | Managed, clean, easy to scale, low ops overhead | Less control over network and installed software |
| Larger GitHub-hosted runner | High-memory/CPU or static IP needs | Managed by GitHub, more resources, some networking features | Higher cost / plan constraints |
| Self-hosted runner | Private network, custom hardware, internal tooling | Full control, can be placed close to internal systems | We maintain OS, patching, hardening, and availability |

### Runner policy
1. **CI on GitHub-hosted runners by default**
2. **Deployment jobs use the least-privilege runner that can reach the target**
3. **Self-hosted runners are allowed only for jobs that have a documented infrastructure requirement**
4. **All runner selection must be label-based and documented in workflow YAML**

## Artifact and package management plan

### 1) GitHub Packages
Use GitHub Packages for language-native package publishing and internal reuse:
- **npm** for JavaScript/TypeScript packages
- **Maven** for Java artifacts
- **NuGet** for .NET packages
- **Docker/OCI** artifacts through GHCR

How to use it:
- publish from GitHub Actions on tagged releases or protected merges
- keep package permissions aligned with repository access where possible
- use scoped package naming for npm
- use package source mapping for NuGet to reduce dependency confusion risk

### 2) GitHub Container Registry (ghcr.io)
Use GHCR as the canonical container registry for application images.

Recommended image lifecycle:
- build on merge to `main`
- tag with branch, commit SHA, and release version where appropriate
- push to `ghcr.io/<org>/<image>`
- add OCI labels such as `org.opencontainers.image.source`
- promote the same immutable image digest from staging to production

Preferred tagging model:
- `sha-<commit>` for traceability
- `main` or `latest` only if required for convenience
- semver tags for releases

### 3) Artifacts vs caches
Treat these as different tools:
- **Artifacts**: store build outputs, logs, test reports, and release bundles
- **Caches**: store reusable dependencies and intermediate files that can be regenerated

Rule of thumb:
- If the file is a deliverable, use an artifact
- If the file is a speed optimization, use a cache

## Deployment pipeline design

### Pipeline stages

#### Stage 1: Validate
Trigger: pull request

Jobs:
- lint
- unit test
- static analysis
- dependency audit

Runner:
- GitHub-hosted Ubuntu runner

Outputs:
- test reports
- code quality signals
- package cache warmup

#### Stage 2: Build
Trigger: merge to `main` or tagged release

Jobs:
- build application
- build container image
- package release artifacts

Runner:
- GitHub-hosted runner unless a specialized build needs self-hosted capacity

Outputs:
- release artifact
- GHCR image
- GitHub Packages artifacts where relevant

#### Stage 3: Deploy to staging
Trigger:
- merge to `main`
- manual promotion from release pipeline

Controls:
- environment: `staging`
- required reviewers: optional but recommended for sensitive services
- secrets scoped to staging only

Behavior:
- deploy only after validation succeeds
- write deployment status back to GitHub
- run smoke tests after deployment

#### Stage 4: Deploy to production
Trigger:
- manual approval or release tag promotion

Controls:
- environment: `production`
- required reviewers enabled
- branch restrictions enforced
- wait timer if needed for change windows
- custom deployment protection rule if an external system must approve the release

Behavior:
- production deploy starts only after environment rules pass
- environment secrets remain unavailable until approval completes
- deployment history is retained in GitHub

### Recommended workflow topology

- `.github/workflows/ci.yml` — pull request validation
- `.github/workflows/build.yml` — build and publish outputs
- `.github/workflows/deploy.yml` — environment-gated deployment
- `.github/workflows/release.yml` — release tagging and promotion
- `.github/workflows/reusable-deploy.yml` — reusable deployment logic

## Environment setup guide

### Environments to create
Create at least:
- `staging`
- `production`

Optional:
- `development`
- `preview`

### Environment configuration
For each environment:
1. Set **deployment branches/tags** to restrict who can deploy
2. Add **required reviewers** for production
3. Add **wait timers** if release windows matter
4. Add **environment secrets** for credentials specific to that environment
5. Add **environment variables** for non-sensitive config values

### Secret and variable scoping
Use the right scope for the right job:
- **Repository secrets**: shared CI credentials
- **Repository variables**: non-sensitive global settings
- **Environment secrets**: deployment credentials for a specific target
- **Environment variables**: environment-specific config such as URLs or feature flags

Policy:
- do not place production credentials at repository scope if only production jobs need them
- do not store secrets in workflow files, caches, or artifacts
- use environment-scoped secrets whenever approval gates should protect access

### Recommended approval model
- `staging`: no approval or one lightweight reviewer
- `production`: mandatory reviewer from DevOps/leadership
- prevent self-review for production where feasible

## Secrets and token policy

### GitHub token
Set the default `GITHUB_TOKEN` permissions to the minimum required:
- `contents: read` by default
- elevate only in jobs that publish, deploy, or comment

### Long-lived secrets
Avoid long-lived cloud credentials where possible.
Instead:
- use **OpenID Connect (OIDC)** to exchange GitHub workflow identity for short-lived cloud credentials
- use cloud-native trust policies to scope access to specific repositories, branches, and environments

### Reusable workflow secrets
Important rules:
- secrets are not automatically passed to reusable workflows
- environment secrets remain tied to the environment referenced by the called workflow
- pass only the secrets that a workflow actually needs

## Caching strategy

### What to cache
Cache these kinds of files:
- package manager downloads
- dependency directories
- build tool caches
- generated intermediate files that are expensive to regenerate

Recommended tools:
- `actions/cache`
- `setup-node` for Node.js
- `setup-java` for Maven/Gradle
- `setup-dotnet` for NuGet
- `setup-python` for Python workflows

### Cache key design
Use keys that include:
- runner OS
- lockfile hash
- tool version if relevant
- branch-specific restore keys when useful

Example pattern:
- primary key: `${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}`
- restore keys: progressively broader fallbacks

### Cache security rules
- never store tokens, passwords, certificates, or secret files in cache paths
- keep cache writes on trusted workflows such as `push` to `main` or scheduled maintenance jobs
- use restore-only behavior in low-trust workflows if needed
- periodically review and prune stale caches

## Marketplace actions policy

### What to use
Adopt proven Marketplace actions for common tasks:
- checkout
- language setup
- caching
- Docker login/build/push
- artifact upload/download
- release automation

### How to use them safely
- pin to a major version or, preferably, a full commit SHA
- use verified actions when possible
- keep Dependabot enabled for action updates
- avoid unreviewed third-party actions in production deploy jobs

### Recommended action categories
- source checkout
- setup actions for language toolchains
- Docker login/build/push actions
- artifact upload/download actions
- dependency caching actions
- release and changelog actions

## Reusable workflows and composite actions

### Reusable workflows
Use reusable workflows when we want to standardize a full job or pipeline fragment.
Best use cases:
- build/test workflow template
- deployment workflow template
- release promotion workflow
- compliance or security checks that every repo should run

Benefits:
- centralized maintenance
- less YAML duplication
- consistent environments and permissions
- easy reuse across repositories

### Composite actions
Use composite actions when we want to reuse a sequence of steps inside a single job.
Best use cases:
- language bootstrap logic
- common setup scripts
- shared build helper commands
- deployment helper steps

### Governance rules
- reusable workflows should be called by SHA when possible
- pass inputs explicitly
- pass secrets explicitly
- use `vars` for shared non-sensitive configuration
- do not rely on `env` propagation between caller and called workflow

## Security guardrails

1. **Least privilege everywhere**
   - minimal `GITHUB_TOKEN` permissions
   - environment-scoped secrets only where needed

2. **Protected production deployment**
   - required reviewers
   - branch restrictions
   - optional wait timers
   - custom deployment protection rules when external approval is required

3. **Runner hardening**
   - avoid self-hosted runners for untrusted public PRs
   - isolate runner groups for sensitive workloads

4. **Supply-chain hygiene**
   - pin third-party actions
   - keep Dependabot enabled
   - prefer GHCR and GitHub Packages for internal distribution

5. **Cache safety**
   - never cache secrets
   - treat restored cache contents as untrusted input

## Implementation roadmap

### Phase 1: Foundation
- create reusable CI and deployment workflow templates
- define staging and production environments
- enforce default token permissions
- enable action pinning and Dependabot updates

### Phase 2: Build acceleration
- add dependency caching for npm, Maven, NuGet, or other active stacks
- measure cache hit rate and build time reduction
- add artifact upload for test reports and build bundles

### Phase 3: Package distribution
- publish packages to GitHub Packages where applicable
- publish container images to GHCR
- standardize version tags and OCI labels

### Phase 4: Environment-controlled deployment
- deploy to staging automatically
- require approval for production
- add branch restrictions and protection rules
- use OIDC for cloud auth where possible

### Phase 5: Hardening and operations
- review permissions quarterly
- prune stale caches and old artifacts
- monitor runner usage and workflow duration
- refine reusable workflows based on adoption

## Success metrics
Track the following metrics monthly:
- average CI duration
- cache hit rate
- deployment lead time
- approval wait time for production
- number of failed deployments
- number of workflows using reusable templates
- percentage of actions pinned to SHA or major version

## Evidence and sources consulted
Official GitHub documentation reviewed during research:

- Self-hosted runners: https://docs.github.com/actions/hosting-your-own-runners
- GitHub-hosted runners: https://docs.github.com/actions/using-github-hosted-runners/about-github-hosted-runners
- GitHub-hosted runners reference: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- GitHub Packages documentation: https://docs.github.com/packages
- Working with the Container registry: https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-container-registry
- Deployments and environments: https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
- Managing environments for deployment: https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment
- Using secrets in GitHub Actions: https://docs.github.com/actions/security-guides/using-secrets-in-github-actions
- Dependency caching reference: https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
- Reuse workflows: https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
- Reusing workflow configurations: https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations
- Using pre-written building blocks in your workflow: https://docs.github.com/actions/writing-workflows/choosing-what-your-workflow-does/using-pre-written-building-blocks-in-your-workflow
- Secure use reference: https://docs.github.com/en/actions/reference/security/secure-use
- GitHub Marketplace: https://docs.github.com/marketplace

## Conclusion
This plan keeps GitHub as the control plane for automation, packaging, and deployment governance. The result is a pipeline that is fast by default, secure by design, and flexible enough to grow from simple CI into production-grade delivery.
