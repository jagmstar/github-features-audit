# Audit Service Technical Architecture

## 1. Purpose

This document describes the technical architecture of the GitHub Features Audit service. The service analyzes a client repository and produces a private audit report that highlights GitHub feature usage, workflow quality, security posture, and operational opportunities.

The architecture is intentionally GitHub-centric so the audit can run in a controlled CI environment without exporting repository data to external systems.

## 2. Architecture overview

The service is built around four primary system components:

- **`audit_pipeline.py`**
  - Core orchestration script.
  - Collects repository data, runs checks, aggregates findings, and prepares report inputs.
  - Encapsulates the audit logic so it can be executed consistently in CI.

- **GitHub Actions**
  - Execution layer for running the pipeline in a managed CI sandbox.
  - Handles triggers, environment setup, isolation, and artifact publication.
  - Provides repeatable execution for each audit request.

- **Test repos**
  - Controlled sample repositories used for validation, regression testing, and pipeline smoke tests.
  - Ensure changes to the audit logic do not break report generation or assumptions about repo structure.
  - Provide safe fixtures for testing GitHub API interactions and edge cases.

- **Report templates**
  - Markdown or structured templates used to transform findings into client-facing deliverables.
  - Keep the report format stable while allowing the pipeline to update content dynamically.
  - Support standardized sections such as findings, severity, recommendations, and next steps.

## 3. Logical component model

The service is organized into the following layers:

1. **Request intake layer**
   - Receives the audit request from a client-facing process or repository workflow.
   - Validates the target repository, audit scope, and required metadata.

2. **Execution layer**
   - GitHub Actions starts the audit job.
   - The workflow prepares the runtime, checks out the code, and invokes `audit_pipeline.py`.

3. **Analysis layer**
   - `audit_pipeline.py` queries repository metadata, evaluates workflows and files, and produces findings.
   - The pipeline can use test repos during validation to confirm expected behavior.

4. **Report layer**
   - Report templates render the analysis output into a private audit document.
   - The generated report is stored as a private artifact or written to a private repository location.

5. **Delivery layer**
   - The report is delivered back to the client through GitHub-controlled access.
   - Delivery is limited to authenticated GitHub access paths so the output remains private.

## 4. Data flow

The operational flow is:

```text
Client request -> Pipeline run -> Report generation -> Delivery
```

Expanded view:

1. **Client request**
   - A request is submitted with the repository identifier and audit scope.
   - The request is converted into a GitHub workflow input or equivalent repository-controlled trigger.

2. **Pipeline run**
   - GitHub Actions launches a runner and invokes `audit_pipeline.py`.
   - The pipeline reads repository metadata, workflow files, and other relevant GitHub-hosted sources.

3. **Report generation**
   - The analysis output is passed into a report template.
   - The template renders a private markdown report and supporting summary data.

4. **Delivery**
   - The generated report is published as a private artifact, release asset, or repository-controlled document.
   - Only authorized GitHub users can access the output.

## 5. Security architecture

Security is a first-class design constraint.

### Security goals

- **No data leaves GitHub**
  - Repository data, intermediate findings, and final audit outputs remain inside GitHub-controlled storage and GitHub Actions execution.
  - The baseline design avoids sending source content, secrets, or report data to third-party services.

- **Audit runs in a CI sandbox**
  - Each audit executes inside a GitHub Actions runner.
  - The runner provides a temporary, isolated environment with limited lifetime and scoped permissions.
  - The job should use least-privilege token permissions and avoid persistent credentials.

- **Reports are private**
  - Generated reports are not publicly exposed.
  - Access is limited to authenticated users with explicit permission to the repository or artifact.
  - Any future sharing mechanism must preserve the same privacy boundary.

### Security controls

- Use GitHub Actions permissions scoped to the minimum required access.
- Prefer read-only repository access for analysis jobs.
- Store no secrets in report output.
- Redact sensitive values before rendering the report.
- Keep the audit workflow in a private repository or private execution context.
- Use private artifacts or private repository files for delivery.

### Threat model notes

- The main risks are accidental disclosure through logs, artifacts, or misconfigured permissions.
- The pipeline should never print secrets, full tokens, or raw private configuration values.
- Any external integration added later must be reviewed against the no-data-leaves-GitHub constraint.

## 6. Scalability model

The service should support multiple concurrent audits without cross-contamination between jobs.

### Concurrency strategy

- **Per-audit isolated runs**
  - Each client request becomes a separate GitHub Actions run.
  - Every run gets its own workspace, environment variables, and output paths.

- **Parallel job execution**
  - Where possible, split the pipeline into stages such as discovery, analysis, and report rendering.
  - Independent checks can run in parallel to reduce total runtime.

- **Concurrency controls**
  - Use workflow concurrency groups keyed by audit request or repository.
  - Prevent duplicate runs for the same target from overwriting each other.

- **Reusable workflows**
  - Encapsulate the audit workflow so future repos or audit tiers can reuse the same pipeline definition.
  - Centralize validation and reporting logic to reduce maintenance effort.

### Operational scaling considerations

- GitHub API rate limits must be respected when multiple audits run at once.
- Artifact names and output directories should include audit IDs or run IDs.
- Long-running audits should be split into smaller tasks so a single slow check does not block the entire run.
- If volume grows significantly, introduce a queue-like dispatch pattern while keeping the actual execution inside GitHub Actions.

## 7. Integration points

### GitHub API

The pipeline uses the GitHub API to:

- inspect repository metadata
- read workflow and repository settings
- enumerate commits, branches, and file structure where needed
- collect issue or PR context when relevant to the audit scope

The API should be accessed through the GitHub token assigned to the workflow and should be limited to read-only operations whenever possible.

### CI/CD

GitHub Actions is the execution and delivery backbone.

- Triggers the audit pipeline
- Sets up the runtime environment
- Runs tests against controlled test repos
- Publishes the final report as a private artifact or repository-controlled asset
- Records audit results for traceability

### Client communication

Client communication remains GitHub-native in the secure baseline.

- Request metadata can be captured through GitHub-controlled intake.
- Status updates can be shared through private issue comments, workflow run status, or repository notices.
- Final report delivery should stay inside GitHub-controlled access boundaries.

If email or another external channel is introduced later, it should carry only minimal routing metadata and never contain the report body or repository content.

## 8. Current technical debt

The current implementation has several likely limitations:

1. **Monolithic pipeline logic**
   - `audit_pipeline.py` may combine orchestration, analysis, and formatting in one file.
   - This makes testing and change isolation harder.

2. **Limited validation automation**
   - Test repos may cover only a subset of real-world repository shapes.
   - Edge cases such as large repos, unusual workflow structures, or missing metadata may not yet be fully covered.

3. **Report format rigidity**
   - Template-driven output may be constrained to a single markdown style.
   - Alternative delivery formats such as HTML, PDF, or JSON may not yet be available.

4. **Manual output review**
   - Human review may still be needed to refine recommendations or resolve ambiguous findings.

5. **Rate-limit and retry handling**
   - Concurrent GitHub API access can fail without stronger backoff, retry, and pagination controls.

6. **Limited observability**
   - Job logs may not yet provide enough structured telemetry to diagnose recurring pipeline issues.

7. **No formal queue**
   - Audit requests may be launched directly rather than queued and scheduled with priority controls.

## 9. Improvement roadmap

### Near term

- Split `audit_pipeline.py` into smaller modules for discovery, analysis, scoring, and rendering.
- Add stronger fixtures in test repos for common repository patterns and failure cases.
- Standardize report sections and severity scoring across all audit runs.
- Add rate-limit-safe GitHub API wrappers with retries and pagination.

### Mid term

- Create reusable GitHub Actions workflows for audit execution and validation.
- Add structured intermediate output such as JSON alongside markdown.
- Introduce stronger artifact naming, retention, and cleanup rules.
- Add automated smoke tests for pipeline changes before production use.

### Long term

- Add a lightweight dispatch queue for high-volume audit intake.
- Support multi-format report generation while preserving private delivery.
- Add provenance tracking so each report is traceable to a commit, workflow run, and audit scope.
- Improve observability with structured logs and summary metrics.

## 10. Architecture decision summary

- GitHub Actions is the execution platform.
- `audit_pipeline.py` is the main orchestration entry point.
- Test repos provide safe validation coverage.
- Report templates create consistent client output.
- The security model keeps all data inside GitHub and keeps reports private.
- Concurrency is handled with isolated workflow runs and GitHub Actions concurrency controls.

## 11. Conclusion

This architecture keeps the audit service simple, private, and scalable inside GitHub. It uses GitHub Actions for execution, GitHub APIs for analysis, and private report artifacts for delivery. The design supports concurrent audits while preserving strict security boundaries and leaves a clear path for future modularization and automation improvements.