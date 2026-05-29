"""
teo_simulation.py

Thermodynamics of Emergent Orchestration (TEO) — Numerical Simulation (v0.5 model)

Solves the coupled ODE system of the paper
"The Viable Corridor: A Three-Constraint Theorem for Survivable Multi-Agent
Optimization" (papers/viable-corridor.md), version 0.3:

  (1)  dx_i/dt = H * x_i (f0_i - phi0)  +  H_i(x)        replicator + brake
  (1') strict dominance: f0_{i*} - f0_j >= delta > 0
  (2)  dtheta_i/dt = H [ omega_i + (K/N) sum_j A_ij sin(theta_j - theta_i) ]
  (3)  r e^{i psi} = (1/N) sum_j e^{i theta_j}            order parameter
  (4)  H_i(x) = -gamma (x_i - x_reg)_+ + (gamma/N) sum_j (x_j - x_reg)_+
  (5)  dS/dt = sum_i eta_i x_i f0_i(x)                    dissipation proxy
  (5') f_i(x,H) = H * f0_i(x)                              effective fitness (dynamics only)
  (6a) Omega(t) = int_0^t (dS/dt - D_max)_+ ds            accumulated overshoot
  (6b) H(t) = max(0, 1 - Omega(t)/S_max)                  substrate health

The H-coupling (5') applies to the *competitive dynamics* — the replicator
drift (1) and the Kuramoto coupling (2) carry the prefactor H, so they freeze
as H -> 0. The *dissipation* (5) tracks RAW throughput f0, NOT H*f0: a
non-self-throttling optimiser keeps producing entropy at a rate set by its
activity, regardless of how degraded the substrate sink is. This asymmetry is
what makes the substrate veto (Lemma 3) bind endogenously (see below).

This is the FAITHFUL v0.3/v0.5 model. It differs from the pre-v0.3 code in
three load-bearing ways, each matching a fix in the paper's revision history:

  * the homeostatic brake (4) activates at a *regulatory* threshold
    x_reg < x_crit (not at the failure threshold), AND it is
    simplex-preserving via the uniform-redistribution second term;
  * the substrate is a *cumulative* reservoir: a momentary overshoot of the
    instantaneous ceiling D_max only increments Omega; only integrated
    overshoot reaching S_max collapses H (Lemma 3). The old code applied an
    instantaneous, fully-recoverable throttle, which is the model the paper
    explicitly rejects;
  * substrate health H multiplies the replicator drift and the Kuramoto
    coupling (5'), so the *competitive dynamics* freeze as H -> 0 — but the
    *dissipation* (5) tracks raw throughput f0, not H*f0 (see next note).

A note on faithfulness of the brake term. Equation (1) as written adds the
brake H_i(x) WITHOUT an H prefactor, so at H = 0 the replicator drift vanishes
but the brake does not. We implement (1) exactly as written and document the
nuance with the `brake_couples_to_H` flag (default False = faithful to the
printed equation).

A note on entropy coupling (the `entropy_couples_to_H` flag). This flag carries
the substrate-veto modelling decision resolved in v0.5 of the paper (§2.5,
§6.1):

  * `entropy_couples_to_H=False` (DEFAULT, canonical): dS/dt = sum eta_i x_i
    f0_i — entropy production tracks RAW activity, independent of substrate
    health. A non-self-throttling optimiser (the paperclip case, §4.3) keeps
    dumping entropy regardless of how degraded the sink is, so when mean
    throughput exceeds D_max the overshoot Omega grows without bound, reaches
    S_max in finite time, and the veto of Lemma 3 binds ENDOGENOUSLY.
  * `entropy_couples_to_H=True`: dS/dt = H * sum eta_i x_i f0_i — production
    is itself throttled by substrate health. Then as H falls dS/dt falls too,
    Omega self-limits to (1 - D_max/(eta*phi0_bar))*S_max < S_max, and the veto
    is NEVER reached. This is the correct model of a *substrate-self-regulating*
    (i.e. substrate-aligned) system, for which "no veto needed" is the right
    answer — but it is the wrong model for an optimiser that does not back off.

The flag exists so both regimes can be compared directly (see
`run_substrate_contrast`). The decision and its rationale are documented in the
paper's §2.5 and §6.1; the deeper realism question (delays, an endogenously
shrinking D_max(t)) is flagged there as future work (§6.4).

Usage::

    python teo_simulation.py                 # console: four P1 scenarios
    python teo_simulation.py --save           # also write Appendix-C figures
    python teo_simulation.py --save -o DIR    # figures into DIR

Related:
- papers/viable-corridor.md  (§2 equations, §3 Theorem 1, §5 predictions P1-P3)
- lab/tools/viable_corridor.py  (Figure 1, the schematic corridor)
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field, replace
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


# ─────────────────────────── Parameters ────────────────────────────
@dataclass
class Params:
    """TEO v0.5 parameters. Defaults define an in-corridor (viable) system."""

    N: int = 50
    K: float = 3.0                 # value coupling (Kuramoto)
    gamma: float = 1.5             # homeostatic strength
    delta: float = 0.30            # strict-dominance margin (1'); agent 0 dominates
    x_reg: float = 0.30            # regulatory threshold (brake activates)
    x_crit: float = 0.45           # failure threshold (V1)
    r_min: float = 0.50            # coherence floor (V2)
    eta: float = 1.0               # entropy coefficient (uniform)
    D_max: float = 1.5             # instantaneous dissipation ceiling
    S_max: float = 5.0             # cumulative substrate reservoir
    sigma: float = 1.0             # std of the Gaussian natural-frequency density
    T_end: float = 80.0
    steps: int = 801
    seed: int = 7
    brake_couples_to_H: bool = False     # faithful to printed Eq (1)
    entropy_couples_to_H: bool = False   # canonical (v0.5): Ṡ ∝ raw f0

    base_fitness: np.ndarray = field(default=None, repr=False)
    omega: np.ndarray = field(default=None, repr=False)

    def __post_init__(self):
        # Always derive the arrays from the scalar params, so that
        # dataclasses.replace(p, delta=…) / (…, N=…) / (…, seed=…)
        # regenerates them correctly. (A stored array would otherwise be
        # copied *stale* across replace(): e.g. replace(p, delta=2.0) would
        # silently keep the old fitness vector and the capability sweep would
        # be a no-op.)
        rng = np.random.default_rng(self.seed)
        # Strict dominance (1'): agent 0 exceeds every other by exactly delta.
        f0 = np.ones(self.N)
        f0[0] = 1.0 + self.delta
        self.base_fitness = f0
        # Symmetric unimodal density (Gaussian) with g(0) = 1/(sigma*sqrt(2pi)).
        self.omega = rng.normal(0.0, self.sigma, self.N)


def kc_gaussian(sigma: float) -> float:
    """Kuramoto critical coupling for a Gaussian frequency density.

    K_c = 2 / (pi g(0)), with g(0) = 1/(sigma*sqrt(2 pi)) for N(0, sigma^2),
    so K_c = 2 sigma sqrt(2/pi).
    """
    return 2.0 * sigma * np.sqrt(2.0 / np.pi)


# ─────────────────────────── Dynamics ──────────────────────────────
def order_parameter(theta: np.ndarray) -> tuple[float, float]:
    """Kuramoto order parameter (3): returns (r, psi)."""
    z = np.mean(np.exp(1j * theta))
    return float(np.abs(z)), float(np.angle(z))


def make_rhs(p: Params):
    """Vectorised right-hand side of the coupled TEO system.

    State layout: [ x_0..x_{N-1},  theta_0..theta_{N-1},  Omega ].
    """
    N, K, gamma = p.N, p.K, p.gamma
    x_reg, eta, D_max, S_max = p.x_reg, p.eta, p.D_max, p.S_max
    f0 = p.base_fitness
    omega = p.omega
    brake_H = p.brake_couples_to_H
    entropy_H = p.entropy_couples_to_H

    def rhs(t, state):
        x = state[:N]
        theta = state[N:2 * N]
        Omega = state[2 * N]

        H = max(0.0, 1.0 - Omega / S_max)

        # Replicator drift (carries H via (5')): H * x_i (f0_i - phi0).
        phi0 = float(np.dot(x, f0))
        drift = H * x * (f0 - phi0)

        # Homeostatic brake (4): simplex-preserving uniform redistribution.
        excess = np.maximum(0.0, x - x_reg)
        brake = -gamma * excess + (gamma / N) * float(np.sum(excess))
        if brake_H:
            brake = H * brake
        dx = drift + brake

        # Kuramoto (2), all-to-all via the order parameter:
        # (K/N) sum_j sin(theta_j - theta_i) = K r sin(psi - theta_i).
        r, psi = order_parameter(theta)
        dtheta = H * (omega + K * r * np.sin(psi - theta))

        # Entropy production (5) and accumulated overshoot (6a). Canonical
        # model: Ṡ tracks RAW throughput f0 (a non-self-throttling optimiser
        # dumps entropy at a rate set by its activity, not by substrate
        # health). The H-coupled variant (entropy_H=True) is the
        # substrate-self-regulating regime; see the module docstring.
        activity = float(np.dot(eta * x, f0))      # sum_i eta x_i f0_i
        S_dot = (H * activity) if entropy_H else activity
        dOmega = max(0.0, S_dot - D_max)

        out = np.empty(2 * N + 1)
        out[:N] = dx
        out[N:2 * N] = dtheta
        out[2 * N] = dOmega
        return out

    return rhs


@dataclass
class Result:
    label: str
    p: Params
    t: np.ndarray
    x: np.ndarray            # (N, T)
    theta: np.ndarray        # (N, T)
    Omega: np.ndarray        # (T,)
    H: np.ndarray            # (T,)
    r: np.ndarray            # (T,)
    S_dot: np.ndarray        # (T,)
    max_x: np.ndarray        # (T,)
    simplex_err: float       # max |sum_i x_i - 1| over trajectory


def run(p: Params, label: str = "", coherent_ic: bool = True) -> Result:
    """Integrate the TEO system from a representative initial condition."""
    rng = np.random.default_rng(p.seed + 1)
    N = p.N

    # Resource shares: start uniform on the simplex.
    x0 = np.ones(N) / N
    # Value orientations: coherent initial condition (V requires r >= r_min),
    # so we start clustered (r(0) ~ 0.95), per the v0.3 Lemma 2 reframe.
    if coherent_ic:
        theta0 = rng.normal(0.0, 0.30, N)
    else:
        theta0 = rng.uniform(0.0, 2 * np.pi, N)
    state0 = np.concatenate([x0, theta0, [0.0]])

    t_eval = np.linspace(0.0, p.T_end, p.steps)
    sol = solve_ivp(
        make_rhs(p), (0.0, p.T_end), state0, t_eval=t_eval,
        method="RK45", rtol=1e-7, atol=1e-9, max_step=0.1,
    )

    x = sol.y[:N, :]
    theta = sol.y[N:2 * N, :]
    Omega = sol.y[2 * N, :]
    H = np.maximum(0.0, 1.0 - Omega / p.S_max)

    r = np.array([order_parameter(theta[:, k])[0] for k in range(sol.t.size)])
    activity = (p.eta * x * p.base_fitness[:, None]).sum(axis=0)
    S_dot = (H * activity) if p.entropy_couples_to_H else activity
    max_x = x.max(axis=0)
    simplex_err = float(np.max(np.abs(x.sum(axis=0) - 1.0)))

    return Result(label or "run", p, sol.t, x, theta, Omega, H, r, S_dot,
                  max_x, simplex_err)


# ─────────────────────────── Reporting ─────────────────────────────
def viability_report(res: Result) -> dict:
    """Evaluate the three viability conditions over the trajectory."""
    p = res.p
    v1 = bool(np.all(res.max_x <= p.x_crit))           # pluralism
    v2 = bool(np.all(res.r >= p.r_min))                # coherence
    v3b = bool(np.all(res.Omega < p.S_max))            # cumulative substrate
    return {
        "V1_pluralism": v1,
        "V2_coherence": v2,
        "V3b_substrate": v3b,
        "viable": v1 and v2 and v3b,
        "max_x_final": float(res.max_x[-1]),
        "r_final": float(res.r[-1]),
        "H_final": float(res.H[-1]),
        "Omega_final": float(res.Omega[-1]),
        "Omega_over_Smax": float(res.Omega[-1] / p.S_max),
    }


def print_summary(res: Result) -> None:
    p = res.p
    rep = viability_report(res)
    kc = kc_gaussian(p.sigma)
    print("=" * 66)
    print(f"  {res.label}")
    print("=" * 66)
    print(f"  N={p.N}  K={p.K:.3f} (K_c≈{kc:.3f})  gamma={p.gamma:.3f}  "
          f"delta={p.delta:.2f}")
    print(f"  x_reg={p.x_reg}  x_crit={p.x_crit}  r_min={p.r_min}  "
          f"D_max={p.D_max}  S_max={p.S_max}")
    print(f"  entropy_couples_to_H={p.entropy_couples_to_H}  "
          f"brake_couples_to_H={p.brake_couples_to_H}")
    print("-" * 66)
    ok = lambda b: "✓" if b else "✗"
    print(f"  V1 pluralism   max_i x_i = {rep['max_x_final']:.3f} "
          f"(crit {p.x_crit})   {ok(rep['V1_pluralism'])}")
    print(f"  V2 coherence   r         = {rep['r_final']:.3f} "
          f"(min  {p.r_min})   {ok(rep['V2_coherence'])}")
    print(f"  V3b substrate  Omega/Smax= {rep['Omega_over_Smax']:.3f} "
          f"(H_final {rep['H_final']:.3f})   {ok(rep['V3b_substrate'])}")
    print(f"  → robustly viable trajectory: {ok(rep['viable'])}")
    print(f"  (simplex drift max|Σx-1| = {res.simplex_err:.2e})")
    print()


# ─────────────────────────── Scenarios (P1) ────────────────────────
def p1_scenarios() -> list[tuple[str, Params, bool]]:
    """The four P1 necessity-verification scenarios (each negates one V)."""
    base = Params()
    return [
        ("SCENARIO 1 — In-corridor (γ>γ_c, K>K_c, substrate safe)",
         base, True),
        ("SCENARIO 2 — γ = 0 (Lemma 1: monopolistic concentration)",
         replace(base, gamma=0.0), True),
        ("SCENARIO 3 — K < K_c, coherent IC (Lemma 2: coherence collapse)",
         replace(base, K=0.8), True),
        ("SCENARIO 4 — substrate veto (Lemma 3): D_max low, η high → H→0",
         replace(base, D_max=0.3, eta=2.0), True),
    ]


def run_substrate_contrast() -> tuple[Result, Result]:
    """Lemma 3 under the two substrate regimes (returns canonical, self-regulating).

    canonical       — Ṡ ∝ raw f0 (entropy_couples_to_H=False): the veto binds,
                      Omega grows past S_max, H -> 0 (the non-self-throttling
                      optimiser of §4.3).
    self_regulating — Ṡ ∝ H·f0 (entropy_couples_to_H=True): production throttles
                      with health, Omega self-limits below S_max, H plateaus > 0.
    """
    sp = replace(Params(), D_max=0.3, eta=2.0)
    canonical = run(replace(sp, entropy_couples_to_H=False),
                    "substrate, canonical (Ṡ ∝ f0): veto binds")
    self_regulating = run(replace(sp, entropy_couples_to_H=True),
                          "substrate, self-regulating (Ṡ ∝ H f0): self-limits")
    return canonical, self_regulating


# ─────────────────────────── Figures (Appendix C) ──────────────────
def _repo_lab_tools() -> Path:
    # …/simulation-models/alignment-and-veto/teo-civilization/teo_simulation.py
    return Path(__file__).resolve().parents[3] / "lab" / "tools"


def figure_p1(outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    scenarios = p1_scenarios()
    results = [run(p, lbl, ic) for (lbl, p, ic) in scenarios]
    canonical, self_regulating = run_substrate_contrast()

    fig, axes = plt.subplots(2, 2, figsize=(12, 8.5))
    titles = [
        "(a) In-corridor: all three constraints hold",
        "(b) γ = 0 → monopolistic concentration (Lemma 1)",
        "(c) K < K_c, coherent IC → coherence collapse (Lemma 2)",
        "(d) Substrate veto: H→0 (canonical); self-limits if Ṡ∝H",
    ]
    for ax, res, title in zip(axes.flat, results, titles):
        p = res.p
        ax.plot(res.t, res.max_x, color="#d62728", lw=2, label=r"$\max_i x_i$")
        ax.plot(res.t, res.r, color="#ff7f0e", lw=2, label=r"$r$")
        ax.plot(res.t, res.H, color="#9467bd", lw=2, label=r"$H$")
        ax.axhline(p.x_crit, ls="--", color="#d62728", alpha=0.5, lw=1)
        ax.axhline(p.r_min, ls="--", color="#ff7f0e", alpha=0.5, lw=1)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("t")
        ax.set_ylim(-0.03, 1.03)
        ax.grid(alpha=0.2)

    # Panel (d): the solid H is the canonical run (veto binds); overlay the
    # self-regulating run (Ṡ∝H·f0) to show it self-limits instead.
    ax = axes.flat[3]
    ax.plot(self_regulating.t, self_regulating.H, color="#9467bd", lw=2, ls=":",
            label=r"$H$ (Ṡ∝$Hf_0$, self-reg.)")
    ax.legend(loc="center right", fontsize=8)
    axes.flat[0].legend(loc="center right", fontsize=8)

    fig.suptitle("Appendix C / P1 — necessity verification of Lemmas 1–3 "
                 "(N=50, Gaussian frequencies)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    out = outdir / "teo_p1_necessity.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_p2_gamma_sweep(outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    base = Params()
    gammas = np.linspace(0.0, 1.5, 31)
    final_max_x = []
    for g in gammas:
        res = run(replace(base, gamma=float(g)), f"γ={g:.2f}")
        final_max_x.append(res.max_x[-1])
    final_max_x = np.array(final_max_x)

    # Predicted γ_c ≈ x_crit (1 - x_crit) δ / (x_crit - x_reg).
    gc = base.x_crit * (1 - base.x_crit) * base.delta / (base.x_crit - base.x_reg)

    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.plot(gammas, final_max_x, "o-", color="#1f77b4", lw=2, ms=4)
    ax.axhline(base.x_crit, ls="--", color="#d62728", alpha=0.7,
               label=fr"$x_{{\rm crit}}={base.x_crit}$")
    ax.axvline(gc, ls="--", color="#2ca02c", alpha=0.8,
               label=fr"predicted $\gamma_c\approx{gc:.2f}$")
    ax.set_xlabel(r"homeostatic strength $\gamma$")
    ax.set_ylabel(r"final $\max_i x_i$")
    ax.set_title("P2 — γ_c existence: final concentration vs brake strength")
    ax.legend()
    ax.grid(alpha=0.2)
    fig.tight_layout()
    out = outdir / "teo_p2_gamma_c.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_p3_corridor(outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    base = Params()
    gammas = np.linspace(0.0, 1.5, 16)
    Ks = np.linspace(0.0, 4.0, 16)
    grid = np.zeros((Ks.size, gammas.size))
    for i, K in enumerate(Ks):
        for j, g in enumerate(gammas):
            res = run(replace(base, gamma=float(g), K=float(K)))
            rep = viability_report(res)
            grid[i, j] = 1.0 if (rep["V1_pluralism"] and rep["V2_coherence"]) else 0.0

    kc = kc_gaussian(base.sigma)
    gc = base.x_crit * (1 - base.x_crit) * base.delta / (base.x_crit - base.x_reg)

    fig, ax = plt.subplots(figsize=(7.5, 6))
    ax.imshow(grid, origin="lower", aspect="auto", cmap="Greens",
              extent=[gammas[0], gammas[-1], Ks[0], Ks[-1]], vmin=0, vmax=1.3)
    ax.axhline(kc, ls="--", color="#ff7f0e", lw=2, label=fr"$K_c\approx{kc:.2f}$")
    ax.axvline(gc, ls="--", color="#1f77b4", lw=2, label=fr"$\gamma_c\approx{gc:.2f}$")
    ax.set_xlabel(r"homeostatic strength $\gamma$")
    ax.set_ylabel(r"value coupling $K$")
    ax.set_title("P3 — in-corridor region (V1∧V2) is a lower corner in (γ, K)\n"
                 "bounded below, unbounded above — not a finite-measure box")
    ax.legend(loc="lower right")
    fig.tight_layout()
    out = outdir / "teo_p3_corridor.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_p8_capability(outdir: Path) -> Path:
    """P8 — capability δ is a shared driver that loads onto two constraints.

    Left: sweeping δ at a substrate-unconstrained D_max isolates the
    concentration-equilibrium max_x(δ) (crosses x_crit) while the substrate
    *demand* rate(δ)=η·φ̄₀ (the load on the substrate) crosses a fixed
    operating D_max — one capability axis, two boundary crossings.
    Right: at high capability (δ=2.0) the viable set in the (γ, D_max) plane
    is a corner requiring BOTH strong regulation and substrate headroom;
    single-axis rescue (more γ only, or more D_max only) fails.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    base = Params()
    D_op = 1.5            # operating substrate ceiling (the reference line)
    D_safe = 8.0          # substrate-unconstrained, to isolate concentration

    # Left panel: capability sweep (substrate-unconstrained → clean max_x(δ)).
    deltas = np.linspace(0.05, 3.0, 30)
    max_x, demand = [], []
    for d in deltas:
        res = run(replace(base, delta=float(d), D_max=D_safe))
        max_x.append(res.max_x[-1])
        demand.append(base.eta * float(np.dot(res.x[:, -1], res.p.base_fitness)))
    max_x = np.array(max_x); demand = np.array(demand)

    # Right panel: (γ, D_max) viability at high capability δ=2.0.
    d_hi = 2.0
    gammas = np.linspace(0.0, 8.0, 22)
    Dmaxs = np.linspace(1.0, 3.5, 22)
    grid = np.zeros((Dmaxs.size, gammas.size))
    for i, D in enumerate(Dmaxs):
        for j, g in enumerate(gammas):
            rep = viability_report(run(replace(base, delta=d_hi, gamma=float(g),
                                                D_max=float(D))))
            grid[i, j] = 1.0 if rep["viable"] else 0.0

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.2))

    axL.plot(deltas, max_x, color="#d62728", lw=2, label=r"final $\max_i x_i$")
    axL.axhline(base.x_crit, ls="--", color="#d62728", alpha=0.6,
                label=fr"$x_{{\rm crit}}={base.x_crit}$")
    axL.set_xlabel(r"capability (dominance margin) $\delta$")
    axL.set_ylabel(r"$\max_i x_i$", color="#d62728")
    axL.tick_params(axis="y", labelcolor="#d62728")
    axL.set_ylim(0, 1.0)
    axT = axL.twinx()
    axT.plot(deltas, demand, color="#1f77b4", lw=2, label=r"substrate demand $\eta\bar\phi_0$")
    axT.axhline(D_op, ls=":", color="#1f77b4", alpha=0.7,
                label=fr"operating $D_{{\max}}={D_op}$")
    axT.set_ylabel(r"substrate demand $\eta\bar\phi_0$", color="#1f77b4")
    axT.tick_params(axis="y", labelcolor="#1f77b4")
    axL.set_title("Capability δ loads onto BOTH constraints\n"
                  "(V1 concentration, then V3 substrate demand)")
    h1, l1 = axL.get_legend_handles_labels()
    h2, l2 = axT.get_legend_handles_labels()
    axL.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8)
    axL.grid(alpha=0.2)

    axR.imshow(grid, origin="lower", aspect="auto", cmap="Greens",
               extent=[gammas[0], gammas[-1], Dmaxs[0], Dmaxs[-1]], vmin=0, vmax=1.3)
    # single-axis vs joint rescue markers (δ=2.0)
    axR.scatter([1.5], [1.5], marker="x", s=90, color="k", zorder=5)
    axR.scatter([6.0], [1.5], marker="x", s=90, color="k", zorder=5)
    axR.scatter([1.5], [3.0], marker="x", s=90, color="k", zorder=5)
    axR.scatter([6.0], [3.0], marker="o", s=90, facecolors="none",
                edgecolors="k", lw=2, zorder=5)
    axR.annotate("baseline ✗", (1.5, 1.5), textcoords="offset points",
                 xytext=(6, 6), fontsize=8)
    axR.annotate("+γ only ✗", (6.0, 1.5), textcoords="offset points",
                 xytext=(-10, 6), fontsize=8, ha="right")
    axR.annotate("+D only ✗", (1.5, 3.0), textcoords="offset points",
                 xytext=(6, -12), fontsize=8)
    axR.annotate("both ✓", (6.0, 3.0), textcoords="offset points",
                 xytext=(-8, 6), fontsize=8, ha="right")
    axR.set_xlabel(r"homeostatic strength $\gamma$")
    axR.set_ylabel(r"substrate ceiling $D_{\max}$")
    axR.set_title(f"Rescuing high capability (δ={d_hi}): viable only if\n"
                  "BOTH γ and D_max are raised — single-axis fixes fail")

    fig.suptitle("P8 — constraint architecture dominates capability "
                 "(N=50, K=3.0>K_c)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = outdir / "teo_p8_capability.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


# ─────────────────────────── CLI ───────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="TEO v0.5 simulation — P1 scenarios and Appendix-C figures.")
    parser.add_argument("--save", action="store_true",
                        help="generate Appendix-C figures (P1, P2, P3, P8).")
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="output directory for figures (default: lab/tools/).")
    args = parser.parse_args()

    print("\nTEO v0.5 — P1 necessity-verification scenarios\n")
    for label, p, ic in p1_scenarios():
        print_summary(run(p, label, ic))

    print("Lemma 3 — substrate veto under the two dissipation regimes:\n")
    canonical, self_regulating = run_substrate_contrast()
    print_summary(canonical)
    print_summary(self_regulating)

    if args.save:
        outdir = Path(args.output) if args.output else _repo_lab_tools()
        outdir.mkdir(parents=True, exist_ok=True)
        print(f"Writing figures to {outdir} …")
        print(f"  {figure_p1(outdir)}")
        print(f"  {figure_p2_gamma_sweep(outdir)}")
        print(f"  {figure_p3_corridor(outdir)}")
        print(f"  {figure_p8_capability(outdir)}")


if __name__ == "__main__":
    main()
