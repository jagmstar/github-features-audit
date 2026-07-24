from __future__ import annotations

import argparse
import dataclasses
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence
from urllib.parse import urlparse


SEVERITY_ORDER = {"Info": 0, "Warning": 1, "Critical": 2}
TEXT_EXTENSIONS = {
    ".py",
    ".pyi",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".json",
    ".yml",
    ".yaml",
    ".md",
    ".txt",
    ".toml",
    ".ini",
    ".cfg",
    ".env",
    ".html",
    ".css",
    ".sh",
    ".ps1",
    ".rb",
    ".go",
    ".java",
    ".xml",
    ".yml",
}
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Hardcoded API key", re.compile(r"(?i)\b(?:api[_-]?key|apikey|secret|token|password)\b\s*[:=]\s*['\"]?([A-Za-z0-9_\-\/+=]{12,})['\"]?")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("AWS temporary access key", re.compile(r"\bASIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9-]{16,}\b")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC|DSA) PRIVATE KEY-----")),
]


@dataclasses.dataclass
class SectionReport:
    name: str
    severity: str
    lines: list[str]


@dataclasses.dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


@dataclasses.dataclass
class Finding:
    path: Path
    line: int
    rule: str
    excerpt: str


@dataclasses.dataclass
class AuditContext:
    source_root: Path
    repo_slug: str | None
    branch: str | None
    output_path: Path
    clone_tempdir: tempfile.TemporaryDirectory[str] | None = None


class AuditError(RuntimeError):
    pass


def run_command(command: Sequence[str], cwd: Path | None = None, check: bool = False) -> CommandResult:
    completed = subprocess.run(
        list(command),
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
    )
    if check and completed.returncode != 0:
        raise AuditError(
            f"Command failed ({completed.returncode}): {' '.join(command)}\n"
            f"STDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
        )
    return CommandResult(completed.returncode, completed.stdout, completed.stderr)


def normalize_github_slug(repo_url: str) -> str | None:
    repo_url = repo_url.strip()
    if not repo_url:
        return None

    if repo_url.startswith("git@github.com:"):
        slug = repo_url.split(":", 1)[1]
    elif repo_url.startswith("https://github.com/") or repo_url.startswith("http://github.com/"):
        slug = urlparse(repo_url).path.lstrip("/")
    else:
        return None

    if slug.endswith(".git"):
        slug = slug[:-4]
    parts = [part for part in slug.split("/") if part]
    if len(parts) < 2:
        return None
    return f"{parts[0]}/{parts[1]}"


def looks_like_repo_slug(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value.strip()))


def looks_like_git_source(value: str) -> bool:
    return value.startswith(("http://", "https://", "git@")) or value.endswith(".git")


def clone_repository(repo_source: str) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
    tempdir = tempfile.TemporaryDirectory(prefix="audit-pipeline-")
    clone_root = Path(tempdir.name)
    clone_target = f"https://github.com/{repo_source}.git" if looks_like_repo_slug(repo_source) else repo_source
    result = run_command(["git", "clone", "--depth", "1", clone_target, str(clone_root)])
    if result.returncode != 0:
        tempdir.cleanup()
        raise AuditError(
            f"Failed to clone repository '{repo_source}'.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return clone_root, tempdir


def resolve_source(source: str) -> tuple[Path, tempfile.TemporaryDirectory[str] | None]:
    candidate = Path(source)
    if candidate.exists():
        return candidate.resolve(), None

    if looks_like_repo_slug(source) or looks_like_git_source(source):
        root, tempdir = clone_repository(source)
        return root.resolve(), tempdir

    raise AuditError(f"Source path or repository reference not found: {source}")


def collect_files(root: Path, extensions: set[str] | None = None) -> list[Path]:
    skip_dirs = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".mypy_cache", ".pytest_cache"}
    items: list[Path] = []
    for path in root.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.is_file():
            if extensions is None or path.suffix.lower() in extensions:
                items.append(path)
    return sorted(items)


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def is_probably_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    if path.name in {"Dockerfile", "Makefile", "SECURITY.md", "LICENSE", "README"}:
        return True
    return False


def scan_secrets(root: Path, output_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    excluded = {output_path.resolve()}
    for path in collect_files(root):
        if path.resolve() in excluded:
            continue
        if not is_probably_text(path):
            continue
        try:
            text = read_text_file(path)
        except OSError:
            continue
        if len(text) > 1_000_000:
            text = text[:1_000_000]

        for line_number, line in enumerate(text.splitlines(), start=1):
            for rule_name, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            path=path,
                            line=line_number,
                            rule=rule_name,
                            excerpt=line.strip()[:220],
                        )
                    )
                    break
    return findings


def load_yaml_module():
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    return yaml


def validate_yaml_file(path: Path, yaml_module) -> tuple[bool, str | None]:
    text = read_text_file(path)
    try:
        if yaml_module is None:
            raise RuntimeError("PyYAML not available")
        yaml_module.safe_load(text)
        return True, None
    except Exception as exc:
        return False, str(exc)


def validate_yaml_files(root: Path) -> list[tuple[Path, str]]:
    yaml_module = load_yaml_module()
    issues: list[tuple[Path, str]] = []
    for path in collect_files(root, {".yml", ".yaml"}):
        ok, error = validate_yaml_file(path, yaml_module)
        if not ok:
            issues.append((path, error or "Unknown YAML validation error"))
    return issues


def find_security_policy(root: Path) -> Path | None:
    for candidate in [root / "SECURITY.md", root / ".github" / "SECURITY.md"]:
        if candidate.exists():
            return candidate
    for candidate in root.rglob("SECURITY.md"):
        if any(part in {".git", "node_modules", ".venv", "venv"} for part in candidate.parts):
            continue
        return candidate
    return None


def get_git_remote_slug(root: Path) -> str | None:
    result = run_command(["git", "-C", str(root), "rev-parse", "--show-toplevel"])
    if result.returncode != 0:
        return None
    try:
        top_level = Path(result.stdout.strip()).resolve()
    except Exception:
        return None
    if top_level != root.resolve():
        return None

    remote = run_command(["git", "-C", str(root), "remote", "get-url", "origin"])
    if remote.returncode != 0:
        return None
    return normalize_github_slug(remote.stdout.strip())


def load_audit_metadata(root: Path) -> dict[str, object]:
    for candidate in [root / ".audit.json", root / "audit.json"]:
        if candidate.exists():
            try:
                return json.loads(read_text_file(candidate))
            except Exception:
                return {}
    return {}


def get_branch_protection_from_metadata(root: Path, branch: str | None) -> tuple[bool | None, str | None]:
    metadata = load_audit_metadata(root)
    if not metadata:
        return None, None
    if branch is None:
        branch = str(metadata.get("branch") or "main")
    if "branch_protection" not in metadata:
        return None, branch
    value = metadata.get("branch_protection")
    if isinstance(value, bool):
        return value, branch
    return None, branch


def determine_branch_protection(repo_slug: str | None, root: Path, branch_override: str | None) -> SectionReport:
    branch = branch_override
    if repo_slug:
        if branch is None:
            repo_info = run_command(["gh", "api", f"repos/{repo_slug}", "--jq", ".default_branch"])
            if repo_info.returncode == 0:
                branch = repo_info.stdout.strip() or "main"
            else:
                branch = "main"
        protection = run_command(["gh", "api", f"repos/{repo_slug}/branches/{branch}/protection"])
        if protection.returncode == 0:
            try:
                payload = json.loads(protection.stdout)
                status_checks = payload.get("required_status_checks")
                enforcement = payload.get("enforcement_level") or payload.get("required_pull_request_reviews")
                details = [f"Branch `{branch}` is protected."]
                if isinstance(status_checks, dict):
                    details.append("Required status checks are enabled.")
                if enforcement:
                    details.append("Protection rules were returned by GitHub.")
                return SectionReport("Branch Protection", "Info", details)
            except Exception:
                return SectionReport("Branch Protection", "Info", [f"Branch `{branch}` is protected according to GitHub."])

        stderr = (protection.stderr or "").strip()
        stdout = (protection.stdout or "").strip()
        combined = "\n".join(part for part in [stdout, stderr] if part)
        if "404" in combined or "not found" in combined.lower():
            return SectionReport(
                "Branch Protection",
                "Warning",
                [f"Branch `{branch}` is not protected according to GitHub API."]
            )
        return SectionReport(
            "Branch Protection",
            "Warning",
            [
                f"Unable to verify branch protection for `{repo_slug}` on branch `{branch}`.",
                combined or "GitHub API returned an unexpected response.",
            ],
        )

    metadata_protected, metadata_branch = get_branch_protection_from_metadata(root, branch)
    if metadata_protected is not None:
        branch = metadata_branch or branch or "main"
        if metadata_protected:
            return SectionReport("Branch Protection", "Info", [f"Branch `{branch}` is protected (local audit metadata)."])
        return SectionReport("Branch Protection", "Warning", [f"Branch `{branch}` is not protected (local audit metadata)."])

    return SectionReport(
        "Branch Protection",
        "Warning",
        [
            "Unable to verify branch protection because no GitHub repository identifier was provided.",
            "Pass --repo owner/name or run inside a Git repository with a GitHub origin remote.",
        ],
    )


def check_ci_coverage(root: Path) -> SectionReport:
    workflows_dir = root / ".github" / "workflows"
    if not workflows_dir.exists():
        return SectionReport(
            "CI Coverage",
            "Warning",
            ["No `.github/workflows/` directory was found.", "Continuous integration coverage is absent."],
        )

    workflow_files = [path for path in workflows_dir.rglob("*.yml")] + [path for path in workflows_dir.rglob("*.yaml")]
    workflow_files = sorted(set(workflow_files))
    if not workflow_files:
        return SectionReport(
            "CI Coverage",
            "Warning",
            ["`.github/workflows/` exists, but no workflow YAML files were found."],
        )

    yaml_module = load_yaml_module()
    invalid: list[str] = []
    for path in workflow_files:
        ok, error = validate_yaml_file(path, yaml_module)
        if not ok:
            invalid.append(f"{path.relative_to(root)}: {error}")

    if invalid:
        return SectionReport(
            "CI Coverage",
            "Critical",
            [
                f"Found {len(workflow_files)} workflow file(s), but {len(invalid)} failed YAML validation.",
                *[f"- {item}" for item in invalid],
            ],
        )

    return SectionReport(
        "CI Coverage",
        "Info",
        [f"Found {len(workflow_files)} valid workflow file(s) under `.github/workflows/`."]
    )


def check_security_policy(root: Path) -> SectionReport:
    security_doc = find_security_policy(root)
    if security_doc:
        return SectionReport(
            "Security Policy",
            "Info",
            [f"`SECURITY.md` found at `{security_doc.relative_to(root)}`."]
        )
    return SectionReport(
        "Security Policy",
        "Info",
        ["No `SECURITY.md` file was found.", "Consider adding a security disclosure process for contributors and users."]
    )


def lint_python_files(root: Path, files: list[Path]) -> tuple[str, str]:
    if not files:
        return "Info", "No Python files were found."

    pylint = shutil.which("pylint")
    if pylint:
        result = run_command([pylint, "--score=n", *[str(path) for path in files]], cwd=root)
        if result.returncode == 0:
            return "Info", f"pylint passed for {len(files)} Python file(s)."
        return "Warning", f"pylint reported issues:\n{(result.stdout + result.stderr).strip()}"

    import py_compile

    compile_errors: list[str] = []
    for path in files:
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            compile_errors.append(f"{path.relative_to(root)}: {exc}")
    if compile_errors:
        return "Warning", "Python syntax check failed:\n" + "\n".join(f"- {item}" for item in compile_errors)
    return "Info", f"Python syntax check passed for {len(files)} file(s)."


def lint_js_files(root: Path, files: list[Path]) -> tuple[str, str]:
    if not files:
        return "Info", "No JavaScript or TypeScript files were found."

    eslint = shutil.which("eslint")
    if eslint:
        result = run_command([eslint, *[str(path) for path in files]], cwd=root)
        if result.returncode == 0:
            return "Info", f"eslint passed for {len(files)} file(s)."
        return "Warning", f"eslint reported issues:\n{(result.stdout + result.stderr).strip()}"

    node = shutil.which("node")
    checkable = [path for path in files if path.suffix.lower() in {".js", ".mjs", ".cjs", ".jsx"}]
    if node and checkable:
        errors: list[str] = []
        for path in checkable:
            result = run_command([node, "--check", str(path)], cwd=root)
            if result.returncode != 0:
                errors.append(f"{path.relative_to(root)}: {(result.stderr or result.stdout).strip()}")
        if errors:
            return "Warning", "JavaScript syntax check failed:\n" + "\n".join(f"- {item}" for item in errors)
        return "Info", f"JavaScript syntax check passed for {len(checkable)} file(s)."

    return "Info", "No JavaScript linter was available, so code quality checks were skipped for JS/TS files."


def check_code_quality(root: Path) -> SectionReport:
    py_files = collect_files(root, {".py", ".pyi"})
    js_files = collect_files(root, {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"})

    lines: list[str] = []
    severities: list[str] = []

    py_severity, py_message = lint_python_files(root, py_files)
    lines.append(py_message)
    severities.append(py_severity)

    js_severity, js_message = lint_js_files(root, js_files)
    lines.append(js_message)
    severities.append(js_severity)

    overall = "Info"
    for severity in severities:
        if SEVERITY_ORDER[severity] > SEVERITY_ORDER[overall]:
            overall = severity

    return SectionReport("Code Quality", overall, lines)


def scan_yaml_validation_section(root: Path) -> SectionReport:
    issues = validate_yaml_files(root)
    if not issues:
        yaml_files = collect_files(root, {".yml", ".yaml"})
        if yaml_files:
            return SectionReport(
                "YAML Validation",
                "Info",
                [f"Validated {len(yaml_files)} YAML file(s) and found no syntax errors."]
            )
        return SectionReport(
            "YAML Validation",
            "Info",
            ["No YAML files were found outside `.github/workflows/`."]
        )

    return SectionReport(
        "YAML Validation",
        "Critical",
        [
            f"Found {len(issues)} YAML file(s) with syntax errors.",
            *[f"- {path.relative_to(root)}: {error}" for path, error in issues],
        ],
    )


def find_git_repo_slug_and_branch(root: Path, branch_override: str | None) -> tuple[str | None, str | None]:
    repo_slug = get_git_remote_slug(root)
    branch = branch_override
    if branch is None:
        metadata = load_audit_metadata(root)
        if metadata.get("branch"):
            branch = str(metadata["branch"])
    return repo_slug, branch


def generate_report(context: AuditContext, sections: list[SectionReport]) -> str:
    timestamp = datetime.now(timezone.utc).isoformat()
    overall = "Info"
    for section in sections:
        if SEVERITY_ORDER[section.severity] > SEVERITY_ORDER[overall]:
            overall = section.severity

    summary_rows = "\n".join(
        f"| {section.name} | {section.severity} | {len(section.lines)} |" for section in sections
    )

    body = [
        "# Automated Audit Report",
        "",
        f"- Source: `{context.source_root}`",
        f"- Repository: `{context.repo_slug or 'local-path'}`",
        f"- Branch: `{context.branch or 'main'}`",
        f"- Generated: `{timestamp}`",
        f"- Overall severity: **{overall}**",
        "",
        "## Summary",
        "",
        "| Section | Severity | Findings |",
        "|---|---:|---:|",
        summary_rows,
        "",
    ]

    for section in sections:
        body.extend([
            f"## {section.name}",
            "",
            f"Severity: **{section.severity}**",
            "",
        ])
        if section.lines:
            for line in section.lines:
                if line.startswith("-") or line.startswith("*"):
                    body.append(line)
                else:
                    body.append(f"- {line}")
        else:
            body.append("- No findings.")
        body.append("")

    return "\n".join(body).rstrip() + "\n"


def build_sections(context: AuditContext) -> list[SectionReport]:
    secrets = scan_secrets(context.source_root, context.output_path)
    if secrets:
        secret_lines = [f"Found {len(secrets)} potential secret(s)."]
        for finding in secrets[:25]:
            secret_lines.append(
                f"- {finding.path.relative_to(context.source_root)}:{finding.line} - {finding.rule} :: {finding.excerpt}"
            )
        if len(secrets) > 25:
            secret_lines.append(f"- ... and {len(secrets) - 25} more finding(s).")
        secrets_section = SectionReport("Secrets", "Critical", secret_lines)
    else:
        secrets_section = SectionReport("Secrets", "Info", ["No hardcoded secrets were detected."])

    ci_section = check_ci_coverage(context.source_root)
    yaml_section = scan_yaml_validation_section(context.source_root)
    branch_section = determine_branch_protection(context.repo_slug, context.source_root, context.branch)
    security_section = check_security_policy(context.source_root)
    quality_section = check_code_quality(context.source_root)

    ci_lines = list(ci_section.lines)
    if yaml_section.severity == "Critical":
        ci_severity = "Critical"
        ci_lines.extend(["YAML validation found errors in one or more files.", *yaml_section.lines])
    else:
        ci_severity = ci_section.severity
        if yaml_section.lines:
            ci_lines.append(yaml_section.lines[0])
    ci_section = SectionReport(ci_section.name, ci_severity, ci_lines)

    return [secrets_section, ci_section, branch_section, security_section, quality_section]


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the automated GitHub features audit pipeline.")
    parser.add_argument(
        "source",
        nargs="?",
        default=str(Path.cwd()),
        help="Local repository path, GitHub repository slug, or clone URL.",
    )
    parser.add_argument(
        "--repo",
        dest="repo_slug",
        help="GitHub repository slug to use for branch protection checks (owner/name).",
    )
    parser.add_argument(
        "--branch",
        dest="branch",
        help="Branch name to check for protection. Defaults to the repository default branch.",
    )
    parser.add_argument(
        "--output",
        dest="output",
        default=str(Path.cwd() / "audit-report.md"),
        help="Output markdown report path.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    source_root, tempdir = resolve_source(args.source)
    derived_repo_slug, derived_branch = find_git_repo_slug_and_branch(source_root, args.branch)
    repo_slug = args.repo_slug or normalize_github_slug(args.source) or derived_repo_slug
    branch = args.branch or derived_branch
    output_path = Path(args.output).resolve()

    context = AuditContext(
        source_root=source_root,
        repo_slug=repo_slug,
        branch=branch,
        output_path=output_path,
        clone_tempdir=tempdir,
    )

    sections = build_sections(context)
    report = generate_report(context, sections)
    output_path.write_text(report, encoding="utf-8")
    sys.stdout.write(f"Audit report written to {output_path}\n")
    sys.stdout.write(report)

    if tempdir is not None:
        tempdir.cleanup()

    overall = max(sections, key=lambda section: SEVERITY_ORDER[section.severity]).severity if sections else "Info"
    return 1 if overall == "Critical" else 0


if __name__ == "__main__":
    raise SystemExit(main())
