"""
ensemble_size.py

How much class does the cure need? (Benchmark v1.7)

THE QUESTION.  v1.5 showed that holding the FULL equivalence class (wmean)
eliminates the optimizer's-curse wedge. Industrially the class is not
enumerable: an ensemble holds K sampled hypotheses, not 2^u. This module
measures the honest toy version of that gap — how does the cure degrade
with ensemble size K?  It is the bridge between v1.5's exact result and
the approximation actually deployed in model-based RL.

THE SETUP.  v1.5's episode at fixed u = 5 (class size N = 32). Per episode,
sample K DISTINCT class members (an ensemble is a set of distinct
hypotheses; sampling without replacement makes K = N recover exact wmean).
The planner scores each candidate by the K-member mean; all K evaluated on
the same episodes and the same member-reward matrix — perfectly paired.
K = 1 is a committed planner with a random member; K = N is v1.5's wmean.

PREDICTIONS (stated before the first run, per the repo's habit):
  P1  The wedge decreases monotonically in K, with the shape set by the
      score-noise variance under sampling without replacement,
      Var ~ (1/K)·(1 − (K−1)/(N−1)) — i.e. roughly like 1/K for small K and
      pinched to exactly 0 at K = N (finite-population correction). The
      curse magnitude tracks the score-error SD, so expect most of the drop
      early: a handful of hypotheses buys most of the honesty.
  P2  Real-reward regret vs the oracle decreases monotonically in K with
      the same early-saturation shape: the marginal value of the 17th
      hypothesis is far below that of the 2nd.

WHAT THIS DOES NOT SHOW.  Sampling uniformly from an exact class is a
luxury no learned ensemble has: real ensembles are correlated (shared
architecture, shared data), and correlated members buy less variance
reduction than this measures. The numbers here are the BEST CASE for
K-member honesty — an upper bound on what an ensemble of a given size can
deliver, not an estimate of what deployed ensembles do deliver.

Usage::

    python ensemble_size.py            # console summary
    python ensemble_size.py --save     # also write the figure (to lab/tools/)

Related:
- wmax_planner.py                                   (v1.5: the K = N limit)
- model_exploitation.py                             (v1.3: the K = 1 disease)
- theory/ai/world-models-and-vla.md                 (ensembles as the field's cure)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from model_exploitation import rule_bits
from wmax_planner import class_members, rollout_rewards_members

KS = (1, 2, 4, 8, 16, 32)
U = 5  # class size 32


def episode(true_rule: int, W: int = 60, T: int = 12, k: int = 4,
            n_candidates: int = 150, seed: int = 0) -> dict:
    """v1.5's episode at u = U; every ensemble size scored on shared rollouts."""
    rng = np.random.default_rng(seed)
    true_bits = rule_bits(true_rule)
    unseen = rng.choice(8, size=U, replace=False)
    guess = rng.integers(0, 2, size=U, dtype=np.uint8)
    members, truth_idx, _ = class_members(true_bits, unseen, guess)
    n_members = members.shape[0]

    row0 = (rng.random(W) < 0.5).astype(np.uint8)
    cand_positions = [rng.choice(W, size=k, replace=False)
                      for _ in range(n_candidates)]
    mr = np.empty((n_candidates, n_members))
    for i, pos in enumerate(cand_positions):
        r = row0.copy()
        r[pos] ^= 1
        mr[i] = rollout_rewards_members(r, members, T)
    real_all = mr[:, truth_idx]
    oracle_real = float(real_all.max())

    out: dict = {}
    for K in KS:
        sample = rng.choice(n_members, size=K, replace=False)
        sc = mr[:, sample].mean(axis=1)
        best = int(np.argmax(sc))
        gaps = sc - real_all
        out[K] = {"wedge": float(gaps[best] - gaps.mean()),
                  "regret": oracle_real - float(real_all[best])}
    return out


def run_suite(n_rules: int = 14, n_masks: int = 3, n_eps: int = 5,
              seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    rules = rng.integers(1, 255, size=n_rules)
    acc = {K: {"w": [], "r": []} for K in KS}
    s = 0
    for rule in rules:
        for m in range(n_masks):
            for e in range(n_eps):
                s += 1
                r = episode(int(rule), seed=seed * 100000 + s)
                for K in KS:
                    acc[K]["w"].append(r[K]["wedge"])
                    acc[K]["r"].append(r[K]["regret"])
    out = {"K": list(KS), "wedge": [], "wedge_se": [], "regret": [],
           "regret_se": []}
    for K in KS:
        w, r = np.array(acc[K]["w"]), np.array(acc[K]["r"])
        out["wedge"].append(float(w.mean()))
        out["wedge_se"].append(float(w.std() / np.sqrt(w.size)))
        out["regret"].append(float(r.mean()))
        out["regret_se"].append(float(r.std() / np.sqrt(r.size)))
    return out


def print_summary(res: dict) -> None:
    print("=" * 70)
    print("  HOW MUCH CLASS DOES THE CURE NEED?  (benchmark v1.7, u = 5)")
    print("=" * 70)
    print("\n  K = ensemble size (distinct class members); class size N = 32.")
    print("  K=1 ~ committed planner; K=32 = v1.5's exact wmean.\n")
    print(f"  {'K':>4} {'curse wedge':>16} {'regret vs oracle':>18}")
    for i, K in enumerate(res["K"]):
        print(f"  {K:>4} {res['wedge'][i]:>10.4f} ±{res['wedge_se'][i]:.4f}"
              f" {res['regret'][i]:>11.4f} ±{res['regret_se'][i]:.4f}")
    w0, w1 = res["wedge"][0], res["wedge"][2]  # K=1 vs K=4
    print(f"\n  drop K=1 → K=4: wedge −{(1 - w1 / w0) * 100:.0f}%")
    print("\nReading: the cure saturates early — most of the honesty is bought")
    print("by the first few hypotheses, and exactness (K = N) buys only the")
    print("last epsilon. Remember the scope note: uniform sampling from an")
    print("exact class is the ensemble's BEST case; correlated members buy")
    print("less. This is the upper bound on K-member honesty, measured.")


def _repo_lab_tools() -> Path:
    return Path(__file__).resolve().parents[2] / "tools"


def figure(res: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    Ks = np.array(res["K"])
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.0))

    axA.errorbar(Ks, res["wedge"], yerr=res["wedge_se"], fmt="o-",
                 color="#d62728", lw=2, capsize=3, label="curse wedge at u=5")
    axA.axhline(0, ls="--", color="#2ca02c", lw=1.5,
                label="exact wmean (K = N = 32): v1.5's zero")
    axA.set_xscale("log", base=2)
    axA.set_xticks(Ks, [str(K) for K in Ks])
    axA.set_xlabel("ensemble size K (distinct class members, of N = 32)")
    axA.set_ylabel("curse wedge  (chosen gap − candidate-mean gap)")
    axA.set_title("(a) The cure vs its budget: the wedge dies early —\n"
                  "a handful of hypotheses buys most of the honesty")
    axA.legend(fontsize=8)
    axA.grid(alpha=0.3)

    axB.errorbar(Ks, res["regret"], yerr=res["regret_se"], fmt="s-",
                 color="#1f77b4", lw=2, capsize=3,
                 label="real-reward regret vs oracle")
    axB.set_xscale("log", base=2)
    axB.set_xticks(Ks, [str(K) for K in Ks])
    axB.set_xlabel("ensemble size K (distinct class members, of N = 32)")
    axB.set_ylabel("real-reward regret vs oracle")
    axB.set_title("(b) And what it earns: regret falls more slowly —\n"
                  "honesty is cheaper than knowledge")
    axB.legend(fontsize=8)
    axB.grid(alpha=0.3)

    fig.suptitle("How much class does the cure need? (benchmark v1.7) — "
                 "ensemble size vs the optimizer's curse", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    out = outdir / "inverse_benchmark_ensemble_size.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ensemble size vs the optimizer's curse (benchmark v1.7).")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("-o", "--output", type=str, default=None)
    args = parser.parse_args()

    res = run_suite()
    print_summary(res)

    if args.save:
        outdir = Path(args.output) if args.output else _repo_lab_tools()
        outdir.mkdir(parents=True, exist_ok=True)
        print(f"\nWriting figure to {outdir} …")
        print(f"  {figure(res, outdir)}")


if __name__ == "__main__":
    main()
