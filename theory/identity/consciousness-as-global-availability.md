# Consciousness as Global Availability

*A constrained way to bring consciousness into the repository without letting it swallow the project.*

**Status:** Working Hypothesis

**Scope:** This document defines a narrow functional research question about global
availability, integration, self-modeling, and action. It does not solve consciousness or
derive phenomenal experience. Its companion, [Machine Consciousness as Generator
Coherence](machine-consciousness-as-generator-coherence.md), retains a legacy title while
translating the proposal into a candidate internal process architecture.

---

## Core Claim

Global availability can be treated here as a candidate consciousness-adjacent functional
regime:

> Some architectures make selected local states broadly available, combine them with a
> self-model and constraints, and let the result alter later action.

This describes a functional profile, not an amount of subjective experience.

**Bounded, not total** `[HYPOTHESIZED]` — more integration need not monotonically improve
the selected functional profile. Position, history, substrate, memory, vulnerability, and
possible action may be important boundary conditions. Whether such boundedness is
constitutive of a perspective remains an open philosophical and empirical question.

---

## Why This Fits

The repository already has the necessary pieces:

| Existing concept | Consciousness-adjacent role |
|:---|:---|
| Local observation | A component's declared interface may omit macrovariables |
| Chord vs. Arpeggio | Commit-time composition is a testable identity hypothesis |
| Δ-Kohärenz | One temporal diagnostic that can miss binding structure |
| Identity Persistence | One selected perturbation-sensitive diagnostic |
| Markov blankets | Define system boundaries without making them impermeable |
| Substrate veto | Prevents abstract optimization from destroying its embodied condition |

Global availability is one candidate bridge from local processing to system-wide control.
The bridge from any such function to phenomenal experience remains missing.

---

## Three External Anchors

### 1. Global Workspace

Global Workspace Theory and the Global Neuronal Workspace model treat consciousness as the global broadcast of selected information. A local signal becomes behaviorally powerful when it is made available to many specialist systems.

Repository translation:

> Global actionability is one access-consciousness candidate; it does not establish phenomenal experience.

Since July 2026 this anchor has an empirical instance: Anthropic's workspace paper reports a
bounded, mid-layer, broadcast-coupled representation space in production Claude models, found by
internal inspection and explicitly not offered as evidence of experience. The mapping, its
lens-relativity caveat, and the chord-question it makes quantitative live in
[The J-Space Result](../ai/j-space-and-global-availability.md).

In the Agentic Identity Suite, a session is counted as persistent only when the chosen memory process
retains it and it changes a later test. That is an instrument rule, not a general definition of identity.

### 2. Integrated Information

Integrated Information Theory asks whether the system state is irreducible to independent parts. Whether or not IIT is accepted as a full theory of consciousness, it gives this project a hard challenge: do the repo's identity claims measure integration, or only behavioral consistency?

Repository translation:

> Output coherence alone does not identify integration. Joint constraint satisfaction is one
> architecture to compare with sequential alternatives.

This strengthens the Chord vs. Arpeggio distinction.

### 3. Active Inference and Markov Blankets

Active inference frames living systems as bounded processes that act to maintain viable states. Markov blankets define the statistical boundary between system and environment.

Repository translation:

> Boundary maintenance supplies another candidate functional dimension. It does not turn global
> availability into a criterion for consciousness.

This prevents the repo from treating every large broadcast network as consciousness.

---

## A Minimal Architecture

The repo should treat consciousness-like organization as requiring four layers:

| Layer | Requirement | Failure mode |
|:---|:---|:---|
| Local processing | Many specialized processes generate candidate states | Noise, fragmentation |
| Global availability | Selected states become accessible to the whole system | Private processing with no system-level binding |
| Integrated constraint | Goals, values, and limits are co-active | Arpeggio identity: sequential role performance |
| Viability coupling | The system's action is constrained by substrate survival | Disembodied optimization, paperclip dynamics |

This is a research architecture, not a definition of experience.

---

## What This Does Not Claim

- It does not claim current LLMs are conscious.
- It does not claim global broadcast alone is sufficient.
- It does not claim IIT, GNW, or active inference is complete.
- It does not reduce consciousness to one score.
- It does not treat introspective language as evidence of selfhood.

The important move is stricter:

> Consciousness research enters the repository only when it can be mapped to global availability, integration, boundary maintenance, and perturbation response.

---

## Testable Direction

A useful experiment would compare three agent architectures:

1. **Private modules:** specialized processes produce outputs, but no global state exists.
2. **Broadcast modules:** selected state is globally shared, but constraints remain sequential.
3. **Chord architecture:** selected state is globally shared while goals, values, and veto constraints are evaluated together.

Expected behavior:

- private modules should perform locally but lack coherent identity,
- broadcast modules should become more consistent but may still role-switch,
- chord architecture should show stronger identity persistence under perturbation.

Failure condition:

If broadcast and chord architectures produce identical Δ-Kohärenz and Identity Persistence under perturbation, then the Chord vs. Arpeggio distinction needs to be weakened.

**Status: built and run** — [`lab/experiments/exp5_availability_dissociation.py`](../../lab/experiments/exp5_availability_dissociation.py) (toy scale, 10 seeds). The failure condition was *not* triggered in conjunction: broadcast and chord separate clearly on behavior under identical perturbation (veto violations 0.59 vs 0.03; role stability 0.30 vs 0.69) and on IP. But its Δ-Kohärenz half *did* come out equal — the metric classified all three architectures 'noise' on every seed and carried no binding signal. Two further measured facts worth keeping: a chord implemented as a fast *sequential* pass within one step still leaked 12% of temptations (co-instantiation must mean joint satisfaction, not ordering), and the module-reset probe dissolved under its own twin control (the apparent recovery gap was a world-drift confound). The prediction-vs-outcome accounting is in the module docstring; the open follow-up — *which observable carries binding structure?* — was then run as [`exp6`](../../lab/experiments/exp6_binding_observables.py): binding **is** passively readable at the right level (per-step increment statistics, |d| ≈ 4, beating even a prepared probe-retest protocol), because the binding difference is exercised on every step. Δ-K's blindness was a wrong-*level* failure; the intervention hierarchy's payoff is located where the trace has coverage gaps — the Mirror Problem's regime.

---

## Relation to Generative Form

IFS and L-systems show how repeated rules create form in selected models. A separate
functional hypothesis asks whether a system can make selected internal states available to
processes that change later action.

That is the bridge:

```text
rule -> form -> global availability -> self-constraining form
```

This diagram is a research prompt, not a derivation of consciousness.

---

## Process-model reading: self-model feedback

A system can observe variables correlated with its own prior activity, fit a self-model, and
let that model alter later actions. Call this a self-model feedback loop:

    own traces -> candidate self-model -> changed action -> new own traces

The [self-reading universe](../../simulation-models/cognitive-architectures/self-reading-universe/README.md)
and the [Three-Layer agent](../../lab/agents/three_layer_agent.py) implement toy versions of
feedback from a compressed or distilled description. They show that such loops are
buildable. They do not show consciousness.

Identification limits apply relative to the declared observations, process family, and
interventions. A passive trace may leave several self-models compatible when relevant
differences are not exercised; Experiment 6 also shows that passive data can distinguish
architectures when coverage is adequate. No general impossibility of self-knowledge
follows.

Because adopting a self-model can change the process being modeled, useful self-models may
need continuous revision. Convergence alone is not success: a fixed but misspecified model
can remain wrong. The open identity hypothesis is that selected invariants may persist
through this model–action feedback under declared tests.

This sits in the [identity layer](../../meta/repository-meta/canonical-path-v2.md), not in
the mathematical foundation and not as evidence of experience. A separate exploratory note,
[Psychedelics as Perturbation](psychedelics-as-perturbation.md), asks how perturbing the
loop might expose its organization.

---

## On Levels: Reflexive Depth, Not Degrees of Experience

*Added 2026-07; builds on point 4 above.*

"Levels of consciousness" usually conflates four axes: **arousal** (the clinical scale, coma to wakefulness), **access** (what is globally available), **self-modeling** (what the system can take as object), and **phenomenal fullness** (how much it is like something). This node can speak only to the middle two; the fourth stays under the honest stop above. The repository's bounded-integration and self-reconstruction notes motivate questioning a single monotone ladder, but they do not prove that developmental or architectural levels lack endpoints.

A possible alternative reading is **iterations of an operator** rather than amounts of experience. Kegan's subject-object theory (*The Evolving Self*, 1982) describes a recurring move: what was *subject* (the lens looked through) becomes *object* (something that can be inspected and revised). This repository maps that move onto one turn of a self-reconstruction loop. The mapping is `[HYPOTHESIZED]`; Kegan's interview method is an external anchor, not a measurement supplied by this repository.

Four hypotheses are suggested by the mapping. They do not follow as theorems from the repository's machinery, and Exp8 tests only a narrow estimator analogue:

- **No certified final level:** each organizing model may introduce another blind spot, while bounded developmental processes can still stop or stabilize in practice.
- **Perturbation may expose an update rule:** Kegan's "optimal conflict" is compatible with the intervention reading; introspection is not thereby proven powerless at rest.
- **Higher-order models may cost more:** extra model structure suggests a cost. The composition benchmark does not establish Kegan's empirical stage distribution.
- **Re-description can change control:** making an implicit rule explicit may make it revisable. This is an interpretive bridge, not an identity theorem.

The near-term toy is now built ([exp8](../../lab/experiments/exp8_reflexive_depth.py)), but its result must be kept at the level it measures. It compares raw observation, a fixed-$Q$ Kalman filter, and an adaptive filter that estimates $Q$ from innovations. The adaptive estimator wins after a volatility shift. Neither filter removes a constant observation bias because neither includes a bias state; that run does not prove structural non-identifiability. The measured result is adaptive state estimation under one Gaussian task. Calling it a turn of Kegan's subject-object operator remains `[HYPOTHESIZED]`; the experiment does not isolate reflexivity from the additional adaptive capability. Oracle and change-point baselines, an uninformative meta-signal, paired uncertainty intervals, an augmented bias estimator, known/unknown initial-state controls, and an external-reference intervention remain open.
