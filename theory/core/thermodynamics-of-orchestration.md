# Thermodynamics of Emergent Orchestration (TEO)

*A stylized viability model coupling evolutionary game theory, nonlinear dynamics, control
theory, and a substrate-budget proxy.*

> **Foundation context.** TEO is an added domain model, not the repository's mathematical
> foundation. Running its ODEs predicts the model's own trajectories. Whether it describes
> an AI ecology, organization, or civilization requires calibration and comparison with
> alternatives.

---

## Motivation

The Multi-Paradigm Orchestrator introduced in this repository describes four qualitative regimes (Harmonic, Homeostatic, Market, Flow) for steering agent ecologies. TEO translates these paradigms into a single **coupled system of ordinary differential equations (ODEs)** that can be numerically simulated, empirically calibrated, and — critically — *falsified*.

## 1. System State

We consider $N$ agents. Each agent $i$ at time $t$ is described by two state variables:

- $x_i(t) \in [0, 1]$: Its share of total system resources (power, capital, compute). Constrained such that $\sum_i x_i = 1$.
- $\theta_i(t) \in [0, 2\pi)$: Its "value orientation" — the direction of its utility vector projected onto a unit circle.

## 2. The Market Paradigm — Replicator Dynamics

The economic engine of the system is modeled by the **replicator equation** from evolutionary game theory (Taylor & Jonker, 1978):

$$\frac{dx_i}{dt} = x_i \left( f_i(\mathbf{x}) - \bar{\phi}(\mathbf{x}) \right)$$

where $f_i(\mathbf{x})$ is the fitness (profitability, task-completion rate) of agent $i$, and $\bar{\phi}(\mathbf{x}) = \sum_j x_j f_j(\mathbf{x})$ is the population-average fitness.

**Interpretation:** Agents that outperform the population average grow under this equation.
Winner-take-all follows for selected fitness functions and dominance assumptions, not from
every unregulated replicator system. The link to instrumental convergence is interpretive.

## 3. The Harmonic Paradigm — Kuramoto Synchronization

Value alignment across agents is modeled by the **Kuramoto model** for coupled oscillators (Kuramoto, 1975), gated by the substrate-health variable $H \in [0,1]$ (§5) so that value dynamics also freeze at substrate collapse:

$$\frac{d\theta_i}{dt} = H\left[\omega_i + \frac{K}{N} \sum_{j=1}^{N} A_{ij} \sin(\theta_j - \theta_i)\right]$$

(At full substrate health $H = 1$ this is the standard Kuramoto model, so the critical-coupling analysis below is unaffected.) Where:
- $\omega_i$: The intrinsic "natural frequency" of agent $i$ (its inherent bias or personality).
- $K > 0$: The global coupling strength (culture, discourse, shared media).
- $A_{ij} \in \{0, 1\}$: The adjacency matrix of the communication network.

**Interpretation:** Under the frequency distribution, topology, coupling convention, and
limit assumed in the paper, a Kuramoto synchronization transition occurs near $K_c$.
Calling synchronized phase “cultural consensus” or low order “polarization” is a heuristic
mapping. Low order does not imply chaos.

The **order parameter** $r(t)$ measures global coherence:

$$r(t) e^{i\psi(t)} = \frac{1}{N} \sum_{j=1}^{N} e^{i\theta_j(t)}$$

When $r \to 1$, the system is synchronized. When $r \to 0$, it is incoherent. This is the *thermodynamic analogue* of our Coherence Score $C$.

## 4. The Homeostatic Paradigm — Regulatory Control

To prevent the replicator equation from producing monopolies, we introduce a control term $\mathcal{H}_i$ that acts as the system's "immune response" (the equivalent of antitrust law or agent kill-switches):

$$\mathcal{H}_i(\mathbf{x}) = -\gamma \cdot \max\left(0,\ x_i - x_{\text{reg}}\right) + \frac{\gamma}{N}\sum_{j=1}^{N}\max\left(0,\ x_j - x_{\text{reg}}\right)$$

where $\gamma > 0$ is the regulatory strength and $x_{\text{reg}}$ is a **regulatory** threshold set strictly below the failure threshold $x_{\text{crit}}$ — the brake must engage *before* the boundary, not at it. The second, uniform-redistribution term makes the brake **simplex-preserving** ($\sum_i \mathcal{H}_i = 0$), so $\sum_i x_i = 1$ is conserved exactly.

**Interpretation:** Any agent exceeding the regulatory threshold $x_{\text{reg}}$ experiences a proportional corrective force, and the aggregate penalty is redistributed across the population — antitrust law or agent kill-switches that act early, without leaking probability mass off the simplex.

## 5. The Biological Veto — Entropy Budget

Physical implementations dissipate energy, but TEO selects a particular proxy. The model
assigns a finite *instantaneous* capacity $D_{\max}$ and cumulative tolerance $S_{\max}$.
Modeled production tracks **raw throughput** $f_i^{(0)}$:

$$\frac{dS_{\text{sys}}}{dt} = \sum_{i=1}^{N} \eta_i\, x_i\, f_i^{(0)}(\mathbf{x})$$

where $\eta_i$ is agent $i$'s entropy-per-unit-output coefficient. The **accumulated overshoot** and the **substrate-health** variable are

$$\Omega(t) = \int_0^t \big(\dot{S}_{\text{sys}} - D_{\max}\big)_+\, ds, \qquad H(t) = \max\!\Big(0,\ 1 - \frac{\Omega(t)}{S_{\max}}\Big),$$

and $H$ multiplies the replicator drift and the value dynamics (§3), so the system freezes as $H \to 0$. The operative constraint is **cumulative**, $\Omega(t) < S_{\max}$ for all $t$: a brief overshoot is survivable; only *sustained* overshoot that fills the reservoir collapses the substrate.

**Interpretation:** The chosen damage law sets $H=0$ when integrated overshoot fills the
reservoir, freezing the modeled drift. This is inspired by finite physical limits; it is
not a derivation of planetary boundaries or server failure from first principles.

## 6. The Full Coupled System

Combining all terms, the complete TEO dynamics are:

$$\frac{dx_i}{dt} = H\,x_i \left( f_i^{(0)}(\mathbf{x}) - \bar{\phi}^{(0)}(\mathbf{x}) \right) + \mathcal{H}_i(\mathbf{x})$$

$$\frac{d\theta_i}{dt} = H\left[\omega_i + \frac{K}{N} \sum_{j=1}^{N} A_{ij} \sin(\theta_j - \theta_i)\right]$$

subject to the cumulative substrate constraint $\Omega(t) < S_{\max}$ for all $t$, where (§5)

$$\Omega(t) = \int_0^t \Big(\sum_i \eta_i x_i f_i^{(0)} - D_{\max}\Big)_+ ds, \qquad H = \max\!\Big(0, 1 - \tfrac{\Omega}{S_{\max}}\Big)$$

feeds back into both equations above. The brake $\mathcal{H}_i$ carries no $H$ prefactor (it acts even as the drift freezes).

## 7. Predictions

Under the paper's stated assumptions, this system makes model-internal predictions:

1. **With strict dominance and $\gamma=0$:** the dominant resource share approaches a
   simplex vertex.
2. **Under the paper's Kuramoto assumptions and $K<K_c$:** a coherent initial state
   dephases toward the reported low-order regime.
3. **When $\Omega(t)$ reaches $S_{\max}$:** the declared health law sets $H=0$.
4. **Viability in the model:** the stated component conditions are necessary; sufficiency
   remains conjectured and is expected to require $\gamma>\gamma_c$.

> **Canonical derivation.** This page is the conceptual derivation; the citation-ready, source-of-truth version of these equations — including the strict-dominance assumption, the $K_c = 2/(\pi g(0))$ result, and the capability-loading result — is [The Viable Corridor](../../papers/viable-corridor.md) (§2–§3, Appendix A).

## 8. Identity Persistence: The Chord vs. Arpeggio

Following Perrier & Bennett (2026), we define the **Identity Persistence $\text{IP}$** of an agent (see [glossary](../reference/glossary.md) and [lerchner-boundary.md](../teo-framework/lerchner-boundary.md) for the formal definition). 

The identity branch hypothesizes that selected goals and constraints should jointly affect
a commitment under perturbation.

- **Arpeggio model:** selected components are consulted or applied at different times.
- **Chord model:** selected components are composed at the commitment boundary.

IP and $\text{SII}=P\times R\times A\times\text{IP}$ are selected diagnostics for toy
tests. Neither distinguishes “talking about the self” from “being the self” in general, and
neither is derived from the TEO equations.

## References

1. Taylor, P. D., & Jonker, L. B. (1978). *Evolutionary stable strategies and game dynamics.* Mathematical Biosciences.
2. Kuramoto, Y. (1975). *Self-entrainment of a population of coupled non-linear oscillators.* Lecture Notes in Physics.
3. Rockström, J. et al. (2009). *A safe operating space for humanity.* Nature.
4. Friston, K. (2010). *The free-energy principle: a unified brain theory?* Nature Reviews Neuroscience.
