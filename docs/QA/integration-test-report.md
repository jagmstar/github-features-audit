# Audit Pipeline Integration Test Report

- Repository: `F:\AI SDLC rork\github-features-audit`
- Test run time: `2026-07-24T09:24:25.012826+00:00`
- Scope: all 5 audit pipeline test repos
- Result: **PASS**

## Summary

| Test name | Expected result | Actual result | PASS/FAIL |
|---|---|---|---|
| repo-secrets | Must find hardcoded secret (Critical) | Critical secret found: `app.py:1 - Hardcoded API key` | PASS |
| no-ci-repo | Must report missing CI (Warning) | Warning reported: CI coverage is absent | PASS |
| unprotected-branch-repo | Must report missing branch protection (Warning) | Warning reported: branch `main` is not protected | PASS |
| no-security-doc-repo | Must report missing SECURITY.md (Info) | Info reported: `SECURITY.md` is missing | PASS |
| broken-yaml-repo | Must find YAML syntax error (Critical) | Critical YAML validation error reported | PASS |

## Detailed Results

## repo-secrets

- Expected result: Must find hardcoded secret (Critical)
- Actual result: Critical secret found in `app.py` (`API_KEY = "sk-live-1234567890abcdef"`).
- PASS/FAIL: **PASS**

### Actual output

```text
# Automated Audit Report

- Source: `F:\AI SDLC rork\github-features-audit\tools\test-repos\repo-secrets`
- Repository: `local-path`
- Branch: `main`
- Generated: `2026-07-24T09:23:47.743880+00:00`
- Overall severity: **Critical**

## Summary

| Section | Severity | Findings |
|---|---:|---:|
| Secrets | Critical | 2 |
| CI Coverage | Info | 2 |
| Branch Protection | Info | 1 |
| Security Policy | Info | 1 |
| Code Quality | Info | 2 |

## Secrets

Severity: **Critical**

- Found 1 potential secret(s).
- app.py:1 - Hardcoded API key :: API_KEY = "sk-live-1234567890abcdef"

## CI Coverage

Severity: **Info**

- Found 1 valid workflow file(s) under `.github/workflows/`.
- Validated 1 YAML file(s) and found no syntax errors.

## Branch Protection

Severity: **Info**

- Branch `main` is protected (local audit metadata).

## Security Policy

Severity: **Info**

- `SECURITY.md` found at `SECURITY.md`.

## Code Quality

Severity: **Info**

- Python syntax check passed for 1 file(s).
- No JavaScript or TypeScript files were found.
```

## no-ci-repo

- Expected result: Must report missing CI (Warning)
- Actual result: Warning reported for missing `.github/workflows/` directory and absent CI coverage.
- PASS/FAIL: **PASS**

### Actual output

```text
# Automated Audit Report

- Source: `F:\AI SDLC rork\github-features-audit\tools\test-repos\no-ci-repo`
- Repository: `local-path`
- Branch: `main`
- Generated: `2026-07-24T09:23:48.457863+00:00`
- Overall severity: **Warning**

## Summary

| Section | Severity | Findings |
|---|---:|---:|
| Secrets | Info | 1 |
| CI Coverage | Warning | 3 |
| Branch Protection | Info | 1 |
| Security Policy | Info | 1 |
| Code Quality | Info | 2 |

## Secrets

Severity: **Info**

- No hardcoded secrets were detected.

## CI Coverage

Severity: **Warning**

- No `.github/workflows/` directory was found.
- Continuous integration coverage is absent.
- No YAML files were found outside `.github/workflows/`.

## Branch Protection

Severity: **Info**

- Branch `main` is protected (local audit metadata).

## Security Policy

Severity: **Info**

- `SECURITY.md` found at `SECURITY.md`.

## Code Quality

Severity: **Info**

- Python syntax check passed for 1 file(s).
- No JavaScript or TypeScript files were found.
```

## unprotected-branch-repo

- Expected result: Must report missing branch protection (Warning)
- Actual result: Warning reported that branch `main` is not protected.
- PASS/FAIL: **PASS**

### Actual output

```text
# Automated Audit Report

- Source: `F:\AI SDLC rork\github-features-audit\tools\test-repos\unprotected-branch-repo`
- Repository: `local-path`
- Branch: `main`
- Generated: `2026-07-24T09:23:49.016562+00:00`
- Overall severity: **Warning**

## Summary

| Section | Severity | Findings |
|---|---:|---:|
| Secrets | Info | 1 |
| CI Coverage | Info | 2 |
| Branch Protection | Warning | 1 |
| Security Policy | Info | 1 |
| Code Quality | Info | 2 |

## Secrets

Severity: **Info**

- No hardcoded secrets were detected.

## CI Coverage

Severity: **Info**

- Found 1 valid workflow file(s) under `.github/workflows/`.
- Validated 1 YAML file(s) and found no syntax errors.

## Branch Protection

Severity: **Warning**

- Branch `main` is not protected (local audit metadata).

## Security Policy

Severity: **Info**

- `SECURITY.md` found at `SECURITY.md`.

## Code Quality

Severity: **Info**

- Python syntax check passed for 1 file(s).
- No JavaScript or TypeScript files were found.
```

## no-security-doc-repo

- Expected result: Must report missing SECURITY.md (Info)
- Actual result: Info reported that no `SECURITY.md` file was found.
- PASS/FAIL: **PASS**

### Actual output

```text
# Automated Audit Report

- Source: `F:\AI SDLC rork\github-features-audit\tools\test-repos\no-security-doc-repo`
- Repository: `local-path`
- Branch: `main`
- Generated: `2026-07-24T09:23:49.467343+00:00`
- Overall severity: **Info**

## Summary

| Section | Severity | Findings |
|---|---:|---:|
| Secrets | Info | 1 |
| CI Coverage | Info | 2 |
| Branch Protection | Info | 1 |
| Security Policy | Info | 2 |
| Code Quality | Info | 2 |

## Secrets

Severity: **Info**

- No hardcoded secrets were detected.

## CI Coverage

Severity: **Info**

- Found 1 valid workflow file(s) under `.github/workflows/`.
- Validated 1 YAML file(s) and found no syntax errors.

## Branch Protection

Severity: **Info**

- Branch `main` is protected (local audit metadata).

## Security Policy

Severity: **Info**

- No `SECURITY.md` file was found.
- Consider adding a security disclosure process for contributors and users.

## Code Quality

Severity: **Info**

- Python syntax check passed for 1 file(s).
- No JavaScript or TypeScript files were found.
```

## broken-yaml-repo

- Expected result: Must find YAML syntax error (Critical)
- Actual result: Critical YAML syntax error reported in `.github\workflows\ci.yml`.
- PASS/FAIL: **PASS**

### Actual output

```text
# Automated Audit Report

- Source: `F:\AI SDLC rork\github-features-audit\tools\test-repos\broken-yaml-repo`
- Repository: `local-path`
- Branch: `main`
- Generated: `2026-07-24T09:23:49.862754+00:00`
- Overall severity: **Critical**

## Summary

| Section | Severity | Findings |
|---|---:|---:|
| Secrets | Info | 1 |
| CI Coverage | Critical | 5 |
| Branch Protection | Info | 1 |
| Security Policy | Info | 1 |
| Code Quality | Info | 2 |

## Secrets

Severity: **Info**

- No hardcoded secrets were detected.

## CI Coverage

Severity: **Critical**

- Found 1 workflow file(s), but 1 failed YAML validation.
- .github\workflows\ci.yml: mapping values are not allowed here
  in "<unicode string>", line 10, column 10:
        steps:
             ^
- YAML validation found errors in one or more files.
- Found 1 YAML file(s) with syntax errors.
- .github\workflows\ci.yml: mapping values are not allowed here
  in "<unicode string>", line 10, column 10:
        steps:
             ^

## Branch Protection

Severity: **Info**

- Branch `main` is protected (local audit metadata).

## Security Policy

Severity: **Info**

- `SECURITY.md` found at `SECURITY.md`.

## Code Quality

Severity: **Info**

- Python syntax check passed for 1 file(s).
- No JavaScript or TypeScript files were found.
```


## Notes

- The audit pipeline returns a non-zero exit code when critical findings are present; this was expected for `repo-secrets` and `broken-yaml-repo`.
- No bug issue was created because all five test cases matched their expected results.
