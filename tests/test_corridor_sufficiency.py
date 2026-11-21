"""Pins for the finite-N corridor thresholds: the closed forms, the inequalities
their proofs rest on (evaluated on the canonical right-hand side), and the
committed result file."""

import importlib.util
import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

EXP = Path(__file__).resolve().parents[1] / "lab/experiments/corridor_sufficiency"
spec = importlib.util.spec_from_file_location("corridor_sufficiency", EXP / "corridor_sufficiency.py")
cs = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cs
spec.loader.exec_module(cs)
teo = cs.teo_model()
BASE = teo.Params()
N, X_REG, X_CRIT = BASE.N, BASE.x_reg, BASE.x_crit
REPORT = json.loads((EXP / "results/results.json").read_text())


def test_closed_forms_at_the_paper_parameters():
    assert cs.gamma_low(0.3, N, X_REG, X_CRIT) == pytest.approx(0.07425 / (0.15 * 0.98), rel=1e-12)
    assert cs.excess_max(X_CRIT, X_REG) == pytest.approx(0.30, abs=1e-12)
    assert cs.gamma_full(0.3, N, X_REG, X_CRIT) == pytest.approx(0.515625, rel=1e-12)
    assert cs.gamma_low(0.3, N, X_REG, X_CRIT) < cs.gamma_full(0.3, N, X_REG, X_CRIT) \
        < cs.gamma_up(0.3, N, X_REG, X_CRIT)
    # Eq. (9) of the paper is the large-N limit of gamma_low.
    assert cs.gamma_low(0.3, 10**9, X_REG, X_CRIT) == pytest.approx(0.495, abs=1e-8)
    # Appendix C headline values, now in closed form.
    assert cs.y_star(1.5, 0.3, N, X_REG) == pytest.approx(0.346193, abs=5e-7)        # C.1 (a): 0.346
    assert cs.delta_concentration(1.5, N, X_REG, X_CRIT) == pytest.approx(0.890909, abs=5e-7)  # C.4: ~0.9
    assert cs.delta_substrate(1.5, 1.5, N, X_REG) == pytest.approx(1.046759, abs=5e-7)         # C.4: ~1.05
    assert cs.y_star(1.5, 2.0, N, X_REG) == pytest.approx(0.620410, abs=5e-7)        # C.4: ~0.62
    assert cs.d_low(6.0, 2.0, N, X_REG) == pytest.approx(1.760296, abs=5e-7)
    assert cs.d_floor(2.0, X_REG) == pytest.approx(1.6)
    # The two capability thresholds are the inverses of gamma_low and d_low.
    for delta in (0.2, 0.9, 2.5):
        assert cs.delta_concentration(cs.gamma_low(delta, N, X_REG, X_CRIT), N, X_REG, X_CRIT) \
            == pytest.approx(delta, rel=1e-12)
        assert cs.delta_substrate(1.5, cs.d_low(1.5, delta, N, X_REG), N, X_REG) == pytest.approx(delta, rel=1e-12)


@pytest.mark.parametrize("gamma,delta", [(1.5, 0.3), (6.0, 2.0), (0.6, 0.3)])
def test_equilibrium_share_and_locked_coherence_match_the_canonical_runner(gamma, delta):
    res = teo.run(replace(BASE, gamma=gamma, delta=delta, D_max=1e9, T_end=200.0, steps=2001))
    assert float(res.max_x[-1]) == pytest.approx(cs.y_star(gamma, delta, N, X_REG), abs=1e-9)
    assert float(res.r[-1]) == pytest.approx(cs.locked_state(BASE.omega, BASE.K)[1], abs=1e-7)


def _share_derivatives(p, x, health):
    state = np.concatenate([x, np.zeros(N), [(1 - health) * p.S_max]])
    return teo.make_rhs(p)(0.0, state)[:N]


def test_boundary_derivative_inequality_of_proposition_2():
    """Above gamma_full no share at the level x_crit grows, whatever the others or H do."""
    rng = np.random.default_rng(0)
    full = cs.gamma_full(0.3, N, X_REG, X_CRIT)
    above, below = replace(BASE, gamma=1.001 * full), replace(BASE, gamma=0.999 * full)
    worst = -np.inf
    for k in range(4000):
        leaders = rng.integers(1, 3)
        x = rng.dirichlet(np.full(N, rng.choice([0.05, 1.0])))
        x[:leaders] = 0.0
        x *= (1 - leaders * X_CRIT) / x.sum()
        x = np.minimum(x, X_CRIT)
        x[:leaders] = X_CRIT
        x[leaders:] *= (1 - leaders * X_CRIT) / x[leaders:].sum()
        if x.max() > X_CRIT + 1e-12:
            continue
        perm = rng.permutation(N) if k % 2 else np.arange(N)
        dx = _share_derivatives(above, x[perm], rng.uniform(0, 1))
        worst = max(worst, float(dx[np.isclose(x[perm], X_CRIT)].max()))
    assert worst < 0
    # The extremal configuration: the dominant agent and one other at x_crit.
    x = np.full(N, (1 - 2 * X_CRIT) / (N - 2))
    x[:2] = X_CRIT
    x[2], x[3:] = 1 - 2 * X_CRIT, 0.0
    assert _share_derivatives(above, x, 1.0)[0] < 0 < _share_derivatives(below, x, 1.0)[0]


@pytest.mark.parametrize("factor,exits", [(0.99, True), (1.01, False)])
def test_gamma_low_brackets_the_exit_from_uniform_shares(factor, exits):
    p = replace(BASE, gamma=factor * cs.gamma_low(0.3, N, X_REG, X_CRIT))
    out = cs.integrate(p, np.ones(N) / N, np.zeros(N), 200.0, rtol=1e-8, atol=1e-10, max_step=0.1)
    assert bool(out["x"].max() > X_CRIT) is exits


@pytest.mark.parametrize("seed", [7, 0, 3])
def test_locked_state_is_a_minimum_exactly_on_the_increasing_branch(seed):
    """Proposition 5: reduced Hessian positive definite iff S(u) > 0 iff u > u_s."""
    omega = teo.Params(seed=seed).omega
    nu = cs.centred(omega)
    thr = cs.lock_threshold(omega)
    grid = np.linspace(np.abs(nu).max() * 1.0001, 3 * thr["u_s"], 400)
    assert np.all(np.diff([cs.stability_sum(nu, u) for u in grid]) > 0)
    assert min(cs.coupling_of_u(nu, u) for u in grid) >= thr["K_lock"] - 1e-12
    for u in (0.5 * (np.abs(nu).max() + thr["u_s"]), 1.02 * thr["u_s"], 2 * thr["u_s"]):
        phi = np.arcsin(nu / u)
        eig = np.sort(np.linalg.eigvalsh(cs.potential_hessian(phi, cs.coupling_of_u(nu, u))))
        assert abs(eig[0]) < 1e-9 or eig[0] < 0          # rotation direction, or a descent direction
        positive_definite = eig[0] > -1e-9 and eig[1] > 1e-9
        assert positive_definite == (cs.stability_sum(nu, u) > 0) == (u > thr["u_s"])
        # A locked state: the canonical phase velocities are all equal there.
        rate = teo.make_rhs(replace(teo.Params(seed=seed), K=float(cs.coupling_of_u(nu, u))))(
            0.0, np.concatenate([np.ones(N) / N, phi, [0.0]]))[N:2 * N]
        assert np.ptp(rate) < 1e-9


def test_seed_7_coherence_thresholds():
    thr = cs.lock_threshold(BASE.omega)
    assert thr["K_lock"] == pytest.approx(2.534332, abs=5e-6)
    assert thr["r_at_threshold"] == pytest.approx(0.905178, abs=5e-6)
    assert cs.floor_coupling(BASE.omega, 0.5) == thr["K_lock"]
    assert cs.floor_coupling(BASE.omega, 0.95) > thr["K_lock"]
    assert cs.locked_state(BASE.omega, 3.0)[1] == pytest.approx(0.946247, abs=5e-6)   # C.1 (a): 0.946
    assert thr["K_lock"] < BASE.K < cs.arc_threshold(BASE.omega, 0.5)["K_arc"]
    assert cs.arc_threshold(BASE.omega, 0.5)["K_arc"] == pytest.approx(3.593572, abs=5e-6)


def test_arc_inequality_of_proposition_6_on_the_canonical_right_hand_side():
    """On the arc's boundary the cluster's extreme phase difference shrinks."""
    arc = cs.arc_threshold(BASE.omega, 0.5)
    p = replace(BASE, K=1.001 * arc["K_arc"])
    order = np.argsort(BASE.omega)
    cluster = order[arc["cluster_start"]:arc["cluster_start"] + arc["cluster_size"]]
    outside = np.setdiff1d(np.arange(N), cluster)
    rng = np.random.default_rng(1)
    rhs, worst = teo.make_rhs(p), -np.inf
    for k in range(3000):
        theta = np.empty(N)
        theta[cluster] = rng.uniform(-1, 1, cluster.size) * arc["half_arc"]
        if k % 3 == 0:
            theta[cluster] = rng.choice([-1, 1], cluster.size) * arc["half_arc"]
        top, bottom = rng.choice(cluster, size=2, replace=False)
        theta[top], theta[bottom] = arc["half_arc"], -arc["half_arc"]
        theta[outside] = np.pi if k % 2 else rng.uniform(0, 2 * np.pi, outside.size)
        rate = rhs(0.0, np.concatenate([np.ones(N) / N, theta, [0.0]]))[N:2 * N]
        worst = max(worst, float(rate[top] - rate[bottom]))
        z = abs(np.exp(1j * theta).mean())
        assert z >= arc["coherence_bound"] - 1e-12
    assert worst < 0
    assert arc["coherence_bound"] >= BASE.r_min


def test_population_arc_thresholds():
    import math
    gauss = lambda c: math.erf(c / math.sqrt(2))
    lorentz = lambda c: 2 / math.pi * math.atan(c)
    assert cs.arc_threshold_density(gauss, 0.5) == pytest.approx(4.3184, abs=2e-4)
    assert cs.arc_threshold_density(lorentz, 0.5) == pytest.approx(12.3180, abs=2e-4)


def test_damage_stabilised_window_and_its_closure():
    """Printed model: health settles at the predicted value; brake scaled by H: veto."""
    p = replace(BASE, gamma=6.0, delta=2.0, D_max=1.70)
    assert cs.d_floor(2.0, X_REG) < p.D_max < cs.d_low(6.0, 2.0, N, X_REG)
    predicted = cs.health_limit(1.70, 6.0, 2.0, N, X_REG)
    assert predicted == pytest.approx(0.646154, abs=5e-6)
    printed = cs.classify(p, 400.0)
    assert printed["outcome"] == "damage-stabilised"
    assert printed["H_final"] == pytest.approx(predicted, abs=2e-3)
    assert printed["throughput_final"] == pytest.approx(1.70, abs=1e-3)
    assert printed["sup_max_x"] < X_CRIT and printed["r_min_sampled"] > BASE.r_min
    assert cs.classify(replace(p, brake_couples_to_H=True), 400.0)["outcome"] == "veto"
    assert cs.classify(replace(p, D_max=1.59), 400.0)["outcome"] == "veto"


def test_committed_results_are_complete_and_consistent():
    assert REPORT["thresholds"]["gamma_low"] == pytest.approx(cs.gamma_low(0.3, N, X_REG, X_CRIT))
    assert REPORT["thresholds"]["seed_7"]["lock"]["K_lock"] == pytest.approx(
        cs.lock_threshold(BASE.omega)["K_lock"])
    for row in REPORT["closed_forms"]:
        assert row["max_x_simulated"] == pytest.approx(row["y_star"], abs=1e-9)
        assert row["throughput_simulated"] == pytest.approx(row["throughput_formula"], abs=1e-9)
        assert row["r_simulated"] == pytest.approx(row["r_lock"], abs=1e-7)
    for row in REPORT["resource_thresholds"]:
        factor = row.get("gamma_over_gamma_low", row.get("gamma_over_gamma_full"))
        assert (row["sup_max_x_minus_x_crit"] > 0) == (factor < 1)
    assert [row["samples"] for row in REPORT["open_sets"]] == [200, 200, 200]
    assert all(row["violations"] == 0 for row in REPORT["open_sets"])
    plane = REPORT["plane"]
    assert len(plane) == 81
    proved = [c for c in plane if c["proved"] != "none"]
    assert len(proved) == 63 and all(c["simulation_agrees"] for c in proved)
    window = [c for c in plane if c["proved"] == "none"]
    low = cs.gamma_low(2.0, N, X_REG, X_CRIT)
    assert all(c["outcome"] == "damage-stabilised" for c in window if c["gamma"] >= low)
    for row in REPORT["damage_window"]:
        assert row["brake_scaled_by_H"]["outcome"] == "veto"
        assert (row["printed_model"]["outcome"] == "damage-stabilised") == row["inside_window"]
        if row["inside_window"]:
            assert row["printed_model"]["H_final"] == pytest.approx(row["H_predicted"], abs=1e-3)
    assert len(REPORT["coherence_thresholds"]) == 48
    assert all(c["r_at_threshold"] > 0.5 and c["K_floor_0.5"] == c["K_lock"]
               for c in REPORT["coherence_thresholds"])
    # Neither coherence clause dominates: one N = 1000 draw locks later than its arc threshold.
    later = [c for c in REPORT["coherence_thresholds"] if c["K_lock"] >= c["K_arc_0.5"]]
    assert [(c["N"], c["seed"]) for c in later] == [(1000, 0)]
