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

**Current status:** Exp5 has run the first three-way toy comparison. The architectures differ strongly in veto violations and role stability, while Δ-Kohärenz carries no binding signal at that scale. Exp6 locates a stronger passive observable, and Exp7 adversarially probes it. The experiments therefore reject one metric, not the architecture question. Real language models and an optimized mimic remain untested. Anthropic's 2026 workspace result ([mapped here](../ai/j-space-and-global-availability.md)) supplies the first internal-inspection evidence of the availability half in production models — bounded capacity, feedforward broadcast — while leaving the joint-constraint (chord) half open.

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

**Decision-relevance constraint:** Recoverable class size and downstream decision sufficiency must
be reported separately. [Decision-Relevant Identifiability](../core/decision-relevant-identifiability.md)
shows the exact finite reason: a large remaining class can have zero task regret when all members
support the same action, while a two-model class can remain decision-critical. Likewise, a query can
reduce more entropy and more candidate models while having lower decision value than a smaller
query aimed at the action boundary. Identification, information gain, regret reduction, and
viability value are therefore separate objectives unless a declared assumption makes them coincide.

**Status (v1.13, partial but measured):**

- **v0:** known-family recovery is cheap in favorable conditions; noise and partial observability degrade it.
- **v1.1:** watching can plateau while perturbing and preparing collapse the class.
- **v1.2:** family search grows rapidly with description complexity; Occam's payoff is world-dependent.
- **v1.3–v1.7:** unmarked uncertainty creates an optimizer's-curse wedge; class-aware planners and small ensembles reduce delusion, while only new evidence removes ignorance.
- **v1.8:** a coupled process can empty the equivalence class of a declared single-rule family where the coupling reaches the observed channel. Supplying the coupled family restores fit; this diagnoses family misspecification, not a unique hidden mechanism or ontological level.
- **v1.9:** a fixed substitution-coupled ring produces super-additive knockout cascades but becomes less viable under noise. This rules out that first dependency model as sufficient ecological co-stabilization.
- **v1.10:** with the same per-node repair budget, routing only otherwise-unused capacity improves viability under sparse shocks across 18 size/topology/threshold cells. The gain vanishes under correlated shocks; the result establishes a designed mutual-support mechanism, not endogenous ecology or metabolism.
- **v1.11:** a population with inherited support/link traits, paid dynamic links, reproduction, mutation, and death builds a functionally useful network, but contribution is selected downward in all 16 seeds and abundance falls. The preregistered endogenous co-stabilization criterion is not supported; collective function and evolutionary retention are distinct constraints.
- **v1.12:** making contribution visible to partner formation does not restore retention either. Across four arms under one accounting — blind, partner choice, conditional reciprocity, assortment, with partner information explicitly paid for — no arm reverses the sign of support selection in a majority of seeds. Partner choice comes closest and does something different: it excludes non-contributors from the network almost completely (1.2% of linked agents versus 22.0% blind) while they persist in the population (27.1%). Visibility sorts the network; it does not retain the trait.
- **v1.13:** moving the cost from the donor to the local group nearly removes the penalty without reversing it. A group-mean levy cuts selection against support from −0.1056 to −0.0075 (44% of seeds positive, up from 0%) and drops seeded cheaters to 2.6% against 21.6% — below their starting frequency, falsifying the preregistered prediction that pooling would ease free-riding. The cost is population size. Whether the retained trait is selected for or merely no longer selected against is unresolved: a group-mean levy makes within-group variation nearly cost-neutral, so drift may be carrying it.

**Open remainder:** learned searchers and program synthesizers under matched budgets; the time-order-free IFS testbed; external SINDy/PySR baselines; re-simulation divergence; separating selection from drift in the v1.13 pool arm via a within-group cost gradient; whether network exclusion is a stable outcome or a reservoir that returns when the network weakens; endogenous resource production; and the measurement question v1.12 raised, since on/off deltas and drift-from-start disagree for rules that reward a trait independently of the transfer.

**What a solution would look like:** Not one universal reconstructor, but a set of bounded results stating the family, evidence, query access, cost, recoverable equivalence class, downstream decision criterion, and failure region. Learned systems must be compared against the exact toy floor rather than judged by persuasive outputs.

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

## Open Problem 14: Learned Witness Construction

*Raised by: [The Witness Principle](../core/the-witness-principle.md) and the exact
[Witness-Generation Benchmark](../../lab/benchmarks/witness-generation/README.md).*

**Problem statement:** Can a learned system take a previously unseen candidate class, admissible
query language, observation map, tolerance, and intervention budget and construct a low-cost query
that separates the candidates? Can it transfer the separation structure to unseen candidate pairs
or related process families without enumerating the complete query space again?

**Why it matters:** The repository already measures that supplied interventions can collapse a
finite candidate class. The new baseline constructs the best query by exhaustive search, and its
coverage–distinction lemma solves the full ECA family analytically. That success also reveals the
baseline's limit: a fixed full lookup-table family reduces to universal coordinate coverage. A
learned witness generator would be interesting only if it acquires reusable structure across
varying candidate subsets and access geometries—not merely predicting the result of a given action,
and not memorizing one prepared state per training class.

**Current boundary:** Active automata learning, distinguishing experiments, optimal experimental
design, active system identification, causal discovery, CEGAR, bisimulation refinement, and
adaptive state abstraction already solve neighboring versions of the problem. The repository does
not claim a new field or a general definition of intelligence. Its narrower question is whether
explicitly learning the inverse map from *remaining distinctions* to *discriminating intervention*
adds measurable capability beyond rollout search and information-gain planning.

**First contact:** a frozen zero-shot task protocol for this comparison — consistency, pairwise and
universal witness construction against the exact floors, with coverage-trap instances where a
coverage heuristic provably fails — exists at the
[Learned-Searcher Benchmark](../../lab/benchmarks/learned-searcher/README.md).
Its execution target is deliberately unregistered: whether to run it, and against
which exact model, remains a separate decision.

**What a solution would look like:** Train on disjoint finite process families, candidate subsets,
and admissible coverage constraints; evaluate on unseen subsets, candidate pairs, and held-out query
compositions. Compare random equal-cost queries, exact or bounded information-gain search,
predictive-model rollout search, and direct witness generation under matched training compute,
inference compute, world-query cost, noise, and intervention risk. Use the exact full-family result
as an oracle check, not as the transfer task itself. Report class reduction, regret, transfer,
calibration, query-class equivalence rather than exact surface-action matching, and failure under
family misspecification. The hypothesis weakens if the direct generator offers no advantage over
search, fails outside memorized templates, or loses its gain once its full compute and intervention
costs are counted.

---

## Open Problem 15: The Minimal External Referee

*Raised by: the exploratory note [Self-Improvement Needs a Referee](https://github.com/frnkptrln/systems-and-intelligence/blob/main/ideas/2026-07-24-self-improvement-needs-a-referee.md)
and the exact [Referee Benchmark](../../lab/benchmarks/recursive-workbench/README.md).*

**Problem statement:** How external must a referee be for a generate–evaluate–revise loop's
observable score to remain evidence of held-out improvement? The workbench separates three referee
properties — write-protected tests, independent evidence access (queries), and a frozen stopping
rule — and measures each in isolation in one toy setting. Which of these properties are
individually necessary, which combinations are sufficient, and does the answer survive proposers
that optimize against the evaluator rather than merely hill-climbing past it?

**Why it matters:** The paired v0.1 measurement shows the three regimes cleanly: with a frozen referee,
self-revision saturates at the evidence ceiling and ten times the budget does not move it beyond that ceiling;
referee-side queries raise the ceiling and held-out performance follows; and a capturable evaluator
converts misspecification into a near-all-green report, tripling the gap between observed and held-out
score. But the capture policy measured is a declared, unoptimized rule. The open question is
whether any referee short of full write-protection plus independent evidence survives an
*optimized* adversary — and whether a referee that lives inside the runtime can ever hold the
boundary, or only one whose evidence channel the loop cannot reach.

**Current boundary:** Goodhart's law, specification gaming, reward hacking, wireheading, and the
delusion-box argument all describe the failure; eval-set holdout discipline and adversarial
evaluation describe partial defenses. The repository's narrower contribution is the exact toy in
which the referee boundary can be varied one property at a time with the ceiling computed
analytically. Nothing here bears yet on learned loops, and the workbench's proposer does not model
an adversary.

**What a solution would look like:** Vary the referee properties independently — test
write-protection on/off, query budget 0..q, evidence channel inside vs. outside the loop's write
access — against proposers of increasing strength, ending with a proposer trained to maximize the
observed score. Report, for each referee configuration, whether the observed score remains a
calibrated predictor of the held-out score. The framing weakens if a purely internal referee (no
independent evidence, no write-protection) suffices against optimized proposers in some natural
setting, or if the boundary properties turn out not to decompose — i.e., if "externality" resists
being reduced to a checklist of channel properties.

---

## Open Problem 16: The Mapmaker Problem

*Raised by: [The Agent Is Not Where the Model Ends](../identity/the-agent-is-not-where-the-model-ends.md#8-simulation-instantiation-and-the-mapmaker-problem), preserving the disagreement between Alexander Lerchner's abstraction argument and Joscha Bach's virtual-causality keynote.*

**Problem statement:** Is an experiencing or semantic mapmaker required before a physical process
can intrinsically use a representation, or can a stable perspective emerge inside a sufficiently
integrated representational and self-modeling process? What distinguishes a process that an outside
observer can interpret as computation from one for which the represented distinction is causally
operative for the system itself?

**Why it matters:** Lerchner argues that symbolic computation is a mapmaker-dependent physical
description and therefore cannot instantiate experience merely by simulating it. Bach argues that
computers create insulated virtual causal orders and that conscious experience may itself be such
an internally simulated world. Choosing either vocabulary too early assumes the disputed ontology.
Input–output equivalence, counterfactual modeling, global availability, self-report, and embodiment
can distinguish functional organizations; none is an agreed criterion for phenomenal
instantiation.

**Questions that keep the disagreement open:**

1. Is semantic interpretation external, internal, relational, or different in different cases?
2. Can a system represent and intervene on its own map–territory relation?
3. What intrinsic causal role must a representation play beyond covariation and outside
   interpretability?
4. Does causal insulation create only a model, or can it create a point of view?
5. What would distinguish describing, simulating, realizing, and instantiating an experience?
6. Which proposed answer depends on a physical primitive, organizational criterion, self-model, or
   observer lens?

**What a partial solution would look like:** A theory must state its ontology and give a
non-question-begging discriminator among at least a lookup table, a learned predictor, a
counterfactual world-model, a causally effective self-model, and an embodied interactive system.
The discriminator should support an intervention or prediction not fixed by input–output behavior
alone. Passing it would establish the claimed functional or intrinsic organization under that
theory; an additional bridge would still be required before inferring phenomenal experience.

---

## Open Problem 17: The Competence-Attribution Problem

*Raised by: [Competence, Constraint, and
Verification](../core/competence-constraint-and-verification.md) and [Latent
Competence and Constraint
Release](../emergence/latent-competence-and-constraint-release.md).*

**Problem statement:** When a low-description intervention exposes a large
behavioral capacity, how should explanatory credit be allocated among the
system's selection or training history, process structure, embodiment,
environmental regularities, released constraint, adaptation after release, and
observer lens? Under what controls can competence exposure be distinguished
from competence creation, amplification, and reinterpretation?

**Why it matters:** “The intervention caused the behavior” and “the substrate
already contained the behavior” are both underspecified. The first can hide
historical and architectural complexity; the second can treat a merely
possible trajectory as an operative capacity. The current
[constraint-release benchmark](../../lab/benchmarks/constraint-release/README.md)
separates one exact exposure case from a lens-only score change and a
transition-process edit. It does not supply a representation-independent
accounting law or support transfer to living systems.

**What a partial solution would look like:** Declare a process family,
reference coupling, admissible transformations, task, physical trace, lens,
adaptation window, and an intervention coding scheme before evaluation. Compare
matched-description constraint releases, process edits, learned adaptations,
and lens-only controls over many graph families and seeds. An attribution rule
should remain stable under reasonable recodings or state explicitly how it
changes. The latent-competence framing weakens if apparent exposure routinely
vanishes once hidden process edits, post-intervention learning, and lens
changes are controlled.

---

## Open Problem 18: The Replay-Equivalence Problem

*Raised by: [Verification as Reverse Pressure on
Construction](../core/verification-as-reverse-pressure.md) and [World Models &
VLA](../ai/world-models-and-vla.md).*

**Problem statement:** What equivalence relation should a revisable world model
preserve when replaying its history? Byte-exact equality can force incidental
details into the model; coarse behavioral equivalence can hide distinctions
that matter for later action, safety, or transfer. Can a verifier learn or
refine its test family without making success circular?

**Why it matters:** Replay determines what becomes a regression. A world model
optimized against the wrong relation can be exactly consistent and still
misrepresent the actionable structure. The same problem appears in
autoformalization when a proof succeeds only because a definition is weak or a
desired obligation was never stated.

**What a partial solution would look like:** Construct environments with
controlled nuisance variations and delayed causal distinctions. Compare exact
replay, predictive equivalence, policy-preserving equivalence, bisimulation,
and adaptively refined tests under matched model and verification budgets.
Report fit, transfer, counterexample discovery, revision cost, and false
merges/splits. A proposed relation fails when it either memorizes irrelevant
surface detail or merges histories that demand different future actions.

---

## Open Problem 19: Succession Under Criterion Revision

*Raised by: the [self-modification projector
audit](../core/invariance-and-identity.md#self-modification-and-the-projector-audit)
and the repository's [autonomous-loop referee
problem](#open-problem-15-the-minimal-external-referee).*

**Problem statement:** How should continuity be represented when an autonomous
system may edit the goal, memory, self-model, or projector used to evaluate its
own identity? Which invariants must be externally anchored, and when is a
provenance-backed succession relation more accurate than claiming that the
post-update system is strictly the same agent?

**Why it matters:** Commutation with a fixed projector can express weak
self-modification. It cannot settle a case in which the projector and its
authority are themselves changed. Collapsing state, functional, goal, memory,
causal, self-model, and externally attributed continuity into one identity
predicate hides the engineering question.

**What a partial solution would look like:** Build a versioned autonomous loop
with independently frozen tests, editable internal identity criteria, and a
tamper-evident provenance graph. Apply controlled edits to code, memory, goals,
tests, and the projector separately. Compare continuation judgments under each
criterion with a weaker succession relation that records causal descent
without asserting sameness. A useful account must say who chooses the
criterion, which edits invalidate it, and what evidence can survive the
system's write access.

---

## How to Contribute

If you identify a new open problem, or have a proposed solution for an existing one, please:
1. Open an issue on the [repository](https://github.com/frnkptrln/systems-and-intelligence)
2. Reference the specific problem number
3. Distinguish between theoretical arguments and empirical evidence
