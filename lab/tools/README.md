# 🔧 Tools

**Status:** Directory index, corrected 2026-09-02; the earlier text described utilities that do not exist here.

Validators, build tools, and figures used across the repository.

- Validators that CI runs: `validate_links.py`, `validate_indexes.py` (every directory index covers its directory; a link whose text is a file path points at that file), `validate_nav.py`, `validate_math.py`, `validate_katex.js`, and `audit_repository_freshness.py` (copied counts, benchmark version range, freshness metadata, review candidates).
- Build tools: `build_paper_pdf.py` (the corridor paper PDF) and `mkdocs_repo_links.py` (the MkDocs hook that keeps links working across the repository/site boundary).
- Figures: the `inverse_benchmark_*.png`, `exp*_*.png`, `teo_*.png`, and `viable_corridor.png` images that the benchmark pages and the paper embed; `viable_corridor.py` draws the corridor figure.
- Helpers: `evolutionary_optimizer.py`, `morphospace_visualizer.py`, `migrate_sims.py`, and the `web-explorer/` cellular-automaton page published on the site.

These are not standalone projects. Run them from the repository root, as CI does. The KaTeX check needs a local `npm install katex` first (the installed `node_modules/` is ignored by git).
