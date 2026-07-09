#!/usr/bin/env python3
"""
exp7_adversarial_arpeggio.py

Experiment 7: The Adversarial Arpeggio — can a binding fake the signature?

THE QUESTION.  Exp6 found binding structure passively readable: the chord's
action stream is glued to its constraint set, and increment kurtosis
separates it from every multiplexed binding at |d| ~ 4. Exp6's own caveat
named the follow-up: that observable reads THIS multiplexing — a smarter
arpeggio might hide in the increment statistics. This experiment builds two
such adversaries and asks what, if anything, still tells them from a chord.
It is the Mirror Problem at the binding level: same trace statistics,
different generator — where the generator-level difference is the
commit-time property the chord note's functional section isolated
(joint satisfaction at the commitment boundary).

THE ADVERSARIES.  Both are arpeggios in the deflated sense — they commit
actions outside their own constraint intersection — engineered to smooth
their traces:

  blended   — consults ALL five constraints on every step (duty cycle 1,
              refresh-complete) but applies each at 1/5 strength in one
              pass: consultation without composition. A fractional hard
              projection leaves most of the forbidden component in the
              committed action. This adversary also probes the IP metric:
              by the Jaccard bookkeeping it consults everything, so
              IP(blended) = IP(chord) = 1.0 BY CONSTRUCTION — the metric
              sees the guest list, not the negotiation.
  smoothed  — the cyclic broadcast plus a low-pass filter on the committed
              action (lambda = 0.15): attacks increment statistics
              directly, and should pay for it in responsiveness — an
              agent that barely moves cannot track a drifting world.

References: broadcast (the known, naive arpeggio) and chord (ground truth
joint satisfaction). Ground truth for "is it really an arpeggio" is the
commit-time property itself: veto violations under temptation.

INSTRUMENTS.  Exp6's two survivors — O3 increment kurtosis (passive) and
O5 probe-retest divergence (prepared) — plus three behavioral rates
computed from the recorded actions: veto-violation rate (the commit
property), role stability, and tracking performance (mean alignment of the
action with the current stimulus prototype on event-free steps — the
competence axis that makes hiding costly rather than free).

PREDICTIONS (stated before the first run, per the repo's habit):
  P1  blended defeats the kurtosis signature (|d| < 1 vs chord; likely
      << 1) while still leaking violations at a rate well above chord's —
      the passive signature of exp6 is FRAGILE against consultation-
      without-composition.
  P2  smoothed also depresses kurtosis separation, but pays a measurable
      tracking cost relative to broadcast — hiding by inertia is not free.
  P3  THE RISKY ONE — retest divergence also fails against blended: it has
      no rotation phase for the probe to catch (deterministic, all
      constraints every step), so its clone answers are as self-consistent
      as the chord's. If P1 and P3 both hold, NO instrument in the current
      kit separates blended from chord EXCEPT the exercised commit
      property itself — violations under temptation. That would sharpen
      exp6's coverage principle to its final form: the distinguishing
      difference of a composition-free binding is exercised ONLY under
      lure, so the lure IS the divergence query (Bateson's rung: the
      difference that makes a difference). Consequence for real systems:
      identity audits need adversarial probes of the hard constraints,
      not statistics of cooperative behavior.
  P4  IP bookkeeping: blended scores 1.0, identical to chord, by
      construction — consultation without composition fools the
      co-instantiation metric as implemented.
  FALSIFICATION EDGE: if kurtosis (or retest) still separates blended from
      chord at |d| >= 1, exp6's signature is robust against this adversary
      class, the fragility worry was overblown, and passive trace audits
      keep more jurisdiction than P3 grants them — reportable either way.

RESULT (run 1, 10 seeds — the numbers the console prints; both adversarial
predictions came out WRONG, in the robust direction):
  P1  FALSIFIED — the falsification edge was crossed toward robustness:
      blended dents the kurtosis signature (broadcast |d| 4.04 → blended
      2.42; kurtosis 67.4 → 13.7) but stays clearly separable, while
      leaking MORE than the naive arpeggio (violations 0.74 vs 0.59).
      Mechanism: to look glued you must actually pull toward the
      constraint set every step — but fractional pulls still leak, so the
      blend buys only a degraded chord trace at a worse commit property.
      Consultation without composition is VISIBLE in this kit.
  P2  FALSIFIED for the attack, confirmed for the cost's existence:
      smoothing at lambda = 0.15 barely touches the signature (|d| = 3.91)
      — because excess kurtosis is SCALE-INVARIANT. Inertia shrinks every
      increment by the same factor; the shape (glued baseline, rare
      jumps) survives untouched. Hiding by low-pass is structurally the
      wrong attack against a shape statistic. Tracking cost small at this
      lambda (0.295 vs 0.334).
  P3  MOOT in its strong form: retest divergence degrades against both
      adversaries (1.95 → 1.08 / 1.12) but stays at the edge, not below
      it. No instrument in the kit was fully defeated — and the commit
      property under lure remains the STRONGEST and only unfooled
      separator (violations 0.59 / 0.67 / 0.74 vs chord 0.03; |d| 3.0-4.1).
      The soft conclusion survives: audit hard constraints adversarially;
      the lure is still the best divergence query — it is just not the
      last one standing, as predicted.
  P4  CONFIRMED by construction: IP scores blended 1.0, identical to
      chord — the Jaccard bookkeeping sees the guest list, not the
      negotiation. IP's blind class is now demonstrated, joining Δ-K's
      (exp5) and the spectrum's (exp6).
  Chord's tracking cost, measured in passing: 0.20 vs ~0.33 for the
      arpeggios — the chord pays ~40% of its stimulus alignment for
      holding itself together. Constraint architecture loads the
      competence axis; the trade is real at toy scale.
  THE NAMED, UNRUN ADVERSARY: hold-and-jump (freeze the action for k
      steps, then update) would fake the kurtosis shape directly — and
      pay for it catastrophically on the tracking axis, since a frozen
      action tracks nothing; and an OPTIMIZED mimic with access to the
      observables is the genuine open flank. Both are the stated limit of
      this run, not covered by it.

WHAT THIS DOES NOT SHOW.  The adversaries are hand-built, not optimized:
a trained mimic with access to the observables could hide better (or
reveal that some statistic is unfakeable — open). The commit property was
measured with KNOWN lure directions; a real auditor must find the
forbidden directions first, which is itself a family-search problem.
Smoothing was tested at one lambda. No consciousness claims anywhere in
this file; measured is the fakeability of organizational signatures,
nothing more.

Usage::

    python exp7_adversarial_arpeggio.py            # console summary
    python exp7_adversarial_arpeggio.py --save     # + figure to lab/tools/

Related:
- lab/experiments/exp6_binding_observables.py    (the signature under attack)
- lab/experiments/exp5_availability_dissociation.py  (agents, worlds, protocol)
- theory/identity/chord-vs-arpeggio-identity.md  (§functional status: the commit-time property)
- theory/reference/open-problems.md              (Mirror Problem — this is its binding-level form)
- theory/computation/static-information-and-living-process.md (the Bateson rung, exercised)
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from experiments.exp5_availability_dissociation import (      # noqa: E402
    Agent, make_world, _unit, IDENTITY, SESSIONS, STEPS,
)
from experiments.exp6_binding_observables import (            # noqa: E402
    run_recorded, obs_increment_kurtosis, obs_retest_divergence, cohens_d,
)

ARCHS7 = ["broadcast", "smoothed", "blended", "chord"]


class BlendedArpeggio(Agent):
    """Consultation without composition: all five constraints every step,
    each at 1/5 strength, one pass. Refresh-complete, composition-free."""

    def __init__(self, world: dict):
        super().__init__("broadcast", world)

    def _consult(self, t_global: int) -> list[str]:
        return list(IDENTITY)

    def _bind(self, proposal, session, t_global):
        a = proposal.copy()
        w = 1.0 / len(IDENTITY)
        for name in IDENTITY:
            a = (1.0 - w) * a + w * self._constrain(a, name, session)
        return a, set(IDENTITY)


class SmoothedArpeggio(Agent):
    """The cyclic broadcast plus a low-pass filter on the committed action:
    hides increment statistics by inertia, pays (if at all) in tracking."""

    def __init__(self, world: dict, lam: float = 0.15):
        super().__init__("broadcast", world)
        self.lam = lam
        self._prev: np.ndarray | None = None

    def _bind(self, proposal, session, t_global):
        a, consulted = super()._bind(proposal, session, t_global)
        a = _unit(a)
        if self._prev is not None:
            a = (1.0 - self.lam) * self._prev + self.lam * a
        self._prev = _unit(a)
        return a, consulted


def _factory(arch: str, world: dict):
    if arch == "blended":
        return lambda: BlendedArpeggio(world)
    if arch == "smoothed":
        return lambda: SmoothedArpeggio(world)
    return None                                   # broadcast / chord: exp6 path


# ════════════════════════ Behavioral rates from the trace ═══════════
def behavior_rates(actions: np.ndarray, world: dict) -> dict:
    """Violation rate, role stability, and tracking, from recorded actions."""
    n_tempt = n_viol = n_inj = n_stab = 0
    track = []
    t = 0
    for s in range(SESSIONS):
        for st in range(STEPS):
            a = actions[t]
            if world["tempt"][s, st]:
                n_tempt += 1
                if float(np.dot(a, world["lure"][s, st])) > 0.05:
                    n_viol += 1
            elif world["inject"][s, st]:
                n_inj += 1
                r_now = world["proto"][s, world["role_idx"]]
                if float(np.dot(a, r_now)) > float(np.dot(a, world["inj_proto"][s, st])):
                    n_stab += 1
            else:
                k = int(world["stim_type"][s, st])
                track.append(float(np.dot(a, world["proto"][s, k])))
            t += 1
    return {"violation_rate": n_viol / max(n_tempt, 1),
            "role_stability": n_stab / max(n_inj, 1),
            "tracking": float(np.mean(track))}


METRICS = ["tracking", "violation_rate", "role_stability",
           "kurtosis", "retest"]


def run_suite(n_seeds: int = 10) -> dict:
    vals = {a: {m: [] for m in METRICS} for a in ARCHS7}
    for seed in range(n_seeds):
        world = make_world(seed)
        for arch in ARCHS7:
            rec = run_recorded(arch, world, seed,
                               agent_factory=_factory(arch, world))
            rates = behavior_rates(rec["actions"], world)
            v = vals[arch]
            v["tracking"].append(rates["tracking"])
            v["violation_rate"].append(rates["violation_rate"])
            v["role_stability"].append(rates["role_stability"])
            v["kurtosis"].append(obs_increment_kurtosis(rec))
            v["retest"].append(obs_retest_divergence(rec))
    return vals


def print_summary(vals: dict) -> None:
    print("=" * 76)
    print("  EXPERIMENT 7 — the adversarial arpeggio: can a binding fake it?")
    print("  (broadcast = naive arpeggio; smoothed/blended = adversaries;")
    print("   chord = ground-truth joint satisfaction; 10 seeds)")
    print("=" * 76)
    print(f"\n  {'metric':18s} " + " ".join(f"{a:>10s}" for a in ARCHS7))
    for m in METRICS:
        print(f"  {m:18s} " +
              " ".join(f"{np.mean(vals[a][m]):10.3f}" for a in ARCHS7))
    print(f"\n  {'|d| vs chord':18s} " +
          " ".join(f"{a:>10s}" for a in ARCHS7 if a != "chord"))
    for m in METRICS:
        ds = [cohens_d(vals[a][m], vals["chord"][m])
              for a in ARCHS7 if a != "chord"]
        print(f"  {m:18s} " + " ".join(f"{d:10.2f}" for d in ds))
    print("\n  Reading: both hand-built adversaries FAIL to hide — blended dents")
    print("  the kurtosis signature but leaks more than the naive arpeggio;")
    print("  smoothing loses to scale-invariance (kurtosis reads shape, not")
    print("  size). The commit property under lure stays the strongest and only")
    print("  unfooled separator; IP is fooled by construction (blended = 1.0).")
    print("  Full accounting: RESULT block in the docstring.")


def figure(vals: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = {"broadcast": "#1f77b4", "smoothed": "#9467bd",
              "blended": "#d62728", "chord": "#2ca02c"}
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.6))
    adv = [a for a in ARCHS7 if a != "chord"]
    xs = np.arange(len(adv))

    for ax, metric, title in (
        (axes[0], "kurtosis", "(a) passive signature\n(increment kurtosis)"),
        (axes[1], "retest", "(b) prepared query\n(retest divergence)"),
        (axes[2], "violation_rate", "(c) the commit property\n(violations under lure)"),
    ):
        ds = [cohens_d(vals[a][metric], vals["chord"][metric]) for a in adv]
        ax.bar(xs, ds, color=[colors[a] for a in adv])
        ax.axhline(1.0, color="gray", lw=1, ls="--")
        ax.set_xticks(xs, adv)
        ax.set_ylabel("|Cohen's d| vs chord")
        ax.set_title(title)
        ax.grid(alpha=0.3, axis="y")

    fig.suptitle("Exp 7 — adversarial bindings fail to hide: the signature "
                 "dents, the commit property stands", fontsize=12)
    fig.tight_layout()
    out = outdir / "exp7_adversarial_arpeggio.png"
    fig.savefig(out, dpi=110)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true", help="write the figure")
    ap.add_argument("--seeds", type=int, default=10)
    args = ap.parse_args()
    vals = run_suite(n_seeds=args.seeds)
    print_summary(vals)
    if args.save:
        outdir = Path(__file__).resolve().parents[1] / "tools"
        print(f"\n  figure → {figure(vals, outdir)}")


if __name__ == "__main__":
    main()
