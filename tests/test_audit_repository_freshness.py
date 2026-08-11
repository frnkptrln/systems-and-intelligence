import re
from pathlib import Path

import pytest

from lab.tools.audit_repository_freshness import (
    DerivedCount,
    canonical_benchmark_version,
    canonical_open_problem_count,
    corpus_markdown_file_count,
    corpus_word_count,
    find_benchmark_range_errors,
    find_copied_count_errors,
    find_derived_count_errors,
    find_missing_freshness_metadata,
    find_relative_time_candidates,
    find_review_candidates,
)


def write(repo: Path, rel: str, text: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def seed_open_problems(repo: Path, n: int = 3) -> None:
    body = "\n\n".join(f"## Open Problem {i}: P{i}" for i in range(1, n + 1))
    write(repo, "theory/reference/open-problems.md", body)


def test_counts_canonical_open_problem_headings(tmp_path):
    seed_open_problems(tmp_path, 4)
    assert canonical_open_problem_count(tmp_path) == 4


def test_detects_stale_copied_open_problem_count(tmp_path):
    seed_open_problems(tmp_path, 4)
    write(
        tmp_path,
        "book/current.md",
        "The repository now maintains [3 open problems](../theory/reference/open-problems.md).",
    )

    findings = find_copied_count_errors(tmp_path)

    assert len(findings) == 1
    assert findings[0].path == "book/current.md"
    assert "canonical registry has 4" in findings[0].message


def test_accepts_matching_copied_count(tmp_path):
    seed_open_problems(tmp_path, 4)
    write(tmp_path, "book/current.md", "The repository maintains 4 open problems.")
    assert find_copied_count_errors(tmp_path) == []


def test_relative_time_is_warning_not_error_source(tmp_path):
    seed_open_problems(tmp_path, 1)
    write(tmp_path, "theory/ai/note.md", "This result is weeks old and currently unreplicated.")
    write(tmp_path, "logs/001.md", "Today we tried something.")

    findings = find_relative_time_candidates(tmp_path)

    assert {f.path for f in findings} == {"theory/ai/note.md"}
    assert {f.message for f in findings} == {
        'review relative-time phrase "weeks old"',
        'review relative-time phrase "currently"',
    }


def test_novelty_language_is_review_candidate(tmp_path):
    seed_open_problems(tmp_path, 1)
    write(
        tmp_path,
        "meta/research-alignment/map.md",
        "This is the first internal-inspection evidence for the proposed layer.",
    )

    findings = find_review_candidates(tmp_path)

    assert len(findings) == 1
    assert findings[0].path == "meta/research-alignment/map.md"
    assert findings[0].message == (
        'review novelty claim "first internal-inspection evidence"'
    )


def test_retired_strong_language_is_review_candidate(tmp_path):
    seed_open_problems(tmp_path, 1)
    write(
        tmp_path,
        "papers/current.md",
        "The Chord Postulate predicts a phase transition at a critical IP_c.",
    )

    findings = find_review_candidates(tmp_path)

    assert len(findings) == 1
    assert findings[0].path == "papers/current.md"
    assert findings[0].message == (
        'review retired strong formulation "Chord Postulate predicts a phase transition"'
    )


def test_history_lanes_excluded_from_novelty_warnings(tmp_path):
    seed_open_problems(tmp_path, 1)
    write(tmp_path, "ideas/001.md", "For the first time, the note tried this framing.")
    write(tmp_path, "fiction/001.md", "The first evidence arrived after midnight.")

    assert find_review_candidates(tmp_path) == []


def test_quarantined_legacy_paper_is_excluded_from_review_warnings(tmp_path, monkeypatch):
    seed_open_problems(tmp_path, 1)
    rel = "papers/quantifying-emergent-utility-in-llms.md"
    write(
        tmp_path,
        rel,
        "Recently, the Chord Postulate predicts a phase transition at a critical IP_c.",
    )

    assert find_review_candidates(tmp_path) == []


def test_managed_file_requires_review_date_and_trigger(tmp_path, monkeypatch):
    seed_open_problems(tmp_path, 1)
    write(tmp_path, "managed.md", "# External snapshot\n")

    import lab.tools.audit_repository_freshness as audit

    monkeypatch.setattr(audit, "FRESHNESS_MANAGED", {"managed.md"})
    findings = find_missing_freshness_metadata(tmp_path)

    assert {f.message for f in findings} == {
        "missing absolute last-reviewed date",
        "missing explicit review trigger",
    }


def test_managed_file_accepts_frontmatter_review_metadata(tmp_path, monkeypatch):
    seed_open_problems(tmp_path, 1)
    write(
        tmp_path,
        "managed.md",
        "---\nlast_reviewed: 2026-08-08\nreview_trigger: provider contract changes\n---\n",
    )

    import lab.tools.audit_repository_freshness as audit

    monkeypatch.setattr(audit, "FRESHNESS_MANAGED", {"managed.md"})
    assert find_missing_freshness_metadata(tmp_path) == []


def test_managed_file_accepts_bold_markdown_metadata(tmp_path, monkeypatch):
    seed_open_problems(tmp_path, 1)
    write(
        tmp_path,
        "managed.md",
        "# Snapshot\n\n**Last reviewed:** 2026-08-08  \n"
        "**Review trigger:** provider contract changes.\n",
    )

    import lab.tools.audit_repository_freshness as audit

    monkeypatch.setattr(audit, "FRESHNESS_MANAGED", {"managed.md"})
    assert find_missing_freshness_metadata(tmp_path) == []


def test_managed_file_accepts_external_interface_review_label(tmp_path, monkeypatch):
    seed_open_problems(tmp_path, 1)
    write(
        tmp_path,
        "managed.md",
        "# Provider\n\n**External interface last reviewed:** 2026-08-08  \n"
        "**Review trigger:** API behavior changes.\n",
    )

    import lab.tools.audit_repository_freshness as audit

    monkeypatch.setattr(audit, "FRESHNESS_MANAGED", {"managed.md"})
    assert find_missing_freshness_metadata(tmp_path) == []


# --- derived counts copied into prose ---------------------------------------


def guard(compute, pattern=r"roughly ([\d,]+) words") -> DerivedCount:
    return DerivedCount("docs/page.md", re.compile(pattern), compute, "widget count")


def use_guard(monkeypatch, claim: DerivedCount) -> None:
    import lab.tools.audit_repository_freshness as audit

    monkeypatch.setattr(audit, "DERIVED_COUNTS", (claim,))


def test_derived_count_accepts_value_inside_tolerance(tmp_path, monkeypatch):
    write(tmp_path, "docs/page.md", "It holds roughly 100 words.")
    use_guard(monkeypatch, guard(lambda repo: 105))

    assert find_derived_count_errors(tmp_path) == []


def test_derived_count_flags_value_outside_tolerance(tmp_path, monkeypatch):
    write(tmp_path, "docs/page.md", "It holds roughly 100 words.")
    use_guard(monkeypatch, guard(lambda repo: 130))

    findings = find_derived_count_errors(tmp_path)

    assert len(findings) == 1
    assert findings[0].path == "docs/page.md"
    assert "stated widget count is 100" in findings[0].message
    assert "repository has 130" in findings[0].message


def test_derived_count_reads_thousands_separators(tmp_path, monkeypatch):
    write(tmp_path, "docs/page.md", "It holds roughly 244,000 words.")
    use_guard(monkeypatch, guard(lambda repo: 244_444))

    assert find_derived_count_errors(tmp_path) == []


def test_reworded_claim_does_not_silently_unguard_the_number(tmp_path, monkeypatch):
    """Dropping the guarded phrasing must be reported, not quietly accepted."""
    write(tmp_path, "docs/page.md", "It holds a great many words.")
    use_guard(monkeypatch, guard(lambda repo: 130))

    findings = find_derived_count_errors(tmp_path)

    assert len(findings) == 1
    assert "guard pattern" in findings[0].message


def test_missing_page_carrying_a_guarded_count_is_an_error(tmp_path, monkeypatch):
    use_guard(monkeypatch, guard(lambda repo: 130))

    findings = find_derived_count_errors(tmp_path)

    assert len(findings) == 1
    assert "is missing" in findings[0].message


def test_corpus_counts_measure_the_markdown_tree(tmp_path):
    write(tmp_path, "theory/a.md", "one two three")
    write(tmp_path, "logs/b.md", "four five")
    write(tmp_path, "lab/tool.py", "ignored source file")

    assert corpus_word_count(tmp_path) == 5
    assert corpus_markdown_file_count(tmp_path) == 2


# --- benchmark version range ------------------------------------------------


def seed_benchmark(repo: Path, version: int = 13) -> None:
    write(
        repo,
        "lab/benchmarks/inverse-reconstruction/README.md",
        f"# Inverse-Reconstruction Benchmark (v0-v1.{version}) - Trace to Candidates",
    )


def test_canonical_benchmark_version_comes_from_its_own_title(tmp_path):
    seed_benchmark(tmp_path, 13)
    assert canonical_benchmark_version(tmp_path) == 13


def test_stale_benchmark_range_is_an_error(tmp_path):
    seed_benchmark(tmp_path, 13)
    write(tmp_path, "theory/core/conceptual-map.md", "| instrument | benchmark v0-v1.8 |")

    findings = find_benchmark_range_errors(tmp_path)

    assert len(findings) == 1
    assert findings[0].path == "theory/core/conceptual-map.md"
    assert "the benchmark is at v1.13" in findings[0].message


def test_matching_benchmark_range_passes(tmp_path):
    seed_benchmark(tmp_path, 13)
    write(tmp_path, "meta/registry.md", "Inverse-reconstruction benchmark (v0-v1.13)")

    assert find_benchmark_range_errors(tmp_path) == []


def test_en_dash_range_is_matched(tmp_path):
    seed_benchmark(tmp_path, 13)
    write(tmp_path, "meta/registry.md", "benchmark v0–v1.9 is the instrument")

    findings = find_benchmark_range_errors(tmp_path)

    assert len(findings) == 1
    assert "v0-v1.9" in findings[0].message


def test_naming_one_past_version_is_history_not_drift(tmp_path):
    """A bare ``v1.9`` reports a result and must never be rewritten."""
    seed_benchmark(tmp_path, 13)
    write(
        tmp_path,
        "theory/core/note.md",
        "v1.9 ruled out that dependency model; v1.11 selected support downward.",
    )

    assert find_benchmark_range_errors(tmp_path) == []


def test_benchmark_readme_without_a_range_is_reported(tmp_path):
    write(tmp_path, "lab/benchmarks/inverse-reconstruction/README.md", "# Benchmark")

    with pytest.raises(ValueError):
        canonical_benchmark_version(tmp_path)


# --- quoted mentions are demonstrations, not claims ---------------------------


def test_quoted_relative_time_phrase_is_not_flagged(tmp_path):
    """A page explaining that it avoids a phrase must not be flagged for it."""
    seed_open_problems(tmp_path, 1)
    write(
        tmp_path,
        "theory/ai/note.md",
        "This note records the source date rather than relying on relative "
        'phrases such as "weeks old."\n',
    )

    assert find_review_candidates(tmp_path) == []


def test_curly_quoted_mention_is_not_flagged(tmp_path):
    seed_open_problems(tmp_path, 1)
    write(tmp_path, "theory/ai/note.md", "Avoid “currently” in reader pages.\n")

    assert find_review_candidates(tmp_path) == []


def test_unquoted_use_on_a_line_with_quotes_is_still_flagged(tmp_path):
    """Quoting something else on the line must not grant blanket immunity."""
    seed_open_problems(tmp_path, 1)
    write(
        tmp_path,
        "theory/ai/note.md",
        'The suite is called "the Agentic Identity Suite" and currently runs on toys.\n',
    )

    findings = find_review_candidates(tmp_path)

    assert len(findings) == 1
    assert findings[0].message == 'review relative-time phrase "currently"'


def test_quoted_novelty_claim_is_not_flagged(tmp_path):
    seed_open_problems(tmp_path, 1)
    write(
        tmp_path,
        "meta/research-alignment/map.md",
        'Reviewers should challenge any "first evidence" wording in the draft.\n',
    )

    assert find_review_candidates(tmp_path) == []


def test_quote_spanning_lines_does_not_swallow_later_uses(tmp_path):
    """Quote matching is per line, so an unclosed quote cannot mask a page."""
    seed_open_problems(tmp_path, 1)
    write(
        tmp_path,
        "theory/ai/note.md",
        'An opening " quote mark on this line.\nThe suite currently runs on toys.\n',
    )

    findings = find_review_candidates(tmp_path)

    assert len(findings) == 1
    assert findings[0].line == 2


def test_story_count_excludes_the_fiction_index(tmp_path):
    """The index page in fiction/ is not a story."""
    from lab.tools.audit_repository_freshness import story_count

    write(tmp_path, "fiction/README.md", "index")
    write(tmp_path, "fiction/01_a.md", "story")
    write(tmp_path, "fiction/02_b.md", "story")

    assert story_count(tmp_path) == 2
