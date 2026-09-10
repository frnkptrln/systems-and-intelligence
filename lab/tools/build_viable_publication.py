#!/usr/bin/env python3
"""Build a review copy from the erratum-bearing source; no submission or upload.

Run from the repository root. Requires the repository scientific Python stack,
pandoc and xelatex (or tectonic). All simulations retain their original defaults
and seeds. Dependencies are checked before the expensive figure calculations.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.util
import json
import platform
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import numpy
import scipy
import yaml

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "papers/viable-corridor.md"
TEO = "simulation-models/alignment-and-veto/teo-civilization/teo_simulation.py"
ABM = "simulation-models/alignment-and-veto/agent-ecology/agent_budget_sim.py"
FIGURE_SOURCES = ("lab/tools/viable_corridor.py", TEO, ABM)
FIGURE_NAMES = tuple(f"figures/{stem}.{ext}" for stem in (
    "viable_corridor", "teo_p1_necessity", "teo_p2_gamma_c", "teo_p3_corridor",
    "teo_p8_capability", "teo_p7p8_agent_ecology") for ext in ("png", "pdf"))


def validate_figure_cache(output: Path) -> None:
    """Require every canonical artifact to be covered by the prior manifest."""
    prior = json.loads((output / "manifest.json").read_text())
    for source in FIGURE_SOURCES:
        if prior["sources_sha256"].get(source) != sha(ROOT / source):
            raise ValueError(f"Figure source changed; regenerate figures: {source}")
    for name in FIGURE_NAMES:
        if not (output / name).is_file():
            raise ValueError(f"Missing canonical figure: {name}")
        if prior["artifacts_sha256"].get(name) != sha(output / name):
            raise ValueError(f"Cached figure changed or is unrecorded: {name}")


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def figures(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    schematic = load("publication_schematic", "lab/tools/viable_corridor.py")
    schematic.plot_viable_corridor(output / "viable_corridor.png", dpi=600)
    schematic.plot_viable_corridor(output / "viable_corridor.pdf")
    teo = load("publication_teo", TEO)
    for name in ("figure_p1", "figure_p2_gamma_sweep", "figure_p3_corridor", "figure_p8_capability"):
        print(name, flush=True)
        getattr(teo, name)(output, dpi=600, vector=True)
    print("figure_p7p8 (200 seeds per point)", flush=True)
    load("publication_abm", ABM).figure_p7p8(output, n_seeds=200, dpi=600, vector=True)


def article_body(body: str) -> str:
    edits = json.loads((ROOT / "papers/viable-corridor-publication/article-edits.json").read_text())
    for edit in edits["edits"]:
        if body.count(edit["old"]) != 1:
            raise ValueError(f"Article edit no longer matches exactly once: {edit['old'][:90]}")
        body = body.replace(edit["old"], edit["new"], 1)
    return re.sub(r"\n{3,}", "\n\n", body)


def visible_figure_captions(body: str) -> str:
    """Keep manuscript captions visible when implicit figure numbering is off.

    Pandoc otherwise treats the entire Markdown image description as alt text,
    so critical scope and numerical qualifications disappear from printed PDFs.
    Explicit prose also preserves the source's Figure 1/C1-C4/D1 numbering.
    """
    def figure(match):
        caption, target = match.groups()
        label = re.search(r"Figure\s+(?:[A-D])?\d+", caption)
        if not label:
            raise ValueError(f"Missing figure label: {caption[:80]}")
        return f"![{label[0]}]({target})\n\n{caption}"
    return re.sub(r"!\[(.*?)\]\((figures/[^)]+)\)", figure, body, flags=re.DOTALL)


def reference_paragraphs(body: str) -> str:
    """Use hanging-indent references in the export, preserving each entry."""
    before, marker, references = body.partition("## References\n\n")
    if not marker:
        raise ValueError("Missing References section")
    note, marker, entries = references.partition("\n\n- ")
    if not marker:
        raise ValueError("Missing reference entries")
    entries = "- " + entries
    paragraphs = re.sub(r"(?m)^- ", "", entries).strip()
    return (before + "## References\n\n" + note + "\n\n"
            + r"\begingroup\setlength{\parindent}{-1.5em}\setlength{\leftskip}{1.5em}"
            + "\n\n" + paragraphs + "\n\n" + r"\endgroup" + "\n")


def manuscript(output: Path, engine: str = "xelatex", *, edition: str = "manuscript") -> dict:
    source = PAPER.read_text(encoding="utf-8")
    metadata = yaml.safe_load(source.split("---", 2)[1])
    source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    # Keep scientific sections, appendices and references verbatim. The website
    # entrance, drafting history and post-v1.0 task list remain in the source.
    body = source[source.index("## Abstract"):source.index("## TODO (post-v1.0)")].strip()
    if edition == "article":
        body = article_body(body)
        body = body[:body.index("## Appendices")] + body[body.index("## References"):]
    elif edition == "supplementary-material":
        body = "## Supplementary Material\n\n" + body[body.index("## Appendices"):]
    body = body.replace("../lab/tools/", "figures/")
    body = body.replace("✓", "yes").replace("✗", "no")
    body = body.replace("revision v0.5 in the log above", "revision v0.5 in the repository revision history")
    body = re.sub(r"(figures/[^)]+)\.png\)", r"\1.pdf)", body)
    body = visible_figure_captions(body)
    body = reference_paragraphs(body)
    # Resolve repository prose links; local image paths remain build inputs.
    def link(match):
        label, target = match.groups()
        path, sep, anchor = target.partition("#")
        absolute = (PAPER.parent / path).resolve()
        rel = absolute.relative_to(ROOT)
        return f"[{label}](https://github.com/frnkptrln/systems-and-intelligence/blob/{source_commit}/{rel}{sep}{anchor})"
    body = re.sub(r"(?<!!)\[([^\]]+)\]\((\.\.?/[^)]+)\)", link, body)
    notice = (
        "**Review copy: v1.0 with the 7 September 2026 erratum.** "
        "The Lorentzian continuum sufficiency conjunction is refuted. "
        "External scientific reviews remain outstanding.\n\n"
    )
    front = {"title": metadata["title"], "author": metadata["author"],
             "date": f"{datetime.date.today().isoformat()} - erratum-bearing review copy",
             "documentclass": "article", "fontsize": "11pt",
             "papersize": "a4", "geometry": "margin=25mm", "linestretch": 2,
             "colorlinks": True, "mainfont": "DejaVu Serif",
             "header-includes": [r"\usepackage{xurl}"]}
    if edition == "supplementary-material":
        front["title"] = "Supplementary Material: " + metadata["title"]
    md = "---\n" + yaml.safe_dump(front, allow_unicode=True) + "---\n\n"
    correspondence = metadata["correspondence"].split(" (", 1)[0]
    body = body.replace("## §1. Introduction", "\\clearpage\n\n## §1. Introduction", 1)
    if edition == "article":
        body = body.replace("## §1. Introduction", "## §1. Introduction\n\n" + notice + "Appendices A–D and Figures C1–C4/D1 are supplied in the accompanying Supplementary Material.", 1)
        body = body.replace("\n---\n\n\\clearpage", "\n\\clearpage", 1)
    # The full review keeps the original abstract; the Article uses the
    # explicit, checked shortening map and retains all six keywords.
    if edition == "article":
        md += metadata["affiliation"] + f"; correspondence: {correspondence}\n\n" + body + "\n"
    else:
        md += metadata["affiliation"] + f"  \nCorrespondence: {correspondence}\n\n" + notice + body + "\n"
    (output / f"{edition}.md").write_text(md, encoding="utf-8")
    subprocess.run(["pandoc", f"{edition}.md", "--standalone", "--from=markdown-implicit_figures+autolink_bare_uris",
                    "--to=latex", f"--output={edition}.tex"], cwd=output, check=True)
    tex = (output / f"{edition}.tex").read_text()
    if edition == "article":
        # A compact, double-spaced cover keeps the shortened abstract and six
        # keywords on page one, with the main text starting on page two.
        title_layout = (r"\makeatletter\renewcommand{\maketitle}{\begin{center}"
                        r"{\bfseries\@title\par}\@author\par\@date\end{center}}"
                        r"\makeatother" + "\n")
        tex = tex.replace(r"\begin{document}", title_layout + r"\begin{document}")
    tex = re.sub(r"\\texttt\{([^{}]*[\/][^{}]*)\}",
                 lambda m: r"\path{" + m[1].replace(r"\_", "_") + "}", tex)
    tex = tex.replace(
        r"\qquad\text{equivalently}\qquad",
        r"\\ \text{equivalently}\quad &")
    # Three long displays need line breaks, not a smaller mathematical font.
    tex = re.sub(r"\\\[\s*(H\(t\) = [\s\S]*?\\text\{\(6b\)\})\s*\\\]",
                 lambda m: "\\[\\begin{aligned}\n&" + m[1] + "\n\\end{aligned}\\]", tex)
    tex = tex.replace(
        r"\mathcal{C} = \left\lbrace(\gamma, K, D_{\max}) : (\gamma, K, D_{\max}, S_{\max}) \text{ admits robust viability as defined in Section 3.1}\right\rbrace. \qquad \text{(7)}",
        r"\begin{aligned}\mathcal{C} = \{(\gamma, K, D_{\max}) :\;& (\gamma, K, D_{\max}, S_{\max})\text{ admits robust viability}\\ &\text{as defined in Section 3.1}\}.\qquad\text{(7)}\end{aligned}")
    tex = tex.replace(
        r"\gamma > 0 \ \text{(finite-$N$, Lemma 1)}, \quad K > K_c \ \text{($N \to \infty$, Lemma 2)}, \quad \Omega(t) < S_{\max} \ \forall t \ \text{(finite-$N$, Lemma 3)}. \qquad \text{(8)}",
        r"\begin{aligned}\gamma &> 0 &&\text{(finite-$N$, Lemma 1)},\\ K &> K_c &&\text{($N \to \infty$, Lemma 2)},\\ \Omega(t) &< S_{\max}\ \forall t &&\text{(finite-$N$, Lemma 3)}.\qquad\text{(8)}\end{aligned}")
    (output / f"{edition}.tex").write_text(tex)
    # Compile the generated TeX directly. Parsing it back through pandoc would
    # discard its font/spacing preamble and can silently drop Unicode symbols.
    if engine == "tectonic":
        result = subprocess.run([engine, "--keep-logs", f"{edition}.tex"], cwd=output,
                                capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(f"TeX compilation failed; inspect {output / (edition + '.log')}\n{result.stderr[-1600:]}")
    else:
        for _ in range(2):
            subprocess.run([engine, "-halt-on-error", "-interaction=nonstopmode", f"{edition}.tex"],
                           cwd=output, check=True, stdout=subprocess.DEVNULL)
    log = (output / f"{edition}.log").read_text()
    if "Missing character:" in log or "Overfull \\hbox" in log:
        raise ValueError("Typesetting needs review: missing glyph or overfull line")
    for suffix in ("aux", "log", "out"):
        (output / f"{edition}.{suffix}").unlink(missing_ok=True)
    main = body.split("## Appendices")[0].split("## References")[0]
    plain = subprocess.check_output(["pandoc", "--from=markdown", "--to=plain"], input=main, text=True, stderr=subprocess.DEVNULL)
    all_plain = subprocess.check_output(["pandoc", "--from=markdown", "--to=plain"], input=body, text=True, stderr=subprocess.DEVNULL)
    content_scope = {
        "manuscript": "complete canonical scientific sections Abstract through References, with appendices",
        "article": "shortened abstract and framing/discussion via article-edits.json; original model definitions, displays, lemmas, erratum, predictions and limitations; references retained; appendices supplied separately",
        "supplementary-material": "original Appendices A-D and references; no abstract or main-text sections",
    }[edition]
    info = {"source_sha256": sha(PAPER), "title": front["title"], "repository_link_commit": source_commit,
            "edition": edition,
            "conversion": content_scope + "; website header, revision history and TODO excluded; figure captions rendered as visible prose with original numbering; reference bullets rendered as hanging-indent paragraphs; figure/link paths resolved; check/cross marks rendered yes/no; long equations reflowed and paths made breakable; revision-log reference made explicit",
            "word_count_whitespace_main_including_abstract": len(main.split()),
            "word_count_pandoc_plain_main_including_abstract": len(plain.split()),
            "word_count_pandoc_plain_complete_body": len(all_plain.split()),
            "complete_body_count_scope": "All exported body text, including references and editorial notices; excludes title/author cover details; mathematics retained as text by pandoc",
            "word_count_scope": "Abstract, keywords and sections 1-8; includes headings, captions, tables and mathematical text; excludes appendices and references; not a journal-certified count",
            "format": "single-column A4 11pt LaTeX article, double-spaced, 25 mm margins; review copy, not certified as venue-ready",
            "engine": engine}
    if edition == "supplementary-material":
        info.pop("word_count_whitespace_main_including_abstract")
        info.pop("word_count_pandoc_plain_main_including_abstract")
        info["word_count_scope"] = "Complete Supplementary Material: headings, Appendices A-D, captions, mathematical text and references; excludes cover details"
    return info


def manifest(output: Path, manuscript_info: dict, article_info: dict, supplement_info: dict) -> None:
    sources = ["papers/viable-corridor.md", "lab/tools/viable_corridor.py", TEO, ABM,
               "simulation-models/alignment-and-veto/teo-civilization/separability_grid.py",
               "lab/tools/build_viable_publication.py", "requirements.txt", "requirements-docs.txt",
               "papers/viable-corridor-publication/article-edits.json",
               "tests/test_corridor_headlines.py", "tests/test_coherence_margin.py",
               "tests/test_viable_publication.py",
               "lab/tools/build_paper_pdf.py", "tests/test_site_paper_captions.py",
               "lab/experiments/coherence_margin/coherence_margin.py",
               "lab/experiments/coherence_margin/results/results.json"]
    sources += [str(p.relative_to(ROOT)) for p in sorted((ROOT / "papers/viable-corridor-publication").glob("*.txt"))]
    artifacts = [f"{stem}.{ext}" for stem in ("manuscript", "article", "supplementary-material") for ext in ("md", "tex", "pdf")]
    artifacts += list(FIGURE_NAMES)
    artifacts += ["article-edits.json"]
    artifacts += [p.name for p in sorted((ROOT / "papers/viable-corridor-publication").glob("*.txt"))]
    record = {"status": "review_package_not_submitted", "paper_version": "1.0 with erratum 2026-09-07",
              "repository_base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "source_identity": "base commit plus exact current source hashes; base commit alone does not identify working-tree changes",
              "manuscript": manuscript_info,
              "article": article_info,
              "supplementary_material": supplement_info,
              "sources_sha256": {p: sha(ROOT / p) for p in sources},
              "generated_on": datetime.date.today().isoformat(),
              "artifacts_sha256": {name: sha(output / name) for name in artifacts},
              "seeds": {"teo": {"omega": 7, "initial_conditions": 8}, "agent_ecology": {"first": 0, "count_per_point": 200}, "schematic": "deterministic, not a simulation"},
              "runtime": {"python": platform.python_version(), "numpy": numpy.__version__,
                          "scipy": scipy.__version__, "matplotlib": matplotlib.__version__,
                          "pandoc": subprocess.check_output(["pandoc", "--version"], text=True).splitlines()[0],
                          "tex_engine": subprocess.check_output([manuscript_info["engine"], "--version"], text=True).splitlines()[0]},
              "remaining_gates": ["independent dynamical-systems, alignment/framing and coupled-systems/substrate reviews",
                                  "author review of shortened Article and declarations; accepted-stage BibTeX/publication forms if requested by venue",
                                  "author publication approval; no submission or deployment performed"],
              "live_pdf": {"url": "https://frnkptrln.github.io/systems-and-intelligence/papers/viable-corridor.pdf",
                           "identity": "not claimed identical to this review copy; live deployment was not performed"}}
    (output / "manifest.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    with zipfile.ZipFile(output / "review-package.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for name in ["manifest.json", *artifacts]:
            archive.write(output / name, name)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reuse-figures", action="store_true", help="reuse an already generated figure directory")
    parser.add_argument("--engine", choices=("xelatex", "tectonic"), default="xelatex")
    args = parser.parse_args()
    for command in ("pandoc", args.engine):
        if not shutil.which(command):
            parser.error(f"Required program is unavailable: {command}. Install it before generating figures.")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if not args.reuse_figures:
        figures(output / "figures")
    else:
        validate_figure_cache(output)
    for name in FIGURE_NAMES:
        if not (output / name).is_file():
            raise ValueError(f"Missing canonical figure: {name}")
    for source in (ROOT / "papers/viable-corridor-publication").glob("*.txt"):
        shutil.copyfile(source, output / source.name)
    shutil.copyfile(ROOT / "papers/viable-corridor-publication/article-edits.json", output / "article-edits.json")
    manuscript_info = manuscript(output, args.engine)
    article_info = manuscript(output, args.engine, edition="article")
    supplement_info = manuscript(output, args.engine, edition="supplementary-material")
    manifest(output, manuscript_info, article_info, supplement_info)
    print(f"Review package: {output}")


if __name__ == "__main__":
    main()
