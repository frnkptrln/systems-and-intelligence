"""
composition.py

Coupled processes: detecting model-family misspecification. (Benchmark v1.8)

THE QUESTION.  When data come from two coupled elementary cellular automata,
when does a declared single-rule family become inconsistent with the trace?
If the coupled family is then supplied, which exercised rule-table entries
can be recovered? This is a model-selection and coverage experiment, not an
ontological test for a “higher level.”

THE SETUP.  Two elementary CAs, streams a and b on a ring (W=120), each
evolving by its own rule — coupled at a fixed random site mask of density
g: at masked sites, the center bit each stream reads is XORed with the
other stream's cell. g = 0 → two independent CAs; g grows → the composite
is exercised harder. The observer sees STREAM A ONLY (the phenotype) and
asks the benchmark's standard question: which elementary rule produced
this?

  Single-family verdict: scan the observed transitions for functionality —
  the same 3-cell pattern mapping to two different successors anywhere
  in the trace means NO elementary rule is consistent: the declared class is
  EMPTY. This diagnoses family misspecification relative to the trace.

  Coupled-family recovery: with the coupled-pair family supplied (structure and
  mask given — the v0 concession, as in the original benchmark) and both
  streams observed, tabulate the augmented neighborhoods and recover
  both rule tables.

  Two symbiont-invisibility controls: (a) the center-blind reader —
  ruleA = 90 is left XOR right, so the XOR coupling that lands on the
  CENTER bit never changes its output; (b) the dying symbiont —
  ruleB = 0 collapses stream b to zeros after one step.

PREDICTIONS (stated before the first run, per the repo's habit):
  P1  g = 0: the single-rule class is never empty; with random ICs all eight
      patterns are exercised, so the class is exactly {ruleA} — the
      observed stream is represented by ruleA. The unused coupling is not
      identified from that observation.
  P2  Detection cost falls like a coverage law: median time-to-empty-class
      T_detect decreases monotonically in g, roughly hyperbolically
      (~1/(gW) until floor); by g = 0.1 detection is near-immediate
      (a few steps).
  P3  Coupled-family recovery stays cheap for every g with the family known:
      near-exact rule bits for both streams. The mismatch is not parameter
      fitting inside the single-rule family: the supplied coupled family has
      additional rule bits and mask structure. This is a larger declared
      family, not a general complexity bound.
  P4  OBSERVATION-CHANNEL TEST — the dying symbiont (ruleB = 0) stays single-rule
      consistent at every g: compositionality is invisible when the
      coupling is never exercised. Composition is visible exactly insofar
      as it makes a difference in the trace — the coverage principle's
      third appearance (exp6: bindings; exp7: lures; here: symbionts),
      and the Bateson rung verbatim: a difference that makes no difference
      is, to the observer, no information.

RESULT (run 1, 20 seeds x pairs — console numbers; two predictions were
wrong, and the errors are the two best findings):
  P1  CONFIRMED: at g = 0, 100% consistent, class size exactly 1 on every
      seed — the observed stream is represented cleanly by one rule.
  P2  CONFIRMED for center-READING observers, sharper than predicted:
      the two pairs whose ruleA reads its center (110, 30) leave the
      single-rule family empty on
      100% of seeds with median T_detect = 1 step for every g >= 0.02
      (75% and 2 steps already at g = 0.01). One live coupled site
      suffices, given trace. Detection is coverage-limited, not
      possibility-limited.
  P3  CONFIRMED: family + mask known, coupled-family tabulation recovers every
      exercised rule bit exactly (accuracy 1.0 for all g > 0; coverage
      ~8/8). The larger supplied family fits the exercised entries.
  P4  RE-FOUND, in a cleaner place than the control. The prediction named
      the dying symbiont; the run showed TWO invisibility mechanisms, and
      the elegant one was unplanned:
        * OBSERVATION-RELATIVE (permanent): ruleA = 90 is center-blind, so coupling
          through the center bit is invisible to it at EVERY density —
          empty-class rate 0/20 for all g. The composite is real, the
          partner is active, and the phenotype is still exactly a lone
          rule 90. Visibility is a property of whether the OBSERVED
          update function reads the coupled channel, not of the coupling
          strength. This is the coverage principle sharpened: a difference
          in the world that the observed function discards makes no
          difference in the trace.
        * TRANSIENT (my control, corrected): ruleB = 0 does NOT stay
          invisible — stream b's random initial condition participates in
          the first transition before it dies, so the coupling leaks once,
          and the empty-class rate RISES with g (0.30 -> 1.00) as more
          sites catch that single live step. A genuinely prepared zero-IC
          symbiont would be permanently invisible; a merely dying one is
          not. The prediction conflated "dies" with "never fired".
  READING.  An empty single-rule class is evidence that the declared family
      cannot express the observed transitions. The supplied coupled family
      restores a fit where the coupled channel changes the observed trace.
      It is one candidate explanation, not a unique mechanism. The ecology
      version — in which coupling and dissolution are dynamic and support
      must reproduce its own conditions — remains open.

WHAT THIS DOES NOT SHOW.  A pair with a fixed mask is not an ecology:
nothing here composes spontaneously, persists differentially, or is
selected — the BFF phenomena this bridge cites are exactly the parts not
modeled. "Level" is defined relative to a fixed family ladder (elementary
CA → coupled pair); real family ladders are not given in advance. And the
empty-class diagnosis assumes noise-free traces — under noise, emptiness
must be statistical, which is an open sharpening.

Usage::

    python composition.py            # console summary (~15 s)
    python composition.py --save     # + figure to lab/tools/

Related:
- theory/computation/static-information-and-living-process.md  (the composition bridge this operationalizes)
- family_search.py                                (v1.2: the floor this jump lands on)
- theory/core/mathematical-axioms.md              (model-relative equivalence)
- theory/core/the-generator-question.md           (legacy motivation)
- lab/experiments/exp6_binding_observables.py     (the coverage principle, second appearance)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

W = 120
T = 300
GS = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
READING_PAIRS = [(110, 90), (30, 110)]     # ruleA reads its center bit
BLIND_PAIR = (90, 30)                       # ruleA = 90 = L XOR R, center-blind
DYING = (110, 0)                            # ruleB = 0: symbiont dies after step 1
N_SEEDS = 20


# ════════════════════════ Forward: the coupled pair ═════════════════
def coupled_forward(ruleA: int, ruleB: int, g: float, seed: int,
                    w: int = W, steps: int = T):
    """Two elementary CAs, XOR-coupled at a fixed random site mask."""
    rng = np.random.default_rng(seed)
    bitsA = np.array([(ruleA >> k) & 1 for k in range(8)], dtype=np.uint8)
    bitsB = np.array([(ruleB >> k) & 1 for k in range(8)], dtype=np.uint8)
    mask = rng.random(w) < g
    a = (rng.random(w) < 0.5).astype(np.uint8)
    b = (rng.random(w) < 0.5).astype(np.uint8)
    A = np.empty((steps, w), dtype=np.uint8)
    B = np.empty((steps, w), dtype=np.uint8)
    for t in range(steps):
        A[t], B[t] = a, b
        ca = np.where(mask, a ^ b, a).astype(int)
        cb = np.where(mask, b ^ a, b).astype(int)
        nbA = (np.roll(a, 1).astype(int) << 2) | (ca << 1) \
            | np.roll(a, -1).astype(int)
        nbB = (np.roll(b, 1).astype(int) << 2) | (cb << 1) \
            | np.roll(b, -1).astype(int)
        a, b = bitsA[nbA], bitsB[nbB]
    return A, B, mask


# ════════════════════════ Level 1: the component-family verdict ═════
def level1_scan(A: np.ndarray) -> tuple[int | None, int]:
    """Scan the observed stream against the elementary family.

    Returns (t_detect, class_size): t_detect is the first step at which
    NO elementary rule is consistent (class empty; class_size 0), or None
    if the trace stays functional — then class_size = 2**unseen.
    """
    seen = -np.ones(8, dtype=int)
    for t in range(A.shape[0] - 1):
        row, nxt = A[t].astype(int), A[t + 1].astype(int)
        nb = (np.roll(row, 1) << 2) | (row << 1) | np.roll(row, -1)
        for pat in range(8):
            m = nb == pat
            if not m.any():
                continue
            succ = nxt[m]
            if succ.min() != succ.max():
                return t + 1, 0                    # conflict within one step
            if seen[pat] == -1:
                seen[pat] = int(succ[0])
            elif int(succ[0]) != seen[pat]:
                return t + 1, 0                    # conflict across steps
    return None, int(2 ** int((seen == -1).sum()))


# ════════════════════════ Level 2: family-known recovery ════════════
def level2_recover(A, B, mask, ruleA: int, ruleB: int) -> dict:
    """With the coupled-pair family and mask known and both streams
    observed, tabulate augmented neighborhoods and recover both tables."""
    out = {}
    for name, X, Y, rule in (("A", A, B, ruleA), ("B", B, A, ruleB)):
        true_bits = np.array([(rule >> k) & 1 for k in range(8)])
        seen = -np.ones(8, dtype=int)
        for t in range(X.shape[0] - 1):
            row, other, nxt = X[t].astype(int), Y[t].astype(int), X[t + 1].astype(int)
            c = np.where(mask, row ^ other, row)
            nb = (np.roll(row, 1) << 2) | (c << 1) | np.roll(row, -1)
            for pat in range(8):
                m = nb == pat
                if m.any() and seen[pat] == -1:
                    seen[pat] = int(nxt[m][0])
        sm = seen >= 0
        out[name] = {"coverage": int(sm.sum()),
                     "correct": bool((seen[sm] == true_bits[sm]).all())}
    return out


# ════════════════════════ Suite ═════════════════════════════════════
def _empty_stats(pairs, g, n_seeds):
    empty = n = 0
    tds = []
    for ruleA, ruleB in pairs:
        for s in range(n_seeds):
            A, _, _ = coupled_forward(ruleA, ruleB, g, seed=s)
            td, _ = level1_scan(A)
            n += 1
            if td is not None:
                empty += 1
                tds.append(td)
    return empty / n, tds


def run_suite(n_seeds: int = N_SEEDS) -> dict:
    res = {"reading": {}, "blind": {}, "dying": {},
           "level2": {g: {"cov": [], "ok": []} for g in GS}}
    for g in GS:
        rate_r, tds = _empty_stats(READING_PAIRS, g, n_seeds)
        res["reading"][g] = {"rate": rate_r, "t_detect": tds}
        res["blind"][g] = {"rate": _empty_stats([BLIND_PAIR], g, n_seeds)[0]}
        res["dying"][g] = {"rate": _empty_stats([DYING], g, n_seeds)[0]}
        for ruleA, ruleB in READING_PAIRS + [BLIND_PAIR]:
            for s in range(n_seeds):
                A, B, mask = coupled_forward(ruleA, ruleB, g, seed=s)
                l2 = level2_recover(A, B, mask, ruleA, ruleB)
                res["level2"][g]["cov"].append(
                    (l2["A"]["coverage"] + l2["B"]["coverage"]) / 2.0)
                res["level2"][g]["ok"].append(
                    l2["A"]["correct"] and l2["B"]["correct"])
    return res


def print_summary(res: dict) -> None:
    print("=" * 78)
    print("  BENCHMARK v1.8 — coupled processes: family misspecification")
    print(f"  (coupled elementary CAs, W={W}, T={T}, {N_SEEDS} seeds/pair)")
    print("=" * 78)
    print(f"\n  {'g':>6s} {'reading empty':>14s} {'median T_det':>13s} "
          f"{'blind empty':>12s} {'dying empty':>12s} "
          f"{'L2 cov/8':>9s} {'L2 exact':>9s}")
    for g in GS:
        r = res["reading"][g]
        l2 = res["level2"][g]
        td = (f"{np.median(r['t_detect']):.1f}" if r["t_detect"] else "—")
        print(f"  {g:6.2f} {r['rate']:14.2f} {td:>13s} "
              f"{res['blind'][g]['rate']:12.2f} {res['dying'][g]['rate']:12.2f} "
              f"{np.mean(l2['cov']):9.1f} {np.mean(l2['ok']):9.2f}")
    print("\n  Reading: a center-READING observer's class empties within ~1 step")
    print("  of any live coupling (single-rule misspecification detected). The")
    print("  center-BLIND observer (rule 90) never empties at any g under this")
    print("  observation channel;")
    print("  the DYING symbiont leaks only through its initial condition, so its")
    print("  empty-rate RISES with g. When the coupled family and mask are")
    print("  supplied, its fit stays exact; that larger family is not a unique")
    print("  explanation of the hidden mechanism.")


# ════════════════════════ Figure ════════════════════════════════════
def figure(res: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4))

    ax = axes[0]
    ax.plot(GS, [res["reading"][g]["rate"] for g in GS],
            "o-", color="#d62728", label="center-reading (110, 30)")
    ax.plot(GS, [res["blind"][g]["rate"] for g in GS],
            "^-", color="#1f77b4", label="center-blind (rule 90)")
    ax.plot(GS, [res["dying"][g]["rate"] for g in GS],
            "s--", color="#999999", label="dying symbiont (ruleB=0)")
    ax.set_xlabel("coupling density g")
    ax.set_ylabel(f"empty-class rate within T={T}")
    ax.set_title("(a) Single-rule family misspecification\n"
                 "(structural: blind never empties;\ntransient: dying leaks via its IC)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1]
    gs = [g for g in GS if g > 0]
    med = [np.median(res["reading"][g]["t_detect"]) for g in gs]
    ax.semilogx(gs, med, "o-", color="#d62728")
    ax.set_xlabel("coupling density g")
    ax.set_ylabel("median steps to empty class")
    ax.set_ylim(0, max(med) + 1)
    ax.set_title("(b) Detection is coverage-limited\n(center-reading T_detect vs g)")
    ax.grid(alpha=0.3, which="both")

    ax = axes[2]
    ax.plot(GS, [np.mean(res["level2"][g]["cov"]) for g in GS], "o-",
            color="#2ca02c", label="mean table coverage (/8)")
    ax.plot(GS, [8 * np.mean(res["level2"][g]["ok"]) for g in GS], "s--",
            color="#d62728", label="exact recovery × 8")
    ax.set_xlabel("coupling density g")
    ax.set_ylim(0, 8.5)
    ax.set_title("(c) Supplied coupled family fits cheaply\n(not a unique mechanism)")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.suptitle("Benchmark v1.8 — coupled data can empty a declared "
                 "single-rule family",
                 fontsize=11)
    fig.tight_layout()
    out = outdir / "inverse_benchmark_composition.png"
    fig.savefig(out, dpi=110)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true", help="write the figure")
    args = ap.parse_args()
    res = run_suite()
    print_summary(res)
    if args.save:
        outdir = Path(__file__).resolve().parents[2] / "tools"
        print(f"\n  figure → {figure(res, outdir)}")


if __name__ == "__main__":
    main()
