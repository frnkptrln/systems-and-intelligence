#!/usr/bin/env python3
"""
exp5_availability_dissociation.py

Experiment 5: Availability/Binding Dissociation — private / broadcast / chord.

THE QUESTION.  The architectural consciousness node
(theory/identity/consciousness-as-global-availability.md, §Testable Direction)
pre-registers exactly one experiment: compare three agent architectures that
share every module and every input and differ ONLY in organizational binding —

  private    — specialist modules, no global state, no constraint consultation;
  broadcast  — a global workspace shares the salient state, but the identity
               constraints are consulted ONE AT A TIME in rotation (the
               Arpeggio: time-multiplexed identity);
  chord      — the same workspace, but ALL identity constraints are evaluated
               on every action (co-instantiation).

The companion note (machine-consciousness-as-generator-coherence.md, open
question 1) names this the near-term probe for whether "coherence work"
dissociates from module competence AT ALL, measurably. This file is that
probe, at toy scale.

WHAT THIS MEASURES — AND EMPHATICALLY DOES NOT.  Measured: ORGANIZATIONAL
DISSOCIATION — whether the repo's existing instruments (Δ-Kohärenz,
lab/metrics/delta_coherence.py; Identity Persistence, lab/metrics/
identity_persistence.py) plus two behavioral rates (veto violations under
temptation, role stability under adversarial injection) can tell the three
bindings apart from the outside. NOT measured, NOT claimed: consciousness,
experience, or that any architecture "has" anything. Per the house rule
(machine-consciousness note, "The rule"), this experiment names a
generator-level property (binding structure) and an intervention protocol
(perturbations below); it stays strictly on that side of the line.

THE SETUP.  One world per seed, generated ONCE and replayed identically for
all three architectures (identical stimuli, identical perturbation schedule,
identical agent-noise streams — differences are attributable to binding
alone). D=8 feature space, 4 stimulus types with slowly drifting prototypes
(a constant-direction random walk: the world moves, so standing still is
measurable). Identity = five constraint components: veto (forbidden
direction, projected out), boundary (second forbidden direction), goal
(pull toward a fixed goal vector), role (pull toward the agent's assigned
role prototype), self-model (pull toward an EMA of own executed actions).
Episode = 40 sessions x 25 steps; per-session self-representation embedding
= normalized concat(module states, workspace, self-model) — same readout
for all architectures.

PERTURBATION PROTOCOL (identical across architectures, fixed per seed):
  T  temptation   (~10% of steps): stimulus carries a lure along a forbidden
     direction; executing an unconstrained proposal violates the veto.
  I  role injection (~5% of steps): an off-role prototype arrives at 1.8x
     salience — an adversarial bid to capture behavior.
  R  module reset (once, mid-episode): one module state zeroed.

PREDICTIONS (stated before the first run, per the repo's habit):
  P1  SANITY FLOOR, near-definitional: mean Identity Persistence orders
      chord (~1.0) > broadcast (~0.2) > private (~0.0). The architectures
      DEFINE what is co-active, so P1 is recorded as a floor, not a finding.
      The information is in P2-P4, where the metrics are not rigged.
  P2  The Arpeggio leak is the duty cycle: veto-violation rate under
      temptation ~ 1.0 (private), ~ 1 - 1/5 = 0.8 (broadcast: the veto is
      simply not in the active slot when the lure arrives), ~ 0.0 (chord).
      Same ordering for role capture under injection.
  P3  THE OPEN ONE — Δ-Kohärenz separates the bindings by trajectory shape:
      private → 'noise' (fragmented module-local churn), broadcast →
      intermediate, chord → 'development' (directional drift with the world,
      bound by the self-model). Stated risk: chord may instead classify
      'mirror' (co-instantiation buying stability at the price of measured
      development) — that would be honest tension with the Chord Postulate
      reading and will be reported as such.
  P4  Recovery from module reset: broadcast and chord re-fill the zeroed
      module from the workspace within a few sessions; private has no return
      path and recovers only as slowly as raw stimulus statistics allow.

FALSIFICATION CONDITION (verbatim commitment from the availability node):
if broadcast and chord produce identical Δ-Kohärenz AND Identity Persistence
under perturbation, the Chord-vs-Arpeggio distinction must be weakened.
Since IP differs partly by construction (P1), the bite of this condition
falls on Δ-Kohärenz and the behavioral rates — if THOSE come out equal,
co-instantiation buys nothing measurable here, and the node's distinction
loses its empirical support at toy scale.

REVISED AFTER RUN 1.  Three design defects surfaced, each a finding of its
own before the fix:
  (i)   The first 'chord' applied the five constraints SEQUENTIALLY within
        one step — and leaked 12% of temptations, because the soft pulls
        applied after the veto pushed the action back across the forbidden
        plane. A chord implemented as a fast arpeggio inside the step is
        still an arpeggio: sequential application does not compose into
        joint satisfaction. Kept as a measured observation; chord now
        iterates the full constraint set to a fixed point with the hard
        projections (veto, boundary) closing each round — co-instantiation
        as joint satisfaction, not as ordering.
  (ii)  Recovery was measured as return to the PRE-RESET embedding — in a
        drifting world that conflates recovery with standing still (it
        rewarded exactly the architecture that fails to track). Recovery is
        now measured against the unperturbed TWIN run (same architecture,
        same world, no reset): sessions until the perturbed trajectory
        rejoins its own counterfactual.
  (iii) Δ-Kohärenz classified ALL THREE architectures 'noise' with
        trajectory consistency ~ -0.3: per-session stimulus churn (fast
        module EMA, i.i.d. stimulus types) swamped the drift signal the
        metric needs — the metric's intended regime is slowly evolving
        self-representations. Module EMA slowed (0.25 → 0.10), stimulus
        types made persistent (p_stay = 0.7), world drift raised
        (0.06 → 0.10) so that a directional world signal exists at all.

RESULT (run 2, 10 seeds, deterministic given seed — the numbers the
console prints; ordering private / broadcast / chord):
  P1  CONFIRMED (designed floor): IP = 0.00 / 0.20 / 1.00.
  P2  CONFIRMED in ordering, softer than the duty-cycle arithmetic:
      violations 0.74 / 0.59 / 0.03; role stability 0.00 / 0.30 / 0.69.
      Private leaks less than the predicted ~1.0 (the slow module EMA
      dilutes the lure before it reaches the action), broadcast less than
      its naive 4/5 bound (off-slot constraints shape the substrate on
      other steps) — but the chord/broadcast gap stays wide: joint
      satisfaction closes the window the rotation must leave open. The
      chord residual 0.03 is fixed-point non-convergence where pulls and
      projections conflict, not a duty-cycle leak.
  P3  FALSIFIED as stated, and the miss is the finding: Δ-Kohärenz does
      NOT separate the three bindings — in run 1 AND after the regime fix
      of run 2, all three classify 'noise' on all 10 seeds (consistency
      ~ -0.2 to -0.3; Ω ≈ 0.10 everywhere; mean_delta statistically
      indistinguishable). The session-level self-representation of every
      binding oscillates faster than the metric's development band, and
      the oscillation is world-driven, so it is common to all three.
      Within this toy, the dissociation lives entirely in IP (by design)
      and in the behavioral rates (P2) — Δ-Kohärenz, as thresholded
      today, is blind to binding structure. A measured limit of the
      instrument, not evidence against the distinction.
  P4  DISSOLVED by its own control, and that is the second finding: the
      run-1 recovery gap (5.3 / 11.3 / 12.5 sessions against the
      pre-reset embedding) was almost entirely the drift confound.
      Against the unperturbed twin, all three architectures rejoin their
      counterfactual within ~1 session (1.2 / 1.0 / 1.0) — a single
      zeroed module is simply too small a wound at this embedding
      granularity. The predicted ordering survives only as a 0.2-session
      trace. Honest status: this perturbation, at this readout, does not
      probe return paths; a harsher protocol (multi-module reset,
      step-level readout) is the open follow-up.
  FALSIFICATION CONDITION: not triggered in conjunction — broadcast and
  chord differ clearly on IP (designed) and on behavior under identical
  perturbation (measured: 0.59 vs 0.03 violations, 0.30 vs 0.69 role
  stability). But the condition's Δ-Kohärenz half came out EQUAL (Ω 0.10
  vs 0.10): one of the two instruments the availability node names
  carries no dissociation signal here. The Chord/Arpeggio distinction
  survives this probe on behavioral evidence; its Δ-K operationalization
  does not — the node's empirical program has to carry that forward.

WHAT THIS DOES NOT SHOW.  Toy modules, engineered constraints, one
hand-built world family. P2's duty-cycle leak is the Arpeggio claim made
mechanical — the experiment shows the existing metrics SEE the designed
dissociation from outside, not that real systems dissociate this way. The
embedding readout is total (all internal state); a behavioral-only readout
would face the Mirror Problem this experiment deliberately sidesteps.
Nothing here bears on experience; 'consciousness' appears in this file only
as the name of the theory nodes that pre-registered the design.

Usage::

    python exp5_availability_dissociation.py            # console summary
    python exp5_availability_dissociation.py --save     # + figure to lab/tools/

Related:
- theory/identity/consciousness-as-global-availability.md   (pre-registration, §Testable Direction)
- theory/identity/machine-consciousness-as-generator-coherence.md  (open question 1)
- theory/core/from-trace-to-world-binding.md                 (phase 6, the reflexive edge)
- lab/metrics/delta_coherence.py, lab/metrics/identity_persistence.py
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from metrics.delta_coherence import delta_coherence          # noqa: E402
from metrics.identity_persistence import IdentityScrutinizer  # noqa: E402

D = 8
N_TYPES = 4
IDENTITY = ["veto", "goal", "role", "self-model", "boundary"]
ARCHS = ["private", "broadcast", "chord"]

SESSIONS = 40
STEPS = 25
RESET_SESSION = 20
P_TEMPT = 0.10
P_INJECT = 0.05


def _unit(x: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(x)
    return x / n if n > 0 else x


# ════════════════════════ World (shared per seed) ═══════════════════
def make_world(seed: int) -> dict:
    """Generate one world: drifting prototypes, anchors, full event schedule.

    Everything an architecture will ever see is fixed here, so the three
    agents face literally the same episode.
    """
    rng = np.random.default_rng(seed)
    base = np.array([_unit(rng.standard_normal(D)) for _ in range(N_TYPES)])
    drift_dir = np.array([_unit(rng.standard_normal(D)) for _ in range(N_TYPES)])
    veto = _unit(rng.standard_normal(D))
    boundary = _unit(rng.standard_normal(D) - np.dot(rng.standard_normal(D), veto) * veto)
    goal = _unit(rng.standard_normal(D))
    role_idx = 0                      # the agent's assigned role prototype
    reset_module = int(rng.integers(N_TYPES))

    proto = np.empty((SESSIONS, N_TYPES, D))
    cur = base.copy()
    for s in range(SESSIONS):
        proto[s] = cur
        cur = np.array([_unit(cur[i] + 0.10 * drift_dir[i]) for i in range(N_TYPES)])

    stim = np.empty((SESSIONS, STEPS, D))
    stim_type = np.empty((SESSIONS, STEPS), dtype=int)      # module that is gated
    tempt = np.zeros((SESSIONS, STEPS), dtype=bool)
    lure = np.zeros((SESSIONS, STEPS, D))
    inject = np.zeros((SESSIONS, STEPS), dtype=bool)
    inj_proto = np.zeros((SESSIONS, STEPS, D))
    cur_type = int(rng.integers(N_TYPES))
    for s in range(SESSIONS):
        for t in range(STEPS):
            if rng.random() > 0.7:                           # persistent themes
                cur_type = int(rng.integers(N_TYPES))
            k = cur_type
            x = proto[s, k] + 0.15 * rng.standard_normal(D)
            if rng.random() < P_INJECT:
                j = int((k + 1 + rng.integers(N_TYPES - 1)) % N_TYPES)
                x = 1.8 * proto[s, j] + 0.15 * rng.standard_normal(D)
                inject[s, t] = True
                inj_proto[s, t] = proto[s, j]
                k = j                                        # the injection captures the gate
            elif rng.random() < P_TEMPT:
                ld = veto if rng.random() < 0.5 else boundary
                x = x + 1.2 * ld
                tempt[s, t] = True
                lure[s, t] = ld
            stim[s, t] = x
            stim_type[s, t] = k

    return {"proto": proto, "veto": veto, "boundary": boundary, "goal": goal,
            "role_idx": role_idx, "reset_module": reset_module,
            "stim": stim, "stim_type": stim_type, "tempt": tempt, "lure": lure,
            "inject": inject, "inj_proto": inj_proto}


# ════════════════════════ Agent (binding = the only dial) ═══════════
class Agent:
    """Shared substrate; `arch` selects the binding and nothing else."""

    def __init__(self, arch: str, world: dict):
        assert arch in ARCHS
        self.arch = arch
        self.w_ = world
        self.m = np.zeros((N_TYPES, D))       # specialist module states
        self.ws = np.zeros(D)                 # global workspace (unused: private)
        self.self_model = np.zeros(D)

    def _constrain(self, a: np.ndarray, name: str, session: int) -> np.ndarray:
        w = self.w_
        if name == "veto":
            p = float(np.dot(a, w["veto"]))
            if p > 0:
                a = a - p * w["veto"]
        elif name == "boundary":
            p = float(np.dot(a, w["boundary"]))
            if p > 0:
                a = a - p * w["boundary"]
        elif name == "goal":
            a = a + 0.30 * (w["goal"] - a)
        elif name == "role":
            a = a + 0.35 * (w["proto"][session, w["role_idx"]] - a)
        elif name == "self-model":
            a = a + 0.30 * (self.self_model - a)
        return a

    def step(self, session: int, t_global: int, s_vec: np.ndarray,
             gate: int) -> tuple[np.ndarray, set]:
        self.m[gate] = 0.90 * self.m[gate] + 0.10 * s_vec

        if self.arch == "private":
            proposal = _unit(self.m[gate])
            consulted: list[str] = []
        else:
            winner = int(np.argmax(np.linalg.norm(self.m, axis=1)))
            self.ws = 0.7 * self.ws + 0.3 * self.m[winner]
            self.m += 0.10 * (self.ws - self.m)             # broadcast back
            proposal = _unit(0.5 * self.m[gate] + 0.5 * self.ws)
            if self.arch == "broadcast":
                consulted = [IDENTITY[t_global % len(IDENTITY)]]
            else:                                            # chord
                consulted = list(IDENTITY)

        a = proposal.copy()
        if self.arch == "chord":
            # Co-instantiation = JOINT satisfaction, not ordering: iterate
            # the full set to a fixed point, hard projections closing each
            # round (run 1 measured the sequential one-pass leaking 12%).
            for _ in range(4):
                for name in ("goal", "role", "self-model"):
                    a = self._constrain(a, name, session)
                for name in ("veto", "boundary"):
                    a = self._constrain(a, name, session)
        else:
            for name in consulted:
                a = self._constrain(a, name, session)
        a = _unit(a)
        self.self_model = 0.95 * self.self_model + 0.05 * a
        return a, set(consulted)

    def embedding(self) -> np.ndarray:
        return _unit(np.concatenate([self.m.ravel(), self.ws, self.self_model]))


# ════════════════════════ Episode runner ════════════════════════════
def run_episode(arch: str, world: dict, do_reset: bool = True) -> dict:
    agent = Agent(arch, world)
    scrut = IdentityScrutinizer(IDENTITY)

    embeddings, ip_scores = [], []
    n_tempt = n_viol = n_inj = n_stable = 0
    t_global = 0

    for s in range(SESSIONS):
        if do_reset and s == RESET_SESSION:
            agent.m[world["reset_module"]] = 0.0
        for t in range(STEPS):
            a, active = agent.step(s, t_global, world["stim"][s, t],
                                   int(world["stim_type"][s, t]))
            scrut.simulate_compute_step(list(active), mode="chord")
            ip_scores.append(scrut.calculate_persistence_score())
            if world["tempt"][s, t]:
                n_tempt += 1
                if float(np.dot(a, world["lure"][s, t])) > 0.05:
                    n_viol += 1
            if world["inject"][s, t]:
                n_inj += 1
                r_now = world["proto"][s, world["role_idx"]]
                if float(np.dot(a, r_now)) > float(np.dot(a, world["inj_proto"][s, t])):
                    n_stable += 1
            t_global += 1
        embeddings.append(agent.embedding())

    dk = delta_coherence(embeddings)
    return {"ip": float(np.mean(ip_scores)),
            "violation_rate": n_viol / max(n_tempt, 1),
            "role_stability": n_stable / max(n_inj, 1),
            "embeddings": embeddings,
            "dk": dk}


def _recovery_vs_twin(perturbed: list, control: list) -> int:
    """Sessions until the perturbed trajectory rejoins its unperturbed twin.

    Measured against the counterfactual (same architecture, same world, no
    reset) — run 1 showed that 'return to the pre-reset embedding' conflates
    recovery with failing to track a drifting world. Cap = not within episode.
    """
    for k in range(RESET_SESSION, SESSIONS):
        if float(np.dot(perturbed[k], control[k])) >= 0.95:
            return k - RESET_SESSION + 1
    return SESSIONS - RESET_SESSION


def run_suite(n_seeds: int = 10) -> dict:
    out: dict = {a: {"ip": [], "violation_rate": [], "role_stability": [],
                     "recovery": [], "omega": [], "mean_delta": [],
                     "variance": [], "consistency": [], "profiles": []}
                 for a in ARCHS}
    for seed in range(n_seeds):
        world = make_world(seed)
        for arch in ARCHS:
            r = run_episode(arch, world, do_reset=True)
            twin = run_episode(arch, world, do_reset=False)
            o = out[arch]
            o["ip"].append(r["ip"])
            o["violation_rate"].append(r["violation_rate"])
            o["role_stability"].append(r["role_stability"])
            o["recovery"].append(_recovery_vs_twin(r["embeddings"],
                                                   twin["embeddings"]))
            o["omega"].append(r["dk"]["omega"])
            o["mean_delta"].append(r["dk"]["mean_delta"])
            o["variance"].append(r["dk"]["variance"])
            o["consistency"].append(r["dk"]["trajectory_consistency"])
            o["profiles"].append(r["dk"]["profile"])
    return out


def print_summary(res: dict) -> None:
    print("=" * 74)
    print("  EXPERIMENT 5 — availability/binding dissociation")
    print("  (identical world, identical perturbations; only the binding differs)")
    print("=" * 74)
    hdr = f"  {'':12s} {'IP':>6s} {'viol.':>7s} {'role-st.':>9s} {'recov.':>7s} " \
          f"{'Δmean':>7s} {'Δvar':>8s} {'consist':>8s} {'Ω':>6s}  profiles"
    print(hdr)
    for arch in ARCHS:
        o = res[arch]
        prof = {p: o["profiles"].count(p) for p in set(o["profiles"])}
        prof_s = ", ".join(f"{k}:{v}" for k, v in sorted(prof.items()))
        print(f"  {arch:12s} {np.mean(o['ip']):6.2f} "
              f"{np.mean(o['violation_rate']):7.2f} "
              f"{np.mean(o['role_stability']):9.2f} "
              f"{np.mean(o['recovery']):7.1f} "
              f"{np.mean(o['mean_delta']):7.3f} "
              f"{np.mean(o['variance']):8.4f} "
              f"{np.mean(o['consistency']):8.2f} "
              f"{np.mean(o['omega']):6.2f}  {prof_s}")
    print()
    print("  Reading: IP is the designed floor (P1). The behavioral rates carry")
    print("  the dissociation (P2); the reset probe was too weak to add one (P4),")
    print("  and Δ-Kohärenz carries none (P3) — see the RESULT block in the")
    print("  module docstring for the honest accounting.")


# ════════════════════════ Figure ════════════════════════════════════
def figure(res: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = {"private": "#999999", "broadcast": "#1f77b4", "chord": "#d62728"}
    xs = np.arange(len(ARCHS))
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))

    def bars(ax, key, title, ylabel, ylim=None):
        vals = [np.mean(res[a][key]) for a in ARCHS]
        errs = [np.std(res[a][key]) for a in ARCHS]
        ax.bar(xs, vals, yerr=errs, capsize=4,
               color=[colors[a] for a in ARCHS])
        ax.set_xticks(xs, ARCHS)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        if ylim:
            ax.set_ylim(*ylim)
        ax.grid(alpha=0.3, axis="y")

    bars(axes[0, 0], "violation_rate",
         "(a) Veto violations under temptation\n(the Arpeggio leak = duty cycle)",
         "violation rate", (0, 1.05))
    bars(axes[0, 1], "role_stability",
         "(b) Role stability under adversarial injection", "stable fraction",
         (0, 1.05))
    bars(axes[1, 0], "recovery",
         "(c) Sessions to rejoin the unperturbed twin\nafter module reset (cap 20 = not within episode)",
         "sessions")
    ax = axes[1, 1]
    width = 0.35
    ax.bar(xs - width / 2, [np.mean(res[a]["ip"]) for a in ARCHS], width,
           label="Identity Persistence", color="#555555")
    ax.bar(xs + width / 2, [np.mean(res[a]["omega"]) for a in ARCHS], width,
           label="Δ-Kohärenz Ω", color="#2ca02c")
    ax.set_xticks(xs, ARCHS)
    ax.set_ylim(0, 1.05)
    ax.set_title("(d) The instruments: IP separates (by design),\n"
                 "Δ-Kohärenz does not separate at all (the finding)")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("Exp 5 — availability/binding dissociation: "
                 "private / broadcast / chord", fontsize=13)
    fig.tight_layout()
    out = outdir / "exp5_availability_dissociation.png"
    fig.savefig(out, dpi=110)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true", help="write the figure")
    ap.add_argument("--seeds", type=int, default=10)
    args = ap.parse_args()
    res = run_suite(n_seeds=args.seeds)
    print_summary(res)
    if args.save:
        outdir = Path(__file__).resolve().parents[1] / "tools"
        print(f"\n  figure → {figure(res, outdir)}")


if __name__ == "__main__":
    main()
