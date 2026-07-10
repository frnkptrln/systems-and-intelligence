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
| Invariance (what survives a transformation) | [invariance-and-identity.md](../../theory/core/invariance-and-identity.md) | formalized framing (Klein/Noether anchors) | IP as invariance-under-perturbation; class-invariants reading of the benchmark; rule: never claim an invariant without naming the group |
| Consistent-generator equivalence class | benchmark README; [Open Problem 11](../../theory/reference/open-problems.md) | **operationalized (measured)** | CA rule 90 single-seed: class size 8; collapse under interventions |
| Measurement vs. intervention (coupling is not identification) | [measurement-as-weak-intervention.md](../../theory/core/measurement-as-weak-intervention.md) | formalized framing — three of four regimes measured | two axes: dynamical footprint × identifying power; regimes 1–3 = benchmark v1.1 (watching < perturbing < preparing), unmarked-guess mirror = v1.3; regime 4 (the metric enters the generator) = Goodhart/Campbell/Lucas + Log 018 H3 (pre-registered, untested); identity edition measured in [exp6](../../lab/experiments/exp6_binding_observables.py) — the hierarchy's payoff is *located*: queries win where the trace has coverage gaps; for constantly-exercised differences, right-level watching sufficed |

## Research frontier

| Concept | Home | Status | Operationalization / anchor |
|:---|:---|:---|:---|
| Inverse-reconstruction benchmark (v0–v1.10) | [lab/benchmarks/inverse-reconstruction/](../../lab/benchmarks/inverse-reconstruction/README.md) | **operationalized** | noise / observability / coverage / interventions / family-search floor / model exploitation / honest uncertainty / closed-loop measurement / ensemble size / composition level-jump (v1.8) / substitution-dependency boundary (v1.9) / budget-matched redundant mutual support under sparse shocks (v1.10) |
| Capability loading | [Viable Corridor §7.1, App. C.4/D](../../papers/viable-corridor.md) | demonstrated **in-model** (two independent models) | TEO ODE + agent-ecology ABM; real agents open |
| Grokking, generator reading | [grokking-phase-transition.md](../../theory/emergence/grokking-phase-transition.md) | hypothesis with strong external anchor | Power 2022; Nanda 2023 (mech-interp executed the inverse) |
| Provenance depth / verification economy | [Log 017](../../logs/017_provenance-depth-and-the-verification-economy.md) | formalized schema (proposal) | narrative origin: [Entry 15](../../fiction/15_the_exchange_rate.md); C2PA/SBOM siblings |
| Animism as generator prior | [animism-as-generator-prior.md](../../theory/emergence/animism-as-generator-prior.md) | hypothesis | the agent prior over equivalence classes (HADD, Guthrie, Dennett's intentional stance); Occam-sibling with world-dependent payoff |
| Information ladder (Shannon → Kolmogorov → Bateson → computation) | [static-information-and-living-process.md](../../theory/computation/static-information-and-living-process.md) | formalized framing (reading aid over textbook formalisms) | H/K in the axioms; Bateson's "difference that makes a difference" = the v1.1 distinguishing-trace result, named; computation-as-unfolding = Log 016 |
| Generator composition (symbiogenesis bridge) | [static-information-and-living-process.md](../../theory/computation/static-information-and-living-process.md) | `[HYPOTHESIZED]` — **first artifact measured** | Margulis 1967; "life is an ecology of functions" (Agüera y Arcas, podcast, 2026); BFF as illustration; [benchmark v1.8](../../lab/benchmarks/inverse-reconstruction/composition.py): the empty equivalence class certifies a higher-order generator; visible only where the observed generator transmits the coupling (rule-90 center-blindness); ecology/population version open |
| Co-stabilization (self-maintenance threshold) | [static-information-and-living-process.md](../../theory/computation/static-information-and-living-process.md) (§open questions) | `[HYPOTHESIZED]` at the ecology/self-maintenance level; **first mutual-support mechanism measured** in [v1.10](../../lab/benchmarks/inverse-reconstruction/co_stabilization_redundancy.py) | v1.9 rules out substitution coupling as sufficient. v1.10 shows budget-matched redundant repair improving viability under sparse shocks across the sensitivity grid, with no gain under common-mode shocks; this is a designed support network, not spontaneous ecology or metabolism. Endogenous population version open. NOT self-binding (phase 6). |
| World models & VLA (the spine, industrialized) | [world-models-and-vla.md](../../theory/ai/world-models-and-vla.md) | hypothesis (mapping) | world models = trace→generator at scale (model exploitation = adversarial divergence queries against one's own model); VLA = the generator coupled to matter, d=0 at every timestep; exploitation bridge measured in benchmark v1.3 |

## Identity layer

| Concept | Home | Status | Operationalization / anchor |
|:---|:---|:---|:---|
| Mirror Problem | [Open Problem 1](../../theory/reference/open-problems.md); dramatized in [Entry 02](../../fiction/02_interrogation_of_a_mirror.md) | open problem | Observer Divergence protocol (mock embeddings — real models pending) |
| Chord vs. Arpeggio | [chord-vs-arpeggio-identity.md](../../theory/identity/chord-vs-arpeggio-identity.md) | hypothesis — first toy dissociation measured; functionally deflated; adversarially probed | IP metric; Co-Instantiation open problem; [exp5](../../lab/experiments/exp5_availability_dissociation.py): bindings dissociate behaviorally (violations 0.74/0.59/0.03), and sequential-within-one-step is measurably still an arpeggio (12% leak); functional status (§ in home file): joint satisfaction at the commitment boundary — refresh/commit ratio + composition, not simultaneity; [exp7](../../lab/experiments/exp7_adversarial_arpeggio.py): hand-built mimics fail to fake the regime — the commit property under lure is the unfooled measurement; optimized mimic open |
| Identity Persistence (IP) | [lab/metrics/identity_persistence.py](../../lab/metrics/identity_persistence.py) | formalized metric — blind class demonstrated | not yet run on real models; in [exp5](../../lab/experiments/exp5_availability_dissociation.py) its ordering is by design (the sanity floor), not a finding; [exp7](../../lab/experiments/exp7_adversarial_arpeggio.py): consultation-without-composition scores 1.0 — IP certifies the guest list, not the negotiation |
| Δ-Kohärenz | [lab/metrics/delta_coherence.py](../../lab/metrics/delta_coherence.py) | formalized metric | not yet run on real models; measured limit ([exp5](../../lab/experiments/exp5_availability_dissociation.py)): blind to binding structure at toy scale — diagnosed in [exp6](../../lab/experiments/exp6_binding_observables.py) as a wrong-*level* failure: per-step increment statistics see the same binding at \|d\| ≈ 4 |
| Identity reduction (identity *as* generator recovery) | [the-generator-question.md](../../theory/core/the-generator-question.md) | tagged `[FOUNDATIONAL ASSUMPTION]` | both failure directions stated; runtime caveat in [Log 016](../../logs/016_the-runtime-is-part-of-the-generator.md) |
| Consciousness (global availability + self-reconstruction loop) | [consciousness-as-global-availability.md](../../theory/identity/consciousness-as-global-availability.md) | hypothesis (architecture) + `[SPECULATIVE]` (experience — explicitly out of scope) | self-reading universe; Three-Layer agent; GNW/Hofstadter/Metzinger anchors; §Testable Direction now run — [exp5](../../lab/experiments/exp5_availability_dissociation.py) (failure condition not triggered; Δ-K half carried no signal); bounded-not-total integration `[HYPOTHESIZED]` with the collective-attention boundary case in the [loop note](../../theory/core/from-trace-to-world-binding.md); bounded self-reconstruction (point 4): complete certified identification is not guaranteed; local useful models may converge; levels = reflexive depth (Kegan 1982, subject-object move = one loop turn; interview-grade anchor), phenomenal degrees out of scope |
| Reflexive depth (Kegan's subject-object move) | [consciousness-as-global-availability.md](../../theory/identity/consciousness-as-global-availability.md) (§On Levels) | `[HYPOTHESIZED]` mapping; adaptive-estimation toy operationalized in [exp8](../../lab/experiments/exp8_reflexive_depth.py) | exp8 shows an adaptive Kalman estimator beating a fixed-$Q$ estimator after a volatility shift and remaining unable to remove a sole-channel bias; this measures second-order adaptation in one Gaussian tracking task, not Kegan stages or consciousness. Depth 3, external-reference control, alternative adaptive baselines, and real agents open. |
| Consciousness as generator coherence | [machine-consciousness-as-generator-coherence.md](../../theory/identity/machine-consciousness-as-generator-coherence.md) | hypothesis (spine reading) + `[SPECULATIVE]` (experience — out of scope) | companion to the global-availability node; "no Turing test for consciousness" = trace underdetermines generator; coherence work = K-axis; attention = regime-3 intervention turned inward; Bach & Sorensen (2025/26) as pressure test, marked a position paper not evidence |
| Psychedelics as perturbation | [psychedelics-as-perturbation.md](../../theory/identity/psychedelics-as-perturbation.md) | hypothesis (mapping over REBUS) | self-intervention reading; integration = invariant extraction; sober basis as referee; epistemics only — practice out of scope |

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
| The city as deployed intelligence | [the-city-as-deployed-intelligence.md](../../theory/human-organism-silicon-age/the-city-as-deployed-intelligence.md) | hypothesis, strong external anchors | West's scaling laws (capability loading, measured); Jacobs vs. Moses (the documented single-axis catastrophe); flagged as the tractable Class B field site (N=thousands vs N=1) |
| City panel protocol (pre-registered) | [Log 018](../../logs/018_the-city-panel-protocol.md) | **protocol** — frozen before data contact | H1 conjunction / H2 capability loading / H3 unwatched axis, with falsifiers; commit hash as timestamp (Log 017 mechanism); execution open, explicitly an invitation |

## Narrative layer (poetic hostnames — marked, never evidence)

| Concept | Home | Status | Notes |
|:---|:---|:---|:---|
| Machines of Loving Grace | [machines-of-loving-grace.md](../../theory/narrative/machines-of-loving-grace.md) | narrative | formal counterpart: the Viable Corridor paper |
| Narrative as Cognitive Technology | [narrative-as-cognitive-technology.md](../../theory/narrative/narrative-as-cognitive-technology.md) | hypothesis (about narratives) | internal datum: Entry 15 → Log 017 |
| Art–Science: one practice, two referees | [art-science-one-practice-two-referees.md](../../theory/narrative/art-science-one-practice-two-referees.md) | hypothesis | receipts: elegance curves (family search), Entry 15 → Log 017, Morelli/Ginzburg (evidential paradigm) |
| The Inversion / Exchange Rate / Assay vocabulary | [Entry 15](../../fiction/15_the_exchange_rate.md) | narrative | formal counterpart: Log 017 |
| The conscious universe / transmission cosmology | [Entry 16](../../fiction/16_the_second_receiver.md) | narrative — *kept question*, not a claim | the divergence-query analysis lives in the benchmark README and the psychedelics note; the story dramatizes the retreat-tell and the honest residue |
| Emergent spacetime / LQG motifs | [Entry 16](../../fiction/16_the_second_receiver.md) (world-texture) | narrative | theory-side: at most a future intake line in generative-form-systems; no repo claims about quantum gravity |
| Fractal Architecture of Emergence | [fractal-architecture-of-emergence.md](../../theory/emergence/fractal-architecture-of-emergence.md) | hypothesis, **under-evidenced** | related-work map demands scale-invariance diagnostics before "fractal" is more than a figure |
| Mycelial Veto | [the-mycelial-veto.md](../../theory/veto/the-mycelial-veto.md) | narrative/speculative | **no operationalization — flagged by this registry**: needs an experiment, an open problem, or an explicit narrative marking |
| Thermodynamic Hardware Manifesto | [thermodynamic-hardware-manifesto.md](../../theory/core/thermodynamic-hardware-manifesto.md) | `[SPECULATIVE]` | frontdoor lists hardware prototyping as speculative/long-horizon |
| "Grand Synthesis" | — | **retired** | removed from all frontdoor surfaces (2026-06); kept here so its retirement is on record |

## Meta / governance

| Concept | Home | Status | Operationalization / anchor |
|:---|:---|:---|:---|
| Feynman Mode | [feynman-mode.md](feynman-mode.md) | governance check | seven questions, each with a documented catch from this repo's own history; run before committing concepts/essays |

---

*Maintenance rule: new load-bearing terms enter this registry in the same change that introduces them, or they don't enter the repository. Terms whose row cannot be filled honestly (no home, no status, no anchor) are either marked narrative or removed. The registry is the audit the governance rule always implied — kept short enough to actually read.*
