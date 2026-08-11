#!/usr/bin/env python3
"""Parse the 8+8 raw runs and create a sealed, randomized item bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from pathlib import Path

BLIND_SEED = 26081142
ITEM_START = re.compile(r"(?m)^\s*([1-5])[.)]\s+")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_items(text: str) -> list[str]:
    matches = list(ITEM_START.finditer(text))
    if len(matches) != 5:
        raise ValueError(f"expected five numbered items, found {len(matches)}")
    items: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        items.append(text[match.start() : end].strip())
    return items


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()

    run_dir = args.run_dir.resolve()
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "completed" or len(manifest["runs"]) != 16:
        parser.error("generation manifest is not a completed 16-run experiment")

    source_records: list[dict[str, object]] = []
    for run in manifest["runs"]:
        raw_path = run_dir / run["raw_path"]
        raw_text = raw_path.read_text(encoding="utf-8")
        if sha256_file(raw_path) != run["raw_sha256"]:
            raise ValueError(f"raw hash changed: {raw_path}")
        for item_index, item_text in enumerate(split_items(raw_text), start=1):
            source_records.append(
                {
                    "condition": run["condition"],
                    "run_id": run["run_id"],
                    "replicate": run["replicate"],
                    "item_index": item_index,
                    "text": item_text,
                    "text_sha256": hashlib.sha256(
                        item_text.encode("utf-8")
                    ).hexdigest(),
                }
            )

    if len(source_records) != 80:
        raise ValueError(f"expected 80 items, found {len(source_records)}")
    random.Random(BLIND_SEED).shuffle(source_records)

    blind_dir = run_dir / "blind"
    blind_dir.mkdir(parents=True, exist_ok=True)
    public_records: list[dict[str, str]] = []
    key_records: list[dict[str, object]] = []
    for index, source in enumerate(source_records, start=1):
        blind_id = f"Q{index:03d}"
        public_records.append({"id": blind_id, "text": str(source["text"])})
        key_records.append(
            {
                "id": blind_id,
                "condition": source["condition"],
                "run_id": source["run_id"],
                "replicate": source["replicate"],
                "item_index": source["item_index"],
                "text_sha256": source["text_sha256"],
            }
        )

    items_jsonl = blind_dir / "items.jsonl"
    items_jsonl.write_text(
        "".join(
            json.dumps(record, ensure_ascii=False) + "\n" for record in public_records
        ),
        encoding="utf-8",
    )
    (blind_dir / "items.md").write_text(
        "\n\n".join(
            f"## {record['id']}\n\n{record['text']}" for record in public_records
        )
        + "\n",
        encoding="utf-8",
    )
    key_path = blind_dir / "key.json"
    key_path.write_text(json.dumps(key_records, indent=2) + "\n", encoding="utf-8")
    preparation = {
        "blind_seed": BLIND_SEED,
        "item_count": len(public_records),
        "items_jsonl_sha256": sha256_file(items_jsonl),
        "key_sha256": sha256_file(key_path),
        "source_manifest_sha256": sha256_file(run_dir / "manifest.json"),
    }
    (blind_dir / "preparation.json").write_text(
        json.dumps(preparation, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
