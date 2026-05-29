# TEO Framework — Thermodynamics of Emergent Orchestration

The **TEO framework** is the mathematical core of this repository's theoretical architecture. It translates the qualitative principles — self-organization, homeostasis, criticality, identity — into a single coupled system of ordinary differential equations (ODEs) that can be simulated, calibrated, and falsified.

> **Formalized in the paper.** The constraint conjunction developed here is given a citation-ready treatment — necessity theorem, sufficiency conjecture, and the capability-loading result — in [*The Viable Corridor*](../../papers/viable-corridor.md), which carries the current refined formalism (substrate-coupled value dynamics, cumulative overshoot). For where this node sits in the wider project, see [Canonical Path v2](../../meta/repository-meta/canonical-path-v2.md).

---

## Sub-Documents

Each document below derives a specific aspect of the framework from the governing TEO equations defined in [`thermodynamics-of-orchestration.md`](../core/thermodynamics-of-orchestration.md):

| Document | Focus |
|:---------|:------|
| [**Lerchner Boundary**](lerchner-boundary.md) | The formal definition of **Identity Persistence (IP)** — the metric that distinguishes *simulating* a self (Arpeggio) from *instantiating* a self (Chord). Derives the IP score from TEO state variables and proposes a testable phase transition. |
| [**Attractor Geometry**](antikythera-topology.md) | Classification of TEO's dynamical regimes — fixed point (Chord equilibrium), limit cycle (oscillatory consensus), and chaotic (Edge of Chaos) — through Lyapunov exponent analysis and basin-of-attraction structure. |
| [**Dupoux Integration**](dupoux-integration.md) | Maps developmental learning theory (Dupoux) onto TEO: System A (unconstrained competition), System B (top-down regulation), System M (the full coupled system). Shows why constraints are prerequisites for learning, not obstacles. |
| [**Love as Constraint**](love-as-constraint.md) | Formalizes "care" as three mathematical boundaries: structural resilience ($\lambda_2$), thermodynamic ceiling ($D_{\max}$), and identity persistence (IP). Their conjunction defines the **viable corridor**. |
| [**Why the Paperclip Maximizer Fails**](why-paperclip-maximizer-fails.md) | Step-by-step derivation of the trajectory from unconstrained optimization ($\gamma = 0$, $K = 0$) through monopoly to substrate collapse. Shows why intelligence alone cannot escape the entropy budget. |
| [**Thermodynamic Tokenomics**](thermodynamic-tokenomics.md) | Applies the TEO entropy budget ($D_{\max}$) to political economy: compute as the base currency, Ecological Dissipation Rights (EDR) as the unit, Proof-of-Dissipation as the protocol. The framework's application to economic substrate-coupling. |

---

## The Governing Equations

The full TEO system is:

$$\frac{dx_i}{dt} = x_i \left( f_i(\mathbf{x}) - \bar{\phi}(\mathbf{x}) \right) + \mathcal{H}_i(\mathbf{x})$$

$$\frac{d\theta_i}{dt} = \omega_i + \frac{K}{N} \sum_{j=1}^{N} A_{ij} \sin(\theta_j - \theta_i)$$

subject to:

$$\sum_{i=1}^{N} \eta_i\, x_i\, f_i(\mathbf{x}) \leq D_{\max}$$

See [Thermodynamics of Emergent Orchestration](../core/thermodynamics-of-orchestration.md) for the complete derivation, parameter definitions, and simulation results.