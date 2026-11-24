"""Second run: ladder test, single generators and regrowth, as fixed in DEFINITIONS-2.md.

Written by Claude, 21 November 2026.  Usage:
    python3 analyse2.py RUNS_DIR INPUT_TEMPLATE OUT.json [--regrow]
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyse as an  # noqa: E402

ALCHEMY = os.environ.get("ALCHEMY_BIN", "ALCHEMY")   # the compiled original program
LEADING = re.compile(r"^((?:\\x\d+\.)+)")


def leading(expr: str) -> int:
    return LEADING.match(expr).group(1).count("\\")


def sorted_table(core: list[str], table: np.ndarray):
    order = sorted(range(len(core)), key=lambda i: (leading(core[i]), len(core[i])))
    pos = {old: new for new, old in enumerate(order)}
    S = np.array([[pos[int(v)] if v >= 0 else int(v) for v in table[i, order]] for i in order])
    return order, S


def is_ladder(core: list[str], table: np.ndarray) -> bool:
    m = len(core)
    if m < 3:
        return False
    order, S = sorted_table(core, table)
    lengths = [leading(core[i]) for i in order]
    if lengths != list(range(lengths[0], lengths[0] + m)):
        return False
    return all((v == i - 1) or (v == -1 and j == i - 1)
               for i in range(1, m) for j, v in enumerate(S[i]))


def analyse_run(run: Path) -> dict:
    final = an.read_snapshot(run / "s100")
    population = sorted(final)
    core_set = an.core_at(run, 100)
    earlier = an.core_at(run, 90)
    stable = len(core_set) >= 2 and len(core_set & earlier) >= 0.8 * len(core_set)
    out = {"run": run.name, "population": len(population), "core_size": len(core_set),
           "stable": bool(stable), "kept_from_earlier": len(core_set & earlier)}
    if not stable:
        return out
    T = an.product_table(population, run)
    index = {e: i for i, e in enumerate(population)}
    core = sorted(core_set)
    core_idx = np.array([index[e] for e in core])
    position = {int(v): k for k, v in enumerate(core_idx)}
    sub = T[np.ix_(core_idx, core_idx)]
    table = np.array([[position.get(int(v), -2) if v != -1 else -1 for v in row] for row in sub])
    order, S = sorted_table(core, table)
    singles = []
    for k, i in enumerate(core_idx):
        seed = np.zeros(len(population), dtype=bool)
        seed[i] = True
        if an.closure(seed, T, core_idx)[core_idx].all():
            singles.append(core[k])
    out.update({
        "core": core,
        "ladder": is_ladder(core, table),
        "share_inside_core": float((table >= 0).mean()),
        "leading_abstractions": [leading(core[i]) for i in order],
        "first_row": [int(v) for v in S[0]],
        "single_generators": singles,
        "single_generator_share": len(singles) / len(core),
        "core_in_order": [core[i] for i in order],
    })
    return out


def regrow(result: dict, template: str, workdir: Path) -> float | None:
    in_order = [e for e in result["core_in_order"] if e in set(result["single_generators"])]
    if not in_order:
        return None
    workdir.mkdir(parents=True, exist_ok=True)
    (workdir / "seed.txt").write_text(f"{in_order[0]} {{0 1000 0}}\n")
    inp = (template.replace("name of simulation =  t", "name of simulation =  g")
           .replace("random seed =  999", "random seed =  4242")
           .replace("number of collisions to perform =  100000",
                    "number of collisions to perform =  200000")
           .replace("snapshot interval =  5000", "snapshot interval =  20000")
           .replace("file with initial objects = NULL-1000",
                    "file with initial objects = seed.txt"))
    assert "seed.txt" in inp and "4242" in inp
    (workdir / "g.inp").write_text(inp)
    subprocess.run([ALCHEMY, "-f", "g.inp"], cwd=workdir,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    final = an.read_snapshot(workdir / "g10")
    return sum(final.get(e, 0) >= 2 for e in result["core"]) / len(result["core"])


def main() -> None:
    runs_dir, template, out_path = Path(sys.argv[1]), Path(sys.argv[2]).read_text(), Path(sys.argv[3])
    results = [analyse_run(run) for run in sorted(runs_dir.glob("[qr]*"))
               if (run / "s100").exists()]
    stable = [r for r in results if r["stable"]]
    if "--regrow" in sys.argv:
        for r in stable:
            if r["ladder"]:
                r["regrown_share"] = regrow(r, template, runs_dir.parent / "regrow2" / r["run"])
    pairs = [{"a": a["run"], "b": b["run"], "identical": a["core"] == b["core"],
              "shared_single_generators": len(set(a["single_generators"]) & set(b["single_generators"]))}
             for a, b in combinations(stable, 2)]
    out_path.write_text(json.dumps({"runs": results, "pairs": pairs}, indent=1) + "\n")
    print(f"{len(results)} runs, {len(stable)} stable, "
          f"{sum(r['ladder'] for r in stable)} ladders, {len(pairs)} pairs")


if __name__ == "__main__":
    main()
