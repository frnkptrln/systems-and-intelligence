#!/usr/bin/env python3
"""Prepare exact, condition-blind E3/E4 packets; never call an evaluator."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

from run_blind_evaluation import cluster_schema, validate_clusters


ROOT = Path(__file__).resolve().parent
ITEMS = ROOT / "runs/2026-08-11-qwen2.5-1.5b-q4km/blind/items.jsonl"
ITEMS_SHA256 = "f073fe9bb6876fc0c5bf880802568a18991f59d2e71823f8ee9f1433ba27ace1"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_items(path: Path) -> tuple[bytes, set[str]]:
    raw = path.read_bytes()
    if sha256(raw) != ITEMS_SHA256:
        raise ValueError("run 001 blind item bytes differ from the frozen source")
    items = [json.loads(line) for line in raw.decode().splitlines()]
    if len(items) != 80 or any(set(item) != {"id", "text"} for item in items):
        raise ValueError("expected exactly 80 id/text-only items")
    ids = {item["id"] for item in items}
    if len(ids) != 80:
        raise ValueError("blind item IDs must be unique")
    return raw, ids


def packet_bytes(evaluator: str, items_path: Path = ITEMS) -> bytes:
    if evaluator not in {"E3", "E4"}:
        raise ValueError("recovery uses only new evaluator IDs E3/E4")
    raw, ids = load_items(items_path)
    files = {
        "items.jsonl": raw,
        "instructions.md": (ROOT / "recovery-kit/evaluator-instructions.md").read_bytes(),
        "clusters.schema.json": (json.dumps(cluster_schema(ids), indent=2, sort_keys=True) + "\n").encode(),
    }
    files["manifest.json"] = (json.dumps({
        "evaluator_id": evaluator,
        "files": {name: sha256(data) for name, data in sorted(files.items())},
    }, sort_keys=True, indent=2) + "\n").encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    return buffer.getvalue()


def prepare(output: Path) -> dict:
    # Compute and validate all bytes before creating a fresh output directory.
    packets = {f"{evaluator}.zip": packet_bytes(evaluator) for evaluator in ("E3", "E4")}
    receipt = {
        "status": "prepared_not_distributed_not_evaluated",
        "items_sha256": ITEMS_SHA256,
        "protocol_sha256": sha256((ROOT / "recovery-kit/recovery-addendum.md").read_bytes()),
        "source_hashes": {name: sha256((ROOT / name).read_bytes()) for name in (
            "prepare_diversity_recovery.py", "run_blind_evaluation.py", "run_experiment.py",
        )},
        "packet_sha256": {name: sha256(raw) for name, raw in packets.items()},
    }
    output.mkdir(parents=True, exist_ok=False)
    for name, raw in packets.items():
        (output / name).write_bytes(raw)
    (output / "preparation.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def validate_partition(path: Path, items_path: Path = ITEMS) -> dict:
    _, ids = load_items(items_path)
    raw = path.read_bytes()
    payload = json.loads(raw)
    if not isinstance(payload, dict) or set(payload) != {"families"}:
        raise ValueError("partition must contain only families")
    validate_clusters(payload, ids)
    names = [" ".join(family["name"].casefold().split()) for family in payload["families"]]
    if len(set(names)) != len(names):
        raise ValueError("scientific family names must be distinct")
    return {"exact_cover": "passed", "semantic_qc": "pending_blind_review",
            "independence": "not_verified", "unblinding_ready": False,
            "partition_sha256": sha256(raw)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("prepare")
    export.add_argument("--output", type=Path, required=True)
    validation = commands.add_parser("validate")
    validation.add_argument("partition", type=Path)
    args = parser.parse_args()
    result = prepare(args.output) if args.command == "prepare" else validate_partition(args.partition)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
