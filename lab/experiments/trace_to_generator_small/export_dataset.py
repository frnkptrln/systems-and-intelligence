#!/usr/bin/env python3
"""Export deterministic JSONL splits suitable for a Hugging Face dataset repo."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .data import SPLIT_PARAMETER_QUANTILES, DataConfig, write_jsonl
from .dynamics import FAMILIES


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--train-size", type=int, default=20_000)
    parser.add_argument("--eval-size", type=int, default=4_000)
    parser.add_argument("--trace-length", type=int, default=24)
    parser.add_argument("--seed", type=int, default=260811)
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        parser.error("output directory must be absent or empty")
    output_dir.mkdir(parents=True, exist_ok=True)
    config = DataConfig(trace_length=args.trace_length)
    sizes = {"train": args.train_size, "iid": args.eval_size, "ood": args.eval_size}
    files: dict[str, dict[str, str | int]] = {}
    for split, size in sizes.items():
        path = output_dir / f"{split}.jsonl"
        write_jsonl(path, size, split, seed=args.seed, config=config)
        files[split] = {"path": path.name, "size": size, "sha256": sha256_file(path)}
    manifest = {
        "dataset": "trace-to-generator-small",
        "status": "synthetic deterministic export",
        "seed": args.seed,
        "data_config": config.to_dict(),
        "families": [family.to_dict() for family in FAMILIES],
        "split_parameter_quantiles": SPLIT_PARAMETER_QUANTILES,
        "files": files,
    }
    (output_dir / "dataset_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
