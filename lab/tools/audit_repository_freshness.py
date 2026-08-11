#!/usr/bin/env python3
"""Audit repository text for stale derived state and freshness review candidates.

This tool deliberately separates two classes of maintenance:

1. **Deterministic internal drift** can be checked in CI. Example: a reader page
   says the repository has 13 open problems while the canonical registry has 19.
2. **External or semantic freshness** cannot be inferred from repository text
   alone. The tool surfaces review candidates such as relative recency language,
   novelty claims, or explicitly retired strong formulations; a human or
   research agent must decide whether the source/claim still holds.

Usage:
    python lab/tools/audit_repository_freshness.py
    python lab/tools/audit_repository_freshness.py --strict

``--strict`` exits non-zero for deterministic errors. Review candidates remain
warnings because CI cannot know whether an external or conceptual claim is true.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


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

# Reader-facing pages describe the corpus by its size and by how much of it the
# site publishes. Those magnitudes are recomputable, so they belong to the
# deterministic lane — but they move on ordinary work, and a check that fires on
# every prose edit would train the author to ignore it. The tolerance below is
# what separates "the corpus grew" from "the page stopped describing it": a 10%
# band absorbs normal growth and still catches the multi-week drift this guard
# was written for.
CORPUS_TOLERANCE = 0.10

BENCHMARK_README = Path("lab/benchmarks/inverse-reconstruction/README.md")

# ``v0–v1.13`` in a title or registry row is a currency claim about the whole
# benchmark. A bare ``v1.9`` naming one result is history and must not be
# touched, so only the range form is matched.
BENCHMARK_RANGE = re.compile(r"v0[–-]v1\.(\d+)")

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

# A tiny explicit list of formulations that later repository work has already
# weakened or retired. These are warnings rather than automatic rewrites: an
# occurrence can be historical, quoted, or part of an argument under review.
RETIRED_STRONG_LANGUAGE = (
    re.compile(r"Chord Postulate predicts a phase transition", re.I),
    re.compile(r"Identity is a thermodynamic attractor", re.I),
    re.compile(
        r"(?:Δ-Kohärenz|Delta Coherence|omega|Ω).{0,80}proxy for Identity Persistence",
        re.I,
    ),
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
    # Explicitly quarantined as an early unrecalibrated synthesis. Its old
    # vendor/model language is provenance, not a changing-present claim.
    "papers/quantifying-emergent-utility-in-llms.md",
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


@dataclass(frozen=True)
class DerivedCount:
    """A number copied into prose that can be recomputed from the repository."""

    path: str
    pattern: re.Pattern
    compute: Callable[[Path], int]
    label: str


def _validate_nav():
    """Load the navigation validator by file path.

    ``audit_repository_freshness`` runs both as a script (CI) and as an imported
    package module (tests), and those two modes disagree about what is on
    ``sys.path``. Loading by path sidesteps that instead of duplicating the
    ``exclude_docs`` matching rules, which are the part that must not drift.
    """
    spec = importlib.util.spec_from_file_location(
        "_audit_validate_nav", Path(__file__).with_name("validate_nav.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def corpus_word_count(repo: Path = REPO) -> int:
    return sum(len(read_text(path).split()) for path in markdown_files(repo))


def corpus_markdown_file_count(repo: Path = REPO) -> int:
    return len(markdown_files(repo))


def _theory_counts(repo: Path = REPO) -> tuple[int, int]:
    """Return (theory pages the site publishes, theory pages that exist)."""
    nav = _validate_nav()
    config = nav.load_config(repo / "mkdocs.yml")
    patterns = nav.exclude_patterns(config.get("exclude_docs"))
    docs_dir = repo / config.get("docs_dir", "docs")
    published = nav.markdown_pages(docs_dir, patterns)
    total = len(list((repo / "theory").rglob("*.md")))
    return sum(1 for page in published if page.startswith("theory/")), total


def published_theory_count(repo: Path = REPO) -> int:
    return _theory_counts(repo)[0]


def theory_file_count(repo: Path = REPO) -> int:
    return _theory_counts(repo)[1]


# Every entry is a magnitude a reader is asked to trust. Adding a claim here is
# what keeps it honest; rewording the sentence out from under its pattern is
# reported rather than silently unguarding the number.
DERIVED_COUNTS: tuple[DerivedCount, ...] = (
    DerivedCount(
        "docs/repository-map.md",
        re.compile(r"roughly ([\d,]+) words"),
        corpus_word_count,
        "corpus word count",
    ),
    DerivedCount(
        "docs/repository-map.md",
        re.compile(r"across ([\d,]+) Markdown files"),
        corpus_markdown_file_count,
        "corpus Markdown file count",
    ),
    DerivedCount(
        "docs/repository-map.md",
        re.compile(r"\|\s*Theory\s*\|\s*([\d,]+) essays of [\d,]+\s*\|"),
        published_theory_count,
        "published theory essays",
    ),
    DerivedCount(
        "docs/repository-map.md",
        re.compile(r"\|\s*Theory\s*\|\s*[\d,]+ essays of ([\d,]+)\s*\|"),
        theory_file_count,
        "theory files that exist",
    ),
)


def find_derived_count_errors(repo: Path = REPO) -> list[Finding]:
    """Compare recomputable magnitudes against the numbers written into prose."""
    findings: list[Finding] = []
    for claim in DERIVED_COUNTS:
        path = repo / claim.path
        if not path.exists():
            findings.append(
                Finding(claim.path, 1, f"page carrying the {claim.label} is missing")
            )
            continue
        text = read_text(path)
        match = claim.pattern.search(text)
        if match is None:
            findings.append(
                Finding(
                    claim.path,
                    1,
                    f"no {claim.label} claim matches its guard pattern; "
                    "restore the wording or update DERIVED_COUNTS",
                )
            )
            continue
        stated = int(match.group(1).replace(",", ""))
        actual = claim.compute(repo)
        if actual and abs(stated - actual) / actual > CORPUS_TOLERANCE:
            findings.append(
                Finding(
                    claim.path,
                    line_number(text, match.start()),
                    f"stated {claim.label} is {stated:,}; repository has "
                    f"{actual:,} (outside the {CORPUS_TOLERANCE:.0%} band)",
                )
            )
    return findings


def canonical_benchmark_version(repo: Path = REPO) -> int:
    """Highest inverse-reconstruction benchmark version, from its own title."""
    text = read_text(repo / BENCHMARK_README)
    match = BENCHMARK_RANGE.search(text)
    if match is None:
        raise ValueError(f"No 'v0-v1.N' range found in {BENCHMARK_README}")
    return int(match.group(1))


def find_benchmark_range_errors(repo: Path = REPO) -> list[Finding]:
    """Flag pages that state a stale span for the whole benchmark."""
    canonical = canonical_benchmark_version(repo)
    findings: list[Finding] = []
    for path in markdown_files(repo):
        rel = path.relative_to(repo).as_posix()
        if Path(rel) == BENCHMARK_README:
            continue
        text = read_text(path)
        for match in BENCHMARK_RANGE.finditer(text):
            stated = int(match.group(1))
            if stated != canonical:
                findings.append(
                    Finding(
                        rel,
                        line_number(text, match.start()),
                        f"states benchmark range v0-v1.{stated}; the benchmark "
                        f"is at v1.{canonical}",
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


QUOTED_SPAN = re.compile(r"\"[^\"\n]*\"|“[^”\n]*”")


def quoted_mention(text: str, start: int) -> bool:
    """True when the match sits inside quotation marks on its own line.

    A page that writes: *this note records the source date rather than relying
    on relative phrases such as "weeks old"* is demonstrating the phrase, not
    using it. Flagging the demonstration is worse than missing it — the warning
    lane only works while every entry in it is worth a look, and a standing
    false positive is what teaches a reader to skim past the real one.
    """
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", start)
    line = text[line_start : line_end if line_end != -1 else len(text)]
    offset = start - line_start
    return any(span.start() < offset < span.end() for span in QUOTED_SPAN.finditer(line))


def find_review_candidates(repo: Path = REPO) -> list[Finding]:
    findings: list[Finding] = []
    for path in markdown_files(repo):
        rel = path.relative_to(repo).as_posix()
        if review_excluded(rel):
            continue
        text = read_text(path)
        for match in RELATIVE_RECENCY.finditer(text):
            if quoted_mention(text, match.start()):
                continue
            findings.append(
                Finding(
                    rel,
                    line_number(text, match.start()),
                    f'review relative-time phrase "{match.group(0)}"',
                )
            )
        for match in NOVELTY_LANGUAGE.finditer(text):
            if quoted_mention(text, match.start()):
                continue
            findings.append(
                Finding(
                    rel,
                    line_number(text, match.start()),
                    f'review novelty claim "{match.group(0)}"',
                )
            )
        for pattern in RETIRED_STRONG_LANGUAGE:
            for match in pattern.finditer(text):
                findings.append(
                    Finding(
                        rel,
                        line_number(text, match.start()),
                        f'review retired strong formulation "{match.group(0)}"',
                    )
                )
    return findings


# Backward-compatible name for tests and callers created with the first audit.
def find_relative_time_candidates(repo: Path = REPO) -> list[Finding]:
    return [f for f in find_review_candidates(repo) if "relative-time" in f.message]


def run_audit(repo: Path = REPO) -> tuple[list[Finding], list[Finding]]:
    errors = find_copied_count_errors(repo)
    errors.extend(find_derived_count_errors(repo))
    errors.extend(find_benchmark_range_errors(repo))
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
    print(f"Canonical benchmark version: v1.{canonical_benchmark_version(REPO)}")
    print(
        f"Corpus: {corpus_word_count(REPO):,} words across "
        f"{corpus_markdown_file_count(REPO):,} Markdown files"
    )
    print_findings("ERROR", errors)
    print_findings("REVIEW", warnings)

    if not errors:
        print("\nNo deterministic freshness/integrity errors found.")
    if warnings:
        print(
            "Review findings are candidates only; external truth, novelty, and semantic scope "
            "must be checked against dated primary sources and the current repository theory."
        )

    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
