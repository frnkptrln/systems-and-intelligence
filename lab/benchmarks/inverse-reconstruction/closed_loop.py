"""
closed_loop.py

Acting is measuring: the closed loop. (Benchmark v1.6)

THE QUESTION.  v1.3 and v1.5 were open-loop: plan once, execute once, no
feedback. Both left the same item open — what changes when the agent lives
in the loop, replanning and (possibly) updating its model from what
execution reveals?  The conceptual stake is the measurement note's regime
hierarchy running by itself: in a closed loop, EVERY EXECUTED PLAN IS AN
INTERVENTION whether the agent intends one or not. Executing a plan drives
the world through neighborhoods, and reality answers with their true
successor bits — a stream of free divergence queries. Acting is measuring
(theory/core/measurement-as-weak-intervention.md, regime 3, made automatic).

THE SETUP.  One episode = H planning rounds on a persistent world. Hidden
CA rule; u0 neighborhoods initially unseen (class size 2^u0). Each round:
sample candidate interventions (flip cells on the CURRENT real row), score
them under the agent's model, execute the chosen one for T real steps, and
continue from the real outcome. Observing the executed trajectory reveals
the true successor bit of every neighborhood it exercises. Agents:

  oracle           — plans with the true rule (ceiling).
  frozen-committed — v1.3's planner, never updates: guess stays fact forever.
  upd-committed    — same guess-filled model, but harvests executed
                     trajectories: revealed bits overwrite guesses.
  upd-wmean        — v1.5's marked planner in the loop: holds the REMAINING
                     class, scores by class mean, harvests likewise.
  random-upd       — picks a random candidate, harvests likewise. The
                     exploration baseline: how fast does the class collapse
                     with NO optimization pressure at all?

PREDICTIONS (stated before the first run, per the repo's habit):
  P1  Free collapse: for every updating agent, remaining-unseen u_r decays
      over rounds with no dedicated exploration — execution alone exercises
      neighborhoods. The decay rate is the free-query rate of acting.
  P2  Self-limiting curse: the updating agents' per-round chosen gap decays
      toward 0 as the class collapses; the frozen agent's gap persists at
      v1.3 levels round after round. Cumulative real-reward regret orders
      oracle < upd-wmean < upd-committed < frozen-committed.
  P3  THE RISKY ONE — the curse funds its own cure: upd-committed's class
      should collapse FASTER than random-upd's. Mechanism: the argmax
      preferentially selects plans whose imagined value leans on flattering
      guesses (v1.3's selection result); executing those plans preferentially
      tests exactly the guessed bits, so exploitation is an involuntary
      active-learning policy aimed at its own delusions. If instead the
      collapse rates are equal, the v1.3 usage-null extends to the closed
      loop (selection without navigation, even here) — also worth knowing,
      and the docstring will say so honestly.

REVISED AFTER RUN 1 (dense regime).  At the original settings (W=60, T=6,
dense start rows) P1 and P2 confirm cleanly — but the free-query channel
SATURATES: one executed plan exercises all 8 neighborhoods almost surely,
so u drops 5 -> 0 in a single round for every updating agent and P3 is
undecidable (both collapse rates hit the floor instantly). That is itself
a reportable fact: in information-dense regimes, acting measures
EVERYTHING immediately — the closed loop erases the class faster than any
selective mechanism can show. The differential question (P3) lives in the
information-SPARSE regime, exactly as v1.1 found from the other side ("the
deader the dynamics, the more structure the query itself must supply").
A sparse regime (W=24, T=2, near-empty start rows, single-cell flips) was
therefore added — settings chosen so that one round reveals only a few
neighborhoods — and P3 is evaluated there.

RESULT (run 2, sparse regime): P3 is FALSIFIED. The argmax does not
collapse the class faster than the random policy — if anything slightly
slower (residual u after 16 rounds: 0.26 committed vs 0.18 random).
Mechanism, in hindsight: optimization is not curiosity. The argmax settles
into reward-good orbits that RE-USE known neighborhoods, while random
flailing wanders into novelty. v1.3's null (selection, not navigation)
extends to the closed loop, and gains a mild anti-exploration corollary.
Two further honest observations: (i) a residual u ~ 0.2 persists for every
agent — neighborhoods the dynamics never produce, v1.1's frozen exception
appearing endogenously (only a prepared state would reveal them); (ii) the
random agent finishes with the BEST model and the WORST reward — free
measurement without optimization is not a strategy either.

WHAT THIS DOES NOT SHOW.  Still a toy: exact class, tabular model, no
function approximation, no partial observability of the state itself. The
industrial analogue (a learned world model updated online) adds failure
modes this setting cannot exhibit — most importantly, an update step that
can be WRONG. Here updates are noiseless reads of reality; the measured
content is the loop structure, not the learning rule.

Usage::

    python closed_loop.py            # console summary
    python closed_loop.py --save     # also write the figure (to lab/tools/)

Related:
- model_exploitation.py / wmax_planner.py           (v1.3 / v1.5: the open-loop pair)
- intervention_experiment.py                        (v1.1: queries collapse the class)
- theory/core/measurement-as-weak-intervention.md   (the regime hierarchy this automates)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from model_exploitation import rule_bits

BITS = ((np.arange(256)[:, None] >> np.arange(8)[None, :]) & 1).astype(np.uint8)


def real_rollout(row: np.ndarray, true_bits: np.ndarray,
                 T: int) -> tuple[np.ndarray, float, np.ndarray]:
    """Execute T real steps; return final row, reward, and the set of
    neighborhood patterns exercised (these are what reality reveals)."""
    r = row.astype(int)
    seen = np.zeros(8, dtype=bool)
    for _ in range(T):
        nb = (np.roll(r, 1) << 2) | (r << 1) | np.roll(r, -1)
        seen[np.unique(nb)] = True
        r = true_bits[nb].astype(int)
    return r.astype(np.uint8), float(r.sum()) / r.size, np.where(seen)[0]


def imagined_reward(row: np.ndarray, model_bits: np.ndarray, T: int) -> float:
    r = row.astype(int)
    for _ in range(T):
        nb = (np.roll(r, 1) << 2) | (r << 1) | np.roll(r, -1)
        r = model_bits[nb].astype(int)
    return float(r.sum()) / r.size


def class_mean_reward(row: np.ndarray, known: np.ndarray, true_bits: np.ndarray,
                      guess: np.ndarray, T: int) -> float:
    """Mean imagined reward over all completions of the unknown bits."""
    unk = np.where(~known)[0]
    u = len(unk)
    base = np.where(known, true_bits, guess).astype(np.uint8)
    members = np.tile(base, (2 ** u, 1))
    for j in range(2 ** u):
        for b, p in enumerate(unk):
            members[j, p] = (j >> b) & 1
    n = members.shape[0]
    R = np.tile(row.astype(int), (n, 1))
    for _ in range(T):
        nb = (np.roll(R, 1, axis=1) << 2) | (R << 1) | np.roll(R, -1, axis=1)
        R = np.take_along_axis(members, nb, axis=1).astype(int)
    return float(R.sum(axis=1).mean()) / row.size


AGENTS = ("oracle", "frozen_committed", "upd_committed", "upd_wmean",
          "random_upd")


def episode(true_rule: int, u0: int = 5, W: int = 60, T: int = 6, H: int = 8,
            k: int = 3, n_candidates: int = 60, density: float = 0.5,
            seed: int = 0) -> dict:
    """One closed-loop episode per agent, paired initial conditions."""
    rng0 = np.random.default_rng(seed)
    true_bits = rule_bits(true_rule)
    unseen0 = rng0.choice(8, size=u0, replace=False)
    guess = rng0.integers(0, 2, size=8, dtype=np.uint8)  # used on unknown bits
    row_init = (rng0.random(W) < density).astype(np.uint8)

    out: dict = {}
    for agent in AGENTS:
        rng = np.random.default_rng(seed + 777)  # same stream per agent
        known = np.ones(8, dtype=bool)
        known[unseen0] = False
        row = row_init.copy()
        gaps, us, rewards = [], [], []
        for _ in range(H):
            cands = [rng.choice(W, size=k, replace=False)
                     for _ in range(n_candidates)]
            model_bits = np.where(known, true_bits, guess).astype(np.uint8)
            if agent == "oracle":
                scores = [imagined_reward(_flip(row, c), true_bits, T)
                          for c in cands]
            elif agent in ("frozen_committed", "upd_committed"):
                scores = [imagined_reward(_flip(row, c), model_bits, T)
                          for c in cands]
            elif agent == "upd_wmean":
                scores = [class_mean_reward(_flip(row, c), known, true_bits,
                                            guess, T) for c in cands]
            else:  # random_upd
                scores = None
            best = (int(rng.integers(0, n_candidates)) if scores is None
                    else int(np.argmax(scores)))
            new_row, reward, exercised = real_rollout(_flip(row, cands[best]),
                                                      true_bits, T)
            if scores is not None:
                gaps.append(scores[best] - reward)
            us.append(int((~known).sum()))
            rewards.append(reward)
            if agent in ("upd_committed", "upd_wmean", "random_upd"):
                known[exercised] = True  # reality reveals what execution touched
            row = new_row
        out[agent] = {"gap": gaps, "u": us, "reward": rewards}
    return out


def _flip(row: np.ndarray, pos: np.ndarray) -> np.ndarray:
    r = row.copy()
    r[pos] ^= 1
    return r


# ══════════════════════ Sweep ═══════════════════════════════════════
DENSE = dict(W=60, T=6, k=3, n_candidates=60, density=0.5, H=8)
SPARSE = dict(W=24, T=2, k=1, n_candidates=24, density=0.12, H=16)


def run_suite(settings: dict, n_rules: int = 12, n_eps: int = 12,
              seed: int = 0) -> dict:
    H = settings["H"]
    rng = np.random.default_rng(seed)
    rules = rng.integers(1, 255, size=n_rules)
    acc = {a: {"gap": [], "u": [], "reward": []} for a in AGENTS}
    s = 0
    for rule in rules:
        for e in range(n_eps):
            s += 1
            r = episode(int(rule), seed=seed * 100000 + s, **settings)
            for a in AGENTS:
                if r[a]["gap"]:
                    acc[a]["gap"].append(r[a]["gap"])
                acc[a]["u"].append(r[a]["u"])
                acc[a]["reward"].append(r[a]["reward"])
    out: dict = {"H": H}
    for a in AGENTS:
        out[a] = {
            "gap": (np.array(acc[a]["gap"]).mean(axis=0).tolist()
                    if acc[a]["gap"] else None),
            "gap_se": (np.array(acc[a]["gap"]).std(axis=0)
                       / np.sqrt(len(acc[a]["gap"]))).tolist()
            if acc[a]["gap"] else None,
            "u": np.array(acc[a]["u"]).mean(axis=0).tolist(),
            "reward": np.array(acc[a]["reward"]).mean(axis=0).tolist(),
        }
    oracle_cum = np.cumsum(out["oracle"]["reward"])
    for a in AGENTS:
        out[a]["cum_regret"] = (oracle_cum
                                - np.cumsum(out[a]["reward"])).tolist()
    return out


def print_summary(res: dict, regime: str) -> None:
    H = res["H"]
    print("=" * 70)
    print(f"  ACTING IS MEASURING — the closed loop (v1.6, {regime} regime)")
    print("=" * 70)
    print(f"\n  u0 = 5 unseen neighborhoods (class 32); H = {H} rounds.")
    print("  Updating agents harvest what execution reveals.\n")
    print("  remaining unseen u_r (P1/P3 — the free-query rate of acting):")
    for a in ("upd_committed", "upd_wmean", "random_upd", "frozen_committed"):
        print(f"    {a:>17}: " + " ".join(f"{u:.2f}" for u in res[a]["u"]))
    print("\n  per-round chosen gap, imagined − real (P2):")
    for a in ("frozen_committed", "upd_committed", "upd_wmean", "oracle"):
        if res[a]["gap"] is not None:
            print(f"    {a:>17}: " + " ".join(f"{g:+.3f}"
                                              for g in res[a]["gap"]))
    print("\n  cumulative real-reward regret vs oracle (P2, final round):")
    for a in ("upd_wmean", "upd_committed", "frozen_committed", "random_upd"):
        print(f"    {a:>17}: {res[a]['cum_regret'][-1]:+.3f}")
    print()


# ══════════════════════ Figure ══════════════════════════════════════
def _repo_lab_tools() -> Path:
    return Path(__file__).resolve().parents[2] / "tools"


def figure(res_dense: dict, res_sparse: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.0))

    rounds_s = np.arange(1, res_sparse["H"] + 1)
    styleA = {"upd_committed": ("#d62728", "o-", "updating committed (argmax)"),
              "upd_wmean": ("#2ca02c", "s-", "updating wmean (argmax, class held)"),
              "random_upd": ("#7f7f7f", "^--", "random policy (no optimization)")}
    for a, (col, fmt, lab) in styleA.items():
        axA.plot(rounds_s, res_sparse[a]["u"], fmt, color=col, lw=2, label=lab)
    axA.axhline(5, ls=":", color="gray", lw=1,
                label="frozen agent (never updates): u stays 5")
    axA.set_xlabel("planning round")
    axA.set_ylabel("remaining unseen neighborhoods $u_r$")
    axA.set_title("(a) SPARSE regime: the collapse race — does the argmax\n"
                  "measure faster than a random policy? (dense: 5→0 in one round)")
    axA.legend(fontsize=8)
    axA.set_xticks(rounds_s)
    axA.grid(alpha=0.3)

    rounds_d = np.arange(1, res_dense["H"] + 1)
    styleB = {"frozen_committed": ("#d62728", "o-", "frozen committed (v1.3 forever)"),
              "upd_committed": ("#ff9896", "o--", "updating committed"),
              "upd_wmean": ("#2ca02c", "s-", "updating wmean")}
    for a, (col, fmt, lab) in styleB.items():
        axB.errorbar(rounds_d, res_dense[a]["gap"], yerr=res_dense[a]["gap_se"],
                     fmt=fmt, color=col, lw=2, capsize=3, label=lab)
    axB.axhline(0, ls=":", color="gray")
    axB.set_xlabel("planning round")
    axB.set_ylabel("chosen-plan gap (imagined − real)")
    axB.set_title("(b) DENSE regime — the curse in the loop: persistent when\n"
                  "frozen, gone after one round of honest updating")
    axB.legend(fontsize=8)
    axB.set_xticks(rounds_d)
    axB.grid(alpha=0.3)

    fig.suptitle("Acting is measuring (benchmark v1.6) — the closed loop, "
                 "measured", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    out = outdir / "inverse_benchmark_closed_loop.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Closed-loop exploitation (benchmark v1.6).")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("-o", "--output", type=str, default=None)
    args = parser.parse_args()

    res_dense = run_suite(DENSE)
    print_summary(res_dense, "dense")
    res_sparse = run_suite(SPARSE)
    print_summary(res_sparse, "sparse")

    if args.save:
        outdir = Path(args.output) if args.output else _repo_lab_tools()
        outdir.mkdir(parents=True, exist_ok=True)
        print(f"\nWriting figure to {outdir} …")
        print(f"  {figure(res_dense, res_sparse, outdir)}")


if __name__ == "__main__":
    main()
