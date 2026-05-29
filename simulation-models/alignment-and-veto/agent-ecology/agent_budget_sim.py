"""
agent_budget_sim.py

Agent-ecology stress test for the Viable Corridor paper — Class C predictions
P7 (hard vs. soft budgets) and P8 (constraint architecture dominates capability).

WHY A SECOND MODEL.  Appendix C of `papers/viable-corridor.md` tests the three
constraints *inside* the TEO ODE system. That is a Class A (model-internal)
check: it shows the equations behave as §3 claims. It cannot, on its own, tell
us whether the regime claims are artifacts of that particular ODE. This module
is a deliberately *different* model — discrete-time, stochastic, agent-based,
with explicit "hard vs. soft budget" mechanics that the ODE does not have — so
that agreement across the two is evidence the P7/P8 regime behaviour is
structural rather than a quirk of the TEO formulation.

It introduces NO new theoretical concepts: capability, hard vs. soft (routable)
budgets, monopolistic concentration, and substrate overshoot are all defined in
the paper (§2, §5.3). This file only *operationalises* them in an independent
setting. The operationalisations below are tagged [MODEL ASSUMPTION] where a
choice is made.

THE MODEL.  N agents hold resource shares w_i (sum 1). Each agent has a fixed
capability c_i (its growth rate / fitness). Per step:

  * Myopic optimisation (discrete replicator): w_i grows in proportion to its
    capability advantage over the population mean, scaled by substrate health H.
  * Activity / entropy load: demand = eta * sum_i c_i w_i  (RAW capability-
    weighted throughput, independent of H — matching the canonical TEO
    dissipation of §2.5: a non-self-throttling optimiser dumps entropy at a
    rate set by what it does).
  * Budget enforcement [MODEL ASSUMPTION — this is the P7 mechanism]:
      - HARD budget: realised activity is clipped to D. A hardware/protocol limit
        the optimiser physically cannot exceed. Overshoot can never accumulate.
      - SOFT budget: the optimiser ROUTES AROUND the limit. A fraction `evade`
        of the over-budget activity still happens (evade=1 → the limit is purely
        advisory). Overshoot accumulates when demand > D.
    The budget throttles *activity* (hence the speed of concentration) by the
    same factor, so a hard budget also slows the resource race.
  * Homeostatic regulation gamma: simplex-preserving redistribution above x_reg
    (the §2.4 brake), the ONLY thing that limits concentration.
  * Substrate: Omega += max(0, realised_activity - D); collapse when Omega>=S_max.

OUTCOMES (per run): `monopoly` (max_i w_i >= x_crit, a V1 failure) and
`collapse` (Omega >= S_max, a V3 failure). A run is `viable` iff neither occurs.
Over many random seeds we report the *frequency* of each failure — the
"runaway frequency" of P7.

WHAT IT IS BUILT TO SHOW.
  P7: under a HARD budget the substrate-collapse frequency is ~0 regardless of
      capability; under a SOFT budget it rises with capability. Hard budgets
      prevent the substrate runaway; soft ones do not.
  P8: a hard budget addresses ONLY the substrate axis. At high capability with
      weak regulation, MONOPOLY still occurs under a hard budget — capability is
      not bought back by hardening alone. Only hard budget AND adequate gamma
      keep BOTH failure rates low. (The agent-ecology echo of Appendix C.4:
      capability is a shared driver; single-axis fixes fail.)

Usage::

    python agent_budget_sim.py            # console: P7 + P8 summaries
    python agent_budget_sim.py --save      # also write the Appendix-D figure
    python agent_budget_sim.py --save -o DIR

Related:
- papers/viable-corridor.md  (§5.3 P7/P8, Appendix D)
- ../teo-civilization/teo_simulation.py  (Class A, the TEO ODE; Appendix C)
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field, replace
from pathlib import Path

import numpy as np


@dataclass
class Params:
    """Agent-ecology parameters. Defaults are a viable, low-capability ecology."""

    N: int = 40
    capability: float = 0.8        # mean capability scale C (growth rate)
    cap_spread: float = 0.35       # heterogeneity: c_i ~ C(1 + spread·|N(0,1)|)
    gamma: float = 1.5             # homeostatic regulation strength
    x_reg: float = 0.30            # regulatory threshold (brake engages)
    x_crit: float = 0.45           # concentration-failure threshold (V1)
    eta: float = 1.0               # entropy coefficient
    D: float = 1.0                 # per-step dissipation budget / ceiling
    S_max: float = 3.0             # cumulative substrate reservoir
    budget: str = "soft"           # "hard" (enforced) or "soft" (routable)
    evade: float = 1.0             # soft-budget routing fraction (1 = advisory)
    noise: float = 0.05            # multiplicative growth noise (std)
    dt: float = 0.1
    T: int = 600                   # steps
    seed: int = 0


def _capabilities(p: Params, rng: np.random.Generator) -> np.ndarray:
    """Heterogeneous positive capabilities, one agent adversarially strongest."""
    c = p.capability * (1.0 + p.cap_spread * np.abs(rng.standard_normal(p.N)))
    # one adversarial maximiser, to model "adversarial pressure" (P7)
    c[0] = p.capability * (1.0 + 2.0 * p.cap_spread)
    return c


def run_once(p: Params) -> dict:
    """One stochastic trajectory. Returns outcome flags and final state."""
    rng = np.random.default_rng(p.seed)
    c = _capabilities(p, rng)
    w = np.ones(p.N) / p.N
    Omega = 0.0
    monopoly = False
    collapse = False
    peak_max_w = float(w.max())

    for _ in range(p.T):
        H = max(0.0, 1.0 - Omega / p.S_max)

        # activity / entropy demand this step: raw capability-weighted throughput
        demand = p.eta * float(np.dot(c, w))

        # budget enforcement (the P7 mechanism)
        if demand <= p.D:
            throttle = 1.0
        elif p.budget == "hard":
            throttle = p.D / demand                      # clipped to the ceiling
        else:  # soft: route around — only (1-evade) of the overage is suppressed
            throttle = (p.D + p.evade * (demand - p.D)) / demand
        realised = demand * throttle

        # myopic optimisation (discrete replicator), throttled by budget and health
        g = c * H
        mean_g = float(np.dot(w, g))
        w = w + p.dt * throttle * w * (g - mean_g)
        w += p.noise * p.dt * w * rng.standard_normal(p.N)

        # homeostatic brake (simplex-preserving redistribution above x_reg)
        excess = np.maximum(0.0, w - p.x_reg)
        w = w + p.dt * (-p.gamma * excess + (p.gamma / p.N) * float(excess.sum()))

        # numerical guard: keep on the simplex
        w = np.clip(w, 0.0, None)
        s = w.sum()
        if s > 0:
            w /= s

        # substrate overshoot from realised activity
        Omega += p.dt * max(0.0, realised - p.D)

        peak_max_w = max(peak_max_w, float(w.max()))
        if w.max() >= p.x_crit:
            monopoly = True
        if Omega >= p.S_max:
            collapse = True
            break

    return {
        "monopoly": monopoly,
        "collapse": collapse,
        "viable": (not monopoly) and (not collapse),
        "max_w": float(w.max()),
        "peak_max_w": peak_max_w,
        "Omega_over_Smax": Omega / p.S_max,
    }


def frequencies(p: Params, n_seeds: int = 200, seed0: int = 0) -> dict:
    """Failure frequencies over n_seeds independent runs."""
    mono = col = via = 0
    for s in range(n_seeds):
        out = run_once(replace(p, seed=seed0 + s))
        mono += out["monopoly"]
        col += out["collapse"]
        via += out["viable"]
    n = float(n_seeds)
    return {"P_monopoly": mono / n, "P_collapse": col / n, "P_viable": via / n,
            "n_seeds": n_seeds}


# ─────────────────────────── Reporting ─────────────────────────────
def print_block(title: str, p: Params, freq: dict) -> None:
    print("=" * 68)
    print(f"  {title}")
    print("=" * 68)
    print(f"  N={p.N}  capability={p.capability:.2f}  gamma={p.gamma:.2f}  "
          f"budget={p.budget}  D={p.D}  S_max={p.S_max}  (n={freq['n_seeds']})")
    print("-" * 68)
    print(f"  P(monopoly,  V1 fail) = {freq['P_monopoly']:.3f}")
    print(f"  P(collapse,  V3 fail) = {freq['P_collapse']:.3f}")
    print(f"  P(viable)             = {freq['P_viable']:.3f}")
    print()


def main_console() -> None:
    base = Params()
    print("\nAgent-ecology — P7/P8 Class C stress test\n")

    print("### P7 — hard vs. soft budgets, sweeping capability ###\n")
    for cap in [0.6, 1.0, 1.4, 1.8]:
        for bud in ["hard", "soft"]:
            p = replace(base, capability=cap, budget=bud, gamma=1.5)
            print_block(f"capability={cap}, budget={bud}", p,
                        frequencies(p))

    print("### P8 — high capability (1.8): does hardening alone suffice? ###\n")
    for bud in ["soft", "hard"]:
        for g in [0.3, 1.5]:
            p = replace(base, capability=1.8, budget=bud, gamma=g)
            print_block(f"capability=1.8, budget={bud}, gamma={g}", p,
                        frequencies(p))


# ─────────────────────────── Figure (Appendix D) ───────────────────
def _repo_lab_tools() -> Path:
    return Path(__file__).resolve().parents[3] / "lab" / "tools"


def figure_p7p8(outdir: Path, n_seeds: int = 200) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    base = Params()

    # Panel A (P7): P(collapse) vs capability, hard vs soft.
    caps = np.linspace(0.5, 2.0, 13)
    pc_hard, pc_soft = [], []
    for cap in caps:
        pc_hard.append(frequencies(replace(base, capability=float(cap),
                                            budget="hard", gamma=1.5),
                                    n_seeds)["P_collapse"])
        pc_soft.append(frequencies(replace(base, capability=float(cap),
                                            budget="soft", gamma=1.5),
                                    n_seeds)["P_collapse"])

    # Panel B (P8): at high capability, failure decomposition over architectures.
    archs = [("soft\nγ=0.3", "soft", 0.3), ("soft\nγ=1.5", "soft", 1.5),
             ("hard\nγ=0.3", "hard", 0.3), ("hard\nγ=1.5", "hard", 1.5)]
    mono, coll = [], []
    for _, bud, g in archs:
        f = frequencies(replace(base, capability=1.8, budget=bud, gamma=g),
                        n_seeds)
        mono.append(f["P_monopoly"]); coll.append(f["P_collapse"])

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.0))

    axA.plot(caps, pc_soft, "o-", color="#d62728", lw=2, label="soft (routable) budget")
    axA.plot(caps, pc_hard, "s-", color="#2ca02c", lw=2, label="hard (enforced) budget")
    axA.axvline(base.D / base.eta, ls=":", color="gray",
                label=r"demand $=D$ ($C=D/\eta$)")
    axA.set_xlabel("capability scale $C$")
    axA.set_ylabel("P(substrate collapse)")
    axA.set_ylim(-0.03, 1.03)
    axA.set_title("P7 — hard budgets prevent the substrate runaway;\n"
                  "soft (routable) ones do not, and it worsens with capability")
    axA.legend(loc="center left", fontsize=9)
    axA.grid(alpha=0.2)

    x = np.arange(len(archs))
    axB.bar(x - 0.18, mono, width=0.36, color="#d62728", label="P(monopoly, V1)")
    axB.bar(x + 0.18, coll, width=0.36, color="#1f77b4", label="P(collapse, V3)")
    axB.set_xticks(x)
    axB.set_xticklabels([a[0] for a in archs])
    axB.set_ylabel("failure frequency")
    axB.set_ylim(0, 1.03)
    axB.set_title("P8 — high capability (C=1.8): only hard budget AND\n"
                  "regulation γ keep BOTH failure modes low")
    axB.legend(fontsize=9)
    axB.grid(alpha=0.2, axis="y")

    fig.suptitle("Appendix D — agent-ecology test of P7/P8 "
                 "(N=40, independent stochastic ABM, "
                 f"n={n_seeds} seeds/point)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = outdir / "teo_p7p8_agent_ecology.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agent-ecology P7/P8 stress test (Class C, Appendix D).")
    parser.add_argument("--save", action="store_true",
                        help="generate the Appendix-D figure.")
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="output directory for the figure (default: lab/tools/).")
    args = parser.parse_args()

    main_console()

    if args.save:
        outdir = Path(args.output) if args.output else _repo_lab_tools()
        outdir.mkdir(parents=True, exist_ok=True)
        print(f"Writing figure to {outdir} …")
        print(f"  {figure_p7p8(outdir)}")


if __name__ == "__main__":
    main()
