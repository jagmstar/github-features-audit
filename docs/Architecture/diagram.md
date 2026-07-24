# Audit Service Architecture Diagram

```text
Client Request
   |
   v
GitHub Actions Workflow (CI sandbox)
   |
   +--> audit_pipeline.py ------------------------------+
   |        |                                           |
   |        | uses GitHub API                            |
   |        v                                           |
   |   Repository metadata / settings                   |
   |                                                    |
   |        +--> Test Repos (fixtures / regression)     |
   |        |                                           |
   |        +--> Analysis + scoring + findings          |
   |                                                    |
   +--> Report Templates -------------------------------+
            |
            v
     Private Report Artifact / Private Repo Document
            |
            v
     Client Communication via GitHub-only access
```

## Relationships

- **Client Request** starts the audit.
- **GitHub Actions Workflow** provides the execution sandbox and orchestration.
- **`audit_pipeline.py`** performs repository inspection, analysis, and findings generation.
- **GitHub API** supplies read-only repository context when needed.
- **Test Repos** validate the pipeline safely before changes are promoted.
- **Report Templates** convert findings into a consistent client-facing deliverable.
- **Private Report Artifact / Private Repo Document** stores the output securely.
- **Client Communication via GitHub-only access** keeps delivery inside GitHub-controlled permissions.

## Security boundary

- All repository data stays inside GitHub.
- Audit execution happens in the GitHub Actions CI sandbox.
- Reports remain private and access-controlled.

## Scalability notes

- Use one workflow run per audit request.
- Use concurrency groups to prevent collisions for the same target.
- Split discovery, analysis, and rendering into parallel jobs when possible.
- Respect GitHub API rate limits during concurrent runs.
```