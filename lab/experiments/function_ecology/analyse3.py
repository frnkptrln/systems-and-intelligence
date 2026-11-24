"""Third step: lowerers, bundles, generating sets and regrowth.

Written by Claude, 22 November 2026.  Usage:
    python3 analyse3.py OUT.json TEMPLATE REGROW_DIR RUNS_DIR [RUNS_DIR ...]
"""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyse as an  # noqa: E402
import analyse2 as a2  # noqa: E402

PROJECTION = re.compile(r"^(\\x[0-9]+\.)+x[0-9]+$")
TWO_CORE = sorted(["\\x1.\\x2.x2", "\\x1.x1"])
K = "\\x1.\\x2.x1"


def lowerers(core_in_order: list[str], S: np.ndarray) -> list[int]:
    """Members whose row is one constant member a level down, elastic exactly where
    that product would be a copy, and nowhere outside the core."""
    level = [a2.leading(e) for e in core_in_order]
    found = []
    for i in range(len(core_in_order)):
        row = S[i]
        targets = set(int(v) for v in row if v >= 0)
        if len(targets) != 1:
            continue
        p = targets.pop()
        if level[p] != level[i] - 1:
            continue
        if (row == -2).any():
            continue
        elastic = np.flatnonzero(row == -1)
        if elastic.tolist() != [p]:
            continue
        found.append(i)
    return found


def analyse_run(run: Path, rng: random.Random) -> dict:
    final = an.read_snapshot(run / "s100")
    population = sorted(final)
    core_set = an.core_at(run, 100)
    earlier = an.core_at(run, 90)
    stable = len(core_set) >= 2 and len(core_set & earlier) >= 0.8 * len(core_set)
    out = {"run": run.name, "population": len(population), "core_size": len(core_set),
           "stable": bool(stable)}
    if not stable:
        return out
    T = an.product_table(population, run)
    index = {e: i for i, e in enumerate(population)}
    core = sorted(core_set)
    core_idx = np.array([index[e] for e in core])
    position = {int(v): k for k, v in enumerate(core_idx)}
    sub = T[np.ix_(core_idx, core_idx)]
    table = np.array([[position.get(int(v), -2) if v != -1 else -1 for v in row] for row in sub])
    order, S = a2.sorted_table(core, table)
    in_order = [core[i] for i in order]
    low = lowerers(in_order, S)
    sets = an.generating_sets(T, core_idx, rng)
    smallest = min(sets, key=len)
    out.update({
        "core": core,
        "ladder": a2.is_ladder(core, table),
        "lowerers": len(low),
        "lowerer_share": len(low) / len(core),
        "bundle": len(low) > len(core) / 2,
        "share_inside_core": float((table >= 0).mean()),
        "smallest_generating_set": [population[i] for i in sorted(smallest)],
        "generating_set_size": len(smallest),
        "two_core": core == TWO_CORE,
        "k_ladder": bool(a2.is_ladder(core, table) and in_order[0] == K
                         and all(PROJECTION.match(e) for e in core)),
    })
    return out


def regrow(result: dict, template: str, workdir: Path) -> float:
    gens = result["smallest_generating_set"]
    workdir.mkdir(parents=True, exist_ok=True)
    per = 1000 // len(gens)
    (workdir / "seed.txt").write_text("".join(f"{g} {{{k} {per} 0}}\n" for k, g in enumerate(gens)))
    inp = (template.replace("name of simulation =  t", "name of simulation =  g")
           .replace("random seed =  999", "random seed =  4242")
           .replace("number of collisions to perform =  100000",
                    "number of collisions to perform =  200000")
           .replace("snapshot interval =  5000", "snapshot interval =  20000")
           .replace("file with initial objects = NULL-1000",
                    "file with initial objects = seed.txt"))
    assert "seed.txt" in inp and "4242" in inp
    (workdir / "g.inp").write_text(inp)
    subprocess.run([a2.ALCHEMY, "-f", "g.inp"], cwd=workdir,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    final = an.read_snapshot(workdir / "g10")
    return sum(final.get(e, 0) >= 2 for e in result["core"]) / len(result["core"])


def main() -> None:
    out_path, template, regrow_dir = Path(sys.argv[1]), Path(sys.argv[2]).read_text(), Path(sys.argv[3])
    runs = [run for d in sys.argv[4:] for run in sorted(Path(d).glob("[a-z][0-9][0-9]"))
            if (run / "s100").exists()]
    results = [analyse_run(run, random.Random(20261122 + k)) for k, run in enumerate(runs)]
    for r in results:
        if r["stable"] and r["bundle"]:
            r["regrown_share"] = regrow(r, template, regrow_dir / r["run"])
    out_path.write_text(json.dumps({"runs": results}, indent=1) + "\n")
    stable = [r for r in results if r["stable"]]
    print(f"{len(results)} runs, {len(stable)} stable, {sum(r['bundle'] for r in stable)} bundles")


if __name__ == "__main__":
    main()
