import importlib.util
import json
import math
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "budget_check", ROOT / "lab/benchmarks/collective-agency/intervention_budget_check.py"
)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def test_closed_form_counterexample_and_frozen_gate():
    result = check.report()
    assert result["result"]["coherence"] == pytest.approx(math.sqrt(2) / 2)
    assert result["result"]["macro_budget_rad"] == pytest.approx(2 * math.pi)
    assert result["same_strength_half_control_budget_rad"] == pytest.approx(math.pi)
    assert result["result"]["one_oscillator_match_feasible"] is False
    assert result["implementation_authorized"] is False
    assert result["execution_authorized"] is False


def test_budget_is_invariant_to_rotations_and_full_turns():
    phases = [.2, -.3, .4, -.1]
    expected = check.contraction_budget(phases, .5)["macro_budget_rad"]
    shifted = [x + 1.9 + i * 2 * math.pi for i, x in enumerate(phases)]
    assert check.contraction_budget(shifted, .5)["macro_budget_rad"] == pytest.approx(expected)
    assert check.contraction_budget(phases, 0)["macro_budget_rad"] == 0
    assert check.contraction_budget(phases, .5)["one_oscillator_match_feasible"]


def test_undefined_mean_cannot_silently_choose_an_intervention():
    with pytest.raises(ValueError, match="undefined"):
        check.contraction_budget([0, math.pi], .5)


def test_half_support_capacity_is_a_necessary_and_sufficient_bound():
    # Mean zero, with unequal support and complement contraction capacities.
    phases = [0, 0, math.pi / 4, -math.pi / 4]
    limits = check.matching_capacity(phases, [0, 2])
    assert limits["full_contraction_capacity_rad"] == pytest.approx(math.pi / 2)
    assert limits["support_contraction_capacity_rad"] == pytest.approx(math.pi / 4)
    assert limits["common_budget_max_rad"] == pytest.approx(math.pi / 4)
    # A constructive witness for every budget in the claimed closed interval:
    # macro and half may use different strengths, but neither exceeds one.
    for fraction in (0, .25, .5, 1):
        budget = fraction * limits["common_budget_max_rad"]
        macro_strength = budget / limits["full_contraction_capacity_rad"]
        half_strength = budget / limits["support_contraction_capacity_rad"]
        assert 0 <= macro_strength <= 1 and 0 <= half_strength <= 1
        assert check.contraction_budget(phases, macro_strength)["macro_budget_rad"] == pytest.approx(budget)
        half_displacements = check.contraction_budget(phases, half_strength)["component_displacements_rad"]
        assert sum(half_displacements[i] for i in [0, 2]) == pytest.approx(budget)
        assert abs(check.wrap(budget)) == pytest.approx(budget)
    assert check.matching_capacity(phases, [0, 1])["common_budget_max_rad"] == 0
    assert check.matching_capacity([0, 0, 0, 0], [0, 1])["common_budget_max_rad"] == 0
    assert check.matching_capacity([math.pi / 4] * 8 + [-math.pi / 4] * 8,
                                   list(range(8)))["common_budget_max_rad"] == pytest.approx(math.pi)


def test_cap_cannot_repair_every_half_at_positive_coherence():
    result = check.report()["half_control_feasibility"]
    original = result["original_fixture"]
    assert original["supports_unable_to_match_requested_budget"] == math.comb(16, 8)
    assert original["supports_unable_to_match_proposed_capped_budget"] == 0
    aligned = result["aligned_half_fixture"]
    assert aligned["coherence"] == pytest.approx((1 + math.sqrt(2) / 2) / 2)
    assert aligned["requested_macro_budget_rad"] == pytest.approx(math.pi)
    assert aligned["half_supports"] == math.comb(16, 8)
    # A half containing k of the eight off-mean phases has capacity k*pi/4.
    # There are C(8,k)*C(8,8-k) such halves, independent of the enumerator.
    assert aligned["supports_unable_to_match_requested_budget"] == sum(math.comb(8, k) ** 2 for k in range(4))
    assert aligned["supports_unable_to_match_proposed_capped_budget"] == 1 + 8 ** 2
    assert aligned["maximum_budget_feasible_for_every_half_rad"] == 0


def test_support_limits_respect_circular_symmetries():
    phases = [0, 0, .3, -.3, .6, -.6]
    rotated = [x + 1.9 + i * 2 * math.pi for i, x in enumerate(phases)]
    expected = check.matching_capacity(phases, [0, 2, 5])
    assert check.matching_capacity(rotated, [0, 2, 5]) == pytest.approx(expected)


@pytest.mark.parametrize("support", [[], [0, 0], [-1], [4], [0.0], [True]])
def test_invalid_supports_are_rejected(support):
    with pytest.raises(ValueError, match="support"):
        check.matching_capacity([0, 0, .3, -.3], support)


def test_saved_certificate_reproduces():
    def assert_equivalent(actual, expected):
        if isinstance(expected, float):
            assert actual == pytest.approx(expected, rel=1e-12, abs=1e-12)
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

    expected = json.loads((check.HERE / "intervention-budget-result.json").read_text())
    assert_equivalent(check.report(), expected)
