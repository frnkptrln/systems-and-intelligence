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

Additional adjacent references to consider in future updates:
- Active inference and free-energy principle literature (for formal grounding of orchestration claims).
- Safety cases from high-reliability engineering (for veto/control-plane fault tolerance).

## 4) Cross-links added

Short “Related work” pointers were added to selected canonical files so major theory text remains intact.

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
