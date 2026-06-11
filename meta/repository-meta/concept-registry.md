# Concept Registry — the Zone File

**Status:** Reference — maintained alongside the concepts themselves.

**Scope:** Every load-bearing term in the repository, with its layer, home file, epistemic status, and operationalization. This is the "DNS" of the project's personal web: for each name, where it resolves, and whether it is a *protocol* (operationalized / formalized) or a *poetic hostname* (narrative, and marked as such). The governing rule, from the [glossary](../../theory/reference/glossary.md) and [Canonical Path v2](canonical-path-v2.md): **a term with no layer, no home, no experiment, and no open problem is decoration.** This page makes the rule auditable.

**Status vocabulary:** `operationalized` (has a runnable experiment / measurement) · `formalized` (math, schema, or metric exists; no decisive experiment yet) · `hypothesis` (tagged claim, falsifiable in principle) · `speculative` (entertained, not committed) · `narrative` (poetic hostname — legitimate, but never evidence) · `retired` (no longer used as a claim).

---

## Spine

| Concept | Home | Status | Operationalization / anchor |
|:---|:---|:---|:---|
| The Generator Question (forward/inverse asymmetry) | [the-generator-question.md](../../theory/core/the-generator-question.md) | formalized framing, on two tagged `[FOUNDATIONAL ASSUMPTION]`s | the inverse benchmark; the three walls (Cook, Chaitin, Gödel) |
| Trace → Generator | [trace-to-generator.md](../../theory/emergence/trace-to-generator.md) | hypothesis → **operationalized** | [inverse-reconstruction benchmark](../../lab/benchmarks/inverse-reconstruction/README.md) |
| Construction vs. Deduction | [construction-vs-deduction.md](../../theory/computation/construction-vs-deduction.md) | formalized framing (Curry–Howard is theorem-grade) | family-search Occam curves; Bishop/Howard/Martin-Löf |
| Consistent-generator equivalence class | benchmark README; [Open Problem 11](../../theory/reference/open-problems.md) | **operationalized (measured)** | CA rule 90 single-seed: class size 8; collapse under interventions |

## Research frontier

| Concept | Home | Status | Operationalization / anchor |
|:---|:---|:---|:---|
| Inverse-reconstruction benchmark (v0–v1.2) | [lab/benchmarks/inverse-reconstruction/](../../lab/benchmarks/inverse-reconstruction/README.md) | **operationalized** | noise / observability / coverage / interventions / family-search floor |
| Capability loading | [Viable Corridor §7.1, App. C.4/D](../../papers/viable-corridor.md) | demonstrated **in-model** (two independent models) | TEO ODE + agent-ecology ABM; real agents open |
| Grokking, generator reading | [grokking-phase-transition.md](../../theory/emergence/grokking-phase-transition.md) | hypothesis with strong external anchor | Power 2022; Nanda 2023 (mech-interp executed the inverse) |
| Provenance depth / verification economy | [Log 017](../../logs/017_provenance-depth-and-the-verification-economy.md) | formalized schema (proposal) | narrative origin: [Entry 15](../../fiction/15_the_exchange_rate.md); C2PA/SBOM siblings |

## Identity layer

| Concept | Home | Status | Operationalization / anchor |
|:---|:---|:---|:---|
| Mirror Problem | [Open Problem 1](../../theory/reference/open-problems.md); dramatized in [Entry 02](../../fiction/02_interrogation_of_a_mirror.md) | open problem | Observer Divergence protocol (mock embeddings — real models pending) |
| Chord vs. Arpeggio | [chord-vs-arpeggio-identity.md](../../theory/identity/chord-vs-arpeggio-identity.md) | hypothesis | IP metric; Co-Instantiation open problem |
| Identity Persistence (IP) | [lab/metrics/identity_persistence.py](../../lab/metrics/identity_persistence.py) | formalized metric | not yet run on real models |
| Δ-Kohärenz | [lab/metrics/delta_coherence.py](../../lab/metrics/delta_coherence.py) | formalized metric | not yet run on real models |
| Identity reduction (identity *as* generator recovery) | [the-generator-question.md](../../theory/core/the-generator-question.md) | tagged `[FOUNDATIONAL ASSUMPTION]` | both failure directions stated; runtime caveat in [Log 016](../../logs/016_the-runtime-is-part-of-the-generator.md) |
| Consciousness (global availability + self-reconstruction loop) | [consciousness-as-global-availability.md](../../theory/identity/consciousness-as-global-availability.md) | hypothesis (architecture) + `[SPECULATIVE]` (experience — explicitly out of scope) | self-reading universe; Three-Layer agent; GNW/Hofstadter/Metzinger anchors |

## Safety / application layer

| Concept | Home | Status | Operationalization / anchor |
|:---|:---|:---|:---|
| TEO (Thermodynamics of Emergent Orchestration) | [teo-framework/](../../theory/teo-framework/README.md); [derivation](../../theory/core/thermodynamics-of-orchestration.md) | formalized model | [teo-civilization sim](../../simulation-models/alignment-and-veto/teo-civilization/README.md) |
| Viable Corridor | [papers/viable-corridor.md](../../papers/viable-corridor.md) | `[FORMAL]` (necessity) + `[CONJECTURE]` (sufficiency) + `[HEURISTIC]` (civilization mapping) | Appendix C (ODE) + D (ABM); working draft |
| Substrate Veto | [substrate-veto-thermodynamics.md](../../theory/veto/substrate-veto-thermodynamics.md) | hypothesis / model assumption | binds endogenously in the canonical TEO model |
| Biological Veto / Bootloader | [ai-alignment-biological-veto.md](../../theory/veto/ai-alignment-biological-veto.md) | design hypothesis | [ai-alignment-veto toy](../../simulation-models/alignment-and-veto/ai-alignment-veto/README.md) |
| Action Budgets (hard vs. soft) | IA-doc anchors; [paper P7](../../papers/viable-corridor.md) | **operationalized in-model** | [agent-ecology ABM](../../simulation-models/alignment-and-veto/agent-ecology/README.md) |
| Impedance Matching / Latency as Mercy | [Log 002](../../logs/002_impedance-mismatch-friction.md), [Log 012](../../logs/012_latency-as-mercy.md) | design hypothesis | no simulation yet; dramatized in [Entry 01](../../fiction/01_the_impedance_crash.md) |
| Transition Problem | [the-transition-problem.md](../../theory/veto/the-transition-problem.md) | open problem | flagged in paper §7.4 as harder than the static result |

## Narrative layer (poetic hostnames — marked, never evidence)

| Concept | Home | Status | Notes |
|:---|:---|:---|:---|
| Machines of Loving Grace | [machines-of-loving-grace.md](../../theory/narrative/machines-of-loving-grace.md) | narrative | formal counterpart: the Viable Corridor paper |
| Narrative as Cognitive Technology | [narrative-as-cognitive-technology.md](../../theory/narrative/narrative-as-cognitive-technology.md) | hypothesis (about narratives) | internal datum: Entry 15 → Log 017 |
| The Inversion / Exchange Rate / Assay vocabulary | [Entry 15](../../fiction/15_the_exchange_rate.md) | narrative | formal counterpart: Log 017 |
| Fractal Architecture of Emergence | [fractal-architecture-of-emergence.md](../../theory/emergence/fractal-architecture-of-emergence.md) | hypothesis, **under-evidenced** | related-work map demands scale-invariance diagnostics before "fractal" is more than a figure |
| Mycelial Veto | [the-mycelial-veto.md](../../theory/veto/the-mycelial-veto.md) | narrative/speculative | **no operationalization — flagged by this registry**: needs an experiment, an open problem, or an explicit narrative marking |
| Thermodynamic Hardware Manifesto | [thermodynamic-hardware-manifesto.md](../../theory/core/thermodynamic-hardware-manifesto.md) | `[SPECULATIVE]` | frontdoor lists hardware prototyping as speculative/long-horizon |
| "Grand Synthesis" | — | **retired** | removed from all frontdoor surfaces (2026-06); kept here so its retirement is on record |

---

*Maintenance rule: new load-bearing terms enter this registry in the same change that introduces them, or they don't enter the repository. Terms whose row cannot be filled honestly (no home, no status, no anchor) are either marked narrative or removed. The registry is the audit the governance rule always implied — kept short enough to actually read.*
