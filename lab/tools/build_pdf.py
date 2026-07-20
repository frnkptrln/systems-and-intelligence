"""
build_pdf.py

Compiles the Systems & Intelligence book (book/00 ... book/09) into a single
PDF snapshot at the repository root.

Scope: the book chapters only. The theory, lab, fiction, and log layers live
in the repository and on the docs site; a partial embedding here rotted twice
(a moved theory file was silently skipped, and the fiction folder outgrew a
hard-coded five-story subset), so the PDF now matches its filename: the book.

Math is rendered locally via matplotlib mathtext and embedded as SVG data
URIs. No network is required to build; if an expression exceeds the mathtext
subset, it falls back to typewriter text instead of failing the build.

Usage (any working directory):
    python lab/tools/build_pdf.py
"""

import base64
import datetime
import io
import re
import subprocess
from pathlib import Path

import markdown
import matplotlib

matplotlib.use("Agg")
from matplotlib import mathtext  # noqa: E402  (backend must be set first)
from weasyprint import CSS, HTML  # noqa: E402
from weasyprint.text.fonts import FontConfiguration  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
BOOK_DIR = REPO_ROOT / "book"
OUTPUT = REPO_ROOT / "systems-and-intelligence-book.pdf"

SUBTITLE = (
    "A research notebook on processes, model identification, emergence, and viability"
)


def snapshot_line() -> str:
    """Date + commit of the snapshot, so staleness is visible on the title page."""
    stamp = datetime.date.today().isoformat()
    try:
        sha = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        return f"Snapshot {stamp} · git {sha}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return f"Snapshot {stamp}"


def render_math(expr: str, inline: bool) -> str:
    """Render one LaTeX expression to an embedded SVG; fall back to code text."""
    try:
        buf = io.BytesIO()
        mathtext.math_to_image(f"${expr}$", buf, format="svg", dpi=120)
        data = base64.b64encode(buf.getvalue()).decode("ascii")
        src = f"data:image/svg+xml;base64,{data}"
        if inline:
            return (
                f'<img src="{src}" alt="{expr}" '
                'style="vertical-align: middle; height: 1.05em;" />'
            )
        return (
            '<div style="text-align: center; margin: 1.5em 0;">'
            f'<img src="{src}" alt="{expr}" /></div>'
        )
    except Exception:
        return f"<code>{expr}</code>"


def substitute_math(text: str) -> str:
    text = re.sub(
        r"\$\$(.*?)\$\$",
        lambda m: "\n" + render_math(m.group(1).strip(), inline=False) + "\n",
        text,
        flags=re.DOTALL,
    )
    return re.sub(
        r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)",
        lambda m: render_math(m.group(1).strip(), inline=True),
        text,
    )


def generate_pdf() -> None:
    chapters = sorted(BOOK_DIR.glob("*.md"))
    if not chapters:
        raise SystemExit(f"No book chapters found in {BOOK_DIR}")

    page_break = "\n\n<div style='page-break-after: always;'></div>\n\n"
    full_markdown = (
        "# Systems & Intelligence\n\n"
        f"## {SUBTITLE}\n\n"
        f"*By Frank Peterlein*\n\n*{snapshot_line()}*"
        + page_break
    )

    for chapter in chapters:
        content = chapter.read_text(encoding="utf-8")
        content = content.replace("../../", "").replace("../", "")
        full_markdown += content + page_break

    full_markdown = substitute_math(full_markdown)

    html_body = markdown.markdown(
        full_markdown,
        extensions=["tables", "fenced_code", "footnotes", "nl2br"],
    )

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Systems & Intelligence</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&family=JetBrains+Mono&display=swap');

            @page {{
                size: A4;
                margin: 2.5cm;
                @bottom-center {{
                    content: counter(page);
                    font-family: 'Inter', sans-serif;
                    font-size: 9pt;
                    color: #666;
                }}
            }}

            body {{
                font-family: 'Inter', sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #222;
            }}

            h1, h2, h3, h4 {{
                font-family: 'Outfit', sans-serif;
                color: #111;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}

            h1 {{
                font-size: 24pt;
                font-weight: 700;
                border-bottom: 1px solid #ddd;
                padding-bottom: 0.2em;
                page-break-before: always;
            }}

            /* Special styling for the title page */
            h1:first-of-type {{
                font-size: 32pt;
                text-align: center;
                margin-top: 30%;
                border-bottom: none;
                page-break-before: avoid;
            }}

            h2:first-of-type {{
                text-align: center;
                font-weight: 400;
                color: #555;
            }}

            blockquote {{
                border-left: 4px solid #5e35b1;
                margin: 1.5em 0;
                padding: 0.5em 1em;
                background-color: #f8f9fa;
                font-style: italic;
                color: #444;
            }}

            code {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 9pt;
                background-color: #f1f3f5;
                padding: 0.1em 0.3em;
                border-radius: 3px;
            }}

            pre {{
                background-color: #1e1e1e;
                color: #d4d4d4;
                padding: 1em;
                border-radius: 5px;
                overflow-x: auto;
                page-break-inside: avoid;
            }}

            pre code {{
                background-color: transparent;
                color: inherit;
                padding: 0;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 1.5em 0;
                page-break-inside: avoid;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 8px 12px;
                text-align: left;
            }}

            th {{
                background-color: #f8f9fa;
                font-family: 'Outfit', sans-serif;
            }}

            a {{
                color: #5e35b1;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    print(f"Generating PDF from {len(chapters)} book chapters...")
    font_config = FontConfiguration()
    HTML(string=html_content, base_url=str(REPO_ROOT)).write_pdf(
        str(OUTPUT), font_config=font_config
    )
    print(f"Success! Book exported to {OUTPUT}")


if __name__ == "__main__":
    generate_pdf()
