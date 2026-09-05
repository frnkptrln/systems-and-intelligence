"""Exact static controls: source order, reconstructing coalitions and known erasures."""

import importlib.util
import json
from math import isclose
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "lab/experiments/collective-agency-control"
SPEC = importlib.util.spec_from_file_location(
    "collective_information_distribution", CONTROL / "information_distribution.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

# Collect the seven original mathematical calibration tests in the normal CI suite.
TestOriginalCalibration = MODULE.CalibrationTests


def assert_equivalent(actual, expected):
    """Pin structure exactly and transcendental floating-point values to tolerance."""
    if isinstance(expected, float):
        assert isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12)
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            assert_equivalent(actual[key], expected[key])
    elif isinstance(expected, list):
        assert len(actual) == len(expected)
        for left, right in zip(actual, expected):
            assert_equivalent(left, right)
    else:
        assert actual == expected


def test_result_reproduces_committed_static_calibration():
    expected = json.loads((CONTROL / "information-distribution-result.json").read_text())
    actual = MODULE.run()
    assert_equivalent(actual, expected)
    assert sum(case["equiprobable_states"] for case in actual["cases"]) == 180


def test_minimal_coalitions_and_all_subset_accuracies():
    expected = {
        "broadcast": [[1], [2], [3]],
        "hub_essential": [[1, 2], [1, 3]],
        "two_of_three": [[1, 2], [1, 3], [2, 3]],
        "three_of_three": [[1, 2, 3]],
    }
    keys = {"empty", "1", "2", "3", "1,2", "1,3", "2,3", "1,2,3"}
    for name, minimal in expected.items():
        result = MODULE.summarize(name)
        assert result["minimal_reconstructing_coalitions"] == minimal
        profile = result["coalition_optimal_decoding_accuracy"]
        assert profile.keys() == keys
        for key, accuracy in profile.items():
            observed = set() if key == "empty" else set(map(int, key.split(",")))
            reconstructs = any(set(group) <= observed for group in minimal)
            assert accuracy == (1.0 if reconstructs else 1 / MODULE.PRIME)


def test_three_way_information_is_not_visible_in_any_pair():
    result = MODULE.summarize("three_of_three")
    assert isclose(result["joint_target_information_bits"], result["target_entropy_bits"])
    for pair in result["pair_pid_imin"].values():
        assert pair["joint_information_bits"] == 0.0
        assert pair["synergy_bits"] == 0.0
    assert result["minimal_reconstructing_coalitions"] == [[1, 2, 3]]


def test_per_location_results_not_only_average_or_worst_case():
    expected = {
        "broadcast": [1.0, 1.0, 1.0],
        "hub_essential": [0.2, 1.0, 1.0],
        "two_of_three": [1.0, 1.0, 1.0],
        "three_of_three": [0.2, 0.2, 0.2],
    }
    for name, accuracies in expected.items():
        result = MODULE.summarize(name)
        assert [case["erased_component"] for case in result["known_erasures"]] == [1, 2, 3]
        assert [case["optimal_decoding_accuracy"] for case in result["known_erasures"]] == accuracies
        assert result["worst_single_erasure_accuracy"] == min(accuracies)
        assert isclose(result["uniform_single_erasure_accuracy"], sum(accuracies) / 3)
