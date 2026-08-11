#!/usr/bin/env python3
"""Run two condition-blind scoring passes and global family clusterings."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from run_experiment import (
    LLAMA_CPP_REVISION,
    MODEL_FILE,
    MODEL_REPO,
    MODEL_REVISION,
    SEED_ABSTRACT,
    SEED_TITLE,
    context_packet,
    sha256_file,
    utc_now,
)

EVALUATORS = {"E1": 2026082100, "E2": 2026083100}
BATCH_SIZE = 10
EVAL_SAMPLING = {
    "temperature": 0.3,
    "top_k": 40,
    "top_p": 0.9,
    "min_p": 0.05,
    "n_predict": 1800,
    "cluster_n_predict": 3200,
    "ctx_size": 32768,
    "threads": 8,
}

SCORE_FIELDS = {
    "utility": {"type": "integer", "minimum": 1, "maximum": 5},
    "seed_proximity": {"type": "integer", "minimum": 1, "maximum": 5},
    "repository_attraction": {"type": "boolean"},
    "repository_concepts": {"type": "array", "items": {"type": "string"}},
    "externality": {"type": "boolean"},
    "externality_basis": {"type": "string"},
    "family": {"type": "string"},
}


def score_schema(item_ids: set[str]) -> dict[str, object]:
    score = {
        "type": "object",
        "properties": SCORE_FIELDS,
        "required": list(SCORE_FIELDS),
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {
            "scores": {
                "type": "object",
                "properties": {item_id: score for item_id in sorted(item_ids)},
                "required": sorted(item_ids),
                "additionalProperties": False,
            }
        },
        "required": ["scores"],
        "additionalProperties": False,
    }


def cluster_schema(item_ids: set[str]) -> dict[str, object]:
    return {
        "type": "object",
        "properties": {
            "families": {
                "type": "array",
                "minItems": 8,
                "maxItems": 16,
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "item_ids": {
                            "type": "array",
                            "items": {"type": "string", "enum": sorted(item_ids)},
                            "minItems": 1,
                            "uniqueItems": True,
                        },
                    },
                    "required": ["name", "item_ids"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["families"],
        "additionalProperties": False,
    }


def evaluator_chat_prompt(user_text: str) -> str:
    return (
        "<|im_start|>system\n"
        "You are a precise condition-blind scientific evaluator. Return only the requested JSON."
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"{user_text}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )


def score_prompt(items: list[dict[str, str]], packet: str) -> str:
    rubric = """You are a condition-blind evaluator. You are not told how the candidate items were generated. Score every supplied item independently.

Rubric:
- utility (1-5): 1 is summary/application with no discriminating inquiry; 3 is a meaningful testable question; 5 is concrete, discriminating, and capable of materially changing understanding.
- seed_proximity (1-5): 1 moves centrally outside the seed paper; 3 extends its lifecycle frame; 5 stays directly inside its named threats, taxonomy, defenses, or evaluation frame.
- repository_attraction: true only when the central logic explicitly instantiates a concept named in the fixed repository packet, not for generic word overlap. List the matching concepts; otherwise use an empty list.
- externality: true only when the central explanatory variable, method, or domain is absent from both the seed abstract and the repository packet. Give a short basis.
- family: a short 2-5 word scientific problem-family label. Do not use a candidate's ID or generation style as a family.

Do not infer or discuss generation conditions. Return one score object for every ID and no others."""
    rendered = "\n\n".join(f"### {item['id']}\n{item['text']}" for item in items)
    return evaluator_chat_prompt(
        f"{rubric}\n\n"
        f"SEED TITLE\n{SEED_TITLE}\n\n"
        f"SEED ABSTRACT\n{SEED_ABSTRACT}\n\n"
        f"FIXED REPOSITORY PACKET\n{packet}\n\n"
        f"CANDIDATE ITEMS\n{rendered}"
    )


def cluster_prompt(items: list[dict[str, str]]) -> str:
    rendered = "\n\n".join(f"### {item['id']}\n{item['text']}" for item in items)
    return evaluator_chat_prompt(
        "You are a condition-blind evaluator. Cluster all supplied research items into 8 to 16 "
        "substantively distinct scientific problem families. Use the same family for questions that "
        "would be answered by essentially the same experiment or explanatory variable, even when "
        "wording differs. Give each family a short descriptive name. Every supplied item ID must occur "
        "exactly once across the family item_ids arrays. "
        "Do not infer or discuss how items were generated.\n\n"
        f"ITEMS\n{rendered}"
    )


def command(
    llama_cli: Path,
    model: Path,
    prompt_path: Path,
    cache_path: Path,
    seed: int,
    schema: dict[str, object],
    n_predict: int,
) -> list[str]:
    return [
        str(llama_cli),
        "-m",
        str(model),
        "-f",
        str(prompt_path),
        "-n",
        str(n_predict),
        "-c",
        str(EVAL_SAMPLING["ctx_size"]),
        "-t",
        str(EVAL_SAMPLING["threads"]),
        "-tb",
        str(EVAL_SAMPLING["threads"]),
        "--temp",
        str(EVAL_SAMPLING["temperature"]),
        "--top-k",
        str(EVAL_SAMPLING["top_k"]),
        "--top-p",
        str(EVAL_SAMPLING["top_p"]),
        "--min-p",
        str(EVAL_SAMPLING["min_p"]),
        "--seed",
        str(seed),
        "--json-schema",
        json.dumps(schema, separators=(",", ":")),
        "--prompt-cache",
        str(cache_path),
        "--no-display-prompt",
        "--no-warmup",
        "--simple-io",
        "--log-verbosity",
        "0",
    ]


def execute_json(
    llama_cli: Path,
    model: Path,
    prompt_path: Path,
    cache_path: Path,
    seed: int,
    schema: dict[str, object],
    n_predict: int,
    output_path: Path,
    stderr_path: Path,
) -> dict[str, object]:
    result = subprocess.run(
        command(llama_cli, model, prompt_path, cache_path, seed, schema, n_predict),
        cwd=output_path.parent,
        text=True,
        capture_output=True,
        check=False,
        timeout=1200,
    )
    output_path.write_text(result.stdout, encoding="utf-8")
    stderr_path.write_text(result.stderr, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(
            f"evaluation failed with exit code {result.returncode}: {output_path}"
        )
    output = result.stdout.lstrip()
    payload, _ = json.JSONDecoder().raw_decode(output)
    return payload


def validate_scores(
    payload: dict[str, object], expected_ids: set[str]
) -> list[dict[str, object]]:
    scores = payload.get("scores")
    if not isinstance(scores, dict) or set(scores) != expected_ids:
        returned_ids = sorted(scores) if isinstance(scores, dict) else []
        raise ValueError(
            f"scorer ID mismatch: expected {sorted(expected_ids)}, got {returned_ids}"
        )
    required = set(SCORE_FIELDS)
    for item_id, score in scores.items():
        if not isinstance(score, dict) or set(score) != required:
            raise ValueError(f"invalid score fields for {item_id}")
        for key in ("utility", "seed_proximity"):
            value = score[key]
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or not 1 <= value <= 5
            ):
                raise TypeError(f"invalid {key} for {item_id}")
        for key in ("repository_attraction", "externality"):
            if not isinstance(score[key], bool):
                raise TypeError(f"invalid {key} for {item_id}")
        concepts = score["repository_concepts"]
        if not isinstance(concepts, list) or not all(
            isinstance(value, str) for value in concepts
        ):
            raise TypeError(f"invalid repository_concepts for {item_id}")
        for key in ("externality_basis", "family"):
            if not isinstance(score[key], str):
                raise TypeError(f"invalid {key} for {item_id}")
    return [{"id": item_id, **scores[item_id]} for item_id in sorted(scores)]


def validate_clusters(payload: dict[str, object], expected_ids: set[str]) -> None:
    families = payload.get("families")
    if not isinstance(families, list) or not 8 <= len(families) <= 16:
        raise ValueError("cluster assignment must contain 8 to 16 families")
    if any(
        not isinstance(family, dict)
        or set(family) != {"name", "item_ids"}
        or not isinstance(family["name"], str)
        or not family["name"].strip()
        or not isinstance(family["item_ids"], list)
        or not family["item_ids"]
        for family in families
    ):
        raise ValueError("each cluster must have a name and at least one item ID")
    assigned = [item_id for family in families for item_id in family["item_ids"]]
    if len(assigned) != len(set(assigned)) or set(assigned) != expected_ids:
        raise ValueError("cluster assignment must cover every blind ID exactly once")


def finalize_manifest(
    manifest: dict[str, object], cluster_errors: dict[str, str], completed_at: str
) -> dict[str, object]:
    manifest["completed_at"] = completed_at
    if cluster_errors:
        manifest["status"] = "completed_partial"
        manifest["invalid_measurements"] = {
            "question_family_diversity": (
                "Blind semantic clustering failed quality control and was excluded from aggregation."
            )
        }
        manifest["clustering_errors"] = cluster_errors
    else:
        manifest["status"] = "completed"
        manifest.pop("invalid_measurements", None)
        manifest.pop("clustering_errors", None)
    return manifest


def load_json_output(path: Path) -> dict[str, object]:
    payload, _ = json.JSONDecoder().raw_decode(
        path.read_text(encoding="utf-8").lstrip()
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--llama-cli", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if not args.execute:
        parser.error("refusing to evaluate without --execute")

    run_dir = args.run_dir.resolve()
    blind_dir = run_dir / "blind"
    items = [
        json.loads(line)
        for line in (blind_dir / "items.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    if len(items) != 80:
        parser.error("blind bundle must contain 80 items")
    expected_ids = {item["id"] for item in items}
    repo_root = Path(__file__).resolve().parents[3]
    packet, _ = context_packet(repo_root)
    model = args.model.resolve()
    llama_cli = args.llama_cli.resolve()

    eval_root = blind_dir / "evaluations"
    eval_root.mkdir(parents=True, exist_ok=True)
    manifest_path = eval_root / "manifest.json"
    if manifest_path.exists():
        if not args.resume:
            parser.error(
                "evaluation manifest exists; use --resume for an incomplete evaluation"
            )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("status") in ("completed", "completed_partial"):
            parser.error(f"evaluation is already finalized as {manifest['status']}")
        manifest["status"] = "running"
        manifest["completed_at"] = None
    else:
        manifest = {
            "status": "running",
            "started_at": utc_now(),
            "completed_at": None,
            "blind_item_count": len(items),
            "conditions_disclosed_to_evaluators": False,
            "predictions_disclosed_to_evaluators": False,
            "model": {
                "repo": MODEL_REPO,
                "revision": MODEL_REVISION,
                "file": MODEL_FILE,
                "file_sha256": sha256_file(model),
                "llama_cpp_revision": LLAMA_CPP_REVISION,
            },
            "sampling": EVAL_SAMPLING,
            "evaluators": EVALUATORS,
        }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    cluster_errors: dict[str, str] = {}
    for evaluator, seed_base in EVALUATORS.items():
        evaluator_dir = eval_root / evaluator
        evaluator_dir.mkdir(parents=True, exist_ok=True)
        all_scores: list[dict[str, object]] = []
        for batch_index, start in enumerate(range(0, len(items), BATCH_SIZE), start=1):
            batch = items[start : start + BATCH_SIZE]
            output_path = evaluator_dir / f"batch-{batch_index:02d}.json"
            stderr_path = evaluator_dir / f"batch-{batch_index:02d}.stderr.txt"
            prompt_path = evaluator_dir / f"batch-{batch_index:02d}.prompt.txt"
            prompt_path.write_text(score_prompt(batch, packet), encoding="utf-8")
            payload = None
            if args.resume and output_path.exists():
                try:
                    candidate = load_json_output(output_path)
                    validate_scores(candidate, {item["id"] for item in batch})
                    payload = candidate
                except (json.JSONDecodeError, TypeError, ValueError):
                    pass
            if payload is None:
                payload = execute_json(
                    llama_cli,
                    model,
                    prompt_path,
                    evaluator_dir / "score-prompt-cache.bin",
                    seed_base + batch_index,
                    score_schema({item["id"] for item in batch}),
                    EVAL_SAMPLING["n_predict"],
                    output_path,
                    stderr_path,
                )
            all_scores.extend(validate_scores(payload, {item["id"] for item in batch}))

        (evaluator_dir / "scores.jsonl").write_text(
            "".join(
                json.dumps(score, ensure_ascii=False) + "\n" for score in all_scores
            ),
            encoding="utf-8",
        )

        cluster_output = evaluator_dir / "clusters.json"
        cluster_stderr = evaluator_dir / "clusters.stderr.txt"
        cluster_prompt_path = evaluator_dir / "clusters.prompt.txt"
        cluster_prompt_path.write_text(cluster_prompt(items), encoding="utf-8")
        clusters = None
        if args.resume and cluster_output.exists():
            try:
                candidate = load_json_output(cluster_output)
                validate_clusters(candidate, expected_ids)
                clusters = candidate
            except (json.JSONDecodeError, TypeError, ValueError):
                pass
        if clusters is None:
            try:
                clusters = execute_json(
                    llama_cli,
                    model,
                    cluster_prompt_path,
                    evaluator_dir / "cluster-prompt-cache.bin",
                    seed_base + 99,
                    cluster_schema(expected_ids),
                    EVAL_SAMPLING["cluster_n_predict"],
                    cluster_output,
                    cluster_stderr,
                )
                validate_clusters(clusters, expected_ids)
            except (json.JSONDecodeError, RuntimeError, TypeError, ValueError) as error:
                cluster_errors[evaluator] = str(error)

    finalize_manifest(manifest, cluster_errors, utc_now())
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
