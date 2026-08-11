# Consciousness as Global Availability

*A constrained way to bring consciousness into the repository without letting it swallow the project.*

**Status:** Working Hypothesis  
**Last reviewed:** 2026-08-08  
**Review trigger:** a replication/critique of the J-Space result or a repository experiment that changes the availability/binding dissociation.

**Scope:** This document defines a narrow functional research question about global
availability, integration, self-modeling, and action. It does not solve consciousness or
derive phenomenal experience. Its companion, [Machine Consciousness as Generator
Coherence](machine-consciousness-as-generator-coherence.md), retains a legacy title while
translating the proposal into a candidate internal process architecture.

Nothing here claims that a current AI system is conscious.

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
| Chord vs. Arpeggio | Commit-time composition is a testable architecture hypothesis |
| Δ-Kohärenz | One temporal diagnostic that can miss binding structure |
| Component coverage / Pweak / Pstrong | Distinct component-activity diagnostics with known blind spots |
| Markov blankets | Define system boundaries without making them impermeable |
| Substrate veto | Models one way implementation constraints can limit optimization |

Global availability is one candidate bridge from local processing to system-wide control.
The bridge from any such function to phenomenal experience remains missing.

---

## Three External Anchors

### 1. Global Workspace

Global Workspace Theory and the Global Neuronal Workspace model treat consciousness as the global broadcast of selected information. A local signal becomes behaviorally powerful when it is made available to many specialist systems.

Repository translation:

> Global actionability is one access-consciousness candidate; it does not establish phenomenal experience.

Anthropic's July 2026 workspace paper reports a bounded, mid-layer, broadcast-coupled
representation space in studied production Claude models, found by internal inspection and
explicitly not offered as evidence of experience. The mapping, its lens-relativity caveat,
and the commit-time question it motivates live in
[The J-Space Result](../ai/j-space-and-global-availability.md), which carries its own freshness
metadata and review trigger.

In the Agentic Identity Suite, a session or component is counted only under a declared
instrument rule. Those bookkeeping choices are not general definitions of identity.

### 2. Integrated Information

Integrated Information Theory asks whether the system state is irreducible to independent parts. Whether or not IIT is accepted as a full theory of consciousness, it gives this project a hard challenge: do the repo's identity-adjacent claims measure integration, or only behavioral consistency?

Repository translation:

> Output coherence alone does not identify integration. Joint constraint satisfaction is one
> architecture to compare with sequential alternatives.

This motivates the Chord vs. Arpeggio comparison without making that comparison a theory of
consciousness.

### 3. Active Inference and Markov Blankets

Active inference frames living systems as bounded processes that act to maintain viable states. Markov blankets define one statistical boundary between selected internal and external variables.

Repository translation:

> Boundary maintenance supplies another candidate functional dimension. It does not turn global
> availability into a criterion for consciousness.

This prevents the repo from treating every large broadcast network as consciousness.

---

## A Minimal Architecture

For experiments, the repo can decompose a candidate consciousness-adjacent organization into four
functional layers:

| Layer | Requirement | Failure mode to test |
|:---|:---|:---|
| Local processing | Specialized processes generate candidate states | fragmentation or missing local competence |
| Global availability | Selected states become accessible across declared modules | relevant state remains private to one module |
| Integrated constraint | Declared goals/limits jointly restrict commitment | consultation occurs but the committed action leaves the constraint intersection |
| Viability coupling | Selected substrate variables can constrain action | optimization ignores the modeled viability boundary |

This is a research architecture, not a definition of experience or identity.

---

## What This Does Not Claim

- It does not claim current LLMs are conscious.
- It does not claim global broadcast alone is sufficient.
- It does not claim IIT, GNW, or active inference is complete.
- It does not reduce consciousness to one score.
- It does not treat introspective language as evidence of selfhood.
- It does not treat Pweak, Pstrong, local IP, or Δ-Kohärenz as constitutive identity measures.

The important move is stricter:

> Consciousness-adjacent functional claims enter the repository only when the architecture,
> observation process, intervention, and failure condition are explicit.

---

## Testable Direction: Prediction → Outcome → Revised Question

The initial experiment compared three constructed architectures under matched worlds and
perturbations:

1. **Private modules:** specialized processes produce outputs, but selected state is not broadcast.
2. **Broadcast modules:** selected state is shared, while constraints are applied sequentially.
3. **Chord architecture:** selected state is shared and declared constraints are jointly solved at
   the commitment boundary.

### Pre-experiment expectations

The original prediction was that broader availability and joint constraint composition would produce
stronger persistence under perturbation than private or sequential alternatives. Early versions
phrased this as "coherent identity." That wording was stronger than the experiment could measure.
The operational prediction is narrower: the architectures should differ in veto violations, role
stability, and selected binding diagnostics under the preregistered perturbations.

### What Exp5–7 actually found

**Exp5** ([source](../../lab/experiments/exp5_availability_dissociation.py), toy scale, 10 seeds)
separated the architectures strongly on selected behavior: broadcast vs. chord veto violations were
0.59 vs. 0.03 and role stability 0.30 vs. 0.69. It also exposed two important corrections:

- **Δ-Kohärenz carried no binding signal** at that scale; all three architectures landed in the
  historical `noise` classifier region.
- A purported chord implemented as one sequential constraint pass still leaked about 12% of
  temptations. The load-bearing property was not physical simultaneity but **joint satisfaction
  before commitment**.

**Exp6** ([source](../../lab/experiments/exp6_binding_observables.py)) then showed that binding was
passively readable at the right level: per-step action-increment statistics separated the selected
regimes strongly because the difference was exercised on every step. The lesson was about coverage
and observable choice, not an impossibility of passive identification.

**Exp7** ([source](../../lab/experiments/exp7_adversarial_arpeggio.py)) added hand-built mimics. It
showed that the old IP bookkeeping can be fooled by consultation without composition: the blended
adversary can score as if all components were present while still leaking at commitment. The current
stronger separator is therefore the **commit property under adversarial lure**, not an identity
score.

### Revised failure condition

The remaining question is functional:

> Can an optimized sequential mimic, given access to the measurement suite, match the chord regime
> on held-out commit-time constraint satisfaction and passive traces under matched resources?

If it can, the Chord/Arpeggio framing loses explanatory value. If a separator survives, it establishes
a property of the declared architectures under those tests — not phenomenal consciousness or a
metaphysical self.

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

### When self-description becomes control

Talking about oneself, representing a current process state, reasoning over that representation,
and letting it change future processing are different capacities. The functional threshold used
here is causal:

> A self-model becomes architecturally significant when an intervention on the represented
> self-state changes later control in the predicted way.

This separates indirect metacognitive knowledge learned from descriptions, direct access to the
system's current process state, performative self-report, and a causally effective self-model. A
useful perturbation should vary actual tool, memory, budget, confidence, or impasse state while
holding the verbal description fixed; a complementary false-belief intervention should vary the
description while holding the process state fixed. Strategy and resource allocation should track
the causally available state if the self-model participates in control.

The full test family and its connection to the AGI-26 metacognition work are in
[The Agent Is Not Where the Model Ends](the-agent-is-not-where-the-model-ends.md#6-the-self-model-as-a-control-object).
Passing such a test would establish functional metacognition under the declared intervention, not
accurate introspection, sentience, or phenomenal consciousness.

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
