#!/usr/bin/env python3
"""Audit repository text for stale derived state and freshness review candidates.

This tool deliberately separates two classes of maintenance:

1. **Deterministic internal drift** can be checked in CI. Example: a reader page
   says the repository has 13 open problems while the canonical registry has 19.
2. **External freshness** cannot be inferred from repository text alone. The tool
   only surfaces review candidates such as relative recency language or current
   vendor/model claims; a human or research agent must check primary sources.

Usage:
    python lab/tools/audit_repository_freshness.py
    python lab/tools/audit_repository_freshness.py --strict

``--strict`` exits non-zero for deterministic errors. Review candidates remain
warnings because CI cannot know whether an external claim is still true.
"""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SKIP_DIRS = {
    ".git",
    ".venv",
    "site",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".gemini",
}

OPEN_PROBLEMS_PATH = Path("theory/reference/open-problems.md")
OPEN_PROBLEM_HEADING = re.compile(r"^## Open Problem\s+(\d+):", re.MULTILINE)

# These patterns are intentionally narrow. We only fail when prose explicitly
# claims a copied count for the canonical open-problem registry.
OPEN_PROBLEM_COUNT_PATTERNS = (
    re.compile(r"\b(?:maintains|contains|tracks|lists)\s+\[(\d+)\s+open problems\]", re.I),
    re.compile(r"\b(?:maintains|contains|tracks|lists)\s+(\d+)\s+open problems\b", re.I),
)

RELATIVE_RECENCY = re.compile(
    r"\b(today|currently|recently|weeks? old|the latest|latest work|state of the art)\b",
    re.I,
)

# Dated exploratory/history lanes may use relative language without pretending
# to describe the present. They are not part of the warning scan.
RELATIVE_TIME_EXCLUDED_PREFIXES = (
    "fiction/",
    "ideas/",
    "logs/",
)
RELATIVE_TIME_EXCLUDED_FILES = {
    "meta/repository-meta/freshness-and-review.md",
}

# Files whose argument materially depends on a changing external interface or
# research snapshot. Add to this set deliberately; do not try to infer the list
# from filenames.
FRESHNESS_MANAGED = {
    "lab/providers/README.md",
    "theory/ai/j-space-and-global-availability.md",
    "theory/narrative/asimov-ai-latent-thinking.md",
}

LAST_REVIEWED = re.compile(
    r"(?:"
    r"(?:\*\*)?Last reviewed(?:\*\*)?:\s*\d{4}-\d{2}-\d{2}"
    r"|^last_reviewed:\s*\d{4}-\d{2}-\d{2}\s*$"
    r")",
    re.I | re.MULTILINE,
)
EXTERNAL_LAST_REVIEWED = re.compile(
    r"(?:\*\*)?External interface last reviewed(?:\*\*)?:\s*\d{4}-\d{2}-\d{2}",
    re.I,
)
REVIEW_TRIGGER = re.compile(
    r"(?:"
    r"(?:\*\*)?Review trigger(?:\*\*)?:"
    r"|^review_trigger:\s*\S.+$"
    r")",
    re.I | re.MULTILINE,
)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    message: str


def markdown_files(repo: Path = REPO) -> list[Path]:
    files: list[Path] = []
    for root, dirs, names in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in names:
            if name.endswith(".md"):
                files.append(Path(root) / name)
    return sorted(files)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def canonical_open_problem_count(repo: Path = REPO) -> int:
    path = repo / OPEN_PROBLEMS_PATH
    matches = [int(n) for n in OPEN_PROBLEM_HEADING.findall(read_text(path))]
    if not matches:
        raise ValueError(f"No open-problem headings found in {OPEN_PROBLEMS_PATH}")
    if len(matches) != len(set(matches)):
        raise ValueError("Duplicate open-problem numbers in canonical registry")
    return len(matches)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def find_copied_count_errors(repo: Path = REPO) -> list[Finding]:
    canonical = canonical_open_problem_count(repo)
    findings: list[Finding] = []
    for path in markdown_files(repo):
        rel = path.relative_to(repo).as_posix()
        if Path(rel) == OPEN_PROBLEMS_PATH:
            continue
        text = read_text(path)
        for pattern in OPEN_PROBLEM_COUNT_PATTERNS:
            for match in pattern.finditer(text):
                copied = int(match.group(1))
                if copied != canonical:
                    findings.append(
                        Finding(
                            rel,
                            line_number(text, match.start()),
                            f"copied open-problem count is {copied}; canonical registry has {canonical}",
                        )
                    )
    return findings


def find_missing_freshness_metadata(repo: Path = REPO) -> list[Finding]:
    findings: list[Finding] = []
    for rel in sorted(FRESHNESS_MANAGED):
        path = repo / rel
        if not path.exists():
            findings.append(Finding(rel, 1, "freshness-managed file does not exist"))
            continue
        text = read_text(path)
        has_review_date = bool(LAST_REVIEWED.search(text) or EXTERNAL_LAST_REVIEWED.search(text))
        if not has_review_date:
            findings.append(Finding(rel, 1, "missing absolute last-reviewed date"))
        if not REVIEW_TRIGGER.search(text):
            findings.append(Finding(rel, 1, "missing explicit review trigger"))
    return findings


def find_relative_time_candidates(repo: Path = REPO) -> list[Finding]:
    findings: list[Finding] = []
    for path in markdown_files(repo):
        rel = path.relative_to(repo).as_posix()
        if rel in RELATIVE_TIME_EXCLUDED_FILES:
            continue
        if rel.startswith(RELATIVE_TIME_EXCLUDED_PREFIXES):
            continue
        text = read_text(path)
        for match in RELATIVE_RECENCY.finditer(text):
            findings.append(
                Finding(
                    rel,
                    line_number(text, match.start()),
                    f'review relative-time phrase "{match.group(0)}"',
                )
            )
    return findings


def run_audit(repo: Path = REPO) -> tuple[list[Finding], list[Finding]]:
    errors = find_copied_count_errors(repo)
    errors.extend(find_missing_freshness_metadata(repo))
    warnings = find_relative_time_candidates(repo)
    return errors, warnings


def print_findings(title: str, findings: list[Finding]) -> None:
    if not findings:
        return
    print(f"\n{title} ({len(findings)}):")
    for finding in findings:
        print(f"  {finding.path}:{finding.line}: {finding.message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero for deterministic internal drift or missing freshness metadata",
    )
    args = parser.parse_args()

    errors, warnings = run_audit(REPO)
    print(f"Canonical open problems: {canonical_open_problem_count(REPO)}")
    print_findings("ERROR", errors)
    print_findings("REVIEW", warnings)

    if not errors:
        print("\nNo deterministic freshness/integrity errors found.")
    if warnings:
        print(
            "Relative-time findings are review candidates only; external truth must be "
            "checked against dated primary sources."
        )

    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
