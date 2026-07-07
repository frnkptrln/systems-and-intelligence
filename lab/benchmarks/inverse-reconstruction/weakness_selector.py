"""
weakness_selector.py

Weakness vs. simplicity: the Bennett bridge. (Benchmark v1.4)

THE QUESTION.  Bennett's Stack Theory result ("The Optimal Choice of
Hypothesis Is the Weakest, Not the Shortest", 2023; Exp. 1 of "No Selves,
No Consciousness", 2026) claims the generalisation-optimal selector holds
the WEAKEST consistent hypothesis — the one leaving the most future
completions open — not the SHORTEST. On this testbed the weakest consistent
hypothesis has a familiar face: it is the PARTIAL RULE that asserts exactly
the observed neighborhoods and stays silent on the rest — i.e. **the
uncollapsed consistent-generator equivalence class itself** (v0/v1.1's
object). The shortest consistent hypothesis is v1.2's Occam pick: one full
rule, minimal DSL description. So Bennett's claim is testable on our own
generator: what does committing to the elegant member COST, relative to
holding the class, as a function of what kind of world the rules come from?

THE SETUP.  Worlds are priors over the 256 elementary CA rules, reusing
v1.2's split: SIMPLE (min DSL size <= 4), UNIFORM (all 256), COMPLEX
(min size >= 7). Per episode: draw the true rule from the world, observe k
of 8 neighborhoods (u = 8-k unseen; class size 2^u). Selectors:

  simpmax — v1.2's occam_pick: the minimal-description consistent FULL rule
            (commits to all u unseen bits).
  wmax    — the weakest consistent statement: the partial rule / the class.
            Commits to nothing; when FORCED to bet on unseen bits, flips
            coins (that is what "no commitment" means at the betting window).
  bayes   — oracle knowing the world prior: per-bit majority vote over the
            class ∩ world-support (upper bound reference).

TWO CURRENCIES (the ledger).  A selector can pay in two ways:
  - uncertainty HELD OPEN: wmax holds u bits; simpmax holds 0.
  - survival odds PAID: P(committed statement remains true when all 8
    neighborhoods are eventually seen). wmax's statement survives with
    certainty; simpmax survives only if its pick IS the truth, so it pays
    -log2 P(hit) bits of odds.
  COMMITMENT EFFICIENCY := u + log2 P(hit) — bits of uncertainty closed
  minus odds-bits paid. Positive: committing is profitable compression.
  Zero: neutral. Negative: the commitment costs more than the uncertainty
  it removes. (Laplace smoothing (hits+1)/(N+2) keeps log2 finite where the
  measured hit rate is 0; affected cells are marked in the output.)

PREDICTIONS (stated before the first run, per the repo's habit):
  P1  Efficiency ordering: > 0 on the simple world; = 0 on the uniform
      world (analytic: v1.2 measured hit = 1/class = 2^-u there); < 0 on
      the complex world at low-to-mid coverage. If the uniform world comes
      out far from 0 or the ordering breaks, the Bennett convergence is
      superficial and the related-work row must be corrected.
  P2  Wrong-bits crossover: simpmax's expected wrong unseen bits < u/2 on
      simple, ~ u/2 on uniform, > u/2 on complex — on complexity-biased
      worlds committing to the elegant member is worse than admitting
      ignorance (a coin).
  P3  Support violation: on the complex world, simpmax's pick frequently
      lies OUTSIDE the world's support — probability-zero under the prior.
      Elegance does not merely miss there; it asserts impossible generators.

RELATION TO v1.2 AND v1.3.  v1.2 measured WHOM the simplicity prior serves
(hit-rate curves). This experiment prices the same behaviour in Bennett's
currency (survival odds vs. held uncertainty) and adds the weakest-hypothesis
selector as the explicit alternative. v1.3 is the downstream disease: what
happens when committed-but-unmarked guesses are consumed by an argmax (the
exploitation wedge). wmax is the accounting discipline that prevents exactly
that consumption — "mark what the traces actually determine"
(theory/core/measurement-as-weak-intervention.md).

WHAT THIS DOES NOT SHOW.  Nothing here tests Stack Theory's consciousness
claims (selves, do/see tagging, binding) — only its selector principle, on
one toy family. And "weakness wins on uniform worlds" is partly definitional
(wmax is Bayes-optimal under a uniform extension prior by construction);
the measured content is the SIZE of the gap, its world-dependence, and the
support-violation rate.

Usage::

    python weakness_selector.py            # console summary
    python weakness_selector.py --save     # also write the figure (to lab/tools/)

Related:
- family_search.py                                     (v1.2: the Occam side)
- model_exploitation.py                                (v1.3: the downstream cost)
- theory/core/measurement-as-weak-intervention.md      (the accounting rule)
- meta/research-alignment/related-work-map.md          (Stack Theory row)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from family_search import minimal_sizes

# BITS[t, p] = bit p of rule table t.
BITS = ((np.arange(256)[:, None] >> np.arange(8)[None, :]) & 1).astype(np.uint8)
TABLES = np.arange(256)


def run_weakness_suite(best: dict[int, int], n_masks: int = 40,
                       seed: int = 0) -> dict:
    """Ledger metrics for simpmax / wmax / bayes across worlds and coverage."""
    rng = np.random.default_rng(seed)
    best_arr = np.array([best[t] for t in range(256)])
    worlds = {
        "simple": np.array([r for r in range(256) if best[r] <= 4]),
        "uniform": np.arange(256),
        "complex": np.array([r for r in range(256) if best[r] >= 7]),
    }
    ks = [3, 4, 5, 6, 7]
    out: dict = {"k": ks, "worlds": {}}
    for wname, support in worlds.items():
        in_support = np.zeros(256, dtype=bool)
        in_support[support] = True
        res = {"n": len(support), "hit_simp": [], "hit_bayes": [], "chance": [],
               "wrong_simp": [], "wrong_bayes": [], "wrong_coin": [],
               "eff_simp": [], "support_rate": [], "floored": []}
        for k in ks:
            u = 8 - k
            hits_s, hits_b, wr_s, wr_b, wr_c, sup = [], [], [], [], [], []
            for rule in support:
                for _ in range(n_masks):
                    pats = rng.choice(8, size=k, replace=False)
                    mask = 0
                    for p in pats:
                        mask |= (1 << int(p))
                    unseen = np.array([p for p in range(8)
                                       if not (mask >> p) & 1])
                    cls = (TABLES & mask) == (rule & mask)
                    # simpmax: canonical minimal-size consistent table (= v1.2)
                    cls_idx = TABLES[cls]
                    msize = best_arr[cls_idx].min()
                    pick = int(cls_idx[best_arr[cls_idx] == msize].min())
                    truth_bits = BITS[rule, unseen]
                    wr_s.append(int((BITS[pick, unseen] != truth_bits).sum()))
                    hits_s.append(pick == rule)
                    sup.append(bool(in_support[pick]))
                    # wmax forced bet: coins on the unseen bits
                    wr_c.append(int((rng.integers(0, 2, size=u).astype(np.uint8)
                                     != truth_bits).sum()))
                    # bayes oracle: majority per unseen bit over class ∩ support
                    cs = cls & in_support
                    freq = BITS[cs][:, unseen].mean(axis=0)
                    bet = (freq > 0.5).astype(np.uint8)
                    tie = freq == 0.5
                    if tie.any():
                        bet[tie] = rng.integers(0, 2, size=int(tie.sum()))
                    wr_b.append(int((bet != truth_bits).sum()))
                    hits_b.append(1.0 / cs.sum())  # expected exact-hit, MAP tie-broken
            n_ep = len(hits_s)
            hit_s = float(np.mean(hits_s))
            res["hit_simp"].append(hit_s)
            res["hit_bayes"].append(float(np.mean(hits_b)))
            res["chance"].append(2.0 ** -u)
            res["wrong_simp"].append(float(np.mean(wr_s)))
            res["wrong_bayes"].append(float(np.mean(wr_b)))
            res["wrong_coin"].append(float(np.mean(wr_c)))
            smoothed = (np.sum(hits_s) + 1) / (n_ep + 2)
            res["eff_simp"].append(u + float(np.log2(smoothed)))
            res["floored"].append(np.sum(hits_s) == 0)
            res["support_rate"].append(float(np.mean(sup)))
        out["worlds"][wname] = res
    return out


# ════════════════ Reporting ═════════════════════════════════════════
def print_summary(out: dict) -> None:
    ks = out["k"]
    print("=" * 70)
    print("  WEAKNESS vs SIMPLICITY — the Bennett bridge (benchmark v1.4)")
    print("=" * 70)
    print("\nwmax (weakest consistent = the uncollapsed class) pays 0 odds-bits")
    print("and holds u = 8-k bits open, in every world, by construction.")
    print("simpmax (shortest consistent member) closes all u bits; the ledger")
    print("below prices that commitment per world.\n")
    for wname, res in out["worlds"].items():
        print(f"[{wname.upper()} world]  (n_rules = {res['n']})")
        print("    commitment efficiency (u + log2 P(hit); >0 profitable, "
              "<0 harmful):")
        print("      " + "  ".join(
            f"k={k}: {e:+.2f}{'*' if f else ''}"
            for k, e, f in zip(ks, res["eff_simp"], res["floored"])))
        print("    wrong unseen bits, simpmax vs coin (=u/2) vs bayes oracle:")
        print("      " + "  ".join(
            f"k={k}: {ws:.2f}/{wc:.2f}/{wb:.2f}"
            for k, ws, wc, wb in zip(ks, res["wrong_simp"],
                                     res["wrong_coin"], res["wrong_bayes"])))
        print("    exact-hit simpmax vs chance (=2^-u):   " + "  ".join(
            f"k={k}: {h:.0%}/{c:.0%}" for k, h, c in
            zip(ks, res["hit_simp"], res["chance"])))
        print("    P(simpmax pick inside world support):  " + "  ".join(
            f"k={k}: {s:.0%}" for k, s in zip(ks, res["support_rate"])))
        print()
    print("(* = zero measured hits; efficiency shown with Laplace floor, true")
    print("value is more negative.)")
    print("\nReading: the efficiency row is the exchange rate between the two")
    print("currencies — bits of uncertainty closed vs odds-bits paid. Where it")
    print("is ~0 (uniform world), committing buys nothing: the elegant member")
    print("is a guess dressed as an answer. Where it is negative (complex")
    print("world), the guess costs more than the ignorance it hides — and the")
    print("support row shows elegance asserting generators the world cannot")
    print("even contain. Holding the class (wmax) is exactly the discipline")
    print("v1.3 showed the exploiting planner lacks: mark what the traces")
    print("actually determine.")


def _repo_lab_tools() -> Path:
    return Path(__file__).resolve().parents[2] / "tools"


def figure(out: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ks = out["k"]
    # entity colors held fixed across the benchmark's figures (= v1.2 panel b)
    style = {"simple": ("#2ca02c", "o-"), "uniform": ("#1f77b4", "s-"),
             "complex": ("#d62728", "v-")}
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.0))

    for wname, res in out["worlds"].items():
        col, fmt = style[wname]
        label = f"{wname} world (n={res['n']})"
        axA.plot(ks, res["eff_simp"], fmt, color=col, lw=2, label=label)
        if any(res["floored"]):
            fk = [k for k, f in zip(ks, res["floored"]) if f]
            fe = [e for e, f in zip(res["eff_simp"], res["floored"]) if f]
            axA.scatter(fk, fe, facecolors="none", edgecolors=col, s=140,
                        zorder=5)
    axA.axhline(0, ls="--", color="k", lw=1.5,
                label="wmax: hold the class (0 by construction)")
    axA.set_xlabel("coverage k (neighborhoods observed, of 8)")
    axA.set_ylabel("commitment efficiency  u + log₂ P(hit)  (bits)")
    axA.set_title("(a) What committing to the elegant member buys:\n"
                  "profit on simple worlds, nothing on uniform, loss on complex")
    axA.legend(fontsize=8, loc="lower right")
    axA.set_xticks(ks)
    axA.grid(alpha=0.3)

    for wname, res in out["worlds"].items():
        col, fmt = style[wname]
        penalty = [ws - wc for ws, wc in zip(res["wrong_simp"],
                                             res["wrong_coin"])]
        axB.plot(ks, penalty, fmt, color=col, lw=2,
                 label=f"{wname} world (n={res['n']})")
    axB.axhline(0, ls="--", color="k", lw=1.5,
                label="coin on unseen bits (admitted ignorance)")
    axB.set_xlabel("coverage k (neighborhoods observed, of 8)")
    axB.set_ylabel("wrong unseen bits: simpmax − coin")
    axB.set_title("(b) The crossover: on complex worlds the elegant guess is\n"
                  "worse than a coin — systematically, not by bad luck")
    axB.legend(fontsize=8, loc="center right")
    axB.set_xticks(ks)
    axB.grid(alpha=0.3)

    fig.suptitle("Weakness vs simplicity (benchmark v1.4) — pricing the "
                 "commitment Bennett's selector refuses", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    out_path = outdir / "inverse_benchmark_weakness.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Weakness vs simplicity selectors (benchmark v1.4).")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("-o", "--output", type=str, default=None)
    args = parser.parse_args()

    best = minimal_sizes()
    out = run_weakness_suite(best)
    print_summary(out)

    if args.save:
        outdir = Path(args.output) if args.output else _repo_lab_tools()
        outdir.mkdir(parents=True, exist_ok=True)
        print(f"\nWriting figure to {outdir} …")
        print(f"  {figure(out, outdir)}")


if __name__ == "__main__":
    main()
