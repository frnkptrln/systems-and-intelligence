# TEO Framework — Thermodynamics of Emergent Orchestration

The **TEO framework** is one executable model in the repository's viability branch. It
combines selected resource, synchronization, regulation, and substrate variables in a
coupled system of ordinary differential equations. Those choices are additions to the
[reconstructed foundation](../core/mathematical-axioms.md), not consequences of it.

> **Formalized in the paper.** The constraint conjunction developed here is given a citation-ready treatment — necessity theorem, sufficiency conjecture, and the capability-loading result — in [*The Viable Corridor*](../../papers/viable-corridor.md), which carries the current refined formalism (substrate-coupled value dynamics, cumulative overshoot). For where this node sits in the wider project, see [Canonical Path v2](../../meta/repository-meta/canonical-path-v2.md).

---

## Sub-Documents

Each document below develops or interprets a specific aspect of the framework defined in
[`thermodynamics-of-orchestration.md`](../core/thermodynamics-of-orchestration.md):

| Document | Focus |
|:---------|:------|
| [**Lerchner Boundary**](lerchner-boundary.md) | An earlier formalization of **Identity Persistence (IP)** and a proposed Chord/Arpeggio distinction. IP is a selected instrument, not a criterion for a “real” self. |
| [**Attractor Geometry**](antikythera-topology.md) | Classification of TEO's dynamical regimes — fixed point (Chord equilibrium), limit cycle (oscillatory consensus), and chaotic (Edge of Chaos) — through Lyapunov exponent analysis and basin-of-attraction structure. |
| [**Dupoux Integration**](dupoux-integration.md) | An exploratory mapping of developmental-learning ideas onto TEO's selected variables. |
| [**Love as Constraint**](love-as-constraint.md) | A normative name for one proposed bundle of viability constraints, with corrected scope for connectivity, substrate budgets, and IP. |
| [**A Paperclip Maximizer in TEO**](why-paperclip-maximizer-fails.md) | A conditional concentration-and-overshoot trajectory under declared dynamics and controller assumptions. |
| [**Thermodynamic Tokenomics**](thermodynamic-tokenomics.md) | Applies the TEO entropy budget ($D_{\max}$) to political economy: compute as the base currency, Ecological Dissipation Rights (EDR) as the unit, Proof-of-Dissipation as the protocol. The framework's application to economic substrate-coupling. |

---

## The Governing Equations

The full TEO system (v0.8 form — value dynamics gated by substrate health $H$; cumulative substrate budget) is:

$$\frac{dx_i}{dt} = H\,x_i \left( f_i^{(0)}(\mathbf{x}) - \bar{\phi}^{(0)}(\mathbf{x}) \right) + \mathcal{H}_i(\mathbf{x})$$

$$\frac{d\theta_i}{dt} = H\left[\omega_i + \frac{K}{N} \sum_{j=1}^{N} A_{ij} \sin(\theta_j - \theta_i)\right]$$

subject to the cumulative substrate constraint $\Omega(t) < S_{\max}$, where

$$\Omega(t) = \int_0^t \Big(\sum_i \eta_i\, x_i\, f_i^{(0)} - D_{\max}\Big)_+\, ds, \qquad H = \max\!\Big(0,\ 1 - \tfrac{\Omega}{S_{\max}}\Big)$$

See [Thermodynamics of Emergent Orchestration](../core/thermodynamics-of-orchestration.md)
for parameter definitions and simulation results, and [The Viable
Corridor](../../papers/viable-corridor.md) for the current proof scope and limitations.
