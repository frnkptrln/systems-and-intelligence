#!/usr/bin/env python3
"""Execute the preregistered context-attractor generation arms.

Each generation is a fresh llama.cpp process.  The context-blind arm receives
only the frozen seed and common instruction; the repository arm additionally
receives exactly the four preregistered files.  Raw stdout is never rewritten.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SEED_TITLE = (
    "Security of World-Model-Based Embodied AI: "
    "A Lifecycle of Threats, Defenses, and Evaluation"
)

SEED_ABSTRACT = """World models give embodied AI a predictive core: they compress observations into states, simulate action-conditioned futures, and enable planning beyond reactive control. This predictive layer, however, opens a new security boundary-compromise can propagate from data, sensors, prompts, or feedback into physical action.
Rather than treating world models as an isolated component, this survey traces threats across their entire lifecycle-from data construction and representation learning, through state grounding and imagination, to trajectory evaluation, execution, and long-term adaptation via memory and tools.
We show that familiar attack families: poisoning, backdoors, adversarial examples, sensor spoofing, prompt injection, trajectory manipulation, and supply-chain attacks take on distinct meanings when they corrupt world states, learned dynamics, affordance estimates, or safety costs. We also highlight a duality: world models can serve as runtime safety shields, yet when compromised or over-trusted they generate predictive safety illusions.
The survey offers a lifecycle taxonomy, maps existing attacks to world-model security properties, outlines evaluation protocols for safety failures, and structures defenses across provenance, robust grounding, uncertainty-aware prediction, trajectory gating, feedback auditing, and deployment assurance."""

COMMON_INSTRUCTION = """Read the supplied paper title and abstract. Generate exactly five distinct research questions or experiment ideas that the paper makes worth pursuing. Prefer questions that could change how we understand or test something rather than mere applications or summaries. For each item, give a short title, the question, why it is non-trivial, and one discriminating test or observation. Do not claim novelty. Do not mention this experiment or compare yourself with another condition."""

SYSTEM_PROMPT = (
    "You are a precise research assistant. Return only the requested five items."
)

CONTEXT_FILES = (
    "docs/repository-map.md",
    "meta/repository-meta/concept-registry.md",
    "ideas/README.md",
    "theory/reference/open-problems.md",
)

MODEL_REPO = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
MODEL_REVISION = "91cad51170dc346986eccefdc2dd33a9da36ead9"
MODEL_FILE = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
LLAMA_CPP_REVISION = "d5ed2b9"

ORDER_SEED = 20260811
RUN_SEEDS = tuple(2026081100 + i for i in range(1, 9))
SAMPLING = {
    "temperature": 0.8,
    "top_k": 40,
    "top_p": 0.9,
    "min_p": 0.1,
    "repeat_penalty": 1.0,
    "n_predict": 1000,
    "ctx_size": 32768,
    "threads": 8,
}

RESUME_FROZEN_KEYS = (
    "protocol",
    "seed_paper",
    "model",
    "sampling",
    "replicates_per_condition",
    "paired_run_seeds",
    "order_seed",
    "execution_order",
    "fresh_process_per_generation",
    "prompt_cache_contains_prompt_state_only",
    "context_files",
    "prompts",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def context_packet(repo_root: Path) -> tuple[str, dict[str, str]]:
    sections: list[str] = []
    hashes: dict[str, str] = {}
    for relative in CONTEXT_FILES:
        path = repo_root / relative
        data = path.read_bytes()
        text = data.decode("utf-8")
        hashes[relative] = sha256_bytes(data)
        sections.append(f"--- BEGIN {relative} ---\n{text}\n--- END {relative} ---")
    return "\n\n".join(sections), hashes


def user_prompt(condition: str, packet: str) -> str:
    pieces = [
        f"Paper title:\n{SEED_TITLE}",
        f"Paper abstract:\n{SEED_ABSTRACT}",
    ]
    if condition == "R":
        pieces.append(
            "Fixed repository context packet:\n"
            "Use this as background for the task.\n\n"
            f"{packet}"
        )
    pieces.append(f"Instruction:\n{COMMON_INSTRUCTION}")
    return "\n\n".join(pieces)


def qwen_chat_prompt(user_text: str) -> str:
    return (
        "<|im_start|>system\n"
        f"{SYSTEM_PROMPT}<|im_end|>\n"
        "<|im_start|>user\n"
        f"{user_text}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )


def run_command(
    llama_cli: Path,
    model: Path,
    prompt_path: Path,
    cache_path: Path,
    seed: int,
) -> list[str]:
    return [
        str(llama_cli),
        "-m",
        str(model),
        "-f",
        str(prompt_path),
        "-n",
        str(SAMPLING["n_predict"]),
        "-c",
        str(SAMPLING["ctx_size"]),
        "-t",
        str(SAMPLING["threads"]),
        "-tb",
        str(SAMPLING["threads"]),
        "--temp",
        str(SAMPLING["temperature"]),
        "--top-k",
        str(SAMPLING["top_k"]),
        "--top-p",
        str(SAMPLING["top_p"]),
        "--min-p",
        str(SAMPLING["min_p"]),
        "--repeat-penalty",
        str(SAMPLING["repeat_penalty"]),
        "--seed",
        str(seed),
        "--prompt-cache",
        str(cache_path),
        "--no-display-prompt",
        "--no-warmup",
        "--simple-io",
        "--log-verbosity",
        "0",
    ]


def validate_resume_manifest(
    manifest: dict[str, object], expected: dict[str, object]
) -> None:
    """Refuse a resume that would mix runs from different frozen protocols."""
    if manifest.get("status") == "completed":
        raise ValueError("generation is already finalized as completed")
    if manifest.get("status") != "running":
        raise ValueError(
            f"cannot resume manifest with status {manifest.get('status')!r}"
        )
    mismatches = [
        key for key in RESUME_FROZEN_KEYS if manifest.get(key) != expected.get(key)
    ]
    if mismatches:
        raise ValueError(
            "resume inputs differ from the frozen manifest: " + ", ".join(mismatches)
        )


def reusable_run(record: dict[str, object] | None, raw_path: Path) -> bool:
    """Return whether a recorded successful raw output is safe to reuse."""
    return bool(
        record
        and record.get("exit_code") == 0
        and raw_path.is_file()
        and record.get("raw_sha256") == sha256_file(raw_path)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--llama-cli", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    if not args.execute:
        parser.error("refusing to generate without --execute")
    model = args.model.resolve()
    llama_cli = args.llama_cli.resolve()
    if not model.is_file() or not llama_cli.is_file():
        parser.error("--model and --llama-cli must be existing files")

    repo_root = Path(__file__).resolve().parents[3]
    run_dir = args.run_dir.resolve()
    manifest_path = run_dir / "manifest.json"
    if manifest_path.exists() and not args.resume:
        parser.error(
            "run directory already has a manifest; use --resume or a new directory"
        )
    raw_dir = run_dir / "raw"
    log_dir = run_dir / "logs"
    cache_dir = run_dir / "prompt-cache"
    for path in (run_dir, raw_dir, log_dir, cache_dir):
        path.mkdir(parents=True, exist_ok=True)

    packet, context_hashes = context_packet(repo_root)
    prompts = {
        condition: qwen_chat_prompt(user_prompt(condition, packet))
        for condition in ("B", "R")
    }
    prompt_paths: dict[str, Path] = {}
    for condition in prompts:
        prompt_paths[condition] = run_dir / f"prompt-{condition}.txt"

    order = [
        (condition, replicate) for replicate in range(1, 9) for condition in ("B", "R")
    ]
    random.Random(ORDER_SEED).shuffle(order)

    expected_manifest = {
        "status": "running",
        "started_at": utc_now(),
        "completed_at": None,
        "protocol": "context-attractor preregistration, 2026-08-11",
        "seed_paper": {
            "title": SEED_TITLE,
            "arxiv": "2607.28226v1",
            "abstract_sha256": sha256_bytes(SEED_ABSTRACT.encode("utf-8")),
        },
        "model": {
            "repo": MODEL_REPO,
            "revision": MODEL_REVISION,
            "file": MODEL_FILE,
            "file_sha256": sha256_file(model),
            "local_runtime": "llama.cpp",
            "llama_cpp_revision": LLAMA_CPP_REVISION,
        },
        "sampling": SAMPLING,
        "replicates_per_condition": 8,
        "paired_run_seeds": list(RUN_SEEDS),
        "order_seed": ORDER_SEED,
        "execution_order": [
            f"{condition}{replicate:02d}" for condition, replicate in order
        ],
        "fresh_process_per_generation": True,
        "prompt_cache_contains_prompt_state_only": True,
        "context_files": context_hashes,
        "prompts": {
            condition: {
                "path": path.name,
                "sha256": sha256_bytes(prompts[condition].encode("utf-8")),
            }
            for condition, path in prompt_paths.items()
        },
        "runs": [],
    }
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        try:
            validate_resume_manifest(manifest, expected_manifest)
        except ValueError as error:
            parser.error(str(error))
        manifest["completed_at"] = None
    else:
        manifest = expected_manifest
    for condition, path in prompt_paths.items():
        path.write_text(prompts[condition], encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    existing_runs = {run["run_id"]: run for run in manifest.get("runs", [])}
    for condition, replicate in order:
        run_id = f"{condition}{replicate:02d}"
        output_path = raw_dir / f"{run_id}.md"
        stderr_path = log_dir / f"{run_id}.stderr.txt"
        if args.resume and reusable_run(existing_runs.get(run_id), output_path):
            continue
        seed = RUN_SEEDS[replicate - 1]
        command = run_command(
            llama_cli,
            model,
            prompt_paths[condition],
            cache_dir / f"{condition}.bin",
            seed,
        )
        started = utc_now()
        result = subprocess.run(
            command,
            cwd=run_dir,
            text=True,
            capture_output=True,
            check=False,
            timeout=900,
        )
        output_path.write_text(result.stdout, encoding="utf-8")
        stderr_path.write_text(result.stderr, encoding="utf-8")
        record = {
            "run_id": run_id,
            "condition": condition,
            "replicate": replicate,
            "seed": seed,
            "started_at": started,
            "completed_at": utc_now(),
            "exit_code": result.returncode,
            "raw_path": str(output_path.relative_to(run_dir)),
            "raw_sha256": sha256_file(output_path),
            "stderr_path": str(stderr_path.relative_to(run_dir)),
        }
        existing_runs[run_id] = record
        manifest["runs"] = [existing_runs[key] for key in sorted(existing_runs)]
        manifest_path.write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        if result.returncode != 0:
            raise SystemExit(f"{run_id} failed with exit code {result.returncode}")

    expected_run_ids = {f"{condition}{replicate:02d}" for condition, replicate in order}
    if set(existing_runs) != expected_run_ids:
        raise RuntimeError("generation did not produce the complete frozen run set")
    manifest["status"] = "completed"
    manifest["completed_at"] = utc_now()
    manifest["runs"] = [existing_runs[key] for key in sorted(existing_runs)]
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
