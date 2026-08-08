#!/usr/bin/env python3
"""Audit repository text for stale derived state and freshness review candidates.

This tool deliberately separates two classes of maintenance:

1. **Deterministic internal drift** can be checked in CI. Example: a reader page
   says the repository has 13 open problems while the canonical registry has 19.
2. **External freshness** cannot be inferred from repository text alone. The tool
   only surfaces review candidates such as relative recency language or novelty
   claims; a human or research agent must check primary sources.

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

# Novelty/superlative language can be perfectly correct when written and decay
# without any local edit. The audit therefore surfaces it for review rather
# than treating it as an error.
NOVELTY_LANGUAGE = re.compile(
    r"\b(?:"
    r"for the first time"
    r"|first\s+(?:internal[- ]inspection\s+)?evidence"
    r"|first\s+(?:reported\s+)?demonstration"
    r"|first\s+(?:known\s+)?result"
    r"|first\s+(?:known\s+)?example"
    r"|only\s+(?:known\s+)?(?:method|result|example|system)"
    r")\b",
    re.I,
)

# Dated exploratory/history lanes may use relative language or rhetorical
# superlatives without pretending to describe the present. They are not part
# of the warning scan.
REVIEW_EXCLUDED_PREFIXES = (
    "fiction/",
    "ideas/",
    "logs/",
)
REVIEW_EXCLUDED_FILES = {
    "meta/repository-meta/freshness-and-review.md",
}

# Files whose argument materially depends on a changing external interface or
# research snapshot. Add to this set deliberately; do not try to infer the list
# from filenames.
FRESHNESS_MANAGED = {
    "lab/providers/README.md",
    "theory/ai/j-space-and-global-availability.md",
    "theory/ai/world-models-and-vla.md",
    "theory/emergence/emergence-origin-intelligence.md",
    "theory/identity/consciousness-as-global-availability.md",
    "theory/narrative/asimov-ai-latent-thinking.md",
}

# Markdown authors commonly bold either the label alone (``**Label**:``) or
# the label plus colon (``**Label:**``). Accept both, as well as plain text.
_FIELD_COLON = r"(?::\*\*|\*\*:|:)"

LAST_REVIEWED = re.compile(
    rf"(?:"
    rf"(?:\*\*)?Last reviewed{_FIELD_COLON}\s*\d{{4}}-\d{{2}}-\d{{2}}"
    rf"|^last_reviewed:\s*\d{{4}}-\d{{2}}-\d{{2}}\s*$"
    rf")",
    re.I | re.MULTILINE,
)
EXTERNAL_LAST_REVIEWED = re.compile(
    rf"(?:\*\*)?External interface last reviewed{_FIELD_COLON}\s*\d{{4}}-\d{{2}}-\d{{2}}",
    re.I,
)
REVIEW_TRIGGER = re.compile(
    rf"(?:"
    rf"(?:\*\*)?Review trigger{_FIELD_COLON}"
    rf"|^review_trigger:\s*\S.+$"
    rf")",
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


def review_excluded(rel: str) -> bool:
    return rel in REVIEW_EXCLUDED_FILES or rel.startswith(REVIEW_EXCLUDED_PREFIXES)


def find_review_candidates(repo: Path = REPO) -> list[Finding]:
    findings: list[Finding] = []
    for path in markdown_files(repo):
        rel = path.relative_to(repo).as_posix()
        if review_excluded(rel):
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
        for match in NOVELTY_LANGUAGE.finditer(text):
            findings.append(
                Finding(
                    rel,
                    line_number(text, match.start()),
                    f'review novelty claim "{match.group(0)}"',
                )
            )
    return findings


# Backward-compatible name for tests and callers created with the first audit.
def find_relative_time_candidates(repo: Path = REPO) -> list[Finding]:
    return [f for f in find_review_candidates(repo) if "relative-time" in f.message]


def run_audit(repo: Path = REPO) -> tuple[list[Finding], list[Finding]]:
    errors = find_copied_count_errors(repo)
    errors.extend(find_missing_freshness_metadata(repo))
    warnings = find_review_candidates(repo)
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
            "Review findings are candidates only; external truth and novelty must be "
            "checked against dated primary sources."
        )

    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
