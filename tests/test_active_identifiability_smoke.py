import json
from pathlib import Path

from lab.experiments.active_identifiability.smoke_contract import (
    execution_protocol_errors,
    parse_output,
    select_smoke_records,
    summarize,
)
from lab.experiments.active_identifiability.study_design import (
    build_manifest,
    load_protocol,
)


REPO = Path(__file__).resolve().parents[1]
RUNNER = (
    REPO
    / "lab"
    / "experiments"
    / "active_identifiability"
    / "run_open_model.py"
)


def test_current_draft_cannot_cross_execution_boundary() -> None:
    errors = execution_protocol_errors(load_protocol())
    assert errors
    assert "status is not frozen_smoke_authorized" in errors
    assert "model_calls_authorized is not true" in errors


def test_draft_manifest_selects_exact_declared_smoke_shape_offline() -> None:
    protocol = load_protocol()
    primary = build_manifest(protocol, phase="primary")
    selected = select_smoke_records(primary, protocol)
    assert len(selected) == protocol["gates"]["smoke"]["expected_records"] == 20
    assert {record["measurement_channel"] for record in selected} == {
        "sampled_text",
        "forced_choice",
    }
    assert all(record["model_calls_authorized"] is False for record in selected)


def test_parser_preserves_invalid_outputs() -> None:
    assert parse_output("sampled_text", "A\nBecause...") == (
        "A",
        "explicit_first_line_symbol",
        None,
    )
    assert parse_output("sampled_text", "The answer is A") == (
        None,
        "invalid",
        "missing_exact_first_line_symbol",
    )
    assert parse_output("forced_choice", "E") == (
        "E",
        "choice_restricted_single_token",
        None,
    )
    assert parse_output("forced_choice", '{"choice":"E"}') == (
        None,
        "invalid",
        "not_single_choice_symbol",
    )


def test_summary_is_canonical_json_with_invalid_bucket() -> None:
    records = [
        {
            "measurement_channel": "forced_choice",
            "parsed_symbol": "A",
            "invalid_reason": None,
            "matches_expected_bin": True,
        },
        {
            "measurement_channel": "forced_choice",
            "parsed_symbol": None,
            "invalid_reason": "not_single_choice_symbol",
            "matches_expected_bin": None,
        },
    ]
    summary = summarize(records)
    assert summary["channels"]["forced_choice"]["parsed_symbols"] == {
        "<invalid>": 1,
        "A": 1,
    }
    assert summary["smoke_gate_pass"] is False
    json.dumps(summary, sort_keys=True)


def test_recovered_runner_compiles_and_avoids_historical_global() -> None:
    source = RUNNER.read_text(encoding="utf-8")
    compile(source, str(RUNNER), "exec")
    assert "study.parsed_symbol_counts" not in source
    assert "study.select_smoke_records" not in source
