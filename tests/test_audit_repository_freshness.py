from pathlib import Path

from lab.tools.audit_repository_freshness import (
    canonical_open_problem_count,
    find_copied_count_errors,
    find_missing_freshness_metadata,
    find_relative_time_candidates,
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
