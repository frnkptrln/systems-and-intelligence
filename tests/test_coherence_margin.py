"""Independent controls and the pinned headline for the coherence-floor check."""

import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import solve_ivp

EXP = Path(__file__).resolve().parents[1] / "lab/experiments/coherence_margin"
spec = importlib.util.spec_from_file_location("coherence_margin", EXP / "coherence_margin.py")
cm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cm)
REPORT = json.loads((EXP / "results/results.json").read_text())


@pytest.mark.parametrize("coupling", [0.0, 1.8, 2.0, 2.2, 8/3, 3.0])
def test_closed_solution_matches_independent_integration(coupling):
    t = np.linspace(0, 80, 401)
    r0 = 0.9
    # Write the published differential equation independently of amplitude_rhs.
    sol = solve_ivp(lambda t, r: -r + coupling/2 * r * (1-r*r), (0, 80),
                    [r0], t_eval=t, rtol=1e-11, atol=1e-13, max_step=0.1)
    assert sol.success
    np.testing.assert_allclose(cm.amplitude_exact(t, coupling, r0), sol.y[0], atol=1e-9)


def test_critical_and_zero_amplitudes_and_boundary_condition():
    t = np.array([0, 1, 80.0])
    np.testing.assert_allclose(cm.amplitude_exact(t, 2, 0.5), 0.5/np.sqrt(1+0.5*t))
    np.testing.assert_array_equal(cm.amplitude_exact(t, 3, 0), np.zeros_like(t))
    # This countercase has positive synchronization but no admissible equilibrium.
    assert 0 < np.sqrt(1-2/2.2) < 0.5
    assert np.all(cm.amplitude_rhs(np.linspace(0.5, 1, 100), 2.2) < 0)
    assert cm.amplitude_rhs(0.5, 8/3) == pytest.approx(0, abs=1e-15)
    assert cm.amplitude_rhs(0.5, 3) > 0


@pytest.mark.parametrize("floor", [0.25, 0.5, 0.75])
def test_stationary_quadrature_has_an_independent_lorentzian_control(floor):
    assert cm.stationary_floor(floor, "lorentzian") == pytest.approx(
        2/(1-floor**2), abs=1e-9)


def test_committed_grid_is_complete_and_pins_the_headline():
    cells = REPORT["finite_cells"]
    expected = {(k, seed) for k in (0.8, 1.6, 1.7, 2.0, 3.0) for seed in range(16)}
    assert len(cells) == 80
    assert {(c["K"], c["seed"]) for c in cells} == expected
    assert [sum(not c["V2_coherence"] for c in cells if c["K"] == k)
            for k in (0.8, 1.6, 1.7, 2.0, 3.0)] == [16, 10, 9, 2, 0]
    assert REPORT["summary"]["above_onset_isolated_failures"] == 21
    assert all(c["solver_complete"] and c["numerically_valid"] and
               c["V1_resources_sampled"] and c["V3_substrate_sampled"] and
               c["r_initial"] > 0.5 for c in cells)
    assert len(REPORT["scalar_checks"]) == 45
    assert REPORT["maximum_scalar_error"] < 1e-7
    assert REPORT["maximum_lorentzian_quadrature_error"] < 1e-7
    assert all(v["classification_unchanged"] and v["r_min_absolute_change"] < 1e-6
               for v in REPORT["validation"])


@pytest.mark.parametrize("coupling,coherent", [(1.6, False), (3.0, True)])
def test_selected_witness_and_control_reproduce_with_the_canonical_runner(coupling, coherent):
    # Use the existing run() including its initial-condition construction, not
    # the experiment's integration wrapper, to guard model/IC drift.
    teo = cm.teo_model()
    result = teo.run(teo.Params(K=coupling, seed=0))
    saved = next(c for c in REPORT["finite_cells"] if c["K"] == coupling and c["seed"] == 0)
    assert bool(np.all(result.r >= 0.5)) is coherent
    assert float(result.r.min()) == pytest.approx(saved["r_min_sampled"], abs=1e-6)
    assert float(result.r[-1]) == pytest.approx(saved["r_final"], abs=1e-6)
    assert result.simplex_err < 1e-8
    assert np.all(result.max_x < 0.45)
    assert np.all(result.Omega == 0)
