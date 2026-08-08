"""
build_paper_pdf.py

Typesets one paper from ``papers/`` as a standalone PDF.

Why a paper and not the book: the previous builder compiled ``book/00…09``
into a repository-root snapshot that nothing linked to and no workflow
rebuilt, so it drifted from the moment it was written while the book layer
itself stopped moving. A paper is the artifact that actually wants a fixed
form — a bounded document with a frozen claim set, meant to be printed,
cited, and sent to a reviewer. The notebook stays on the web, where it can
keep changing without lying about its own currency.

The PDF is a build artifact, not a committed file: CI rebuilds it before
``mkdocs build`` so the site always serves a copy that matches its source.

Math is rendered locally through matplotlib mathtext and embedded as SVG
data URIs; expressions outside the mathtext subset degrade to typewriter
text rather than failing the build. Fonts are fetched from Google Fonts when
the network allows and fall back to system faces when it does not.

Usage:
    python lab/tools/build_paper_pdf.py                     # viable corridor
    python lab/tools/build_paper_pdf.py papers/other.md
    python lab/tools/build_paper_pdf.py --output /tmp/x.pdf
"""

import argparse
import base64
import datetime
import html
import io
import re
import subprocess
from pathlib import Path

import markdown
import matplotlib
import yaml

matplotlib.use("Agg")
from matplotlib import mathtext  # noqa: E402  (backend must be set first)
from weasyprint import HTML  # noqa: E402
from weasyprint.text.fonts import FontConfiguration  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PAPER = REPO_ROOT / "papers" / "viable-corridor.md"

# Light-mode tokens from docs/stylesheets/extra.css, so a printed paper and
# the site it came from are recognisably the same object.
INK = "#17190f"
INK_SOFT = "#3d4036"
INK_DIM = "#767a6d"
LINE = "#dedbd0"
ACCENT = "#4a7016"


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
                f'<img src="{src}" alt="{html.escape(expr)}" '
                'style="vertical-align: middle; height: 1.05em;" />'
            )
        return (
            '<div class="math-display">'
            f'<img src="{src}" alt="{html.escape(expr)}" /></div>'
        )
    except Exception:
        return f"<code>{html.escape(expr)}</code>"


FENCE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)


def substitute_math(text: str) -> str:
    """Replace ``$…$`` and ``$$…$$`` outside fenced code with rendered SVG."""
    protected: list[str] = []

    def stash(match: re.Match) -> str:
        protected.append(match.group(0))
        return f"\x00FENCE{len(protected) - 1}\x00"

    text = FENCE.sub(stash, text)
    text = re.sub(
        r"\$\$(.*?)\$\$",
        lambda m: "\n" + render_math(m.group(1).strip(), inline=False) + "\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)",
        lambda m: render_math(m.group(1).strip(), inline=True),
        text,
    )
    for index, block in enumerate(protected):
        text = text.replace(f"\x00FENCE{index}\x00", block)
    return text


def split_front_matter(source: str) -> tuple[dict, str]:
    """Peel the YAML front matter off a paper, returning (metadata, body)."""
    if not source.startswith("---\n"):
        return {}, source
    end = source.find("\n---", 4)
    if end == -1:
        return {}, source
    meta = yaml.safe_load(source[4:end]) or {}
    body = source[end + len("\n---"):].lstrip("\n")
    return (meta if isinstance(meta, dict) else {}), body


def title_page(meta: dict) -> str:
    """Build the cover from the paper's own front matter."""
    def field(name: str) -> str:
        value = meta.get(name)
        return html.escape(str(value).strip()) if value else ""

    byline = " · ".join(part for part in (field("author"), field("affiliation")) if part)
    version = field("version")
    date = field("date")
    stamp = " · ".join(
        part for part in (f"Version {version}" if version else "", date) if part
    )

    parts = [
        '<div class="cover">',
        f'<p class="cover-eyebrow">Systems &amp; Intelligence · Paper</p>',
        f'<h1 class="cover-title">{field("title") or "Untitled"}</h1>',
    ]
    if byline:
        parts.append(f'<p class="cover-byline">{byline}</p>')
    if stamp:
        parts.append(f'<p class="cover-meta">{stamp}</p>')
    if meta.get("status"):
        parts.append(f'<p class="cover-status">{field("status")}</p>')
    parts.append(f'<p class="cover-meta">{html.escape(snapshot_line())}</p>')
    parts.append(
        '<p class="cover-source">Source and revision history: '
        "github.com/frnkptrln/systems-and-intelligence</p>"
    )
    parts.append("</div>")
    return "\n".join(parts)


STYLESHEET = f"""
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600&family=JetBrains+Mono:wght@400&display=swap');

@page {{
    size: A4;
    margin: 2.4cm 2.2cm 2.2cm;
    @bottom-center {{
        content: counter(page);
        font-family: 'JetBrains Mono', monospace;
        font-size: 8pt;
        color: {INK_DIM};
    }}
}}

@page :first {{
    @bottom-center {{ content: ""; }}
}}

body {{
    color: {INK_SOFT};
    font-family: 'Space Grotesk', system-ui, sans-serif;
    font-size: 10.2pt;
    font-weight: 300;
    line-height: 1.55;
    hyphens: auto;
}}

h1, h2, h3, h4 {{
    color: {INK};
    font-weight: 400;
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin: 1.6em 0 0.6em;
    page-break-after: avoid;
}}

h1 {{ font-size: 17pt; }}
h2 {{
    border-top: 0.5pt solid {LINE};
    font-size: 13pt;
    margin-top: 2em;
    padding-top: 0.7em;
}}
h3 {{ font-size: 11pt; font-weight: 500; }}
h4 {{ font-size: 10pt; font-weight: 500; }}

p {{ margin: 0 0 0.8em; }}
strong {{ color: {INK}; font-weight: 500; }}

a {{ color: {ACCENT}; text-decoration: none; }}

.cover {{
    page-break-after: always;
    padding-top: 5.5cm;
}}

.cover-eyebrow {{
    color: {INK_DIM};
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
    letter-spacing: 0.12em;
    margin-bottom: 2.6em;
    text-transform: uppercase;
}}

.cover-title {{
    font-size: 25pt;
    font-weight: 300;
    letter-spacing: -0.035em;
    line-height: 1.12;
    margin: 0 0 1.1em;
}}

.cover-byline {{ color: {INK}; font-size: 11pt; margin-bottom: 0.3em; }}

.cover-meta, .cover-status, .cover-source {{
    color: {INK_DIM};
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
    line-height: 1.6;
    margin-bottom: 0.4em;
}}

.cover-status {{
    border-left: 1.5pt solid {ACCENT};
    margin-top: 2.4em;
    padding-left: 0.9em;
}}

.cover-source {{ margin-top: 2.4em; }}

blockquote {{
    border-left: 1.5pt solid {LINE};
    color: {INK_DIM};
    margin: 1.2em 0;
    padding-left: 1em;
}}

code {{
    background-color: #f1efe6;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.4pt;
    padding: 0.1em 0.3em;
}}

pre {{
    background-color: #f6f5ee;
    border: 0.5pt solid {LINE};
    font-size: 8.2pt;
    padding: 0.9em;
    page-break-inside: avoid;
    white-space: pre-wrap;
    word-wrap: break-word;
}}

pre code {{ background-color: transparent; padding: 0; }}

table {{
    border-collapse: collapse;
    font-size: 8.6pt;
    margin: 1.4em 0;
    page-break-inside: avoid;
    width: 100%;
}}

th, td {{
    border-bottom: 0.5pt solid {LINE};
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
}}

th {{
    border-bottom-width: 1pt;
    color: {INK_DIM};
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.6pt;
    font-weight: 400;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}}

hr {{ border: none; border-top: 0.5pt solid {LINE}; margin: 2em 0; }}

.math-display {{
    margin: 1.3em 0;
    page-break-inside: avoid;
    text-align: center;
}}

img {{ max-width: 100%; }}

.footnote {{ border-top: 0.5pt solid {LINE}; font-size: 8.6pt; margin-top: 2.5em; }}
"""


def build(paper: Path, output: Path) -> None:
    meta, body = split_front_matter(paper.read_text(encoding="utf-8"))

    # Repository-relative links have no meaning in a detached PDF.
    body = body.replace("../../", "").replace("../", "")
    body = substitute_math(body)

    html_body = markdown.markdown(
        body,
        extensions=["tables", "fenced_code", "footnotes", "attr_list"],
    )

    document = (
        "<!DOCTYPE html>\n"
        '<html lang="en"><head><meta charset="UTF-8">'
        f"<title>{html.escape(str(meta.get('title', paper.stem)))}</title>"
        f"<style>{STYLESHEET}</style></head><body>"
        f"{title_page(meta)}{html_body}"
        "</body></html>"
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=document, base_url=str(REPO_ROOT)).write_pdf(
        str(output), font_config=FontConfiguration()
    )
    size_kb = output.stat().st_size / 1024
    print(f"Wrote {output.relative_to(REPO_ROOT)} ({size_kb:.0f} KB) from {paper.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paper", nargs="?", default=str(DEFAULT_PAPER),
        help="Markdown paper to typeset (default: papers/viable-corridor.md)",
    )
    parser.add_argument(
        "--output", help="Destination PDF (default: alongside the source paper)",
    )
    args = parser.parse_args()

    paper = Path(args.paper)
    if not paper.is_absolute():
        paper = REPO_ROOT / paper
    if not paper.is_file():
        raise SystemExit(f"No such paper: {paper}")

    output = Path(args.output) if args.output else paper.with_suffix(".pdf")
    if not output.is_absolute():
        output = REPO_ROOT / output

    build(paper, output)


if __name__ == "__main__":
    main()
