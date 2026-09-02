# 🧭 Repository Information Architecture

**Lane:** Repository Meta  
**Status:** Working repository policy — §0 written after the foundations audit; §1, §2, §4, §5, §6, §7, and §10 reconciled with it on 2026-09-02  
**Last reviewed:** 2026-09-02  
**Review trigger:** a new research arc, register, or lane; a maintainer decision on §5; any change to the spine table in the README.

This document defines **where new content should live** so the project can scale without turning into one undifferentiated stream of notes.

---

## 0) Foundation and Research Arcs

The repository's mathematical language is defined in the [Foundations
Reconstruction](../../theory/core/mathematical-axioms.md): standard Borel interfaces and stochastic
processes, with typed sequential and parallel composition. This language derives structure through
conditional prediction but does not derive identity, learning, intelligence, goals, or phenomenal
consciousness without additional model structure.

Two bounded research arcs then use that language. The **model-identification arc** studies
equivalence classes, coverage, intervention, and revision under declared model families and costs.
The **viability arc** models intelligence as constrained dynamical performance rather than raw
prediction or unconstrained optimization. Its claims remain challengeable within their stated
models: if optimization can scale without substrate stress, regulator overload, or loss of
corrective feedback, those architecture claims weaken or fail.

> **Relation to the Generator Question.** [The Generator
> Question](../../theory/core/the-generator-question.md) remains an active typed construction and
> model-identification programme. Its former universal formulation is retained as research history:
> the unqualified generator and generic forward/inverse asymmetry do not control the architecture,
> but that correction does not make generation or reconstruction merely historical.

---

## 1) Content Lanes (What goes where)

### `ideas/` → Exploratory notes
Use this for **one thought before it needs a stable home**.  
Characteristics:
- usually around 100–200 words
- begins with an observation, question, hypothesis, analogy, or disturbance
- preserves context and an open tension without requiring a category or destination
- explicitly non-canonical until developed elsewhere

### `meta/research-alignment/leads/` → Externally sourced leads
Use this for **a paper, preprint, or result found outside the repository** that bears on a row of
the [Related Work Map](../research-alignment/related-work-map.md) or on a register claim.  
Characteristics:
- one file per month, append-only within the month
- each entry: source identifier, one sentence on the result, the row or claim it supports or
  challenges, one sentence why, and who recorded it (maintainer or intake run)
- never writes outside the lane; a lead is not an idea, not evidence, not a claim, and not a
  status change
- rules in [`leads/README.md`](../research-alignment/leads/README.md); added 2026-09-02

### A. `book/` → Curated narrative
Use this for the **reader-first canonical path**.  
Characteristics:
- pedagogical ordering
- lower branching, higher coherence
- links outward to theory/code, but does not duplicate all details

### B. `theory/` → Formal + conceptual essays
Use this for claims, derivations, definitions, and argument structure.  
Characteristics:
- can be exploratory, but should still target falsifiability
- may be longer and denser than book chapters
- should clearly mark epistemic status (demonstrated / hypothesized / open / speculative)

### C. `papers/` (and mirrored `docs/papers/`) → Publication packaging
Use this for concise, citation-ready syntheses of a bounded scope.  
Characteristics:
- tighter than theory essays
- explicit method / limitations framing
- less world-building, more formal communication

### D. `logs/` → Applied architecture journals
Use this for "**if we built this for real**" design logs.  
Characteristics:
- architectural options, protocol sketches, operational constraints
- more applied than theory, less polished than papers
- can include unknowns and design forks

### E. `fiction/` → Narrative stress-testing
Use this for scenario-driven exploration constrained by the theory.  
Characteristics:
- story format (dossier, transcript, short story, etc.)
- translates formal constraints into lived consequences
- should not silently contradict core physical/theoretical constraints

### F. `lab/`, `simulation-models/` → Executables
Use this for runnable artifacts and reusable implementation primitives.  
Characteristics:
- code first; docs explain assumptions, parameters, and expected behavior
- when possible, map simulation outcomes back to specific theory claims

---

## 2) Operating Modes

The repository should remain split into two modes. The point is not to make all files equally polished.

### Thinking Space (Exploration)

Contradictions, partial models, scenario tests, and fragments are allowed here. These files should remain visibly exploratory:

- `ideas/` — small, unclassified notes before clustering or synthesis
- `logs/` — applied architecture journals and deployment sketches
- `fiction/` — narrative stress tests constrained by the theory
- `simulation-models/` — toy models, visualizations, and executable probes
- `lab/` — the unified python framework, agentic experiments, cognitive benchmarks, and data-analysis tools
- `meta/` — epistemic framing, repository structure, and maintenance notes

Exploration does not owe the synthesis layer a result. A seed may be recorded before it has a
stable claim, mechanism, home, or falsifier, and it may remain unresolved. Raw unclassified notes
live in [`ideas/`](https://github.com/frnkptrln/systems-and-intelligence/tree/main/ideas). The public
[Thinking Space](https://frnkptrln.github.io/systems-and-intelligence/thinking-space/) maps the wider
exploration landscape and may surface selected seeds without promoting them.

### Synthesis (Claims)

These files assert or compress claims about reality and therefore need clearer epistemic status, definitions, and failure conditions:

*Foundation*

- `theory/core/mathematical-axioms.md` — the Foundations Reconstruction; takes precedence over
  legacy universal claims where they conflict
- `theory/reference/what-this-project-does-not-claim.md` — the negative space, named in the README
  spine beside the reconstruction (entry added 2026-09-02)

*Model-identification arc* (entries added 2026-09-02)

- `meta/repository-meta/identification-claims.md` — the arc's claim register, proposed 2026-09-02
- `theory/core/the-generator-question.md` — the active bounded programme; its superseded universal
  framing is retained in the same file as research history
- `theory/core/from-trace-to-world-binding.md`
- `theory/core/the-witness-principle.md`
- `lab/benchmarks/inverse-reconstruction/README.md` — the arc's measured results; the code is the
  executable, the README is the synthesis

*Emergence claims, viability arc, and identity branch*

- `meta/repository-meta/core-claims.md` — the register for the viability arc and identity branch
- `theory/optimization/optimization-and-its-blindness.md` — the hinge the README spine names for the
  viability arc (entry added 2026-09-02)
- `papers/viable-corridor.md` — the arc's stabilized artifact, named in the README spine (entry
  added 2026-09-02; the `papers/` lane as a whole is listed below)
- `theory/core/emergence-manifesto-v1.3.md`
- `theory/core/thermodynamics-of-orchestration.md`
- `theory/identity/minimal-thermodynamic-agent.md`
- `theory/veto/substrate-veto-thermodynamics.md`
- `theory/veto/ai-alignment-biological-veto.md`
- `theory/veto/biological-veto-architectural-requirements.md`
- `theory/teo-framework/`

*Situated-competence extension* (entry added 2026-09-02; placement proposed)

- `theory/core/competence-constraint-and-verification.md` — named in the README as the extension's
  central synthesis; the README says the extension adds no new primitive and is not a third arc

*Maps, reference, and packaging*

- `theory/core/simulation-theory-map.md`
- `theory/reference/open-problems.md`
- `book/`
- `papers/` and `docs/papers/`

TEO, the veto documents, and the minimal thermodynamic agent are the synthesis layer of the
viability arc; they are not the whole synthesis layer. As of 2026-09-02 the identification arc's
synthesis is proposed here as the foundation, the Generator Question in its bounded form, the loop
note, the Witness Principle, the benchmark README, and the register listed above. The register also
draws on `theory/core/decision-relevant-identifiability.md` and
`lab/experiments/active_identifiability/README.md`; whether those two join this list is left to the
maintainer.

When a document moves from Thinking Space to Synthesis, it should gain explicit claims, definitions, links to proof artifacts, and a statement of what would count against it.

---

## 3) Minimal Architecture

The current folder structure is mostly sufficient. Do not reorganize the whole repository unless a concrete duplication or navigation failure requires it.

Recommended conceptual architecture:

| Conceptual layer | Current location | Role |
|:---|:---|:---|
| Entry point | `README.md`, `docs/index.md` | Short orientation and one reading path |
| Seeds | `ideas/` | Atomic notes before classification, clustering, or synthesis |
| Core claims | `theory/` (sub-dirs: `core/`, `veto/`, `emergence/`, `identity/`, `symbiotic/`, `narrative/`, `reference/`, `teo-framework/`, `human-organism-silicon-age/`), `papers/`, `book/` | Synthesis layer and publication packaging |
| Models | `simulation-models/`, `lab/core/`, `lab/orchestration/` | Executable demonstrations and reusable primitives |
| Lab | `logs/`, `fiction/`, `lab/benchmarks/`, `lab/experiments/`, `lab/tools/`, `lab/data-analysis/` | Experiments, stress tests, applied designs, narrative probes |
| Meta | `meta/` | Information architecture, epistemic notes, maintenance rules |

The architecture should optimize for navigability, not taxonomy purity.

---

## 4) Three Non-Trivial Viability and Identity Claims to Keep Testable

The three claims below belong to the viability arc and the identity branch. Their register, with
artifacts marked by evidential kind and with failure conditions, is [Core Claims](core-claims.md),
which also carries a fourth claim (Vital Floors in Governance) that is not repeated here. The
model-identification arc has its own register, [Identification Claims](identification-claims.md);
its entries are anchored to measured or exact results inside declared testbeds, with unmeasured
halves recorded as such, rather than to architecture hypotheses, so they are listed there and not in
this section.

1. **Substrate Veto:** Implemented optimizers have finite resource limits; the testable design claim
   is that an independently enforced, measured capacity constraint can bound selected actions before
   substrate failure. Physical collapse is not itself a safe veto.
2. **Impedance Matching:** High-speed silicon proposal generation becomes unsafe when it exceeds the absorption bandwidth of slower biological or institutional regulators; action budgets and latency are safety mechanisms, not UX defects.
3. **Identity Persistence:** The current hypothesis predicts that systems with high prediction and adaptation scores can still differ in the stability of goals, constraints, and values under perturbation; whether co-active constraint structure improves that stability must be tested against sequential alternatives.

Each claim should remain connected to at least one simulation, benchmark, or explicit open problem.

---

## 5) Proof Artifact to Build Next

**Status as of 2026-09-02:** unchanged since pre-audit; maintainer decision pending. The section
below still names the control-plane simulation as the artifact to build next. A runnable toy with
this purpose exists at
[`simulation-models/alignment-and-veto/human-vital-systems/`](../../simulation-models/alignment-and-veto/human-vital-systems/README.md)
(its own status line: "Proof artifact"; registered under Claim 4 of [Core Claims](core-claims.md)
as a *runnable toy*, with the note that nothing there is calibrated against a real vital system).
In the visible git history this section and that toy enter together in the root commit of
2026-07-20, and the section has not been edited since. Whether the toy discharges this section, or
whether the section describes a larger artifact that is still planned, is not decided here.

Side by side with this section, what [Open Problems](../../theory/reference/open-problems.md) names
as next, as of 2026-09-02:

| Arc | This section (pre-audit) | What `open-problems.md` names as next |
|:---|:---|:---|
| Viability arc | Human Vital Systems Control Plane Simulation | `open-problems.md` does not label its problems by arc and names no corridor or control-plane item as next. The arc's own open list is [Canonical Path v2 §9](canonical-path-v2.md#9-open-problems): proving sufficiency and deriving the critical coupling; operationalizing the effective parameters for real systems; a finite-size coherence result; validating P7/P8 on real agent systems; overshoot–collapse dynamics; and whether the corridor stays in this repository. The paper's post-v1.0 checklist and the "What's next" list in [`docs/index.md`](../../docs/index.md) overlap with these on rigorous sufficiency and a real-agent P7/P8 test; the checklist otherwise lists submission mechanics and external-review reads, and the index list adds external review and two identification-arc items. |
| Identity branch | — | Selected: Problem 1: a preregistered longitudinal experiment with an interaction-shaped agent, a transcript-initialized control, and an optimized mimic. Problem 3: a preregistered experiment with relational history as the independent variable. Problem 8: an optimized mimic against the full measurement suite, then held-out constraints and lures. Problem 10: replicate the three-way comparison on real models with matched capabilities. Problem 7: a constructive architecture plus a preregistered perturbation suite with a trace-matched control. |
| Model-identification arc | — | Problem 11's open remainder (five of eight items): learned searchers and program synthesizers under matched budgets, the IFS testbed, external SINDy/PySR baselines, re-simulation divergence, and a within-group cost gradient for the v1.13 pool arm. Problem 14: the frozen [Learned-Searcher](../../lab/benchmarks/learned-searcher/README.md) protocol, execution target deliberately unregistered. Adjacent, arc placement not decided: Problem 15, vary the referee properties independently against stronger proposers; Problem 18, compare exact replay, predictive, policy-preserving, bisimulation, and adaptively refined equivalences under matched budgets. |

### Human Vital Systems Control Plane Simulation

**Purpose:** Demonstrate whether Vital Impact Cards and Layer-2 vetoes improve outcomes compared with naive efficiency optimization.

**Inputs:**
- synthetic districts with food access, indoor temperature, care latency, utility continuity, and trust indicators
- policy proposals generated by a Layer-1 planner
- random shocks: cold front, logistics delay, clinic overload, data lag

**Parameters:**
- action budget per planning cycle
- human review bandwidth
- threshold floors per vital indicator
- uncertainty level and data delay
- strength of local community compensation

**Expected behavior:** Naive optimization improves aggregate efficiency while occasionally violating vital floors. The control-plane version should sacrifice throughput but reduce irreversible red-line violations and improve recovery after shocks.

**Failure condition:** If the control-plane version does not reduce vital-floor violations, reduces them only by hiding harm in unmeasured indicators, or collapses under review latency, the architecture claim should be weakened or rejected.

---

## 6) Internal Language Anchors

Custom terms should be kept, but anchored to known concepts.

| Repo term | Systems theory anchor | Physics anchor | Computer science anchor |
|:---|:---|:---|:---|
| TEO | viability theory, control theory, coupled dynamical systems | entropy production, dissipation bounds | constrained optimization, resource-bounded agents |
| Substrate Veto | regulator failure boundary, viability constraint | Landauer cost, heat dissipation, finite carrying capacity | hardware limits, circuit breakers, backpressure |
| Action Budgets | rate limiting, requisite variety management | bounded entropy production | quotas, schedulers, token/compute budgets |
| Impedance Matching | regulator bandwidth matching | timescale separation, coupling limits | queues, flow control, human-in-the-loop latency |
| Biological Veto | distributed human regulator | biospheric carrying capacity | approval gates, commit authorization |
| Chord/Arpeggio | stable attractor vs transient trajectory | phase-space stability | persistent state vs stateless response policy |
| Vital Impact Card | observability and control dashboard | state variables near viability boundary | typed policy output, safety case, decision record |
| Candidate family (model class) | model set / model structure in system identification (Ljung 1999) | parametrized family of Hamiltonians or effective theories | hypothesis class; version space (Mitchell 1982) |
| Equivalence class (consistent-process-model class) | observational equivalence; minimal realization (Kalman) | parameter degeneracy; gauge equivalence; sloppy models | version space after evidence; bisimulation |
| Coverage | persistence of excitation; informative experiments (Ljung 1999) | sampling of phase space; ergodicity of the orbit | test coverage; teaching dimension (Goldman & Kearns 1995) |
| Intervention hierarchy (watching < perturbing < preparing) | open-loop vs closed-loop identification; input design | passive observation vs state preparation | seeing vs doing (Pearl 2009); membership queries (Angluin 1987); active learning |
| Readout / witness | observation map, sensor model; distinguishing sequence (Moore 1956) | measurement operator; observable | distinguishing input (Lee & Yannakakis 1994); certificate checked by a verifier; oracle query |

The rows from *Candidate family* downward were added on 2026-09-02 for the model-identification
arc. They anchor terms already in use in the benchmark README, the Witness Principle, the Active
Identifiability README, and the [Concept Registry](concept-registry.md); none is a new coinage,
and the anchors are standard system-identification and causal-inference concepts.

---

## 7) Decision Rules (Quick triage)

When adding a new artifact, ask:

If it is still one small, unfinished observation, question, or hypothesis, record it as an
exploratory note in `ideas/` without forcing it through the choices below.

If it is an externally sourced lead — a paper, preprint, or result found outside the repository —
record it in the [leads lane](../research-alignment/leads/README.md). A lead stays in the lane:
matrix rows, registers, status lines, and `ideas/` change only through a maintainer-authored
change.

1. **Is this primarily runnable?**  
   → put in `simulation-models/`, `lab/core/`, or `lab/orchestration/`.
2. **Is this primarily a formal argument?**  
   → put in `theory/`.
3. **Is this optimized for linear reading?**  
   → put in `book/`.
4. **Is this publication-facing and compact?**  
   → put in `papers/`.
5. **Is this an applied design notebook with open decisions?**  
   → put in `logs/`.
6. **Is this a narrative scenario to test implications?**  
   → put in `fiction/`.

If two answers are true, choose one **home location** and cross-link instead of duplicating.

If the artifact asserts or promotes a load-bearing claim, run it through [Feynman
Mode](feynman-mode.md) before committing it (toy model? counterexample? load-bearing assumption?
beautiful word in place of a mechanism?) and add any load-bearing term to the [Concept
Registry](concept-registry.md) in the same change. An explicitly exploratory seed is exempt until it
asks to enter the synthesis layer.

---

## 8) Minimal Maturity Tags (recommended)

For non-code documents, add a short status line near the top. Notes in `ideas/` use
`Status: Exploratory note` and remain outside the maturity ladder until they begin to develop into a
larger artifact.

- `Status: Draft`
- `Status: Working Note`
- `Status: Formalized`
- `Status: Publication Draft`

This keeps expectations clear for readers and contributors.

---

## 9) Anti-Entropy Rules

To keep the repository "rounder":

1. **One source of truth per concept.**  
   Everything else links to it.
2. **No silent duplicates.**  
   If mirrored for docs rendering, note the canonical file.
3. **Map code ↔ claim.**  
   Each simulation README should name the theory claims it informs.
4. **Separate modes of writing.**  
   Theory argues, logs design, fiction dramatizes, papers compress.

---

## 10) Suggested Next Cleanup Steps

Each step checked against the repository on 2026-09-02:

1. Add a short `Status + Scope + Links` header template to every `logs/*.md`.  
   **Done in substance (verified 2026-09-02).** All twenty logs carry a status line and a scope
   line, and `logs/README.md` carries the template. The format is not uniform: logs 001–013 use a
   bullet header (Mode, Status, Date, Scope, Depends on), logs 014–020 use bold fields with the same
   names.
2. Build a small index table mapping each `logs` entry to related `theory` and `simulation-models` files.  
   **Not done (verified 2026-09-02).** `logs/README.md` has an ordered list with one-line
   descriptions, not a mapping to theory and simulation files; the mapping exists only piecemeal in
   the logs' own `Depends on:` lines.
3. Add "home file" references where `papers/` and `docs/papers/` intentionally mirror each other.  
   **Moot (verified 2026-09-02).** `docs/papers` is a symlink to `../papers`, so there is no mirror
   to annotate. The wording "mirrored `docs/papers/`" in §1.C and the `docs/papers/` entry in §2
   are left as written and reported as stale descriptions.
