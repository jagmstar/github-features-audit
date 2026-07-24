# Audit Results Summary

These three demo audits were run against public GitHub repositories from the target-company list:

1. **Sovri** — `Sovri/sovri`
2. **Lex-Orchestra** — `thomasbln/Lex-Orchestra`
3. **Point.RED** — `point-red/point`

## Executive summary

The audits show the service can quickly assess public repositories for:

- secret-like patterns
- CI workflow coverage and YAML quality
- branch protection posture
- presence of a security policy
- basic code-quality signals by language

Across the three demos, the pipeline surfaced a mix of strong signals and actionable gaps, which is exactly the kind of evidence a buyer wants from a risk-focused repository review service.

## Key findings by audit

### 1) Sovri (`Sovri/sovri`)

- **Overall severity:** Critical
- **Secrets:** Many secret-pattern matches were found, but most appeared in tests and fixtures using fake or sample tokens.
- **CI Coverage:** Workflow files exist, but one YAML file failed validation because of a malformed fixture file.
- **Branch Protection:** `main` is not protected according to GitHub API.
- **Security Policy:** A `SECURITY.md` file exists.

**Takeaway:** This repo demonstrates how the audit detects both real operational concerns and noisy secret-like test data that should be triaged or suppressed.

### 2) Lex-Orchestra (`thomasbln/Lex-Orchestra`)

- **Overall severity:** Critical
- **Secrets:** A few secret-like strings were found in test fixtures.
- **CI Coverage:** No `.github/workflows/` directory was present.
- **Branch Protection:** `main` is not protected according to GitHub API.
- **Security Policy:** No `SECURITY.md` file was found.

**Takeaway:** This repo shows the service identifying a missing CI baseline and missing security policy, both of which are high-value recommendations for any public codebase.

### 3) Point.RED (`point-red/point`)

- **Overall severity:** Warning
- **Secrets:** No hardcoded secrets were detected.
- **CI Coverage:** No `.github/workflows/` directory was present.
- **Branch Protection:** `alpha1` is not protected according to GitHub API.
- **Security Policy:** No `SECURITY.md` file was found.

**Takeaway:** This repo is a good example of a lower-risk codebase that still benefits from governance checks and CI/security hardening recommendations.

## Recommendations

1. **Add or strengthen CI workflows** for every public repo so audits can verify build, test, and lint coverage.
2. **Protect default branches** and require checks before merge.
3. **Add a SECURITY.md** file where missing to provide a clear disclosure path.
4. **Tune secret detection for test fixtures** so known fake tokens do not create unnecessary noise.
5. **Keep YAML valid in all tracked files**, including fixtures, because malformed config can break automation and cloud tooling.

## How this demonstrates service value

This demo proves the audit service can:

- scan multiple public repos quickly
- surface security posture issues in a consistent format
- identify both true governance gaps and noisy findings that need triage
- turn raw repository data into executive-friendly, actionable recommendations

For a sales conversation, the key value is simple: **the service helps companies see risk, fix it faster, and standardize repository governance across teams.**