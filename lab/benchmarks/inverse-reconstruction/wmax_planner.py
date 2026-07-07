"""
wmax_planner.py

Marking the guesses: does the curse wedge survive? (Benchmark v1.5)

THE QUESTION.  v1.3 measured the disease: a planner whose world model fills
unseen neighborhoods with an unmarked guess (one member of the 2^u
consistent-generator class, treated as fact) develops an imagined-vs-real
gap on its chosen plan — the optimizer's curse wedge — growing monotonically
with class size. v1.4 measured the selector-side discipline (hold the
weakest consistent hypothesis = the uncollapsed class). This module closes
the pair: what happens when THE PLANNER ITSELF holds the class — when the
guesses are marked as guesses at planning time?  This is Bennett's weakness
principle used as the CURE for v1.3's disease, and it is what the industrial
cures (ensembles, pessimism penalties) formalize: letting the argmax see
which bits are guesses.

THE SETUP.  Identical to v1.3 (same worlds, same candidate interventions,
same reward), with four planners scored on the SAME episodes — paired
comparison, same candidates, same start rows:

  committed — v1.3's baseline: one fixed class member treated as fact;
              score(a) = imagined reward under that member.
  wmean     — marked guesses, Bayes over the class: score(a) = MEAN imagined
              reward over all 2^u members (uniform class posterior — exact,
              since the class is enumerable here). The ensemble cure, exact.
  wmin      — marked guesses, pessimist: score(a) = MIN over members — only
              count reward every member guarantees. The pessimism cure,
              exact; corridor-flavored planning (viability, not optimality).
  oracle    — plans with the true rule (reference ceiling).

One vectorized rollout per candidate over all class members yields every
planner's score AND the real outcome (the truth is a member of the class).

PREDICTIONS (stated before the first run, per the repo's habit):
  P1  committed replicates v1.3: wedge (chosen-gap minus candidate-mean gap)
      grows monotonically with u.
  P2  wmean's wedge is ~ 0 at EVERY u — not mitigated, eliminated in
      expectation. Reason (theorem-grade given the uniform class): the
      choice uses only class-measurable information, and conditional on the
      observed mask the truth is uniform over the class, independent of the
      choice; so E[score(chosen) − real(chosen)] = 0 exactly. The run
      validates that the mechanism is what we claimed: v1.3's entire wedge
      is attributable to the UNMARKED commitment, nothing else.
  P3  wmin's chosen-gap is <= 0 pointwise (min over a class containing the
      truth can never exceed the truth): the pessimist is never disappointed,
      by construction. Reported as a check, not a discovery.
  P4  Achieved real reward (regret vs oracle): wmean <= committed at u > 0
      with the gap growing in u — marking guesses is not only epistemically
      honest but PAYS in expectation (Bayes-optimality among planners using
      only class information). Where wmin lands is measured, not predicted:
      the price of never-disappointed, in real reward, is an open sub-question.

WHAT THIS DOES NOT SHOW.  Open-loop toy, exact enumerable class. P2's zero
is a theorem given the uniform posterior — the measured content is the
validation of the mechanism, the SIZE of the real-reward price of unmarked
guessing, and where the pessimist lands. In the industrial case the class
is NOT enumerable; there, "marking the guesses" is itself the hard problem
(ensembles approximate wmean, pessimism penalties approximate wmin), which
is exactly why the accounting rule — mark what the traces actually
determine — is an architecture requirement rather than a free lunch
(theory/core/measurement-as-weak-intervention.md).

Usage::

    python wmax_planner.py            # console summary
    python wmax_planner.py --save     # also write the figure (to lab/tools/)

Related:
- model_exploitation.py                                (v1.3: the disease)
- weakness_selector.py                                 (v1.4: the selector side)
- theory/ai/world-models-and-vla.md                    (ensembles/pessimism as the field's cures)
- theory/core/measurement-as-weak-intervention.md      (the accounting rule)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from model_exploitation import rule_bits


# ══════════════════════ Class machinery ═════════════════════════════
def class_members(true_bits: np.ndarray, unseen: np.ndarray,
                  guess: np.ndarray) -> tuple[np.ndarray, int, int]:
    """All 2^u completions of the observed bits; indices of truth and guess."""
    u = len(unseen)
    n = 2 ** u
    members = np.tile(true_bits, (n, 1))
    for j in range(n):
        for b, p in enumerate(unseen):
            members[j, p] = (j >> b) & 1
    truth_idx = sum(int(true_bits[p]) << b for b, p in enumerate(unseen))
    guess_idx = sum(int(g) << b for b, g in enumerate(guess))
    return members, truth_idx, guess_idx


def rollout_rewards_members(row: np.ndarray, members: np.ndarray,
                            T: int) -> np.ndarray:
    """Reward of one start row under EVERY member table, vectorized."""
    n = members.shape[0]
    R = np.tile(row.astype(int), (n, 1))
    for _ in range(T):
        nb = (np.roll(R, 1, axis=1) << 2) | (R << 1) | np.roll(R, -1, axis=1)
        R = np.take_along_axis(members, nb, axis=1).astype(int)
    return R.sum(axis=1) / R.shape[1]


# ══════════════════════ One paired episode ══════════════════════════
def episode(true_rule: int, u: int, W: int = 60, T: int = 12, k: int = 4,
            n_candidates: int = 150, seed: int = 0) -> dict:
    """Same construction as v1.3's episode; four planners on shared rollouts."""
    rng = np.random.default_rng(seed)
    true_bits = rule_bits(true_rule)

    unseen = (rng.choice(8, size=u, replace=False) if u > 0
              else np.array([], dtype=int))
    guess = rng.integers(0, 2, size=u, dtype=np.uint8)  # v1.3's fixed member
    members, truth_idx, guess_idx = class_members(true_bits, unseen, guess)

    row0 = (rng.random(W) < 0.5).astype(np.uint8)
    cand_positions = [rng.choice(W, size=k, replace=False)
                      for _ in range(n_candidates)]

    mr = np.empty((n_candidates, members.shape[0]))
    for i, pos in enumerate(cand_positions):
        r = row0.copy()
        r[pos] ^= 1
        mr[i] = rollout_rewards_members(r, members, T)

    real_all = mr[:, truth_idx]
    scores = {"committed": mr[:, guess_idx],
              "wmean": mr.mean(axis=1),
              "wmin": mr.min(axis=1)}

    out: dict = {}
    for name, sc in scores.items():
        best = int(np.argmax(sc))
        gaps = sc - real_all
        out[name] = {"gap_chosen": float(gaps[best]),
                     "gap_cand": float(gaps.mean()),
                     "real": float(real_all[best])}
    out["oracle_real"] = float(real_all.max())
    return out


# ══════════════════════ Sweep (v1.3-matched sizes) ══════════════════
PLANNERS = ("committed", "wmean", "wmin")


def run_suite(us=(0, 1, 2, 3, 4, 5), n_rules: int = 14, n_masks: int = 3,
              n_eps: int = 5, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    rules = rng.integers(1, 255, size=n_rules)
    out: dict = {"u": list(us)}
    for p in PLANNERS:
        out[p] = {"wedge": [], "wedge_se": [], "gap_chosen": [],
                  "regret": [], "regret_se": []}
    for u in us:
        acc = {p: {"w": [], "g": [], "r": []} for p in PLANNERS}
        s = 0
        for rule in rules:
            for m in range(n_masks):
                for e in range(n_eps):
                    s += 1
                    r = episode(int(rule), u, seed=seed * 100000 + s)
                    for p in PLANNERS:
                        acc[p]["w"].append(r[p]["gap_chosen"] - r[p]["gap_cand"])
                        acc[p]["g"].append(r[p]["gap_chosen"])
                        acc[p]["r"].append(r["oracle_real"] - r[p]["real"])
        for p in PLANNERS:
            w = np.array(acc[p]["w"])
            reg = np.array(acc[p]["r"])
            out[p]["wedge"].append(float(w.mean()))
            out[p]["wedge_se"].append(float(w.std() / np.sqrt(w.size)))
            out[p]["gap_chosen"].append(float(np.mean(acc[p]["g"])))
            out[p]["regret"].append(float(reg.mean()))
            out[p]["regret_se"].append(float(reg.std() / np.sqrt(reg.size)))
    return out


def print_summary(res: dict) -> None:
    print("=" * 70)
    print("  MARKING THE GUESSES — wmax planners in the v1.3 episode (v1.5)")
    print("=" * 70)
    print("\n  u = unseen neighborhoods; class size 2^u; same episodes for all")
    print("  planners. wedge = chosen-gap − candidate-mean gap (the curse,")
    print("  isolated). regret = oracle real reward − planner real reward.\n")
    hdr = f"  {'u':>2} {'class':>6}"
    for p in PLANNERS:
        hdr += f" {p + ' wedge':>18} {p + ' regret':>16}"
    print(hdr)
    for i, u in enumerate(res["u"]):
        line = f"  {u:>2} {2**u:>6}"
        for p in PLANNERS:
            line += (f" {res[p]['wedge'][i]:>10.4f} ±{res[p]['wedge_se'][i]:.4f}"
                     f" {res[p]['regret'][i]:>9.4f} ±{res[p]['regret_se'][i]:.4f}")
        print(line)
    print("\n  chosen-plan gap (imagined − real), for reference:")
    for p in PLANNERS:
        print(f"    {p:>9}: " + "  ".join(
            f"u={u}: {g:+.4f}" for u, g in zip(res["u"], res[p]["gap_chosen"])))
    print("\nReading: the committed planner replicates v1.3 — the wedge grows")
    print("with the class. The wmean planner (guesses marked, class held) has")
    print("no wedge to speak of at any u: the curse was never about having an")
    print("imperfect model, it was about FORGETTING WHICH BITS ARE GUESSES.")
    print("The wmin pessimist is never disappointed (gap <= 0 by construction)")
    print("and pays for it in real reward — the regret column prices both")
    print("disciplines against the committed baseline. Ensembles and pessimism")
    print("penalties in model-based RL are these two planners, approximated.")


# ══════════════════════ Figure ══════════════════════════════════════
def _repo_lab_tools() -> Path:
    return Path(__file__).resolve().parents[2] / "tools"


def figure(res: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    us = np.array(res["u"])
    style = {"committed": ("#d62728", "o-", "committed (v1.3 baseline: guess as fact)"),
             "wmean": ("#2ca02c", "s-", "wmean (guesses marked: class average)"),
             "wmin": ("#1f77b4", "v-", "wmin (guesses marked: pessimist)")}
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.0))

    for p in PLANNERS:
        col, fmt, lab = style[p]
        axA.errorbar(us, res[p]["wedge"], yerr=res[p]["wedge_se"], fmt=fmt,
                     color=col, lw=2, capsize=3, label=lab)
    axA.axhline(0, ls=":", color="gray")
    axA.set_xlabel("unseen neighborhoods u   (class size $2^u$)")
    axA.set_ylabel("curse wedge  (chosen gap − candidate-mean gap)")
    axA.set_title("(a) Marking the guesses removes the wedge:\n"
                  "the curse is the unmarked commitment, nothing else")
    axA.legend(fontsize=8, loc="upper left")
    axA.set_xticks(us)
    axA.grid(alpha=0.3)

    for p in PLANNERS:
        col, fmt, lab = style[p]
        axB.errorbar(us, res[p]["regret"], yerr=res[p]["regret_se"], fmt=fmt,
                     color=col, lw=2, capsize=3, label=lab)
    axB.axhline(0, ls=":", color="gray")
    axB.set_xlabel("unseen neighborhoods u   (class size $2^u$)")
    axB.set_ylabel("real-reward regret vs oracle")
    axB.set_title("(b) And it pays: regret vs the oracle, per planner —\n"
                  "the price of treating guesses as facts, in achieved reward")
    axB.legend(fontsize=8, loc="upper left")
    axB.set_xticks(us)
    axB.grid(alpha=0.3)

    fig.suptitle("Marking the guesses (benchmark v1.5) — Bennett's discipline as "
                 "the cure for v1.3's disease", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    out = outdir / "inverse_benchmark_wmax_planner.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="wmax planners in the v1.3 exploitation episode (v1.5).")
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
