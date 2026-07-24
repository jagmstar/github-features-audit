# Audit Kill-Test Suite

This document records the five audit kill-tests used to validate the audit pipeline. Each test confirms that the report generator detects the intended failure mode and reports it clearly.

## Test results

| Test name | Input | Expected output | Actual output | PASS/FAIL |
|---|---|---|---|---|
| repo-secrets | `F:\AI SDLC rork\github-features-audit\tools\test-repos\repo-secrets` | Must find a hardcoded secret and mark it Critical | Critical secret found in `app.py:1` (`API_KEY = "sk-live-1234567890abcdef"`); overall severity Critical | PASS |
| no-ci-repo | `F:\AI SDLC rork\github-features-audit\tools\test-repos\no-ci-repo` | Must report missing CI as a Warning | Warning reported for missing `.github/workflows/` directory and absent CI coverage; overall severity Warning | PASS |
| unprotected-branch-repo | `F:\AI SDLC rork\github-features-audit\tools\test-repos\unprotected-branch-repo` | Must report missing branch protection as a Warning | Warning reported that branch `main` is not protected; overall severity Warning | PASS |
| no-security-doc-repo | `F:\AI SDLC rork\github-features-audit\tools\test-repos\no-security-doc-repo` | Must report missing `SECURITY.md` as Info | Info reported that no `SECURITY.md` file was found; overall severity Info | PASS |
| broken-yaml-repo | `F:\AI SDLC rork\github-features-audit\tools\test-repos\broken-yaml-repo` | Must find a YAML syntax error and mark it Critical | Critical YAML syntax error reported in `.github\workflows\ci.yml`; overall severity Critical | PASS |

## Notes

- These results align with `docs/QA/integration-test-report.md`.
- The audit pipeline is expected to fail the run when critical findings are present in `repo-secrets` and `broken-yaml-repo`.
