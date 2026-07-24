#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ISSUE_NUMBER = 33
DEFAULT_PREFIX = "[DevOps]"
LOG_FILE = Path(__file__).resolve().with_name("notifications.log")


@dataclass(slots=True)
class AuditSummary:
    report_path: Path
    display_path: str | None = None
    source: str | None = None
    repository: str | None = None
    branch: str | None = None
    generated: str | None = None
    severity: str | None = None
    sections: list[tuple[str, str, str]] | None = None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_first_match(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def parse_report(report_path: Path) -> AuditSummary:
    text = read_text(report_path)
    summary = AuditSummary(report_path=report_path)
    summary.source = extract_first_match(r"^- Source:\s*`(.+?)`$", text)
    summary.repository = extract_first_match(r"^- Repository:\s*`(.+?)`$", text)
    summary.branch = extract_first_match(r"^- Branch:\s*`(.+?)`$", text)
    summary.generated = extract_first_match(r"^- Generated:\s*`(.+?)`$", text)
    summary.severity = extract_first_match(r"^- Overall severity:\s*\*\*(.+?)\*\*$", text)
    summary.sections = parse_summary_table(text)
    return summary


def parse_summary_table(text: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    in_table = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "| Section | Severity | Findings |":
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table:
            if not line.startswith("|"):
                break
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) != 3 or cells[0].lower() == "section":
                continue
            rows.append((cells[0], cells[1], cells[2]))
    return rows


def build_comment(summary: AuditSummary, prefix: str) -> str:
    report_name = summary.display_path or summary.report_path.as_posix()
    lines = [
        f"{prefix} Audit completed.",
        "",
        f"- Report: `{report_name}`",
    ]
    if summary.repository:
        lines.append(f"- Repository: `{summary.repository}`")
    if summary.branch:
        lines.append(f"- Branch: `{summary.branch}`")
    if summary.generated:
        lines.append(f"- Generated: `{summary.generated}`")
    if summary.severity:
        lines.append(f"- Overall severity: **{summary.severity}**")

    lines.extend(["", "### Summary"])
    if summary.sections:
        for section, severity, findings in summary.sections:
            lines.append(f"- {section}: {severity} ({findings})")
    else:
        lines.append("- No summary table was found in the report.")
        lines.append("- Review the audit report file for full details.")

    return "\n".join(lines)


def normalize_github_slug(remote_url: str) -> str | None:
    remote_url = remote_url.strip()
    if not remote_url:
        return None
    if remote_url.startswith("git@github.com:"):
        slug = remote_url.split(":", 1)[1]
    elif remote_url.startswith(("https://github.com/", "http://github.com/")):
        slug = remote_url.split("github.com/", 1)[1]
    else:
        return None
    if slug.endswith(".git"):
        slug = slug[:-4]
    parts = [part for part in slug.split("/") if part]
    if len(parts) < 2:
        return None
    return f"{parts[0]}/{parts[1]}"


def infer_repo_slug(start: Path) -> str | None:
    env_repo = os.getenv("GITHUB_REPOSITORY")
    if env_repo:
        return env_repo.strip() or None

    git_root = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
    )
    if git_root.returncode != 0:
        return None

    remote = subprocess.run(
        ["git", "-C", git_root.stdout.strip(), "remote", "get-url", "origin"],
        text=True,
        capture_output=True,
    )
    if remote.returncode != 0:
        return None

    return normalize_github_slug(remote.stdout)


def post_issue_comment(repo_slug: str | None, issue_number: int, body: str) -> None:
    command = ["gh", "issue", "comment", str(issue_number), "--body", body]
    if repo_slug:
        command.extend(["--repo", repo_slug])

    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(
            "Failed to post GitHub issue comment.\n"
            f"Command: {' '.join(command)}\n"
            f"STDOUT:\n{completed.stdout}\n"
            f"STDERR:\n{completed.stderr}"
        )


def run_win11toast(title: str, message: str) -> bool:
    try:
        from win11toast import toast  # type: ignore
    except Exception:
        return False

    try:
        toast(title, message)
        return True
    except Exception:
        return False


def run_powershell_notification(title: str, message: str) -> bool:
    powershell = shutil.which("pwsh") or shutil.which("powershell")
    if not powershell:
        return False

    script = r"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.Visible = $true
$notify.BalloonTipTitle = $env:NOTIFY_TITLE
$notify.BalloonTipText = $env:NOTIFY_MESSAGE
$notify.BalloonTipIcon = 'Info'
$notify.ShowBalloonTip(5000)
Start-Sleep -Seconds 6
$notify.Dispose()
"""
    env = os.environ.copy()
    env["NOTIFY_TITLE"] = title
    env["NOTIFY_MESSAGE"] = message
    completed = subprocess.run([powershell, "-NoProfile", "-Command", script], env=env, text=True, capture_output=True)
    return completed.returncode == 0


def send_toast(title: str, message: str) -> str:
    if platform.system().lower() != "windows":
        return "skipped (non-Windows host)"

    if run_win11toast(title, message):
        return "win11toast"

    if run_powershell_notification(title, message):
        return "powershell"

    return "skipped (no supported Windows notification backend)"


def append_log(summary: AuditSummary, issue_number: int, comment_status: str, toast_status: str, body: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    payload = {
        "timestamp": timestamp,
        "report": summary.display_path or str(summary.report_path),
        "issue": issue_number,
        "repository": summary.repository,
        "branch": summary.branch,
        "severity": summary.severity,
        "comment_status": comment_status,
        "toast_status": toast_status,
        "summary": body.splitlines()[0] if body else "",
    }
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Notify on audit completion.")
    parser.add_argument("report_path", help="Path to the audit report file")
    parser.add_argument("--issue", type=int, default=DEFAULT_ISSUE_NUMBER, help="GitHub issue number to comment on")
    parser.add_argument("--prefix", default=DEFAULT_PREFIX, help="Comment prefix to include in the GitHub issue comment")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report_path = Path(args.report_path).expanduser().resolve()
    if not report_path.exists():
        raise FileNotFoundError(f"Audit report not found: {report_path}")

    summary = parse_report(report_path)
    summary.display_path = Path(args.report_path).as_posix()
    repo_slug = infer_repo_slug(report_path.parent)
    comment_body = build_comment(summary, args.prefix)

    comment_status = "pending"
    error: Exception | None = None
    try:
        post_issue_comment(repo_slug, args.issue, comment_body)
        comment_status = "posted"
    except Exception as exc:
        error = exc
        comment_status = f"failed: {exc}"

    toast_title = "Audit completed"
    toast_message_parts = [
        summary.repository or report_path.name,
        summary.severity or "Audit complete",
        f"Issue #{args.issue}",
    ]
    toast_status = send_toast(toast_title, " | ".join(toast_message_parts))
    append_log(summary, args.issue, comment_status, toast_status, comment_body)
    print(comment_body)
    if error is not None:
        raise error
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
