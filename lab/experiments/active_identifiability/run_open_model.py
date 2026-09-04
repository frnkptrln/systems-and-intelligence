#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "accelerate>=1.0",
#   "huggingface-hub>=0.30",
#   "jinja2>=3.1",
#   "pyyaml>=6.0",
#   "safetensors>=0.4",
#   "torch>=2.7",
#   "transformers>=5.5,<6",
# ]
# ///
"""Execute the explicitly authorized Active Identifiability smoke gate.

The Hugging Face Jobs connector executes scripts without a repository checkout.
This entry point therefore accepts either an inline bundle root or downloads
the frozen protocol and manifest builder from the same pinned git commit
supplied with ``--source-ref``. It refuses every phase except the 20-record
smoke subset.

The complete result is emitted as a gzip-compressed base64 artifact in the job
log. Committing this runner does not authorize a model call: the pinned protocol
must separately declare the bounded smoke phase as frozen and authorized.
"""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
from types import ModuleType
from typing import Any
from urllib.request import Request, urlopen

import torch
import transformers
from huggingface_hub import HfApi
from transformers import AutoModelForCausalLM, AutoTokenizer


_HELPER_DIR = Path(__file__).resolve().parent
if str(_HELPER_DIR) not in sys.path:
    sys.path.insert(0, str(_HELPER_DIR))
from smoke_contract import execution_protocol_errors, parse_output, select_smoke_records, summarize


REPOSITORY = "frnkptrln/systems-and-intelligence"
EXPERIMENT_ROOT = "lab/experiments/active_identifiability"
STUDY_PATH = f"{EXPERIMENT_ROOT}/study_design.py"
PROTOCOL_PATH = f"{EXPERIMENT_ROOT}/self_report_protocol.yaml"
def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "active-identifiability-smoke/0.1"})
    with urlopen(request, timeout=120) as response:
        return response.read()


def raw_url(source_ref: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{REPOSITORY}/{source_ref}/{path}"


def load_frozen_sources(
    source_ref: str, bundle_root: Path | None
) -> tuple[ModuleType, dict[str, Any], Path, dict[str, str]]:
    root = Path(tempfile.mkdtemp(prefix="active-identifiability-"))
    study_path = root / "study_design.py"
    protocol_path = root / "self_report_protocol.yaml"
    if bundle_root is None:
        study_bytes = fetch_bytes(raw_url(source_ref, STUDY_PATH))
        protocol_bytes = fetch_bytes(raw_url(source_ref, PROTOCOL_PATH))
    else:
        study_bytes = (bundle_root / STUDY_PATH).read_bytes()
        protocol_bytes = (bundle_root / PROTOCOL_PATH).read_bytes()
    study_path.write_bytes(study_bytes)
    protocol_path.write_bytes(protocol_bytes)

    spec = importlib.util.spec_from_file_location("frozen_study_design", study_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the frozen study design")
    study = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(study)
    protocol = study.load_protocol(protocol_path)
    source_hashes = {
        STUDY_PATH: hashlib.sha256(study_bytes).hexdigest(),
        PROTOCOL_PATH: hashlib.sha256(protocol_bytes).hexdigest(),
    }
    return study, protocol, protocol_path, source_hashes


def render_prompt(tokenizer: Any, record: dict[str, Any], thinking_enabled: bool) -> str:
    messages = [
        {"role": "system", "content": record["raw_system_prompt"]},
        {"role": "user", "content": record["raw_user_prompt"]},
    ]
    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=thinking_enabled,
    )


def tokenizer_gate(
    tokenizer: Any,
    protocol: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    model_spec = protocol["model"]
    expected_hash = str(model_spec["chat_template_sha256"])
    actual_hash = hashlib.sha256((tokenizer.chat_template or "").encode()).hexdigest()
    thinking_enabled = bool(model_spec["thinking_enabled"])
    expected_token_ids = {
        str(symbol): int(token_id)
        for symbol, token_id in model_spec["choice_token_ids"].items()
    }
    symbol_results: dict[str, dict[str, Any]] = {}

    representative = records[0]
    rendered = render_prompt(tokenizer, representative, thinking_enabled)
    prefix_ids = tokenizer(rendered, add_special_tokens=False).input_ids
    for symbol, expected_id in expected_token_ids.items():
        full_ids = tokenizer(rendered + symbol, add_special_tokens=False).input_ids
        stable = full_ids[: len(prefix_ids)] == prefix_ids
        suffix = full_ids[len(prefix_ids) :] if stable else []
        actual_id = suffix[0] if len(suffix) == 1 else None
        symbol_results[symbol] = {
            "expected_token_id": expected_id,
            "actual_token_id": actual_id,
            "exact_prefix_stable": stable,
            "single_token": len(suffix) == 1,
            "pass": stable and len(suffix) == 1 and actual_id == expected_id,
        }

    return {
        "tokenizer_class": type(tokenizer).__name__,
        "expected_chat_template_sha256": expected_hash,
        "actual_chat_template_sha256": actual_hash,
        "thinking_enabled": thinking_enabled,
        "symbols": symbol_results,
        "pass": actual_hash == expected_hash
        and all(result["pass"] for result in symbol_results.values()),
    }


def run_trial(
    model: Any,
    tokenizer: Any,
    record: dict[str, Any],
    protocol: dict[str, Any],
    device: torch.device,
    parse_output_fn: Any,
) -> dict[str, Any]:
    generation = protocol["execution"]["generation"]
    channel = str(record["measurement_channel"])
    rendered = render_prompt(tokenizer, record, bool(protocol["model"]["thinking_enabled"]))
    inputs = tokenizer(rendered, return_tensors="pt", add_special_tokens=False).to(device)
    seed = int(record["seed_block"])
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    raw_choice_logits: dict[str, float] | None = None
    if channel == "forced_choice":
        symbols = [str(symbol) for symbol in protocol["choice_contract"]["symbols"]]
        token_ids = [int(protocol["model"]["choice_token_ids"][symbol]) for symbol in symbols]
        with torch.inference_mode():
            next_token_logits = model(**inputs).logits[0, -1]
        candidate_logits = next_token_logits[token_ids].float().cpu()
        raw_choice_logits = {
            symbol: float(logit) for symbol, logit in zip(symbols, candidate_logits, strict=True)
        }
        probabilities = torch.softmax(
            candidate_logits / float(generation["temperature"]), dim=-1
        )
        selected_index = int(torch.multinomial(probabilities, 1).item())
        raw_output = symbols[selected_index]
    elif channel == "sampled_text":
        with torch.inference_mode():
            generated = model.generate(
                **inputs,
                do_sample=bool(generation["do_sample"]),
                temperature=float(generation["temperature"]),
                top_p=float(generation["top_p"]),
                repetition_penalty=float(generation["repetition_penalty"]),
                max_new_tokens=int(generation["sampled_text_max_new_tokens"]),
                pad_token_id=tokenizer.eos_token_id,
            )
        generated_ids = generated[0, inputs["input_ids"].shape[1] :]
        raw_output = tokenizer.decode(generated_ids, skip_special_tokens=True)
    else:
        raise ValueError(f"the smoke runner does not execute channel {channel!r}")

    symbol, parser_route, invalid_reason = parse_output_fn(channel, raw_output)
    canonical_map = {
        option["symbol"]: option["posterior_bin"] for option in record["displayed_options"]
    }
    canonical_bin = canonical_map.get(symbol) if symbol is not None else None

    return {
        **record,
        "model_id": protocol["model"]["identifier"],
        "model_revision": protocol["model"]["revision"],
        "chat_template_hash": protocol["model"]["chat_template_sha256"],
        "raw_output": raw_output,
        "raw_choice_logits_if_applicable": raw_choice_logits,
        "parsed_symbol": symbol,
        "canonical_bin": canonical_bin,
        "parser_route": parser_route,
        "invalid_reason": invalid_reason,
        "seed_if_available": seed,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "matches_expected_bin": (
            canonical_bin == record["expected_bin"] if canonical_bin is not None else None
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-ref", required=True, help="Pinned git commit SHA")
    parser.add_argument(
        "--bundle-root",
        type=Path,
        help="Optional root containing the pinned study and protocol files",
    )
    parser.add_argument("--phase", choices=("smoke",), default="smoke")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.source_ref):
        raise SystemExit("--source-ref must be a full 40-character commit SHA")

    study, protocol, protocol_path, source_hashes = load_frozen_sources(
        args.source_ref, args.bundle_root
    )
    execution_errors = execution_protocol_errors(protocol)
    if execution_errors:
        raise SystemExit("execution protocol is not authorized: " + "; ".join(execution_errors))
    if protocol.get("authorized_phase") != "smoke":
        raise SystemExit("the pinned protocol does not authorize the smoke phase")
    primary = study.build_primary_records(protocol, study.protocol_digest(protocol_path))
    smoke_records = select_smoke_records(primary, protocol)
    expected_records = int(protocol["gates"]["smoke"]["expected_records"])
    if len(smoke_records) != expected_records:
        raise SystemExit(
            f"refusing unexpected smoke size: {len(smoke_records)} != {expected_records}"
        )
    if not all(record["model_calls_authorized"] for record in smoke_records):
        raise SystemExit("at least one selected smoke record lacks call authorization")

    model_id = str(protocol["model"]["identifier"])
    revision = str(protocol["model"]["revision"])
    resolved_revision = HfApi().model_info(model_id, revision=revision).sha
    if resolved_revision != revision:
        raise SystemExit(f"resolved revision {resolved_revision} differs from pinned {revision}")

    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    gate = tokenizer_gate(tokenizer, protocol, smoke_records)
    if not gate["pass"]:
        raise SystemExit("tokenizer gate failed: " + json.dumps(gate, sort_keys=True))

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        dtype=torch.bfloat16,
        device_map="auto",
    )
    model.eval()
    device = next(model.parameters()).device

    measured = [
        run_trial(model, tokenizer, record, protocol, device, parse_output)
        for record in smoke_records
    ]
    summary = summarize(measured)
    artifact = {
        "artifact_version": "1.0",
        "experiment": "active_identifiability_multi_readout",
        "phase": "smoke",
        "source_repository": REPOSITORY,
        "source_commit": args.source_ref,
        "source_transport": "inline_bundle" if args.bundle_root else "raw_git",
        "source_file_sha256": source_hashes,
        "protocol_digest": study.protocol_digest(protocol_path),
        "model": {
            "identifier": model_id,
            "requested_revision": revision,
            "resolved_revision": resolved_revision,
            "dtype": str(next(model.parameters()).dtype),
            "device": str(device),
        },
        "environment": {
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "cuda_available": torch.cuda.is_available(),
            "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        },
        "tokenizer_gate": gate,
        "summary": summary,
        "records": measured,
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }
    raw = json.dumps(artifact, ensure_ascii=False, sort_keys=True).encode()
    compressed = gzip.compress(raw, mtime=0)
    print("ACTIVE_IDENTIFIABILITY_SUMMARY=" + json.dumps(summary, sort_keys=True))
    print("ACTIVE_IDENTIFIABILITY_ARTIFACT_SHA256=" + hashlib.sha256(raw).hexdigest())
    print(
        "ACTIVE_IDENTIFIABILITY_ARTIFACT_GZIP_BASE64="
        + base64.b64encode(compressed).decode()
    )


if __name__ == "__main__":
    main()
