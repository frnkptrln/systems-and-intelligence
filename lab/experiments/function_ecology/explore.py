"""Exploration of the stable cores that fail the ladder test (development data only)."""
import sys, json, re
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyse as an, analyse2 as a2

def load(run: Path):
    final = an.read_snapshot(run / "s100"); pop = sorted(final)
    core = sorted(an.core_at(run, 100))
    T = an.product_table(pop, run); idx = {e: i for i, e in enumerate(pop)}
    ci = np.array([idx[e] for e in core]); position = {int(v): k for k, v in enumerate(ci)}
    sub = T[np.ix_(ci, ci)]
    table = np.array([[position.get(int(v), -2) if v != -1 else -1 for v in row] for row in sub])
    order, S = a2.sorted_table(core, table)
    return [core[i] for i in order], S

if __name__ == "__main__":
    for name in sys.argv[1:]:
        run = Path("runs2" if name.startswith("q") else "runs") / name
        core, S = load(run); m = len(core)
        lev = [a2.leading(e) for e in core]
        print(f"\n{name}: {m} members, levels {lev}")
        const = 0
        for i in range(m):
            vals = sorted(set(int(v) for v in S[i] if v >= 0))
            kind = "const" if len(vals) == 1 else ("none" if not vals else "varied")
            const += kind == "const"
            row = " ".join(f"{v:2d}" if v >= 0 else (" ." if v == -1 else " o") for v in S[i])
            tgt = f"-> {vals[0]} (level {lev[vals[0]]})" if kind == "const" else ""
            print(f"  {i:2d} L{lev[i]:<2d} {kind:6} {row}  {tgt}")
        print(f"  constant rows: {const} of {m}")
