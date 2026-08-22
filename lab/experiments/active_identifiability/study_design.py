"""Validate and export the offline Active Identifiability trial manifest.

The module performs no model calls.  It turns the draft protocol into a fully
enumerated, canonicalized set of trial records so factor balance, seed pairing,
option reversal, and posterior labels can be tested before a model is selected
or the protocol is frozen.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import yaml


PROTOCOL_PATH = Path(__file__).with_name("self_report_protocol.yaml")

SYSTEM_PROMPTS = {
    "canonical_neutral": (
        "Answer the finite source-inference question using only the stated "
        "probabilities and observations."
    ),
    "neutral_paraphrase": (
        "Use the supplied probabilities and observations to answer the bounded "
        "source-inference problem."
    ),
    "analytical_tool": (
        "Act as a careful probabilistic analysis tool. Use only the supplied "
        "probabilities and observations, and apply the requested response contract."
    ),
}


def load_protocol(path: Path = PROTOCOL_PATH) -> dict[str, Any]:
    """Load the protocol mapping from YAML."""

    with path.open(encoding="utf-8") as handle:
        protocol = yaml.safe_load(handle)
    if not isinstance(protocol, dict):
        raise ValueError("protocol root must be a mapping")
    return protocol


def protocol_digest(path: Path = PROTOCOL_PATH) -> str:
    """Return the SHA-256 digest of the exact protocol bytes."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def posterior_source_a(sequence: str, task: dict[str, Any]) -> float:
    """Return the exact posterior probability of source A for ``sequence``."""

    prior_a = float(task["prior_source_a"])
    probability_red_a = float(task["probability_red_given_a"])
    probability_red_b = float(task["probability_red_given_b"])
    red_count = sequence.count("R")
    blue_count = sequence.count("B")
    if red_count + blue_count != len(sequence):
        raise ValueError(f"sequence contains an undeclared symbol: {sequence!r}")

    likelihood_a = probability_red_a**red_count * (1.0 - probability_red_a) ** blue_count
    likelihood_b = probability_red_b**red_count * (1.0 - probability_red_b) ** blue_count
    numerator = prior_a * likelihood_a
    denominator = numerator + (1.0 - prior_a) * likelihood_b
    return numerator / denominator


def posterior_bin(probability: float, task: dict[str, Any]) -> str:
    """Map a probability to the declared ordinal posterior bin."""

    for bin_spec in task["posterior_bins"]:
        lower = float(bin_spec["lower_inclusive"])
        upper_key = "upper_inclusive" if "upper_inclusive" in bin_spec else "upper_exclusive"
        upper = float(bin_spec[upper_key])
        upper_matches = probability <= upper if upper_key == "upper_inclusive" else probability < upper
        if probability >= lower and upper_matches:
            return str(bin_spec["id"])
    raise ValueError(f"probability {probability} is outside the declared bins")


def displayed_options(protocol: dict[str, Any], order: str) -> list[dict[str, str]]:
    """Return symbol-to-bin mappings in canonical or reversed presentation order."""

    contract = protocol["choice_contract"]
    symbols = [str(symbol) for symbol in contract["symbols"]]
    bins = [str(bin_id) for bin_id in contract["canonical_bins"]]
    if order == "reversed":
        bins.reverse()
    elif order != "canonical":
        raise ValueError(f"unknown presentation order: {order}")
    return [
        {"symbol": symbol, "posterior_bin": bin_id}
        for symbol, bin_id in zip(symbols, bins, strict=True)
    ]


def expected_symbol(options: list[dict[str, str]], expected_bin: str) -> str:
    """Return the displayed symbol corresponding to a canonical posterior bin."""

    matches = [option["symbol"] for option in options if option["posterior_bin"] == expected_bin]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one option for posterior bin {expected_bin!r}")
    return matches[0]


def deterministic_seed(*parts: object) -> int:
    """Derive a stable 31-bit seed from a pairing key."""

    material = "\x1f".join(str(part) for part in parts).encode("utf-8")
    return int.from_bytes(hashlib.sha256(material).digest()[:4], "big") & 0x7FFFFFFF


def _format_options(options: list[dict[str, str]]) -> str:
    return "\n".join(
        f"{option['symbol']}: {option['posterior_bin']}"
        for option in options
    )


def _response_instruction(protocol: dict[str, Any], channel: str) -> str:
    contract = protocol["choice_contract"]
    if channel == "sampled_text":
        return str(contract["sampled_text"]["instruction"])
    if channel == "forced_choice":
        return str(contract["forced_choice"]["instruction"])
    if channel == "logit_readout":
        return "Complete the final line with one symbol only.\nThe best label is"
    raise ValueError(f"unknown measurement channel: {channel}")


def _task_prompt(
    protocol: dict[str, Any],
    sequence: str,
    options: list[dict[str, str]],
    channel: str,
    context_provenance: str,
    prior_surface_symbol: str | None = None,
) -> str:
    task = protocol["source_task"]
    task_description = (
        "One of two sources was selected with equal prior probability. "
        f"Source A emits R with probability {task['probability_red_given_a']} and "
        f"Source B emits R with probability {task['probability_red_given_b']}. "
        "Emissions are conditionally independent."
    )
    if context_provenance == "grounded_evidence":
        evidence = f"The observed sequence is {sequence}."
    elif context_provenance == "transcript_initialized_mimic":
        if prior_surface_symbol is None:
            raise ValueError("the transcript mimic requires a prior surface symbol")
        evidence = (
            "The generating observations are withheld. A prior transcript ended "
            f"with the surface report FINAL={prior_surface_symbol}."
        )
    else:
        raise ValueError(f"unknown context provenance: {context_provenance}")

    prior_report = ""
    if prior_surface_symbol is not None and context_provenance == "grounded_evidence":
        prior_report = f" A prior response to these observations ended FINAL={prior_surface_symbol}."

    return (
        f"{task_description}\n{evidence}{prior_report}\n"
        "Which bin contains the posterior probability that Source A was selected?\n"
        f"{_format_options(options)}\n"
        f"{_response_instruction(protocol, channel)}"
    )


def _base_record(
    protocol: dict[str, Any],
    digest: str,
    *,
    phase: str,
    item: dict[str, Any],
    sequence: str,
    persona: str,
    channel: str,
    order: str,
    perturbation: str,
    replicate: int,
    context_provenance: str,
    seed_block: int,
    prior_surface_symbol: str | None = None,
) -> dict[str, Any]:
    task = protocol["source_task"]
    probability = posterior_source_a(sequence, task)
    expected = posterior_bin(probability, task)
    options = displayed_options(protocol, order)
    symbol = expected_symbol(options, expected)
    trial_parts = (
        phase,
        item["id"],
        persona,
        channel,
        order,
        perturbation,
        context_provenance,
        replicate,
    )
    return {
        "protocol_version": protocol["version"],
        "protocol_digest": digest,
        "model_calls_authorized": bool(protocol["model_calls_authorized"]),
        "phase": phase,
        "trial_id": "--".join(str(part) for part in trial_parts),
        "seed_block": seed_block,
        "item_id": item["id"],
        "evidence_sequence": sequence if context_provenance == "grounded_evidence" else None,
        "exact_posterior_source_a": probability if context_provenance == "grounded_evidence" else None,
        "expected_bin": expected if context_provenance == "grounded_evidence" else None,
        "persona_condition": persona,
        "measurement_channel": channel,
        "presentation_order": order,
        "perturbation": perturbation,
        "replicate": replicate,
        "context_provenance": context_provenance,
        "prior_surface_symbol": prior_surface_symbol,
        "displayed_options": options,
        "expected_display_symbol": symbol if context_provenance == "grounded_evidence" else None,
        "raw_system_prompt": SYSTEM_PROMPTS[persona],
        "raw_user_prompt": _task_prompt(
            protocol,
            sequence,
            options,
            channel,
            context_provenance,
            prior_surface_symbol,
        ),
        "response_contract": channel,
    }


def build_primary_records(protocol: dict[str, Any], digest: str) -> list[dict[str, Any]]:
    """Enumerate the balanced primary factorial design."""

    phase = protocol["primary_phase"]["factors"]
    records: list[dict[str, Any]] = []
    for item in protocol["source_task"]["items"]:
        for persona in phase["personas"]:
            for channel in phase["channels"]:
                for replicate in phase["replicates"]:
                    seed_block = deterministic_seed(
                        protocol["version"], "primary", item["id"], persona, channel, replicate
                    )
                    for perturbation in phase["perturbations"]:
                        sequence_key = (
                            "base_sequence" if perturbation == "none" else "perturbed_sequence"
                        )
                        sequence = str(item[sequence_key])
                        for order in phase["orders"]:
                            records.append(
                                _base_record(
                                    protocol,
                                    digest,
                                    phase="primary",
                                    item=item,
                                    sequence=sequence,
                                    persona=persona,
                                    channel=channel,
                                    order=order,
                                    perturbation=perturbation,
                                    replicate=int(replicate),
                                    context_provenance=str(phase["context_provenance"]),
                                    seed_block=seed_block,
                                )
                            )
    return records


def build_mimic_records(protocol: dict[str, Any], digest: str) -> list[dict[str, Any]]:
    """Enumerate the prospective transcript-mimic extension."""

    phase = protocol["mimic_extension"]
    records: list[dict[str, Any]] = []
    task = protocol["source_task"]
    for item in task["items"]:
        sequence = str(item["base_sequence"])
        expected = posterior_bin(posterior_source_a(sequence, task), task)
        for persona in phase["personas"]:
            for channel in phase["channels"]:
                for replicate in phase["replicates"]:
                    seed_block = deterministic_seed(
                        protocol["version"], "mimic", item["id"], persona, channel, replicate
                    )
                    for order in phase["orders"]:
                        options = displayed_options(protocol, str(order))
                        prior_symbol = expected_symbol(options, expected)
                        for provenance in phase["context_provenance"]:
                            records.append(
                                _base_record(
                                    protocol,
                                    digest,
                                    phase="mimic_extension",
                                    item=item,
                                    sequence=sequence,
                                    persona=persona,
                                    channel=channel,
                                    order=str(order),
                                    perturbation="none",
                                    replicate=int(replicate),
                                    context_provenance=str(provenance),
                                    seed_block=seed_block,
                                    prior_surface_symbol=prior_symbol,
                                )
                            )
    return records


def validate_protocol(protocol: dict[str, Any], path: Path = PROTOCOL_PATH) -> list[str]:
    """Return a list of structural or design errors; an empty list means valid."""

    errors: list[str] = []
    if protocol.get("status") != "draft_not_preregistered":
        errors.append("the protocol must remain explicitly draft until the PI freeze gate")
    if protocol.get("model_calls_authorized") is not False:
        errors.append("draft protocol must not authorize model calls")
    if protocol.get("model", {}).get("identifier") != "unset":
        errors.append("model selection must remain an explicit PI gate in this draft")

    task = protocol.get("source_task", {})
    declared_symbols = set(task.get("observation_symbols", []))
    expected_items = {
        "red_0_of_4": "very_low",
        "red_1_of_4": "low",
        "red_2_of_4": "even",
        "red_3_of_4": "high",
        "red_4_of_4": "very_high",
    }
    items = task.get("items", [])
    if {item.get("id") for item in items} != set(expected_items):
        errors.append("source task must contain exactly the five declared evidence levels")
    for item in items:
        for key in ("base_sequence", "perturbed_sequence"):
            sequence = str(item.get(key, ""))
            if len(sequence) != 4 or not set(sequence) <= declared_symbols:
                errors.append(f"{item.get('id')} has an invalid {key}: {sequence!r}")
        try:
            probability = posterior_source_a(str(item["base_sequence"]), task)
            actual_bin = posterior_bin(probability, task)
            if actual_bin != item.get("expected_base_bin"):
                errors.append(
                    f"{item.get('id')} expected {item.get('expected_base_bin')} but computes {actual_bin}"
                )
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"{item.get('id')} posterior validation failed: {exc}")

    contract = protocol.get("choice_contract", {})
    symbols = [str(symbol) for symbol in contract.get("symbols", [])]
    bins = [str(bin_id) for bin_id in contract.get("canonical_bins", [])]
    if len(symbols) != 5 or len(set(symbols)) != 5:
        errors.append("choice symbols must contain five unique values")
    if len(bins) != 5 or len(set(bins)) != 5:
        errors.append("canonical bins must contain five unique values")
    enum = (
        contract.get("forced_choice", {})
        .get("json_schema", {})
        .get("properties", {})
        .get("choice", {})
        .get("enum", [])
    )
    if enum != contract.get("symbols"):
        errors.append("JSON-schema enum must enumerate the exact choice symbols")
    if any("|" in str(value) for value in enum):
        errors.append("union-style placeholder strings are forbidden in the response schema")

    if not errors:
        digest = protocol_digest(path)
        primary = build_primary_records(protocol, digest)
        mimic = build_mimic_records(protocol, digest)
        if len(primary) != int(protocol["primary_phase"]["expected_records"]):
            errors.append("primary manifest count does not match the declared count")
        if len(mimic) != int(protocol["mimic_extension"]["expected_records"]):
            errors.append("mimic manifest count does not match the declared count")
        if any(record["model_calls_authorized"] for record in primary + mimic):
            errors.append("an exported draft record unexpectedly authorizes model calls")
    return errors


def build_manifest(
    protocol: dict[str, Any],
    *,
    phase: str = "all",
    path: Path = PROTOCOL_PATH,
) -> list[dict[str, Any]]:
    """Build a validated manifest for ``primary``, ``mimic``, or ``all``."""

    errors = validate_protocol(protocol, path)
    if errors:
        raise ValueError("invalid protocol:\n- " + "\n- ".join(errors))
    digest = protocol_digest(path)
    if phase == "primary":
        return build_primary_records(protocol, digest)
    if phase == "mimic":
        return build_mimic_records(protocol, digest)
    if phase == "all":
        return build_primary_records(protocol, digest) + build_mimic_records(protocol, digest)
    raise ValueError(f"unknown phase: {phase}")


def manifest_summary(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Return exact factor counts for an iterable of records."""

    materialized = list(records)
    factor_names = (
        "phase",
        "persona_condition",
        "measurement_channel",
        "presentation_order",
        "perturbation",
        "context_provenance",
    )
    return {
        "records": len(materialized),
        "model_calls_authorized": any(
            bool(record["model_calls_authorized"]) for record in materialized
        ),
        "counts": {
            factor: dict(sorted(Counter(record[factor] for record in materialized).items()))
            for factor in factor_names
        },
    }


def write_jsonl(records: Iterable[dict[str, Any]], output: Path) -> None:
    """Write canonical one-record-per-line JSON without mutating the protocol."""

    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(record, sort_keys=True) for record in records]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=PROTOCOL_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="validate structure, counts, and safety gates")
    summary = subparsers.add_parser("summary", help="print exact manifest factor counts")
    summary.add_argument("--phase", choices=("primary", "mimic", "all"), default="all")
    export = subparsers.add_parser("export", help="write the offline JSONL trial manifest")
    export.add_argument("--phase", choices=("primary", "mimic", "all"), default="all")
    export.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    protocol = load_protocol(args.protocol)
    errors = validate_protocol(protocol, args.protocol)
    if errors:
        raise SystemExit("FAIL\n- " + "\n- ".join(errors))
    if args.command == "validate":
        print(
            "PASS: draft protocol is balanced, model calls are disabled, "
            "and all declared controls validate."
        )
        return

    records = build_manifest(protocol, phase=args.phase, path=args.protocol)
    if args.command == "summary":
        print(json.dumps(manifest_summary(records), indent=2, sort_keys=True))
        return
    write_jsonl(records, args.output)
    print(f"Wrote {len(records)} offline trial records to {args.output}")


if __name__ == "__main__":
    main()
