"""Analysis of the function-ecology runs, implementing DEFINITIONS.md.

Written by Claude, 21 November 2026.  Usage:
    python3 analyse.py RUNS_DIR OUT.json
"""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from itertools import combinations
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PRODUCTS = HERE / "products"
HEAP, CYCLES = 800, 500
ABSTRACTION = re.compile(r"^\\x[0-9]+")
PROJECTION = re.compile(r"^(\\x[0-9]+\.)+x[0-9]+$")
LINE = re.compile(r"^(.*) \{(\d+) (\d+) (\d+)\}$")
ORDERS = 20
ISO_BUDGET = 200_000


def read_snapshot(path: Path) -> dict[str, int]:
    """expression -> number of instances"""
    out = {}
    for raw in path.read_text().splitlines():
        m = LINE.match(raw)
        if m:
            out[m.group(1)] = int(m.group(3))
    return out


def core_at(run: Path, last: int) -> set[str]:
    now, before = read_snapshot(run / f"s{last}"), read_snapshot(run / f"s{last - 10}")
    return {e for e, k in now.items() if k >= 2 and e in before}


def product_table(exprs: list[str], workdir: Path) -> np.ndarray:
    """T[i, j] = index in exprs of the product (f_i)f_j, -1 elastic, -2 outside."""
    src = workdir / "population.txt"
    src.write_text("\n".join(exprs) + "\n")
    res = subprocess.run([str(PRODUCTS), str(src), str(HEAP), str(CYCLES)],
                         capture_output=True, text=True, check=True)
    index = {e: i for i, e in enumerate(exprs)}
    n = len(exprs)
    T = np.full((n, n), -1, dtype=np.int32)
    for raw in res.stdout.splitlines():
        i, j, result = raw.split("\t", 2)
        i, j = int(i), int(j)
        if result == "#" or not ABSTRACTION.match(result):
            continue                              # no normal form, or not an abstraction
        if result == exprs[i] or result == exprs[j]:
            continue                              # copy action
        T[i, j] = index.get(result, -2)
    return T


def closure(seed: np.ndarray, T: np.ndarray, need: np.ndarray | None = None) -> np.ndarray:
    """Members reachable from `seed` by products that stay in the population."""
    inside = seed.copy()
    while True:
        idx = np.flatnonzero(inside)
        prod = T[np.ix_(idx, idx)]
        found = prod[prod >= 0]
        if found.size == 0:
            break
        new = np.zeros_like(inside)
        new[found] = True
        new &= ~inside
        if not new.any():
            break
        inside |= new
        if need is not None and inside[need].all():
            break
    return inside


def ancestors(T: np.ndarray, core_idx: np.ndarray) -> np.ndarray:
    """Everything that takes part in some product chain ending in the core.  A product
    that lands in this set has both factors in it, so members outside it can never
    help to generate the core: greedy removal drops them in any order, and dropping
    them first changes no result."""
    inside = np.zeros(T.shape[0], dtype=bool)
    inside[core_idx] = True
    while True:
        hits = (T >= 0) & inside[np.clip(T, 0, None)]
        grown = inside | hits.any(axis=1) | hits.any(axis=0)
        if (grown == inside).all():
            return inside
        inside = grown


def generating_sets(T: np.ndarray, core_idx: np.ndarray, rng: random.Random) -> list[frozenset]:
    relevant = ancestors(T, core_idx)
    candidates = np.flatnonzero(relevant).tolist()
    found = []
    for _ in range(ORDERS):
        order = candidates[:]
        rng.shuffle(order)
        keep = relevant.copy()
        for x in order:
            keep[x] = False
            if not closure(keep, T, core_idx)[core_idx].all():
                keep[x] = True
        found.append(frozenset(np.flatnonzero(keep).tolist()))
    return found


def refine(table: np.ndarray) -> list[int]:
    """Colour refinement on a core table whose entries are member indices or negatives."""
    n = table.shape[0]
    colour = [0] * n
    for _ in range(n + 1):
        def tag(v):
            return ("m", colour[v]) if v >= 0 else ("x", int(v))
        sig = []
        for i in range(n):
            row = sorted((colour[j], tag(table[i, j])) for j in range(n))
            col = sorted((colour[j], tag(table[j, i])) for j in range(n))
            hits = sorted((colour[a], colour[b]) for a, b in zip(*np.nonzero(table == i)))
            sig.append((colour[i], tag(table[i, i]), tuple(row), tuple(col), tuple(hits)))
        ranks = {s: r for r, s in enumerate(sorted(set(sig)))}
        new = [ranks[s] for s in sig]
        if new == colour:
            break
        colour = new
    return colour


def isomorphic(A: np.ndarray, B: np.ndarray) -> str:
    """'yes', 'no' or 'undecided' for two core tables (negatives are fixed symbols)."""
    n = A.shape[0]
    if B.shape[0] != n:
        return "no"
    ca, cb = refine(A), refine(B)
    if sorted(ca) != sorted(cb):
        return "no"
    # colours are comparable only if the signature sets coincide; compare via joint refinement
    joint = np.full((2 * n, 2 * n), -3, dtype=np.int64)
    joint[:n, :n] = A
    joint[n:, n:] = np.where(B >= 0, B + n, B)
    cj = refine(joint)
    ca, cb = cj[:n], cj[n:]
    if sorted(ca) != sorted(cb):
        return "no"
    classes = {}
    for j, c in enumerate(cb):
        classes.setdefault(c, []).append(j)
    order = sorted(range(n), key=lambda i: len(classes[ca[i]]))
    image, used, steps = {}, set(), [0]

    def consistent(i, j):
        for a, b in image.items():
            for (p, q), (r, s) in (((i, a), (j, b)), ((a, i), (b, j))):
                u, v = A[p, q], B[r, s]
                if (u >= 0) != (v >= 0) or (u < 0 and u != v):
                    return False
                if u >= 0 and u in image and image[u] != v:
                    return False
        u, v = A[i, i], B[j, j]
        if (u >= 0) != (v >= 0) or (u < 0 and u != v):
            return False
        return True

    def extend(k):
        steps[0] += 1
        if steps[0] > ISO_BUDGET:
            raise TimeoutError
        if k == n:
            return all((image[A[p, q]] if A[p, q] >= 0 else A[p, q]) == B[image[p], image[q]]
                       for p in range(n) for q in range(n))
        i = order[k]
        for j in classes[ca[i]]:
            if j in used or not consistent(i, j):
                continue
            image[i] = j
            used.add(j)
            if extend(k + 1):
                return True
            del image[i]
            used.discard(j)
        return False

    try:
        return "yes" if extend(0) else "no"
    except TimeoutError:
        return "undecided"


def analyse_run(run: Path, rng: random.Random) -> dict:
    final = read_snapshot(run / "s100")
    population = sorted(final)
    core = core_at(run, 100)
    earlier = core_at(run, 90)
    stable = len(core) >= 2 and len(core & earlier) >= 0.8 * len(core)
    out = {"run": run.name, "population": len(population), "core_size": len(core),
           "stable": bool(stable), "core": sorted(core),
           "kept_from_earlier": len(core & earlier)}
    if not stable:
        return out
    T = product_table(population, run)
    index = {e: i for i, e in enumerate(population)}
    core_idx = np.array(sorted(index[e] for e in core))
    out["projection_share"] = sum(bool(PROJECTION.match(e)) for e in core) / len(core)
    sub = T[np.ix_(core_idx, core_idx)].astype(np.int64)
    position = {int(v): k for k, v in enumerate(core_idx)}
    core_table = np.array([[position.get(int(v), -2) if v != -1 else -1 for v in row]
                           for row in sub], dtype=np.int64)
    out["core_table"] = core_table.tolist()
    inside = core_table >= 0
    out["core_entries_in_core"] = int(inside.sum())
    out["core_entries_elastic"] = int((core_table == -1).sum())
    out["core_entries_outside"] = int((core_table == -2).sum())
    out["core_closed_under_itself"] = bool(closure(
        np.isin(np.arange(len(population)), core_idx), T)[core_idx].all())
    sets = generating_sets(T, core_idx, rng)
    smallest = min(sets, key=len)
    out["generating_set_sizes"] = sorted(len(s) for s in sets)
    out["generating_set_unique"] = len(set(sets)) == 1
    out["distinct_generating_sets"] = len(set(sets))
    out["smallest_generating_set"] = [population[i] for i in sorted(smallest)]
    out["smallest_in_core"] = sum(population[i] in core for i in smallest)
    return out


def _one(job):
    k, run = job
    return analyse_run(run, random.Random(20261121 + k))


def main() -> None:
    runs_dir, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    runs = [run for run in sorted(runs_dir.glob("r*")) if (run / "s100").exists()]
    with Pool(2) as pool:
        results = pool.map(_one, list(enumerate(runs)))
    stable = [r for r in results if r["stable"]]
    pairs = []
    for a, b in combinations(stable, 2):
        identical = a["core"] == b["core"]
        strict = "yes" if identical else isomorphic(np.array(a["core_table"]),
                                                    np.array(b["core_table"]))
        pairs.append({"a": a["run"], "b": b["run"], "identical": identical, "strict": strict})
    out_path.write_text(json.dumps({"runs": results, "pairs": pairs}, indent=1) + "\n")
    print(f"{len(results)} runs, {len(stable)} stable, {len(pairs)} pairs")


if __name__ == "__main__":
    main()
