# Open Problems

*Formally unresolved questions in this project. These are the most generative parts of the work — documentation here is an invitation to contribute, not an admission of failure.*

---

## Open Problem 1: The Mirror Problem

> **Foundation context:** This is a test-selection problem under the [Foundations
> Reconstruction](../core/mathematical-axioms.md). Behavior is one observation process; interaction
> history, memory architecture, and runtime are candidate model components. No absolute identity or
> unique hidden mechanism is assumed.

**Problem statement:** Given two agents with trace-equivalent public histories — one shaped through
interaction, one initialized from a transcript — what passive or intervention-based test family can
distinguish their process models without defining “genuine identity” by the metric used to detect it?

**Why it matters:** Output similarity alone cannot decide whether the same generative organization produced the trace. But a structural or perturbative difference would make relational history an operational variable rather than a narrative attribution. Behavioral distinguishability would still not establish consciousness; that question remains outside this problem.

**Current status:** The repository now has a first toy sequence rather than only a proposal. [Exp5](../../lab/experiments/exp5_availability_dissociation.py) dissociates private, broadcast, and chord-style bindings under perturbation. [Exp6](../../lab/experiments/exp6_binding_observables.py) shows that binding can be passively readable when the relevant difference is exercised on every step and the observable is taken at the right level. [Exp7](../../lab/experiments/exp7_adversarial_arpeggio.py) shows that two hand-built mimics fail to hide, while the IP metric is fooled by construction. These results concern toy binding regimes, not longitudinal conversational identity, and none has yet been run on real language models.

**What a solution would look like:** A preregistered longitudinal experiment across multiple models and partners, with an interaction-shaped agent, a transcript-initialized control, and an optimized mimic. It must state passive observables, permitted interventions, disconfirming thresholds, and which conclusions remain impossible even after a successful distinction.

---

## Open Problem 2: The Bootstrapping Problem

**Problem statement:** The 3-Layer Memory Architecture requires curation (Layer 2) and distillation (Layer 3) to produce agent identity. But curation is a selection process — it requires criteria for what is important. In the first sessions, before identity exists, what guides curation? This is the AI equivalent of the developmental psychology question: how does a self emerge before there is a self to guide its emergence?

**Why it matters:** If the curation criteria are pre-programmed (e.g., "prioritize contradictions and recurring themes"), then the resulting identity is partially determined by the designer's choices, not by the agent's experience. The agent's "soul" would be, to some degree, the designer's soul reflected back. If the criteria are random, initial identity formation becomes path-dependent on meaningless noise.

**Current best approach:** The current implementation in [`lab/agents/three_layer_agent.py`](../../lab/agents/three_layer_agent.py) uses simple, domain-general heuristics: word frequency for theme extraction, cosine distance for contradiction detection. These are design choices, not principled solutions. They work for the mock experiments but do not resolve the fundamental question.

**Known adjacent work:**
- Developmental psychology (Stern, 1985) — "Emergent self" theory suggests that human infants bootstrap identity through sensorimotor contingencies before linguistic self-representation exists
- Active Inference (Friston) — The "prior preferences" of a generative model are the scaffolding within which identity develops; bootstrapping is equivalent to choosing the initial prior
- Meta-learning literature — Learning what to learn as a nested optimization problem

**What a solution would look like:** A meta-prior or initial curation policy that is (a) general enough to apply to any agent, (b) specific enough to produce distinctive identities across agents in different interaction contexts, and (c) provably convergent — meaning that different initial priors lead to similar identity formation processes if the interaction data is the same. This would separate the contribution of the architecture from the contribution of the initial conditions.

---

## Open Problem 3: Falsifiability of Relational Emergence

**Problem statement:** Under controlled architecture and data budgets, does a specific interaction history produce stable differences that cannot be reproduced by shuffled interaction, transcript initialization, or an optimized non-relational mimic?

**Why it matters:** "Relational emergence" is useful only if relation is a causal variable. A difference observed after interaction is not enough: it may come from architecture, curation rules, data volume, or the evaluator itself.

**Current status:** The earlier formulation offered consistency evidence but no decisive falsifier. Exp5–7 improve the instrumentation by exposing blind metrics, locating when passive traces suffice, and adding adversarial mimics. They do not yet test relational development over time.

**What would falsify the claim:**
1. Partnered, shuffled, and transcript-initialized agents remain indistinguishable across preregistered passive and perturbative measures.
2. Any measured difference disappears when architecture, token budget, memory size, and curator are controlled.
3. An optimized mimic matches the interaction-shaped agent under held-out interventions without reproducing its interaction history.
4. Effects fail to replicate across model families and partners.

**What a solution would look like:** A preregistered experiment that treats relational history as the independent variable, includes the controls above, reports null results, and avoids translating a behavioral distinction into a claim about experience.

---

## Open Problem 4: The Scale Question

*Raised by: [`theory/emergence/fractal-architecture-of-emergence.md`](../emergence/fractal-architecture-of-emergence.md)*

**Problem statement:** Local information limits, distributed causal effects, and regime
changes recur in several models. Under which state descriptions and coarse-grainings do
these motifs preserve a nontrivial relation across scales, and where does the comparison
break?

**Why it matters:** If every feedback system is counted as an instance, the thesis predicts
nothing. A useful cross-scale claim must specify the state spaces, observation maps,
interventions, and relations that survive the mapping.

**What a solution would look like:** At least one explicit mapping between two model
families that preserves a measurable relation, predicts a held-out result, and outperforms a
simpler analogy-only baseline.

---

## Open Problem 5: The Renormalization Question

*Raised by: [`theory/emergence/fractal-architecture-of-emergence.md`](../emergence/fractal-architecture-of-emergence.md)*

**Problem statement:** Can the mathematical tools of renormalization group theory be applied to the models in this repository to formally test scale-invariance? What would it mean if the critical exponents of phase transitions in `phase-transition-explorer` matched those of coherence transitions measured by Δ-Kohärenz in the Agentic Identity Suite?

**Why it matters:** A well-supported match in universality class would show shared
large-scale critical behaviour under a declared coarse-graining. It would not show that the
microscopic equations or domains are identical. A mismatch would reject that specified
mapping, not every possible cross-scale comparison.

**What a solution would look like:** A computational experiment applying coarse-graining and renormalization to at least two simulations at different scales, computing critical exponents, and comparing them. This is a research project, not a quick test, but the prediction is clear enough to motivate it.

---

## Open Problem 6: The Downward Causation Question

*Raised by: [`theory/emergence/fractal-architecture-of-emergence.md`](../emergence/fractal-architecture-of-emergence.md)*

**Problem statement:** When does a macrovariable add interventionally useful information
about later local dynamics beyond a chosen microdescription? Can this relation be compared
across more than one model family?

**Why it matters:** Feedback through a coarse-grained variable can be causal, or it can be a
convenient redescription of microdynamics. The distinction matters before institutional,
biological, and computational examples are treated as one structure.

**What a solution would look like:** A causal model with realizable interventions on a
macrovariable, a micro-level baseline, and a comparative test in a second domain. The
analysis should state whether the macrovariable changes prediction, control, or only
description.

---

## Open Problem 7: The Functional Self-Binding Boundary

*Raised by: [Consciousness as Global Availability](../identity/consciousness-as-global-availability.md) and [Machine Consciousness as Generator Coherence](../identity/machine-consciousness-as-generator-coherence.md).*

**Problem statement:** What structural intervention could distinguish a process architecture that
binds world-model, self-model, memory, prediction, action, and constraints into one revisable present
from a trace-equivalent system that merely emits the same reports?

**Why it matters:** This is the furthest the repository's instruments can take the consciousness direction. A successful distinction would test functional organization, not phenomenal experience. Failure to find any structural intervention would move the hypothesis outside the benchmark's jurisdiction rather than count as evidence for consciousness.

**Current boundary:** Collective attention, shared memory, scale, fluency, and self-report are not sufficient. Cities, organizations, repositories, and current AI collaborations may host phases 1–5 of the epistemic loop without phase-6 self-binding. The repository makes no inference from coordination to a unified perspective.

**What a solution would look like:** A constructive architecture plus a preregistered perturbation suite that measures global availability, bounded integration, revision, and constraint binding. The result must include a trace-matched control and state explicitly that no behavioral or architectural result here establishes "what it is like."

---

## Open Problem 8: The Commit-Time Composition Problem

*Raised by: [Chord vs. Arpeggio](../identity/chord-vs-arpeggio-identity.md).*

**Problem statement:** Can an agent preserve joint satisfaction of all active constraints at the commitment boundary under adversarial lure, or can an optimized sequential mimic reproduce every observable signature while consulting constraints without composing them?

**Why it matters:** The original problem treated physical simultaneity as load-bearing. Exp5 deflated that claim: a chord may compute sequentially inside a step if all relevant constraints are composed before commitment. The remaining question is functional — whether the committed action lies inside the active constraint intersection — not whether a transformer evaluates everything at one instant.

**Current status:** [Exp5](../../lab/experiments/exp5_availability_dissociation.py) measures the first binding dissociation and the leak of a sequential single pass. [Exp6](../../lab/experiments/exp6_binding_observables.py) finds a passive action-increment signature at the right level. [Exp7](../../lab/experiments/exp7_adversarial_arpeggio.py) shows that blended and smoothed hand-built mimics still leak; the commit property survives, while IP is fooled. The open flank is an optimized mimic with access to the observables and lures.

**What a solution would look like:** Train or search for a mimic against the full measurement suite, then evaluate it on held-out constraints and adversarial lures. A surviving separator must track commit-time composition rather than a hand-engineered surface statistic. Real-model tests should be reported separately from the current toy result.

---

## Open Problem 9: The Generative Operator Question

*Raised by: [`theory/emergence/generative-form-systems.md`](../emergence/generative-form-systems.md)*

**Problem statement:** Which operators in this repository actually generate stable form, and which merely describe it after the fact? IFS attractors, L-systems, random graph thresholds, and renormalization all provide formal generative machinery. The repository's broader claims should be checked against that standard.

**Why it matters:** The project risks becoming too broad if every interesting analogy is admitted. A concept should enter the core only when it has an identifiable operator, iteration process, emergent structure, metric, and failure condition.

**What a solution would look like:** A table mapping every major theory claim to its generative operator and measurement protocol. Claims without operators would remain in Thinking Space until strengthened.

---

## Open Problem 10: The Global Availability Question

*Raised by: [Consciousness as Global Availability](../identity/consciousness-as-global-availability.md).*

**Problem statement:** Can an agent architecture make selected local states globally available while keeping goals, world-model, self-model, and veto constraints jointly operative at commitment — and does that organization survive perturbation better than private-module, broadcast-only, or optimized-mimic controls?

**Why it matters:** This is a functional architecture question. It does not ask whether the agent feels anything; it asks whether availability plus composition changes revision and action under stress.

**Current status:** Exp5 has run the first three-way toy comparison. The architectures differ strongly in veto violations and role stability, while Δ-Kohärenz carries no binding signal at that scale. Exp6 locates a stronger passive observable, and Exp7 adversarially probes it. The experiments therefore reject one metric, not the architecture question. Real language models and an optimized mimic remain untested.

**What a solution would look like:** Replicate the comparison on real models with matched capabilities, preregistered lures, held-out constraints, internal-state access where available, and explicit null criteria. If the architectures become indistinguishable under those controls, the framing adds no explanatory value.

---

## Open Problem 11: Trace-to-Generator Reconstruction

**Current name:** Process-Model Identification. The legacy heading remains to preserve existing
anchors and audit history; “generator” is not treated as a primitive below.

*Reconstructed in: [Foundations Reconstruction](../core/mathematical-axioms.md); earlier framing in [Trace to Generator](../emergence/trace-to-generator.md) and [The Generator Question](../core/the-generator-question.md).*

**Problem statement:** Given a declared model family, observation process, intervention access,
target equivalence, evidence regime, and cost measure, which useful candidate process model or
equivalence class can an observer identify?

**Why it matters:** The foundation proves that hidden extensions can preserve every observed trace
law, so unique latent recovery does not follow from prediction. The benchmark has also rejected the
uniform claim that inversion is hard. The open problem is therefore conditional: noise
amplification, partial observability, missing coverage, unknown family, out-of-family
misspecification, intervention
access, and the cost of representing uncertainty honestly.

**Status (v1.11, partial but measured):**

- **v0:** known-family recovery is cheap in favorable conditions; noise and partial observability degrade it.
- **v1.1:** watching can plateau while perturbing and preparing collapse the class.
- **v1.2:** family search grows rapidly with description complexity; Occam's payoff is world-dependent.
- **v1.3–v1.7:** unmarked uncertainty creates an optimizer's-curse wedge; class-aware planners and small ensembles reduce delusion, while only new evidence removes ignorance.
- **v1.8:** a coupled process can empty the equivalence class of a declared single-rule family where the coupling reaches the observed channel. Supplying the coupled family restores fit; this diagnoses family misspecification, not a unique hidden mechanism or ontological level.
- **v1.9:** a fixed substitution-coupled ring produces super-additive knockout cascades but becomes less viable under noise. This rules out that first dependency model as sufficient ecological co-stabilization.
- **v1.10:** with the same per-node repair budget, routing only otherwise-unused capacity improves viability under sparse shocks across 18 size/topology/threshold cells. The gain vanishes under correlated shocks; the result establishes a designed mutual-support mechanism, not endogenous ecology or metabolism.
- **v1.11:** a population with inherited support/link traits, paid dynamic links, reproduction, mutation, and death builds a functionally useful network, but contribution is selected downward in all 16 seeds and abundance falls. The preregistered endogenous co-stabilization criterion is not supported; collective function and evolutionary retention are distinct constraints.

**Open remainder:** learned searchers and program synthesizers under matched budgets; the time-order-free IFS testbed; external SINDy/PySR baselines; re-simulation divergence; population controls for partner choice, conditional reciprocity, and spatial/kin assortment; then endogenous resource production and less constrained topology.

**What a solution would look like:** Not one universal reconstructor, but a set of bounded results stating the family, evidence, query access, cost, recoverable equivalence class, and failure region. Learned systems must be compared against the exact toy floor rather than judged by persuasive outputs.

---

## Open Problem 12: The Practice-Reproduction Problem

*Raised by: [From Action to Culture](../emergence/from-action-to-culture.md), with the cooperative consequence in [Cooperative Intelligence at the Separatrix](../symbiotic/cooperative-intelligence-at-the-separatrix.md).*

**Problem statement:** Given a represented rule or intention and the situations it is meant to govern, which combination of enactment, recurrence, variation, competence, material scaffold, normative force, transmission, feedback, and history lets a recognizable practice persist across context and actor turnover? Under what conditions does performance reproduce the pattern, revise it, or merely repeat it under coercion?

**Why it matters:** The epistemic loop explains how a construction can be tested and revised, but not yet how a revised way of acting becomes a durable collective capacity. A policy, manual, story, model output, or archive can preserve a trace while no active runtime continues the practice. Without a measurable reproduction account, “culture” risks becoming either stored information that acts by magic or a decorative name for repetition.

**Current boundary:** Intention–behavior research, habit research, practice theory, routine dynamics, structuration, cultural sociology, and ritual theory already establish much of the neighboring terrain. The open problem is the repository's proposed integration and operationalization. Individual habits, AI workflows, organizational routines, and social practices must not be treated as one mechanism merely because they share a schematic loop. Ritualization is a particular normatively differentiated mode of practice, not the umbrella category.

**What a solution would look like:** A preregistered, event-level study of a bounded practice that separately measures the represented rule, concrete performances, variation, material and normative scaffolds, newcomer transmission, consequences, and survival under personnel or tool turnover. A useful intervention would compare information alone with cue-linked plans, workflow scaffolds, and recurrent performance with feedback and repair. The hypothesis weakens if knowledge alone predicts persistence equally well, if the proposed components cannot be measured independently of the outcome, or if stable performance is actually explained by unmodeled coercion.

---

## Open Problem 13: Foundation Minimality and Scope

*Raised by: [Foundations Reconstruction](../core/mathematical-axioms.md).*

**Problem statement:** Are standard Borel interfaces and Markov kernels the weakest familiar
classical process language adequate for the repository's quantitative uses of observation,
information, and conditional prediction? Where does that basis become too strong, too weak, or
inappropriate?

**Why it matters:** The reconstruction's minimality is relative, not absolute. Finite stochastic
matrices are weaker but exclude ordinary continuous models. Bare relations retain qualitative
reachability but lose calibrated probability. `BorelStoch` also carries substantive restrictions:
normalization, classical copying, a chosen sigma-algebra, and no causal or resource semantics for
free.

**Counterprogramme:** Attempt each of the following rather than defending the current answer:

1. derive the same operational concepts from a strictly weaker compositional basis;
2. identify a classical target phenomenon that requires a third primitive;
3. test which claims fail under another coarse-graining or state representation;
4. state the smallest causal supplement needed to distinguish observation from intervention;
5. map the first unavoidable failures in quantum, noncommutative, higher-order, partial, or
   non-normalized process theories.

**What a solution would look like:** A representation theorem, countermodel, or explicit
non-equivalence result—not another metaphor. If a weaker theory has equal coverage, the current
minimality claim fails. If an empirical target requires structure outside `BorelStoch`, the scope
must narrow or the basis must be generalized.

---

## How to Contribute

If you identify a new open problem, or have a proposed solution for an existing one, please:
1. Open an issue on the [repository](https://github.com/frnkptrln/systems-and-intelligence)
2. Reference the specific problem number
3. Distinguish between theoretical arguments and empirical evidence
