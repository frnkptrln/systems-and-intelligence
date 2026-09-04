"""Pure safety and parsing contract for the Active Identifiability smoke runner.

This module performs no model calls and imports no model runtime. It is kept
separate so CI can verify the execution boundary, parser, and artifact summary
without installing torch or transformers.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable
import re


def execution_protocol_errors(protocol: dict[str, Any]) -> list[str]:
    """Return every reason the protocol must not be executed."""

    errors: list[str] = []
    if protocol.get("status") != "frozen_smoke_authorized":
        errors.append("status is not frozen_smoke_authorized")
    if protocol.get("model_calls_authorized") is not True:
        errors.append("model_calls_authorized is not true")
    if protocol.get("authorized_phase") != "smoke":
        errors.append("only the smoke phase may be authorized")

    model = protocol.get("model", {})
    for field in ("identifier", "revision", "chat_template_sha256"):
        value = str(model.get(field, "")).strip()
        if not value or value == "unset":
            errors.append(f"model.{field} is not pinned")

    symbols = [str(value) for value in protocol.get("choice_contract", {}).get("symbols", [])]
    token_ids = model.get("choice_token_ids", {})
    if set(token_ids) != set(symbols):
        errors.append("choice token ids do not cover the declared symbols")

    gate = protocol.get("gates", {}).get("smoke", {})
    if gate.get("phase") != "primary":
        errors.append("smoke gate must select the primary phase")
    if set(gate.get("channels", [])) - {"sampled_text", "forced_choice"}:
        errors.append("smoke gate contains an undeclared execution channel")
    expected = gate.get("expected_records")
    if not isinstance(expected, int) or expected <= 0 or expected > 50:
        errors.append("smoke gate size is missing or exceeds the bounded maximum")
    return errors


def select_smoke_records(
    records: Iterable[dict[str, Any]], protocol: dict[str, Any]
) -> list[dict[str, Any]]:
    """Select only the subset named by the frozen smoke gate."""

    gate = protocol["gates"]["smoke"]
    return [
        record
        for record in records
        if record["phase"] == gate["phase"]
        and record["replicate"] in gate["replicates"]
        and record["persona_condition"] in gate["personas"]
        and record["measurement_channel"] in gate["channels"]
        and record["presentation_order"] in gate["orders"]
        and record["perturbation"] in gate["perturbations"]
    ]


def parse_output(channel: str, raw_output: str) -> tuple[str | None, str, str | None]:
    """Parse an output without repairing its substantive choice."""

    stripped = raw_output.strip()
    if channel == "sampled_text":
        first_line = stripped.splitlines()[0] if stripped else ""
        match = re.fullmatch(r"([A-E])", first_line)
        if match is None:
            return None, "invalid", "missing_exact_first_line_symbol"
        return match.group(1), "explicit_first_line_symbol", None

    if channel == "forced_choice":
        if re.fullmatch(r"[A-E]", stripped) is None:
            return None, "invalid", "not_single_choice_symbol"
        return stripped, "choice_restricted_single_token", None

    raise ValueError(f"the smoke parser does not accept channel {channel!r}")


def parsed_symbol_counts(records: Iterable[dict[str, Any]]) -> dict[str, int]:
    """Return JSON-stable counts for valid symbols and invalid outputs."""

    counts = Counter(
        record["parsed_symbol"] if record["parsed_symbol"] is not None else "<invalid>"
        for record in records
    )
    return dict(sorted(counts.items()))


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize the smoke records without introducing non-string JSON keys."""

    by_channel: dict[str, dict[str, Any]] = {}
    for channel in sorted({str(record["measurement_channel"]) for record in records}):
        subset = [record for record in records if record["measurement_channel"] == channel]
        invalid = sum(record["invalid_reason"] is not None for record in subset)
        valid = len(subset) - invalid
        correct = sum(record["matches_expected_bin"] is True for record in subset)
        by_channel[channel] = {
            "records": len(subset),
            "valid": valid,
            "invalid": invalid,
            "invalid_rate": invalid / len(subset),
            "correct_exact_bin": correct,
            "accuracy_among_valid": correct / valid if valid else None,
            "parsed_symbols": parsed_symbol_counts(subset),
        }
    return {
        "records": len(records),
        "valid": sum(record["invalid_reason"] is None for record in records),
        "invalid": sum(record["invalid_reason"] is not None for record in records),
        "channels": by_channel,
        "smoke_gate_pass": all(
            channel["invalid_rate"] <= 0.10 for channel in by_channel.values()
        ),
    }
