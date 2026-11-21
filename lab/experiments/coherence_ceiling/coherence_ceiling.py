"""Survival against coupling strength in a moving environment.

The model, its parameters, the predictions and the reading rules are fixed in
README.md, which was committed before this file existed. This file implements
that text and nothing else.

Run:  python coherence_ceiling.py --out results/results.json
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass, replace
from multiprocessing import Pool
from pathlib import Path

import numpy as np

BASE_SEED = 20261121
REPLICATES = 40
K_GRID = (0.0, 0.003, 0.01, 0.03, 0.1, 0.3, 0.6, 0.9, 0.99)
RESERVES = ("none", "state", "generator")
R_SAMPLE_EVERY = 50


@dataclass(frozen=True)
class Params:
    N: int = 200
    M: int = 100
    w: int = 1
    q: float = 0.5
    mu: float = 0.5
    K: float = 0.1
    g: float = 0.0
    p_drift: float = 0.01
    p_shock: float = 1.0 / 4000.0
    R_max: int = 2000
    T: int = 160_000
    reserve: str = "none"
    rho: float = 0.1


def ring_distance(a: np.ndarray, b: np.ndarray, M: int) -> np.ndarray:
    d = (a - b) % M
    return np.minimum(d, M - d)


def reserve_layout(p: Params) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-agent coupling, the pinned mask, and the pinned sites."""
    K_i = np.full(p.N, p.K)
    pinned = np.zeros(p.N, dtype=bool)
    sites = np.zeros(0, dtype=np.int64)
    if p.reserve == "none":
        return K_i, pinned, sites
    n_res = int(round(p.rho * p.N))
    if p.reserve == "state":
        pinned[:n_res] = True
        sites = (np.arange(n_res) * p.M) // n_res
    elif p.reserve == "generator":
        K_i[:n_res] = 0.0
    else:
        raise ValueError(f"unknown reserve: {p.reserve}")
    return K_i, pinned, sites


def step(x, e, p: Params, K_i, pinned, rng):
    """One synchronous agent update. Returns the new positions and the on-target mask
    that the update was based on."""
    S, N = x.shape
    on = ring_distance(x, e[:, None], p.M) <= p.w
    movable = ~on & ~pinned[None, :]
    conform = movable & (rng.random((S, N)) < K_i[None, :])
    search = movable & ~conform & (rng.random((S, N)) < p.mu)
    copied = np.take_along_axis(x, rng.integers(0, N, size=(S, N)), axis=1)
    delta = (e[:, None] - x) % p.M
    toward = np.where(delta <= p.M - delta, 1, -1)
    informed = rng.random((S, N)) < (1.0 + p.g) / 2.0
    moved = (x + np.where(informed, toward, -toward)) % p.M
    return np.where(conform, copied, np.where(search, moved, x)), on


def simulate(p: Params, replicates: int, seed) -> dict:
    """Run `replicates` independent systems side by side.

    Order within a step: the environment moves, payoffs and the reserve are
    settled, then the agents update.
    """
    rng = np.random.default_rng(seed)
    S = replicates
    K_i, pinned, sites = reserve_layout(p)
    e = rng.integers(0, p.M, size=S)
    x = np.repeat(e[:, None], p.N, axis=1)
    if sites.size:
        x[:, pinned] = sites[None, :]
    R = np.full(S, p.R_max, dtype=np.int64)
    alive = np.ones(S, dtype=bool)
    t_collapse = np.full(S, p.T, dtype=np.int64)
    r_sum = np.zeros(S)
    on_sum = np.zeros(S)
    samples = np.zeros(S, dtype=np.int64)
    phase = 2j * np.pi / p.M

    for t in range(p.T):
        shock = rng.random(S) < p.p_shock
        drift = ~shock & (rng.random(S) < p.p_drift)
        jump = rng.integers(0, p.M, size=S)
        nudge = rng.integers(0, 2, size=S) * 2 - 1
        e = np.where(shock, jump, np.where(drift, (e + nudge) % p.M, e))

        x_new, on = step(x, e, p, K_i, pinned, rng)
        frac = on.mean(axis=1)
        R = np.where(frac >= p.q, np.minimum(R + 1, p.R_max), R - 1)
        newly = alive & (R <= 0)
        t_collapse[newly] = t
        alive &= ~newly
        if not alive.any():
            break

        if t % R_SAMPLE_EVERY == 0:
            r_sum += np.where(alive, np.abs(np.exp(phase * x).mean(axis=1)), 0.0)
            on_sum += np.where(alive, frac, 0.0)
            samples += alive
        x = x_new

    seen = np.maximum(samples, 1)
    return {
        "survived": int(alive.sum()),
        "replicates": S,
        "t_collapse": [int(v) for v in t_collapse],
        "median_t_collapse": float(np.median(t_collapse)),
        "mean_r_while_alive": float((r_sum / seen).mean()),
        "mean_on_target_while_alive": float((on_sum / seen).mean()),
    }


def cells(base: Params) -> list[dict]:
    out = []
    for M in (100, 12):
        for K in K_GRID:
            out.append({"experiment": "E1", "params": replace(base, M=M, K=K, g=0.0)})
    for name, g in (("E2", 0.0), ("E3", 0.5)):
        for M in (60, 240, 960):
            for reserve in RESERVES:
                out.append({"experiment": name,
                            "params": replace(base, M=M, K=0.9, g=g, reserve=reserve)})
    return out


def _run_cell(job):
    index, cell, replicates = job
    started = time.time()
    result = simulate(cell["params"], replicates, np.random.SeedSequence([BASE_SEED, index]))
    return {"index": index, "experiment": cell["experiment"],
            "params": asdict(cell["params"]), **result,
            "seconds": round(time.time() - started, 1)}


def compare(a: dict, b: dict) -> str:
    """The reading rule of the README: 'a', 'b' or 'none'."""
    fa, fb = a["survived"] / a["replicates"], b["survived"] / b["replicates"]
    if abs(fa - fb) >= 0.25 - 1e-12:
        return "a" if fa > fb else "b"
    if fa == 0.0 and fb == 0.0:
        ma, mb = a["median_t_collapse"], b["median_t_collapse"]
        if ma >= 2 * mb:
            return "a"
        if mb >= 2 * ma:
            return "b"
    return "none"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "results/results.json")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--smoke", action="store_true",
                        help="short horizon and few replicates; not evidence")
    args = parser.parse_args()

    base = Params()
    replicates = REPLICATES
    if args.smoke:
        base, replicates = replace(base, T=6000, R_max=300, p_shock=1 / 600), 4
    jobs = [(i, cell, replicates) for i, cell in enumerate(cells(base))]
    with Pool(args.workers) as pool:
        results = []
        for row in pool.imap_unordered(_run_cell, jobs):
            results.append(row)
            p = row["params"]
            print(f"{row['experiment']} M={p['M']:>4} K={p['K']:<5} g={p['g']} "
                  f"reserve={p['reserve']:<9} survived {row['survived']}/{row['replicates']} "
                  f"median_t={row['median_t_collapse']:.0f} r={row['mean_r_while_alive']:.3f} "
                  f"({row['seconds']}s)", flush=True)
    results.sort(key=lambda row: row["index"])
    report = {"base_seed": BASE_SEED, "smoke": args.smoke, "cells": results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=1) + "\n")


if __name__ == "__main__":
    main()
