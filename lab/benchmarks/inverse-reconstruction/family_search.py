"""
family_search.py

Family search: the wall, measured. (Benchmark v1, part 2)

THE QUESTION.  Benchmark v0 showed that recovering a generator is cheap when
the MODEL FAMILY is known — fit parameters, done. The spine's hardness claim
was therefore relocated to *family search*: finding the generator when the
hypothesis space is a space of programs, not a parameter vector. This module
measures that wall in the smallest honest setting.

THE SETUP.  Target generators: the 256 elementary CA rules. Hypothesis space:
a DSL of boolean formulas over the neighborhood variables (l, c, r) with
operators NOT, AND, OR, XOR. Every rule is expressible (the DSL is complete
for 3-variable boolean functions); each rule therefore has a MINIMAL
DESCRIPTION SIZE — the node count of its shortest formula. Rule 90 is
XOR(l, r): size 3. Rule 110 needs a deeper formula. The minimal size is the
DSL-relative Kolmogorov complexity of the rule, and it is exactly computable
here (which is the point of the toy: in general it is uncomputable).

TWO MEASUREMENTS.

  A. THE SEARCH WALL.  An exhaustive enumerator generates candidate formulas
     in size order and tests each against the trace. Testing one candidate
     costs 8 bit-comparisons — flat, tiny: VERIFICATION IS CHEAP. But the
     number of candidates that must be generated before reaching size m grows
     exponentially in m (counted exactly by recurrence, no enumeration
     needed): CONSTRUCTION IS EXPENSIVE, and the cost is set by the *target's
     description complexity*, not by the data. This is the P-vs-NP shape of
     the spine, drawn from a real (if small) system: cost-to-find grows like
     the candidate stream; cost-to-check stays at 8 operations.

  B. OCCAM UNDER PARTIAL COVERAGE.  When the trace exercises only k of the 8
     neighborhoods, many formulas are consistent with everything seen. The
     searcher returns the MINIMAL consistent one — selection by elegance,
     exactly the move `theory/computation/construction-vs-deduction.md`
     claims we perform on the world ("the world-as-modeled is chosen from the
     equivalence class by criteria that are ours"). Here that claim becomes a
     curve: how often does the most elegant consistent generator equal the
     true one, as a function of coverage k? Occam is a *prior*, and priors
     can be wrong; this measures how wrong, where.

WHAT THIS DOES NOT SHOW.  This is exhaustive search in a complete, tiny DSL —
the FLOOR of family search, not a model of intelligent search. Whether
learned searchers (LLMs, program synthesizers) beat the enumeration floor,
and by how much, is exactly the open real-model question; this testbed
provides the baseline they must beat. (Levin search formalizes the
enumeration strategy; Rissanen's MDL formalizes the Occam selection. See the
README's related-work pointers.)

Usage::

    python family_search.py            # console summary
    python family_search.py --save     # also write the figure (to lab/tools/)

Related:
- inverse_benchmark.py / intervention_experiment.py   (v0, v1.1)
- theory/computation/construction-vs-deduction.md     (elegance as selection)
- theory/computation/p-vs-np-as-generator-search.md   (the formal shadow)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

# Truth tables as uint8 bitmasks over neighborhood patterns p = (l<<2)|(c<<1)|r.
VAR_L, VAR_C, VAR_R = 0b11110000, 0b11001100, 0b10101010
MASK8 = 0xFF


# ════════════════ Minimal description size (semantic DP) ════════════
def minimal_sizes(max_size: int = 15) -> dict[int, int]:
    """min_size[table] = node count of the shortest DSL formula computing it.

    Dynamic programming over DISTINCT truth tables (≤256), exact. Formula
    size = number of nodes (leaves + operators).
    """
    by_size: dict[int, set[int]] = {1: {VAR_L, VAR_C, VAR_R}}
    best: dict[int, int] = {t: 1 for t in by_size[1]}
    for n in range(2, max_size + 1):
        new: set[int] = set()
        # NOT(f), f of size n-1
        for t in by_size.get(n - 1, ()):
            cand = (~t) & MASK8
            if cand not in best:
                new.add(cand)
        # (f op g), size(f) + size(g) = n - 1
        for a in range(1, n - 1):
            b = n - 1 - a
            for ta in by_size.get(a, ()):
                for tb in by_size.get(b, ()):
                    for cand in (ta & tb, ta | tb, ta ^ tb):
                        if cand not in best:
                            new.add(cand)
        for t in new:
            best[t] = n
        by_size[n] = new
        if len(best) == 256:
            break
    return best


def stream_sizes(max_size: int = 15) -> list[int]:
    """s[n] = number of SYNTACTIC formulas of size n (with semantic duplicates).

    Exact recurrence: s(1) = 3 (variables); s(n) = s(n-1) [NOT]
    + 3 * sum_{a+b=n-1} s(a)·s(b) [AND/OR/XOR over ordered pairs].
    The cumulative sum up to size m is the number of candidates an exhaustive
    size-ordered enumerator must GENERATE before it has seen all of size m —
    the construction cost. Each candidate costs 8 bit-comparisons to verify.
    """
    s = [0] * (max_size + 1)
    s[1] = 3
    for n in range(2, max_size + 1):
        total = s[n - 1]
        for a in range(1, n - 1):
            total += 3 * s[a] * s[n - 1 - a]
        s[n] = total
    return s


# ════════════════ Part B: Occam under partial coverage ══════════════
def occam_pick(true_rule: int, mask: int, best: dict[int, int]) -> tuple[int, int, int]:
    """The most elegant consistent generator for a partially observed rule.

    mask: bitmask of OBSERVED neighborhood patterns. A table t is consistent
    iff it agrees with true_rule on every observed pattern. Returns
    (picked_table, n_min_size_ties, consistent_count). Pick = canonical
    (lowest table value) among minimal-size consistent tables — a fixed,
    documented tie-break.
    """
    consistent = [t for t in range(256)
                  if (t & mask) == (true_rule & mask)]
    msize = min(best[t] for t in consistent)
    ties = [t for t in consistent if best[t] == msize]
    return min(ties), len(ties), len(consistent)


def run_occam_suite(best: dict[int, int], n_masks: int = 40,
                    seed: int = 0) -> dict:
    """P(most-elegant consistent table == truth) vs coverage k.

    Reported three ways: over ALL 256 rules (uniform prior on generators),
    over SIMPLE targets (min size ≤ 4), and over COMPLEX targets (min size
    ≥ 7). The split is the finding: under a uniform world, elegance is no
    better than chance within the consistent class; it pays exactly when the
    world itself is biased toward simplicity.
    """
    rng = np.random.default_rng(seed)
    ks = list(range(3, 9))
    simple = [r for r in range(256) if best[r] <= 4]
    complx = [r for r in range(256) if best[r] >= 7]
    out = {"k": ks, "hit": [], "hit_simple": [], "hit_complex": [],
           "class": [], "n_simple": len(simple), "n_complex": len(complx)}
    for k in ks:
        hits, hits_s, hits_c, classes = [], [], [], []
        for rule in range(256):
            for _ in range(n_masks):
                pats = rng.choice(8, size=k, replace=False)
                mask = 0
                for p in pats:
                    mask |= (1 << int(p))
                pick, ties, ccount = occam_pick(rule, mask, best)
                hit = (pick == rule)
                hits.append(hit)
                classes.append(ccount)
                if best[rule] <= 4:
                    hits_s.append(hit)
                elif best[rule] >= 7:
                    hits_c.append(hit)
        out["hit"].append(float(np.mean(hits)))
        out["hit_simple"].append(float(np.mean(hits_s)))
        out["hit_complex"].append(float(np.mean(hits_c)))
        out["class"].append(float(np.mean(classes)))
    return out


def orbit_mask(rule: int, W: int = 200, T: int = 200) -> int:
    """Observed-neighborhood mask of the single-seed orbit (cf. v0/v1.1)."""
    bits = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    row = np.zeros(W, dtype=np.uint8)
    row[W // 2] = 1
    mask = 0
    for _ in range(T):
        r = row.astype(int)
        nb = (np.roll(r, 1) << 2) | (r << 1) | np.roll(r, -1)
        for p in np.unique(nb):
            mask |= (1 << int(p))
        row = bits[nb]
    return mask


# ════════════════ Reporting ═════════════════════════════════════════
def print_summary(best: dict[int, int], s: list[int], occ: dict) -> None:
    sizes = np.array([best[r] for r in range(256)])
    cum = np.cumsum(s)
    print("=" * 70)
    print("  FAMILY SEARCH — the wall, measured (DSL: NOT/AND/OR/XOR over l,c,r)")
    print("=" * 70)
    print("\n[A] Minimal description size of the 256 rules, and the search wall")
    print(f"    size distribution: " + "  ".join(
        f"m={m}:{int((sizes == m).sum())}" for m in range(1, sizes.max() + 1)
        if (sizes == m).any()))
    print(f"    exhaustive-enumeration cost to REACH size m (candidates):")
    for m in sorted(set(sizes.tolist())):
        print(f"      m={m:>2}: ≤{cum[m]:>12,} candidates   "
              f"(verification per candidate: 8 ops, flat)")
    for rule, name in ((90, "XOR(l,r)"), (30, "l XOR (c OR r)"), (110, "—"),
                       (0, "const-0")):
        print(f"    rule {rule:>3}: min size {best[rule]:>2}  "
              f"→ search cost ≤{cum[best[rule]]:,}   ({name})")
    print("\n[B] Occam under partial coverage "
          "(pick = minimal consistent formula):")
    print("    all 256 rules (uniform world):   " +
          "  ".join(f"k={k}: {h:.0%}" for k, h in zip(occ["k"], occ["hit"])))
    print(f"    simple targets (m≤4, n={occ['n_simple']}):      " +
          "  ".join(f"k={k}: {h:.0%}" for k, h in
                    zip(occ["k"], occ["hit_simple"])))
    print(f"    complex targets (m≥7, n={occ['n_complex']}):    " +
          "  ".join(f"k={k}: {h:.0%}" for k, h in
                    zip(occ["k"], occ["hit_complex"])))
    print("    mean consistent-class size:       " +
          "  ".join(f"k={k}: {c:.0f}" for k, c in zip(occ["k"], occ["class"])))
    print("    NOTE: over the uniform world, the all-rules hit rate equals")
    print("    1/class — elegance is chance there. It pays exactly when the")
    print("    world itself is biased toward simplicity.")
    print("\n    single-seed orbit anecdotes:")
    for rule in (90, 0):
        m = orbit_mask(rule)
        k = bin(m).count("1")
        pick, ties, ccount = occam_pick(rule, m, best)
        verdict = "TRUE rule" if pick == rule else f"IMPOSTER (rule {pick})"
        print(f"      rule {rule:>3}: orbit covers {k}/8 patterns; "
              f"{ccount} consistent; most elegant = {verdict} "
              f"(min size {best[pick]}, {ties} tie(s))")
    print("\nReading: verification stays at 8 operations while construction")
    print("cost grows exponentially with the target's description size — the")
    print("P-vs-NP shape, drawn from a real enumeration. Under partial")
    print("coverage, elegance (minimal consistent description) is a prior:")
    print("strong but fallible, and measurably so. This is the FLOOR that")
    print("any intelligent searcher — including a language model — must beat.")


def _repo_lab_tools() -> Path:
    return Path(__file__).resolve().parents[2] / "tools"


def figure(best: dict[int, int], s: list[int], occ: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sizes = np.array([best[r] for r in range(256)])
    cum = np.cumsum(s)
    ms = sorted(set(sizes.tolist()))

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.0))

    axA.semilogy(ms, [cum[m] for m in ms], "o-", color="#d62728", lw=2,
                 label="construction: candidates enumerated\nto reach size m (exhaustive search)")
    axA.axhline(8, ls="--", color="#2ca02c", lw=2,
                label="verification: 8 ops per candidate (flat)")
    for rule, dx, dy in ((90, 0.15, 0.4), (30, 0.15, 0.4), (110, -1.3, 2.5)):
        m = best[rule]
        axA.annotate(f"rule {rule}", (m, cum[m]),
                     textcoords="offset fontsize", xytext=(dx, dy), fontsize=8)
        axA.scatter([m], [cum[m]], color="k", zorder=5, s=18)
    axA.set_xlabel("minimal description size m of the target rule (DSL nodes)")
    axA.set_ylabel("candidates / operations (log)")
    axA.set_title("(a) The family-search wall: finding grows exponentially\n"
                  "with target complexity; checking stays flat")
    axA.legend(fontsize=8, loc="center right")
    axA.grid(alpha=0.3)

    axB.plot(occ["k"], occ["hit_simple"], "o-", color="#2ca02c", lw=2,
             label=f"simple targets (m≤4, n={occ['n_simple']})")
    axB.plot(occ["k"], occ["hit"], "s-", color="#1f77b4", lw=2,
             label="all 256 rules (uniform world) — equals 1/class: chance")
    axB.plot(occ["k"], occ["hit_complex"], "v-", color="#d62728", lw=2,
             label=f"complex targets (m≥7, n={occ['n_complex']})")
    axB.set_xlabel("coverage k (neighborhoods observed, of 8)")
    axB.set_ylabel("P(most elegant consistent = true rule)")
    axB.set_ylim(-0.03, 1.05)
    axB.set_title("(b) Elegance is a prior, and the measurement shows whom\n"
                  "it serves: simple worlds — and systematically not complex ones")
    axB.legend(fontsize=8, loc="upper left")
    axB.grid(alpha=0.3)

    fig.suptitle("Family search (benchmark v1.2) — the hardness the spine claimed, "
                 "as two curves", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    out = outdir / "inverse_benchmark_family_search.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Family-search testbed (benchmark v1, part 2).")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("-o", "--output", type=str, default=None)
    args = parser.parse_args()

    best = minimal_sizes()
    s = stream_sizes()
    occ = run_occam_suite(best)
    print_summary(best, s, occ)

    if args.save:
        outdir = Path(args.output) if args.output else _repo_lab_tools()
        outdir.mkdir(parents=True, exist_ok=True)
        print(f"\nWriting figure to {outdir} …")
        print(f"  {figure(best, s, occ, outdir)}")


if __name__ == "__main__":
    main()
