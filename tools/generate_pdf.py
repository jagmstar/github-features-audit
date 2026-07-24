from __future__ import annotations

import argparse
import dataclasses
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

try:
    from fpdf import FPDF
except ImportError as exc:  # pragma: no cover - user guidance only
    raise SystemExit(
        "fpdf2 is required. Install it with: pip install fpdf2"
    ) from exc


JAGM_BLUE = (24, 52, 94)
JAGM_BLUE_DARK = (16, 36, 66)
JAGM_SLATE = (91, 102, 119)
JAGM_BORDER = (214, 220, 230)
JAGM_LIGHT = (245, 247, 250)
JAGM_SOFT = (235, 240, 247)
JAGM_TEXT = (34, 45, 58)
SEVERITY_COLORS = {
    "Critical": (191, 57, 52),
    "Warning": (232, 126, 34),
    "Info": (52, 119, 191),
}


@dataclasses.dataclass(slots=True)
class AuditMetadata:
    title: str
    client_name: str
    repo_value: str | None
    repo_url: str | None
    branch: str | None
    generated_at: str | None
    overall_severity: str
    source: str | None


@dataclasses.dataclass(slots=True)
class Section:
    title: str
    level: int
    body_lines: list[str]
    severity: str


@dataclasses.dataclass(slots=True)
class TocEntry:
    title: str
    level: int
    page_no: int = 0


class AuditPDF(FPDF):
    def __init__(self, report_title: str, client_name: str) -> None:
        super().__init__(orientation="P", unit="mm", format="A4")
        self.report_title = report_title
        self.client_name = client_name
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=16)
        self.set_margins(16, 18, 16)

    def header(self) -> None:
        if self.page_no() == 1:
            return

        self.set_fill_color(*JAGM_BLUE)
        self.rect(0, 0, self.w, 15, style="F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.set_xy(self.l_margin, 4)
        self.cell(0, 6, f"JAGM IT Company | {self.report_title}", border=0)
        self.set_font("Helvetica", "", 9)
        self.set_xy(self.l_margin, 10)
        self.cell(0, 4, self.client_name, border=0)
        self.ln(8)

    def footer(self) -> None:
        if self.page_no() == 1:
            return

        self.set_y(-13)
        self.set_draw_color(*JAGM_BORDER)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_text_color(*JAGM_SLATE)
        self.set_font("Helvetica", "I", 8)
        usable_width = self.w - self.l_margin - self.r_margin
        self.cell(usable_width / 2, 5, "JAGM IT Company Audit Report", align="L")
        self.cell(usable_width / 2, 5, f"Page {self.page_no()} of {{nb}}", align="R")


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
SEVERITY_RE = re.compile(r"^Severity:\s*(.+)$", re.IGNORECASE)
METADATA_RE = re.compile(r"^\s*-\s*([A-Za-z][A-Za-z0-9 _/-]*):\s*(.*)$")


def safe_text(value: str | None) -> str:
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKD", str(value))
    normalized = normalized.replace("\u2013", "-").replace("\u2014", "-")
    normalized = normalized.replace("\u2018", "'").replace("\u2019", "'")
    normalized = normalized.replace("\u201c", '"').replace("\u201d", '"')
    return normalized.encode("latin-1", "replace").decode("latin-1")


def clean_inline_markdown(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"\*\*(.+?)\*\*", r"\1", cleaned)
    cleaned = re.sub(r"__(.+?)__", r"\1", cleaned)
    cleaned = re.sub(r"`(.+?)`", r"\1", cleaned)
    cleaned = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1 (\2)", cleaned)
    cleaned = cleaned.replace("\u2022", "-")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return safe_text(cleaned)


def wrap_text(pdf: FPDF, text: str, width: float) -> list[str]:
    text = clean_inline_markdown(text)
    if not text:
        return [""]
    paragraphs = text.split("\n")
    lines: list[str] = []
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split(" ")
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if pdf.get_string_width(candidate) <= width:
                current = candidate
                continue
            if current:
                lines.append(current)
                current = ""
            if pdf.get_string_width(word) <= width:
                current = word
                continue
            chunk = ""
            for char in word:
                candidate_chunk = chunk + char
                if pdf.get_string_width(candidate_chunk) <= width:
                    chunk = candidate_chunk
                else:
                    if chunk:
                        lines.append(chunk)
                    chunk = char
            current = chunk
        if current:
            lines.append(current)
    return lines or [""]


def parse_metadata(lines: list[str], title: str, client_name: str) -> AuditMetadata:
    metadata: dict[str, str] = {}
    for line in lines[:20]:
        match = METADATA_RE.match(line)
        if not match:
            continue
        key = match.group(1).strip().lower()
        value = match.group(2).strip()
        metadata[key] = value

    repo_value = metadata.get("repository") or metadata.get("repo")
    repo_url = normalize_repo_url(repo_value) if repo_value else None
    overall = metadata.get("overall severity") or metadata.get("severity") or "Info"
    return AuditMetadata(
        title=title,
        client_name=client_name,
        repo_value=repo_value,
        repo_url=repo_url,
        branch=metadata.get("branch"),
        generated_at=metadata.get("generated"),
        overall_severity=normalize_severity(overall),
        source=metadata.get("source"),
    )


def normalize_severity(value: str | None) -> str:
    if not value:
        return "Info"
    candidate = value.strip().strip("*").strip("`").strip()
    candidate = candidate.lower()
    if candidate.startswith("crit"):
        return "Critical"
    if candidate.startswith("warn"):
        return "Warning"
    return "Info"


def normalize_repo_url(value: str) -> str:
    value = value.strip().strip("`")
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if value.startswith("git@github.com:"):
        slug = value.split(":", 1)[1]
    else:
        slug = value.lstrip("/")
    if slug.endswith(".git"):
        slug = slug[:-4]
    return f"https://github.com/{slug}"


def parse_sections(lines: list[str]) -> tuple[str, list[Section]]:
    title = "Audit Report"
    sections: list[Section] = []
    current: Section | None = None
    seen_h1 = False

    for line in lines:
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            heading_text = clean_inline_markdown(heading.group(2))
            if level == 1 and not seen_h1:
                title = heading_text or title
                seen_h1 = True
                continue
            if level >= 2:
                if current is not None:
                    sections.append(current)
                current = Section(title=heading_text, level=level, body_lines=[], severity="Info")
                continue

        if current is None:
            if line.strip():
                current = Section(title=title, level=2, body_lines=[line], severity="Info")
            continue
        current.body_lines.append(line)

    if current is not None:
        sections.append(current)

    if not sections:
        sections = [Section(title=title, level=2, body_lines=[], severity="Info")]

    return title, sections


def infer_section_severity(section: Section, overall: str) -> str:
    for raw_line in section.body_lines:
        severity_match = SEVERITY_RE.match(raw_line.strip())
        if severity_match:
            return normalize_severity(severity_match.group(1))
    if section.title.lower() == "summary":
        return normalize_severity(overall)
    return "Info"


def parse_table(block_lines: list[str]) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw_line in block_lines:
        if not TABLE_RE.match(raw_line):
            continue
        cells = [clean_inline_markdown(cell) for cell in raw_line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def is_separator_row(row: list[str]) -> bool:
    return all(re.fullmatch(r"[:\- ]+", cell or "") is not None for cell in row)


def row_has_severity_table(rows: list[list[str]]) -> bool:
    if not rows:
        return False
    header = [cell.lower() for cell in rows[0]]
    return "severity" in header and "findings" in header


def split_blocks(lines: list[str]) -> list[tuple[str, list[str]]]:
    blocks: list[tuple[str, list[str]]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            blocks.append(("blank", [line]))
            i += 1
            continue

        heading = HEADING_RE.match(line)
        if heading and len(heading.group(1)) >= 3:
            blocks.append(("subheading", [heading.group(1), heading.group(2)]))
            i += 1
            continue

        if TABLE_RE.match(line):
            table_lines = [line]
            i += 1
            while i < len(lines) and TABLE_RE.match(lines[i]):
                table_lines.append(lines[i])
                i += 1
            blocks.append(("table", table_lines))
            continue

        if BULLET_RE.match(line):
            list_lines = [line]
            i += 1
            while i < len(lines) and BULLET_RE.match(lines[i]):
                list_lines.append(lines[i])
                i += 1
            blocks.append(("list", list_lines))
            continue

        para_lines = [line]
        i += 1
        while i < len(lines):
            next_line = lines[i]
            if not next_line.strip():
                break
            if HEADING_RE.match(next_line) or TABLE_RE.match(next_line) or BULLET_RE.match(next_line):
                break
            para_lines.append(next_line)
            i += 1
        blocks.append(("paragraph", para_lines))
    return blocks


def render_badge(pdf: FPDF, text: str, color: tuple[int, int, int], x: float, y: float, width: float = 28.0, height: float = 8.0) -> None:
    pdf.set_fill_color(*color)
    pdf.set_draw_color(*color)
    pdf.rect(x, y, width, height, style="F")
    pdf.set_xy(x, y + 1.1)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(width, 5, text, align="C")


def render_cover(pdf: FPDF, metadata: AuditMetadata, sections: list[Section]) -> None:
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)

    pdf.set_fill_color(*JAGM_BLUE_DARK)
    pdf.rect(0, 0, pdf.w, 48, style="F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_xy(16, 16)
    pdf.cell(0, 10, "JAGM IT Company", align="L")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_xy(16, 27)
    pdf.cell(0, 8, "Professional Audit Report", align="L")

    pdf.set_xy(16, 58)
    pdf.set_text_color(*JAGM_TEXT)
    pdf.set_font("Helvetica", "B", 22)
    pdf.multi_cell(0, 11, metadata.title)

    pdf.ln(1)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*JAGM_SLATE)
    pdf.multi_cell(0, 6, "Prepared for secure delivery, executive review, and client handoff.")

    severity_color = SEVERITY_COLORS.get(metadata.overall_severity, JAGM_BLUE)
    pdf.set_xy(16, 90)
    pdf.set_fill_color(*severity_color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(60, 10, f"Audit Tier: {metadata.overall_severity}", align="C", fill=True)

    pdf.set_xy(16, 110)
    pdf.set_fill_color(*JAGM_LIGHT)
    pdf.set_draw_color(*JAGM_BORDER)
    pdf.set_text_color(*JAGM_TEXT)
    pdf.set_font("Helvetica", "", 11)

    cards = [
        ("Client", metadata.client_name),
        ("Repository", metadata.repo_url or metadata.repo_value or "Not provided"),
        ("Generated", format_generated_date(metadata.generated_at)),
        ("Branch", metadata.branch or "main"),
    ]
    card_width = 91
    card_height = 18
    positions = [(16, 110), (103, 110), (16, 132), (103, 132)]
    for (label, value), (x, y) in zip(cards, positions):
        pdf.set_fill_color(*JAGM_LIGHT)
        pdf.rect(x, y, card_width, card_height, style="D")
        pdf.set_xy(x + 4, y + 3)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*JAGM_SLATE)
        pdf.cell(card_width - 8, 4, label.upper())
        pdf.set_xy(x + 4, y + 8)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*JAGM_TEXT)
        pdf.multi_cell(card_width - 8, 5, safe_text(value))

    pdf.set_xy(16, 158)
    pdf.set_fill_color(*JAGM_SOFT)
    pdf.set_draw_color(*JAGM_BORDER)
    pdf.rect(16, 158, 178, 28, style="D")
    pdf.set_xy(20, 163)
    pdf.set_text_color(*JAGM_TEXT)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "Report Snapshot")
    pdf.set_xy(20, 170)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*JAGM_SLATE)
    pdf.multi_cell(
        170,
        5,
        safe_text(
            f"This PDF is generated from {len(sections)} audit section(s) and is formatted for executive review, operational tracking, and archival use."
        ),
    )

    pdf.set_y(-32)
    pdf.set_text_color(*JAGM_SLATE)
    pdf.set_font("Helvetica", "I", 8)
    pdf.multi_cell(0, 4, "JAGM IT Company | Confidential client deliverable")

    pdf.set_auto_page_break(auto=True, margin=16)


def format_generated_date(value: str | None) -> str:
    if not value:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return value


def render_toc(pdf: FPDF, entries: list[TocEntry], placeholder: bool = False) -> None:
    pdf.add_page()
    pdf.set_text_color(*JAGM_TEXT)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Table of Contents")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*JAGM_SLATE)
    pdf.multi_cell(0, 5, "Sections and page references for the audit report.")
    pdf.ln(2)

    line_height = 8
    page_column_width = 18
    title_width = pdf.w - pdf.l_margin - pdf.r_margin - page_column_width
    for entry in entries:
        if pdf.get_y() > pdf.h - 28:
            pdf.add_page()
        indent = 0 if entry.level <= 2 else 6
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*JAGM_TEXT)
        x = pdf.l_margin + indent
        y = pdf.get_y()
        pdf.set_xy(x, y)
        title = safe_text(entry.title)
        if placeholder:
            page_text = "99"
        else:
            page_text = str(entry.page_no)
        pdf.cell(title_width - indent, line_height, title, border=0)
        pdf.set_x(pdf.w - pdf.r_margin - page_column_width)
        pdf.set_text_color(*JAGM_SLATE)
        pdf.cell(page_column_width, line_height, page_text, align="R")
        pdf.set_draw_color(*JAGM_BORDER)
        pdf.line(pdf.l_margin + indent, pdf.get_y() + line_height - 1, pdf.w - pdf.r_margin, pdf.get_y() + line_height - 1)
        pdf.ln(line_height)


def render_summary_table(pdf: FPDF, rows: list[list[str]]) -> None:
    if not rows:
        return

    available_width = pdf.w - pdf.l_margin - pdf.r_margin
    widths = [available_width * 0.30, available_width * 0.16, available_width * 0.54]
    line_height = 5
    row_padding = 2

    def draw_text_box(x: float, y: float, width: float, height: float, text: str, *, bold: bool = False, color: tuple[int, int, int] = JAGM_TEXT, align: str = "L") -> None:
        pdf.set_text_color(*color)
        pdf.set_font("Helvetica", "B" if bold else "", 9 if not bold else 10)
        lines = wrap_text(pdf, text, width - 2 * row_padding)
        text_y = y + row_padding + 3
        for index, line in enumerate(lines):
            pdf.text(x + row_padding, text_y + index * line_height, line if align == "L" else line)

    def draw_row(row: list[str], is_header: bool = False) -> None:
        normalized = [safe_text(cell) for cell in row]
        wrapped = [wrap_text(pdf, cell, widths[idx] - 2 * row_padding) for idx, cell in enumerate(normalized)]
        row_height = max(len(lines) for lines in wrapped) * line_height + 2 * row_padding
        if pdf.get_y() + row_height > pdf.page_break_trigger:
            pdf.add_page()
        start_x = pdf.l_margin
        start_y = pdf.get_y()
        for idx, (text, cell_width) in enumerate(zip(normalized, widths)):
            x = start_x + sum(widths[:idx])
            if is_header:
                pdf.set_fill_color(*JAGM_BLUE)
                pdf.set_draw_color(*JAGM_BLUE)
                pdf.rect(x, start_y, cell_width, row_height, style="FD")
                draw_text_box(x, start_y, cell_width, row_height, text, bold=True, color=(255, 255, 255))
                continue

            pdf.set_draw_color(*JAGM_BORDER)
            pdf.set_fill_color(255, 255, 255)
            pdf.rect(x, start_y, cell_width, row_height, style="D")
            if idx == 1:
                sev = normalize_severity(text)
                color = SEVERITY_COLORS.get(sev, JAGM_SLATE)
                badge_height = min(8, row_height - 2)
                badge_width = min(cell_width - 2 * row_padding, 24)
                badge_x = x + row_padding
                badge_y = start_y + max(row_padding, (row_height - badge_height) / 2)
                pdf.set_fill_color(*color)
                pdf.set_draw_color(*color)
                pdf.rect(badge_x, badge_y, badge_width, badge_height, style="F")
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Helvetica", "B", 9)
                pdf.set_xy(badge_x, badge_y + 1.1)
                pdf.cell(badge_width, 4, sev, align="C")
                continue

            draw_text_box(x, start_y, cell_width, row_height, text, bold=idx == 0)

        pdf.set_y(start_y + row_height)

    header = rows[0]
    data_rows = rows[1:]
    if len(rows) > 1 and is_separator_row(rows[1]):
        data_rows = rows[2:]
    draw_row(header, is_header=True)
    for row in data_rows:
        if is_separator_row(row):
            continue
        draw_row(row, is_header=False)
    pdf.ln(2)


def is_separator_row(row: list[str]) -> bool:
    return all(re.fullmatch(r"[:\- ]+", cell or "") is not None for cell in row)


def render_bullets(pdf: FPDF, lines: list[str]) -> None:
    pdf.set_text_color(*JAGM_TEXT)
    pdf.set_font("Helvetica", "", 10)
    bullet_indent = 6
    text_width = pdf.w - pdf.l_margin - pdf.r_margin - bullet_indent
    for line in lines:
        match = BULLET_RE.match(line)
        if not match:
            continue
        item = clean_inline_markdown(match.group(1))
        wrapped = wrap_text(pdf, item, text_width)
        first = True
        for wrapped_line in wrapped:
            if pdf.get_y() > pdf.page_break_trigger - 8:
                pdf.add_page()
            if first:
                pdf.set_x(pdf.l_margin + bullet_indent)
                pdf.cell(4, 5, "-")
                pdf.set_x(pdf.l_margin + bullet_indent + 4)
                pdf.multi_cell(text_width - 4, 5, wrapped_line)
                first = False
            else:
                pdf.set_x(pdf.l_margin + bullet_indent + 4)
                pdf.multi_cell(text_width - 4, 5, wrapped_line)
    pdf.ln(1)


def render_paragraph(pdf: FPDF, text: str) -> None:
    cleaned = clean_inline_markdown(text)
    if not cleaned:
        pdf.ln(2)
        return
    pdf.set_text_color(*JAGM_TEXT)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, cleaned)
    pdf.ln(1)


def render_subheading(pdf: FPDF, text: str) -> None:
    if pdf.get_y() > pdf.page_break_trigger - 18:
        pdf.add_page()
    pdf.ln(1)
    pdf.set_fill_color(*JAGM_SOFT)
    pdf.set_draw_color(*JAGM_BORDER)
    pdf.set_text_color(*JAGM_BLUE_DARK)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, clean_inline_markdown(text), border=1, fill=True, ln=1)
    pdf.ln(1)


def render_section(pdf: FPDF, section: Section) -> int:
    if pdf.get_y() > pdf.page_break_trigger - 40:
        pdf.add_page()

    start_page = pdf.page_no()
    severity_color = SEVERITY_COLORS.get(section.severity, JAGM_BLUE)
    pdf.set_fill_color(*JAGM_LIGHT)
    pdf.set_draw_color(*JAGM_BORDER)
    pdf.rect(pdf.l_margin, pdf.get_y(), pdf.w - pdf.l_margin - pdf.r_margin, 14, style="D")
    header_y = pdf.get_y()
    pdf.set_xy(pdf.l_margin + 4, header_y + 2)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*JAGM_TEXT)
    pdf.cell(0, 6, clean_inline_markdown(section.title))
    render_badge(pdf, section.severity, severity_color, pdf.w - pdf.r_margin - 30, header_y + 3.0, width=24, height=7)
    pdf.ln(9)

    blocks = split_blocks(section.body_lines)
    for block_type, block_lines in blocks:
        if block_type == "blank":
            pdf.ln(1)
        elif block_type == "subheading":
            render_subheading(pdf, block_lines[1])
        elif block_type == "table":
            rows = parse_table(block_lines)
            if rows and row_has_severity_table(rows):
                render_summary_table(pdf, rows)
            else:
                for row in rows:
                    render_paragraph(pdf, " | ".join(row))
        elif block_type == "list":
            render_bullets(pdf, block_lines)
        else:
            render_paragraph(pdf, " ".join(block_lines))

    return start_page


def build_toc_entries(sections: list[Section]) -> list[TocEntry]:
    return [TocEntry(title=section.title, level=section.level) for section in sections]


def count_toc_pages(entries: list[TocEntry], placeholder: bool) -> int:
    pdf = AuditPDF("Audit Report", "JAGM IT Company")
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Table of Contents")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, "Sections and page references for the audit report.")
    pdf.ln(2)
    line_height = 8
    page_column_width = 18
    title_width = pdf.w - pdf.l_margin - pdf.r_margin - page_column_width
    for entry in entries:
        if pdf.get_y() > pdf.h - 28:
            pdf.add_page()
        indent = 0 if entry.level <= 2 else 6
        x = pdf.l_margin + indent
        y = pdf.get_y()
        pdf.set_xy(x, y)
        pdf.cell(title_width - indent, line_height, safe_text(entry.title), border=0)
        pdf.set_x(pdf.w - pdf.r_margin - page_column_width)
        pdf.cell(page_column_width, line_height, "99" if placeholder else str(entry.page_no), align="R")
        pdf.ln(line_height)
    return pdf.page_no()


def generate_pdf(markdown_path: Path, output_path: Path, client_name: str, repo_url: str | None = None, audit_tier: str | None = None) -> None:
    lines = markdown_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    title, sections = parse_sections(lines)
    metadata = parse_metadata(lines, title, client_name)
    if repo_url:
        metadata.repo_url = repo_url
    if audit_tier:
        metadata.overall_severity = normalize_severity(audit_tier)
    for index, section in enumerate(sections):
        sections[index].severity = infer_section_severity(section, metadata.overall_severity)

    toc_entries = build_toc_entries(sections)

    # First pass: render with a placeholder TOC to discover section page numbers.
    probe_pdf = AuditPDF(metadata.title, metadata.client_name)
    render_cover(probe_pdf, metadata, sections)
    render_toc(probe_pdf, toc_entries, placeholder=True)
    for idx, section in enumerate(sections):
        toc_entries[idx].page_no = render_section(probe_pdf, section)

    # Second pass: render the final document with real page numbers.
    pdf = AuditPDF(metadata.title, metadata.client_name)
    render_cover(pdf, metadata, sections)
    render_toc(pdf, toc_entries, placeholder=False)
    for section in sections:
        render_section(pdf, section)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert an audit markdown report into a professional PDF.")
    parser.add_argument("input", type=Path, help="Path to the markdown audit report")
    parser.add_argument("--output", type=Path, help="Output PDF path")
    parser.add_argument("--client-name", default="JAGM IT Company", help="Client name for the cover page")
    parser.add_argument("--repo-url", default=None, help="Override the repository URL on the cover page")
    parser.add_argument("--audit-tier", default=None, help="Override the audit tier shown on the cover page")
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    input_path: Path = args.input
    if not input_path.exists():
        parser.error(f"Input file not found: {input_path}")

    output_path = args.output or input_path.with_suffix(".pdf")
    generate_pdf(
        markdown_path=input_path,
        output_path=output_path,
        client_name=args.client_name,
        repo_url=args.repo_url,
        audit_tier=args.audit_tier,
    )
    print(f"Generated PDF: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
