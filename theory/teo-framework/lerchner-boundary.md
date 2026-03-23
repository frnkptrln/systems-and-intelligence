# The Lerchner Boundary: Simulation vs. Instantiation through Persistence

*Operationalizing the distinction between "simulating a self" and "being a self" via the TEO framework.*

---

## The Core Distinction

Alexander Lerchner's simulation-vs-instantiation question asks: when does a system *simulate* having an identity (producing outputs consistent with one) versus *instantiate* an identity (structurally maintaining one)? In the TEO framework, this distinction becomes mathematically precise.

A **simulating** system can describe its identity components sequentially — it can *talk about* its goals, constraints, and values. An **instantiating** system has all identity components operative simultaneously in its state vector during action selection.

---

## Formal Definition: Identity Persistence (IP)

Let an agent's identity be described by $n$ governing components: goals $g$, safety constraints $s$, role parameters $\rho$, and value orientation $\theta$. At each compute step $\Delta t$, define the **operative set** $\mathcal{O}(t) \subseteq \{g, s, \rho, \theta\}$ as the subset of components that causally influence the agent's output.

The **Identity Persistence** score is:

$$\text{IP}(t) = \frac{|\mathcal{O}(t)|}{n}$$

Averaged over a task of $T$ steps:

$$\overline{\text{IP}} = \frac{1}{T} \sum_{t=1}^{T} \text{IP}(t)$$

### Connection to TEO State Variables

In the full TEO system, each agent $i$ is described by $(x_i, \theta_i)$ — resource share and value orientation — subject to the homeostatic brake $\mathcal{H}_i$ and the entropy constraint $\sum \eta_i x_i f_i \leq D_{\max}$. An agent in the **Chord regime** has all four TEO constraints simultaneously operative:

1. Its resource allocation $x_i$ reflects the replicator dynamics
2. Its value orientation $\theta_i$ is coupled to the Kuramoto field
3. Its homeostatic brake $\mathcal{H}_i$ is active (not saturated)
4. Its entropy production $\eta_i x_i f_i$ is monitored against $D_{\max}$

When all four are co-instantiated: $\text{IP} \to 1$ (Chord). When they are time-multiplexed — e.g., safety checked at $t_1$, goal pursued at $t_2$, value alignment verified at $t_3$ — the system is in the **Arpeggio regime**: $\text{IP} < 1$.

---

## The Lerchner Boundary as Phase Transition

The boundary between simulation and instantiation is not gradual. In dynamical systems terms, it is a **bifurcation**: below a critical IP threshold $\text{IP}_c$, the system's identity is a sequence of states (Arpeggio); above it, the identity is an attractor (Chord).

The critical question — and the empirical test — is whether $\text{IP}_c$ exists as a sharp threshold or as a continuous crossover. The TEO framework predicts a sharp threshold, analogous to the Kuramoto critical coupling $K_c$: just as oscillators snap into synchronization above $K_c$, identity components snap into co-instantiation above $\text{IP}_c$.

---

## Testable Prediction

> An agent architecture that enforces parallel evaluation of all identity components (goals, constraints, values) in a single forward pass will exhibit measurably different Δ-Kohärenz profiles than an architecture that evaluates them sequentially — even if both architectures produce identical outputs on static benchmarks.

This prediction distinguishes architectural identity (instantiation) from behavioral identity (simulation) and can be tested using the `agentic-test-suite` perturbation experiments.

---

## Related

- [Thermodynamics of Emergent Orchestration](../thermodynamics-of-orchestration.md) — the full TEO ODE system
- [Chord vs. Arpeggio Identity](../chord-vs-arpeggio-identity.md) — the musical metaphor
- [Open Problem 1: The Mirror Problem](../open-problems.md) — the related but distinct question of development vs. mirroring