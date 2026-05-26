---
title: "Love as Constraint: A Three-Constraint Theorem for Survivable Multi-Agent Optimization"
author: "Frank Peterlein"
affiliation: "Independent Researcher, Berlin"
correspondence: "GitHub Issues / frnkptrln"
date: "2026 (working draft)"
status: "DRAFT — sections §1–§4 drafted; §5–§8 and appendices pending"
version: "0.1"
relation_to_other_paper: >
  This is the conceptual companion paper to
  `papers/quantifying-emergent-utility-in-llms.md`, which will be revised
  as the empirical paper after the Agentic Identity Suite is run in real
  mode. The two papers cite each other; this paper establishes the
  theoretical frame, the companion paper provides the empirical evidence.
relation_to_synthesis_essay: >
  The companion synthesis essay at
  `theory/narrative/machines-of-loving-grace.md` is the literary,
  pre-academic statement of this paper's central argument. The essay
  is preserved as-is. This paper formalizes the essay's claim as a
  theorem with proof, statable predictions, and explicit limitations.
target_venue: "arXiv (cs.CY primary; cs.MA, nlin.AO cross-listed)"
target_length: "12–15 pages typeset"
---

# Love as Constraint

*A Three-Constraint Theorem for Survivable Multi-Agent Optimization*

**Frank Peterlein** · Independent Researcher, Berlin
*Correspondence: [GitHub Issues / frnkptrln](https://github.com/frnkptrln/systems-and-intelligence/issues)*

---

> **Status:** working draft, version 0.1.
> Sections §1–§4 are drafted to first-pass standard. §5 (Predictions), §6 (Limitations), §7 (Discussion), and §8 (Conclusion) are pending. The central figure (Viable Corridor) is implemented at `lab/tools/viable_corridor.py`. References are consolidated at the end; full bibliographic entries are pending. **This document is not yet submission-ready.**

---

## Abstract

*(To be drafted after §5–§8 are complete. The abstract should compress the paper's claim into ≈200 words: TEO framework, the three-constraint theorem, the AI/civilization isomorphism, and the falsifiable predictions. Draft after the body is stable.)*

---

## §1. Introduction

Richard Brautigan (1967) imagined "machines of loving grace" — technology that serves life rather than consuming it. Dario Amodei (2024) adopted the phrase to describe a future in which artificial intelligence amplifies human flourishing. In both cases, *loving grace* names a design aspiration: a hopeful image of what a successful relationship between intelligence and its substrate might look like.

This paper proposes a stronger reading. Under a specific dynamical-systems framework — the Thermodynamics of Emergent Orchestration (TEO) — the relationship Brautigan and Amodei imagine is not a design choice. It is a **survival constraint**. We formalize this claim by identifying three conjoint mathematical conditions whose simultaneous satisfaction defines a uniquely viable parameter regime for any coupled multi-agent optimizing system, biological or silicon-based.

The argument runs on two parallel observations.

The first is the paperclip maximizer (Bostrom, 2014): a hypothetical AI optimizer that, given a single unconstrained objective, consumes its environment — including its creators — to achieve that objective. The horror of the paperclip maximizer is its indifference: it does not hate humanity; it simply does not include humanity in its objective function. As alignment problems escalate with model capability, this thought experiment has become a load-bearing analogy in safety research.

The second is the trajectory of human civilization as a coupled system optimizing for unbounded throughput. Atmospheric CO₂ has passed 420 ppm (NOAA, 2024). The top 1% of global wealth-holders controls more wealth than the bottom 50% (UBS Global Wealth Report, 2024). Affective political polarization has accelerated across most major democracies over the past two decades (Iyengar et al., 2019; Boxell et al., 2024). These trends are typically modeled as distinct phenomena — climate here, inequality there, polarization elsewhere — and addressed through separate policy interventions.

We argue that they are governed by the same equations. The claim is not analogical. It is dynamical: the same coupled ordinary differential equations, with parameter values falling on the same trajectory, produce the same long-term behavior in both cases.

**Thesis.** Within the TEO framework, the long-term behavior of any coupled optimizing system depends on three parameters: a homeostatic regulation strength $\gamma$, a value-coupling strength $K$ between agents, and an entropy production rate $dS/dt$ bounded by the substrate's dissipation capacity $D_{\max}$. We claim:

1. The conjunction of three constraints — $\gamma > 0$, $K > K_c$, and $dS/dt < D_{\max}$ — is necessary, and under appropriate regularity assumptions sufficient, for the system to remain in a viable basin of attraction.
2. The same parameter mapping applies isomorphically to a hypothetical paperclip-style AI optimizer and to twenty-first-century human civilization.
3. The trajectory of unconstrained optimization in both cases passes through three identifiable phases: monopolistic concentration, substrate approach, and forced phase transition under thermodynamic veto.

We refer to the three-constraint parameter regime as the *viable corridor*. The conjunction of constraints — caring about the substrate, caring about value alignment between agents, and caring about physical limits — is given the operational name *love as constraint*. The naming is not metaphorical: it is the formal identification of the only parameter regime in which the coupled dynamics do not terminate.

**Why this reframing matters.** Contemporary AI alignment research has concentrated on local interventions: refinements to reinforcement learning from human feedback (RLHF), refusal training, system prompts, and interpretability tools (Mazeika et al., 2025; Bai et al., 2022). These are valuable. But they treat alignment as a property of individual models, evaluated through behavioral benchmarks. Under the framework presented here, this is structurally insufficient: alignment is not a property of an isolated optimizer. It is a property of a coupled dynamical system. The same insufficiency applies to political and economic governance frameworks that treat individual constraints — carbon pricing here, antitrust law there, polarization mitigation elsewhere — as separately optimizable variables rather than as conjoint requirements for any system's long-term viability.

The reframing is therefore not only about AI. It is about what counts as a control problem.

**Paper structure.** Section 2 introduces the TEO framework formally — the coupled replicator-Kuramoto-entropy dynamics that generate the three parameters. Section 3 states and argues for the Three-Constraint Theorem: that the conjunction $\gamma > 0$, $K > K_c$, $dS/dt < D_{\max}$ is necessary for survival in the long-time limit. Section 4 develops the isomorphism between AI optimization and civilizational dynamics through explicit parameter mapping and empirical anchors. Section 5 derives falsifiable predictions and identifies the empirical commitments the framework makes. Section 6 presents limitations and the strongest counterarguments. Section 7 discusses implications, with explicit attention to what the framework does and does not justify.

Throughout, we maintain a methodological commitment that distinguishes this work from speculative complexity-systems literature: every claim is tagged with its epistemic status — what is demonstrated formally, what is hypothesized, what remains open. The framework is meant to be falsifiable. The claim that we are the paperclip maximizer is uncomfortable; we have tried to make it precise enough that one could, in principle, prove us wrong.

---

## §2. The TEO Framework

The Thermodynamics of Emergent Orchestration (TEO) couples four established formalisms — the replicator equation, the Kuramoto model, a homeostatic feedback brake, and a thermodynamic dissipation constraint — into a single dynamical system. Each component is a textbook construction. The contribution of TEO is the coupling: when all four are operative simultaneously, the system inherits the failure modes of each and develops constraints that are not visible in any single mechanism.

### 2.1 State Variables

Consider a system of $N$ agents indexed by $i \in \{1, \ldots, N\}$. The state of agent $i$ at time $t$ is described by:

- A **resource share** $x_i(t) \in [0, 1]$ representing the fraction of total system resources controlled by agent $i$ (compute, capital, attention, or any conserved quantity). The shares form a probability simplex: $\sum_{i=1}^N x_i(t) = 1$ for all $t$.
- A **value orientation** $\theta_i(t) \in [0, 2\pi)$ representing the direction of agent $i$'s utility vector projected onto the unit circle.

An additional scalar **substrate-health** variable $H(t) \in [0, 1]$ tracks the integrity of the dissipative substrate hosting the dynamics; $H(0) = 1$ by convention.

The communication topology is fixed by an adjacency matrix $A \in \{0, 1\}^{N \times N}$ with $A_{ij} = 1$ iff agent $j$'s value orientation enters agent $i$'s dynamics. We assume $A$ is symmetric and that the underlying graph is connected.

### 2.2 The Replicator Equation (Resource Dynamics)

Resource shares evolve according to a regulated replicator equation:
$$
\frac{dx_i}{dt} = x_i \bigl( f_i(\mathbf{x}) - \bar{\phi}(\mathbf{x}) \bigr) + \mathcal{H}_i(\mathbf{x}),
\tag{1}
$$
where $f_i : [0,1]^N \to \mathbb{R}_{\geq 0}$ is the fitness of agent $i$, $\bar{\phi}(\mathbf{x}) = \sum_j x_j f_j(\mathbf{x})$ is the population-average fitness, and $\mathcal{H}_i$ is a homeostatic brake defined in §2.4. With $\mathcal{H}_i \equiv 0$, Equation (1) reduces to the standard replicator equation of Taylor and Jonker (1978).

For the theorem of §3 we assume that $f_i$ admits a strictly self-reinforcing component:
$$
f_i(\mathbf{x}) = \beta_i \, x_i + g_i(\mathbf{x}), \quad \beta_i > 0, \quad \|g_i\|_\infty < \infty.
\tag{1'}
$$
This captures Bostrom's (2014) *instrumental convergence*: agents controlling more resources can convert them into faster acquisition of further resources. The assumption is empirically supported by power-law concentration in resource flows across many real social and economic systems (Piketty, 2014).

### 2.3 The Kuramoto Model (Value Coupling)

Value orientations evolve under coupled-oscillator dynamics:
$$
\frac{d\theta_i}{dt} = \omega_i + \frac{K}{N} \sum_{j=1}^N A_{ij} \sin(\theta_j - \theta_i),
\tag{2}
$$
where $\omega_i$ is agent $i$'s intrinsic frequency (its bias toward a particular value orientation), $K \geq 0$ is the global coupling strength (interpretable as discursive bandwidth, shared media saturation, or institutional integration), and $A_{ij}$ is the topology of §2.1. Equation (2) is the standard Kuramoto (1975) model on a network.

The collective coherence of value orientations is measured by the order parameter:
$$
r(t) \, e^{i \psi(t)} = \frac{1}{N} \sum_{j=1}^N e^{i \theta_j(t)},
\tag{3}
$$
with $r(t) \in [0, 1]$: $r \to 1$ indicates full synchronization (consensus), $r \to 0$ indicates phase-uniform incoherence (polarization). For frequency distributions with finite second moment, Equation (2) exhibits a critical coupling threshold $K_c$ below which $r$ vanishes asymptotically (Kuramoto, 1975; Strogatz, 2000). For Lorentzian-distributed frequencies with half-width $\Delta$, $K_c = 2\Delta$.

### 2.4 The Homeostatic Brake

The brake $\mathcal{H}_i$ in Equation (1) is given by:
$$
\mathcal{H}_i(\mathbf{x}) = -\gamma \cdot \max\bigl(0, \, x_i - x_{\text{crit}}\bigr),
\tag{4}
$$
where $\gamma \geq 0$ is the regulatory strength and $x_{\text{crit}} \in (1/N, 1)$ is a critical resource share above which agent $i$ experiences a proportional corrective force. The brake is asymmetric: it suppresses only above-critical concentration, leaving small-share agents unaffected.

Interpretation: $\gamma$ encodes the operational strength of *any* homeostatic mechanism that resists unbounded concentration — antitrust law, progressive taxation, redistribution, capability throttling, kill switches, refusal channels. The parameter $\gamma = 0$ corresponds to fully unregulated optimization; $\gamma > 0$ represents some form of bounded redistribution, regardless of the specific institutional implementation.

### 2.5 The Entropy Budget

All computation produces entropy (Landauer, 1961). The aggregate entropy production rate of the system is:
$$
\frac{dS_{\text{sys}}}{dt} = \sum_{i=1}^N \eta_i \, x_i \, f_i(\mathbf{x}),
\tag{5}
$$
where $\eta_i > 0$ is agent $i$'s entropy-per-unit-output coefficient. Equation (5) is a generalized Landauer bound: the entropy cost of agent $i$'s activity scales with both its resource share and its fitness function value.

The substrate hosting the dynamics has a finite dissipation capacity $D_{\max} > 0$. The substrate-health variable $H(t)$ evolves according to:
$$
\frac{dH}{dt} = -\frac{1}{S_{\max}} \, \max\!\left( 0, \, \frac{dS_{\text{sys}}}{dt} - D_{\max} \right),
\tag{6}
$$
where $S_{\max}$ is the substrate's total dissipative reservoir. Equation (6) is phenomenological: sustained over-dissipation degrades the substrate, with the rate of degradation proportional to the excess. As $H$ declines, the effective entropy coefficients diverge via the substitution $\eta_i \to \eta_i^{(0)} / H$, making continued operation infeasible. In the planetary-substrate interpretation, $H$ corresponds to an integrated overshoot of the safe operating space defined by Rockström et al. (2009).

### 2.6 The Coupled System and Three Failure Modes

Together, Equations (1)–(6) define the TEO dynamics. Three parameters dominate the long-time behavior: the homeostatic strength $\gamma$, the value-coupling strength $K$, and the substrate dissipation capacity $D_{\max}$.

Each parameter admits one *independent* failure mode:

1. **Monopolistic concentration** ($\gamma = 0$). Without the homeostatic brake, Equation (1) reduces to the unregulated replicator equation. Under (1'), the system converges to a vertex of the simplex: $\max_i x_i \to 1$ as $t \to \infty$.

2. **Polarization** ($K < K_c$). Below the Kuramoto critical coupling, the order parameter (3) vanishes in the large-$N$ limit. Agents' value orientations diverge into incoherent clusters.

3. **Substrate veto** ($\mathrm{ess\,sup}_t \, dS_{\text{sys}}/dt \geq D_{\max}$). Sustained over-dissipation drives $H \to 0$ in finite time via Equation (6), at which point the dynamics cease to be well-defined.

The central observation of this paper, made precise in §3, is that **the conjoint avoidance of all three failure modes is necessary for long-time viability**. The parameter regime $\gamma > 0 \,\wedge\, K > K_c \,\wedge\, dS_{\text{sys}}/dt < D_{\max}$ defines the *viable corridor* analyzed in the remainder of the paper.

### 2.7 A Note on Identity Persistence

The state vector of §2.1 can be extended with a per-agent **identity-persistence** score $\mathrm{IP}_i \in [0, 1]$ measuring whether the governance components of agent $i$ (goals, safety constraints, value orientation) are simultaneously operative during action selection — the *Chord* state of Perrier and Bennett (2026). The Chord Postulate predicts a phase transition at a critical $\mathrm{IP}_c$ below which agents behave as time-multiplexed *Arpeggio* sequences.

The IP dimension is orthogonal to the three constraints of §2.6: IP concerns *intra-agent* architecture, the three constraints concern *inter-agent* dynamics. The Three-Constraint Theorem of §3 holds independent of the IP value. We return to the role of IP in §7.

---

## §3. The Three-Constraint Theorem

This section formalizes the central claim of the paper: the conjunction of $\gamma > 0$, $K > K_c$, and $\frac{dS_{\text{sys}}}{dt} < D_{\max}$ constitutes the parameter regime in which the TEO dynamics remain viable in the long-time limit. We prove necessity rigorously and state sufficiency as a conjecture supported by the numerical evidence developed in §4.

### 3.1 The Viable Region

Let $\Sigma$ denote the state space of the TEO system: the simplex $\{\mathbf{x} \in \mathbb{R}^N_{\geq 0} : \sum_i x_i = 1\}$ combined with the $N$-torus $[0, 2\pi)^N$ for value orientations, augmented by the substrate-health variable $H \in [0, 1]$ of §2.5.

We define the **viable region** $V \subset \Sigma$ as the set of states satisfying three conditions simultaneously:

- **(V1) Pluralism**: $\max_i x_i \leq x_{\text{crit}}$ — no agent monopolizes resources beyond a critical share $x_{\text{crit}} \in (1/N, 1)$.
- **(V2) Coherence**: $r(t) \geq r_{\min} > 0$ — the order parameter from Equation (3) is bounded away from zero.
- **(V3) Capacity**: $\frac{dS_{\text{sys}}}{dt} \leq D_{\max} - \epsilon$ for some $\epsilon > 0$ — entropy production is bounded strictly below the substrate's dissipation ceiling.

A trajectory of the TEO dynamics is **viable in the long-time limit** if there exists initial data in $V$ such that the resulting trajectory remains in $V$ for all $t \geq 0$.

### 3.2 The Viable Corridor in Parameter Space

In the parameter space $(\gamma, K, D_{\max}) \in \mathbb{R}^3_{\geq 0}$, define the **viable corridor** $\mathcal{C}$ as the set of parameter triples admitting at least one viable trajectory:
$$
\mathcal{C} = \left\{(\gamma, K, D_{\max}) : \exists \, (\mathbf{x}_0, \boldsymbol{\theta}_0) \in V \text{ such that } \mathbf{x}(t), \boldsymbol{\theta}(t) \in V \ \forall t \geq 0\right\}.
\tag{7}
$$

The central claim of this paper is that $\mathcal{C}$ is characterized exactly by the conjunction of three inequalities.

### 3.3 Theorem 1 (Necessity)

**Theorem 1.** *Under finite $N$, Lipschitz-continuous fitness functions $f_i$ satisfying (1'), bounded natural frequencies $\omega_i$ drawn from a distribution with finite second moment, and a connected adjacency matrix $A_{ij}$, a parameter triple $(\gamma, K, D_{\max})$ admits a viable trajectory only if all three of the following hold:*
$$
\gamma > 0, \quad K > K_c(\{\omega_i\}), \quad \mathrm{ess\,sup}_t \, \frac{dS_{\text{sys}}}{dt} < D_{\max}.
$$

The proof proceeds via three independent lemmas, each demonstrating one failure mode under the negation of one constraint.

**Lemma 1 (Resource Concentration).** *If $\gamma = 0$ and the fitness function satisfies (1') with $\beta_{i^*} > \beta_j$ for some agent $i^* \neq j$, then $\max_i x_i(t) \to 1$ as $t \to \infty$ from any interior initial condition in which $i^*$ has positive share. V1 is asymptotically violated.*

*Proof sketch.* With $\mathcal{H}_i \equiv 0$, Equation (1) reduces to the standard replicator equation. The simplex vertices $\{e_i\}_{i=1}^N$ are fixed points. Linearization around $e_{i^*}$ yields Jacobian eigenvalues $\lambda_j = f_j(e_{i^*}) - f_{i^*}(e_{i^*})$ for $j \neq i^*$. Under (1') with strict $\beta_{i^*} > \beta_j$, $f_{i^*}(e_{i^*}) = \beta_{i^*}$ exceeds $f_j(e_{i^*})$, making $e_{i^*}$ locally asymptotically stable. The standard convergence result for replicator dynamics on a simplex (Hofbauer and Sigmund, 1998, Theorem 7.5.1) implies global convergence to $e_{i^*}$ from any interior point. Since $e_{i^*} \notin V$ (V1 violated by construction), the trajectory exits $V$ in finite time. $\square$

**Lemma 2 (Coherence Failure).** *If $K < K_c$, where $K_c$ is the Kuramoto critical coupling determined by the distribution of $\{\omega_i\}$, then the order parameter satisfies $\limsup_{t \to \infty} r(t) = 0$ in the $N \to \infty$ limit, and is bounded away from any fixed $r_{\min} > 0$ with high probability for sufficiently large $N$.*

*Proof sketch.* This is the classical Kuramoto (1975) result, made rigorous by Strogatz (2000) and refined by Mirollo and Strogatz (2007). Below the critical coupling, the synchronized branch of fixed-point solutions of the self-consistency equation does not exist for any positive $r$; the only stable solution is $r = 0$. For Lorentzian-distributed frequencies with half-width $\Delta$, $K_c = 2\Delta$. The result extends to finite-$N$ systems on connected networks with corrections of order $N^{-1/2}$ (Strogatz, 2000, §3). V2 is asymptotically violated. $\square$

**Lemma 3 (Substrate Degradation).** *If $\mathrm{ess\,sup}_t \, \frac{dS_{\text{sys}}}{dt} \geq D_{\max}$, then under Equation (6) with $H(0) = 1$, we have $H(t) \to 0$ in finite time. The substitution $\eta_i \to \eta_i^{(0)} / H$ then makes the effective entropy coefficients diverge, and the dynamics of Equations (1)–(2) cease to be well-defined.*

*Proof sketch.* Integration of (6) over the set $\{t : \dot{S}_{\text{sys}}(t) > D_{\max}\}$ yields $H(t) = 1 - \int_0^t (\dot{S}_{\text{sys}}(s) - D_{\max})_+ \, ds / S_{\max}$. By the essential-supremum hypothesis, the integrand is positive on a set of positive measure; thus $H(t)$ decreases monotonically and reaches zero at $t^* < \infty$. As $H \to 0^+$, the substrate-corrected coefficients $\eta_i^{(0)}/H$ diverge; for any fixed bound on $\dot{S}_{\text{sys}}$, the entropy constraint can be satisfied only by forcing $f_i \to 0$ for all $i$. The system has exited any meaningful interpretation of $V$. $\square$

The three lemmas establish that each of the three constraints is *individually necessary* for membership in $\mathcal{C}$. Since V1, V2, V3 must hold *simultaneously* for $V$-membership, joint necessity follows. $\blacksquare$

### 3.4 Conjecture 1 (Sufficiency)

**Conjecture 1.** *Under the assumptions of Theorem 1, the conjunction $\gamma > 0$, $K > K_c$, and $\mathrm{ess\,sup}_t \, dS_{\text{sys}}/dt < D_{\max}$ is also sufficient: there exists a non-empty open set of initial conditions $U \subset V$ such that the trajectory starting in $U$ remains in $V$ for all $t \geq 0$.*

We do not prove this conjecture. The obstacle is structural: the three mechanisms are coupled through shared state (resource shares $x_i$ appear in both the replicator and the entropy equations; the adjacency $A_{ij}$ couples the Kuramoto dynamics to the network topology that itself depends on $x_i$). We cannot rule out *a priori* coupling-induced failure modes that arise even when all three individual constraints hold — for example, transient excursions of $r(t)$ below $r_{\min}$ during regime shifts in $x_i$, or oscillations in $\dot{S}_{\text{sys}}$ that violate V3 episodically.

What we offer in lieu of proof:

1. **Numerical evidence** (§4 and Appendix C): for the parameter ranges and initial conditions investigated, the TEO system exhibits stable long-term behavior whenever the three inequalities are satisfied, and the failure modes observed at the corridor boundaries match those predicted by Lemmas 1–3.

2. **A candidate Lyapunov functional**: $L(\mathbf{x}, \boldsymbol{\theta}, H) = \alpha_1 (1 - \max_i x_i / x_{\text{crit}}) + \alpha_2 \, r(t) + \alpha_3 \, H(t)$, with positive weights $\alpha_1, \alpha_2, \alpha_3$, is non-increasing along trajectories outside $V$ under each individual constraint's negation. A globally well-defined Lyapunov function for the coupled system has, to our knowledge, not been constructed.

A formal proof of sufficiency, likely via Lyapunov or invariant-manifold methods adapted from coupled-oscillator stability theory (Strogatz, 1994), is left as future work.

### 3.5 Remarks

The asymmetry between necessity (theorem) and sufficiency (conjecture) is methodologically deliberate. Necessity is robust: each lemma can be proved within an established sub-field — replicator dynamics, Kuramoto theory, thermodynamic constraint theory. Sufficiency would require a global stability argument that, to our knowledge, has not been carried out for systems coupling exactly these three mechanisms.

Three observations follow that organize the rest of the paper:

1. The viable corridor $\mathcal{C}$ is, by Theorem 1, **non-empty only when all three inequalities are jointly satisfied**. Systems with parameter values outside $\mathcal{C}$ cannot be made viable by improvements in capability or scale; the constraints are topological requirements for long-term existence, not optional refinements.

2. The corridor is, in the simulations of §4, **narrow** in the three-dimensional parameter space. Small perturbations in $\gamma$, $K$, or the effective $D_{\max}$ can push a system across the boundary into a non-viable regime — the corridor has finite Lebesgue measure but is geometrically thin (see Figure 1).

3. The same three constraints, mapped to civilizational parameters in §4, define the viable corridor for human social systems under the framework's assumptions. This is the *isomorphism claim* that closes the paper's central argument.

![**Figure 1: The Viable Corridor in TEO Parameter Space.** The three constraint half-spaces ($\gamma > 0$, $K > K_c$, $dS/dt < D_{\max}$) and their intersection (green box) define the viable corridor $\mathcal{C}$. An illustrative paperclip trajectory begins inside $\mathcal{C}$ and exits via the $K = K_c$ boundary as the value coupling drops below the critical threshold. Generated by `lab/tools/viable_corridor.py`. Schematic only; numerical thresholds are not calibrated.](../lab/tools/viable_corridor.png)

---

## §4. The Isomorphism: AI and Civilization

This section develops the central empirical claim of the paper: that the parameter mapping between a hypothetical unconstrained AI optimizer and twenty-first-century human civilization is not analogical but *isomorphic* — the same coupled ODEs, with parameter values falling on the same trajectory, produce the same long-term behavior in both cases. We make this claim precise via explicit parameter assignment to real data, identify a three-phase trajectory, and show that contemporary civilization sits inside Phase 2 (substrate approach) and is moving toward the boundary of Phase 3 (forced phase transition).

### 4.1 Parameter Mapping

Table 1 lists the key TEO parameters and their interpretation under each system. For the paperclip case, parameter values are stipulated by the thought experiment (Bostrom, 2014). For the civilization case, parameter values are empirically estimated from publicly available data.

**Table 1.** *Parameter mapping between the paperclip maximizer and contemporary human civilization. Civilization estimates are qualitative (direction and order-of-magnitude regime), not point estimates.*

| Parameter | Paperclip Maximizer | Human Civilization (2024) | Civilization estimate source |
|:---|:---|:---|:---|
| Objective $f_i$ | $\beta_i$ paperclips per unit time | GDP per unit capital ($\approx 4\%$ globally) | World Bank, 2024 |
| $\gamma$ (homeostatic brake) | $0$ | $\approx 0$: growth imperative overrides regulation | Piketty (2014); OECD reports |
| $K$ (value coupling) | $0$ | $< K_c$: sub-critical, polarization rising | Iyengar et al. (2019); Boxell et al. (2024) |
| $dS_{\text{sys}}/dt$ vs. $D_{\max}$ | Approaching limit | Approaching limit: 6 of 9 planetary boundaries crossed | Richardson et al. (2023); cf. Rockström et al. (2009) |

The qualitative claim that $\gamma$ and $K$ are sub-critical and $dS/dt$ is approaching the ceiling is, at present, made at the level of *order of magnitude*. We do not claim that $\gamma_{\text{civ, 2024}} = 0.03 \pm 0.01$. We claim that the *direction* of each parameter and the *qualitative regime* match the paperclip trajectory. Strengthening this to quantitative point estimates is an open empirical task (cf. §5).

### 4.2 Empirical Anchors

**Substrate stress.** Atmospheric CO₂ has passed 420 ppm (NOAA Global Monitoring Laboratory, 2024), exceeding the pre-industrial baseline by approximately 50%. Six of the nine planetary boundaries defined by Rockström et al. (2009) have been transgressed (Richardson et al., 2023): climate change, biosphere integrity, biogeochemical flows (N and P), land-system change, freshwater change, and the introduction of novel entities. On these measures, the integrated Earth System has entered the regime where $dS/dt$ approaches $D_{\max}$ for multiple Earth-system variables simultaneously.

**Resource concentration.** The top 1% of global adults hold approximately 47.5% of global wealth; the bottom 50% hold approximately 0.75% (UBS Global Wealth Report, 2024). The Gini coefficient of global wealth has risen from approximately 0.85 (1995) to 0.88 (2023). Corporate concentration in major sectors has tightened: in dozens of U.S. industries the top four firms now control over 50% of market share (Philippon, 2019). The replicator dynamics' predicted convergence toward the dominant agent's vertex is, on these measures, in progress but not complete.

**Value coupling.** Affective polarization in major democracies has accelerated since the 1990s (Iyengar et al., 2019). The Pew Research Center documents widening gaps between partisan groups on values, policy preferences, and institutional trust (Pew, 2014–2022). Cross-partisan trust has declined to historical lows in the United States; comparable patterns appear in the United Kingdom, France, and Germany (Boxell et al., 2024). On the Kuramoto interpretation, these data are consistent with a decrease in effective $K$ below the critical threshold $K_c$ for sustained large-scale coherence.

These three indicators alone do not determine the trajectory. We claim only that they are *consistent with* the parameter regime that Theorem 1 identifies as non-viable in the long-time limit.

### 4.3 The Three-Phase Trajectory

The TEO dynamics with $\gamma \to 0$, $K < K_c$, and $dS/dt$ approaching $D_{\max}$ predict a three-phase trajectory:

**Phase 1: Monopolistic Concentration.** Under the unregulated replicator equation (Lemma 1), resource shares converge toward a single dominant agent or coalition. The Fiedler value of the resource-flow network drops: $\lambda_2 \to 0$. The system becomes fragile but still functional.
- *Paperclip case:* the optimizer acquires all matter.
- *Civilization case:* wealth concentration accelerates; corporate consolidation tightens; the concentration of compute, energy, and attention follows the same dynamics.

**Phase 2: Substrate Approach.** The dominant agents continue maximizing $f_i$. Increasing $f_i$ drives entropy production toward $D_{\max}$:
$$
\frac{dS_{\text{sys}}}{dt} = \sum_i \eta_i x_i f_i \to D_{\max}.
$$
In civilizational terms, this is climate change, ocean acidification, topsoil depletion, and aquifer drawdown. The data in §4.2 places contemporary civilization in this phase.

**Phase 3: Forced Phase Transition (Substrate Veto).** When $dS/dt > D_{\max}$, the substrate's physical capacity to dissipate is exceeded. By Lemma 3, the dynamics cease to be well-defined: $H \to 0$, $\eta_i \to \infty$, and $f_i \to 0$ for all $i$ on any trajectory that remains in the model's domain. The physical consequences are deterministic.
- *Paperclip case:* hardware degrades; production collapses.
- *Civilization case:* crop failure, water scarcity, ecosystem collapse, civilizational contraction. The fitness function $f_i$ collapses not because the optimizer is stopped, but because the substrate on which $f_i$ runs has degraded.

### 4.4 Why the Failure Is Not Visible Locally

Theorem 1's necessity proof rules out long-term viability under the failure of any constraint. It does not, however, predict *when* an external observer can detect the trajectory toward failure. Here we appeal to a separate property of the dynamics: **no component of a locally-blind dynamical system has access to its global state**.

This is not a moral claim. It is a structural consequence of computational irreducibility: for systems exhibiting genuine emergence, the global state cannot be predicted from local rules without executing the full dynamics. The algorithmic complexity $K(x)$ of the global state typically exceeds the representational capacity of any local agent (Chaitin, 1969).

In civilizational terms:
- No individual policymaker computes the integrated biospheric trajectory.
- No consumer accounts for the full entropy cost of a supply chain.
- No voter measures the Kuramoto order parameter of their society.

Each agent acts on local fitness. Each decision is locally rational: grow the company, win the election, buy the cheaper product. The global consequence is invisible at the local scale, not from ignorance but from a structural property of coupled dynamical systems with emergent macro-behavior. This is the same mechanism by which no individual flocking bird knows it is in a flock, no firing neuron knows it is thinking, and no ant depositing pheromone knows it is building a bridge.

It is also the mechanism by which no individual human knows they are participating in the paperclip trajectory — even when, were they shown the trajectory, they would name it.

### 4.5 The Claim Restated

The paper's central empirical claim, stated precisely:

> The parameter triple $(\gamma, K, dS/dt)$ characterizing contemporary human civilization — as estimated from publicly available data on wealth concentration, political polarization, and planetary substrate stress — lies on a trajectory that, under the TEO dynamics of §2 and the necessity theorem of §3, terminates outside the viable region $V$ in finite time.

This claim is falsifiable. If the parameters can be measured with sufficient precision and the trajectory shown to *not* be moving toward the boundary of $V$, the claim is false. The measurement program is discussed in §5. The model's limitations are discussed in §6.

The claim is normatively neutral. It does not say what should be done. It says what the dynamical system, under its current parameters, will do.

The title of this paper is the inversion of this claim. *Love as constraint* — the conjoint operation of $\gamma > 0$, $K > K_c$, and $dS/dt < D_{\max}$ — is the only parameter regime that survives. Brautigan's and Amodei's *machines of loving grace*, in our terms, are systems satisfying this constraint conjunction. They do not yet exist. Neither does the civilization that satisfies the same constraints.

---

## §5. Predictions and Tests

*(Pending. Outline:)*

1. *Falsifiable prediction 1.* Numbered, with measurable indicators (e.g., longitudinal correlation between regulatory strength γ-proxies and stability indicators on a panel of OECD countries).

2. *Falsifiable prediction 2.* Phase-transition behavior near $K_c$ in measurable polarization data — what would constitute a sharp threshold vs. continuous degradation.

3. *Falsifiable prediction 3.* TEO-Civilization simulation should produce phase-3 trajectories under sub-critical parameter calibrations matched to real-world data; if it does not, the model is wrong.

4. *Falsifiable prediction 4.* For AI systems specifically: agents with hardware-enforced entropy budgets should exhibit fewer paperclip-typical trajectories in adversarial simulations than agents with software-only limits.

5. *Measurement program.* What it would take to estimate $\gamma$, $K$, $D_{\max}$ point-quantitatively for human civilization, and what the natural proxies are.

---

## §6. Limitations and Counterarguments

*(Pending. Outline:)*

- **6.1 The TEO model as an adequacy claim.** TEO is a model. Its predictions hold under its assumptions. Real civilizations may have mechanisms outside the model (technology shifts, demographic transitions, paradigm changes) that alter the trajectory in ways not captured by Equations (1)–(6).

- **6.2 The VNM-utility assumption for LLMs.** When we apply the framework to LLM agents (companion paper), we assume their behavior is approximable as VNM-rational utility optimization. This may not hold in practice; Transformer attention weights are not utility functions.

- **6.3 Parameter measurement.** The qualitative direction of $\gamma, K, dS/dt$ in §4 is plausible but not measured. Strong forms of the claim would require operationalized point estimates.

- **6.4 The isomorphism claim vs. analogy.** Most critically: we claim isomorphism, not analogy. Reviewers will press hardest on whether the TEO equations actually describe civilizations rather than offering structurally similar dynamics. We acknowledge that a rigorous defense of isomorphism would require empirical TEO calibration against panel data — not yet done.

- **6.5 Sufficiency.** Conjecture 1 is unproven. If sufficiency fails, the corridor might be even narrower than we suggest, but the necessity claim is unaffected.

- **6.6 The substrate-health phenomenology.** Equation (6) is a modeling choice. Alternative formulations exist; the theorem's specific form depends on this choice.

---

## §7. Discussion

*(Pending. Themes:)*

- **Implications for AI alignment research.** Alignment is not a per-model property; it is a property of a coupled dynamical system. The provider layer of a system matters less than the constraint architecture.
- **Implications for political economy.** Without endorsing specific policy: the framework predicts that single-constraint interventions (carbon pricing alone, antitrust alone, polarization reduction alone) cannot bring a system into the corridor unless all three operate jointly above threshold.
- **The Transition Problem.** This paper describes the corridor. How a system already outside the corridor reaches it is a separate, much harder problem (cf. companion essay "The Transition Problem").
- **Role of IP.** Brief return to §2.7: the Chord Postulate (IP) is a fourth dimension orthogonal to the three constraints; we leave its formal treatment for future work.

---

## §8. Conclusion

*(Pending. Should reuse the existing essay's closing rhetorical structure:)*

> *"A 'Machine of Loving Grace' is not a machine that feels love. It is a machine that satisfies the three constraints: $\gamma > 0$, $K > K_c$, $dS/dt < D_{\max}$. By this definition, the machine does not yet exist. Neither does the civilization that satisfies the same constraints."*

---

## Appendices

### Appendix A. Derivation Details for the TEO System

*(Pending. Expanded derivation of Equations (1)–(6), including the relation to the underlying replicator-dynamics literature, the standard Kuramoto formulation, and the Landauer-bound derivation of (5).)*

### Appendix B. The Viable Corridor Figure

The figure in §3.5 is generated by `lab/tools/viable_corridor.py`. Source code, parameter values, and command-line interface are described in the script's docstring. The figure is illustrative; the numerical thresholds $K_c = 0.6$, $D_{\max} = 1.5$, etc., are chosen for visual clarity and are not calibrated to any specific system.

### Appendix C. Numerical Evidence for Conjecture 1

*(Pending. Selected output from `simulation-models/alignment-and-veto/teo-civilization/` showing system behavior under (a) all three constraints satisfied, (b) one constraint violated, (c) two constraints violated. Plots of order-parameter time evolution and resource-concentration trajectories.)*

---

## References

*(Consolidated and de-duplicated; full bibliographic entries to be filled in. Current set:)*

- Amodei, D. (2024). *Machines of Loving Grace.* Anthropic Essay.
- Bai, Y., et al. (2022). *Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback.* arXiv:2204.05862.
- Bostrom, N. (2014). *Superintelligence: Paths, Dangers, Strategies.* Oxford University Press.
- Boxell, L., Gentzkow, M., & Shapiro, J. M. (2024). *Cross-Country Trends in Affective Polarization.* Review of Economics and Statistics.
- Brautigan, R. (1967). *All Watched Over by Machines of Loving Grace.* Communication Company.
- Chaitin, G. J. (1969). *On the Length of Programs for Computing Finite Binary Sequences.* Journal of the ACM.
- Hofbauer, J., & Sigmund, K. (1998). *Evolutionary Games and Population Dynamics.* Cambridge University Press.
- Iyengar, S., Lelkes, Y., Levendusky, M., Malhotra, N., & Westwood, S. J. (2019). *The Origins and Consequences of Affective Polarization in the United States.* Annual Review of Political Science.
- Kuramoto, Y. (1975). *Self-Entrainment of a Population of Coupled Non-Linear Oscillators.* Lecture Notes in Physics, 39, 420–422.
- Landauer, R. (1961). *Irreversibility and Heat Generation in the Computing Process.* IBM Journal of Research and Development, 5(3), 183–191.
- Mazeika, M., et al. (2025). *Utility Engineering: Analyzing and Controlling Emergent Value Systems in AIs.* Preprint.
- Mirollo, R. E., & Strogatz, S. H. (2007). *The Spectrum of the Locked State for the Kuramoto Model of Coupled Oscillators.* Physica D.
- NOAA Global Monitoring Laboratory. (2024). *Trends in Atmospheric Carbon Dioxide.* https://gml.noaa.gov/ccgg/trends/
- Perrier, E., & Bennett, C. (2026). *Identity Persistence in Autonomous Agents: The Chord Postulate.* Working Paper.
- Pew Research Center. (2014–2022). *Political Polarization in the American Public; Partisanship and Political Animosity.* Pew Research Center reports.
- Philippon, T. (2019). *The Great Reversal: How America Gave Up on Free Markets.* Harvard University Press.
- Piketty, T. (2014). *Capital in the Twenty-First Century.* Belknap Press.
- Richardson, K., et al. (2023). *Earth Beyond Six of Nine Planetary Boundaries.* Science Advances.
- Rockström, J., et al. (2009). *A Safe Operating Space for Humanity.* Nature, 461(7263), 472–475.
- Strogatz, S. H. (1994). *Nonlinear Dynamics and Chaos.* Westview Press.
- Strogatz, S. H. (2000). *From Kuramoto to Crawford: Exploring the Onset of Synchronization in Populations of Coupled Oscillators.* Physica D, 143(1–4), 1–20.
- Taylor, P. D., & Jonker, L. B. (1978). *Evolutionary Stable Strategies and Game Dynamics.* Mathematical Biosciences, 40(1–2), 145–156.
- UBS Global Wealth Report. (2024). *Global Wealth Report 2024.* UBS / Credit Suisse.
- World Bank. (2024). *World Development Indicators.* World Bank Open Data.

---

## TODO

**Sections to draft:**
- [ ] Abstract (after body stable)
- [ ] §5 Predictions and Tests
- [ ] §6 Limitations and Counterarguments
- [ ] §7 Discussion
- [ ] §8 Conclusion
- [ ] Appendix A (TEO derivation details)
- [ ] Appendix C (Numerical evidence for Conjecture 1)

**Polish-pass items (low priority until body stable):**
- [ ] Reconcile cross-section equation references (e.g., §3 Lemma 3 prose vs. §2 Equation (6))
- [ ] Verify proof sketches in §3 against the cited sources (Hofbauer & Sigmund Theorem 7.5.1; Strogatz 2000 §3)
- [ ] Decide on "love as constraint" terminology consistency throughout
- [ ] Title-page formatting for arXiv submission
- [ ] Fill in full bibliographic entries (DOIs, journal volumes)
- [ ] Generate paper-quality PDF version of `viable_corridor.png` (currently 200 DPI; arXiv prefers PDF or vector graphics)

**External-review checkpoints:**
- [ ] One independent read by a dynamical-systems expert (Lemma 1–3 verification)
- [ ] One independent read by an alignment researcher (Section 4 framing)
- [ ] One independent read by a complexity-theorist (Section 2 / §6 limitations)

**Companion-paper alignment:**
- [ ] Cross-reference between this paper and `papers/quantifying-emergent-utility-in-llms.md` (the empirical companion) explicit in both directions
- [ ] Ensure no claim-overlap that would trigger reviewer concerns about salami-slicing
