# Attractor Geometry of the TEO Phase Space

*Classifying the dynamical regimes of intelligent collectives through attractor topology.*

---

## Motivation

The TEO system couples replicator dynamics, Kuramoto synchronization, and a thermodynamic constraint into a single phase space. The long-term behavior of this coupled system is governed by its **attractors** — the states toward which trajectories converge. Understanding the attractor geometry tells us what kinds of stable configurations (civilizations, agent ecologies, organizations) the system can produce.

---

## The Three Attractor Types in TEO

### 1. Fixed Point Attractors — Stable Equilibria

When homeostasis ($\gamma > 0$), cultural coupling ($K > K_c$), and entropy budget ($dS/dt < D_{\max}$) are all satisfied, the TEO system converges to a **fixed point**:

- Resource shares $x_i$ stabilize around $x_i \approx 1/N$ (equitable distribution)
- Value orientations $\theta_i$ lock to a common phase $\psi$ (consensus)
- Entropy production settles below $D_{\max}$ (sustainability)

This is the **Chord equilibrium**: a stable, high-IP state where all governance constraints operate simultaneously. The basin of attraction volume measures how many initial conditions lead to this outcome — it shrinks as $\gamma$ decreases or $K$ drops below $K_c$.

### 2. Limit Cycle Attractors — Oscillatory Regimes

Near the Kuramoto critical coupling $K \approx K_c$, the system can enter **limit cycles**: periodic oscillations between partial synchronization and desynchronization. In civilizational terms, these correspond to recurring cycles of consensus and polarization.

The Kuramoto order parameter oscillates: $r(t) = r_0 + \epsilon \sin(\omega t)$. Resource allocation follows, as agents aligned with the momentary consensus gain fitness advantages that reverse when the phase shifts.

These cycles are structurally stable — perturbations shift the phase but not the cycle. They represent a society (or agent ecology) that neither fully polarizes nor fully synchronizes, but perpetually oscillates between the two.

### 3. Chaotic Attractors — Strange Attractors at the Edge

When the system operates near multiple simultaneous critical thresholds — $K \approx K_c$, $\gamma \approx 0$, and $dS/dt \approx D_{\max}$ — the TEO dynamics become **chaotic**: trajectories are bounded but aperiodic, with sensitive dependence on initial conditions.

The maximum Lyapunov exponent $\lambda_{\max}$ characterizes this regime:

$$\lambda_{\max} = \lim_{t \to \infty} \frac{1}{t} \ln \frac{|\delta \mathbf{z}(t)|}{|\delta \mathbf{z}(0)|}$$

where $\mathbf{z} = (x_1, \ldots, x_N, \theta_1, \ldots, \theta_N)$ is the full state vector.

- $\lambda_{\max} < 0$: fixed point (stable)
- $\lambda_{\max} = 0$: limit cycle (neutral stability)
- $\lambda_{\max} > 0$: chaos (exponential divergence of nearby trajectories)

This is the **Edge of Chaos** regime — and, per Claim 8 of the Emergence Manifesto, potentially where maximal information processing occurs.

---

## Basin of Attraction Structure

The TEO phase space is partitioned into basins of attraction. Each basin maps a set of initial conditions to a specific long-term behavior. The **basin boundary** is a fractal in chaotic regimes — meaning that arbitrarily small differences in initial conditions can lead to qualitatively different outcomes.

For the `teo-civilization` simulation, the key parameter axes are:

| Parameter | Low | High |
|:----------|:----|:-----|
| $\gamma$ (homeostasis) | Monopoly basin | Equity basin |
| $K$ (coupling) | Polarization basin | Consensus basin |
| $D_{\max}$ (entropy budget) | Collapse basin | Sustainability basin |

The intersection of all three "high" basins — equity, consensus, sustainability — is the **viable corridor**. The TEO simulation demonstrates that this corridor exists but is narrow.

---

## Connection to Identity Persistence

In the Chord equilibrium (fixed point attractor), all governance constraints co-exist simultaneously: the agent ecology maintains structural resilience ($\lambda_2 > 0$), thermodynamic sustainability ($dS/dt < D_{\max}$), and cognitive persistence ($\text{IP} \to 1$).

In the Arpeggio regime (limit cycle or chaotic attractor), identity components flicker in and out of the operative set, producing the time-multiplexed, unstable identity described in [lerchner-boundary.md](lerchner-boundary.md).

The attractor type thus determines whether a system *can* achieve the Chord state — it is a topological precondition, not merely a parameter choice.

---

## Related

- [Thermodynamics of Emergent Orchestration](../thermodynamics-of-orchestration.md) — the ODE system whose attractors are analyzed here
- [Lerchner Boundary](lerchner-boundary.md) — the IP score as diagnostic for attractor type
- [The Fractal Architecture of Emergence](../fractal-architecture-of-emergence.md) — why the same attractor types appear at every scale