"""Deterministic tests for the context-attractor experiment pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

EXPERIMENT_DIR = (
    Path(__file__).resolve().parents[1] / "lab" / "experiments" / "context-attractor"
)
sys.path.insert(0, str(EXPERIMENT_DIR))

import aggregate_results
import prepare_blind
import run_blind_evaluation
import run_experiment


def score_payload(item_ids: set[str]) -> dict[str, object]:
    return {
        "scores": {
            item_id: {
                "utility": 3,
                "seed_proximity": 4,
                "repository_attraction": False,
                "repository_concepts": [],
                "externality": False,
                "externality_basis": "",
                "family": "Model security",
            }
            for item_id in item_ids
        }
    }


def test_split_items_requires_exactly_five_numbered_items() -> None:
    text = "\n\n".join(f"{index}. Item {index}\nBody" for index in range(1, 6))
    assert len(prepare_blind.split_items(text)) == 5

    with pytest.raises(ValueError, match="expected five"):
        prepare_blind.split_items("1. Only one")


def test_load_json_output_accepts_llama_trailer(tmp_path: Path) -> None:
    output = tmp_path / "output.json"
    output.write_text('{"scores": {}} [end of text]\n', encoding="utf-8")
    assert run_blind_evaluation.load_json_output(output) == {"scores": {}}


def test_generation_resume_requires_matching_frozen_manifest() -> None:
    expected = {key: f"expected-{key}" for key in run_experiment.RESUME_FROZEN_KEYS}
    manifest = {**expected, "status": "running", "started_at": "frozen"}
    run_experiment.validate_resume_manifest(manifest, expected)

    manifest["sampling"] = "changed"
    with pytest.raises(ValueError, match="sampling"):
        run_experiment.validate_resume_manifest(manifest, expected)

    manifest = {**expected, "status": "completed"}
    with pytest.raises(ValueError, match="already finalized"):
        run_experiment.validate_resume_manifest(manifest, expected)


def test_generation_resume_reuses_only_matching_success(tmp_path: Path) -> None:
    raw_path = tmp_path / "B01.md"
    raw_path.write_text("raw output\n", encoding="utf-8")
    matching = {
        "exit_code": 0,
        "raw_sha256": run_experiment.sha256_file(raw_path),
    }
    assert run_experiment.reusable_run(matching, raw_path)

    matching["raw_sha256"] = "changed"
    assert not run_experiment.reusable_run(matching, raw_path)
    assert not run_experiment.reusable_run(None, raw_path)


def test_validate_scores_checks_ids_fields_and_types() -> None:
    item_ids = {"Q001", "Q002"}
    scores = run_blind_evaluation.validate_scores(score_payload(item_ids), item_ids)
    assert [score["id"] for score in scores] == ["Q001", "Q002"]

    missing_field = score_payload(item_ids)
    del missing_field["scores"]["Q001"]["family"]
    with pytest.raises(ValueError, match="invalid score fields"):
        run_blind_evaluation.validate_scores(missing_field, item_ids)

    wrong_type = score_payload(item_ids)
    wrong_type["scores"]["Q001"]["utility"] = True
    with pytest.raises(TypeError, match="invalid utility"):
        run_blind_evaluation.validate_scores(wrong_type, item_ids)


def test_validate_clusters_requires_blind_exact_cover() -> None:
    item_ids = {f"Q{index:03d}" for index in range(1, 17)}
    families = [
        {
            "name": f"Family {index}",
            "item_ids": [f"Q{2 * index - 1:03d}", f"Q{2 * index:03d}"],
        }
        for index in range(1, 9)
    ]
    run_blind_evaluation.validate_clusters({"families": families}, item_ids)

    families[1]["item_ids"][0] = families[0]["item_ids"][0]
    with pytest.raises(ValueError, match="exactly once"):
        run_blind_evaluation.validate_clusters({"families": families}, item_ids)


def test_finalize_manifest_records_partial_clustering_without_losing_start() -> None:
    manifest = {"status": "running", "started_at": "frozen"}
    result = run_blind_evaluation.finalize_manifest(
        manifest, {"E1": "invalid partition"}, "completed"
    )
    assert result["status"] == "completed_partial"
    assert result["started_at"] == "frozen"
    assert result["completed_at"] == "completed"
    assert "question_family_diversity" in result["invalid_measurements"]


def test_aggregate_supports_unavailable_and_available_diversity() -> None:
    keys = {
        "Q001": {"condition": "B", "run_id": "B01"},
        "Q002": {"condition": "B", "run_id": "B02"},
        "Q003": {"condition": "R", "run_id": "R01"},
        "Q004": {"condition": "R", "run_id": "R02"},
    }
    scores = {
        item_id: {
            "utility": index,
            "seed_proximity": 3,
            "repository_attraction": index > 2,
            "externality": False,
        }
        for index, item_id in enumerate(keys, start=1)
    }

    partial = aggregate_results.condition_metrics(keys, scores, families=None)
    assert partial["B"]["question_family_diversity"] is None
    assert aggregate_results.difference(partial)["question_family_diversity"] is None

    families = {"Q001": "F1", "Q002": "F2", "Q003": "F1", "Q004": "F1"}
    complete = aggregate_results.condition_metrics(keys, scores, families=families)
    assert complete["B"]["question_family_diversity"] == 2
    assert complete["R"]["question_family_diversity"] == 1
    assert aggregate_results.difference(complete)["question_family_diversity"] == -1


def test_family_map_reads_valid_cluster_output() -> None:
    payload = {
        "families": [
            {"name": "Grounding", "item_ids": ["Q001", "Q002"]},
            {"name": "Planning", "item_ids": ["Q003"]},
        ]
    }
    assert aggregate_results.family_map(payload) == {
        "Q001": "Grounding",
        "Q002": "Grounding",
        "Q003": "Planning",
    }


def test_result_summary_is_valid_json() -> None:
    run_dir = EXPERIMENT_DIR / "runs" / "2026-08-11-qwen2.5-1.5b-q4km"
    summary = json.loads(
        (run_dir / "results" / "summary.json").read_text(encoding="utf-8")
    )
    assert summary["directional_checks"]["P3_R_lower_diversity_or_externality"] is None
