import importlib.util
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
