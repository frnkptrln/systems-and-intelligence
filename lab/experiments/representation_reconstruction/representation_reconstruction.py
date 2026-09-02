"""Representation and reconstruction difficulty (Experiment B).

Origin notes (``ideas/``): representation-changes-reconstruction-difficulty,
mechanism-as-reconstruction-target, representational-grounding-and-mechanistic-
world-models.

Setting: the elementary-cellular-automaton testbed of the inverse-reconstruction
benchmark (``lab/benchmarks/inverse-reconstruction/inverse_benchmark.py``): a
known family of 256 rules, the benchmark's forward model, its tabulating
reconstructor (majority vote over observed neighborhood -> successor pairs),
its coverage dial (random versus single-seed initial condition) and its noise
dial (bit-flip probability). The reconstructor is unchanged. What changes is
the *representation of the trace it receives*:

- ``raw``            the space-time grid as the benchmark produces it;
- ``complement``     invertible: every cell x -> 1 - x;
- ``reflect``        invertible: every row reversed;
- ``both``           invertible: complement then reflect;
- ``block_or2``      lossy: adjacent cell pairs -> OR (width halves);
- ``majority3``      lossy: every cell -> majority of its 3-neighborhood.

Under an invertible re-encoding the received trace is exactly the trace of
another rule in the same family (the complement conjugate, the mirror rule, or
both), so the reconstructor recovers that *transformed truth*. Class size is
``2 ** (unseen neighborhoods)`` as in the benchmark; a lossy trace can also
contain contradictions (one neighborhood, two successors), which the benchmark's
majority vote hides and which are reported here as ``contradictions``.

The search-cost measure is the benchmark's own (``family_search.py``): the
number of syntactic formulas a size-ordered enumerator over the Boolean DSL
generates before it reaches the minimal description size of the *shortest
table consistent with the observed bits*. Verification of a candidate costs
eight comparisons regardless of representation; only the construction cost
can change.

Requires numpy (repository ``requirements.txt``).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
_BENCH = REPO / "lab" / "benchmarks" / "inverse-reconstruction"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, _BENCH / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ib = _load("representation_ib", "inverse_benchmark.py")
fs = _load("representation_fs", "family_search.py")

CONDITIONS = ("raw", "complement", "reflect", "both", "block_or2", "majority3")
INVERTIBLE = ("complement", "reflect", "both")
LOSSY = ("block_or2", "majority3")
ICS = ("random", "single")
NOISES = (0.0, 0.1, 0.2)
W, T = 64, 64

# The declared CI subgrid: every eighth rule, one seed, two noise levels. Pinned by
# tests/test_representation_reconstruction.py against results/ci_subgrid.json.
CI_SUBGRID = {"seeds": 1, "rules": range(0, 256, 8), "ics": ICS, "noises": (0.0, 0.1)}

MIN_SIZE = fs.minimal_sizes()
STREAM = fs.stream_sizes()
CUM_STREAM = np.cumsum(STREAM).tolist()


# ---------------------------------------------------------------- rule maps
def complement_rule(rule: int) -> int:
    """The rule whose trace is the cell-wise complement of ``rule``'s trace."""
    bits = 0
    for p in range(8):
        q = (~p) & 7
        bits |= (1 - ((rule >> q) & 1)) << p
    return bits


def reflect_rule(rule: int) -> int:
    """The rule whose trace is the left-right mirror of ``rule``'s trace."""
    bits = 0
    for p in range(8):
        l, c, r = (p >> 2) & 1, (p >> 1) & 1, p & 1
        q = (r << 2) | (c << 1) | l
        bits |= ((rule >> q) & 1) << p
    return bits


def transformed_truth(rule: int, condition: str) -> int | None:
    if condition == "raw":
        return rule
    if condition == "complement":
        return complement_rule(rule)
    if condition == "reflect":
        return reflect_rule(rule)
    if condition == "both":
        return reflect_rule(complement_rule(rule))
    return None


# ------------------------------------------------------------- trace encodings
def encode(grid: np.ndarray, condition: str) -> np.ndarray:
    if condition == "raw":
        return grid
    if condition == "complement":
        return 1 - grid
    if condition == "reflect":
        return grid[:, ::-1]
    if condition == "both":
        return (1 - grid)[:, ::-1]
    if condition == "block_or2":
        return (grid[:, 0::2] | grid[:, 1::2]).astype(np.uint8)
    if condition == "majority3":
        s = np.roll(grid, 1, axis=1).astype(int) + grid.astype(int) + np.roll(grid, -1, axis=1).astype(int)
        return (s >= 2).astype(np.uint8)
    raise ValueError(condition)


# --------------------------------------------------------------- reconstruction
def tabulate(grid: np.ndarray) -> np.ndarray:
    """Counts[pattern, successor] over all transitions in the grid."""
    counts = np.zeros((8, 2), dtype=np.int64)
    for t in range(grid.shape[0] - 1):
        row, nxt = grid[t].astype(int), grid[t + 1].astype(int)
        nb = (np.roll(row, 1) << 2) | (row << 1) | np.roll(row, -1)
        for pat in range(8):
            m = nb == pat
            if m.any():
                ones = int(nxt[m].sum())
                counts[pat, 1] += ones
                counts[pat, 0] += int(m.sum()) - ones
    return counts


def reconstruct(grid: np.ndarray, flip_p: float, seed: int) -> dict:
    bits, seen, class_size = ib.ca_inverse(grid, flip_p=flip_p, seed=seed)
    counts = tabulate(_noisy(grid, flip_p, seed))
    contradictions = int(((counts[:, 0] > 0) & (counts[:, 1] > 0)).sum())
    mask = int(sum(1 << p for p in range(8) if seen[p]))
    observed_table = int(sum(int(bits[p]) << p for p in range(8) if seen[p]))
    consistent = [t for t in range(256) if (t & mask) == observed_table]
    min_consistent_size = min(MIN_SIZE[t] for t in consistent)
    return {
        "bits": [int(b) for b in bits],
        "seen": [bool(s) for s in seen],
        "class_size": int(class_size),
        "contradictions": contradictions,
        "min_consistent_size": int(min_consistent_size),
        "search_cost": int(CUM_STREAM[min_consistent_size - 1]),
    }


def _noisy(grid: np.ndarray, flip_p: float, seed: int) -> np.ndarray:
    """The same noise draw ``ca_inverse`` applies, reproduced for the contradiction count."""
    if flip_p <= 0:
        return grid
    rng = np.random.default_rng(seed + 2)
    flips = rng.random(grid.shape) < flip_p
    return grid ^ flips.astype(np.uint8)


def run_one(rule: int, condition: str, ic: str, flip_p: float, seed: int) -> dict:
    grid = ib.ca_forward(rule=rule, W=W, T=T, ic=ic, seed=seed)
    rec = reconstruct(encode(grid, condition), flip_p, seed)
    truth = transformed_truth(rule, condition)
    if truth is not None:
        seen = rec["seen"]
        agree = [rec["bits"][p] == ((truth >> p) & 1) for p in range(8) if seen[p]]
        rec["truth_in_class"] = all(agree)
        rec["bit_accuracy"] = (sum(agree) / len(agree)) if agree else None
        rec["truth_size"] = MIN_SIZE[truth]
    else:
        rec["truth_in_class"] = None
        rec["bit_accuracy"] = None
        rec["truth_size"] = None
    rec["transformed_truth"] = truth
    return rec


def aggregate(seeds: int, rules=range(256), ics=ICS, noises=NOISES) -> dict:
    rules = list(rules); ics = tuple(ics); noises = tuple(noises)
    out: dict = {
        "parameters": {"seeds": seeds, "rules": len(rules), "rule_list": rules if len(rules) < 256 else "all",
                        "width": W, "steps": T,
                        "ics": list(ics), "noises": list(noises), "conditions": list(CONDITIONS)},
        "cells": {},
        "invertibility_check": {},
    }
    per_cell: dict[tuple, dict] = {}
    raw_class: dict[tuple, int] = {}
    raw_cost: dict[tuple, int] = {}
    for ic in ics:
        for flip_p in noises:
            for condition in CONDITIONS:
                key = (ic, flip_p, condition)
                acc = {"runs": 0, "class_size_sum": 0, "contradiction_runs": 0,
                       "truth_in_class": 0, "accuracy_sum": 0.0, "accuracy_n": 0,
                       "search_cost_sum": 0, "class_size_equal_raw": 0, "cost_equal_raw": 0}
                for seed in range(seeds):
                    for rule in rules:
                        r = run_one(rule, condition, ic, flip_p, seed)
                        acc["runs"] += 1
                        acc["class_size_sum"] += r["class_size"]
                        acc["contradiction_runs"] += int(r["contradictions"] > 0)
                        acc["search_cost_sum"] += r["search_cost"]
                        if r["truth_in_class"] is not None:
                            acc["truth_in_class"] += int(r["truth_in_class"])
                        if r["bit_accuracy"] is not None:
                            acc["accuracy_sum"] += r["bit_accuracy"]
                            acc["accuracy_n"] += 1
                        rk = (ic, flip_p, seed, rule)
                        if condition == "raw":
                            raw_class[rk] = r["class_size"]
                            raw_cost[rk] = r["search_cost"]
                        else:
                            acc["class_size_equal_raw"] += int(r["class_size"] == raw_class[rk])
                            acc["cost_equal_raw"] += int(r["search_cost"] == raw_cost[rk])
                per_cell[key] = acc
                out["cells"][f"{ic}|{flip_p}|{condition}"] = {
                    "runs": acc["runs"],
                    "mean_class_size": acc["class_size_sum"] / acc["runs"],
                    "contradiction_fraction": acc["contradiction_runs"] / acc["runs"],
                    "truth_in_class_fraction": (acc["truth_in_class"] / acc["runs"]) if condition not in LOSSY else None,
                    "mean_bit_accuracy": (acc["accuracy_sum"] / acc["accuracy_n"]) if acc["accuracy_n"] else None,
                    "mean_search_cost": acc["search_cost_sum"] / acc["runs"],
                    "class_size_equal_raw_fraction": (acc["class_size_equal_raw"] / acc["runs"]) if condition != "raw" else None,
                    "cost_equal_raw_fraction": (acc["cost_equal_raw"] / acc["runs"]) if condition != "raw" else None,
                }
    # Exact statement of the invertibility prediction over all cells.
    for condition in INVERTIBLE:
        eq = sum(per_cell[(ic, p, condition)]["class_size_equal_raw"] for ic in ics for p in noises)
        runs = sum(per_cell[(ic, p, condition)]["runs"] for ic in ics for p in noises)
        out["invertibility_check"][condition] = {"class_size_equal_raw": eq, "runs": runs, "exact": eq == runs}
    # Description-size shift under the invertible maps, over the 256 rules.
    shift = {}
    for condition in INVERTIBLE:
        diffs = [MIN_SIZE[transformed_truth(r, condition)] - MIN_SIZE[r] for r in range(256)]
        shift[condition] = {
            "rules_with_changed_size": sum(1 for d in diffs if d != 0),
            "rules_cheaper": sum(1 for d in diffs if d < 0),
            "rules_dearer": sum(1 for d in diffs if d > 0),
            "max_abs_size_shift": max(abs(d) for d in diffs),
        }
    out["description_size_shift"] = shift
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=2)
    parser.add_argument("--save", action="store_true", help="write results/representation_reconstruction.json")
    args = parser.parse_args()
    result = aggregate(args.seeds)
    print(json.dumps(result, indent=1))
    if args.save:
        out = HERE / "results" / "representation_reconstruction.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {out.relative_to(REPO)}")
        sub = HERE / "results" / "ci_subgrid.json"
        sub.write_text(json.dumps(aggregate(**CI_SUBGRID), indent=1) + "\n", encoding="utf-8")
        print(f"wrote {sub.relative_to(REPO)}")


if __name__ == "__main__":
    main()
