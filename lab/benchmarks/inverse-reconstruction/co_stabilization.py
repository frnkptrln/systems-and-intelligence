"""
co_stabilization.py

Co-stabilization: when a composite becomes an ecology. (Benchmark v1.9)

THE QUESTION.  v1.8 measured composition — two coupled generators whose
joint trace empties the single-generator equivalence class. But composition
is not yet life. The ladder note's synthesis names the missing threshold:
"a self-maintaining composition of processes whose functions make
differences for one another" — CO-STABILIZATION, each function holding the
others in a viable regime. This file measures it, with the operational
definition the note committed to: co-stabilization is what distinguishes an
ecology from mere coexistence, and it is measurable only by KNOCKOUT — you
cannot see it by watching the healthy system.

THE SETUP.  N nodes ("functions"), each carrying a health h_i in [0, 1];
viable if h_i >= v_thresh. A ring topology (each node coupled to two
neighbors). Dynamics:

    h_i(t+1) = clip( s + c * mean_{j~i} h_j(t) , 0, 1 )

with s = 1 - c chosen so that the all-healthy state h_i = 1 is a fixed
point at EVERY coupling c. This is the crux: at rest, every regime looks
identical — all nodes viable, health 1. The coupling c is the
mutual-dependence dial:

    c = 0   each node is self-sufficient (s = 1). Pure coexistence.
    c -> 1  each node's health is almost entirely its neighbors' (s -> 0).
            A standing web that holds itself up — and can fall together.

THREE PROBES:
  REST      — run undisturbed; record viability. (Predicted: blind — every
              c looks perfectly healthy.)
  KNOCKOUT  — freeze one node at h = 0, relax to steady state, count how
              many of the OTHER N-1 nodes fall below v_thresh. The cascade.
              Co-stabilization score = mean over knockout targets of
              (survivors lost beyond the 1 removed) — additive vs super-
              additive.
  NOISE     — inject i.i.d. per-step health noise, measure the fraction of
              node-steps that stay viable. The other face of coupling:
              mutual support averages distributed shocks away.

The pair of probes asks whether the same coupling that cascades under
targeted knockout also buffers distributed noise — a robustness/fragility
trade. (It does not, in this model, and that is the finding; see RESULT.)

PREDICTIONS (stated before the first run, per the repo's habit):
  P1  REST is blind: viability = 1.0 for every c. Watching a healthy
      ecology cannot distinguish coexistence from co-stabilization — the
      coverage/Bateson principle's fourth appearance (exp6 bindings, exp7
      lures, v1.8 symbionts, here dependencies).
  P2  KNOCKOUT separates them: at c = 0 a knockout costs exactly 1 node
      (additive; cascade ratio ~ 1); as c rises the survivors' health is
      dragged down and extra nodes fall — super-additive collapse — with a
      threshold in c, above which one knockout takes a finite fraction (at
      c -> 1, on a ring pinned to 0, the whole line decays: total collapse).
  P3  NOISE robustness rises with c: averaging over neighbors buffers
      i.i.d. shocks, so the viable fraction under noise increases with
      coupling — the same c that P2 makes fragile.
  P4  THE RISKY ONE — the knockout threshold is SHARP (a phase transition
      in c), not gradual: below it a knockout is local, above it it
      cascades system-wide. If instead the cascade grows smoothly with c,
      there is no critical coupling and co-stabilization is a matter of
      degree, not a threshold — also worth knowing, and the docstring will
      say which.

RESULT (run 1, N=16 ring, 200 noise trials — console numbers):
  P1  CONFIRMED: rest viability = 1.00 at EVERY c. Watching a healthy
      ecology is blind — coexistence (c=0) and near-total mutual
      dependence (c=0.95) are pixel-identical at rest. Co-stabilization
      has no passive signature. The coverage principle's fourth
      appearance (exp6 bindings, exp7 lures, v1.8 symbionts, here
      dependencies): a dependency that never fires makes no difference.
  P2  CONFIRMED: the knockout cascade is 0 (purely additive — a knockout
      costs exactly the one node) for c <= 0.7, then goes super-additive:
      +2 extra nodes at c=0.8-0.9, +4 at c=0.95, and +15 at c=1.0 — one
      knockout kills the ENTIRE ring. Knockout is the instrument that
      rest could not be; the cascade IS the ecology, made visible only by
      removal.
  P3  FALSIFIED — and the miss is the real finding. The noise viability
      does NOT rise with coupling; it FALLS monotonically (0.977 -> 0.521).
      Mechanism: in this model mutual dependence SUBSTITUTES for self-
      sufficiency (s = 1 - c), so as c rises the restoring force to the
      viable setpoint vanishes and distributed noise accumulates instead
      of being reset. There is no robust/fragile trade here: pure mutual
      dependence is fragile BOTH ways — to targeted knockout AND to
      distributed noise — while looking perfectly healthy at rest. The
      cautionary reading: co-stabilization-as-substitution is a
      monoculture, not resilience. Genuine ecological robustness would
      require coupling that ADDS a redundant pathway to self-sufficiency
      rather than replacing it — the redundancy model, named as the
      follow-up below. What this run establishes cleanly is the invariant
      that does NOT depend on which coupling: rest-invisibility, and the
      knockout as the only instrument that reaches it.
  P4  PARTIALLY CONFIRMED: there is a clear critical ONSET near c ~ 0.75
      (strictly local knockouts below it, super-additive above), not a
      gradual rise from c=0 — but above the onset the cascade climbs in
      steps (2 -> 4 -> 15) rather than one clean jump, with true system-
      wide collapse only at c=1.0. Sharper than gradual, but a stepped
      transition, not a single critical point.

WHAT THIS DOES NOT SHOW.  A fixed ring with a linear averaging rule is not
an ecology that composes and dissolves on its own — nothing here is
selected, nothing reproduces, and the knockout is imposed by the
experimenter, not by the dynamics. It measures the SIGNATURE of co-
stabilization (rest-invisibility, the knockout cascade), not its emergence.
Two named follow-ups: (a) the REDUNDANCY model — coupling that adds a
compensating pathway to retained self-sufficiency, rather than substituting
for it (s = 1 - c) — which should show the robust-to-noise / fragile-to-
knockout trade this run's substitution model did NOT; and (b) the
population version, where the coupling structure itself is built and broken
by the processes (the BFF/computational-life reading), one level up again.
"Viability" here is a threshold on a scalar, not a metabolism. No
consciousness claims: co-stabilization is the substrate of the self-
maintenance question, not the self-binding (phase-6) question.

Usage::

    python co_stabilization.py            # console summary (~5 s)
    python co_stabilization.py --save      # + figure to lab/tools/

Related:
- theory/computation/static-information-and-living-process.md  (the co-stabilization threshold this measures)
- composition.py                                               (v1.8: composition, the pair this generalizes)
- theory/core/measurement-as-weak-intervention.md              (watching < perturbing, here rest < knockout)
- papers/viable-corridor.md                                    (capability loading: robustness bought on one axis, paid on another)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

N = 16
V_THRESH = 0.5
CS = [0.0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
RELAX_STEPS = 400
NOISE_TRIALS = 200
NOISE_STEPS = 200
NOISE_SIGMA = 0.25


def _ring_neighbors(n: int) -> list[tuple[int, int]]:
    return [((i - 1) % n, (i + 1) % n) for i in range(n)]


def relax(c: float, frozen: int | None = None,
          steps: int = RELAX_STEPS) -> np.ndarray:
    """Relax the ring to steady state; optionally pin one node at 0."""
    s = 1.0 - c
    nb = _ring_neighbors(N)
    h = np.ones(N)
    if frozen is not None:
        h[frozen] = 0.0
    for _ in range(steps):
        new = np.array([s + c * 0.5 * (h[a] + h[b]) for (a, b) in nb])
        new = np.clip(new, 0.0, 1.0)
        if frozen is not None:
            new[frozen] = 0.0
        h = new
    return h


def rest_viability(c: float) -> float:
    h = relax(c)
    return float((h >= V_THRESH).mean())


def knockout_cascade(c: float) -> float:
    """Mean over knockout targets of (extra survivors lost beyond the 1
    removed). 0 = purely additive (coexistence); large = super-additive."""
    extra = []
    for k in range(N):
        h = relax(c, frozen=k)
        others = np.delete(h, k)
        dead_others = int((others < V_THRESH).sum())
        extra.append(dead_others)          # nodes lost beyond the removed one
    return float(np.mean(extra))


def noise_viability(c: float, seed: int = 0) -> float:
    """Fraction of node-steps staying viable under i.i.d. health noise."""
    rng = np.random.default_rng(seed)
    s = 1.0 - c
    nb = _ring_neighbors(N)
    h = np.ones(N)
    viable = 0
    total = 0
    for _ in range(NOISE_STEPS):
        new = np.array([s + c * 0.5 * (h[a] + h[b]) for (a, b) in nb])
        new = np.clip(new + rng.normal(0, NOISE_SIGMA, N), 0.0, 1.0)
        h = new
        viable += int((h >= V_THRESH).sum())
        total += N
    return viable / total


def run_suite() -> dict:
    rest, cascade, noise = [], [], []
    for c in CS:
        rest.append(rest_viability(c))
        cascade.append(knockout_cascade(c))
        nv = [noise_viability(c, seed=s) for s in range(NOISE_TRIALS)]
        noise.append(float(np.mean(nv)))
    return {"cs": CS, "rest": rest, "cascade": cascade, "noise": noise}


def print_summary(res: dict) -> None:
    print("=" * 72)
    print("  BENCHMARK v1.9 — co-stabilization: when a composite becomes an ecology")
    print(f"  (N={N} ring, knockout cascade + noise robustness vs coupling c)")
    print("=" * 72)
    print(f"\n  {'c':>6s} {'rest viability':>15s} {'knockout cascade':>18s} "
          f"{'noise viability':>16s}")
    for i, c in enumerate(res["cs"]):
        print(f"  {c:6.2f} {res['rest'][i]:15.2f} {res['cascade'][i]:18.2f} "
              f"{res['noise'][i]:16.3f}")
    print("\n  cascade = mean extra nodes lost per knockout, beyond the 1 removed")
    print("  (0 = additive / coexistence; large = super-additive / ecology)")
    print("\n  Reading: rest is blind (all viability 1.0 — watching cannot tell")
    print("  coexistence from co-stabilization); the knockout cascade rises with")
    print("  coupling (super-additive above c~0.75). The predicted noise-robustness")
    print("  trade is FALSIFIED: noise viability FALLS with coupling too — pure")
    print("  mutual dependence (substitution) is fragile BOTH ways, a monoculture.")
    print("  The invariant that survives: rest-invisibility; knockout is the only")
    print("  instrument that reaches co-stabilization. See the RESULT block.")


def figure(res: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    cs = res["cs"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))

    ax = axes[0]
    ax.plot(cs, res["cascade"], "o-", color="#d62728")
    ax.set_xlabel("coupling c (mutual dependence)")
    ax.set_ylabel("extra nodes lost per knockout")
    ax.set_title("(a) Knockout cascade\n(rest viability = 1.0 everywhere — watching is blind)")
    ax.grid(alpha=0.3)

    ax2 = ax.twinx()
    ax2.plot(cs, res["rest"], "s--", color="#999999", alpha=0.6)
    ax2.set_ylabel("rest viability (watching)", color="#999999")
    ax2.set_ylim(0, 1.1)

    ax = axes[1]
    ax.plot(cs, res["noise"], "^-", color="#1f77b4", label="noise viability")
    ax.plot(cs, [x / max(res["cascade"]) if max(res["cascade"]) else 0
                 for x in res["cascade"]], "o--", color="#d62728",
            alpha=0.6, label="knockout cascade (norm.)")
    ax.set_xlabel("coupling c (mutual dependence)")
    ax.set_ylabel("fraction / normalized")
    ax.set_title("(b) No trade — fragile both ways\n(noise viability FALLS as knockout cascade rises)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    fig.suptitle("Benchmark v1.9 — co-stabilization: invisible at rest, "
                 "reached only by knockout", fontsize=11)
    fig.tight_layout()
    out = outdir / "inverse_benchmark_co_stabilization.png"
    fig.savefig(out, dpi=110)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true")
    args = ap.parse_args()
    res = run_suite()
    print_summary(res)
    if args.save:
        outdir = Path(__file__).resolve().parents[2] / "tools"
        print(f"\n  figure -> {figure(res, outdir)}")


if __name__ == "__main__":
    main()
