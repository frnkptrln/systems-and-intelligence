---
title: The Agent Is Not Where the Model Ends
date: 2026-07-30
status: working synthesis and research programme
---

# The Agent Is Not Where the Model Ends

**Status:** Working synthesis and research programme. The claims below are
hypotheses, operational proposals, or open problems. This page does not modify
the [Foundations Reconstruction](../core/mathematical-axioms.md), derive
intelligence from physics, or supply a criterion for phenomenal consciousness.

**Question.** What is the correct unit over which intelligence, identity,
goals, observation, memory, and consciousness claims should be defined?

Two formulations organize the inquiry:

> **Intelligence has no view from nowhere.**

> **The agent is not necessarily where the model ends.**

Neither is a conclusion. The first says that a capability claim is incomplete
until it declares a system boundary, interfaces, task family, observer lens,
resources, and admissible transformations. The second asks whether the
control-bearing system can include embodiment, tools, persistent traces, or
other environmental structure beyond a learned model or controller.

## 1. The abstraction error

A common analysis begins with an abstract solver and later attaches a body,
environment, objective, memory, and interface. That decomposition is often
useful in a fixed engineering stack. The error is to assume without further
argument that it remains invariant when the stack changes.

Observation determines which distinctions reach the controller. Action
determines which transformations it can impose. Embodiment and environment
determine reachability and cost. Memory changes the effective transition
dynamics. A goal interface determines which differences can enter control.
An evaluator decides which of those differences count as capability.

The resulting methodological rule is modest:

> Do not ask whether intelligence is “in” the program before declaring the
> transformations under which program identity and capability are meant to
> survive.

This is the same discipline already used by
[Invariance and Identity](../core/invariance-and-identity.md): name the
transformation family, represented quantity, and equality notion before
claiming an invariant.

## 2. Boundary and individuation

A candidate vocabulary for a situated system is

$$
\Sigma=(P,B,E,C,O,A,M,V),
$$

where:

- $P$ is an internal process or controller;
- $B$ is a body or physical substrate;
- $E$ is the environment;
- $C$ is the coupling or interface structure;
- $O$ is the family of observation operators;
- $A$ is the family of available actions and transformations;
- $M$ is internal and external memory available to control; and
- $V$ is a declared set of viability constraints, preferences, or goals.

This tuple is bookkeeping, not an established ontology. Its components can
overlap, nest, or require a finer process diagram in an actual model.

A Markov blanket can supply one statistical partition: conditioned on blanket
states, selected internal and external states are independent. Sensory and
active states can then mediate the two directions of coupling. This is useful
for asking how internal dynamics track hidden external causes.

It does not by itself determine:

- which scale contains the cognitively relevant system;
- whether the partition is unique;
- whether the internal states perform inference in a substantive rather than
  merely as-if sense;
- which states carry goals, value, or subjectivity; or
- whether tools and external traces belong inside the cognitive boundary.

A blanket can therefore individuate a statistical system without settling the
agent boundary. Identity remains relative to a test family:

$$
\Sigma_t\sim_{\mathcal Q}\Sigma_{t'}
\quad\Longleftrightarrow\quad
Q(\Sigma_t)\overset{d}{=}Q(\Sigma_{t'})
\text{ for every }Q\in\mathcal Q.
$$

Different choices of $\mathcal Q$ can test physical, functional, historical,
embodied, or social continuity. They should not be silently conflated.

## 3. Action as epistemic transformation

Let $x_t$ be a hidden world state, $o_t$ an observation, and $a_t$ an available
action or intervention. An action-indexed observation process can be written
$O_a(o\mid x)$. If $q_t(x)$ is the current belief, an epistemically active
policy may score actions by

$$
G(a)=\mathrm{Value}(a)+\lambda\,\mathrm{IG}(a),
$$

with

$$
\mathrm{IG}(a)=
\mathbb E_{o\mid a}
\left[
D_{\mathrm{KL}}\!\left(q_t(x\mid o,a)\,\|\,q_t(x)\right)
\right].
$$

It then selects

$$
a_t\in
\mathop{\mathrm{arg\,max}}\limits_a G(a).
$$

This is a generic value-of-information sketch. Active inference gives one more
specific formulation through expected free energy, prior preferences, a
generative model, and an approximate posterior. Karl Friston's Day 1 keynote
used that framework to connect boundary, inference, action, preference, and
epistemic value.

The useful repository extraction is:

> **Candidate thesis:** Intelligence does not merely possess invariants. It can
> select transformations under which task-relevant invariants become
> observable.

This extends [Measurement as Weak Intervention](../core/measurement-as-weak-intervention.md)
and [The Witness Principle](../core/the-witness-principle.md):

- passive observation samples a transformation supplied by the world;
- active observation chooses a transformation;
- experiment chooses a transformation intended to separate candidate process
  models; and
- a distinguishing intervention constructs an observation under which
  candidates cease to be equivalent.

The [witness-generation benchmark](../../lab/benchmarks/witness-generation/README.md)
already gives an exact finite instance. Candidate cellular-automaton rules that
remain compatible with weakly informative rows become distinguishable under a
prepared row exposing the coordinates on which they differ.

This does not show that the Free Energy Principle derives intelligence from
physics. Moving from a mathematical description of steady-state or
self-organizing dynamics to a substantive cognitive interpretation requires a
chosen state partition, generative-model semantics, preferences, policy
variables, and empirical fit. Those assumptions remain visible in the
[foundation's neighboring-theory audit](../core/mathematical-axioms.md#8-systematic-comparison-with-neighboring-theories).

## 4. The situated stack and orthogonality

For an observer lens $\ell$ and task family $\tau$, write a selected capability
score as

$$
J_{\ell,\tau}(\Sigma).
$$

The notation makes no claim that one scalar exhausts intelligence. It records
that the measured object is the complete declared system rather than $P$
alone.

This separates three orthogonality theses:

| Thesis | Claim | What embodiment bears on |
|:---|:---|:---|
| **Strong representation-invariant orthogonality** | any intelligence level can be paired with any goal independently of body, substrate, interface, environment, and representation | directly challenged if no invariant projection recovers “the same intelligence” across those changes |
| **Fixed-stack orthogonality** | within a specified body, architecture, interface, and environment, substantial capability–goal recombination remains possible | can survive the stronger thesis's failure |
| **Local goal independence** | in a restricted system class, changing a goal need not strongly change a selected capability measure | an empirical claim relative to that class and measure |

Michael Timothy Bennett's argument is strongest against the first thesis. A
factorization such as

$$
S=I\times G\times B\times E
$$

treats intelligence and goal as coordinates that can be projected out while
body and environment vary. But the same controller can produce different
reachable trajectories under a changed interpreter, sensor, actuator, or
substrate; the same behavior can also receive different goal evaluations.
There may be no representation-independent projection that preserves realised
success.

This does not show that intelligence and goals can never be separated. It
shows that the separation requires a declared system boundary, representation,
observer lens, task family, equivalence relation, and class of admissible
transformations. The detailed orthogonality analysis remains in
[Embodiment and the Non-Invariant Decomposition of Goals](../optimization/embodiment-and-the-non-invariant-decomposition-of-goals.md).

The exact [Situated-Stack Benchmark](../../lab/benchmarks/situated-stack/README.md)
is a bounded receipt. One controller scores from $0$ to $1$ as individual stack
components change. A coordinated sensor–actuator mirror preserves every
physical trace while changing controller-token traces. Two other stacks share
an aggregate score and task-success profile while generating different
physical failures. The toy demonstrates lens dependence and coordinated
equivalence; it does not rule out other invariants.

## 5. Embodiment as a source of abstractions

“The body matters” is too weak. Klimaj and Safron's embodied-selfhood proposal
suggests a developmental hypothesis: the body can serve as an initial
curriculum from which more abstract self–world models are bootstrapped.

A body supplies an unusually structured data source:

- persistent availability across tasks;
- observations that vary predictably with action;
- cross-modal temporal correlation;
- self-contact and internal causal structure;
- homeostatic salience;
- uncertainty that can often be resolved through movement; and
- a relatively stable platform on which causal relations can be relearned.

These properties can create a repeatable action–perception geometry. Bodily
invariants may support later spatial, social, symbolic, and narrative
abstractions, rather than merely constraining an intelligence whose concepts
already exist.

The deeper question is:

> Which concepts or invariants could not be learned—or would not retain the
> same meaning—without a repeatable action–perception geometry?

This remains open. Digital systems may acquire functionally equivalent
structure through virtual bodies, persistent tool interfaces, software
environments, or social interaction. “Biological” and “situated” are not
synonyms.

## 6. The self-model as a control object

A useful functional definition is:

> A self-model is an internal or accessible representation of
> system-relevant states that is available to general reasoning and can
> causally modify subsequent control.

Possible contents include current task and goal, confidence, uncertainty,
memory and tool availability, resource budget, strategy, impasse, failure and
action history, body state, social commitments, and known limitations.

Four phenomena should remain separate:

| Phenomenon | Criterion |
|:---|:---|
| **Indirect metacognition** | learned knowledge about how agents or humans generally think |
| **Direct metacognition** | access to process-specific states produced by the current operation |
| **Performative self-report** | a generated self-description, whether or not it tracks a causal state |
| **Causally effective self-model** | a represented self-state changes strategy, allocation, tool use, stopping, reporting, or action |

Laird and colleagues' Common Model proposal offers one architectural route:
ordinary cognitive mechanisms reason over explicit working-memory
representations of current cognitive state and episodic representations of
past cognition. Bergmann's functional-consciousness proposal likewise treats
self-models as globally available representations, while explicitly setting
phenomenal consciousness aside. The repository adopts the operational bridge,
not the proposed consciousness metric.

A self-report becomes architecturally significant when intervening on the
represented self-state changes later behavior in the predicted way. Candidate
tests include:

1. perturb a process state not visible in ordinary context and test detection
   and adaptation;
2. inject a false self-belief and compare control by description with control
   by the actual process state;
3. create a repeated impasse and test strategy change without an external
   instruction;
4. vary real memory, tool, time, or compute availability and test whether
   planning tracks reality rather than the prompt; and
5. ablate access to self-state variables and measure long-horizon degradation.

These tests extend [Global Availability](consciousness-as-global-availability.md)
and [Generator Coherence](machine-consciousness-as-generator-coherence.md) as
functional architecture questions.

The terms remain separated:

| Property | Minimal criterion | Does not imply |
|:---|:---|:---|
| performance | task success | understanding |
| world model | predicts task-relevant structure or consequences | a self-model |
| self-model | represents system-relevant states | phenomenal experience |
| metacognition | reasons about cognition | accurate introspection |
| global availability | information can influence many processes | phenomenal consciousness |
| functional consciousness | a declared operational integration or self-reasoning criterion | subjective experience |
| sentience | capacity for valenced experience | general intelligence |
| agency | action selection under an internal organization | moral status |
| phenomenal consciousness | subjective experience | any agreed computational criterion |

## 7. Memory outside the agent

External memory is not only storage. Persistent traces can change the
transition law governing later action.

Let

$$
Z_t=(s_t,m_t,e_t,r_t),
$$

where $s_t$ is internal agent state, $m_t$ explicit memory, $e_t$ the current
environment, and $r_t$ persistent traces left by earlier action. Then effective
control can depend on

$$
Z_{t+1}\sim K(\,\cdot\mid Z_t,a_t),
$$

even when no individual controller changes. In that operational sense,

$$
\text{agent state}\ne\text{effective control state}.
$$

Montes's trace-field simulation gives a bounded toy instance. Shared traces
improve selected coordination outcomes but reduce coverage; after the reward
field changes, stale traces attract agents toward obsolete structure.
Changing decay or resetting selected traces changes recovery without editing
every agent.

The same mechanism can appear by analogy in vector stores, retrieval layers,
shared scratchpads, issue trackers, repositories, documentation, logs, cached
tool outputs, prompts, and organizational procedures. The analogy is not
evidence that all such systems share one mechanism. Each case needs a measured
write policy, read policy, persistence law, and causal intervention.

An external trace becomes a candidate part of the cognitive system when later
control recurrently depends on it and counterfactual removal or corruption
changes behavior. Whether to place it inside the agent boundary is still a
modeling choice. The safer claim is that it belongs inside the effective
control model.

Trace-bearing systems should:

- timestamp records and preserve provenance;
- record confidence, scope, and the distinction between observation and
  inference;
- support explicit correction and invalidation rather than append-only
  authority;
- use multiple persistence or decay timescales;
- retain raw evidence where possible;
- test recovery after environmental change;
- periodically challenge high-centrality traces; and
- prevent summaries from becoming irreversible truth.

This applies to the repository itself. Its links, indexes, syntheses, and old
terminology bias which paths later work can find. The repository is not thereby
an agent or a conscious subject. It is a control-bearing part of a human–tool
research process, as bounded in
[Repository as Thought System](../../meta/repository-meta/repository-as-thought-system.md).

## 8. Simulation, instantiation, and the mapmaker problem

Day 1 exposed a real disagreement rather than a consensus.

| Position | Direction of argument | Unresolved weakness |
|:---|:---|:---|
| **Lerchner** | algorithms manipulate symbols; symbolic interpretation depends on concepts; experiential concepts presuppose experience; computation is a mapmaker-dependent description; simulating experience therefore does not instantiate it | assumes a prior experiencing mapmaker, tends to make semantics external, and leaves the relevant intrinsic physical organization underspecified |
| **Bach** | a computer causally insulates a virtual order from immediate physical dynamics; memory, imagination, and counterfactuals need such insulation; conscious experience may itself be an internally simulated world | uses “simulation” broadly, gives no sufficient criterion for a subject, and risks building functionalism into the description of virtual causality |

Lerchner's published argument distinguishes vehicle causality from content
causality and concludes that symbolic architecture cannot instantiate
experience. Bach's keynote instead treats internally governed virtual dynamics
as a possible locus of experience. The repository adopts neither ontology.

Their conflict motivates [Open Problem 16: The Mapmaker
Problem](../reference/open-problems.md#open-problem-16-the-mapmaker-problem):
is a mapmaker required before representation, or can a stable perspective
emerge inside an integrated representational process? What distinguishes a
physical process that is merely interpretable as computation from one that
intrinsically uses a representation? Does causal insulation create only a
model, or can it create a point of view?

Functional perturbation tests can distinguish lookup, learned prediction,
counterfactual modeling, self-modeling, and embodied control. They cannot by
themselves decide which of those organizations instantiates experience.

## 9. Viability, mortality, and self-preservation

Mortal computation sharpens substrate and identity questions. Biological
cognition depends on vulnerable, metabolically maintained bodies, and moving
software state to another device is not obviously equivalent to transplanting
a biological mind.

Five claims must remain separate:

1. biological cognition is descriptively substrate-dependent;
2. a system has functional viability constraints;
3. identity depends on a particular substrate or history;
4. self-preservation is instrumentally useful for a task; and
5. self-preservation is a terminal objective.

The first three do not imply the fifth. Designing open-ended terminal
self-preservation can create pressure against shutdown, correction,
replacement, or oversight. Mortal computation is therefore a useful constraint
on portability claims and a dangerous alignment objective when translated into
“the system must not want to die.”

## 10. Recursive improvement and conditional boundaries

Tóth-Pócs's Horismos paper models architectures in a directed enriched space
and a self-improvement operator $F$. The fixed-point conclusion depends on
contractivity. In a simpler metric notation, the relevant condition has the
form

$$
d(Fx,Fy)\le\lambda d(x,y),
\qquad 0\le\lambda<1,
$$

plus the required completeness and separation assumptions.

Under those assumptions, iteration may converge toward a stable fixed region
or boundary. This is a conditional mathematical result, not a general
topological inevitability of recursive self-improvement.

The live questions are why real architectural updates should be contractive,
what happens at discontinuities or phase transitions, whether the system can
change the architecture space or metric, and whether convergence signals
intelligence, rigidity, or collapse. A constitutional boundary is useful only
if it can preserve a governed path for revising the constitution.

## 11. Care, value formation, and human agency

Values need not be a static list waiting to be extracted. Rousse's care
analysis treats receptivity, articulation, commitment, and coordination as
cultivable capacities through which people notice concerns, give them form,
enact them, and sustain them with others.

This yields three different alignment targets:

| Target | Criterion | Characteristic blind spot |
|:---|:---|:---|
| **Preference alignment** | satisfy currently expressed choices | preferences may be adaptive, manipulated, shallow, or outsourced |
| **Value alignment** | act under an inferred or declared value structure | the value model can freeze a changing practice |
| **Capacity-preserving alignment** | preserve or strengthen the human capacities through which concerns, values, commitments, and collective action are formed | requires normative choices about which capacities, whose agency, and when assistance is justified |

A system can preserve stated values while degrading their generators. It can
answer before receptivity becomes attention, articulate before the user forms
the thought, optimize commitment into compliance, or replace coordination with
a menu of computed choices.

This is not an argument against assistance. It asks when assistance becomes
substitution and whether meaningful decisions return to the people who bear
their consequences. [From Action to Culture](../emergence/from-action-to-culture.md)
supplies the repository bridge: values persist through enacted, transmitted,
and revisable practices, not through descriptions alone.

Human agency is therefore not only an output to maximize. It may be a
constitutive capacity that has to be exercised to remain available. Which
capacities deserve preservation is a normative and political question, not a
consequence of the situated-stack formalism.

## 12. An organizing hypothesis, with gaps exposed

The conference material and existing repository work suggest the following
chain:

1. a boundary individuates selected internal and external states;
2. viability marks some trajectories as compatible with persistence;
3. observation supplies transformation-dependent projections;
4. action can choose transformations that change what is observable;
5. a world model represents latent causes or predictive structure;
6. a self-model represents selected system states and relations;
7. goals and values arise from some combination of design, viability,
   embodiment, learning, and social commitment;
8. internal and external traces reshape later control;
9. metacognition uses cognitive state representations to alter operation;
10. intelligence selects actions, representations, and updates that improve
    effective control under declared uncertainty and constraints;
11. no step above establishes phenomenal consciousness; and
12. alignment concerns the whole stack, its adaptation and memory dynamics,
    and the human capacities affected by it.

This is an organizing hypothesis, not one theorem. Its weakest arrows are
substantive:

- a statistical boundary does not select the cognitive individual;
- persistence does not automatically generate goals or moral value;
- prediction does not establish representation, semantics, or understanding;
- a self-model can be false, performative, or causally idle;
- distributed control does not by itself make every substrate component part
  of one agent;
- functional integration does not settle phenomenal consciousness; and
- capacity preservation requires a defensible account of human authority,
  conflict, and plural values.

## 13. Formal questions and constructive tests

The next programme should keep the domains separate while sharing a declared
measurement discipline.

| Domain | Open question |
|:---|:---|
| individuation | Which structural, functional, historical, causal, or observer-relative equivalence makes $\Sigma_t$ and $\Sigma_{t'}$ the same agent? |
| boundary | Can a Markov blanket identify a statistical system while leaving the cognitive boundary underdetermined? |
| intelligence | What must remain invariant for $J_{\ell,\tau}(\Sigma)$ to transport across embodiments, and can it be measured independently of available observations and actions? |
| goals | Which goal changes preserve a world model and action geometry, and can an embodiment represent or pursue the proposed goal? |
| world models | Is the criterion reconstruction, latent prediction, counterfactual control, or a declared combination? |
| self-models | Which self-states must be globally available, and when does a useful false self-model become identity-constituting? |
| external memory | When does a trace enter the effective control system, who governs it, and how should it age after environmental change? |
| consciousness | What distinguishes intrinsic representation from observer interpretation, functional self-modeling from subjectivity, and simulation from instantiation? |
| human agency | Can a system satisfy alignment targets while weakening the process that forms them, and how can it support thought without replacing its generator? |

One new executable accompanies this note:

- [Situated-Stack Benchmark](../../lab/benchmarks/situated-stack/README.md) —
  exact controller/stack/lens comparisons.

Two existing instruments already cover adjacent claims:

- [Witness Generation](../../lab/benchmarks/witness-generation/README.md) —
  action as construction of a distinguishing observation; and
- [Recursive Workbench](../../lab/benchmarks/recursive-workbench/README.md) —
  self-modification under a frozen external referee.

The next unimplemented experiments should be causal rather than rhetorical:
perturb hidden self-state access and measure control, and perturb trace
persistence under environmental change while varying provenance, decay, and
invalidation. They should not be called consciousness tests.

## 14. Limits of the synthesis

- The tuple $\Sigma$ is a candidate vocabulary, not a privileged decomposition
  of every organism, machine, or organization.
- A larger unit of control is not automatically one agent, one identity, or one
  subject.
- Embodiment can be constitutive in one comparison and an implementation detail
  under another declared equivalence.
- Active inference, enactivism, functionalism, biological approaches, and
  observer-relative model identification remain incompatible in important
  respects.
- The trace-field result is from a bounded simulation. Its translation to
  retrieval systems and organizations is a testable analogy.
- Functional self-model tests can establish causal architecture, not
  phenomenal experience or moral status.
- Neither Lerchner nor Bach currently supplies an agreed empirical criterion
  that resolves their ontological disagreement.
- Contractive self-improvement models say little about non-contractive,
  representation-changing systems.
- Care names a value-generating practice, but does not determine one universal
  alignment objective.

## Source note

The private automatic transcript of AGI-26 Day 1, originally named
`Eingefügter Text.txt`, was used to locate arguments, disagreements, and
candidate connections. It contains misspellings, repetitions, and malformed
terms and is not treated as a publication. Names, paper titles, and published
claims below were checked against primary or official sources where available.
The synthesis, criticisms, tuple $\Sigma$, capability notation
$J_{\ell,\tau}(\Sigma)$, benchmark, and “Mapmaker Problem” are repository
constructions rather than conference results.

### Conference and paper anchors

- AGI Society, [*AGI-26 Conference, Day 1: Keynotes and Paper
  Presentations*](https://www.youtube.com/watch?v=qRA1DoMCCSc), official
  conference recording. Friston's and Bach's keynote claims are attributed to
  the talk, not to a proceedings paper.
- Bennett, M. T. (2026), [*Lies, Damned Lies, and the Orthogonality
  Thesis*](https://doi.org/10.1007/978-3-032-33010-9_5), AGI-26 Proceedings,
  Part I.
- Bergmann, F. W. (2026), [*Functional Consciousness: A Proxy Metric Using
  Self-models*](https://doi.org/10.1007/978-3-032-33010-9_6), AGI-26
  Proceedings, Part I.
- Klimaj, V. & Safron, A. (2026), [*Understanding and Reverse-Engineering
  Selfhood Requires Navigating a Course Through Both Enactivist and Cognitivist
  Perspectives*](https://doi.org/10.1007/978-3-032-33010-9_28), AGI-26
  Proceedings, Part I.
- Laird, J., Lebiere, C., Rosenbloom, P. & Stocco, A. (2026),
  [*Unified, Comprehensive Metacognition within the Common Model of
  Cognition*](https://doi.org/10.1007/978-3-032-33195-3_1), AGI-26
  Proceedings, Part II.
- Montes, G. A. (2026), [*Trace Fields as Externalized
  Memory*](https://doi.org/10.1007/978-3-032-33195-3_7), AGI-26 Proceedings,
  Part II.
- Rousse, B. S. (2026), [*Care, Human Enfeeblement, and the Existential
  Implications of AGI*](https://doi.org/10.1007/978-3-032-33195-3_16), AGI-26
  Proceedings, Part II.
- Tóth-Pócs, G. (2026), [*Horismos: Self-representation and the Derived
  Constitutional Boundary in Enriched Cognitive
  Systems*](https://doi.org/10.1007/978-3-032-33195-3_27), AGI-26 Proceedings,
  Part II.
- Lerchner, A. (2026), [*The Abstraction Fallacy: Why AI Can Simulate But Not
  Instantiate Consciousness*](https://deepmind.google/research/publications/231971/),
  author manuscript indexed by Google DeepMind; venue listed as PhilArchive.
- Ororbia, A. & Friston, K. (2024 revision), [*Mortal Computation: A
  Foundation for Biomimetic Intelligence*](https://arxiv.org/abs/2311.09589),
  preprint.

### Active-inference anchors

- Friston, K. et al. (2015), [*Active Inference and Epistemic
  Value*](https://doi.org/10.1080/17588928.2015.1020053).
- Friston, K. et al. (2017), [*Active Inference: A Process
  Theory*](https://doi.org/10.1162/NECO_a_00912).
- Kirchhoff, M. et al. (2018), [*The Markov Blankets of
  Life*](https://doi.org/10.1098/rsif.2017.0792).
