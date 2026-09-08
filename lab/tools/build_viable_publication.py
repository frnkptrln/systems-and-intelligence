#!/usr/bin/env python3
"""Build a review copy from the erratum-bearing source; no submission or upload.

Run from the repository root. Requires the repository scientific Python stack,
pandoc and xelatex. All simulations retain their original defaults and seeds.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import re
import shutil
import subprocess
import sys
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


def manuscript(output: Path) -> dict:
    source = PAPER.read_text(encoding="utf-8")
    metadata = yaml.safe_load(source.split("---", 2)[1])
    # Keep scientific sections, appendices and references verbatim. The website
    # entrance, drafting history and post-v1.0 task list remain in the source.
    body = source[source.index("## Abstract"):source.index("## TODO (post-v1.0)")].strip()
    body = body.replace("../lab/tools/", "figures/")
    body = body.replace("✓", "yes").replace("✗", "no")
    body = body.replace("The figure's own annotation predates the erratum and names only the $\\gamma > \\gamma_c$ strengthening.", 'The regenerated figure annotation includes both the regulation and coherence-floor corrections.')
    body = re.sub(r"(figures/[^)]+)\.png\)", r"\1.pdf)", body)
    # Resolve repository prose links; local image paths remain build inputs.
    def link(match):
        label, target = match.groups()
        path, sep, anchor = target.partition("#")
        absolute = (PAPER.parent / path).resolve()
        rel = absolute.relative_to(ROOT)
        return f"[{label}](https://github.com/frnkptrln/systems-and-intelligence/blob/main/{rel}{sep}{anchor})"
    body = re.sub(r"(?<!!)\[([^\]]+)\]\((\.\.?/[^)]+)\)", link, body)
    notice = (
        "**Review copy: v1.0 with the 7 September 2026 erratum.** "
        "The Lorentzian continuum sufficiency conjunction is refuted; a corrected, "
        "floor-dependent statement remains open. Historical v1.0 measurements are retained. "
        "External scientific reviews and publication approval remain outstanding.\n\n"
    )
    front = {"title": metadata["title"], "author": metadata["author"],
             "date": "8 September 2026 — erratum-bearing review copy",
             "documentclass": "article", "fontsize": "11pt",
             "geometry": "margin=25mm", "linestretch": 2,
             "colorlinks": True, "mainfont": "DejaVu Serif",
             "header-includes": [r"\usepackage{xurl}"]}
    md = "---\n" + yaml.safe_dump(front, allow_unicode=True) + "---\n\n"
    md += metadata["affiliation"] + "  \nCorrespondence: frank.peterlein@gmail.com\n\n" + notice + body + "\n"
    (output / "manuscript.md").write_text(md, encoding="utf-8")
    subprocess.run(["pandoc", "manuscript.md", "--standalone", "--from=markdown-implicit_figures",
                    "--to=latex", "--output=manuscript.tex"], cwd=output, check=True)
    tex = (output / "manuscript.tex").read_text()
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
    (output / "manuscript.tex").write_text(tex)
    # Compile the generated TeX directly. Parsing it back through pandoc would
    # discard its font/spacing preamble and can silently drop Unicode symbols.
    for _ in range(2):
        subprocess.run(["xelatex", "-halt-on-error", "-interaction=nonstopmode", "manuscript.tex"],
                       cwd=output, check=True, stdout=subprocess.DEVNULL)
    log = (output / "manuscript.log").read_text()
    if "Missing character:" in log or "Overfull \\hbox" in log:
        raise ValueError("Typesetting needs review: missing glyph or overfull line")
    for suffix in ("aux", "log", "out"):
        (output / f"manuscript.{suffix}").unlink(missing_ok=True)
    return {"source_sha256": sha(PAPER),
            "conversion": "scientific sections Abstract through References retained; website header, revision history and TODO excluded; figure/link paths resolved; check/cross marks rendered yes/no, production-only Figure 1 annotation sentence refreshed, long equations reflowed and paths made breakable",
            "word_count_whitespace_main_including_abstract": len(body.split("## Appendices")[0].split()),
            "format": "single-column 11pt LaTeX article, double-spaced, 25 mm margins; author-date references retained, APA audit pending"}


def manifest(output: Path, manuscript_info: dict) -> None:
    sources = ["papers/viable-corridor.md", "lab/tools/viable_corridor.py", TEO, ABM,
               "lab/tools/build_viable_publication.py", "requirements.txt", "requirements-docs.txt",
               "tests/test_corridor_headlines.py", "tests/test_coherence_margin.py",
               "lab/experiments/coherence_margin/coherence_margin.py",
               "lab/experiments/coherence_margin/results/results.json"]
    record = {"status": "review_package_not_submitted", "paper_version": "1.0 with erratum 2026-09-07",
              "repository_base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "source_identity": "base commit plus exact current source hashes; base commit alone does not identify working-tree changes",
              "manuscript": manuscript_info,
              "sources_sha256": {p: sha(ROOT / p) for p in sources},
              "artifacts_sha256": {str(p.relative_to(output)): sha(p) for p in sorted(output.rglob("*"))
                                   if p.is_file() and p.name != "manifest.json"},
              "seeds": {"teo": {"omega": 7, "initial_conditions": 8}, "agent_ecology": {"first": 0, "count_per_point": 200}, "schematic": "deterministic, not a simulation"},
              "runtime": {"python": platform.python_version(), "numpy": numpy.__version__,
                          "scipy": scipy.__version__, "matplotlib": matplotlib.__version__,
                          "pandoc": subprocess.check_output(["pandoc", "--version"], text=True).splitlines()[0],
                          "xelatex": subprocess.check_output(["xelatex", "--version"], text=True).splitlines()[0]},
              "remaining_gates": ["independent dynamical-systems, alignment/framing and coupled-systems/substrate reviews",
                                  "complete APA 7 author-list/DOI/report-series audit and venue positioning",
                                  "author publication approval; no submission or deployment performed"],
              "live_pdf": {"url": "https://frnkptrln.github.io/systems-and-intelligence/papers/viable-corridor.pdf",
                           "identity": "not claimed identical to this review copy; live deployment was not performed"}}
    (output / "manifest.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reuse-figures", action="store_true", help="reuse an already generated figure directory")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if not args.reuse_figures:
        figures(output / "figures")
    else:
        prior = json.loads((output / "manifest.json").read_text())
        for source in ("lab/tools/viable_corridor.py", TEO, ABM):
            if prior["sources_sha256"][source] != sha(ROOT / source):
                raise ValueError(f"Figure source changed; regenerate figures: {source}")
        for name, digest in prior["artifacts_sha256"].items():
            if name.startswith("figures/") and sha(output / name) != digest:
                raise ValueError(f"Cached figure changed: {name}")
    for stem in ("viable_corridor", "teo_p1_necessity", "teo_p2_gamma_c", "teo_p3_corridor", "teo_p8_capability", "teo_p7p8_agent_ecology"):
        for ext in ("png", "pdf"):
            if not (output / "figures" / f"{stem}.{ext}").is_file():
                raise ValueError(f"Missing canonical figure: {stem}.{ext}")
    for source in (ROOT / "papers/viable-corridor-publication").glob("*.txt"):
        shutil.copyfile(source, output / source.name)
    manifest(output, manuscript(output))
    print(f"Review package: {output}")


if __name__ == "__main__":
    main()
