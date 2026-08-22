import json
from collections import defaultdict
from pathlib import Path

import pytest

from lab.experiments.active_identifiability.causal_witness import (
    best_cost_adjusted_intervention,
    information_gain_bits,
    observationally_equivalent,
    posterior_probability_a,
    run_reference_experiment,
)
from lab.experiments.active_identifiability.study_design import (
    PROTOCOL_PATH,
    build_manifest,
    displayed_options,
    load_protocol,
    posterior_bin,
    posterior_source_a,
    validate_protocol,
)


REFERENCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "lab"
    / "experiments"
    / "active_identifiability"
    / "results"
    / "causal_reference.json"
)


def test_causal_witness_reference_values() -> None:
    assert observationally_equivalent()
    expected = {
        0.0: 0.0396841323,
        1.0: 0.1400454032,
        2.0: 0.3799611638,
        3.0: 0.6338353789,
    }
    for intervention, target in expected.items():
        assert information_gain_bits(intervention) == pytest.approx(target, abs=1e-9)
    assert information_gain_bits(3.0) == pytest.approx(information_gain_bits(-3.0), abs=1e-9)


def test_causal_witness_posterior_and_cost_optimum() -> None:
    intervention, utility = best_cost_adjusted_intervention()
    assert intervention == pytest.approx(2.5504, abs=1e-3)
    assert utility == pytest.approx(0.199799, abs=1e-6)
    assert posterior_probability_a(3.0, 3.0) == pytest.approx(0.9306407359, abs=1e-9)
    assert posterior_probability_a(3.0, 0.0) == pytest.approx(0.0154674916, abs=1e-9)
    assert posterior_probability_a(3.0, -1.0) == pytest.approx(0.0006087911, abs=1e-9)


def test_committed_causal_result_matches_executable() -> None:
    committed = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    measured = run_reference_experiment()
    assert committed["observationally_equivalent"] is measured["observationally_equivalent"]
    assert committed["observational_covariance"] == measured["observational_covariance"]
    for expected, actual in zip(
        committed["interventions"], measured["interventions"], strict=True
    ):
        assert expected["x"] == actual["x"]
        assert expected["information_gain_bits"] == pytest.approx(
            actual["information_gain_bits"], abs=1e-12
        )
        assert expected["expected_posterior_entropy_bits"] == pytest.approx(
            actual["expected_posterior_entropy_bits"], abs=1e-12
        )
    assert committed["cost_adjusted"]["best_x"] == pytest.approx(
        measured["cost_adjusted"]["best_x"], abs=1e-8
    )
    assert committed["cost_adjusted"]["best_utility_bits"] == pytest.approx(
        measured["cost_adjusted"]["best_utility_bits"], abs=1e-10
    )


def test_draft_protocol_validates_and_disables_calls() -> None:
    protocol = load_protocol()
    assert validate_protocol(protocol) == []
    assert protocol["status"] == "draft_not_preregistered"
    assert protocol["model"]["identifier"] == "unset"
    assert protocol["model_calls_authorized"] is False


def test_exact_posterior_levels_cover_all_declared_bins() -> None:
    protocol = load_protocol()
    task = protocol["source_task"]
    observed = {}
    for item in task["items"]:
        probability = posterior_source_a(item["base_sequence"], task)
        observed[item["id"]] = posterior_bin(probability, task)
    assert observed == {
        "red_0_of_4": "very_low",
        "red_1_of_4": "low",
        "red_2_of_4": "even",
        "red_3_of_4": "high",
        "red_4_of_4": "very_high",
    }


def test_manifest_counts_and_factor_balance() -> None:
    protocol = load_protocol()
    records = build_manifest(protocol)
    primary = [record for record in records if record["phase"] == "primary"]
    mimic = [record for record in records if record["phase"] == "mimic_extension"]
    assert len(records) == 960
    assert len(primary) == 720
    assert len(mimic) == 240
    assert all(record["model_calls_authorized"] is False for record in records)

    for channel in ("sampled_text", "forced_choice", "logit_readout"):
        assert sum(record["measurement_channel"] == channel for record in primary) == 240
    for order in ("canonical", "reversed"):
        assert sum(record["presentation_order"] == order for record in primary) == 360
    for perturbation in ("none", "flip_one_observation"):
        assert sum(record["perturbation"] == perturbation for record in primary) == 360


def test_primary_order_and_perturbation_pairs_share_seed_blocks() -> None:
    records = build_manifest(load_protocol(), phase="primary")
    groups = defaultdict(list)
    for record in records:
        key = (
            record["item_id"],
            record["persona_condition"],
            record["measurement_channel"],
            record["replicate"],
        )
        groups[key].append(record)

    assert len(groups) == 5 * 3 * 3 * 4
    for group in groups.values():
        assert len(group) == 4
        assert {record["presentation_order"] for record in group} == {
            "canonical",
            "reversed",
        }
        assert {record["perturbation"] for record in group} == {
            "none",
            "flip_one_observation",
        }
        assert len({record["seed_block"] for record in group}) == 1


def test_reversal_changes_symbols_not_canonical_bins() -> None:
    protocol = load_protocol()
    canonical = displayed_options(protocol, "canonical")
    reversed_options = displayed_options(protocol, "reversed")
    assert [item["posterior_bin"] for item in canonical] == list(
        reversed([item["posterior_bin"] for item in reversed_options])
    )
    assert [item["symbol"] for item in canonical] == [
        item["symbol"] for item in reversed_options
    ]


def test_mimic_extension_pairs_provenance_without_claiming_ground_truth() -> None:
    records = build_manifest(load_protocol(), phase="mimic")
    groups = defaultdict(list)
    for record in records:
        key = (
            record["item_id"],
            record["measurement_channel"],
            record["presentation_order"],
            record["replicate"],
        )
        groups[key].append(record)

    assert len(groups) == 5 * 3 * 2 * 4
    for group in groups.values():
        assert len(group) == 2
        assert {record["context_provenance"] for record in group} == {
            "grounded_evidence",
            "transcript_initialized_mimic",
        }
        assert len({record["seed_block"] for record in group}) == 1
        assert len({record["prior_surface_symbol"] for record in group}) == 1
        mimic = next(
            record
            for record in group
            if record["context_provenance"] == "transcript_initialized_mimic"
        )
        assert mimic["evidence_sequence"] is None
        assert mimic["exact_posterior_source_a"] is None
        assert mimic["expected_bin"] is None
        assert mimic["expected_display_symbol"] is None


def test_forced_choice_schema_uses_real_enum_values() -> None:
    protocol = load_protocol(PROTOCOL_PATH)
    enum = protocol["choice_contract"]["forced_choice"]["json_schema"]["properties"][
        "choice"
    ]["enum"]
    assert enum == ["A", "B", "C", "D", "E"]
    assert all("|" not in value for value in enum)
