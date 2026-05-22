from __future__ import annotations

import html
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / ".publication-build"
SITE_URL = "https://zmichels.github.io"
SITE_BASEURL = "/decision-pga-pages"


CHROME_CANDIDATES = [
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
]


def strip_front_matter(markdown: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", markdown, flags=re.S)


def linkify_urls(escaped: str) -> str:
    return re.sub(
        r"(https?://[^\s<]+)",
        lambda match: f'<a href="{match.group(1)}">{match.group(1)}</a>',
        escaped,
    )


def resolve_link_href(href: str) -> str:
    match = re.fullmatch(r"\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}", href.strip())
    if match:
        return f"{SITE_URL}{SITE_BASEURL}{match.group(1)}"
    return href


def resolve_asset_src(src: str) -> str:
    match = re.fullmatch(r"\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}", src.strip())
    if not match:
        return src

    asset_path = match.group(1).split("?", 1)[0].lstrip("/")
    local_asset = ROOT / asset_path
    if local_asset.exists():
        return local_asset.resolve().as_uri()
    return f"{SITE_URL}{SITE_BASEURL}{match.group(1)}"


def inline_markup(text: str) -> str:
    parts: list[str] = []
    last = 0
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        parts.append(linkify_urls(html.escape(text[last : match.start()])))
        label = html.escape(match.group(1))
        href = html.escape(resolve_link_href(match.group(2)), quote=True)
        parts.append(f'<a href="{href}">{label}</a>')
        last = match.end()
    parts.append(linkify_urls(html.escape(text[last:])))
    escaped = "".join(parts)
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
    block = re.sub(
        r"src=\"([^\"]+)\"",
        lambda match: f'src="{html.escape(resolve_asset_src(match.group(1)), quote=True)}"',
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


def render_html(article_html: str, title: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{html.escape(title)}</title>
    <style>
      @page {{
        size: Letter;
        margin: 0.72in 0.78in 0.78in 0.78in;
      }}

      * {{
        box-sizing: border-box;
      }}

      body {{
        margin: 0;
        color: #172033;
        background: white;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 10pt;
        font-weight: 400;
        line-height: 1.42;
        text-rendering: optimizeLegibility;
      }}

      h1 {{
        margin: 0 0 0.16in;
        color: #111827;
        font-size: 23pt;
        line-height: 1.12;
        letter-spacing: 0;
        max-width: 100%;
        overflow-wrap: normal;
        text-wrap: balance;
      }}

      h2 {{
        margin: 0.28in 0 0.10in;
        color: #111827;
        font-size: 14.7pt;
        line-height: 1.2;
        break-after: avoid;
      }}

      h3 {{
        margin: 0.22in 0 0.07in;
        color: #111827;
        font-size: 11.3pt;
        line-height: 1.22;
        break-after: avoid;
      }}

      p {{
        margin: 0 0 0.105in;
        orphans: 3;
        widows: 3;
      }}

      .article-meta {{
        margin: 0 0 0.25in;
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
        margin: 0 0 0.13in 0.24in;
        padding-left: 0.18in;
      }}

      li {{
        margin: 0 0 0.055in;
        break-inside: avoid;
      }}

      .diagram-figure {{
        margin: 0.14in 0 0.18in;
        break-inside: avoid;
      }}

      .diagram-figure img {{
        display: block;
        width: 100%;
        max-height: 3.2in;
        height: auto;
        object-fit: contain;
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

        h2,
        h3 {{
          break-after: avoid;
        }}

        .diagram-figure,
        .diagram-figure img {{
          break-inside: avoid;
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


def document_title(source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    match = re.search(r"^title:\s*(.+)$", text, flags=re.M)
    if match:
        return match.group(1).strip().strip('"')
    heading = re.search(r"^#\s+(.+)$", strip_front_matter(text), flags=re.M)
    if heading:
        return heading.group(1).strip()
    return source.stem


def build_pdf(source: Path, output: Path) -> None:
    BUILD_DIR.mkdir(exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    html_output = BUILD_DIR / f"{source.stem}-print.html"
    html_text = render_html(markdown_to_html(source.read_text(encoding="utf-8")), document_title(source))
    html_output.write_text(html_text, encoding="utf-8")

    chrome = find_chrome()
    command = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=1000",
        f"--print-to-pdf={output}",
        html_output.resolve().as_uri(),
    ]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode != 0:
        sys.stderr.write(completed.stderr)
        raise SystemExit(completed.returncode)
    print(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a browser-rendered PDF from a site Markdown article.")
    parser.add_argument(
        "source",
        nargs="?",
        default="article.md",
        help="Markdown source file relative to the site root.",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="assets/decision-pga-decision-state-diagnostics.pdf",
        help="PDF output path relative to the site root.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build_pdf((ROOT / args.source).resolve(), (ROOT / args.output).resolve())
