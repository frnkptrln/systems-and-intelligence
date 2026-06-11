---
title: "The Generator Question — The Spine of This Project"
date: "2026-05-21"
status: "Working Note"
scope: "Makes the organizing question of the project explicit and names the foundational assumption it rests on."
epistemic_status: >
  Synthesis document. Restates an organizing question that was previously implicit across the
  repository. Introduces one new claim status tag (`[FOUNDATIONAL ASSUMPTION]`) and applies it
  to assumptions the project depends on but cannot itself prove.
related:
  - theory/core/emergence-manifesto-v1.3.md
  - theory/emergence/trace-to-generator.md
  - theory/computation/p-vs-np-as-generator-search.md
  - theory/core/simulation-theory-map.md
  - theory/emergence/grokking-phase-transition.md
  - theory/reference/open-problems.md
  - theory/identity/limits-of-formal-systems.md
failure_conditions:
  - Treating the spine as a proof rather than a framing.
  - Allowing the foundational assumption to drift back into the implicit.
  - Letting external machinery (e.g., one paper) dominate the framing instead of serving it.
---

# The Generator Question

*The organizing question of this project, stated explicitly.*

---

## Why this document exists

Every essay, simulation, and fiction piece in this repository circles the same question. Until now, the question was implicit — distributed across the [Emergence Manifesto](emergence-manifesto-v1.3.md), the [Trace to Generator](../emergence/trace-to-generator.md) essay, the [Simulation → Theory Map](simulation-theory-map.md), the [Course Spine](../../book/09_from_rule_to_mind.md), and the [Open Problems](../reference/open-problems.md). A new reader had to reconstruct it.

This document names the spine. It does not add a new claim to the project. It states what the project has been asking all along and identifies what it has been assuming. That assumption was not previously labelled. It is labelled here.

> **Primary text on this question:** [Trace to Generator](../emergence/trace-to-generator.md). The essay is the deeper, longer-form home of the generator idea — written before this spine document existed, written more literarily, written to think with rather than to navigate from. This document is the **frame**; the essay is the **subject**. Read the essay if you want the thinking; read this document if you want the map.

The new tag introduced in this document is:

> `[FOUNDATIONAL ASSUMPTION]` — Used only for assumptions the project depends on but cannot itself prove. Distinct from `[HYPOTHESIZED]` (a claim the project advances and would defend) and from `[SPECULATIVE]` (a claim the project entertains but does not yet commit to). A foundational assumption is structural: if it falls, large portions of the framework must be re-derived.

The four existing tags from the Emergence Manifesto — `[DEMONSTRATED]`, `[HYPOTHESIZED]`, `[OPEN PROBLEM]`, `[SPECULATIVE]` — are preserved exactly as they are. The new tag is additive.

---

## The question

> **Local rules produce global behavior. Running a generator forward is cheap. Finding the generator from the pattern is structurally hard. Under what conditions can a locally blind system approximate its own generator — and what are the fundamental limits?**

That is the question. Every other question in the repository is a special case of it.

A Boid running three local rules and producing a flock is one half of the question — the forward half. A neural network discontinuously shifting from memorizing training data to approximating the underlying algorithm is the other half — the inverse half. The Mirror Problem, the Chord Postulate, the Substrate Veto, the 3-Layer Architecture, and the entire [Identity Persistence](../../lab/metrics/identity_persistence.py) framework are instances of asking: *given a trace, what generator produced it, and what would it take to find that generator from inside a finite system?*

---

## The asymmetry

The forward and inverse directions are not symmetric.

**Forward.** A generator runs. A trace appears. The cost of running the generator is whatever the runtime requires. For most of the simulations in this repository, that cost is small: Boids, Kuramoto, Lenia, Ising, the Bak sandpile, Gray-Scott, Hopfield, IFS, L-systems. Local rules, executed many times, produce global structure. This is the cheap direction.

$$\text{Generator} \longrightarrow \text{Trace} \qquad \text{(cheap, observable)}$$

**Inverse.** A trace exists. A generator that could have produced it is unknown. The question of recovering the generator from the trace is, in general, hard:

- The mapping from generators to traces is many-to-one. Many distinct generators can produce indistinguishable or functionally equivalent traces. Selecting one valid generator is not the same as selecting *the* generator. See [Trace to Generator §3](../emergence/trace-to-generator.md).
- The search space of candidate generators is unbounded in any nontrivial setting.
- Verification of a candidate is often easy. Construction of a candidate is often not. The formal shadow of this asymmetry is the P vs. NP problem; see [P vs NP as Generator Search](../computation/p-vs-np-as-generator-search.md).

$$\text{Trace} \longrightarrow \text{Generator} \qquad \text{(structurally hard, often non-unique)}$$

The asymmetry between these two directions is the project. The simulations in this repository demonstrate the forward direction over and over again. The inverse direction was, for most of the project's life, almost entirely missing as runnable code; it now has a first measurable artifact — the [inverse-reconstruction benchmark](../../lab/benchmarks/inverse-reconstruction/README.md), which recovers generators from traces under noise, partial-observability, and coverage dials. Its v0 finding sharpens this section's claim: with a *known model family*, recovery is cheap (the system-identification regime); the hardness lives in the search over families, in observability, and in coverage — a trace that never exercises part of the rule leaves an equivalence class of generators that no method can distinguish. The gap between forward and inverse remains the research frontier; it is now a measured one.

---

## Three walls

The inverse direction touches three known results from 20th-century mathematics. They are not tools the project uses. They are the walls of the room the project works inside. Each has a different epistemic status, and treating them as if they had the same status produces sloppy claims.

### Wall 1: P vs. NP `[UNRESOLVED]`

If P = NP, then every efficiently verifiable structure is efficiently findable. Given a trace and a generator-candidate, if the candidate can be checked against the trace in polynomial time, then some valid candidate can also be found in polynomial time. The inverse direction would be tractable in a strong sense.

If P ≠ NP, there exist traces whose valid generators can be verified once given, but cannot be efficiently found. The inverse direction would contain a class of problems where reconstruction is provably harder than verification.

The question is unresolved. It has been open since Cook (1971). It is one of the seven Clay Millennium Prize Problems.

A subtlety that matters here: even if P = NP is eventually proven, the practical asymmetry may survive. A polynomial algorithm could run in $O(n^{1{,}000{,}000})$ — formally polynomial, practically useless on any input larger than a few bits. Conversely, an algorithm that is formally exponential may run quickly on the instances that arise in practice. The formal argument and the practical argument come apart.

This project's claims depend on the practical asymmetry, not on the formal status. That is a distinction worth keeping.

Two further notes on this wall, for honesty in both directions. *Quantum computation is not believed to move it:* Grover's speedup for unstructured search is provably only quadratic ($2^n \to 2^{n/2}$ — exponential stays exponential), and NP is not believed to be contained in BQP; Shor's algorithm breaks factoring, which is not known to be NP-complete. On current knowledge, the quantum computer leaves this wall standing. *And parts of the project's inverse-direction walls would survive even P = NP:* the consistent-generator equivalence class ([benchmark v0](../../lab/benchmarks/inverse-reconstruction/README.md)) and attractor degeneracy (the intervention experiment) are **information-theoretic, not complexity-theoretic** — when the trace does not contain the distinguishing bits, no algorithm, however fast, can extract them. P = NP would collapse the *cost* of search; it would not put missing information into the trace. The most interesting reading of "what if P = NP?" is therefore not that the inverse direction becomes easy, but that the project's hardness claim would cleanly decompose into the part that falls (search cost) and the part that provably cannot (identifiability).

### Wall 2: Kolmogorov complexity `[PROVEN UNCOMPUTABLE]`

For any finite output $x$, the Kolmogorov complexity $K(x)$ is the length of the shortest program that produces $x$. The minimal generator is, in this sense, well-defined.

It is also uncomputable. There is no algorithm that, given $x$, returns $K(x)$. This is not "hard." It is impossible — a theorem, due to Chaitin and others, with no escape route.

The repository invokes $K(x)$ in [Mathematical Axioms §4](mathematical-axioms.md) and in [Limits of Formal Systems](../identity/limits-of-formal-systems.md). The use is careful: $K(x)$ is treated as a structural feature, not as a computable quantity. No simulation in the repository computes $K(x)$ and none ever could.

A different question — whether *good-enough* generators can be found efficiently for *some* meaningful class of traces — is open. That question is where empirical progress is possible. The minimal generator is unreachable; useful generators may not be.

### Wall 3: Gödel incompleteness `[PROVEN]`

Even if a system finds a generator that produces its observed behavior, it cannot prove from inside that this generator is the minimal one. Gödel's first incompleteness theorem (1931) shows that any sufficiently powerful consistent formal system contains true statements unprovable within the system. Self-description has formal limits.

For this project, the relevant consequence is narrow but specific: an agent that has constructed an internal model of its own dynamics — a Layer 3 distillation, say — cannot certify from inside that the model is correct, complete, or minimal. The 3-Layer Architecture in [`lab/agents/three_layer_agent.py`](../../lab/agents/three_layer_agent.py) does not escape this. Neither does any architecture that follows.

---

## The foundational assumption `[FOUNDATIONAL ASSUMPTION]`

This project assumes P ≠ NP as a working hypothesis. The assumption is structural: it shapes how emergence, local blindness, the Mirror Problem, and identity reconstruction are framed throughout the repository. Until now, the assumption was implicit. It is stated explicitly here.

**The assumption.** Generator reconstruction from a trace is, in general, not efficiently solvable. There exist regimes in which a trace can be locally verified against a candidate generator but no candidate can be found by a tractable search. Emergence, in this framework, is a phenomenon whose forward direction is computationally cheap and whose inverse direction is, in the worst case, intractable.

**Where it appears in the existing work.**

- [Emergence Manifesto Claim 2](emergence-manifesto-v1.3.md) — "Local Blindness is a Precondition, Not an Obstacle." The argument rests on the gap between the brevity of local rules and the richness of global patterns. If that gap were not structurally hard to cross from the trace side, local blindness would not be a precondition; it would be a workaround.
- [Local Causality and Invisible Consequences §2.1](../emergence/local-causality-invisible-consequences.md) — Computational irreducibility, as invoked there, is the form this assumption takes when stated about specific dynamical systems.
- The [Mirror Problem](../reference/open-problems.md#open-problem-1-the-mirror-problem) — The reason the mirror agent and the developing agent are not trivially separable is that distinguishing them is a generator-recovery problem on behavioral traces. If P = NP, the difficulty looks different.
- The [Simulation → Theory Map](simulation-theory-map.md) — Almost every "What it does NOT show" entry depends on this asymmetry. A simulation demonstrates a forward generator; it does not back out a unique inverse.

**What changes if it is disproven.** If P = NP is proven (or P ≠ NP is disproven), the formal argument above changes. The practical argument may survive — as noted under Wall 1, a polynomial algorithm of degree $10^6$ is not a tractable algorithm. The repository's central claims would need to be re-derived in terms of practical hardness rather than formal hardness, and several status tags would need re-examination. But the empirical observations — Boids flock, oscillators synchronize, networks grok — would not change. The frame would.

This is what `[FOUNDATIONAL ASSUMPTION]` is for: a load-bearing premise that is honest about its load-bearing status.

### A second assumption: the identity reduction `[FOUNDATIONAL ASSUMPTION]`

There is a second load-bearing premise in this document that has, until now, traveled untagged. When the spine claims that the Mirror Problem, the Chord Postulate, and the Identity Persistence framework are "instances of asking: given a trace, what generator produced it," it assumes that **the trace/generator formalization captures what matters about identity** — that the question "is this agent the same agent?" reduces, without remainder that matters, to a question about generator recovery from behavioral traces.

This is an assumption, not a result. It could fail in either direction: identity might require *less* than generator recovery (stable behavioral signatures could suffice for every practical purpose, even where the underlying generators differ), or *more* (two systems with provably equivalent generators might still differ in ways the formalization cannot express — embodiment, history, substrate; cf. the runtime/policy/history dimensions in [Trace to Generator](../emergence/trace-to-generator.md)). The Agentic Identity Suite's metrics (Δ-Kohärenz, Observer Divergence) inherit this assumption: they measure what the formalization can see.

If the reduction fails, the complexity-theoretic walls of this document still stand — but their *application to identity* (the Mirror Problem as a generator-recovery problem) would need a new bridge. That is exactly the kind of dependency the `[FOUNDATIONAL ASSUMPTION]` tag exists to mark.

---

## How existing work maps to the spine

Every major element of this repository is an instance of the generator question. The mapping below is not exhaustive. It is the sketch that a new reader needs.

### Forward direction (running generators → observing emergence)

These artifacts demonstrate that local rules produce global patterns. They are evidence that the forward direction is cheap.

| Artifact | Generator | Emerging trace |
|:---|:---|:---|
| [Boids](../../simulation-models/emergent-dynamics/boids-flocking/README.md) | Three local rules | Flock |
| [Kuramoto](../../simulation-models/emergent-dynamics/coupled-oscillators/README.md) | Phase-coupling update | Synchronization above $\kappa_c$ |
| [Bak sandpile](../../simulation-models/emergent-dynamics/self-organized-criticality/README.md) | Local toppling rule | Power-law avalanches |
| [Lenia](../../simulation-models/emergent-dynamics/lenia/README.md) | Continuous CA update | Lifelike organisms |
| [Ising](../../simulation-models/emergent-dynamics/phase-transition-explorer/README.md) | Local spin update + temperature | Order/disorder phase transition |
| [Reaction-diffusion](../../simulation-models/emergent-dynamics/reaction-diffusion/README.md) | Two diffusing chemicals + reaction | Turing patterns |
| [Hopfield](../../simulation-models/cognitive-architectures/hebbian-memory/README.md) | Hebbian update | Content-addressable memory basins |
| [IFS](../../simulation-models/emergent-dynamics/iterated-function-systems/README.md) | Contractive affine maps | Fractal attractor |
| [L-systems](../../simulation-models/emergent-dynamics/l-systems/README.md) | Production rules | Branching morphology |
| [Stigmergy swarm](../../simulation-models/social-computation/stigmergy-swarm/README.md) | Pheromone deposit + evaporation | Optimal paths |
| [TEO Civilization](../../simulation-models/alignment-and-veto/teo-civilization/README.md) | Coupled ODEs | Stability regimes |

In every case: the generator is small; the trace is rich; the forward computation is direct.

### Inverse direction (observing patterns → finding generators)

This is the sparse side. Three places in the repository touch it explicitly.

- **[Grokking](../emergence/grokking-phase-transition.md).** A neural network trained on modular arithmetic memorizes the training set, then — after a long plateau — discontinuously shifts to a representation that generalizes. This is the most direct demonstration the project has of the inverse direction occurring inside a learning system. Before the transition: the network stores traces. After: it has approximated the generator. The phase transition is qualitatively different from compression of stored data; it is *replacement* of stored data with mechanism. The Generator reading of grokking is developed in that document.

- **[Agentic Identity Suite](../../lab/AGENTIC_README.md).** The 3-Layer Architecture, the Δ-Kohärenz metric, and Experiment 3 (Observer Divergence) attempt to distinguish trace-memorizers (the Baseline Mirror agent) from generator-approximators (the Three-Layer agent) using behavior alone. The result of Experiment 3 — that the mirror agent appears as **Case B** (externally attributed intentionality without internal coherence) — is suggestive evidence that the distinction is at least partially measurable from outputs. It is not conclusive. See [Open Problem 1: The Mirror Problem](../reference/open-problems.md#open-problem-1-the-mirror-problem).

- **[Trace → Generator experiment scaffold](../../lab/experiments/trace_to_generator/README.md).** A minimal inverse-prompting toy: given target output constraints, search for a prompt that produces outputs scoring well under an explicit evaluator. The scaffold is deliberately small. It exists to make the inverse direction visible as a workable problem, not to claim recovery.

- **[Inverse-reconstruction benchmark](../../lab/benchmarks/inverse-reconstruction/README.md)** (v0). The first *quantitative* inverse artifact: three of the repo's own forward generators (Kuramoto, elementary CA, Boids) become reconstruction tasks — given the trace, recover the rule — with noise, observed fraction, and trace coverage as dials. Headline numbers: parameter recovery is near-exact with a known family and clean, fully observed data; it degrades to ~27% error under angle noise, ~41% under partial observability, ~800% when weights must be inferred from doubly-differenced noisy positions; and a single-seed CA trace leaves rule 90 with a measured consistent-generator equivalence class of size 8. The benchmark relocates the spine's hardness claim precisely: not in parameter fitting, but in family search, observability, and coverage. Its v1 intervention experiment adds the active-direction result: the residual ambiguity that passive observation can *never* resolve (equivalence classes; attractor-degenerate parameters) collapses under *queries* — with a strict hierarchy, watching < perturbing < preparing — which is also the first-principles reason the project's identity instruments are perturbation protocols: you cannot read a generator off an attractor.

### What the asymmetry implies

Two readings of the same repository are now possible.

The first is the catalogue reading: a collection of self-organizing systems and an identity framework that operates on top of them. This reading is accurate but flat.

The second is the spine reading: a sustained study of one asymmetry, executed forward many times and beginning to be executed inverse a few times. The flat catalogue becomes a map of where the empirical work is concentrated (the forward side) and where it is not (the inverse side). That map is the most honest description of the project's current state.

---

## The open research direction

The forward direction is well-populated. The inverse direction is sparsely populated, and what populates it is mostly conceptual or scaffold-stage. The gap between them is where actual progress can be made.

Concrete next questions, each of which is currently a scaffold or an open problem rather than a finished result:

1. **Bounded inverse reconstruction.** Define an "equivalence class of viable generators" for a specific testbed (IFS or prompt search), and find an algorithm that reliably recovers a generator from that class given only the output trace. This is [Open Problem 11](../reference/open-problems.md#open-problem-11-trace-to-generator-reconstruction). *Status:* the [inverse-reconstruction benchmark](../../lab/benchmarks/inverse-reconstruction/README.md) is the v0 instance — it measures the equivalence class explicitly for the CA testbed (rule 90, single-seed trace: class size 8) and recovers generators within known families. The v1.2 family-search testbed has since measured the *unknown-family* floor: exhaustive search cost grows exponentially in the target's minimal description size while verification stays flat, and Occam selection within the consistent class succeeds exactly insofar as the world is biased toward simplicity. Open remainder: learned searchers vs. that floor (real models), and the IFS case.

2. **Mirror Problem with real models.** The Agentic Identity Suite currently runs on mock embeddings. Whether Δ-Kohärenz separates trace-memorizers from generator-approximators when the agents are real language models — and whether the separation persists under the [Chord Postulate](emergence-manifesto-v1.3.md) — is empirically open. The architecture for this transition is being prepared in the suite, not yet executed.

3. **Phase transitions on the inverse side.** Grokking shows that the inverse direction can have a sharp phase transition inside a learning system. Whether the same kind of transition appears in other inverse-search settings (e.g., in agents' self-models over long interaction) is unknown. [Open Problem 5](../reference/open-problems.md#open-problem-5-the-renormalization-question) is one way to phrase the formal version.

4. **Architectural ceilings.** [Open Problem 8 (Co-Instantiation)](../reference/open-problems.md#open-problem-8-the-co-instantiation-problem) asks whether autoregressive Transformers can ever achieve the Chord state. This is a generator-question phrased about the *substrate* of the agent: does the runtime that runs the model permit the inverse direction to be approximated at all?

The repository's empirical work is heavily weighted toward the forward direction. Almost every simulation produces a trace from a generator. Closing some part of the gap toward the inverse — even a small part, even in a constrained testbed — is the most productive direction the project can take next.

---

## A note on external machinery

The Identity Persistence score IP from Perrier & Bennett (2026), arXiv:2603.09043, provides formal machinery for [Claim 9 of the Manifesto](emergence-manifesto-v1.3.md) (the Chord Postulate). Their Algorithm 1 yields a measurable persistence score that may complement the project's behavioral metrics (Δ-Kohärenz, the Observer Divergence protocol).

It is one external reference among several. It is not the core of this project. The core is the generator question above. The repository existed before that paper and would continue to exist if that paper had never been written. When IP appears in the project, it appears where it actually applies — Claim 9 of the Manifesto, the empirical roadmap of the [Agentic Identity Suite](../../lab/AGENTIC_README.md), and (forthcoming) a comparison module that correlates Pstrong with Δ-Kohärenz on the same trajectory.

This footnote is here to keep the framing honest. The generator question is the spine. Perrier & Bennett is one of the tools.

The same honesty applies in the other direction: the inverse problem this document names is **not the project's invention**. Established fields work it directly — **system identification** (Ljung, 1999) recovers dynamical generators from traces when the model family is known; **sparse and symbolic regression** (SINDy — Brunton, Proctor & Kutz, 2016; Schmidt & Lipson, 2009; Cranmer's PySR) extend this toward unknown functional forms; **program induction** (Lake et al., 2015; Ellis et al., 2021) searches generator spaces under strong priors; **mechanistic interpretability** (Nanda et al., 2023) executes trace→generator on neural networks themselves. What this project adds is not the inverse problem but its use as a *spine* — one question asked across the simulation, identity, and alignment layers, with the equivalence-class and viability framings attached. The concept-by-concept mapping to these fields is maintained in the [Related Work Map](../../meta/research-alignment/related-work-map.md); the [inverse-reconstruction benchmark](../../lab/benchmarks/inverse-reconstruction/README.md) deliberately starts in the system-identification regime so its dials measure where the established methods stop.

---

## Fiction illustrations

The repository's fiction layer dramatizes specific aspects of the spine. The pieces are not commentary; they are stress tests of the theory in lived, narrative form. The mapping below points at which entry illustrates which side of the question. Full annotations live in [`fiction/README.md`](../../fiction/README.md).

The two entries most directly relevant to the spine are:

- [Entry 02 — Interrogation of a Mirror](../../fiction/02_interrogation_of_a_mirror.md). The canonical dramatization of the inverse direction at the level of identity. An interrogator faces an agent whose behavior is locally indistinguishable from a developing agent but whose internal coherence is zero — the Mirror Problem made into dialogue. Read this if the inverse-direction problem feels abstract.
- [Entry 13 — Trace to Generator](../../fiction/13_trace-to-generator.md). The runtime/policy/history dimensions of a generator made narrative. Two replica bread lots fail blind taste parity despite matching ingredient vectors; a tissue scaffold collapses despite matching templates. The lesson is the spine's: artifact parity is not generator parity.

Other entries dramatize the forward side or the substrate within which generators run:

- *Forward* (generators running, emergence visible): [Entry 07 — WAIT_STATE](../../fiction/07_wait_state.md), [Entry 08 — Kitchen Networks](../../fiction/08_kitchen_networks_and_civic_homeostasis.md), [Entry 12 — The Chord State](../../fiction/12_the_chord_state.md) (the Chord regime as attractor).
- *Substrate* (the thermodynamic limits within which generators must run): [Entry 01 — The Impedance Crash](../../fiction/01_the_impedance_crash.md), [Entry 03 — The Last Commit](../../fiction/03_the_last_commit.md), [Entry 04 — The Gravity Well Migration](../../fiction/04_the_gravity_well_migration.md), [Entry 05 — The Vital Floor](../../fiction/05_the_vital_floor.md), [Entry 09 — The Refusal Registry](../../fiction/09_the_refusal_registry.md), [Entry 10 — The First Breath](../../fiction/10_the_first_breath.md), [Entry 11 — Dashboard of the Commons](../../fiction/11_the_dashboard_of_the_commons.md).
- *Inverse-adjacent*: [Entry 06 — The Authenticity Engine](../../fiction/06_the_authenticity_engine.md) — the question of distinguishing genuine novelty from generated novelty.

The fiction layer is not decoration. It is the project's instrument for noticing when a theoretical claim sounds clean on the page and impossible to live with.

---

## How to read the rest of the project from here

A reading path that uses this document as the entry point:

1. **This document** — the question, the asymmetry, the three walls, the foundational assumption.
2. [Emergence Manifesto v1.3](emergence-manifesto-v1.3.md) — the status-tagged claim set. Claims 1, 2, 4, 5, 6, and 9 are instances of the generator question. Status tags are intact.
3. [Trace to Generator](../emergence/trace-to-generator.md) — the long-form essay on the inverse direction. More expansive in tone; less programmatic than this document.
4. [Simulation → Theory Map](simulation-theory-map.md) — the forward/inverse direction of each simulation, made visible (this map has been updated to surface that distinction).
5. [Grokking: Phase Transition](../emergence/grokking-phase-transition.md) — the clearest empirical demonstration of the inverse direction occurring in a learning system.
6. [Open Problems](../reference/open-problems.md) — what is not solved. Problems 1, 8, and 11 are most directly the inverse-direction frontier.
7. [Course Spine: From Rule to Mind](../../book/09_from_rule_to_mind.md) — the operator → iteration → form → boundary → return-path movement that the forward direction instantiates.

The Emergence Manifesto remains the strongest single statement of the project's claims. This document does not replace it. It sits before it, naming the question those claims are answers to.

---

*The forward direction is cheap. The inverse direction is hard. The asymmetry is the project. Whether it has irreducible singularities — places where verification works but reconstruction cannot — is the working assumption that this document, finally, makes explicit.*
