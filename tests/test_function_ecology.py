"""Checks for the function-ecology sketch: the table tests do what the definition
files say, and the committed results carry the counts the README reports.  The
original AlChemy program is not needed for any of this."""

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

EXP = Path(__file__).resolve().parents[1] / "lab/experiments/function_ecology"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, EXP / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


an = _load("analyse")
a2 = _load("analyse2")
a3 = _load("analyse3")


def _ladder(n):
    """n members, member i with i+1 leading abstractions; the first raises, the others
    lower by one and are elastic where the product would be a copy."""
    core = ["".join(f"\\x{k}." for k in range(1, i + 2)) + "x1" for i in range(n)]
    table = np.full((n, n), -1)
    for j in range(n):
        table[0, j] = j + 1 if j + 1 < n else -2
    for i in range(1, n):
        for j in range(n):
            table[i, j] = -1 if j == i - 1 else i - 1
    return core, table


def test_ladder_and_lowerers_on_a_built_ladder():
    core, table = _ladder(5)
    assert a2.is_ladder(core, table)
    order, S = a2.sorted_table(core, table)
    assert a3.lowerers([core[i] for i in order], S) == [1, 2, 3, 4]


def test_ladder_test_rejects_a_wrong_row_and_short_cores():
    core, table = _ladder(5)
    broken = table.copy()
    broken[3, 0] = 0
    assert not a2.is_ladder(core, broken)
    short_core, short_table = _ladder(2)
    assert not a2.is_ladder(short_core, short_table)


def test_closure_and_ancestors():
    T = np.full((5, 5), -1)
    T[0, 0], T[1, 0], T[3, 3] = 1, 2, 4
    seed = np.array([True, False, False, False, False])
    assert an.closure(seed, T).tolist() == [True, True, True, False, False]
    assert an.ancestors(T, np.array([2])).tolist() == [True, True, True, False, False]


def test_tables_agree_up_to_renaming_and_not_after_a_change():
    A = np.array([[1, -1, 0], [2, -2, -1], [0, 1, 2]])
    perm = [2, 0, 1]
    B = np.full((3, 3), -9)
    for p in range(3):
        for q in range(3):
            v = A[p, q]
            B[perm[p], perm[q]] = perm[v] if v >= 0 else v
    assert an.isomorphic(A, B) == "yes"
    C = B.copy()
    C[0, 0] = -1 if C[0, 0] != -1 else -2
    assert an.isomorphic(A, C) == "no"


def test_round_1_counts():
    d = json.loads((EXP / "results/run1.json").read_text())
    stable = [r for r in d["runs"] if r["stable"]]
    assert (len(d["runs"]), len(stable), len(d["pairs"])) == (20, 10, 45)
    assert sum(p["identical"] for p in d["pairs"]) == 0
    assert sum(p["strict"] == "yes" for p in d["pairs"]) == 0
    assert sum(r["projection_share"] >= 0.9 for r in stable) == 3
    assert sorted(r["generating_set_sizes"][0] for r in stable) == [1, 1, 1, 1, 1, 1, 1, 2, 27, 53]
    assert sum(r["generating_set_unique"] for r in stable) == 1


def test_round_2_counts():
    d = json.loads((EXP / "results/run2.json").read_text())
    stable = [r for r in d["runs"] if r["stable"]]
    ladders = [r for r in stable if r["ladder"]]
    assert (len(d["runs"]), len(stable), len(ladders)) == (30, 22, 8)
    assert sum(p["identical"] for p in d["pairs"]) == 3
    assert all(r["single_generator_share"] > 0.5 for r in ladders)
    assert [r["regrown_share"] for r in ladders] == [1.0] * 8


def test_round_3_counts():
    d = json.loads((EXP / "results/run3.json").read_text())
    stable = [r for r in d["runs"] if r["stable"]]
    bundles = [r for r in stable if r["bundle"]]
    assert (len(d["runs"]), len(stable), len(bundles)) == (30, 20, 13)
    assert sum(r["ladder"] for r in stable) == 6
    assert sum(r["generating_set_size"] == 1 for r in bundles) == 11
    assert sum(r["regrown_share"] >= 0.8 for r in bundles) == 12
    assert sum(r["two_core"] for r in stable) == 2
    assert sum(r["k_ladder"] for r in stable) == 3
