---
title: "The Viable Corridor: A Three-Constraint Theorem for Survivable Multi-Agent Optimization"
author: "Frank Peterlein"
affiliation: "Independent Researcher, Berlin"
correspondence: "GitHub Issues / frnkptrln"
date: "2026 (working draft)"
status: "DRAFT — sections §1–§4 reviewed and revised; §5–§8 and appendices pending"
version: "0.2"
relation_to_other_paper: >
  This is the conceptual companion paper to
  `papers/quantifying-emergent-utility-in-llms.md`, which will be revised
  as the empirical paper after the Agentic Identity Suite is run in real
  mode. The two papers cite each other; this paper establishes the
  theoretical frame, the companion paper provides the empirical evidence.
relation_to_essay_and_internal_note: >
  Two precursor documents in the repository state related arguments at
  different levels of formality. The synthesis essay at
  `theory/narrative/machines-of-loving-grace.md` is the literary
  statement of the central thesis (the rhetorical voice, the
  Brautigan/Amodei framing). The internal theory note at
  `theory/teo-framework/love-as-constraint.md` is the earlier
  formal sketch of the three-constraint conjunction. Both remain
  in place; this paper subsumes their mathematical core into a single
  academic-format document with proof, predictions, and limitations.
target_venue: "arXiv (cs.CY primary; cs.MA, nlin.AO cross-listed)"
target_length: "12–15 pages typeset"
---

# The Viable Corridor

*A Three-Constraint Theorem for Survivable Multi-Agent Optimization*

**Frank Peterlein** · Independent Researcher, Berlin
*Correspondence: [GitHub Issues / frnkptrln](https://github.com/frnkptrln/systems-and-intelligence/issues)*

---

> **Status:** working draft, version 0.2.
> Sections §1–§4 are drafted and have completed one reviewer pass; §5 (Predictions), §6 (Limitations), §7 (Discussion), and §8 (Conclusion) are pending. The central figure (Viable Corridor) is implemented at `lab/tools/viable_corridor.py`. References are consolidated at the end; full bibliographic entries are pending. **This document is not yet submission-ready.**

### Revision history

- **v0.1** — Initial draft of §1–§4 and Figure 1.
- **v0.2** — Twelve-point structural revision following an internal reviewer pass. Tone in §1 calibrated down to match what §3 actually proves. Homeostatic brake in §2.4 reformulated to preserve the simplex. Substrate-health variable $H$ coupled back into Equation (1) so that substrate collapse halts the dynamics. Viability redefined as **robust viability** (open-set invariance) in §3.1. Theorem 1 scope clarified to the thermodynamic limit. Lemma 1 strengthened to require strict dominance. Lemma 2 explicit about all-to-all coupling and frequency-distribution assumptions. Lemma 3 corrected from `ess sup` to **accumulated overshoot**. §3.4 "Lyapunov candidate" renamed to **viability margin** (no monotonicity claim). §4.1 table reframed as a **heuristic regime mapping**, not a calibrated estimation. §4.4 citation fixed (Wolfram for computational irreducibility, not Chaitin). §4.5 final claim softened from "estimated trajectory" to "proxies consistent with". §2.7 IP note moved to §7 as future work.

---

## Abstract

*(To be drafted after §5–§8 are complete. The abstract should compress the paper's claim into ≈200 words: TEO framework, the three-constraint theorem, the AI/civilization isomorphism, and the falsifiable predictions. Draft after the body is stable.)*

---

## §1. Introduction

Richard Brautigan (1967) imagined "machines of loving grace" — technology that serves life rather than consuming it. Dario Amodei (2024) adopted the phrase to describe a future in which artificial intelligence amplifies human flourishing. In both cases, *loving grace* names a design aspiration: a hopeful image of what a successful relationship between intelligence and its substrate might look like.

This paper develops a related but more constrained reading. Under a specific dynamical-systems framework — the Thermodynamics of Emergent Orchestration (TEO) — we model the relationship Brautigan and Amodei imagine as a **survival constraint within the model**, not merely a design aspiration. We identify three conjoint mathematical conditions on the model's parameters and prove that their simultaneous satisfaction is *necessary* for robust long-time viability of any coupled multi-agent optimizing system that the model describes.

The argument runs on two parallel observations.

The first is the paperclip maximizer (Bostrom, 2014): a hypothetical AI optimizer that, given a single unconstrained objective, consumes its environment — including its creators — to achieve that objective. The horror of the paperclip maximizer is its indifference: it does not hate humanity; it simply does not include humanity in its objective function. As alignment problems escalate with model capability, this thought experiment has become a load-bearing analogy in safety research.

The second is the trajectory of human civilization as a coupled system under sustained pressure for unbounded throughput. Atmospheric CO₂ has passed 420 ppm (NOAA, 2024). The top 1% of global wealth-holders controls more wealth than the bottom 50% (UBS Global Wealth Report, 2024). Affective political polarization has accelerated across most major democracies over the past two decades (Iyengar et al., 2019; Boxell et al., 2024). These trends are typically modeled as distinct phenomena — climate here, inequality there, polarization elsewhere — and addressed through separate policy interventions.

We advance a **structural-isomorphism hypothesis**: that both systems can be represented by the same stylized coupled-dynamics model, with parameter values that map onto similar trajectories. We are explicit that this is a hypothesis to be tested empirically, not an established equivalence. The mapping in §4 is a heuristic regime assignment, not a calibration; what the model would need in order to graduate the hypothesis into a measured isomorphism is discussed in §5 and §6.

**Thesis.** Within the TEO framework, the long-time behavior of any coupled optimizing system the model describes depends on three parameters: a homeostatic regulation strength $\gamma$, a value-coupling strength $K$ between agents, and an entropy production rate $dS/dt$ bounded by the substrate's dissipation capacity $D_{\max}$. We claim:

1. The conjunction of three constraints — $\gamma > 0$, $K > K_c$, and $dS/dt < D_{\max}$ — is **necessary** for robust long-time viability (Theorem 1, §3). Sufficiency is stated as a conjecture (Conjecture 1, §3.4) supported by partial numerical evidence; we do not prove it.
2. The same parameter mapping is *hypothesized* to apply, at the level of qualitative regime, to both a stylized paperclip-style AI optimizer and to twenty-first-century human civilization. This is a structural-isomorphism *hypothesis*, not an established equivalence.
3. Under the model, the trajectory of unconstrained optimization in both cases passes through three identifiable phases: monopolistic concentration, substrate approach, and substrate-driven termination. The mapping of contemporary civilizational data to these phases is interpretive, not measured.

We refer to the three-constraint parameter regime as the **viable corridor**. The conjunction of constraints — operational caring about the substrate, value alignment between agents, and physical limits — is given the *operational* name *love as constraint*. We use the phrase operationally, not psychologically: it denotes the conjunction of three constraints in the model.

**Why this reframing matters.** Contemporary AI alignment research has concentrated on local interventions: refinements to reinforcement learning from human feedback (RLHF), refusal training, system prompts, and interpretability tools (Mazeika et al., 2025; Bai et al., 2022). These are valuable. But they treat alignment as a property of individual models, evaluated through behavioral benchmarks. Under the framework presented here, this is structurally insufficient: alignment is not a property of an isolated optimizer. It is a property of a coupled dynamical system. The same insufficiency applies to political and economic governance frameworks that treat individual constraints — carbon pricing here, antitrust law there, polarization mitigation elsewhere — as separately optimizable variables rather than as conjoint requirements for any system's long-term viability.

The reframing is therefore not only about AI. It is about what counts as a control problem.

**Paper structure.** Section 2 introduces the TEO framework formally — the coupled replicator-Kuramoto-entropy dynamics that generate the three parameters. Section 3 states and argues for the Three-Constraint Theorem: that the conjunction $\gamma > 0$, $K > K_c$, $dS/dt < D_{\max}$ is necessary for survival in the long-time limit. Section 4 develops the isomorphism between AI optimization and civilizational dynamics through explicit parameter mapping and empirical anchors. Section 5 derives falsifiable predictions and identifies the empirical commitments the framework makes. Section 6 presents limitations and the strongest counterarguments. Section 7 discusses implications, with explicit attention to what the framework does and does not justify.

Throughout, we tag claims with their epistemic status:

- **Formal result** (`[FORMAL]`): proved as theorem or lemma under stated assumptions.
- **Conjecture** (`[CONJECTURE]`): plausible and partially supported by numerical or structural evidence, but unproved.
- **Model assumption** (`[MODEL ASSUMPTION]`): a choice in the model that shapes the result; alternatives exist.
- **Heuristic mapping** (`[HEURISTIC]`): a regime assignment or proxy correspondence, not a calibrated measurement.
- **Empirical conjecture** (`[EMPIRICAL CONJECTURE]`): an empirically testable claim that the model suggests but that this paper does not establish.

The framework is meant to be falsifiable. The thesis that the model represents civilizational dynamics in the way we hypothesize is uncomfortable and important enough that we have tried to state it with the precision needed for it to be checked — and, where possible, found wrong.

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

For the theorem of §3 we adopt a **strict-dominance** assumption on $f_i^{(0)}$ (the substrate-unmodified fitness from §2.5). There exists an agent index $i^*$ and a constant $\delta > 0$ such that, for all $j \neq i^*$ and all $\mathbf{x}$ on the simplex,
$$
f_{i^*}^{(0)}(\mathbf{x}) - f_j^{(0)}(\mathbf{x}) \geq \delta.
\tag{1'}
$$
[`[MODEL ASSUMPTION]`]. This is stronger than a $\beta$-dominance condition alone and is the operational form of Bostrom's (2014) *instrumental convergence*: agent $i^*$ has a structural fitness advantage over every other agent at every state of the system. Whether real social and economic systems exhibit such strict dominance is an empirical question (cf. Piketty, 2014, on power-law concentration in resource flows); we treat it here as a model assumption used in §3.

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

The brake $\mathcal{H}_i$ in Equation (1) must preserve the simplex constraint $\sum_i x_i = 1$. A pure penalty term $-\gamma \max(0, x_i - x_{\text{crit}})$ removes mass from above-threshold agents but does not return it elsewhere, breaking simplex invariance. We therefore define the brake as a redistribution:
$$
\mathcal{H}_i(\mathbf{x}) = -\gamma \cdot \max\bigl(0, \, x_i - x_{\text{crit}}\bigr) + \frac{\gamma}{N} \sum_{j=1}^N \max\bigl(0, \, x_j - x_{\text{crit}}\bigr),
\tag{4}
$$
where $\gamma \geq 0$ is the regulatory strength and $x_{\text{crit}} \in (1/N, 1)$ is a critical share threshold. The first term penalises any agent whose share exceeds $x_{\text{crit}}$; the second term distributes the aggregate penalty uniformly across all agents. By construction $\sum_i \mathcal{H}_i(\mathbf{x}) = 0$, so the simplex is preserved.

Interpretation: $\gamma$ encodes the operational strength of *any* homeostatic mechanism that resists unbounded concentration — antitrust law, progressive taxation, redistribution, capability throttling, kill switches, refusal channels. The parameter $\gamma = 0$ corresponds to fully unregulated optimization. The form (4) is one of several simplex-preserving redistributions; alternatives (e.g. redistribution only to below-threshold agents, or weighted by inverse share) yield qualitatively similar dynamics and are discussed in §6 [`[MODEL ASSUMPTION]`].

### 2.5 The Entropy Budget and Substrate Coupling

Computation produces entropy; Landauer (1961) gives a lower bound on the heat dissipated by irreversible bit erasure. Equation (5) is **not** a generalised Landauer bound. It is a **phenomenological dissipation proxy** motivated by Landauer-type physical limits: we assume that the rate of entropy production by agent $i$ scales with its resource share and its activity level [`[MODEL ASSUMPTION]`]:
$$
\frac{dS_{\text{sys}}}{dt} = \sum_{i=1}^N \eta_i \, x_i \, f_i(\mathbf{x}, H),
\tag{5}
$$
where $\eta_i > 0$ is agent $i$'s entropy coefficient. We write $f_i(\mathbf{x}, H)$ to make the substrate-dependence explicit (see below).

The substrate hosting the dynamics has a finite dissipation capacity $D_{\max} > 0$. The substrate-health variable $H(t) \in [0, 1]$ evolves according to:
$$
\frac{dH}{dt} = -\frac{1}{S_{\max}} \, \max\!\left( 0, \, \frac{dS_{\text{sys}}}{dt} - D_{\max} \right),
\tag{6}
$$
with $H(0) = 1$ and $S_{\max} > 0$ the substrate's total dissipative reservoir. Equation (6) is phenomenological [`[MODEL ASSUMPTION]`]: sustained over-dissipation degrades the substrate, with degradation accumulating in proportion to the excess.

**Substrate coupling.** We close the loop by making fitness depend on substrate health:
$$
f_i(\mathbf{x}, H) = H \cdot f_i^{(0)}(\mathbf{x}),
\tag{5'}
$$
where $f_i^{(0)}$ is the substrate-unmodified fitness. Equation (5') ensures that as $H \to 0$, all fitness vanishes and Equations (1)–(2) freeze: the resource-replicator drift goes to zero and the value-coupling dynamics continue only on previously assigned shares. Without this coupling, the dynamics would remain formally defined even at $H = 0$, contradicting the physical interpretation of substrate collapse.

In the planetary-substrate interpretation, $H$ corresponds to an integrated overshoot of the safe operating space defined by Rockström et al. (2009).

### 2.6 The Coupled System and Three Failure Modes

Together, Equations (1)–(6) define the TEO dynamics. Three parameters dominate the long-time behavior: the homeostatic strength $\gamma$, the value-coupling strength $K$, and the substrate dissipation capacity $D_{\max}$.

Each parameter admits one independent failure mode, made formal in §3:

1. **Monopolistic concentration** ($\gamma = 0$). Without the homeostatic brake, Equation (1) reduces to the unregulated replicator equation. Under the strict-dominance assumption (1'), the system converges from any interior initial condition to the vertex of agent $i^*$: $x_{i^*}(t) \to 1$.

2. **Coherence collapse** ($K < K_c$). Below the Kuramoto critical coupling $K_c$ — defined for the thermodynamic limit ($N \to \infty$) of all-to-all coupling with Lorentzian-distributed natural frequencies — the order parameter (3) satisfies $\limsup_{t \to \infty} r(t) = 0$. Agents' value orientations remain phase-uniformly incoherent. (We use "coherence collapse" rather than "polarization" because $r \to 0$ describes loss of any global phase, not specifically two-cluster antagonism.)

3. **Substrate veto** (accumulated overshoot $\int_0^t (\dot{S}_{\text{sys}} - D_{\max})_+ \, ds \geq S_{\max}$ for some finite $t$). When the integrated overshoot of $D_{\max}$ exceeds the substrate's total reservoir, Equation (6) drives $H$ to zero in finite time. Through Equation (5'), $f_i \to 0$ and the dynamics freeze.

The central observation of this paper, made precise in §3, is that **the conjoint avoidance of all three failure modes is necessary for robust long-time viability**. The parameter regime $\gamma > 0 \,\wedge\, K > K_c \,\wedge\, dS_{\text{sys}}/dt < D_{\max}$ (with the third interpreted as an accumulated-overshoot condition, see §3.3) defines the **viable corridor** analyzed in the remainder of the paper.

---

## §3. The Three-Constraint Theorem

This section formalises the central claim of the paper: the conjunction of $\gamma > 0$, $K > K_c$, and $\frac{dS_{\text{sys}}}{dt} < D_{\max}$ is necessary for the TEO dynamics to admit *robust* long-time viability. We prove necessity under stated assumptions (Theorem 1) and state sufficiency as a conjecture (Conjecture 1) supported by partial numerical evidence.

### 3.1 The Viable Region and Robust Viability

Let $\Sigma$ denote the state space of the TEO system: the simplex $\{\mathbf{x} \in \mathbb{R}^N_{\geq 0} : \sum_i x_i = 1\}$ combined with the $N$-torus $[0, 2\pi)^N$ for value orientations, augmented by the substrate-health variable $H \in [0, 1]$ from §2.5.

We define the **viable region** $V \subset \Sigma$ as the set of states satisfying three conditions simultaneously:

- **(V1) Pluralism**: $\max_i x_i \leq x_{\text{crit}}$ — no agent's share exceeds the critical threshold $x_{\text{crit}} \in (1/N, 1)$.
- **(V2) Coherence**: $r(t) \geq r_{\min} > 0$ — the Kuramoto order parameter from Equation (3) is bounded away from zero.
- **(V3) Capacity**: $\frac{dS_{\text{sys}}}{dt} \leq D_{\max} - \epsilon$ for some $\epsilon > 0$ — entropy production is bounded strictly below the substrate's dissipation ceiling.

We use the term **robust viability** rather than "viability of some trajectory". An existential definition — "there exists at least one trajectory starting in $V$ that remains in $V$" — is too weak for the necessity claims that follow, because measure-zero symmetric equilibria can satisfy it even under failed constraints. We therefore define [`[FORMAL]`]:

> A parameter triple $(\gamma, K, D_{\max})$ admits **robust viability** if there exists a non-empty open subset $U \subseteq V$ such that for every initial condition $(\mathbf{x}_0, \boldsymbol{\theta}_0, H_0 = 1) \in U$, the resulting trajectory $(\mathbf{x}(t), \boldsymbol{\theta}(t), H(t))$ remains in $V$ for all $t \geq 0$.

This is the standard open-set / positive-invariance notion of viability used in dynamical systems and viability theory (Aubin, 1991).

### 3.2 The Viable Corridor in Parameter Space

In the parameter space $(\gamma, K, D_{\max}) \in \mathbb{R}^3_{\geq 0}$, define the **viable corridor** $\mathcal{C}$ as the set of parameter triples admitting robust viability:
$$
\mathcal{C} = \left\{(\gamma, K, D_{\max}) : (\gamma, K, D_{\max}) \text{ admits robust viability per §3.1}\right\}.
\tag{7}
$$

The central necessity claim of this paper is that the three inequalities $\gamma > 0$, $K > K_c$, $dS_{\text{sys}}/dt < D_{\max}$ are **necessary boundary conditions** on $\mathcal{C}$ — that is, $\mathcal{C}$ is contained in the open region they define. Whether they are also sufficient is the content of Conjecture 1.

### 3.3 Theorem 1 (Necessity)

We state Theorem 1 in the thermodynamic limit ($N \to \infty$) under explicit assumptions matching each lemma's scope. Finite-$N$ versions hold in a probabilistic, fluctuation-bounded sense; we comment on these after the proof.

**Theorem 1 (Necessity of the three constraints).** *Let the TEO system (Equations 1, 1', 2, 3, 4, 5, 5', 6) be defined for an $N \to \infty$ population of agents with all-to-all coupling ($A_{ij} = 1$ for all $i \neq j$), with natural frequencies $\omega_i$ drawn i.i.d. from a unimodal symmetric density of finite second moment (e.g.\ Lorentzian with half-width $\Delta$), with the strict-dominance fitness assumption (1') applied to $f_i^{(0)}$, and with the substrate coupling (5'). Then a parameter triple $(\gamma, K, D_{\max})$ admits robust viability (in the sense of §3.1) only if all three of the following hold:*
$$
\gamma > 0, \quad K > K_c(\{\omega_i\}), \quad \int_0^t \!\bigl(\dot{S}_{\text{sys}}(s) - D_{\max}\bigr)_+ \, ds < S_{\max} \ \text{ for all } t \geq 0.
\tag{8}
$$

The proof proceeds via three independent lemmas, each demonstrating one failure mode under the negation of one constraint.

---

**Lemma 1 (Resource Concentration).** *Assume $\gamma = 0$ and the strict-dominance condition (1') with constant $\delta > 0$. Then for every interior initial condition $\mathbf{x}_0 \in \mathrm{int}(\Delta^{N-1})$, the trajectory of (1) satisfies $x_{i^*}(t) \to 1$ and $x_j(t) \to 0$ for all $j \neq i^*$ as $t \to \infty$. Equivalently, (V1) is violated asymptotically from every interior initial condition.*

*Proof sketch.* With $\mathcal{H}_i \equiv 0$, Equation (1) is the classical replicator equation $\dot{x}_i = x_i(f_i^{(0)}(\mathbf{x}) - \bar{\phi}(\mathbf{x}))$. Strict dominance (1') states that $f_{i^*}^{(0)}(\mathbf{x}) - f_j^{(0)}(\mathbf{x}) \geq \delta > 0$ for all $j \neq i^*$ and all $\mathbf{x}$ on the simplex. By standard results on replicator dynamics with a strictly dominant strategy (Hofbauer & Sigmund, 1998, §7.2–7.3), $i^*$'s share is monotone non-decreasing: $\dot{x}_{i^*} = x_{i^*}(f_{i^*}^{(0)} - \bar{\phi}) \geq x_{i^*} \cdot (1 - x_{i^*}) \cdot \delta$, which is strictly positive on $\mathrm{int}(\Delta^{N-1})$ until $x_{i^*} = 1$. Therefore $x_{i^*}(t) \to 1$ from every interior initial condition. The vertex $e_{i^*}$ lies outside $V$ (V1 violated by definition for $x_{\text{crit}} < 1$), so every interior trajectory exits $V$ in finite time. This rules out robust viability: there is no open subset $U \subseteq V$ of interior initial conditions whose trajectories remain in $V$. $\square$

*Remark.* Without strict dominance — for example, with $\beta$-dominance alone but unbounded $g_i$ — replicator dynamics can sustain mixed equilibria, cycles, or chaotic attractors. The lemma's strength comes from (1'), which is a substantive model assumption (cf. §6 on its empirical defensibility).

---

**Lemma 2 (Coherence Collapse).** *Under all-to-all coupling ($A_{ij} = 1$), i.i.d.\ natural frequencies $\omega_i$ drawn from a unimodal symmetric density $g(\omega)$ with finite second moment, and incoherent initial phase distribution, in the thermodynamic limit $N \to \infty$ the Kuramoto order parameter satisfies*
$$
\lim_{t \to \infty} r(t) = 0 \quad \text{whenever} \quad K < K_c, \quad \text{where } K_c = \frac{2}{\pi g(0)}.
$$

*Proof sketch.* This is the classical Kuramoto (1975) onset result, made rigorous in the thermodynamic limit by Mirollo and Strogatz (1991) and reviewed in Strogatz (2000) and Acebrón et al. (2005). Below $K_c$, the self-consistency equation $r = K \int \cos(\theta_\omega(\infty)) \, g(\omega) \, d\omega$ admits only the trivial solution $r = 0$ on the incoherent manifold; small perturbations decay rather than grow. For the Lorentzian density $g(\omega) = (\Delta / \pi)/(\omega^2 + \Delta^2)$ this reduces to $K_c = 2\Delta$. The result (V2 violated asymptotically) rules out robust viability when $K < K_c$. $\square$

*Remark.* For finite $N$ and general connected adjacency matrices $A_{ij}$, there is no sharp threshold of this exact form: the critical coupling depends on the spectrum of $A_{ij}$ and on finite-size fluctuations of order $N^{-1/2}$ (Strogatz, 2000, §3; Restrepo, Ott & Hunt, 2005). The thermodynamic-limit statement is the cleanest available; the finite-$N$ extension is discussed in §6 as a model-assumption.

---

**Lemma 3 (Substrate Veto via Accumulated Overshoot).** *If there exists a finite time $t^* > 0$ such that the accumulated overshoot satisfies*
$$
\int_0^{t^*} \bigl(\dot{S}_{\text{sys}}(s) - D_{\max}\bigr)_+ \, ds \geq S_{\max},
$$
*then $H(t^*) \leq 0$, and through the substrate coupling (5') we have $f_i(\mathbf{x}(t^*), H(t^*)) = 0$ for all $i$, halting both the replicator dynamics (1) and the entropy production (5).*

*Proof sketch.* From Equation (6),
$$
H(t) = 1 - \frac{1}{S_{\max}} \int_0^t \bigl(\dot{S}_{\text{sys}}(s) - D_{\max}\bigr)_+ \, ds.
$$
The accumulated-overshoot hypothesis implies $H(t^*) \leq 0$. We extend the definition of $H$ to be clipped at zero: $H \geq 0$ throughout. By (5'), $f_i(\mathbf{x}, H) = H \cdot f_i^{(0)}(\mathbf{x})$, so $H = 0$ forces $f_i \equiv 0$. The replicator drift $x_i(f_i - \bar{\phi})$ then vanishes, the entropy production (5) vanishes, and the coupled trajectory remains frozen at the state reached at $t^*$. (V3 was already violated for some $\tau < t^*$ by hypothesis; once $H = 0$, the trajectory cannot recover.) Robust viability is therefore impossible. $\square$

*Remark.* This is the **crucial correction** from a naive $\mathrm{ess\,sup}_t \, \dot{S}_{\text{sys}} \geq D_{\max}$ condition. A momentary overshoot does not collapse the substrate; only sustained or repeated overshoot accumulating to at least $S_{\max}$ does. This matches the physical intuition that ecosystems and hardware can tolerate transient stress but not integrated, unrelieved overload.

---

The three lemmas establish that each of the three constraints is **individually necessary** for robust viability under the stated assumptions. Since V1, V2, V3 must hold simultaneously for membership in $V$, the joint necessity of $\gamma > 0$, $K > K_c$, and the accumulated-overshoot bound follows. $\blacksquare$

### 3.4 Conjecture 1 (Sufficiency)

**Conjecture 1 (Sufficiency).** *Under the assumptions of Theorem 1, the conjunction $\gamma > 0$, $K > K_c$, and the accumulated-overshoot bound is also sufficient for robust viability: there exists a non-empty open set $U \subseteq V$ such that every trajectory starting in $U$ remains in $V$ for all $t \geq 0$.* [`[CONJECTURE]`]

We do not prove this conjecture. The obstacle is structural: the three mechanisms are coupled through shared state (resource shares $x_i$ appear in both the replicator and the entropy equations; substrate health $H$ feeds back through (5') into the resource dynamics). We cannot rule out *a priori* coupling-induced failure modes that arise even when all three individual constraints hold — for example, transient excursions of $r(t)$ below $r_{\min}$ during regime shifts in $x_i$, or oscillations in $\dot{S}_{\text{sys}}$ that produce accumulated overshoot episodically.

What we offer in lieu of proof:

1. **Numerical evidence** (Appendix C, *forthcoming*): for representative parameter triples satisfying the three inequalities, the TEO system is expected to exhibit stable long-time behaviour, and the failure modes observed at the corridor boundaries should match those predicted by Lemmas 1–3. *This appendix is pending; until the simulations are run, the numerical-evidence claim is itself a conjecture.*

2. **A candidate viability margin**: define
$$
M(\mathbf{x}, \boldsymbol{\theta}, H) := \alpha_1 \bigl(1 - \tfrac{\max_i x_i}{x_{\text{crit}}}\bigr) + \alpha_2 \, r(t) + \alpha_3 \, H(t),
\quad \alpha_1, \alpha_2, \alpha_3 > 0.
$$
$M$ is **not** a Lyapunov function for the coupled system — $r(t)$ is not generally monotone, and $H(t)$ only decreases under accumulated stress. We call $M$ a **viability margin**: it is positive on $V$, vanishes on the boundary $\partial V$, and tracks how close the trajectory is to violating one or more conditions (V1)–(V3). Whether $M$ admits a true Lyapunov-style construction (e.g.\ a modified $\tilde{M}$ that is monotone along trajectories) is open.

A formal proof of sufficiency, likely via Lyapunov or invariant-manifold methods adapted from coupled-oscillator stability theory (Strogatz, 1994; Aubin, 1991), is left as future work.

### 3.5 Remarks

The asymmetry between necessity (Theorem 1) and sufficiency (Conjecture 1) is methodologically deliberate. Necessity is robust: each lemma can be proved within an established sub-field — replicator dynamics, Kuramoto theory, thermodynamic constraint theory — *under the stated assumptions*. Sufficiency would require a global stability argument that, to our knowledge, has not been carried out for systems coupling exactly these three mechanisms.

Three observations follow:

1. By Theorem 1, **the viable corridor $\mathcal{C}$ is contained in the open region $\{\gamma > 0, K > K_c, \text{accumulated overshoot} < S_{\max}\}$**. Under the model's assumptions, parameter values outside this region cannot support robust viability. The constraints are **necessary model conditions** — not topological invariants of physical reality, but conditions that the dynamical system requires under (1'), all-to-all coupling, and the substrate phenomenology of (6) [`[FORMAL]`, conditional on assumptions].

2. The corridor is, in our schematic visualisation (Figure 1), narrow in the three-dimensional parameter space. Whether the corridor's measure (under any reasonable parameterisation) is actually small for systems of interest is an empirical question discussed in §5.

3. The mapping of the three constraints to civilizational parameters in §4 is the *structural-isomorphism hypothesis* introduced in §1, not an established equivalence. §4 develops it as a heuristic regime assignment.

![**Figure 1: The Viable Corridor in TEO Parameter Space.** The three constraint half-spaces ($\gamma > 0$, $K > K_c$, $dS/dt < D_{\max}$) and their intersection (green box) define the viable corridor $\mathcal{C}$. An illustrative paperclip trajectory begins inside $\mathcal{C}$ and exits via the $K = K_c$ boundary as the value coupling drops below the critical threshold. Generated by `lab/tools/viable_corridor.py`. Schematic only; numerical thresholds are not calibrated.](../lab/tools/viable_corridor.png)

---

## §4. AI and Civilization: A Structural-Isomorphism Hypothesis

This section develops the structural-isomorphism hypothesis introduced in §1: that the parameter regime of a hypothetical unconstrained AI optimizer and that of twenty-first-century human civilization map onto similar trajectories in the TEO framework. **We emphasise that this is a hypothesis to be tested**, not a demonstrated isomorphism. The mapping in §4.1 is a *heuristic regime assignment*, not a calibration; the data in §4.2 are *proxies*, not direct measurements of $\gamma$, $K$, or $D_{\max}$. The §5 measurement programme outlines what would be required to graduate the hypothesis into a measured claim.

### 4.1 Heuristic Regime Mapping

Table 1 is a **heuristic regime assignment** [`[HEURISTIC]`] — a mapping at the level of *direction* and *qualitative regime*, not point estimation. Each civilizational entry should be read as "consistent with the model's failure-mode regime", not as "calibrated value of the parameter". The paperclip entries are stipulated by the thought experiment (Bostrom, 2014). The civilizational entries are proxies whose connection to the TEO parameters is discussed in §4.2 and §6.

**Table 1.** *Heuristic regime mapping between the paperclip maximizer and contemporary human civilization. Civilization entries are qualitative regime indicators, not point estimates of TEO parameters.*

| Parameter | Paperclip Maximizer | Human Civilization (2024) | Civilization regime indicator |
|:---|:---|:---|:---|
| Objective $f_i^{(0)}$ | $\beta_i$ paperclips per unit time | GDP growth as dominant societal optimization target ($\sim$3–4% global, with substantial heterogeneity) | World Bank WDI; Penn World Table |
| $\gamma$ (homeostatic brake) | $0$ (by construction) | $\gamma_{\text{eff}}$ **insufficient or subcritical** relative to concentration dynamics: existing brakes (taxation, antitrust, environmental law) have not prevented rising concentration | Piketty (2014); Philippon (2019); cf. §6 on what "subcritical" means here |
| $K$ (value coupling) | undefined (single agent) or $0$ (population of indifferent copies) | $K_{\text{eff}}$ **declining**, possibly approaching a hypothesised critical regime: cross-partisan trust falling, polarization rising in major democracies | Iyengar et al. (2019); Boxell et al. (2024) |
| Substrate stress vs.\ $D_{\max}$ | trajectory approaching the limit (model output, not stipulated) | Substrate-stress proxies indicate **multiple safe-operating-space boundaries transgressed**; not a direct measurement of $dS/dt$ or $D_{\max}$ | Richardson et al. (2023); Rockström et al. (2009); NOAA (2024) |

The qualitative claim is that the *direction* of each parameter and the *regime* match the trajectory the model predicts as non-viable in the long run. We do *not* claim that $\gamma_{\text{civ, 2024}} = 0.03 \pm 0.01$. We claim that civilizational data, interpreted through the proxies named in §4.2, are *consistent with* the parameter regime that Theorem 1 identifies as non-viable. Strengthening this from regime indication to point estimation, and operationalising what $K_c$ would even mean for real societies, are open empirical tasks taken up in §5.

### 4.2 Empirical Proxies (Not Direct Measurements)

**Substrate-stress proxies.** Atmospheric CO₂ has passed 420 ppm (NOAA Global Monitoring Laboratory, 2024), exceeding the pre-industrial baseline by approximately 50%. Six of the nine planetary boundaries defined by Rockström et al. (2009) have been transgressed (Richardson et al., 2023): climate change, biosphere integrity, biogeochemical flows (N and P), land-system change, freshwater change, and the introduction of novel entities. **These are proxies for substrate stress, not direct measurements of $\dot{S}_{\text{sys}}$ or $D_{\max}$**: the planetary-boundaries framework is a multi-variable safe-operating-space assessment, not a single thermodynamic budget. The mapping to TEO variables is heuristic.

**Resource-concentration proxies.** The top 1% of global adults hold approximately 47.5% of global wealth; the bottom 50% hold approximately 0.75% (UBS Global Wealth Report, 2024). The Gini coefficient of global wealth has risen from approximately 0.85 (1995) to 0.88 (2023). Corporate concentration in major sectors has tightened: in dozens of U.S. industries the top four firms now control over 50% of market share (Philippon, 2019). These trends are *consistent with* a regime in which $\gamma_{\text{eff}}$ is insufficient to prevent concentration; they do not directly measure $\gamma$.

**Value-coupling proxies.** Affective polarization in major democracies has accelerated since the 1990s (Iyengar et al., 2019). The Pew Research Center documents widening gaps between partisan groups on values, policy preferences, and institutional trust (Pew, 2014–2022). Cross-partisan trust has declined to historical lows in the United States; comparable patterns appear in the United Kingdom, France, and Germany (Boxell et al., 2024). On the Kuramoto interpretation, these data are *consistent with* a decline in $K_{\text{eff}}$ toward a hypothesized critical regime; they do not establish that $K < K_c$ for any well-defined $K_c$. Indeed, what $K_c$ would mean for real societies is itself open (§5).

These three sets of proxies do not, jointly or individually, determine the trajectory. We claim only that they are *consistent with* the parameter regime that Theorem 1 identifies as non-viable under the model's assumptions.

### 4.3 The Three-Phase Trajectory (Heuristic Scenario)

Under the structural-isomorphism hypothesis, the model with $\gamma \to 0$, $K < K_c$, and accumulated substrate overshoot generates a three-phase scenario [`[HEURISTIC]`]. We label these phases by their dominant dynamic. The scenario is not derived from the coupled ODEs as a single proof — it is a sequencing of the failure modes proved separately in Lemmas 1–3.

**Phase 1: Monopolistic Concentration.** Under the unregulated replicator equation (Lemma 1), resource shares converge toward the strictly-dominant agent's vertex. The Fiedler value of the resource-flow network drops as concentration tightens. The system becomes fragile but still functional.
- *Paperclip case:* the optimizer acquires all matter.
- *Civilization case (heuristic):* wealth concentration accelerates; corporate consolidation tightens; the concentration of compute, energy, and attention is observed in a regime indicator–consistent way.

**Phase 2: Substrate Approach.** The dominant agents continue maximising $f_i$. Increasing $f_i$ drives entropy production toward $D_{\max}$ via Equation (5).
- *Paperclip case (model output):* the optimizer's computation heats its hardware toward thermal limits.
- *Civilization case (heuristic interpretation):* climate change, ocean acidification, topsoil depletion, aquifer drawdown — these are *possible physical manifestations* under the model's mapping, not deterministic consequences of the model alone.

**Phase 3: Substrate-Driven Termination.** Once accumulated overshoot reaches $S_{\max}$ (Lemma 3), $H \to 0$ and the substrate coupling (5') drives $f_i \to 0$. The dynamics freeze. The physical interpretation depends on the substrate:
- *Paperclip case (model output):* hardware degrades; production collapses.
- *Civilization case (heuristic interpretation):* possible manifestations include crop failure, water scarcity, ecosystem collapse, civilizational contraction. These are *contingent, multi-causal, and uneven* — the model does not predict their specific form or timing, only that, under the hypothesised mapping, substrate-driven dynamics dominate.

### 4.4 Why the Failure Is Not Visible Locally

Theorem 1's necessity proof rules out robust viability under the failure of any constraint. It does not predict *when* an external observer would detect the trajectory toward failure. We appeal here to a separate property of the dynamics: in coupled dynamical systems with emergent macro-behaviour, the global state is typically not computable from local information without executing the full dynamics.

One reason this matters is **computational irreducibility** (Wolfram, 1985, 2002): for many systems of interest, there is no shortcut between the local rules and the global trajectory; the trajectory must be simulated. A second reason is **bounded local observability**: each agent sees only its own state and a finite neighbourhood. Together these mean that no local agent computes its system's global trajectory.

In civilizational terms:
- No individual policymaker computes the integrated biospheric trajectory.
- No consumer accounts for the full entropy cost of a supply chain.
- No voter measures the Kuramoto order parameter of their society.

Each agent acts on local fitness. Each decision is locally rational: grow the company, win the election, buy the cheaper product. The global consequence is invisible at the local scale not from ignorance but from a structural property of coupled dynamical systems with emergent macro-behaviour. This is the same mechanism by which no individual flocking bird knows it is in a flock, no firing neuron knows it is thinking, and no ant depositing pheromone knows it is building a bridge.

It is also a partial explanation — within the model — of why the participants in the paperclip trajectory of §4.3 do not perceive it as such, even when, were they shown the trajectory, they would name it.

### 4.5 The Hypothesis Restated

The paper's central empirical hypothesis, stated precisely [`[EMPIRICAL CONJECTURE]`]:

> Available proxies for resource concentration, value coupling, and substrate stress in contemporary human civilization are *consistent with* a regime that the TEO model, under Theorem 1, identifies as non-viable in the long-time limit. Whether the proxies can be sharpened into TEO-parameter estimates, and whether the system's trajectory in parameter space is in fact approaching the boundary of the viable region, are empirical questions taken up in §5.

The hypothesis is falsifiable. If point estimators for $\gamma_{\text{eff}}$, $K_{\text{eff}}$, and substrate-overshoot can be constructed, and if their values are shown to be inside the viable corridor (or moving away from its boundary), the hypothesis is false. §5 discusses the operationalisation; §6 discusses limitations.

The hypothesis is normatively neutral. It does not say what should be done. It says what the model predicts the dynamical system, under the hypothesised parameter regime, would do.

The title of this paper inverts the hypothesis. The **viable corridor** — the parameter region defined by $\gamma > 0$, $K > K_c$, and the accumulated-overshoot bound — is the regime that the model identifies as necessary for robust long-time viability. Brautigan's and Amodei's *machines of loving grace*, in our terms, would be systems whose parameters live inside this corridor. Whether such systems exist, and whether contemporary civilization could be brought into the corridor from outside, are open questions the model frames but does not answer.

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
- **Implications for political economy.** Without endorsing specific policy: under the model, single-constraint interventions (carbon pricing alone, antitrust alone, polarization reduction alone) cannot bring a system into the corridor unless all three operate jointly above their respective thresholds. Whether this prediction holds for real systems is the subject of §5.
- **The Transition Problem.** This paper describes the corridor under the assumption that the model is appropriate. How a system already outside the corridor reaches it — and whether the TEO model itself captures the relevant transition dynamics — is a separate, much harder problem (cf. companion essay "The Transition Problem", Peterlein, 2026).
- **Identity Persistence as a possible fourth dimension (future work).** The TEO state vector can be extended with a per-agent *identity-persistence* score $\mathrm{IP}_i$ measuring whether the governance components of agent $i$ are simultaneously operative during action selection — the *Chord* state of Perrier and Bennett (2026). The Chord Postulate predicts a phase transition at a critical $\mathrm{IP}_c$. We do *not* claim that the IP dimension is orthogonal to the three constraints — intra-agent architecture can plausibly affect effective $f_i$, $K$, and $\gamma$. A coupled treatment of IP and the three-constraint theorem is left to future work; the present paper deliberately restricts attention to the inter-agent dynamics.

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

- Acebrón, J. A., Bonilla, L. L., Pérez Vicente, C. J., Ritort, F., & Spigler, R. (2005). *The Kuramoto Model: A Simple Paradigm for Synchronization Phenomena.* Reviews of Modern Physics, 77(1), 137–185.
- Amodei, D. (2024). *Machines of Loving Grace.* Anthropic Essay.
- Aubin, J.-P. (1991). *Viability Theory.* Birkhäuser.
- Bai, Y., et al. (2022). *Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback.* arXiv:2204.05862.
- Bostrom, N. (2014). *Superintelligence: Paths, Dangers, Strategies.* Oxford University Press.
- Boxell, L., Gentzkow, M., & Shapiro, J. M. (2024). *Cross-Country Trends in Affective Polarization.* Review of Economics and Statistics.
- Brautigan, R. (1967). *All Watched Over by Machines of Loving Grace.* Communication Company.
- Hofbauer, J., & Sigmund, K. (1998). *Evolutionary Games and Population Dynamics.* Cambridge University Press.
- Iyengar, S., Lelkes, Y., Levendusky, M., Malhotra, N., & Westwood, S. J. (2019). *The Origins and Consequences of Affective Polarization in the United States.* Annual Review of Political Science.
- Kuramoto, Y. (1975). *Self-Entrainment of a Population of Coupled Non-Linear Oscillators.* Lecture Notes in Physics, 39, 420–422.
- Landauer, R. (1961). *Irreversibility and Heat Generation in the Computing Process.* IBM Journal of Research and Development, 5(3), 183–191.
- Mazeika, M., et al. (2025). *Utility Engineering: Analyzing and Controlling Emergent Value Systems in AIs.* Preprint.
- Mirollo, R. E., & Strogatz, S. H. (1991). *Stability of Incoherence in a Population of Coupled Oscillators.* Journal of Statistical Physics, 63(3–4), 613–635.
- NOAA Global Monitoring Laboratory. (2024). *Trends in Atmospheric Carbon Dioxide.* https://gml.noaa.gov/ccgg/trends/
- Perrier, E., & Bennett, C. (2026). *Identity Persistence in Autonomous Agents: The Chord Postulate.* Working Paper.
- Peterlein, F. (2026). *The Transition Problem.* In *Systems & Intelligence: An Open Thesis* (online repository).
- Pew Research Center. (2014–2022). *Political Polarization in the American Public; Partisanship and Political Animosity.* Pew Research Center reports.
- Philippon, T. (2019). *The Great Reversal: How America Gave Up on Free Markets.* Harvard University Press.
- Piketty, T. (2014). *Capital in the Twenty-First Century.* Belknap Press.
- Restrepo, J. G., Ott, E., & Hunt, B. R. (2005). *Onset of Synchronization in Large Networks of Coupled Oscillators.* Physical Review E, 71, 036151.
- Richardson, K., et al. (2023). *Earth Beyond Six of Nine Planetary Boundaries.* Science Advances.
- Rockström, J., et al. (2009). *A Safe Operating Space for Humanity.* Nature, 461(7263), 472–475.
- Strogatz, S. H. (1994). *Nonlinear Dynamics and Chaos.* Westview Press.
- Strogatz, S. H. (2000). *From Kuramoto to Crawford: Exploring the Onset of Synchronization in Populations of Coupled Oscillators.* Physica D, 143(1–4), 1–20.
- Taylor, P. D., & Jonker, L. B. (1978). *Evolutionary Stable Strategies and Game Dynamics.* Mathematical Biosciences, 40(1–2), 145–156.
- UBS Global Wealth Report. (2024). *Global Wealth Report 2024.* UBS / Credit Suisse.
- Wolfram, S. (1985). *Undecidability and Intractability in Theoretical Physics.* Physical Review Letters, 54(8), 735–738.
- Wolfram, S. (2002). *A New Kind of Science.* Wolfram Media.
- World Bank. (2024). *World Development Indicators.* World Bank Open Data.

---

## TODO

**Sections to draft:**
- [ ] Abstract (after body stable)
- [ ] §5 Predictions and Tests
- [ ] §6 Limitations and Counterarguments (most v0.2 hedges already point to it; §6 should consolidate them)
- [ ] §7 Discussion (currently has IP future-work note and outline; needs filling in)
- [ ] §8 Conclusion
- [ ] Appendix A (TEO derivation details)
- [ ] Appendix C (Numerical evidence for Conjecture 1)

**Completed in v0.2 (internal reviewer pass):**
- [x] §1 tone calibrated to match what §3 actually proves
- [x] §2.4 homeostatic brake reformulated as simplex-preserving redistribution
- [x] §2.5 substrate coupling: $f_i$ depends on $H$ via (5'); Landauer language softened
- [x] §2.7 IP-note removed from §2; moved to §7 future-work
- [x] §3.1 robust viability defined (open-set / positive-invariance, Aubin 1991)
- [x] §3.3 Theorem 1 scope explicit: thermodynamic limit, all-to-all, Lorentzian
- [x] §3.3 Lemma 1 strengthened with strict-dominance assumption $\delta > 0$
- [x] §3.3 Lemma 2 scope clarified (all-to-all + i.i.d. unimodal symmetric frequencies)
- [x] §3.3 Lemma 3 corrected to accumulated-overshoot condition
- [x] §3.4 candidate "Lyapunov functional" renamed *viability margin* (no monotonicity claim)
- [x] §4.1 table reframed as *heuristic regime mapping*, not calibrated estimation
- [x] §4.4 citation fixed: Wolfram (1985, 2002) for computational irreducibility; Chaitin removed
- [x] §4.5 final claim softened to "consistent with" hypothesis
- [x] References updated: Aubin, Wolfram (×2), Mirollo–Strogatz (1991), Acebrón et al., Restrepo–Ott–Hunt

**v0.3 reviewer-pass items (after Frank's second read):**
- [ ] Whether the strict-dominance assumption (1') is empirically defensible or should be relaxed
- [ ] Whether the redistribution-form (4) of the homeostatic brake is the right choice, or alternatives (only-to-below-threshold, share-weighted) yield qualitatively different results
- [ ] Whether the substrate coupling (5') $f_i = H \cdot f_i^{(0)}$ is too crude; alternatives include $f_i = \phi(H) f_i^{(0)}$ for some monotone $\phi$
- [ ] Whether Theorem 1 in the thermodynamic limit is the right framing, or a finite-$N$ probabilistic theorem would be more useful

**Polish-pass items (post-§5–§8):**
- [ ] Title-page formatting for arXiv submission
- [ ] Fill in full bibliographic entries (DOIs, journal volumes)
- [ ] Generate paper-quality vector version of `viable_corridor.png` (PDF/SVG preferred over PNG for arXiv)

**External-review checkpoints:**
- [ ] One independent read by a dynamical-systems expert (verify Lemma 1–3 sketches against Hofbauer–Sigmund, Strogatz, Mirollo–Strogatz)
- [ ] One independent read by an alignment researcher (Section 4 framing, the heuristic regime mapping in particular)
- [ ] One independent read by a complexity-theorist or coupled-systems specialist (the substrate coupling in (5') and the accumulated-overshoot model in (6))

**Companion-paper alignment:**
- [ ] Cross-reference between this paper and `papers/quantifying-emergent-utility-in-llms.md` (the empirical companion) explicit in both directions
- [ ] Ensure no claim-overlap that would trigger reviewer concerns about salami-slicing
