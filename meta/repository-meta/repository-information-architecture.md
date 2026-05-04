# 🧭 Repository Information Architecture

This document defines **where new content should live** so the project can scale without turning into one undifferentiated stream of notes.

---

## 0) Core Generative Idea

Intelligence is modeled here as constrained dynamical viability, not raw prediction or unconstrained optimization. A system becomes unsafe when local optimization outruns the carrying capacity of its substrate, regulators, or feedback channels; survivable intelligence requires entropy budgets, impedance matching, and veto paths that keep adaptation inside a viable corridor.

This claim is challengeable: if unbounded optimization can remain stable without substrate stress, regulator overload, or loss of corrective feedback, the central architecture is wrong.

---

## 1) Content Lanes (What goes where)

### A. `docs/book/` → Curated narrative
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

### F. `simulation-models/`, `core/`, `systems-orchestration/` → Executables
Use this for runnable artifacts and reusable implementation primitives.  
Characteristics:
- code first; docs explain assumptions, parameters, and expected behavior
- when possible, map simulation outcomes back to specific theory claims

---

## 2) Operating Modes

The repository should remain split into two modes. The point is not to make all files equally polished.

### Thinking Space (Exploration)

Contradictions, partial models, scenario tests, and fragments are allowed here. These files should remain visibly exploratory:

- `logs/` — applied architecture journals and deployment sketches
- `fiction/` — narrative stress tests constrained by the theory
- `simulation-models/` — toy models, visualizations, and executable probes
- `agentic-test-suite/` — experimental identity and observer-attribution tests
- `benchmarks/` — cognitive stress scenarios and evaluation scaffolding
- `tools/` and `data-analysis/` — exploratory diagnostics and visualizers
- `meta/` — epistemic framing, repository structure, and maintenance notes

### Synthesis (Claims)

These files assert or compress claims about reality and therefore need clearer epistemic status, definitions, and failure conditions:

- `theory/emergence-manifesto-v1.2.md`
- `theory/thermodynamics-of-orchestration.md`
- `theory/minimal-thermodynamic-agent.md`
- `theory/substrate-veto-thermodynamics.md`
- `theory/ai-alignment-biological-veto.md`
- `theory/biological-veto-architectural-requirements.md`
- `theory/teo-framework/`
- `theory/simulation-theory-map.md`
- `theory/open-problems.md`
- `docs/book/`
- `papers/` and `docs/papers/`

When a document moves from Thinking Space to Synthesis, it should gain explicit claims, definitions, links to proof artifacts, and a statement of what would count against it.

---

## 3) Minimal Architecture

The current folder structure is mostly sufficient. Do not reorganize the whole repository unless a concrete duplication or navigation failure requires it.

Recommended conceptual architecture:

| Conceptual layer | Current location | Role |
|:---|:---|:---|
| Entry point | `README.md`, `docs/index.md` | Short orientation and one reading path |
| Core claims | `theory/`, `papers/`, `docs/book/` | Synthesis layer and publication packaging |
| Models | `simulation-models/`, `core/`, `systems-orchestration/` | Executable demonstrations and reusable primitives |
| Lab | `logs/`, `benchmarks/`, `agentic-test-suite/`, `fiction/`, `tools/` | Experiments, stress tests, applied designs, narrative probes |
| Meta | `meta/` | Information architecture, epistemic notes, maintenance rules |

The architecture should optimize for navigability, not taxonomy purity.

---

## 4) Three Non-Trivial Claims to Keep Testable

1. **Substrate Veto:** An optimizer coupled to a finite substrate must be bounded by dissipation capacity; if optimization pressure exceeds $D_{\max}$, the system collapses or must throttle.
2. **Impedance Matching:** High-speed silicon proposal generation becomes unsafe when it exceeds the absorption bandwidth of slower biological or institutional regulators; action budgets and latency are safety mechanisms, not UX defects.
3. **Identity Persistence:** A system with high prediction and adaptation scores can still lack stable identity if its goals, constraints, and values are only time-multiplexed; persistent identity requires co-active constraint structure under perturbation.

Each claim should remain connected to at least one simulation, benchmark, or explicit open problem.

---

## 5) Proof Artifact to Build Next

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

---

## 7) Decision Rules (Quick triage)

When adding a new artifact, ask:

1. **Is this primarily runnable?**  
   → put in `simulation-models/`, `core/`, or `systems-orchestration/`.
2. **Is this primarily a formal argument?**  
   → put in `theory/`.
3. **Is this optimized for linear reading?**  
   → put in `docs/book/`.
4. **Is this publication-facing and compact?**  
   → put in `papers/`.
5. **Is this an applied design notebook with open decisions?**  
   → put in `logs/`.
6. **Is this a narrative scenario to test implications?**  
   → put in `fiction/`.

If two answers are true, choose one **home location** and cross-link instead of duplicating.

---

## 8) Minimal Maturity Tags (recommended)

For non-code documents, add a short status line near the top:

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

1. Add a short `Status + Scope + Links` header template to every `logs/*.md`.
2. Build a small index table mapping each `logs` entry to related `theory` and `simulation-models` files.
3. Add "home file" references where `papers/` and `docs/papers/` intentionally mirror each other.
