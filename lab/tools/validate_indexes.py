#!/usr/bin/env python3
"""Index completeness and link-label consistency.

The 2026-09-02 drift sweep found two classes of deterministic drift that the
link validator cannot see: directory indexes that had fallen behind their
directories, and links whose visible text showed a path other than the one
they pointed at. This validator turns both into CI errors.

Rules:

1. Every note in ``ideas/`` (except the index) is linked from ``ideas/README.md``.
2. Every log in ``logs/`` (except the index) is linked from ``logs/README.md``.
3. Every story in ``fiction/`` (except the index) is linked from ``fiction/README.md``.
4. Every ``theory/**/*.md`` (except ``theory/README.md``) is linked from
   ``theory/README.md`` or from a ``README.md`` inside its own ``theory/`` subdirectory.
5. Every ``simulation-models/<group>/<name>/`` directory that has a ``README.md`` is
   named by path in ``theory/core/simulation-theory-map.md`` (the directory's index;
   an entry in its "Not yet mapped" list counts).
6. Every ``lab/benchmarks/<name>/`` and ``lab/experiments/<name>/`` directory that has
   a ``README.md`` is named by path in ``lab/README.md``.
7. A link whose visible text is a code-span file path (``[`theory/x.md`](...)``) points
   at a file whose repository path ends with that text. Directory labels (ending in
   ``/``) are not checked: the entry pages route a directory to its index page.

Usage:
    python lab/tools/validate_indexes.py

Exit status is non-zero when any rule fails. Standard library only.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
CODE_PATH_RE = re.compile(r"^`([^`]+)`$")
FILE_LABEL_RE = re.compile(r"\.(md|py|json|ya?ml|js|txt|css|html)$")
SKIP_DIRS = {".git", "node_modules", "site", "__pycache__", ".pytest_cache", "venv", ".venv"}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.message}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _rel(path: Path, repo: Path) -> str:
    return path.resolve().relative_to(repo.resolve()).as_posix()


def _is_external(href: str) -> bool:
    return href.startswith(("http://", "https://", "mailto:", "#"))


def link_targets(index: Path, repo: Path) -> set[str]:
    """Repository-relative paths of every relative link in ``index``."""
    targets: set[str] = set()
    if not index.exists():
        return targets
    for _, href in LINK_RE.findall(read_text(index)):
        href = href.split("#")[0]
        if not href or _is_external(href):
            continue
        target = (index.parent / href).resolve()
        try:
            targets.add(target.relative_to(repo.resolve()).as_posix())
        except ValueError:
            continue
    return targets


def markdown_files(repo: Path) -> list[Path]:
    out: list[Path] = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.endswith(".md"):
                out.append(Path(root) / name)
    return sorted(out)


def _check_flat_index(repo: Path, folder: str, index_name: str = "README.md") -> list[Finding]:
    """Rules 1-3: every Markdown file in ``folder`` is linked from its index."""
    directory = repo / folder
    index = directory / index_name
    if not directory.is_dir():
        return []
    if not index.exists():
        return [Finding(f"{folder}/{index_name}", 1, "index page is missing")]
    linked = link_targets(index, repo)
    findings = []
    for path in sorted(directory.glob("*.md")):
        if path.name == index_name:
            continue
        rel = _rel(path, repo)
        if rel not in linked:
            findings.append(Finding(rel, 1, f"not linked from {folder}/{index_name}"))
    return findings


def check_theory_index(repo: Path) -> list[Finding]:
    """Rule 4."""
    theory = repo / "theory"
    index = theory / "README.md"
    if not theory.is_dir():
        return []
    if not index.exists():
        return [Finding("theory/README.md", 1, "index page is missing")]
    linked = link_targets(index, repo)
    for sub_index in theory.glob("*/README.md"):
        linked |= link_targets(sub_index, repo)
    findings = []
    for path in sorted(theory.rglob("*.md")):
        if path == index or path.name == "README.md":
            continue
        rel = _rel(path, repo)
        if rel not in linked:
            findings.append(
                Finding(rel, 1, "not linked from theory/README.md or a README.md in its theory subdirectory")
            )
    return findings


def _readme_dirs(base: Path) -> list[Path]:
    if not base.is_dir():
        return []
    return sorted(p.parent for p in base.glob("*/README.md") if p.parent.name not in SKIP_DIRS)


def check_simulation_map(repo: Path) -> list[Finding]:
    """Rule 5."""
    base = repo / "simulation-models"
    index = repo / "theory" / "core" / "simulation-theory-map.md"
    if not base.is_dir():
        return []
    if not index.exists():
        return [Finding("theory/core/simulation-theory-map.md", 1, "simulation map is missing")]
    text = read_text(index)
    findings = []
    for readme in sorted(base.glob("*/*/README.md")):
        mention = readme.parent.relative_to(base).as_posix() + "/"
        if mention not in text:
            findings.append(
                Finding(_rel(readme.parent, repo) + "/", 1, "not named in theory/core/simulation-theory-map.md")
            )
    return findings


def check_lab_index(repo: Path) -> list[Finding]:
    """Rule 6."""
    lab = repo / "lab"
    index = lab / "README.md"
    if not lab.is_dir():
        return []
    if not index.exists():
        return [Finding("lab/README.md", 1, "index page is missing")]
    text = read_text(index)
    findings = []
    for group in ("benchmarks", "experiments"):
        for directory in _readme_dirs(lab / group):
            mention = f"{group}/{directory.name}/"
            if mention not in text:
                findings.append(Finding(_rel(directory, repo) + "/", 1, "not named in lab/README.md"))
    return findings


def check_link_labels(repo: Path) -> list[Finding]:
    """Rule 7."""
    findings = []
    for path in markdown_files(repo):
        rel = _rel(path, repo)
        for number, line in enumerate(read_text(path).splitlines(), start=1):
            for label, href in LINK_RE.findall(line):
                code = CODE_PATH_RE.match(label.strip())
                if not code:
                    continue
                shown = code.group(1).strip()
                if shown.endswith("/") or "/" not in shown and not FILE_LABEL_RE.search(shown):
                    continue
                if not FILE_LABEL_RE.search(shown):
                    continue
                target = href.split("#")[0]
                if not target or _is_external(target):
                    continue
                resolved = (path.parent / target).resolve()
                try:
                    resolved_rel = resolved.relative_to(repo.resolve()).as_posix()
                except ValueError:
                    continue
                if not resolved_rel.endswith(shown.lstrip("./")):
                    findings.append(
                        Finding(rel, number, f"link text `{shown}` does not match its target {resolved_rel}")
                    )
    return findings


def collect_findings(repo: Path = REPO) -> list[Finding]:
    findings: list[Finding] = []
    findings += _check_flat_index(repo, "ideas")
    findings += _check_flat_index(repo, "logs")
    findings += _check_flat_index(repo, "fiction")
    findings += check_theory_index(repo)
    findings += check_simulation_map(repo)
    findings += check_lab_index(repo)
    findings += check_link_labels(repo)
    return findings


def main() -> int:
    findings = collect_findings(REPO)
    if findings:
        print(f"❌ {len(findings)} index or link-label finding(s):")
        for finding in findings:
            print(f"  {finding}")
        return 1
    print("✅ Every index covers its directory and every path-labelled link matches its target.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
