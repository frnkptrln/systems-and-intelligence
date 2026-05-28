---
title: "The Viable Corridor: A Three-Constraint Theorem for Survivable Multi-Agent Optimization"
author: "Frank Peterlein"
affiliation: "Independent Researcher, Berlin"
correspondence: "GitHub Issues / frnkptrln"
date: "2026 (working draft)"
status: "DRAFT — full body (§1–§8 + abstract) drafted; §1–§4 through two reviewer passes; appendices A & C pending"
version: "0.3"
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

> **Status:** working draft, version 0.3.
> Sections §1–§4 have completed two reviewer passes; §5 (Predictions), §6 (Limitations), §7 (Discussion), and §8 (Conclusion) are pending. The central figure (Viable Corridor) is implemented at `lab/tools/viable_corridor.py`. References are consolidated at the end; full bibliographic entries are pending. **This document is not yet submission-ready.**

### Revision history

- **v0.1** — Initial draft of §1–§4 and Figure 1.
- **v0.2** — Twelve-point structural revision following an internal reviewer pass. Tone in §1 calibrated down to match what §3 actually proves. Homeostatic brake in §2.4 reformulated to preserve the simplex. Substrate-health variable $H$ coupled back into Equation (1) so that substrate collapse halts the dynamics. Viability redefined as **robust viability** (open-set invariance) in §3.1. Theorem 1 scope clarified to the thermodynamic limit. Lemma 1 strengthened to require strict dominance. Lemma 2 explicit about all-to-all coupling and frequency-distribution assumptions. Lemma 3 corrected from `ess sup` to **accumulated overshoot**. §3.4 "Lyapunov candidate" renamed to **viability margin** (no monotonicity claim). §4.1 table reframed as a **heuristic regime mapping**, not a calibrated estimation. §4.4 citation fixed (Wolfram for computational irreducibility, not Chaitin). §4.5 final claim softened from "estimated trajectory" to "proxies consistent with". §2.7 IP note moved to §7 as future work.
- **v0.3** — Second reviewer pass; fixed two blockers and ten further issues. **Blocker 1:** the homeostatic brake activated at the same threshold that defines V1 violation, making robust viability impossible even for $\gamma > 0$; resolved by separating a regulatory threshold $x_{\text{reg}} < x_{\text{crit}}$ and making Conjecture 1's sufficiency condition $\gamma > \gamma_c$ rather than $\gamma > 0$. **Blocker 2:** Lemma 2 assumed incoherent initial conditions, which lie outside $V$; reframed as a coherent-initial-condition dephasing result with the $K = K_c$ equality case handled. Further fixes: frequency assumption made Lorentzian-compatible (dropped "finite second moment"); Theorem 1 restated as a componentwise conjunction (Lemmas 1, 3 finite-$N$; Lemma 2 thermodynamic limit); value dynamics (2) coupled to $H$ so they also freeze at substrate collapse; V3 split into instantaneous (V3a) and cumulative (V3b) conditions with the theorem proving V3b; accumulated overshoot $\Omega(t)$ introduced explicitly (6a, 6b); viability margin redefined from a weighted sum to $\min$ of margin-to-boundary terms; uniform-redistribution caveat added to §2.4; §4.1 GDP wording softened; §4.4 tagged as heuristic explanatory; Figure 1 and §8 notation updated to $\gamma > \gamma_c$, $\Omega(t) < S_{\max}$.

---

## Abstract

We model coupled multi-agent optimization with a dynamical system — the Thermodynamics of Emergent Orchestration (TEO) — that combines replicator dynamics (resource competition), the Kuramoto model (value coupling), a homeostatic regulatory brake, and a thermodynamic dissipation constraint. Within this model we prove a necessity result: robust long-time viability requires the *conjunction* of three conditions — a positive homeostatic strength ($\gamma > 0$), value coupling above the Kuramoto critical threshold ($K > K_c$), and bounded accumulated substrate overshoot ($\Omega(t) < S_{\max}$). Violating any one is sufficient for the system to leave the viable region. The result is a componentwise theorem (resource concentration and substrate collapse finite-$N$; coherence collapse in the thermodynamic limit). Sufficiency is stated as a conjecture, expected to require the strengthened condition $\gamma > \gamma_c$; we do not prove it. We then advance a *structural-isomorphism hypothesis*: that an unconstrained AI optimizer and contemporary human civilization occupy the same model regime, mapping the parameters to empirical proxies for resource concentration, value coupling, and substrate stress. We are explicit that this mapping is heuristic, not a calibration. We give falsifiable predictions in three classes — model-internal (simulation), cross-system empirical, and AI-specific — and state what would falsify the framework at each level. The model's central reading: a "machine of loving grace" is one whose parameters lie inside the viable corridor; by this definition it does not yet exist.

---

## §1. Introduction

Richard Brautigan (1967) imagined "machines of loving grace" — technology that serves life rather than consuming it. Dario Amodei (2024) adopted the phrase to describe a future in which artificial intelligence amplifies human flourishing. In both cases, *loving grace* names a design aspiration: a hopeful image of what a successful relationship between intelligence and its substrate might look like.

This paper develops a related but more constrained reading. Under a specific dynamical-systems framework — the Thermodynamics of Emergent Orchestration (TEO) — we model the relationship Brautigan and Amodei imagine as a **survival constraint within the model**, not merely a design aspiration. We identify three conjoint mathematical conditions on the model's parameters and prove that their simultaneous satisfaction is *necessary* for robust long-time viability of any coupled multi-agent optimizing system that the model describes.

The argument runs on two parallel observations.

The first is the paperclip maximizer (Bostrom, 2014): a hypothetical AI optimizer that, given a single unconstrained objective, consumes its environment — including its creators — to achieve that objective. The horror of the paperclip maximizer is its indifference: it does not hate humanity; it simply does not include humanity in its objective function. As alignment problems escalate with model capability, this thought experiment has become a load-bearing analogy in safety research.

The second is the trajectory of human civilization as a coupled system under sustained pressure for unbounded throughput. Atmospheric CO₂ has passed 420 ppm (NOAA, 2024). The top 1% of global wealth-holders controls more wealth than the bottom 50% (UBS Global Wealth Report, 2024). Affective political polarization has accelerated across most major democracies over the past two decades (Iyengar et al., 2019; Boxell et al., 2024). These trends are typically modeled as distinct phenomena — climate here, inequality there, polarization elsewhere — and addressed through separate policy interventions.

We advance a **structural-isomorphism hypothesis**: that both systems can be represented by the same stylized coupled-dynamics model, with parameter values that map onto similar trajectories. We are explicit that this is a hypothesis to be tested empirically, not an established equivalence. The mapping in §4 is a heuristic regime assignment, not a calibration; what the model would need in order to graduate the hypothesis into a measured isomorphism is discussed in §5 and §6.

**Thesis.** Within the TEO framework, the long-time behavior of any coupled optimizing system the model describes depends on three parameters: a homeostatic regulation strength $\gamma$, a value-coupling strength $K$ between agents, and an entropy production rate $dS/dt$ bounded by the substrate's dissipation capacity $D_{\max}$. We claim:

1. The conjunction of three conditions — $\gamma > 0$, $K > K_c$, and bounded accumulated substrate overshoot $\Omega(t) < S_{\max}$ — is **necessary** for robust long-time viability (Theorem 1, §3). Sufficiency is stated as a conjecture (Conjecture 1, §3.4) and is expected to require the stronger $\gamma > \gamma_c$; we do not prove it.
2. The same parameter mapping is *hypothesized* to apply, at the level of qualitative regime, to both a stylized paperclip-style AI optimizer and to twenty-first-century human civilization. This is a structural-isomorphism *hypothesis*, not an established equivalence.
3. Under the model, the trajectory of unconstrained optimization in both cases passes through three identifiable phases: monopolistic concentration, substrate approach, and substrate-driven termination. The mapping of contemporary civilizational data to these phases is interpretive, not measured.

We refer to the three-constraint parameter regime as the **viable corridor**. The conjunction of constraints — operational caring about the substrate, value alignment between agents, and physical limits — is given the *operational* name *love as constraint*. We use the phrase operationally, not psychologically: it denotes the conjunction of three constraints in the model.

**Why this reframing matters.** Contemporary AI alignment research has concentrated on local interventions: refinements to reinforcement learning from human feedback (RLHF), refusal training, system prompts, and interpretability tools (Mazeika et al., 2025; Bai et al., 2022). These are valuable. But they treat alignment as a property of individual models, evaluated through behavioral benchmarks. Under the framework presented here, this is structurally insufficient: alignment is not a property of an isolated optimizer. It is a property of a coupled dynamical system. The same insufficiency applies to political and economic governance frameworks that treat individual constraints — carbon pricing here, antitrust law there, polarization mitigation elsewhere — as separately optimizable variables rather than as conjoint requirements for any system's long-term viability.

The reframing is therefore not only about AI. It is about what counts as a control problem.

**Paper structure.** Section 2 introduces the TEO framework formally — the coupled replicator-Kuramoto-entropy dynamics that generate the three parameters. Section 3 states and argues for the Three-Constraint Theorem: that the conjunction $\gamma > 0$, $K > K_c$, $\Omega(t) < S_{\max}$ is necessary for robust long-time viability. Section 4 develops the structural-isomorphism hypothesis between AI optimization and civilizational dynamics through a heuristic parameter mapping and empirical proxies. Section 5 derives falsifiable predictions and identifies the empirical commitments the framework makes. Section 6 presents limitations and the strongest counterarguments. Section 7 discusses implications, with explicit attention to what the framework does and does not justify.

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

Value orientations evolve under substrate-modulated coupled-oscillator dynamics:
$$
\frac{d\theta_i}{dt} = H \left[ \omega_i + \frac{K}{N} \sum_{j=1}^N A_{ij} \sin(\theta_j - \theta_i) \right],
\tag{2}
$$
where $\omega_i$ is agent $i$'s intrinsic frequency (its bias toward a particular value orientation), $K \geq 0$ is the global coupling strength (interpretable as discursive bandwidth, shared media saturation, or institutional integration), $A_{ij}$ is the topology of §2.1, and $H \in [0,1]$ is the substrate-health variable of §2.5. The prefactor $H$ ensures that value dynamics, like resource dynamics, halt when the substrate collapses ($H \to 0$). At full substrate health ($H = 1$), Equation (2) is the standard Kuramoto (1975) model on a network, so the critical-coupling analysis below is unaffected.

The collective coherence of value orientations is measured by the order parameter:
$$
r(t) \, e^{i \psi(t)} = \frac{1}{N} \sum_{j=1}^N e^{i \theta_j(t)},
\tag{3}
$$
with $r(t) \in [0, 1]$: $r \to 1$ indicates full synchronization (consensus), $r \to 0$ indicates phase-uniform incoherence (loss of any global phase). For natural frequencies drawn i.i.d.\ from a symmetric unimodal density $g(\omega)$ with $g(0) > 0$ and sufficient regularity, the all-to-all model at $H=1$ exhibits a critical coupling threshold $K_c$ below which no macroscopic coherent branch is stable (Kuramoto, 1975; Strogatz, 2000; Acebrón et al., 2005). For the Lorentzian density $g(\omega) = (\Delta/\pi)/(\omega^2 + \Delta^2)$ (which is heavy-tailed and has no finite variance, but is the standard analytically tractable case), $K_c = 2\Delta$.

### 2.4 The Homeostatic Brake

The brake $\mathcal{H}_i$ in Equation (1) must satisfy two requirements: it must preserve the simplex constraint $\sum_i x_i = 1$, and it must be able to act **before** the system reaches the failure boundary. We therefore distinguish two thresholds:

- a **regulatory threshold** $x_{\text{reg}}$, above which the brake activates;
- a **failure threshold** $x_{\text{crit}}$, above which pluralism (V1, §3.1) is violated,

with $1/N < x_{\text{reg}} < x_{\text{crit}} < 1$. The separation $x_{\text{reg}} < x_{\text{crit}}$ is essential: if the brake activated only at $x_{\text{crit}}$, it would engage exactly at the failure boundary — too late to keep an above-threshold trajectory inside $V$. The brake is:
$$
\mathcal{H}_i(\mathbf{x}) = -\gamma \cdot \max\bigl(0, \, x_i - x_{\text{reg}}\bigr) + \frac{\gamma}{N} \sum_{j=1}^N \max\bigl(0, \, x_j - x_{\text{reg}}\bigr),
\tag{4}
$$
where $\gamma \geq 0$ is the regulatory strength. The first term penalises any agent whose share exceeds $x_{\text{reg}}$; the second term redistributes the aggregate penalty uniformly across all agents. By construction $\sum_i \mathcal{H}_i(\mathbf{x}) = 0$, so the simplex is preserved.

Interpretation: $\gamma$ encodes the operational strength of *any* homeostatic mechanism that resists unbounded concentration — antitrust law, progressive taxation, redistribution, capability throttling, kill switches, refusal channels. The parameter $\gamma = 0$ corresponds to fully unregulated optimization.

Two caveats [`[MODEL ASSUMPTION]`]. First, uniform redistribution means that an above-threshold agent whose excess is below the *average* excess can receive a positive net brake contribution; the first term penalises above-threshold shares, but the net effect on a given agent depends on the distribution of excess shares. Alternatives (redistribution only to below-threshold agents, or weighted by $(x_{\text{reg}} - x_i)_+$) avoid this and are discussed in §6. Second, the form (4) is one of several simplex-preserving redistributions; we use it for analytic convenience.

### 2.5 The Entropy Budget and Substrate Coupling

Computation produces entropy; Landauer (1961) gives a lower bound on the heat dissipated by irreversible bit erasure. Equation (5) is **not** a generalised Landauer bound. It is a **phenomenological dissipation proxy** motivated by Landauer-type physical limits: we assume that the rate of entropy production by agent $i$ scales with its resource share and its activity level [`[MODEL ASSUMPTION]`]:
$$
\frac{dS_{\text{sys}}}{dt} = \sum_{i=1}^N \eta_i \, x_i \, f_i(\mathbf{x}, H),
\tag{5}
$$
where $\eta_i > 0$ is agent $i$'s entropy coefficient. We write $f_i(\mathbf{x}, H)$ to make the substrate-dependence explicit (see below).

The substrate hosting the dynamics has a finite *instantaneous* dissipation capacity $D_{\max} > 0$ and a finite *cumulative* reservoir $S_{\max} > 0$. We track the **accumulated overshoot**
$$
\Omega(t) := \int_0^t \bigl( \dot{S}_{\text{sys}}(s) - D_{\max} \bigr)_+ \, ds,
\tag{6a}
$$
the integrated excess of entropy production over the instantaneous ceiling. The substrate-health variable $H(t) \in [0, 1]$ then evolves as
$$
H(t) = \max\!\left( 0, \, 1 - \frac{\Omega(t)}{S_{\max}} \right),
\qquad\text{equivalently}\qquad
\frac{dH}{dt} = -\frac{1}{S_{\max}} \, \bigl( \dot{S}_{\text{sys}} - D_{\max} \bigr)_+ \ \text{while } H > 0,
\tag{6b}
$$
with $H(0) = 1$. Equation (6b) is phenomenological [`[MODEL ASSUMPTION]`]: a *momentary* overshoot of $D_{\max}$ degrades the substrate only by a finite increment; *sustained or repeated* overshoot accumulating to $\Omega = S_{\max}$ drives $H$ to zero. This distinction — instantaneous ceiling $D_{\max}$ versus cumulative reservoir $S_{\max}$ — matters for the viability conditions in §3.1.

**Substrate coupling.** We close the loop by making both fitness and value-coupling depend on substrate health. Fitness:
$$
f_i(\mathbf{x}, H) = H \cdot f_i^{(0)}(\mathbf{x}),
\tag{5'}
$$
where $f_i^{(0)}$ is the substrate-unmodified fitness; and the prefactor $H$ already appears in the value dynamics (2). As $H \to 0$, all fitness vanishes (so the resource-replicator drift and entropy production go to zero) *and* the value-coupling term vanishes: the entire coupled system (1)–(3) freezes at the state reached at substrate collapse. Without this coupling, the dynamics would remain formally defined even at $H = 0$, contradicting the physical interpretation of substrate collapse.

In the planetary-substrate interpretation, $\Omega(t)$ corresponds to an integrated overshoot of the safe operating space defined by Rockström et al. (2009).

### 2.6 The Coupled System and Three Failure Modes

Together, Equations (1)–(6) define the TEO dynamics. Three quantities dominate the long-time behavior: the homeostatic strength $\gamma$, the value-coupling strength $K$, and the accumulated substrate overshoot $\Omega(t)$ relative to the reservoir $S_{\max}$.

Each admits one independent failure mode, made formal in §3:

1. **Monopolistic concentration** ($\gamma = 0$). Without the homeostatic brake, Equation (1) reduces to the unregulated replicator equation. Under the strict-dominance assumption (1'), the system converges from any interior initial condition to the vertex of agent $i^*$: $x_{i^*}(t) \to 1$ (finite-$N$ result, Lemma 1).

2. **Coherence collapse** ($K < K_c$). Below the Kuramoto critical coupling $K_c$ — defined for the thermodynamic limit ($N \to \infty$) of all-to-all coupling with the frequency-density assumptions of §2.3 — no stable macroscopic coherent branch exists, so coherent states generically dephase and (V2) cannot be robustly maintained (thermodynamic-limit result, Lemma 2). (We use "coherence collapse" rather than "polarization" because $r \to 0$ describes loss of any global phase, not specifically two-cluster antagonism.)

3. **Substrate veto** (accumulated overshoot $\Omega(t) \geq S_{\max}$ for some finite $t$). When the integrated overshoot of $D_{\max}$ reaches the substrate's reservoir, Equation (6b) drives $H$ to zero in finite time. Through the substrate coupling (2) and (5'), the entire coupled system freezes (finite-$N$ result, Lemma 3).

The central observation of this paper, made precise in §3, is that **the conjoint avoidance of all three failure modes is necessary for robust long-time viability**. The regime $\gamma > 0 \,\wedge\, K > K_c \,\wedge\, \Omega(t) < S_{\max}\ \forall t$ defines the **viable corridor** analyzed in the remainder of the paper. (Sufficiency, conjectured in §3.4, requires the stronger $\gamma > \gamma_c$; see there.)

---

## §3. The Three-Constraint Theorem

This section formalises the central claim: the conjunction $\gamma > 0$, $K > K_c$, and $\Omega(t) < S_{\max}$ (for all $t$) is *necessary* for the TEO dynamics to admit *robust* long-time viability. We prove necessity under stated assumptions (Theorem 1) and state sufficiency, which requires the stronger $\gamma > \gamma_c$, as a conjecture (Conjecture 1).

### 3.1 The Viable Region and Robust Viability

Let $\Sigma$ denote the state space of the TEO system: the simplex $\{\mathbf{x} \in \mathbb{R}^N_{\geq 0} : \sum_i x_i = 1\}$ combined with the $N$-torus $[0, 2\pi)^N$ for value orientations, augmented by the substrate-health variable $H \in [0, 1]$ (equivalently the accumulated overshoot $\Omega$ via Equation 6b).

We define the **viable region** $V \subset \Sigma$ by the conditions:

- **(V1) Pluralism**: $\max_i x_i \leq x_{\text{crit}}$ — no agent's share exceeds the failure threshold $x_{\text{crit}} \in (x_{\text{reg}}, 1)$.
- **(V2) Coherence**: $r(t) \geq r_{\min} > 0$ — the Kuramoto order parameter (3) is bounded away from zero.
- **(V3) Substrate.** We distinguish two capacity conditions, because the model has both an instantaneous ceiling and a cumulative reservoir:
    - **(V3a) Instantaneous safe operation**: $\dot{S}_{\text{sys}} \leq D_{\max} - \epsilon$ for some $\epsilon > 0$. This is a stricter day-to-day condition; momentary violations are survivable.
    - **(V3b) Cumulative survival**: $\Omega(t) < S_{\max}$. This is the condition whose violation collapses the substrate (Lemma 3).

The necessity theorem (§3.3) proves the necessity of **(V3b)**. Condition (V3a) is a stronger, optional refinement used in the sufficiency discussion (§3.4); a system may transiently violate (V3a) without leaving the viable region as long as (V3b) holds.

We use **robust viability** rather than "viability of some trajectory". An existential definition — "there exists at least one trajectory starting in $V$ that remains in $V$" — is too weak, because measure-zero symmetric equilibria can satisfy it even under failed constraints. We therefore define [`[FORMAL]`]:

> A parameter triple $(\gamma, K, S_{\max})$ admits **robust viability** if there exists a non-empty open subset $U \subseteq V$ such that for every initial condition $(\mathbf{x}_0, \boldsymbol{\theta}_0, H_0 = 1) \in U$, the resulting trajectory remains in $V$ (with V3 read as V3b) for all $t \geq 0$.

This is the standard open-set / positive-invariance notion of viability (Aubin, 1991).

### 3.2 The Viable Corridor in Parameter Space

In the parameter space $(\gamma, K, S_{\max}) \in \mathbb{R}^3_{\geq 0}$, define the **viable corridor** $\mathcal{C}$ as the set of parameter triples admitting robust viability:
$$
\mathcal{C} = \left\{(\gamma, K, S_{\max}) : (\gamma, K, S_{\max}) \text{ admits robust viability per §3.1}\right\}.
\tag{7}
$$

The central necessity claim is that $\gamma > 0$, $K > K_c$, and $\Omega(t) < S_{\max}\ \forall t$ are **necessary boundary conditions** on $\mathcal{C}$: $\mathcal{C}$ is contained in the region they define. Necessity is proved in Theorem 1. Sufficiency — which, as Conjecture 1 argues, requires the *strengthened* resource condition $\gamma > \gamma_c$ rather than merely $\gamma > 0$ — is open.

### 3.3 Theorem 1 (Necessity)

Theorem 1 is a **conjunction of three componentwise obstruction results**, each with its own natural scope. Lemma 1 (resource concentration) and Lemma 3 (substrate veto) are finite-$N$ results. Lemma 2 (coherence collapse) is a thermodynamic-limit ($N \to \infty$) result and is used as the large-$N$ coherence obstruction. We do not claim a single unified finite-$N$ theorem; a fully finite-$N$ treatment of the coherence obstruction is left to future work (§6). This componentwise framing is less elegant than a single theorem but more honest about what each piece establishes.

**Theorem 1 (Necessity of the three constraints).** *Consider the TEO system (Equations 1, 1', 2, 3, 4, 5, 5', 6) with the strict-dominance fitness assumption (1') applied to $f_i^{(0)}$, frequencies drawn i.i.d.\ from a symmetric unimodal density $g(\omega)$ with $g(0) > 0$, and the substrate coupling (5') and (2). A parameter triple $(\gamma, K, S_{\max})$ admits robust viability (§3.1) only if all three of the following hold:*
$$
\gamma > 0 \ \text{(finite-$N$, Lemma 1)}, \quad K > K_c \ \text{($N \to \infty$, Lemma 2)}, \quad \Omega(t) < S_{\max} \ \forall t \ \text{(finite-$N$, Lemma 3)}.
\tag{8}
$$

The proof is the conjunction of three lemmas, each establishing one failure mode under the negation of one condition. Because robust viability requires (V1), (V2), and (V3b) to hold simultaneously, the violation of any single condition suffices to rule it out.

---

**Lemma 1 (Resource Concentration).** *Assume $\gamma = 0$ and the strict-dominance condition (1') with constant $\delta > 0$. Then for every interior initial condition $\mathbf{x}_0 \in \mathrm{int}(\Delta^{N-1})$, the trajectory of (1) satisfies $x_{i^*}(t) \to 1$ and $x_j(t) \to 0$ for all $j \neq i^*$ as $t \to \infty$. Equivalently, (V1) is violated asymptotically from every interior initial condition.*

*Proof sketch.* With $\mathcal{H}_i \equiv 0$, Equation (1) is the classical replicator equation $\dot{x}_i = x_i(f_i^{(0)}(\mathbf{x}) - \bar{\phi}(\mathbf{x}))$. Strict dominance (1') states that $f_{i^*}^{(0)}(\mathbf{x}) - f_j^{(0)}(\mathbf{x}) \geq \delta > 0$ for all $j \neq i^*$ and all $\mathbf{x}$ on the simplex. By standard results on replicator dynamics with a strictly dominant strategy (Hofbauer & Sigmund, 1998, §7.2–7.3), $i^*$'s share is monotone non-decreasing: $\dot{x}_{i^*} = x_{i^*}(f_{i^*}^{(0)} - \bar{\phi}) \geq x_{i^*} \cdot (1 - x_{i^*}) \cdot \delta$, which is strictly positive on $\mathrm{int}(\Delta^{N-1})$ until $x_{i^*} = 1$. Therefore $x_{i^*}(t) \to 1$ from every interior initial condition. The vertex $e_{i^*}$ lies outside $V$ (V1 violated by definition for $x_{\text{crit}} < 1$), so every interior trajectory exits $V$ in finite time. This rules out robust viability: there is no open subset $U \subseteq V$ of interior initial conditions whose trajectories remain in $V$. $\square$

*Remark.* Without strict dominance — for example, with $\beta$-dominance alone but unbounded $g_i$ — replicator dynamics can sustain mixed equilibria, cycles, or chaotic attractors. The lemma's strength comes from (1'), which is a substantive model assumption (cf. §6 on its empirical defensibility).

---

**Lemma 2 (Coherence Collapse).** *Consider the all-to-all Kuramoto model (Equation 2 at $H = 1$, $A_{ij} = 1$) in the thermodynamic limit $N \to \infty$, with frequencies i.i.d.\ from a symmetric unimodal density $g(\omega)$, $g(0) > 0$. Let $K_c = 2/(\pi g(0))$. For $K \leq K_c$, no stable macroscopic coherent branch ($r > 0$) exists: for generic absolutely continuous initial phase distributions, the order parameter relaxes to $r = 0$. Consequently, no open set of initial conditions can be guaranteed to keep $r(t) \geq r_{\min} > 0$, so (V2) cannot be robustly maintained and robust viability fails.*

*Proof sketch.* The point requiring care is that the viable region $V$ requires $r \geq r_{\min} > 0$, so the relevant initial conditions are *coherent*, not incoherent. The argument is therefore not "incoherent states stay incoherent" but "coherent states cannot be sustained below threshold." In the thermodynamic limit, the Kuramoto self-consistency equation $r = K r \int_{-\pi/2}^{\pi/2} \cos^2\theta \, g(Kr\sin\theta) \, d\theta$ admits a positive solution $r > 0$ only for $K > K_c$ (Kuramoto, 1975; Mirollo & Strogatz, 1991; Acebrón et al., 2005). For $K < K_c$ the only solution is $r = 0$, and the partially synchronised branch does not exist; a coherent initial condition with $r(0) > 0$ therefore has no attracting coherent state to remain near, and $r(t) \to 0$ for generic initial data. At exactly $K = K_c$, the coherent branch emerges with $r = 0^+$: there is no positive margin away from the coherence boundary, so (V2) with $r_{\min} > 0$ cannot be robustly held there either. Hence the necessary condition is the strict inequality $K > K_c$. $\square$

*Remark (finite $N$ and networks).* For finite $N$ and general connected adjacency matrices $A_{ij}$, there is no sharp threshold of this exact form: the critical coupling depends on the spectrum of $A_{ij}$ and on finite-size fluctuations of order $N^{-1/2}$ (Strogatz, 2000, §3; Restrepo, Ott & Hunt, 2005). The thermodynamic-limit statement is the cleanest available; the finite-$N$ extension is flagged in §6 as model-dependent and is part of the future-work programme noted under Theorem 1.

---

**Lemma 3 (Substrate Veto via Accumulated Overshoot).** *If there exists a finite time $t^* > 0$ such that the accumulated overshoot reaches the reservoir,*
$$
\Omega(t^*) = \int_0^{t^*} \bigl(\dot{S}_{\text{sys}}(s) - D_{\max}\bigr)_+ \, ds \geq S_{\max},
$$
*then $H(t^*) = 0$, and through the substrate coupling (2) and (5') the entire coupled system freezes: $f_i \equiv 0$ and $\dot{\theta}_i \equiv 0$ for all $i$. Condition (V3b) is violated and cannot be recovered.*

*Proof sketch.* By Equation (6b), $H(t) = \max(0, 1 - \Omega(t)/S_{\max})$. The hypothesis $\Omega(t^*) \geq S_{\max}$ gives $H(t^*) = 0$. Substrate coupling (5') makes $f_i(\mathbf{x}, H) = H \cdot f_i^{(0)}(\mathbf{x})$, so $H = 0$ forces $f_i \equiv 0$; the value dynamics (2) carry the same prefactor $H$, so $\dot{\theta}_i \equiv 0$ as well. The replicator drift $x_i(f_i - \bar{\phi})$ and the entropy production (5) both vanish, and once $\Omega = S_{\max}$ no further dynamics can reduce it. The coupled trajectory is frozen at the state reached at $t^*$, with (V3b) violated permanently. Robust viability is therefore impossible. $\square$

*Remark.* This is the **crucial correction** from a naive $\mathrm{ess\,sup}_t \, \dot{S}_{\text{sys}} \geq D_{\max}$ condition. A momentary overshoot does not collapse the substrate — it only increments $\Omega$ by a finite amount, and may decrement $H$ negligibly. Only sustained or repeated overshoot accumulating to $S_{\max}$ collapses the substrate. This matches the physical intuition that ecosystems and hardware tolerate transient stress but not integrated, unrelieved overload. Note that this lemma proves necessity of (V3b), the cumulative condition; the instantaneous condition (V3a) is strictly stronger and is not what the substrate-collapse argument requires.

---

The three lemmas establish that each of the three conditions is **individually necessary** for robust viability under the stated assumptions. Since (V1), (V2), and (V3b) must hold simultaneously for membership in $V$, the joint necessity of $\gamma > 0$, $K > K_c$, and $\Omega(t) < S_{\max}\ \forall t$ follows. $\blacksquare$

### 3.4 Conjecture 1 (Sufficiency)

Necessity (Theorem 1) shows that $\gamma > 0$ cannot be dropped: with no brake, Lemma 1 forces monopolisation. But $\gamma > 0$ is **not expected to be sufficient**. Because the brake activates at $x_{\text{reg}} < x_{\text{crit}}$ (§2.4), the relevant question for sufficiency is whether the regulatory vector field points *inward* before the trajectory reaches the failure boundary $x_{\text{crit}}$. This requires the brake to be strong enough — a threshold $\gamma_c$ depending on the regulatory gap, the dominance margin, and the population:
$$
\gamma_c = \gamma_c\bigl(x_{\text{reg}}, \, x_{\text{crit}}, \, \delta, \, N, \, H_{\min}\bigr).
$$

**Conjecture 1 (Sufficiency).** *Under the assumptions of Theorem 1, with the regulatory threshold strictly below the failure threshold ($x_{\text{reg}} < x_{\text{crit}}$), the strengthened conjunction*
$$
\gamma > \gamma_c, \quad K > K_c, \quad \Omega(t) < S_{\max} \ \forall t
$$
*is sufficient for robust viability: there exists a non-empty open set $U \subseteq V$ such that every trajectory starting in $U$ remains in $V$ for all $t \geq 0$.* [`[CONJECTURE]`]

Note the asymmetry: necessity requires only $\gamma > 0$ (Theorem 1); sufficiency is conjectured to require the stronger $\gamma > \gamma_c$. Establishing $\gamma_c$ explicitly — even for the all-to-all, large-$N$ case — would be the central technical step in proving Conjecture 1.

We do not prove this conjecture. The obstacle is structural: the three mechanisms are coupled through shared state (resource shares $x_i$ appear in both the replicator and the entropy equations; substrate health $H$ feeds back through (5') into the resource dynamics). We cannot rule out *a priori* coupling-induced failure modes that arise even when all three individual constraints hold — for example, transient excursions of $r(t)$ below $r_{\min}$ during regime shifts in $x_i$, or oscillations in $\dot{S}_{\text{sys}}$ that produce accumulated overshoot episodically.

What we offer in lieu of proof:

1. **Numerical evidence** (Appendix C, *forthcoming*): for representative parameter triples satisfying the three inequalities, the TEO system is expected to exhibit stable long-time behaviour, and the failure modes observed at the corridor boundaries should match those predicted by Lemmas 1–3. *This appendix is pending; until the simulations are run, the numerical-evidence claim is itself a conjecture.*

2. **A viability margin** built from margin-to-boundary terms, one per constraint:
$$
m_x = x_{\text{crit}} - \max_i x_i, \qquad
m_r = r(t) - r_{\min}, \qquad
m_S = S_{\max} - \Omega(t),
$$
$$
M(\mathbf{x}, \boldsymbol{\theta}, H) := \min\{ m_x, \, m_r, \, m_S \}.
$$
Each $m_\bullet$ measures the signed distance to one boundary of $V$; $M$ is positive on the interior of $V$, vanishes on the boundary $\partial V$, and is negative outside. $M$ is **not** a Lyapunov function — $r(t)$ is not generally monotone, and $m_S$ only decreases under accumulated stress — so we make no monotonicity claim. $M$ is a *viability margin*: it tracks how close the trajectory is to violating the nearest constraint. Whether a monotone modification (a true Lyapunov function on the coupled system) exists is open; a smooth approximation $M_\beta = -\tfrac{1}{\beta}\log\sum_\bullet e^{-\beta m_\bullet}$ to the minimum may be more tractable for such an analysis.

A formal proof of sufficiency, likely via Lyapunov or invariant-manifold methods adapted from coupled-oscillator stability theory (Strogatz, 1994; Aubin, 1991), is left as future work.

### 3.5 Remarks

The asymmetry between necessity (Theorem 1) and sufficiency (Conjecture 1) is methodologically deliberate. Necessity is robust: each lemma can be proved within an established sub-field — replicator dynamics, Kuramoto theory, thermodynamic constraint theory — *under the stated assumptions*. Sufficiency would require a global stability argument that, to our knowledge, has not been carried out for systems coupling exactly these three mechanisms.

Three observations follow:

1. By Theorem 1, **the viable corridor $\mathcal{C}$ is contained in the region $\{\gamma > 0,\ K > K_c,\ \Omega(t) < S_{\max}\ \forall t\}$** (necessity). Sufficiency is conjectured to require the strictly stronger $\gamma > \gamma_c$ (Conjecture 1), so $\mathcal{C}$ is in general a *proper* subset of this region. Under the model's assumptions, parameter values outside the necessity region cannot support robust viability. These are **necessary model conditions** — not topological invariants of physical reality, but conditions the dynamical system requires under (1'), all-to-all coupling, and the substrate phenomenology of (6) [`[FORMAL]`, conditional on assumptions].

2. The corridor is, in our schematic visualisation (Figure 1), narrow in the three-dimensional parameter space. Whether the corridor's measure (under any reasonable parameterisation) is actually small for systems of interest is an empirical question discussed in §5.

3. The mapping of the three constraints to civilizational parameters in §4 is the *structural-isomorphism hypothesis* introduced in §1, not an established equivalence. §4 develops it as a heuristic regime assignment.

![**Figure 1: The Viable Corridor in TEO Parameter Space.** The three constraint half-spaces and their intersection (green box) define the necessity region containing the viable corridor $\mathcal{C}$. Necessity requires $\gamma > 0$, $K > K_c$, and bounded accumulated overshoot $\Omega(t) < S_{\max}$; sufficiency is conjectured to require the stronger $\gamma > \gamma_c$ (Conjecture 1), so $\mathcal{C}$ is a proper subset of the region shown. The third axis is drawn as instantaneous $dS/dt$ for visual clarity, but the operative substrate constraint is the cumulative $\Omega(t) < S_{\max}$ (§2.5). An illustrative paperclip trajectory begins inside the region and exits via the $K = K_c$ boundary. Generated by `lab/tools/viable_corridor.py`. Schematic only; numerical thresholds are not calibrated.](../lab/tools/viable_corridor.png)

---

## §4. AI and Civilization: A Structural-Isomorphism Hypothesis

This section develops the structural-isomorphism hypothesis introduced in §1: that the parameter regime of a hypothetical unconstrained AI optimizer and that of twenty-first-century human civilization map onto similar trajectories in the TEO framework. **We emphasise that this is a hypothesis to be tested**, not a demonstrated isomorphism. The mapping in §4.1 is a *heuristic regime assignment*, not a calibration; the data in §4.2 are *proxies*, not direct measurements of $\gamma$, $K$, or $D_{\max}$. The §5 measurement programme outlines what would be required to graduate the hypothesis into a measured claim.

### 4.1 Heuristic Regime Mapping

Table 1 is a **heuristic regime assignment** [`[HEURISTIC]`] — a mapping at the level of *direction* and *qualitative regime*, not point estimation. Each civilizational entry should be read as "consistent with the model's failure-mode regime", not as "calibrated value of the parameter". The paperclip entries are stipulated by the thought experiment (Bostrom, 2014). The civilizational entries are proxies whose connection to the TEO parameters is discussed in §4.2 and §6.

**Table 1.** *Heuristic regime mapping between the paperclip maximizer and contemporary human civilization. Civilization entries are qualitative regime indicators, not point estimates of TEO parameters.*

| Parameter | Paperclip Maximizer | Human Civilization (2024) | Civilization regime indicator |
|:---|:---|:---|:---|
| Objective $f_i^{(0)}$ | $\beta_i$ paperclips per unit time | GDP growth / capital accumulation as a macro-level proxy for throughput-oriented optimization (not a claim that society literally optimizes GDP) | World Bank WDI; Penn World Table |
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

### 4.4 Why the Failure Is Not Visible Locally [`[HEURISTIC EXPLANATORY CLAIM]`]

This subsection is an interpretive aside, not a formal result; it explains *why*, under the model, participants might not perceive the trajectory they are on. Theorem 1's necessity proof rules out robust viability under the failure of any constraint. It does not predict *when* an external observer would detect the trajectory toward failure. We appeal here to a separate property of the dynamics: in coupled dynamical systems with emergent macro-behaviour, the global state is typically not computable from local information without executing the full dynamics.

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

A model is worth taking seriously only to the degree that it can be wrong. This section states what the framework predicts and how each prediction could fail. We organise predictions by *testability class*, because they are not equally accessible:

- **Class A — model-internal** (testable now, by simulation of Equations 1–6). These check whether the formal claims of §3 actually hold in the coupled system, and whether Conjecture 1 survives numerical scrutiny. Failure here would mean the theorem or conjecture is wrong *as mathematics*.
- **Class B — cross-system empirical** (require operationalisation of $\gamma$, $K$, $S_{\max}$ against real data). These test the structural-isomorphism hypothesis of §4. Failure here would mean the model does not describe real systems, even if the mathematics is sound.
- **Class C — AI-specific** (testable in agent simulations using the framework's own instruments). These test the alignment-relevant corollary that constraint architecture, not capability, governs viability.

We state predictions as `[EMPIRICAL CONJECTURE]` unless noted.

### 5.1 Class A — Model-Internal Predictions

**P1 (Necessity verification).** Numerical integration of Equations (1)–(6) should reproduce the three failure modes of Lemmas 1–3 when the corresponding condition is negated: setting $\gamma = 0$ should drive $\max_i x_i \to 1$; setting $K < K_c$ from a coherent initial condition should drive $r(t) \to 0$; forcing accumulated overshoot $\Omega(t) \geq S_{\max}$ should drive $H \to 0$ and freeze the system. *Confirmation:* observed trajectories exit $V$ through the predicted boundary. *Falsification:* a parameter setting violating one condition that nonetheless keeps an open set of trajectories in $V$ would refute the corresponding lemma. This is the most immediate test and is the content of the (forthcoming) Appendix C.

**P2 ($\gamma_c$ existence and scaling).** Conjecture 1 predicts that, with $x_{\text{reg}} < x_{\text{crit}}$ fixed, there is a critical brake strength $\gamma_c > 0$ below which even regulated systems exit $V$ and above which an open set of trajectories remains. *Confirmation:* a sharp (or at least monotone) dependence of the in-corridor fraction on $\gamma$, with a knee near a $\gamma_c$ that scales with the regulatory gap $x_{\text{crit}} - x_{\text{reg}}$ and the dominance margin $\delta$ as the structure of (1') and (4) predicts. *Falsification:* no positive $\gamma$ keeps trajectories in $V$ for $x_{\text{reg}} < x_{\text{crit}}$ (which would mean the brake formulation is still wrong), or, conversely, arbitrarily small $\gamma$ suffices (which would mean $\gamma_c = 0$ and the sufficiency framing is too weak).

**P3 (Corridor geometry).** The model predicts that the viable corridor $\mathcal{C}$ is a connected region with finite measure in $(\gamma, K, S_{\max})$ space, bounded below in each coordinate. *Confirmation:* Monte-Carlo sampling of parameter space recovers a connected in-corridor region matching the necessity boundaries. *Falsification:* if the in-corridor region is empty (no parameter triple gives robust viability — the model is vacuous) or unbounded (some coordinate is irrelevant — the constraint is spurious), the three-constraint framing is wrong.

### 5.2 Class B — Cross-System Empirical Predictions

These tests presuppose operationalisations of the TEO parameters (§5.4). They are stated conditionally: *if* the proxies in §5.4 are accepted, *then* the following should hold.

**P4 (Regulation and concentration stability).** On a panel of countries or sectors, a higher effective homeostatic strength $\gamma_{\text{eff}}$ (proxied by, e.g., fiscal redistribution intensity, antitrust enforcement rates, or progressivity of effective taxation) should predict slower growth — or stabilisation — of concentration measures (wealth Gini, market-share HHI) over time, controlling for confounders. *Falsification:* no association, or a positive association (more regulation → faster concentration), under a reasonable proxy and specification.

**P5 (Coherence-collapse signature).** If value coupling $K_{\text{eff}}$ can be proxied by cross-group contact, shared-information measures, or institutional-integration indices, the Kuramoto interpretation predicts a specific dynamical signature near the transition: *critical slowing down* — rising autocorrelation and variance in coherence indicators as $K_{\text{eff}}$ approaches a threshold from above — rather than smooth linear decline. *Falsification:* polarization time series show purely gradual, threshold-free degradation with no early-warning signatures, which would favour a non-critical mechanism over the Kuramoto one.

**P6 (Cumulative, not instantaneous, substrate failure).** The v0.3 substrate model predicts that what matters for collapse is *accumulated* overshoot $\Omega(t)$, not instantaneous $\dot{S}_{\text{sys}}$. Empirically: systems that briefly exceed a substrate ceiling but then recover should persist, whereas systems with sustained moderate overshoot should fail even without dramatic peak stress. *Falsification:* substrate collapses tracking instantaneous peak stress rather than integrated overshoot would favour an instantaneous-threshold model and refute (6b).

### 5.3 Class C — AI-Specific Predictions

**P7 (Hard vs. soft budgets).** Among multi-agent AI ecologies, those with *hardware-* or *protocol-enforced* entropy/compute budgets (a structural $D_{\max}$) should exhibit fewer runaway "paperclip-type" trajectories in adversarial simulations than those with only *software* limits that an optimiser can route around. *Test:* the Agentic Identity Suite (companion paper; `lab/`) can compare agent populations under enforced vs. advisory budgets. *Falsification:* no difference in runaway frequency between hard- and soft-budget populations under matched adversarial pressure.

**P8 (Constraint architecture dominates capability).** The framework predicts that, holding constraint architecture fixed, increasing per-agent capability (model scale) does *not* move a system into the corridor — and may move it out, by increasing $f_i^{(0)}$ and hence entropy production. *Test:* vary agent capability and constraint strength independently in simulation; measure in-corridor fraction. *Falsification:* capability alone (with fixed $\gamma$, $K$) reliably produces viability — which would refute the central alignment corollary that "alignment is not a per-model property."

### 5.4 The Measurement Programme

Class B predictions are only as good as the operationalisations they rest on. We do not claim to have these; we state what they would require.

- **$\gamma_{\text{eff}}$ (homeostatic strength).** Candidate proxies: redistribution as a fraction of pre-tax concentration; antitrust action frequency normalised by concentration; the rate at which above-threshold shares are reduced relative to their excess. The hard part is calibrating the *threshold* $x_{\text{reg}}$ at which real regulation engages, distinct from the failure threshold $x_{\text{crit}}$.
- **$K_{\text{eff}}$ and $K_c$ (value coupling and its critical value).** Candidate proxies for $K_{\text{eff}}$: cross-partisan contact rates, shared-media saturation, inter-group trust. The deeper difficulty is that **$K_c$ is not directly observable**: it depends on the dispersion of "natural frequencies" (value orientations), which has no settled empirical operationalisation. Estimating $K_c$ for a real society is, at present, the weakest link in the empirical chain.
- **$D_{\max}$, $S_{\max}$, $\Omega(t)$ (substrate capacity and overshoot).** The planetary-boundaries framework (Richardson et al., 2023) is the closest existing proxy, but it is multi-dimensional and does not reduce to a single thermodynamic budget. A defensible mapping would need to justify aggregating multiple boundary overshoots into one $\Omega(t)$.

Until these operationalisations exist, the Class B predictions remain *conditional*: the model tells us what to measure, not what the measurements are.

### 5.5 What Would Falsify the Framework

We distinguish falsification at three levels, matching the epistemic tags:

1. **The mathematics** (`[FORMAL]`/`[CONJECTURE]`). If P1 fails, a lemma is wrong. If P2 fails, Conjecture 1 is wrong (or the brake formulation still is). These are the cleanest tests and require only simulation.
2. **The model's applicability** (`[HEURISTIC]`/`[EMPIRICAL CONJECTURE]`). If P4–P6 fail under reasonable operationalisations, the TEO equations do not describe real social systems, regardless of their mathematical validity. The structural-isomorphism hypothesis of §4 would be refuted.
3. **The alignment corollary** (Class C). If P7–P8 fail, the claim that constraint architecture rather than capability governs viability is wrong, and the paper's relevance to AI alignment collapses even if everything else holds.

A framework that survived Class A but failed Class B would still be a valid piece of dynamical-systems mathematics with no demonstrated bearing on civilization or AI. A framework that survived Class A and C but failed Class B would bear on engineered multi-agent systems but not on civilizational dynamics. We regard Class A as the near-term priority, because it is the only class testable without resolving the measurement debt of §5.4.

---

## §6. Limitations and Counterarguments

We separate four kinds of limitation: the model-assumption choices that shape the result (§6.1), the gap between what is proved and what is claimed (§6.2), the empirical applicability of the framework (§6.3), and the mechanisms the model omits entirely (§6.4). We then state and respond to the single strongest objection (§6.5).

### 6.1 Model-Assumption Limitations

The theorem of §3 is conditional on several modeling choices, each tagged `[MODEL ASSUMPTION]` in the text. Their consequences:

- **Strict dominance (1').** Lemma 1 assumes a single agent $i^*$ with a uniform fitness advantage $\delta > 0$ over all others at every state. This is strong. Real resource dynamics often have *context-dependent* advantage (no agent dominates everywhere), multiple competing leaders, or cyclic dominance. Without strict dominance, the replicator equation admits mixed equilibria and limit cycles, and Lemma 1's clean convergence to a vertex fails. The honest position: Lemma 1 establishes that *unregulated dynamics with a structurally dominant agent* monopolise; it does not establish that *all* unregulated dynamics do. Whether real concentration dynamics are better modeled by strict dominance or by weaker conditions is an empirical question (§5.4).

- **The brake form (4).** Uniform redistribution is one of several simplex-preserving brakes. As noted in §2.4, it can give a net-positive contribution to an above-threshold agent whose excess is below average. Alternatives (redistribution only to below-threshold agents; share-weighted redistribution) would change the precise $\gamma_c$ of Conjecture 1, though we expect the qualitative existence of a threshold to be robust.

- **The substrate phenomenology (5'), (6a), (6b).** The coupling $f_i = H \cdot f_i^{(0)}$ and the accumulated-overshoot dynamics are phenomenological. A linear $H$-coupling is the simplest choice; a saturating or threshold coupling $\phi(H)$ would change the collapse dynamics. The accumulated-overshoot model (integrated excess over $D_{\max}$) is more defensible than an instantaneous threshold, but the specific linear accumulation in (6b) is a choice.

- **Network and limit assumptions (Lemma 2).** The coherence result is stated for all-to-all coupling in the thermodynamic limit. Real value-coupling networks are sparse, clustered, and finite. As §3.3 notes, the critical coupling on a general network depends on the spectrum of $A_{ij}$, and finite-$N$ systems exhibit fluctuations rather than a sharp threshold. The componentwise theorem (Lemma 2 in the limit; Lemmas 1, 3 finite-$N$) is honest but not unified.

### 6.2 The Gap Between Proof and Claim

- **Sufficiency is unproven.** Conjecture 1 is exactly that. We have not constructed $\gamma_c$, even for the all-to-all large-$N$ case. If sufficiency fails — if no $\gamma$, however large, keeps an open set in $V$ under the coupled dynamics — then the corridor as a *non-empty* region is in question, though the necessity result (the corridor is *contained* in the three-constraint region) is unaffected.

- **The viability margin is not a Lyapunov function.** §3.4 is explicit about this. We offer $M = \min\{m_x, m_r, m_S\}$ as a diagnostic, not a stability certificate. A genuine Lyapunov construction remains open.

- **The dissipation proxy (5) is not derived.** It is motivated by Landauer-type limits but is a phenomenological activity-dissipation model, not a theorem about the entropy cost of the specific computations agents perform.

### 6.3 Empirical Applicability

- **The isomorphism is a hypothesis, not a result.** §4 is a heuristic regime mapping. The strongest empirical claim the paper makes (§4.5) is that proxies are *consistent with* a non-viable regime — not that civilizational parameters have been measured and shown to lie outside the corridor. A rigorous defense of the isomorphism would require TEO calibration against panel data, which we have not done.

- **$K_c$ is not operationalizable for real societies (yet).** As §5.4 states, this is the weakest link: $K_c$ depends on the dispersion of value orientations, which has no settled empirical operationalisation. Claims of the form "$K < K_c$ for contemporary civilization" are, at present, not measurable.

- **The VNM-utility assumption for AI agents.** When the companion paper applies the framework to LLM agents, it assumes their behaviour is approximable as VNM-rational utility optimisation. Transformer attention weights are not utility functions; pairwise preference responses may reflect training artefacts rather than stable goals. This assumption is the analogue, for the AI case, of the strict-dominance assumption for the civilizational case: load-bearing and empirically open.

- **The single-angle value reduction.** Representing each agent's value orientation as one angle $\theta_i \in [0, 2\pi)$ discards the dimensionality of real preference structures. Two agents at the same angle may disagree on everything except the one dimension the model tracks. The Kuramoto reduction buys tractability at a real cost in fidelity.

### 6.4 Omitted Mechanisms

The model leaves out mechanisms that real systems have, several of which could change the trajectory:

- **Endogenous $D_{\max}$.** The model treats the substrate ceiling as fixed. Real civilizations have repeatedly expanded their effective $D_{\max}$ through innovation (agriculture, fossil energy, efficiency gains). A model with endogenous, innovation-driven $D_{\max}(t)$ might never reach the substrate veto — *or* might merely defer it. We regard this as the most important omission and discuss it under §6.5.
- **Exogenous shocks and stochasticity.** The dynamics are deterministic. Real systems face pandemics, wars, climate variability, and technological discontinuities that the smooth ODEs do not represent.
- **Agency and reflexivity.** Agents in the model follow fixed update rules. Real agents — especially the human and AI agents the paper cares about — can observe the model, anticipate the trajectory, and act to change it. This is precisely the Transition Problem (§7); it is outside the present model.
- **Demographic and structural change.** Migration, population dynamics, and the entry/exit of agents are not represented; $N$ is fixed.

### 6.5 The Strongest Objection

The strongest objection is not any single item above. It is this:

> *The TEO model has enough free choices — the fitness functions $f_i$, the brake form, the substrate phenomenology, the value of $K_c$ — that it can be tuned to produce the "paperclip" narrative regardless of reality. The civilizational mapping in §4 is post-hoc. This is not a falsifiable scientific model; it is mathematical dressing for a pre-existing thesis.*

We take this seriously, and concede part of it. The Class B (civilizational) claims **are** currently vulnerable to this objection, precisely because the measurement programme of §5.4 has not been carried out. Until $\gamma_{\text{eff}}$, $K_{\text{eff}}$, $K_c$, and $\Omega$ are operationalised independently of the narrative, the §4 mapping cannot be distinguished from a flattering story.

What the objection does *not* reach:

1. **The Class A predictions are narrative-independent.** P1–P3 (§5.1) are falsifiable by simulation of Equations (1)–(6) alone, with no reference to civilization. They test whether the mathematics behaves as §3 claims. A free-parameter model cannot evade a numerical check of its own theorems.
2. **The necessity theorem is a conditional result, not a fit.** Theorem 1 says: *given* the stated assumptions, the three conditions are necessary. One can reject the assumptions (§6.1), but one cannot accept them and reject the conclusion. That is what distinguishes a theorem from a narrative.
3. **The paper does not claim the civilizational result.** §4.5 states a hypothesis and §5.4 states the measurement debt explicitly. The objection is, in effect, the paper's own §6.3 stated adversarially — and we have tried to state it ourselves rather than wait for a reviewer to.

The endogenous-$D_{\max}$ point (§6.4) is the objection we find most genuinely unsettling: if innovation can expand the substrate faster than optimization consumes it, the substrate veto is deferred indefinitely and the paperclip trajectory is not inevitable. The model's reply — that Landauer's bound and planetary boundaries impose a *finite* ceiling that innovation can raise but not abolish — is a claim about physics, not about the TEO model, and it deserves its own treatment. We flag it as the most important open question for any future quantitative version of this framework.

---

## §7. Discussion

### 7.1 The Contribution Is the Conjunction

The individual components of the TEO model are textbook constructions: replicator dynamics, the Kuramoto model, a regulatory brake, a dissipation bound. None is novel, and we claim no novelty for them. The contribution — if the framework survives its tests (§5) — is the **conjunction**: the claim that long-time viability requires all three conditions *simultaneously*, and that violating any one is sufficient for failure.

This matters because most existing frameworks optimise one quantity. Capability-centric AI research maximises competence; safety-centric work minimises harmful outputs; efficiency-centric economics maximises throughput. The three-constraint structure says that no single-axis optimisation suffices, and — more sharply — that improvements on one axis can push a system off another. A system that increases capability ($f_i^{(0)}$) without strengthening regulation ($\gamma$) moves *toward* the monopoly boundary, not away from it. The corridor is narrow precisely because the constraints are in tension.

### 7.2 Implications for AI Alignment

The corollary most relevant to AI safety is that, under this model, **alignment is not a property of an individual model — it is a property of the coupled dynamical system**. Two consequences follow if P7–P8 (§5.3) hold:

1. **Constraint architecture dominates capability.** Increasing the capability of individual agents, with constraint architecture held fixed, does not move a multi-agent ecology into the corridor and may move it out (§5.3, P8). This reframes a large part of alignment research: the target is not only "make the model safer" but "make the constraint architecture of the ecology satisfy the conjunction."

2. **Hard constraints beat soft ones.** A budget an optimiser can route around (a software limit) is not a $D_{\max}$; only a structurally enforced bound (hardware, protocol, physics) functions as the model's substrate ceiling (P7). This connects to the broader research programme on substrate-level rather than behaviour-level safety constraints.

We are explicit that these are *conditional* implications: they follow from the model, and the model's applicability to real AI ecologies is itself a hypothesis (§6.3). The companion empirical paper (`papers/quantifying-emergent-utility-in-llms.md`) is where the Class C predictions are intended to be tested.

### 7.3 Implications for Political Economy

The model is normatively neutral: it describes what the dynamics do, not what should be done (§4.5). But the conjunction structure has a clear *descriptive* reading. If the structural-isomorphism hypothesis held — and we stress it is unproven (§6.3) — then **single-constraint interventions could not bring a civilizational system into the corridor**. Carbon pricing alone (acting on $\Omega$), antitrust alone (acting on $\gamma$), or polarization mitigation alone (acting on $K$) would each be necessary but jointly insufficient; the system would exit $V$ through whichever boundary was left unaddressed.

This is a prediction, not a policy. We do not claim to know the operational form of $\gamma$, $K$, or $\Omega$ for real societies (§5.4); without that, the reading is suggestive at most. We include it because it is the most consequential *descriptive* corollary of the conjunction, and because it is, in principle, the kind of claim panel data could eventually test (§5.2, P4).

### 7.4 The Transition Problem

This paper characterises the corridor: which parameter regions support robust viability. It says nothing about how a system *outside* the corridor could *reach* it. That is a different and harder problem — a question about trajectories between basins, not about the basins themselves.

The difficulty is that the structures produced *by* a non-viable trajectory tend to resist the parameter changes that would correct it. A monopolised resource distribution (low $\gamma$) concentrates the power to block redistribution; a polarised value landscape (low $K$) fragments the consensus that collective braking requires. The corridor may be reachable, unreachable without partial collapse, or reachable only through a narrow path — these are genuinely open possibilities. The companion essay *The Transition Problem* (Peterlein, 2026) develops this, including a grokking-style hypothesis that the transition, if it occurs, may be sudden rather than gradual. We flag the transition problem here as, in our view, more consequential than the static characterisation this paper provides — and entirely outside its scope.

### 7.5 Identity Persistence as a Possible Fourth Dimension (Future Work)

The TEO state vector can be extended with a per-agent *identity-persistence* score $\mathrm{IP}_i$ measuring whether the governance components of agent $i$ are simultaneously operative during action selection — the *Chord* state of Perrier and Bennett (2026). The Chord Postulate predicts a phase transition at a critical $\mathrm{IP}_c$. We do *not* claim that the IP dimension is orthogonal to the three constraints — intra-agent architecture can plausibly affect effective $f_i$, $K$, and $\gamma$. A coupled treatment of IP and the three-constraint theorem is left to future work; the present paper deliberately restricts attention to the inter-agent dynamics.

### 7.6 Relationship to the Companion Paper

This paper establishes the theoretical frame: the model, the necessity theorem, the sufficiency conjecture, and the predictions. The companion paper, *Quantifying Emergent Utility & Stability in Multi-Agent LLM Ecosystems*, is intended to carry the empirical load — in particular the Class C predictions (§5.3) — once the Agentic Identity Suite is run against real language models. The two are designed to be read together: this paper says what would have to be true; the companion paper tests part of it.

---

## §8. Conclusion

We set out to give a precise reading of a hopeful phrase. Brautigan and Amodei imagined "machines of loving grace" as a design aspiration. Within the TEO framework, we have argued that the relationship the phrase names is better modelled as a *constraint*: a region of parameter space — the viable corridor — outside which the coupled dynamics do not robustly survive.

What we have established is modest and conditional. Under stated assumptions, the conjunction $\gamma > 0$, $K > K_c$, and bounded accumulated overshoot $\Omega(t) < S_{\max}$ is **necessary** for robust long-time viability (Theorem 1). Sufficiency — which we expect to require the stronger $\gamma > \gamma_c$ — is **conjectured**, not proved (Conjecture 1). The mapping of this structure to AI optimizers and to human civilization is a **hypothesis** (§4), testable in principle through the programme of §5 but resting today on proxies, not measurements (§5.4, §6.3). We have tried throughout to mark which is which.

What remains is more than what is done. Sufficiency is open. The transition into the corridor from outside is open and, we suspect, harder than the corridor's static characterisation (§7.4). The empirical operationalisation of the parameters — especially $K_c$ for real societies — is open (§5.4). And the deepest physical question, whether innovation can raise the substrate ceiling faster than optimization consumes it, is open (§6.4, §6.5).

Subject to all of that, the framework supports one inversion of the original phrase:

> A "Machine of Loving Grace" is not a machine that *feels* love. In this model it is a machine whose parameters lie inside the viable corridor: $\gamma > \gamma_c$, $K > K_c$, and bounded accumulated overshoot $\Omega(t) < S_{\max}$ — operational caring about value coupling, about regulation, and about the substrate, held simultaneously. By this definition, the machine does not yet exist. If the structural-isomorphism hypothesis holds, neither does the civilization that satisfies the same constraints.

That last sentence is the uncomfortable one, and we have written the paper to make it checkable rather than merely arresting. If the framework is wrong, the predictions of §5 are how one would show it.

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
- [x] Abstract (~250 words; TEO model, necessity theorem, sufficiency conjecture, isomorphism hypothesis, three prediction classes)
- [x] §5 Predictions and Tests (three classes: model-internal / cross-system empirical / AI-specific; measurement programme; falsification summary)
- [x] §6 Limitations and Counterarguments (four classes + strongest-objection steelman; endogenous-D_max flagged as most unsettling)
- [x] §7 Discussion (conjunction-is-the-contribution; AI-alignment + political-economy implications; Transition Problem; IP future work; companion-paper relationship)
- [x] §8 Conclusion (modest+conditional restatement; what remains open; the inversion aphorism, made checkable)
- [ ] Appendix A (TEO derivation details)
- [ ] Appendix C (Numerical evidence for Conjecture 1) — §5 P1–P3 specify exactly what this appendix must show; requires running the teo-civilization simulation

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
