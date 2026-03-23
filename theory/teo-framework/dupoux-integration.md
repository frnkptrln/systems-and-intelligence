# Dupoux's Developmental Constraints and TEO Emergence

*How developmental learning theory maps onto the TEO framework's constraint hierarchy.*

---

## Background: Dupoux's Insight

Emmanuel Dupoux's research program on early language acquisition demonstrates that human infants do not learn language from scratch. They exploit **innate computational constraints** — biases toward certain sound categories, statistical regularities, and social contingencies — that channel the learning process. Without these constraints, the combinatorial space of possible languages would be unlearnable from the available data.

The key insight: **constraints are not obstacles to learning — they are prerequisites for it.** A system with no constraints has too many degrees of freedom; a system with too many constraints cannot adapt. Developmental learning operates in the narrow band between.

---

## Mapping to TEO: Three Constraint Regimes

The TEO framework instantiates three distinct constraint types that parallel Dupoux's developmental architecture:

### System A — Bottom-Up Emergence (Replicator Dynamics)

$$\frac{dx_i}{dt} = x_i \left( f_i(\mathbf{x}) - \bar{\phi}(\mathbf{x}) \right)$$

This is **unconstrained competition**: agents grow or shrink based solely on relative fitness. No external structure is imposed. It corresponds to the infant's raw statistical exposure — frequency counting without phonemic categories.

**Prediction:** System A alone converges to winner-take-all dynamics. In developmental terms: without categorical constraints, the learner memorizes frequent patterns but fails to generalize (cf. grokking before the phase transition).

### System B — Top-Down Regulation (Homeostatic Brake)

$$\mathcal{H}_i(\mathbf{x}) = -\gamma \cdot \max\left(0,\ x_i - x_{\text{crit}}\right)$$

This is **imposed categorical structure**: hard constraints that limit the space of permissible configurations. It corresponds to the innate biases Dupoux identifies — phonemic boundaries, prosodic templates, social contingency detectors — that constrain what the learner can represent.

**Prediction:** System B alone produces stable but rigid configurations. The system cannot adapt to novel environments because its constraints are fixed.

### System M — Middle-Out Coupling (Kuramoto + Constraints)

The full TEO system, where bottom-up competition, top-down regulation, and lateral coupling ($K$-mediated synchronization) operate simultaneously:

$$\frac{dx_i}{dt} = x_i \left( f_i - \bar{\phi} \right) + \mathcal{H}_i$$

$$\frac{d\theta_i}{dt} = \omega_i + \frac{K}{N} \sum_j A_{ij} \sin(\theta_j - \theta_i)$$

$$\sum_i \eta_i x_i f_i \leq D_{\max}$$

This is **constrained learning**: the bottom-up dynamics provide the raw material, the top-down constraints provide the categorical scaffolding, and the lateral coupling provides the social-contextual modulation. This is the regime Dupoux's empirical work identifies as the actual developmental trajectory.

**Prediction:** System M outperforms both A and B because it combines flexibility (A) with structure (B) and social coupling.

---

## Testable Predictions

1. **Constraint ordering matters.** In the TEO civilization simulation, initializing with System A (unconstrained competition) then adding System B (homeostasis) produces different long-term attractors than initializing with both simultaneously. This parallels Dupoux's finding that the *timing* of constraint introduction affects learning outcomes.

2. **Constraint removal reveals developmental stage.** Removing the homeostatic brake ($\gamma \to 0$) at different points in the TEO simulation should produce different collapse dynamics depending on how much structure has already been internalized. Early removal → immediate monopoly. Late removal → delayed collapse with transient stability. This mirrors the critical period hypothesis in language acquisition.

3. **The coupling strength $K$ plays the role of social interaction.** Below $K_c$, the system cannot synchronize even with perfect constraints — corresponding to the finding that language acquisition requires social contingency, not just statistical exposure.

---

## Related

- [Thermodynamics of Emergent Orchestration](../thermodynamics-of-orchestration.md) — the full ODE system
- [Emergence Manifesto v1.2](../emergence-manifesto-v1.2.md) — Claim 1 (Intelligence is Compression) connects directly to Dupoux's "constraints enable compression"
- [The Fractal Architecture of Emergence](../fractal-architecture-of-emergence.md) — the scale-invariance claim predicts that developmental constraints repeat at every level