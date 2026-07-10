"""
co_stabilization.py

Mutual-dependence knockout toy: a first co-stabilization candidate. (Benchmark v1.9)

THE QUESTION.  v1.8 measured composition — two coupled generators whose
joint trace empties the single-generator equivalence class. But composition
is not yet life. The ladder note's synthesis names the missing threshold:
"a self-maintaining composition of processes whose functions make
differences for one another" — CO-STABILIZATION, each function holding the
others in a viable regime. This file tests a first candidate operationalization: designed mutual
dependence on a fixed ring. The pre-run proposal treated a super-additive
knockout cascade as the signature of co-stabilization. The run measured that
cascade, but its failed noise prediction shows that the model establishes
dependency fragility, not yet ecological self-maintenance. The original
predictions remain below; the post-run calibration states what survived.

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

PREDICTIONS (stated before the first run; original language retained,
with interpretation recalibrated in RESULT and POST-RUN CALIBRATION):
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
  P1  CONFIRMED WITHIN THE CONSTRUCTION: rest viability = 1.00 at every
      c because s = 1-c makes h=1 a fixed point by design. The homogeneous
      rest state cannot identify c; this does not establish that ecological
      co-stabilization generally lacks passive signatures.
  P2  CONFIRMED AS DEPENDENCY: the knockout cascade is 0 for c <= 0.7,
      then +2 extra nodes at c=0.8-0.9, +4 at c=0.95, and +15 at c=1.0.
      Knockout exposes the dependency designed into the rule. A super-
      additive cascade does not by itself demonstrate self-maintenance.
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
      follow-up below. What survives is narrower: the homogeneous fixed
      point does not identify c, while knockout separates dependencies
      among the three probes run here.
  P4  NOT ESTABLISHED AS A PHASE TRANSITION: the first threshold crossing
      lies between sampled c=0.7 and c=0.8, then the finite cascade climbs
      in steps. Its location depends on viability cutoff, ring size,
      topology, and the coarse c grid. Total collapse at c=1.0 is the
      boundary where self-sufficiency is exactly zero. Scaling is required
      before "critical coupling" would be justified.

POST-RUN CALIBRATION. The experiment operationalizes mutual dependence,
not co-stabilization itself. Super-additive loss shows that other nodes
depend on the knocked-out node under the chosen update rule. Self-maintenance
would require the coupled organization to contribute robustness or continued
viability that the parts lack alone; this substitution model does the
opposite under noise. The failed P3 therefore rejects this first candidate
as an ecology in the stronger sense.

WHAT THIS DOES NOT SHOW. A fixed ring with a linear averaging rule is not an
ecology that composes and dissolves on its own. Nothing is selected or
reproduces; health is a scalar threshold, not metabolism; and the all-healthy
rest state is identical by construction. Knockout is the separating probe
among the three probes run here, not the only conceivable identifying
intervention. The apparent onset is a threshold crossing in a finite,
thresholded graph, not an established phase transition.

Two follow-ups remain: (a) a REDUNDANCY model in which coupling adds a
compensating pathway while self-sufficiency is retained, tested across
topology, N, viability cutoff, and coupling resolution; and (b) a population
model where coupling is built and broken by the processes. Until one of
those shows mutual maintenance rather than designed dependency,
co-stabilization remains [HYPOTHESIZED]. No consciousness claim follows.

Usage::

    python co_stabilization.py            # console summary (~5 s)
    python co_stabilization.py --save      # + figure to lab/tools/

Related:
- theory/computation/static-information-and-living-process.md  (the open threshold this candidate failed to establish)
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
    print("  BENCHMARK v1.9 — mutual dependence under knockout (candidate model)")
    print(f"  (N={N} ring, knockout cascade + noise robustness vs coupling c)")
    print("=" * 72)
    print(f"\n  {'c':>6s} {'rest viability':>15s} {'knockout cascade':>18s} "
          f"{'noise viability':>16s}")
    for i, c in enumerate(res["cs"]):
        print(f"  {c:6.2f} {res['rest'][i]:15.2f} {res['cascade'][i]:18.2f} "
              f"{res['noise'][i]:16.3f}")
    print("\n  cascade = mean extra nodes lost per knockout, beyond the 1 removed")
    print("  (0 = additive; large = super-additive dependency under this rule)")
    print("\n  Reading: the homogeneous rest state is blind to c by design;")
    print("  knockout exposes super-additive dependency. The predicted noise")
    print("  robustness is FALSIFIED: substitution coupling is fragile both")
    print("  ways. This rejects the candidate as ecological co-stabilization;")
    print("  it does not close the self-maintenance question. See CALIBRATION.")


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
    ax.set_title("(a) Knockout cascade\n(homogeneous rest is blind by construction)")
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
    ax.set_title("(b) Candidate fails resilience\n(substitution coupling is fragile both ways)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    fig.suptitle("Benchmark v1.9 — mutual dependence: knockout reveals fragility",
                  fontsize=11)
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
