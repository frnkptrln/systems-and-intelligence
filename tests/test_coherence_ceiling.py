"""Checks for the coherence-ceiling sketch: the model does what its README says,
runs are reproducible from the seed, and the reading rule is the stated one."""

import importlib.util
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

EXP = Path(__file__).resolve().parents[1] / "lab/experiments/coherence_ceiling"
spec = importlib.util.spec_from_file_location("coherence_ceiling", EXP / "coherence_ceiling.py")
cc = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cc
spec.loader.exec_module(cc)

SHORT = replace(cc.Params(), T=1500, R_max=200, p_shock=1 / 300)


def test_same_seed_same_run():
    a = cc.simulate(replace(SHORT, K=0.1), 4, 7)
    b = cc.simulate(replace(SHORT, K=0.1), 4, 7)
    assert a == b


def test_state_reserve_never_moves_and_positions_stay_on_the_ring():
    p = replace(SHORT, M=60, K=0.9, reserve="state")
    K_i, pinned, sites = cc.reserve_layout(p)
    assert pinned.sum() == 20 and list(sites[:3]) == [0, 3, 6]
    rng = np.random.default_rng(0)
    e = rng.integers(0, p.M, size=3)
    x = np.repeat(e[:, None], p.N, axis=1)
    x[:, pinned] = sites[None, :]
    for _ in range(200):
        x, _ = cc.step(x, e, p, K_i, pinned, rng)
    assert (x[:, pinned] == sites[None, :]).all()
    assert x.min() >= 0 and x.max() < p.M


def test_on_target_agents_stay():
    p = replace(SHORT, K=0.9)
    K_i, pinned, _ = cc.reserve_layout(p)
    rng = np.random.default_rng(1)
    e = np.array([10])
    x = np.full((1, p.N), 10)
    x[0, :50] = 40
    new, on = cc.step(x, e, p, K_i, pinned, rng)
    assert on[0, 50:].all() and (new[0, 50:] == 10).all()


def test_generator_reserve_does_not_copy():
    p = replace(SHORT, K=1.0, mu=0.0, reserve="generator")
    K_i, pinned, _ = cc.reserve_layout(p)
    assert (K_i[:20] == 0).all() and (K_i[20:] == 1).all() and not pinned.any()
    rng = np.random.default_rng(2)
    e = np.array([0])
    x = np.full((1, p.N), 30)
    x[0, :20] = 50
    new, _ = cc.step(x, e, p, K_i, pinned, rng)
    assert (new[0, :20] == 50).all()


def test_search_is_unbiased_without_gradient_and_directed_with_it():
    rng = np.random.default_rng(3)
    n = 20_000
    x = np.full((1, n), 100)
    e = np.array([0])
    blind = replace(SHORT, N=n, M=1000, K=0.0, mu=1.0, g=0.0)
    new, _ = cc.step(x, e, blind, np.zeros(n), np.zeros(n, dtype=bool), rng)
    assert abs((new - 100).mean()) < 0.03
    new, _ = cc.step(x, e, replace(blind, g=1.0), np.zeros(n), np.zeros(n, dtype=bool), rng)
    assert (new == 99).all()


def test_reading_rule():
    cell = lambda survived, median: {"survived": survived, "replicates": 40,
                                     "median_t_collapse": median}
    assert cc.compare(cell(30, 0), cell(20, 0)) == "a"
    assert cc.compare(cell(20, 0), cell(29, 0)) == "none"
    assert cc.compare(cell(0, 9000), cell(0, 4000)) == "a"
    assert cc.compare(cell(0, 5000), cell(0, 4000)) == "none"
    assert cc.compare(cell(3, 5000), cell(0, 100)) == "none"


def test_the_grid_is_the_one_the_readme_fixes():
    grid = cc.cells(cc.Params())
    assert len(grid) == 36
    assert cc.K_GRID == (0.0, 0.003, 0.01, 0.03, 0.1, 0.3, 0.6, 0.9, 0.99)
    assert cc.REPLICATES == 40 and cc.BASE_SEED == 20261121
    base = cc.Params()
    assert (base.N, base.w, base.q, base.mu, base.R_max, base.T) == (200, 1, 0.5, 0.5, 2000, 160_000)
    assert base.p_drift == 0.01 and base.p_shock == 1 / 4000
