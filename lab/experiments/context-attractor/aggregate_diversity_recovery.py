#!/usr/bin/env python3
"""Analyze the received partitions only after hashed independent blind QC."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from aggregate_results import condition_metrics, difference, family_map
from complete_diversity_recovery import PARTITION_HASHES, RECEIVED, qc_packet_bytes
from prepare_diversity_recovery import ROOT, sha256, validate_partition


RUN = ROOT / "runs/2026-08-11-qwen2.5-1.5b-q4km"


def utc(value: str) -> datetime:
    stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if stamp.utcoffset() != timezone.utc.utcoffset(stamp):
        raise ValueError("QC timestamps must explicitly use UTC")
    return stamp


def review_gate(qc_dir: Path, received: Path = RECEIVED) -> dict:
    """Check recorded review provenance; a hash cannot prove reviewer honesty."""
    receipt_raw = (qc_dir / "receipt.json").read_bytes()
    receipt = json.loads(receipt_raw)
    frozen_at = utc(receipt["frozen_at_utc"])
    if frozen_at > datetime.now(timezone.utc):
        raise ValueError("QC freeze timestamp is in the future")
    if set(receipt["reviews"]) != set(PARTITION_HASHES):
        raise ValueError("both E3 and E4 reviews are required")
    reviewers = []
    decisions = {}
    for evaluator in PARTITION_HASHES:
        entry = receipt["reviews"][evaluator]
        if entry.get("fresh_context") is not True:
            raise ValueError("reviewer fresh-context provenance is required")
        if any(not isinstance(entry.get(key), str) or not entry[key].strip()
               for key in ("reviewer_id", "model")):
            raise ValueError("record the actual reviewer identity and model")
        reviewers.append(entry["reviewer_id"])
        if utc(entry["completed_at_utc"]) > frozen_at:
            raise ValueError("both reviews must complete before their freeze")
        packet_hash = sha256(qc_packet_bytes(evaluator, received))
        if packet_hash != entry["input_packet_sha256"]:
            raise ValueError(f"{evaluator} QC did not receive the pinned packet")
        raw = (qc_dir / evaluator / "review.json").read_bytes()
        if sha256(raw) != entry["output_sha256"]:
            raise ValueError(f"{evaluator} QC bytes changed after their freeze")
        review = json.loads(raw)
        if (review.get("decision") not in {"pass", "fail"}
                or not isinstance(review.get("rationale"), str)
                or not review["rationale"].strip()
                or not isinstance(review.get("observations"), list)):
            raise ValueError("QC must record a decision, rationale and observations")
        decisions[evaluator] = review["decision"]
    if len(set(reviewers)) != 2:
        raise ValueError("the two QC reviews must use separate reviewer contexts")
    return {"decisions": decisions, "qc_receipt_sha256": sha256(receipt_raw),
            "frozen_at_utc": receipt["frozen_at_utc"],
            "passed": all(value == "pass" for value in decisions.values())}


def diversity_counts(keys: dict, partitions: dict, utility_delta: float,
                     externality_delta: float) -> dict:
    if len(keys) != 80 or any(sum(key["condition"] == c for key in keys.values()) != 40
                              for c in ("B", "R")):
        raise ValueError("expected the original 40 B and 40 R item assignments")
    per_evaluator = {}
    signs = []
    for evaluator in ("E3", "E4"):
        families = family_map(partitions[evaluator])
        if set(families) != set(keys):
            raise ValueError("partition and condition key IDs differ")
        counts = {condition: len({families[item_id] for item_id, key in keys.items()
                                 if key["condition"] == condition})
                  for condition in ("B", "R")}
        delta = counts["R"] - counts["B"]
        signs.append((delta > 0) - (delta < 0))
        per_evaluator[evaluator] = {
            "conditions": counts, "difference_R_minus_B": delta,
            "directional_checks": {
                "P3_R_lower_diversity_or_externality": delta < 0 or externality_delta < 0,
                "P4_R_bridge_pattern": utility_delta > 0 and delta >= 0 and externality_delta >= 0,
            },
        }
    agreement = len(set(signs)) == 1
    return {
        "per_evaluator": per_evaluator,
        "sign_agreement": agreement,
        "P3_P4_evaluable": agreement,
        "directional_checks": (per_evaluator["E3"]["directional_checks"] if agreement
                               else {name: None for name in per_evaluator["E3"]["directional_checks"]}),
        "status": ("recovered_descriptive_measurement" if agreement
                   else "unresolved_sign_disagreement_requires_blind_adjudication"),
    }


def analyze(qc_dir: Path, run: Path = RUN, received: Path = RECEIVED) -> dict:
    gate = review_gate(qc_dir, received)
    if not gate["passed"]:
        # No key, old scores or unblinded summary is opened on this path.
        return {"status": "blind_semantic_qc_failed", "qc_gate": gate,
                "P3_P4_evaluable": False, "per_evaluator": None,
                "condition_key_accessed": False}

    evidence = json.loads((received / "preserved-evidence.json").read_bytes())
    for name, digest in evidence["files_sha256"].items():
        if sha256((run / name).read_bytes()) != digest:
            raise ValueError(f"original run evidence changed: {name}")
    keys = {record["id"]: record for record in json.loads((run / "blind/key.json").read_bytes())}
    baseline = json.loads((run / "results/summary.json").read_bytes())
    for evaluator in ("E1", "E2"):
        scores = {record["id"]: record for record in (
            json.loads(line) for line in (run / f"blind/evaluations/{evaluator}/scores.jsonl")
            .read_text().splitlines())}
        metrics = condition_metrics(keys, scores, families=None)
        expected = baseline["per_evaluator"][evaluator]
        if metrics != expected["conditions"] or difference(metrics) != expected["difference_R_minus_B"]:
            raise ValueError("original non-diversity metrics do not reproduce")
    partitions = {}
    for evaluator in PARTITION_HASHES:
        path = received / evaluator / "clusters.json"
        validate_partition(path)
        partitions[evaluator] = json.loads(path.read_bytes())
    prior_difference = baseline["consensus_mean_of_evaluators"]["difference_R_minus_B"]
    result = diversity_counts(keys, partitions, prior_difference["utility_mean"],
                              prior_difference["externality_fraction"])
    result.update({"qc_gate": gate, "condition_key_accessed": True,
                   "analysis_at_utc": datetime.now(timezone.utc).isoformat(),
                   "original_evidence_files_unchanged": len(evidence["files_sha256"]),
                   "non_diversity_metrics_reproduced_unchanged": True,
                   "partition_sha256": PARTITION_HASHES,
                   "interpretation_limit": "Single-run descriptive counts; QC is not independent replication or proof of a harmful attractor."})
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qc_dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must be a new file; frozen results are never overwritten")
    result = analyze(args.qc_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
