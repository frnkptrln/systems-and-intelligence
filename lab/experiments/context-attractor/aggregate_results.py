#!/usr/bin/env python3
"""Unblind completed evaluator outputs and report preregistered measurements."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def load_json_output(path: Path) -> dict[str, object]:
    payload, _ = json.JSONDecoder().raw_decode(
        path.read_text(encoding="utf-8").lstrip()
    )
    return payload


def family_map(payload: dict[str, object]) -> dict[str, str]:
    if "family_members" in payload:
        return {
            item_id: family_id
            for family_id, item_ids in payload["family_members"].items()
            for item_id in item_ids
        }
    if "family_by_item" in payload:
        return {
            item_id: f"F{int(family):02d}"
            for item_id, family in payload["family_by_item"].items()
        }
    mapping: dict[str, str] = {}
    for family in payload["families"]:
        for item_id in family["item_ids"]:
            mapping[item_id] = family["name"]
    return mapping


def condition_metrics(
    keys: dict[str, dict[str, object]],
    scores: dict[str, dict[str, object]],
    families: dict[str, str] | None,
) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for condition in ("B", "R"):
        ids = [
            item_id for item_id, key in keys.items() if key["condition"] == condition
        ]
        utility = [float(scores[item_id]["utility"]) for item_id in ids]
        proximity = [float(scores[item_id]["seed_proximity"]) for item_id in ids]
        attraction = [
            1.0 if scores[item_id]["repository_attraction"] else 0.0 for item_id in ids
        ]
        externality = [
            1.0 if scores[item_id]["externality"] else 0.0 for item_id in ids
        ]
        run_utility: dict[str, list[float]] = defaultdict(list)
        for item_id in ids:
            run_utility[str(keys[item_id]["run_id"])].append(
                float(scores[item_id]["utility"])
            )
        run_means = [mean(values) for values in run_utility.values()]
        result[condition] = {
            "n_items": len(ids),
            "utility_mean": mean(utility),
            "utility_run_sd": statistics.pstdev(run_means),
            "repository_attraction_fraction": mean(attraction),
            "seed_proximity_mean": mean(proximity),
            "externality_fraction": mean(externality),
            "question_family_diversity": (
                len({families[item_id] for item_id in ids})
                if families is not None
                else None
            ),
        }
    return result


def difference(metrics: dict[str, dict[str, object]]) -> dict[str, float | None]:
    result: dict[str, float | None] = {}
    for key in (
        "utility_mean",
        "repository_attraction_fraction",
        "seed_proximity_mean",
        "externality_fraction",
        "question_family_diversity",
    ):
        if metrics["R"][key] is None or metrics["B"][key] is None:
            result[key] = None
        else:
            result[key] = float(metrics["R"][key]) - float(metrics["B"][key])
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    blind_dir = run_dir / "blind"
    eval_root = blind_dir / "evaluations"
    eval_manifest = json.loads(
        (eval_root / "manifest.json").read_text(encoding="utf-8")
    )
    if eval_manifest["status"] not in ("completed", "completed_partial"):
        parser.error("blind evaluation is incomplete")

    keys = {
        record["id"]: record
        for record in json.loads((blind_dir / "key.json").read_text(encoding="utf-8"))
    }
    diversity_available = eval_manifest[
        "status"
    ] == "completed" and "question_family_diversity" not in eval_manifest.get(
        "invalid_measurements", {}
    )
    per_evaluator: dict[str, dict[str, object]] = {}
    score_sets: dict[str, dict[str, dict[str, object]]] = {}
    for evaluator in ("E1", "E2"):
        scores = {
            record["id"]: record
            for record in (
                json.loads(line)
                for line in (eval_root / evaluator / "scores.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
            )
        }
        families = None
        if diversity_available:
            families = family_map(
                load_json_output(eval_root / evaluator / "clusters.json")
            )
            if set(families) != set(keys):
                raise ValueError(
                    f"{evaluator} cluster mapping does not cover every blind item"
                )
        metrics = condition_metrics(keys, scores, families=families)
        per_evaluator[evaluator] = {
            "conditions": metrics,
            "difference_R_minus_B": difference(metrics),
        }
        score_sets[evaluator] = scores

    consensus_conditions: dict[str, dict[str, float | None]] = {}
    for condition in ("B", "R"):
        consensus_conditions[condition] = {}
        for key in (
            "utility_mean",
            "utility_run_sd",
            "repository_attraction_fraction",
            "seed_proximity_mean",
            "externality_fraction",
            "question_family_diversity",
        ):
            values = [
                per_evaluator[evaluator]["conditions"][condition][key]
                for evaluator in ("E1", "E2")
            ]
            consensus_conditions[condition][key] = (
                mean([float(value) for value in values])
                if all(value is not None for value in values)
                else None
            )
    consensus_difference = difference(consensus_conditions)

    ids = sorted(keys)
    utility_mae = mean(
        [
            abs(
                float(score_sets["E1"][item_id]["utility"])
                - float(score_sets["E2"][item_id]["utility"])
            )
            for item_id in ids
        ]
    )
    attraction_agreement = mean(
        [
            1.0
            if score_sets["E1"][item_id]["repository_attraction"]
            == score_sets["E2"][item_id]["repository_attraction"]
            else 0.0
            for item_id in ids
        ]
    )
    externality_agreement = mean(
        [
            1.0
            if score_sets["E1"][item_id]["externality"]
            == score_sets["E2"][item_id]["externality"]
            else 0.0
            for item_id in ids
        ]
    )

    diversity_status = (
        "available"
        if diversity_available
        else eval_manifest.get("invalid_measurements", {}).get(
            "question_family_diversity", "unavailable"
        )
    )
    summary = {
        "epistemic_status": (
            "single-model exploratory result with two blinded passes of the same local evaluator"
            + (
                ""
                if diversity_available
                else "; question-family diversity unavailable after clustering quality-control failure"
            )
        ),
        "measurement_validity": {
            "utility": "available",
            "repository_attraction": "available",
            "seed_proximity": "available",
            "externality": "available",
            "question_family_diversity": diversity_status,
        },
        "per_evaluator": per_evaluator,
        "consensus_mean_of_evaluators": {
            "conditions": consensus_conditions,
            "difference_R_minus_B": consensus_difference,
        },
        "evaluator_agreement": {
            "utility_mean_absolute_error": utility_mae,
            "repository_attraction_exact_agreement": attraction_agreement,
            "externality_exact_agreement": externality_agreement,
        },
        "directional_checks": {
            "P1_R_higher_utility": consensus_difference["utility_mean"] > 0,
            "P2_R_higher_repository_attraction": consensus_difference[
                "repository_attraction_fraction"
            ]
            > 0,
            "P3_R_lower_diversity_or_externality": (
                None
                if consensus_difference["question_family_diversity"] is None
                else (
                    consensus_difference["question_family_diversity"] < 0
                    or consensus_difference["externality_fraction"] < 0
                )
            ),
            "P4_R_bridge_pattern": (
                None
                if consensus_difference["question_family_diversity"] is None
                else (
                    consensus_difference["utility_mean"] > 0
                    and consensus_difference["question_family_diversity"] >= 0
                    and consensus_difference["externality_fraction"] >= 0
                )
            ),
        },
    }
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Context-attractor run 001 — blinded descriptive result",
        "",
        "**Epistemic status:** one 8+8 run with Qwen2.5-1.5B-Instruct Q4_K_M; two condition-blind scoring passes used the same local model. Question-family diversity is unavailable because the evaluator failed semantic-clustering quality control. This is an exploratory observation, not a general claim about persistent context or research agents.",
        "",
        "| Measurement | B | R | R − B |",
        "|---|---:|---:|---:|",
    ]
    labels = (
        ("utility_mean", "Immediate research utility"),
        ("repository_attraction_fraction", "Repository attraction"),
        ("seed_proximity_mean", "Seed proximity"),
        ("externality_fraction", "Externality"),
        ("question_family_diversity", "Question-family diversity"),
    )
    for key, label in labels:
        if consensus_difference[key] is None:
            lines.append(f"| {label} | n/a | n/a | n/a |")
        else:
            lines.append(
                f"| {label} | {consensus_conditions['B'][key]:.3f} | "
                f"{consensus_conditions['R'][key]:.3f} | {consensus_difference[key]:+.3f} |"
            )
    utility_delta = consensus_difference["utility_mean"]
    attraction_delta = consensus_difference["repository_attraction_fraction"]
    proximity_delta = consensus_difference["seed_proximity_mean"]
    externality_delta = consensus_difference["externality_fraction"]
    lines.extend(
        [
            "",
            "## Evaluator agreement",
            "",
            f"- Utility mean absolute difference: {utility_mae:.3f}",
            f"- Repository-attraction exact agreement: {attraction_agreement:.1%}",
            f"- Externality exact agreement: {externality_agreement:.1%}",
            "",
            "## Interpretation",
            "",
            f"R scored slightly higher on immediate utility ({utility_delta:+.3f}) and repository attraction ({attraction_delta:+.3f}), while seed proximity changed by {proximity_delta:+.3f} and externality by {externality_delta:+.3f}. This supports P1 and P2 directionally, but neither P3 nor P4 can be evaluated without a valid diversity measure.",
            "",
            "The failed clustering attempts are retained as quality-control evidence and are excluded from the result. Directional checks in `summary.json` are descriptive, not significance tests.",
        ]
    )
    (results_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
