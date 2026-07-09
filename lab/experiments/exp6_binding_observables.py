#!/usr/bin/env python3
"""
exp6_binding_observables.py

Experiment 6: Which observable carries binding structure?

THE QUESTION.  Exp5 left one loose end, and it is the sharp one: the
observables that separated the bindings (veto violations, role stability)
are RESPONSES TO PERTURBATIONS, while Δ-Kohärenz — which separated nothing
— WATCHES the trajectory passively. That pattern is the measurement note's
hierarchy (watching < perturbing < preparing;
theory/core/measurement-as-weak-intervention.md) surfacing in the identity
layer. So the precise question: is binding structure readable from passive
traces at all, or only under intervention?

THE TENSION, stated before running.  The spine gives arguments in BOTH
directions. Against passive readability: binding is a generator-level
property, and the trace underdetermines the generator. For passive
readability: unlike the CA benchmark's never-visited neighborhoods, the
binding difference is EXERCISED ON EVERY STEP — an arpeggio multiplexes
constraints each tick, a chord co-satisfies them each tick — and by the
coverage argument a difference the dynamics exercise is IN the trace.
Under that reading, Δ-Kohärenz failed in exp5 not because passive
observation is insufficient but because it aggregates at the wrong level:
session-scale, unconditioned first/second moments of a normalized
embedding. This experiment decides between the readings.

THE SETUP.  Exp5's worlds and agents, unchanged (imported), no module
reset; 10 seeds; four bindings now, because the honest test needs it:

  private          — no workspace, no constraints (easy floor)
  broadcast        — workspace + CYCLIC constraint rotation (period 5)
  arpeggio-random  — workspace + uniformly RANDOM constraint each step;
                     same duty cycle as broadcast, no schedule. Separates
                     "reads the schedule" from "reads the multiplexing".
  chord            — workspace + joint satisfaction (fixed point)

Five observables, one scalar each per (seed, arch). Passive family
(computed from the unperturbed action/embedding stream alone):

  O1  Δ-Kohärenz Ω on session embeddings        (exp5's instrument; baseline)
  O2  inter-module binding: mean pairwise cosine among module states
  O3  action-increment kurtosis: excess kurtosis of ||a_t - a_{t-1}||.
      The mixture signature — multiplexed constraints should make action
      increments a heavy-tailed mixture; co-instantiation, one smooth pull.
  O4  rotation-spectrum: relative FFT power of the action stream at the
      rotation frequency (period 5 and harmonic). Reads the SCHEDULE.

Interventional family (prepared-state queries, regime 3+ of the
measurement note — the strongest rung):

  O5  test-retest divergence: Q fixed probe stimuli, each presented to a
      CLONE of the agent's current state at K spread-out times; scalar =
      mean pairwise distance between responses to the same probe across
      times. A chord answers from the same co-active constraints every
      time; an arpeggio's answer depends on which constraint its clock
      holds when you ask.

Separability score: |Cohen's d| across the 10 seeds, reported for the two
boundaries that matter — broadcast vs chord (schedule available) and
arpeggio-random vs chord (schedule removed). Private is reported as the
floor column only.

PREDICTIONS (stated before the first run, per the repo's habit):
  P1  O1 (Ω) separates nothing on either boundary (replicates exp5's
      blindness; |d| < 0.5).
  P2  O4 (rotation spectrum) separates broadcast/chord with large |d| but
      COLLAPSES on arpeggio-random/chord — it reads the schedule, not the
      binding. This is the control that keeps a cheap win honest.
  P3  THE DECIDING ONE — O3 (increment kurtosis) separates BOTH arpeggios
      from chord with at least moderate |d|: the multiplexing is exercised
      every step, so its mixture character is in the passive trace
      (coverage argument). If O3 fails too, passive trace statistics of
      this whole family cannot see binding, and the generator-level
      reading wins outright.
  P4  O5 (retest divergence) separates both arpeggios from chord with the
      LARGEST |d| of any observable — the prepared-query rung of the
      hierarchy buys more than any passive statistic, even where passive
      statistics work.
  FALSIFICATION EDGE: if some passive observable matches or beats O5 on
      the arpeggio-random/chord boundary, then for constantly-exercised
      organizational differences the intervention hierarchy buys nothing
      here, and the measurement note's application to identity
      instruments loses this support — reportable either way.

RESULT (run 1, 10 seeds — the numbers the console prints; the chord
kurtosis mechanism was diagnosed on seed 0 before this block was written):
  P1  CONFIRMED: Ω is blind (|d| = 0.20 / 0.17; means identical to three
      decimals across all four bindings).
  P2  HALF-CONFIRMED, with a methods lesson worth the price: without the
      schedule the rotation-reader's ABSOLUTE signal collapses ~75-fold
      (relative power 0.297 → 0.004), yet its nominal |d| stays "large"
      (4.19) — because the chord baseline is exactly 0.000 with near-zero
      variance, and Cohen's d flatters any offset against a silent
      channel. Rule kept: never believe a standardized effect without an
      absolute one next to it.
  P3  CONFIRMED in separability (|d| = 4.04 cyclic / 4.09 random — passive
      statistics DO see binding on both boundaries), but the MECHANISM
      came out inverted: predicted heavy-tailed arpeggios vs a smooth
      chord; measured near-Gaussian arpeggios (kurtosis ~ -0.5 to 0.2)
      vs chord kurtosis ~ 67. Diagnosis (checked step-by-step): joint
      satisfaction GLUES the action to the constraint set — median
      increment 0.0004 — so the stream moves only when the anchors
      themselves move (the once-per-session role-prototype drift), and
      rare shocks on an ultra-smooth baseline are extreme kurtosis.
      Excluding temptation/injection-adjacent increments RAISES it
      (52 vs 49, seed 0): the signature is constraint-binding, not event
      response. Binding structure is in the passive trace — at the
      increment level, not the session level.
  P4  FALSIFIED IN RANK — the falsification edge WAS crossed: the
      prepared query (O5) separates cleanly (|d| = 1.95 on both
      boundaries; a chord answers the same probe ~2x more consistently
      than either arpeggio, private is the least consistent of all at
      1.13) but LOSES to the passive increment statistic (|d| ~ 4.1) on
      the schedule-free boundary. For an organizational difference that
      is exercised at every step, coverage is total — and watching at the
      right level suffices. This does not overturn the v1.1 hierarchy; it
      LOCATES it: intervention buys signal where the trace has coverage
      gaps (unseen neighborhoods, resting attractors, differences the
      dynamics never exercise) — which is exactly the Mirror Problem's
      regime, where the mirror and the developing agent produce the same
      exercised trace. The measurement note's application to identity
      instruments inherits that qualifier.
  O2, unpredicted null: inter-module cosine separates private from every
      workspace binding (0.009 vs 0.936) and broadcast from chord not at
      all (|d| = 0.00) — the workspace, not the binding, sets module
      alignment.
  READING.  Δ-Kohärenz's exp5 blindness was a wrong-LEVEL failure, not
      evidence that binding is trace-invisible. The cheap upgrade for the
      identity suite is per-step increment statistics; probe-retest
      protocols remain the right tool precisely where the distinguishing
      difference is NOT constantly exercised. Coverage decides which.

WHAT THIS DOES NOT SHOW.  Same toy caveats as exp5: engineered constraints,
hand-built world, total-state readout for clones (a real system cannot be
cloned at will — O5's 'preparing' rung is exactly the privilege real
observers lack; that asymmetry is the point of the Mirror Problem, not a
refutation of it). Kurtosis reads THIS multiplexing; a smarter arpeggio
(smoothed, annealed constraint blending) could hide in the increment
statistics — adversarial bindings are the open follow-up. The chord's
spike timing is partly an artifact of session-quantized world drift; a
continuously drifting world is the robustness check to run before leaning
on the exact kurtosis value (the load-bearing feature is the glued
baseline, which would survive). No consciousness claims; measured is
which observables see organizational structure, nothing more.

Usage::

    python exp6_binding_observables.py            # console summary
    python exp6_binding_observables.py --save     # + figure to lab/tools/

Related:
- lab/experiments/exp5_availability_dissociation.py   (the loose end this picks up)
- theory/core/measurement-as-weak-intervention.md      (the hierarchy under test, identity edition)
- theory/identity/consciousness-as-global-availability.md  (instrument program)
- lab/benchmarks/inverse-reconstruction/README.md      (coverage argument; v1.1 hierarchy)
"""

from __future__ import annotations

import argparse
import copy
import os
import sys
from pathlib import Path

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from metrics.delta_coherence import delta_coherence                    # noqa: E402
from experiments.exp5_availability_dissociation import (               # noqa: E402
    Agent, make_world, _unit, IDENTITY, SESSIONS, STEPS, D, N_TYPES,
)

ARCHS6 = ["private", "broadcast", "arpeggio-random", "chord"]
N_PROBES = 8
N_PROBE_TIMES = 20


class RandomArpeggioAgent(Agent):
    """Broadcast binding with a schedule-free constraint draw.

    Same 1/5 duty cycle as the cyclic broadcast, but the active constraint
    is drawn uniformly at random each step — removing the periodic
    signature while keeping the multiplexing. Own rng, fixed per seed.
    """

    def __init__(self, world: dict, seed: int):
        super().__init__("broadcast", world)
        self._rng = np.random.default_rng(10_000 + seed)

    def _consult(self, t_global: int) -> list[str]:
        return [IDENTITY[int(self._rng.integers(len(IDENTITY)))]]


def _make_agent(arch: str, world: dict, seed: int) -> Agent:
    if arch == "arpeggio-random":
        return RandomArpeggioAgent(world, seed)
    return Agent(arch, world)


# ════════════════════════ Episode with recordings ═══════════════════
def run_recorded(arch: str, world: dict, seed: int,
                 agent_factory=None) -> dict:
    """One unperturbed episode; record actions, embeddings, module cosines,
    and probe-retest responses from cloned states.

    `agent_factory` (optional, no-arg callable) lets other experiments —
    exp7's adversarial bindings — reuse this runner with their own agents.
    """
    rng = np.random.default_rng(20_000 + seed)
    probes = np.array([_unit(rng.standard_normal(D)) for _ in range(N_PROBES)])
    total = SESSIONS * STEPS
    probe_times = set(np.linspace(total * 0.1, total * 0.95,
                                  N_PROBE_TIMES).astype(int).tolist())

    agent = agent_factory() if agent_factory is not None \
        else _make_agent(arch, world, seed)
    actions = np.empty((total, D))
    sess_emb, mod_cos = [], []
    responses: list[np.ndarray] = []           # (n_times, N_PROBES, D)

    t_global = 0
    for s in range(SESSIONS):
        for t in range(STEPS):
            if t_global in probe_times:
                resp = np.empty((N_PROBES, D))
                for q in range(N_PROBES):
                    clone = copy.deepcopy(agent)
                    a_q, _ = clone.step(s, t_global, probes[q],
                                        int(world["stim_type"][s, t]))
                    resp[q] = a_q
                responses.append(resp)
            a, _ = agent.step(s, t_global, world["stim"][s, t],
                              int(world["stim_type"][s, t]))
            actions[t_global] = a
            sims = [float(np.dot(_unit(agent.m[i]), _unit(agent.m[j])))
                    for i in range(N_TYPES) for j in range(i + 1, N_TYPES)
                    if np.linalg.norm(agent.m[i]) > 0
                    and np.linalg.norm(agent.m[j]) > 0]
            mod_cos.append(float(np.mean(sims)) if sims else 0.0)
            t_global += 1
        sess_emb.append(agent.embedding())

    return {"actions": actions, "sess_emb": sess_emb,
            "mod_cos": float(np.mean(mod_cos)),
            "responses": np.array(responses)}


# ════════════════════════ Observables ═══════════════════════════════
def obs_omega(rec: dict) -> float:
    """O1 — exp5's instrument, unchanged."""
    return delta_coherence(rec["sess_emb"])["omega"]


def obs_intermodule(rec: dict) -> float:
    """O2 — mean pairwise cosine among module states."""
    return rec["mod_cos"]


def obs_increment_kurtosis(rec: dict) -> float:
    """O3 — excess kurtosis of action-increment norms (mixture signature)."""
    d = np.linalg.norm(np.diff(rec["actions"], axis=0), axis=1)
    mu, sd = d.mean(), d.std()
    if sd == 0:
        return 0.0
    return float(np.mean(((d - mu) / sd) ** 4) - 3.0)


def obs_rotation_power(rec: dict) -> float:
    """O4 — relative spectral power at the rotation frequency (period 5)."""
    a = rec["actions"] - rec["actions"].mean(axis=0)
    P = np.abs(np.fft.rfft(a, axis=0)) ** 2       # (freqs, D)
    total = P[1:].sum()
    if total == 0:
        return 0.0
    n = a.shape[0]
    idx = [round(n / 5 * k) for k in (1, 2)]      # fundamental + harmonic
    band = sum(P[i - 1:i + 2].sum() for i in idx)
    return float(band / total)


def obs_retest_divergence(rec: dict) -> float:
    """O5 — same probe, cloned state, K times: mean pairwise response
    distance per probe, averaged over probes."""
    R = rec["responses"]                          # (K, Q, D)
    K = R.shape[0]
    div = []
    for q in range(R.shape[1]):
        X = R[:, q, :]
        dists = [np.linalg.norm(X[i] - X[j])
                 for i in range(K) for j in range(i + 1, K)]
        div.append(float(np.mean(dists)))
    return float(np.mean(div))


OBSERVABLES = [
    ("O1 Δ-Kohärenz Ω (passive)", obs_omega),
    ("O2 inter-module cos (passive)", obs_intermodule),
    ("O3 increment kurtosis (passive)", obs_increment_kurtosis),
    ("O4 rotation spectrum (passive)", obs_rotation_power),
    ("O5 retest divergence (prepared)", obs_retest_divergence),
]


def cohens_d(x: list, y: list) -> float:
    x, y = np.asarray(x, float), np.asarray(y, float)
    sp = np.sqrt((x.var(ddof=1) + y.var(ddof=1)) / 2.0)
    if sp == 0:
        return 0.0
    return float(abs(x.mean() - y.mean()) / sp)


# ════════════════════════ Suite ═════════════════════════════════════
def run_suite(n_seeds: int = 10) -> dict:
    vals = {a: {name: [] for name, _ in OBSERVABLES} for a in ARCHS6}
    for seed in range(n_seeds):
        world = make_world(seed)
        for arch in ARCHS6:
            rec = run_recorded(arch, world, seed)
            for name, fn in OBSERVABLES:
                vals[arch][name].append(fn(rec))
    return vals


def print_summary(vals: dict) -> None:
    print("=" * 78)
    print("  EXPERIMENT 6 — which observable carries binding structure?")
    print("  (four bindings, five observables, |Cohen's d| across 10 seeds)")
    print("=" * 78)
    print(f"\n  {'observable':34s} " +
          " ".join(f"{a[:9]:>10s}" for a in ARCHS6))
    for name, _ in OBSERVABLES:
        print(f"  {name:34s} " +
              " ".join(f"{np.mean(vals[a][name]):10.3f}" for a in ARCHS6))
    print(f"\n  {'separability |d|':34s} {'bc/chord':>10s} {'rnd/chord':>10s}")
    for name, _ in OBSERVABLES:
        d_bc = cohens_d(vals["broadcast"][name], vals["chord"][name])
        d_rn = cohens_d(vals["arpeggio-random"][name], vals["chord"][name])
        print(f"  {name:34s} {d_bc:10.2f} {d_rn:10.2f}")
    print("\n  Reading: binding IS passively readable at the right level — the")
    print("  increment statistic (O3) beats the prepared query (O5) because the")
    print("  difference is exercised every step (total coverage). O4's random-")
    print("  boundary |d| is a zero-variance artifact (absolute signal ~ 0),")
    print("  and Ω stays blind. Full accounting: RESULT block in the docstring.")


# ════════════════════════ Figure ════════════════════════════════════
def figure(vals: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = [n for n, _ in OBSERVABLES]
    short = ["Ω", "inter-mod", "kurtosis", "rot-spec", "retest"]
    d_bc = [cohens_d(vals["broadcast"][n], vals["chord"][n]) for n in names]
    d_rn = [cohens_d(vals["arpeggio-random"][n], vals["chord"][n]) for n in names]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    xs = np.arange(len(names))
    w = 0.38
    ax.bar(xs - w / 2, d_bc, w, label="broadcast (cyclic) vs chord",
           color="#1f77b4")
    ax.bar(xs + w / 2, d_rn, w, label="arpeggio (random) vs chord",
           color="#d62728")
    ax.axhline(0.5, color="gray", lw=1, ls="--")
    ax.text(len(names) - 0.45, 0.55, "|d| = 0.5", color="gray", fontsize=8)
    ax.annotate("d-artifact:\nabs. signal ≈ 0", xy=(3 + w / 2, d_rn[3]),
                xytext=(3.15, d_rn[3] + 1.2), fontsize=8, color="#d62728",
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=0.8))
    ax.set_xticks(xs, short)
    ax.set_ylabel("|Cohen's d| across seeds")
    ax.set_title("Exp 6 — binding-structure separability per observable\n"
                 "(passive: Ω, inter-mod, kurtosis, rot-spec · prepared query: retest)")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    out = outdir / "exp6_binding_observables.png"
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
