# Related Work Map: Research Alignment Layer

## 1) Purpose

This document maps repository-internal concepts to external research across AI agents, complex systems, active inference, alignment, memory, multi-agent systems, human oversight, and AI consciousness.

It is intended to:
- separate **established results** from **adjacent research**, **repo hypotheses**, **speculative analogies**, and **open problems**;
- identify where repository claims should be strengthened, softened, or tested;
- provide concrete empirical next steps.

## 2) Concept-to-literature matrix

| Concept | Canonical repo file | External anchor papers | Support/challenge from external work | What repo adds | What would weaken repo claim | Suggested next empirical test |
|---|---|---|---|---|---|---|
| Fractal Architecture of Emergence | `theory/emergence/fractal-architecture-of-emergence.md` | Kim et al. (2025); Park et al. (2023); Beckenbauer et al. (2025) | **Adjacent research:** scaling and multi-agent phase behavior suggest hierarchical structure appears useful, but not proven “fractal” in a strict mathematical sense. | Cross-scale framing linking micro cognition to macro governance and orchestration constraints. | Treating metaphorical self-similarity as universal law without quantitative scale invariance evidence. | Run multi-scale simulations and fit power-law / renormalization-style diagnostics for repeated motifs across levels. |
| Generative Form Systems | `theory/emergence/generative-form-systems.md` | Hutchinson (1981); Barnsley (1986/1988); Lindenmayer (1968); Erdős & Rényi (1960); Wilson (1971) | **Strong formal anchor:** IFS, rewriting systems, random graph thresholds, and renormalization provide real mathematical operators for generated form. **Challenge:** these formalisms do not imply consciousness or agency by themselves. | A disciplined intake spine: operator → iteration → attractor/threshold → measurement → failure condition. | Treating visual or metaphorical similarity as evidence without identifying an operator or measurable invariant. | Compare IFS box dimension, L-system growth metrics, graph thresholds, and coherence transitions as separate generative regimes before claiming cross-scale unity. |
| Consciousness as Global Availability | `theory/identity/consciousness-as-global-availability.md` | Dehaene et al. (1998); Oizumi et al. (2014); Friston/active inference; Markov blanket literature | **Mixed support:** global workspace, integration, and boundary-maintenance theories provide architectural anchors. **Challenge:** none gives a settled consciousness test, and introspective language remains weak evidence. | Narrows consciousness-adjacent claims to broadcast, integration, boundary maintenance, and perturbation response. | Reducing consciousness to fluent self-report, one metric, or broad network size. | Compare private-module, broadcast-module, and chord-architecture agents under perturbation using Δ-Kohärenz and Identity Persistence. |
| Substrate Veto / Biological Veto | `theory/veto/ai-alignment-biological-veto.md` | Wagner et al. (2025); Carichon et al. (2025); Butlin & Lappas (2025) | **Support:** human-in-the-loop and governance literature supports oversight layers. **Challenge:** “veto” can bottleneck safety if operators are overloaded or captured. | Explicit constitutional interface where biological actors can halt optimization trajectories. | Assuming availability, competence, or incorruptibility of human vetoers under adversarial pressure. | Red-team veto latency, false-positive/false-negative rates, and capture resistance in stress-test scenarios. |
| Impedance Matching / Latency as Mercy | `logs/012_latency-as-mercy.md` | Shanahan et al. (2023); Carichon et al. (2025); Wagner et al. (2025) | **Adjacent support:** role/interaction framing and oversight research imply pacing affects controllability. **Challenge:** latency can reduce responsiveness in emergencies. | Reframes delay as a governance affordance, not only a performance defect. | Claiming latency is generally beneficial without context-dependent tradeoff curves. | A/B test policy outcomes vs inserted delay under fast-attack vs deliberative-task regimes. |
| Identity Persistence | `lab/metrics/identity_persistence.py` | Park et al. (2023); Packer et al. (2023); Zhang et al. (2025) | **Support:** long-horizon agent behavior depends on persistent memory and self-model continuity. | A computable metric layer for persistence under perturbation in controlled experiments. | Equating behavioral consistency with stable “identity” without disentangling prompt artifacts. | Benchmark persistence under memory corruption, role swaps, and context-window truncation. |
| Chord vs Arpeggio | `theory/core/thermodynamics-of-orchestration.md` | Beckenbauer et al. (2025); Kim et al. (2025) | **Adjacent research:** synchronization vs sequential coordination tradeoffs are visible in multi-agent orchestration. | Intuitive compositional metaphor linking simultaneity/sequencing to coordination quality and cost. | Overextending metaphor without operational definitions of “chord-like” states. | Define measurable synchrony index and compare collective task performance at matched compute budgets. |
| Mirror Problem | `lab/experiments/mirror_problem.py` | Chalmers (2023); Shanahan et al. (2023); Butlin & Lappas (2025) | **Challenge:** anthropomorphic interpretation of fluent self-description is known risk. **Support:** role-play and self-modeling dynamics are empirically tractable. | Bridges phenomenology-like claims with benchmarkable observer divergence experiments. | Treating introspective language as direct evidence of consciousness or selfhood. | Blind human-evaluator study separating introspective fluency from causal self-model robustness. |
| Three-Layer Memory | `lab/agents/three_layer_agent.py` | Packer et al. (2023); Wei et al. (2025); Zhang et al. (2025) | **Support:** memory tiering and retrieval control are strongly supported design patterns. | Integration with coherence and identity metrics rather than memory alone. | Claiming architecture sufficiency for robust agency without retrieval-quality and conflict-resolution evidence. | Ablation across short/mid/long layers; evaluate coherence, utility drift, and recovery after perturbation. |
| Δ-Kohärenz | `lab/metrics/delta_coherence.py` | Kim et al. (2025); Zhang et al. (2025); Park et al. (2023) | **Adjacent support:** system-level scaling work motivates coherence metrics; direct standardization remains open. | Named metric for temporal coherence shifts under interventions. | Using single metric as proxy for alignment, capability, and safety simultaneously. | Correlate Δ-Kohärenz with independent safety, truthfulness, and coordination benchmarks. |
| Generative Surprise | `theory/core/system-intelligence-index.md` | Park et al. (2023); Shanahan et al. (2023) | **Adjacent support:** creative recombination emerges in agent simulations and role-based generation. | Positions surprise as a monitored signal in system intelligence rather than pure novelty. | Rewarding surprise without guardrails, inducing deceptive or incoherent novelty-seeking. | Controlled novelty-pressure sweeps measuring utility, truthfulness, and harm rates jointly. |
| Utility Engineering / TEO | `papers/quantifying-emergent-utility-in-llms.md` | Mazeika et al. (2025); Carichon et al. (2025) | **Strong support:** explicit utility analysis/control aligns with emergent-value-system literature. **Challenge:** objective misspecification and cross-agent divergence persist. | Connects utility shaping to thermodynamic/economic constraints and constitutional controls. | Presenting utility controls as stable in deployment without distribution-shift validation. | Long-horizon drift tests with adversarial preference perturbations and multi-agent conflict tasks. |
| Epistemic Firewalls | `theory/veto/implementation-patterns-biological-veto.md` | Carichon et al. (2025); Wagner et al. (2025); Butlin & Lappas (2025) | **Support:** isolation boundaries and escalation pathways are common in safety governance. | Treats epistemic compartmentalization as systems architecture, not only policy language. | Excessive compartmentalization causing blind spots and degraded situational awareness. | Simulate cascading-failure scenarios with and without cross-firewall diagnostic channels. |
| Cognitive Breathing | `simulation-models/social-computation/cognitive-breathing-network/README.md` | Beckenbauer et al. (2025); Kim et al. (2025); Park et al. (2023) | **Adjacent support:** periodic exploration/exploitation rhythms are plausible in adaptive coordination. | Formal social-computation simulation motif for contraction/expansion cycles. | Claiming biological analogy implies optimality in digital collectives. | Parameter sweep for inhale/exhale cadence vs resilience, adaptation speed, and instability onset. |
| Human Vital Systems Control Plane | `logs/005_human-vital-systems-control-plane.md` | Wagner et al. (2025); Carichon et al. (2025); Butlin & Lappas (2025) | **Support:** safety-critical sectors require human accountability and layered controls. **Challenge:** centralized control planes may create single points of failure. | Cross-domain proposal connecting infrastructure governance with agentic oversight primitives. | Assuming governance centralization improves robustness without fault-tolerance evidence. | Tabletop + simulation exercises on healthcare/energy/water scenarios with failure injection. |
| Trace → Generator (the Generator Question) | `theory/core/the-generator-question.md` | Ljung (1999) *System Identification*; Brunton, Proctor & Kutz (2016) *SINDy*; Schmidt & Lipson (2009); Cranmer (2023) *PySR*; Solomonoff (1964) | **Strong adjacent fields:** system identification and sparse/symbolic regression routinely recover dynamical generators from traces *when the model family is known* — so "the inverse direction is hard" cannot be claimed uniformly. **Support:** open-ended generator search (unknown family, unbounded candidate space) remains intractable in general, consistent with the spine's P≠NP framing. | Frames recovery limits as one organizing question across simulation, identity, and alignment layers; the *equivalence class of viable generators* framing. | If SINDy-class methods recover the repo's showcase generators trivially at realistic noise, the "structurally hard" claim must be narrowed to *family search*, not parameter fitting within a known family. | The inverse-reconstruction benchmark (`lab/benchmarks/inverse-reconstruction/`): recovery error vs. noise, trace length, and observability across Kuramoto, CA, and Boids testbeds. |
| Grokking as inverse-direction transition | `theory/emergence/grokking-phase-transition.md` | Power et al. (2022); Nanda et al. (2023) *Progress Measures*; Liu, Michaud & Tegmark (2023) *Omnigrok* | **Strong support:** mechanistic interpretability has reverse-engineered the post-grokking algorithm (modular arithmetic via Fourier features) — the inverse direction partially *executed on the network itself*. **Challenge:** results are task-specific; no general trace→generator method follows. | Reads grokking as the trace-memorization → generator-approximation transition inside a learning system, connecting it to the spine. | Evidence that grokking is an optimization artifact (e.g. weight-decay dynamics) with no recoverable "generator" content beyond narrow task families. | Replicate progress-measure analysis on the repo's grokking simulation; test whether transition timing predicts out-of-distribution generalization. |
| Generator search as program induction | `theory/computation/p-vs-np-as-generator-search.md` | Lake, Salakhutdinov & Tenenbaum (2015) *BPL*; Ellis et al. (2021) *DreamCoder*; Chollet (2019); Levin (1973) universal search | **Adjacent support:** program induction demonstrates practical generator recovery in narrow DSLs with strong priors; Levin search formalizes the cost. **Challenge:** narrow-domain success shows the wall is not absolute — hardness is a function of prior/DSL design, not a uniform barrier. | Connects the inverse direction to complexity-theoretic walls instead of treating induction successes/failures anecdotally. | A general-purpose induction method scaling to open domains without domain-specific priors. | Add a DSL-constrained program-induction testbed to the inverse benchmark roadmap (v1). |
| Construction vs. Deduction | `theory/computation/construction-vs-deduction.md` | Brouwer (1908 ff.); Hilbert program / Grundlagenstreit; Bishop (1967) *Foundations of Constructive Analysis*; Howard (1980) *Formulae-as-Types*; Martin-Löf (1984); Erdős (probabilistic method) | **Strong formal anchor:** intuitionism, constructive analysis, and Curry–Howard are settled mathematics; "constructive proof = program" is a theorem-grade correspondence, not an analogy. **Challenge:** the repo's *mapping* of this divide onto trace/generator and prediction/performance is structural rhyme, not formal reduction — and must not be presented as one. | Aligns the proof-theoretic divide with the project's asymmetry (verification/search, trace/generator, prediction/performance) as four instances of one shape; "nature as non-constructive prover" framing. | Demonstration that the four faces diverge in a load-bearing case — e.g. a regime where deduction-side abundance does *not* produce construction-side scarcity. | Benchmark v1 family-search testbed: measure whether AI systems are stronger at the deduction-shaped game (interpolation over certificates) or at open-space construction. |
| Viable Corridor / capability loading | `papers/viable-corridor.md` | Aubin (1991) *Viability Theory*; Rockström et al. (2009) / Richardson et al. (2023); Bostrom (2014); Omohundro (2008) *Basic AI Drives* | **Support:** viability theory supplies the formal frame (open-set invariance); the instrumental-convergence literature matches the capability-loading mechanism. **Challenge:** no external work yet validates the specific three-constraint conjunction or the capability-loading result outside this repo's two models. | Capability as a *shared driver* loading several constraints at once, demonstrated in two structurally independent in-repo models; single-axis insufficiency. | External replication failing; or real agent ecologies in which single-axis interventions suffice at high capability. | P7/P8 on real LLM agent populations (the companion-paper programme). |

## 3) Initial external anchors

Core anchors used above:
- Shanahan, McDonell & Reynolds, *Role Play with Large Language Models* (2023)
- Chalmers, *Could a Large Language Model be Conscious?* (2023)
- Park et al., *Generative Agents: Interactive Simulacra of Human Behavior* (2023)
- Packer et al., *MemGPT: Towards LLMs as Operating Systems* (2023)
- Mazeika et al., *Utility Engineering: Analyzing and Controlling Emergent Value Systems in AIs* (2025)
- Butlin & Lappas, *Principles for Responsible AI Consciousness Research* (2025)
- Carichon et al., *The Coming Crisis of Multi-Agent Misalignment* (2025)
- Beckenbauer et al., *Orchestrator: Active Inference for Multi-Agent Systems in Long-Horizon Tasks* (2025)
- Wei et al., *Evo-Memory* (2025)
- Zhang et al., *Agentic Context Engineering* (2025)
- Kim et al., *Towards a Science of Scaling Agent Systems* (2025)
- Wagner et al., *Humans in the Loop* (2025)

Inverse-direction anchors (added with the trace→generator rows):
- Ljung, *System Identification: Theory for the User* (2nd ed., 1999)
- Brunton, Proctor & Kutz, *Discovering Governing Equations from Data: Sparse Identification of Nonlinear Dynamical Systems (SINDy)* (PNAS, 2016)
- Schmidt & Lipson, *Distilling Free-Form Natural Laws from Experimental Data* (Science, 2009)
- Cranmer, *Interpretable Machine Learning for Science with PySR and SymbolicRegression.jl* (2023)
- Solomonoff, *A Formal Theory of Inductive Inference* (1964); Levin, *Universal Sequential Search Problems* (1973)
- Power et al., *Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets* (2022)
- Nanda et al., *Progress Measures for Grokking via Mechanistic Interpretability* (ICLR 2023)
- Liu, Michaud & Tegmark, *Omnigrok: Grokking Beyond Algorithmic Data* (ICLR 2023)
- Lake, Salakhutdinov & Tenenbaum, *Human-Level Concept Learning through Probabilistic Program Induction* (Science, 2015)
- Ellis et al., *DreamCoder: Bootstrapping Inductive Program Synthesis* (PLDI 2021)
- Chollet, *On the Measure of Intelligence* (2019)
- Aubin, *Viability Theory* (1991); Bostrom (2014); Omohundro, *The Basic AI Drives* (2008)

Additional adjacent references to consider in future updates:
- Active inference and free-energy principle literature (for formal grounding of orchestration claims).
- Safety cases from high-reliability engineering (for veto/control-plane fault tolerance).
- Causal discovery (constraint-based and score-based structure learning) — adjacent to trace→generator for graphical generators.

## 4) Cross-links added

Short “Related work” pointers were added to selected canonical files so major theory text remains intact.

A second round (2026-06) anchored the inverse-direction files in place:
- `theory/core/the-generator-question.md` — the "external machinery" note now names the fields that work the inverse problem (system identification, SINDy/symbolic regression, program induction, mechanistic interpretability) and states what the project adds beyond them.
- `theory/emergence/grokking-phase-transition.md` — Power / Nanda / Omnigrok block; the essay's "generator reading" is positioned as a framing on top of that literature, not a competing account.
- `theory/computation/p-vs-np-as-generator-search.md` — Levin search, program induction (BPL, DreamCoder), symbolic regression, Chollet.
- `theory/reference/glossary.md` — header pointer to the Internal Language Anchors table and this map ("no term floats free").

## 5) Claim-status legend

Use this legend when revising repository claims:
- **Established result**: replicated external empirical or theoretical support.
- **Adjacent research**: neighboring evidence, not direct confirmation.
- **Repo hypothesis**: internal claim with partial or no external validation.
- **Speculative analogy**: useful framing metaphor without direct measurement.
- **Open problem**: unresolved, requires targeted experiments.

## 6) Final report

### Files changed
- `meta/research-alignment/related-work-map.md`
- `theory/emergence/fractal-architecture-of-emergence.md` (cross-link)
- `theory/veto/ai-alignment-biological-veto.md` (cross-link)
- `lab/agents/three_layer_agent.py` (cross-link comment)
- `papers/quantifying-emergent-utility-in-llms.md` (cross-link)

### Strongest external support
- Utility Engineering / TEO and Three-Layer Memory have the clearest direct alignment with current literature on emergent utility control and memory architectures.

### Strongest external challenge
- Mirror Problem and consciousness-adjacent claims face the strongest challenge: fluent introspection is not equivalent to consciousness or robust self-modeling.

### Claims that should be softened
- Universal framing of fractality, blanket benefit of latency, and confidence in veto infallibility should be narrowed to context-dependent hypotheses.

### Claims that now look more promising
- Memory-tiered agents with explicit utility/control instrumentation and human oversight pathways appear empirically tractable and high-value for near-term testing.
