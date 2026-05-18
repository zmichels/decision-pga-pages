from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "article.md"
OUTPUT = ROOT / "assets" / "decision-pga-decision-state-diagnostics.pdf"
BUILD_DIR = ROOT / ".publication-build"
HTML_OUTPUT = BUILD_DIR / "decision-pga-print.html"


CHROME_CANDIDATES = [
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
]


def strip_front_matter(markdown: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", markdown, flags=re.S)


def inline_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(
        r"(https?://[^\s<]+)",
        lambda match: f'<a href="{match.group(1)}">{match.group(1)}</a>',
        escaped,
    )
    return escaped


def table_to_html(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)

    if not rows:
        return ""

    head = rows[0]
    body = rows[1:]
    thead = "<thead><tr>" + "".join(f"<th>{inline_markup(cell)}</th>" for cell in head) + "</tr></thead>"
    tbody_rows = []
    for row in body:
        tbody_rows.append("<tr>" + "".join(f"<td>{inline_markup(cell)}</td>" for cell in row) + "</tr>")
    tbody = "<tbody>" + "".join(tbody_rows) + "</tbody>"
    return f'<table class="state-table">{thead}{tbody}</table>'


def figure_to_html(block: str) -> str:
    svg_uri = (ROOT / "assets" / "decision-pga-diagnostic-loop.svg").resolve().as_uri()
    block = re.sub(
        r"\{\{\s*'/assets/decision-pga-diagnostic-loop\.svg(?:\?v=[^']*)?'\s*\|\s*relative_url\s*\}\}",
        svg_uri,
        block,
    )
    return block


def markdown_to_html(markdown: str) -> str:
    markdown = strip_front_matter(markdown).strip()
    lines = markdown.splitlines()
    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("<figure"):
            block = [line]
            i += 1
            while i < len(lines):
                block.append(lines[i])
                if lines[i].strip() == "</figure>":
                    i += 1
                    break
                i += 1
            out.append(figure_to_html("\n".join(block)))
            continue

        if stripped.startswith("<p class=\"article-meta\">"):
            block = [line]
            i += 1
            while i < len(lines):
                block.append(lines[i])
                if lines[i].strip() == "</p>":
                    i += 1
                    break
                i += 1
            out.append("\n".join(block))
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline_markup(heading.group(2))}</h{level}>")
            i += 1
            continue

        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            out.append(table_to_html(table_lines))
            continue

        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                item_lines = [lines[i].strip()[2:]]
                i += 1
                while i < len(lines) and lines[i].startswith("  ") and lines[i].strip():
                    item_lines.append(lines[i].strip())
                    i += 1
                items.append(" ".join(item_lines))
            out.append("<ul>" + "".join(f"<li>{inline_markup(item)}</li>" for item in items) + "</ul>")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                i += 1
                while i < len(lines) and lines[i].startswith("   ") and lines[i].strip():
                    item += " " + lines[i].strip()
                    i += 1
                items.append(item)
            out.append("<ol>" + "".join(f"<li>{inline_markup(item)}</li>" for item in items) + "</ol>")
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            next_line = lines[i]
            next_stripped = next_line.strip()
            if (
                not next_stripped
                or next_stripped.startswith(("#", "- ", "|", "<figure", "<p class=\"article-meta\">"))
                or re.match(r"^\d+\.\s+", next_stripped)
            ):
                break
            paragraph_lines.append(next_stripped)
            i += 1
        out.append(f"<p>{inline_markup(' '.join(paragraph_lines))}</p>")

    return "\n".join(out)


def render_html(article_html: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Decision-PGA and the Need for Decision-State Diagnostics</title>
    <style>
      @page {{
        size: Letter;
        margin: 0.78in 0.82in 0.84in 0.82in;
      }}

      * {{
        box-sizing: border-box;
      }}

      body {{
        margin: 0;
        color: #172033;
        background: white;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 10.6pt;
        font-weight: 400;
        line-height: 1.48;
        text-rendering: optimizeLegibility;
      }}

      h1 {{
        margin: 0 0 0.16in;
        color: #111827;
        font-size: 27pt;
        line-height: 1.08;
        letter-spacing: 0;
      }}

      h2 {{
        margin: 0.34in 0 0.12in;
        color: #111827;
        font-size: 15.4pt;
        line-height: 1.2;
        break-after: avoid;
      }}

      h3 {{
        margin: 0.26in 0 0.08in;
        color: #111827;
        font-size: 11.7pt;
        line-height: 1.22;
        break-after: avoid;
      }}

      p {{
        margin: 0 0 0.12in;
        orphans: 3;
        widows: 3;
      }}

      .article-meta {{
        margin: 0 0 0.31in;
        color: #5d687a;
        font-size: 10.4pt;
        font-weight: 650;
        line-height: 1.42;
      }}

      a {{
        color: #174a59;
        text-decoration: none;
        overflow-wrap: anywhere;
      }}

      ul,
      ol {{
        margin: 0 0 0.16in 0.24in;
        padding-left: 0.18in;
      }}

      li {{
        margin: 0 0 0.055in;
        break-inside: avoid;
      }}

      .diagram-figure {{
        margin: 0.24in 0 0.24in;
        break-inside: avoid;
      }}

      .diagram-figure img {{
        display: block;
        width: 100%;
        height: auto;
        border: 1px solid #dbe1ea;
        background: #f7f8fb;
      }}

      .diagram-figure figcaption {{
        margin-top: 0.07in;
        color: #5d687a;
        font-size: 9.2pt;
        line-height: 1.35;
      }}

      .state-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 0.14in 0 0.18in;
        font-size: 9.5pt;
        break-inside: avoid;
      }}

      th,
      td {{
        border-bottom: 1px solid #dbe1ea;
        padding: 0.075in 0.055in;
        text-align: left;
        vertical-align: top;
      }}

      th {{
        color: #5d687a;
        font-weight: 750;
      }}

      @media print {{
        html,
        body {{
          width: auto;
          min-height: auto;
        }}
      }}
    </style>
  </head>
  <body>
    <article>
      {article_html}
    </article>
  </body>
</html>
"""


def find_chrome() -> Path:
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate
    for name in ("google-chrome", "chromium", "chrome"):
        found = shutil.which(name)
        if found:
            return Path(found)
    raise SystemExit("Could not find Chrome or Chromium for PDF generation.")


def build_pdf() -> None:
    BUILD_DIR.mkdir(exist_ok=True)
    html_text = render_html(markdown_to_html(ARTICLE.read_text(encoding="utf-8")))
    HTML_OUTPUT.write_text(html_text, encoding="utf-8")

    chrome = find_chrome()
    command = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=1000",
        f"--print-to-pdf={OUTPUT}",
        HTML_OUTPUT.resolve().as_uri(),
    ]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode != 0:
        sys.stderr.write(completed.stderr)
        raise SystemExit(completed.returncode)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
