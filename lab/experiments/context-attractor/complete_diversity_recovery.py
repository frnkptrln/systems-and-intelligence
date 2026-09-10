#!/usr/bin/env python3
"""Preserve received partitions and prepare independent, condition-blind QC."""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
import zipfile

from prepare_diversity_recovery import ITEMS, ITEMS_SHA256, ROOT, sha256, validate_partition


RECEIVED = ROOT / "recovery-kit/received"
PARTITION_HASHES = {
    "E3": "2590fdb8a70fe87943a6b2b07748eccad011ae369bfe553c3a0db1c738baccfb",
    "E4": "a3cb96652c787eec196d629f3b52b56cd49d79e4c7f7881df7421e94170bdbbb",
}


def qc_packet_bytes(evaluator: str, received: Path = RECEIVED) -> bytes:
    if evaluator not in PARTITION_HASHES:
        raise ValueError("review only the received E3 or E4 partition")
    partition = received / evaluator / "clusters.json"
    validation = validate_partition(partition)
    if validation["partition_sha256"] != PARTITION_HASHES[evaluator]:
        raise ValueError(f"{evaluator} partition differs from its recorded intake hash")
    files = {
        "items.jsonl": ITEMS.read_bytes(),
        "clusters.json": partition.read_bytes(),
        "instructions.md": (ROOT / "recovery-kit/qc-instructions.md").read_bytes(),
    }
    files["manifest.json"] = (json.dumps({
        "files": {name: sha256(raw) for name, raw in sorted(files.items())},
    }, indent=2, sort_keys=True) + "\n").encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, raw in sorted(files.items()):
            entry = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, raw)
    return buffer.getvalue()


def prepare_qc(output: Path, received: Path = RECEIVED) -> dict:
    """Export only after both original submissions pass exact-cover/hash checks."""
    packets = {f"{evaluator}-qc.zip": qc_packet_bytes(evaluator, received)
               for evaluator in PARTITION_HASHES}
    receipt = {
        "status": "received_structurally_valid_pending_independent_blind_semantic_qc",
        "items_sha256": ITEMS_SHA256,
        "partition_sha256": PARTITION_HASHES,
        "packet_sha256": {name: sha256(raw) for name, raw in packets.items()},
        "unblinding_ready": False,
    }
    output.mkdir(parents=True, exist_ok=False)
    for name, raw in packets.items():
        (output / name).write_bytes(raw)
    (output / "preparation.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare_qc(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
