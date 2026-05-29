# Thermodynamics of Emergent Orchestration (TEO) — Civilization Simulation

*Models civilizations and AI ecologies as coupled dynamical systems to test when societies synchronize, monopolize, polarize, or collapse.*

## What does this simulate?

`teo_simulation.py` integrates the coupled ODE system of the working paper
**"The Viable Corridor: A Three-Constraint Theorem for Survivable Multi-Agent
Optimization"** (`papers/viable-corridor.md`), **version 0.5**. It unifies four
control paradigms into one dynamical model:

| Paradigm | Equation | Paper eq. | Origin |
|----------|----------|-----------|--------|
| **Market** | Regulated replicator dynamics | (1), (1′) | Evolutionary game theory (Taylor–Jonker, 1978) |
| **Harmony** | Kuramoto synchronization | (2), (3) | Nonlinear physics (Kuramoto, 1975) |
| **Homeostasis** | Simplex-preserving redistribution brake | (4) | Control theory |
| **Substrate veto** | Cumulative entropy-overshoot budget | (5), (5′), (6a), (6b) | Thermodynamics (Landauer, 1961) |

This is the **faithful v0.5 model**. It differs from the earlier pre-v0.3 code
in three load-bearing ways, each matching a fix in the paper's revision history:

* the homeostatic brake (4) engages at a **regulatory** threshold
  `x_reg < x_crit` (not at the failure threshold) and is **simplex-preserving**
  via a uniform-redistribution term (the simplex `Σx=1` is conserved to ~1e-15);
* the substrate is a **cumulative** reservoir: only *integrated* overshoot
  `Ω(t)` of the instantaneous ceiling `D_max` reaching `S_max` collapses health
  `H` (Lemma 3) — a momentary spike does not. The old code applied an
  instantaneous, fully-recoverable throttle, which the paper explicitly rejects;
* substrate health `H` multiplies the replicator drift and the Kuramoto
  coupling (5′), so the *competitive dynamics* freeze as `H → 0` — **but** the
  dissipation (5) tracks **raw throughput** `f0`, not `H·f0` (v0.5 canonical
  model, §2.5): a non-self-throttling optimiser keeps producing entropy
  regardless of substrate health, so the veto binds endogenously.

## What it shows (Appendix C of the paper)

Running the script reproduces the necessity tests P1 and prints the viability
margins (V1 pluralism `max_i x_i < x_crit`; V2 coherence `r > r_min`;
V3b substrate `Ω/S_max < 1`) for four scenarios:

1. **In-corridor** — all three constraints hold; trajectory robustly viable.
2. **No regulation** (`γ = 0`) — the strictly-dominant agent's share → 1
   (monopolistic concentration, **Lemma 1**).
3. **Coherence collapse** (`K < K_c`, from a *coherent* initial condition) —
   the order parameter dephases to `r ≈ 0.31 < r_min` (**Lemma 2**).
4. **Substrate veto** (`D_max` low, `η` high) — raw throughput exceeds the
   ceiling, accumulated overshoot crosses `S_max` (`Ω/S_max ≈ 27`), `H → 0`
   and the competitive dynamics freeze (**Lemma 3**, binding endogenously).

### The two substrate regimes (`entropy_couples_to_H`)

The fourth scenario plus a contrast run illustrate the substrate-veto modeling
decision resolved in v0.5 (paper §2.5, §6.1):

* **canonical** (`entropy_couples_to_H=False`, the default): `dS/dt ∝ f0`,
  entropy tracks raw activity. When mean throughput exceeds `D_max`, overshoot
  grows without bound, `Ω` crosses `S_max`, and the veto binds (`Ω/S_max ≈ 27`,
  `H → 0`). This is the non-self-throttling optimiser of §4.3.
* **self-regulating** (`entropy_couples_to_H=True`): `dS/dt ∝ H·f0`, so
  production throttles with health and `Ω` self-limits to
  `(1 − D_max/(η·φ̄0))·S_max < S_max` (`Ω/S_max ≈ 0.86`, `H` plateaus at `≈ 0.14`).
  The veto never binds — the correct model of a system that *does* back off at
  the substrate limit.

`run_substrate_contrast()` runs both; the module docstring documents the
decision and its rationale in full.

## Running

```bash
python teo_simulation.py            # console: the four P1 scenarios + substrate contrast
python teo_simulation.py --save     # also write the Appendix-C figures (P1, P2, P3, P8)
python teo_simulation.py --save -o DIR   # write figures into DIR (default: lab/tools/)
```

Figures written by `--save` (consumed by Appendix C of the paper):
`teo_p1_necessity.png` (Lemmas 1–3), `teo_p2_gamma_c.png` (critical brake
strength `γ_c ≈ 0.49`, matching the closed-form estimate of §3.4),
`teo_p3_corridor.png` (the viable region is a *lower corner* in `(γ, K)`), and
`teo_p8_capability.png` (capability `δ` loads onto two constraints at once;
single-axis rescue of a high-capability system fails — the central P8 result).

Requires `numpy`, `scipy`, `matplotlib` (see the repo `requirements.txt`).

## Related Theory

- [The Viable Corridor](../../../papers/viable-corridor.md) — the working paper this script implements (§2 equations, §3 Theorem 1, §5 predictions P1–P3, Appendix C)
- [Thermodynamics of Emergent Orchestration](../../../theory/core/thermodynamics-of-orchestration.md) — Full mathematical derivation
- [Limitations & Honest Assessment](../../../theory/reference/limitations-and-honest-assessment.md) — Critical self-evaluation
