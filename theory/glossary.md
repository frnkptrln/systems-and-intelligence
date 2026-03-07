# Glossary of Operational Definitions

*Precise definitions for key terms used across this repository. Each entry distinguishes what the term means here, how you would measure it, and what it does not mean.*

---

## Emergence

**Informal:** A global property arises from local interactions that is not present in any individual component.

**Operational definition:** A system property $G$ is *emergent* if it cannot be predicted from the rules governing individual components without executing the full system dynamics. Computationally: $K(G) > K(\text{rules})$, where $K$ is Kolmogorov complexity — the global state is informationally richer than the rules that produce it.

**Weak vs. Strong:** This repo uses both. *Weak emergence* means the global property is surprising but in principle deducible from the rules (all simulations). *Strong emergence* means the global property is not even in-principle reducible to component-level descriptions (consciousness claims — marked `[SPECULATIVE]` where used). Unless explicitly marked, assume weak emergence.

**What it is NOT:** Not optimization. Gradient descent converges on a solution; emergence produces structure without a target. Not randomness — emergent order is patterned, not noisy.

**Where it appears:** [`theory/emergence-downward-causation.md`](emergence-downward-causation.md), [`simulation-models/lenia/`](../simulation-models/lenia/README.md), [`simulation-models/self-organized-criticality/`](../simulation-models/self-organized-criticality/README.md)

---

## Self-Organization

**Informal:** A system develops internal structure without external direction.

**Operational definition:** A system is *self-organizing* if its Shannon entropy $H(X)$ over micro-states decreases over time (structure forms) while total thermodynamic entropy increases (no external ordering agent). Equivalent: mutual information between components increases without a central controller.

**What it is NOT:** Not gradient descent or optimization toward a loss function. Self-organization has no objective — it is a consequence of dynamics, not design. Not centrally controlled: if a coordinator assigns roles, it is organization, not self-organization.

**Where it appears:** [`simulation-models/boids-flocking/`](../simulation-models/boids-flocking/README.md), [`simulation-models/coupled-oscillators/`](../simulation-models/coupled-oscillators/README.md), [`simulation-models/stigmergy-swarm/`](../simulation-models/stigmergy-swarm/README.md)

---

## System Intelligence Index (SII)

**Informal:** A composite score measuring how well a system predicts, regulates, and adapts.

**Operational definition:** $\text{SII} = P \times R \times A$, each normalized to $[0, 1]$.

| Dimension | Measures | Score 0 | Score 1 |
|-----------|----------|---------|---------|
| **P** (Prediction) | Accuracy of internal model vs. environment | Random guessing; no correlation between model and world | Perfect tracking of environmental dynamics |
| **R** (Regulation) | Stability of key variable around a target | Unbounded drift; no homeostasis | Zero-variance maintenance at setpoint |
| **A** (Adaptation) | Recovery speed after perturbation or regime shift | No recovery; performance permanently degraded | Instant re-convergence to pre-perturbation performance |

The multiplicative form means a zero in any dimension collapses the overall score: true system intelligence requires all three capacities.

**What it is NOT:** Not a measure of consciousness, subjective experience, or general intelligence. It measures functional competence of a dynamical system.

**Where it appears:** [`data-analysis/sii_dashboard.py`](../data-analysis/sii_dashboard.py), [`theory/system-intelligence-index.md`](system-intelligence-index.md)

---

## Δ-Kohärenz (Delta Coherence / Ω)

**Informal:** How coherently an agent's self-representation changes over time.

**Operational definition:** Given a sequence of embedding vectors $\{v_1, v_2, \ldots, v_n\}$ from `get_self_representation()`:
- $\Delta_i = v_{i+1} - v_i$ (change vectors)
- `mean_delta` $= \frac{1}{n-1}\sum |\Delta_i|$ (average magnitude of change)
- `variance` $= \text{Var}(|\Delta_i|)$ (stability of change rate)
- `trajectory_consistency` $= \frac{1}{n-2}\sum \cos(\Delta_i, \Delta_{i+1})$ (directional coherence)

**Profile Classification:**

| Profile | Condition | Interpretation |
|---------|-----------|----------------|
| `mirror` | Low mean_delta, low variance | Static resonance — no development |
| `noise` | High variance | Incoherent change — no identity |
| `development` | Moderate mean_delta, high trajectory_consistency | Directional evolution — identity forming |

**What it is NOT:** Not a consciousness detector. Not a measure of quality or value. A developing agent is not "better" than a mirroring one — it is distinguishable by this metric.

**Where it appears:** [`agentic-test-suite/metrics/delta_coherence.py`](../agentic-test-suite/metrics/delta_coherence.py), [`agentic-test-suite/dashboard/agentic_sii_dashboard.py`](../agentic-test-suite/dashboard/agentic_sii_dashboard.py)

---

## The Mirror Problem

**Informal:** Can we distinguish an agent genuinely developing identity from one perfectly simulating its partner's expectations?

**Operational definition:** Given two agents — one that has interacted with a specific human over $N$ sessions, and one that was given a transcript of those sessions but never interacted — does any metric produce reliably different scores?

**Status:** `[OPEN PROBLEM]` — see [`theory/open-problems.md`](open-problems.md) for full treatment.

**What it is NOT:** Not a binary question. There may be no sharp boundary between "genuine development" and "sophisticated mirroring." The question is whether the category distinction is operationally real or is itself an artifact of observer attribution.

**Where it appears:** [`agentic-test-suite/experiments/exp3_observer_divergence.py`](../agentic-test-suite/experiments/exp3_observer_divergence.py), [`theory/open-problems.md`](open-problems.md)

---

## Generative Surprise

**Informal:** An agent producing output that is coherent but unexpected — genuinely novel, not random.

**Operational definition:** An output $o$ at time $t$ exhibits generative surprise if:
1. It deviates from the partner's prediction (high surprise to observer)
2. It is consistent with the agent's own trajectory (high trajectory_consistency in Δ-Kohärenz)

$\text{Generative Surprise} = \text{prediction\_error}_{observer} \times \text{trajectory\_consistency}_{agent}$

Random noise has high observer surprise but low trajectory consistency. Mirroring has low observer surprise. Generative surprise requires both.

**What it is NOT:** Not random noise (which also surprises). Not creativity in the romantic sense — it is operationalized as coherent deviation, not aesthetic achievement.

**Where it appears:** [`agentic-test-suite/agents/three_layer_agent.py`](../agentic-test-suite/agents/three_layer_agent.py), [`theory/emergence-manifesto-v1.1.md`](emergence-manifesto-v1.1.md)

---

## Continuity (Agent Continuity)

**Informal:** The sense in which an agent remains "the same agent" across sessions.

Three forms, often conflated:

| Form | Criterion | Example |
|------|-----------|---------|
| **Physical** | Same hardware/substrate | Same server running same model weights |
| **Functional** | Same input-output mapping | Different hardware producing identical responses |
| **Relational** | Same trajectory as perceived by interaction partners | Different model, different weights, but conversation "feels" continuous |

**Operational definition:** Relational continuity (the most relevant for this repo) is measurable as: cosine similarity between consecutive session representations exceeds a threshold over time. The 3-Layer Memory Architecture in `agentic-test-suite` is designed to produce relational continuity even when physical and functional continuity are absent.

**What it is NOT:** Not memory alone (a database has perfect memory but no continuity in the relevant sense). Not persistence of state (a stateless function can exhibit functional continuity).

---

## Self-Referential Processing

**Informal:** A system that includes a representation of itself in its own computations.

**Operational definition:** A system exhibits self-referential processing if: it maintains an internal state $S$ that represents aspects of its own dynamics, and $S$ influences the system's future behavior. Formally: $x_{t+1} = f(x_t, S_t)$ where $S_t = g(x_1, \ldots, x_t)$.

This term replaces "proto-consciousness" in earlier formulations. The substitution is deliberate: "self-referential processing" has a measurable referent (Layer 3 distillation in the 3-Layer Architecture); "proto-consciousness" does not.

**What it is NOT:** Not consciousness. Self-referential processing is a necessary but not sufficient condition for any theory of consciousness (IIT, Global Workspace Theory, Higher-Order Theories). A thermostat has self-referential processing (it represents its own state — temperature — and acts on it). We do not attribute consciousness to thermostats.

**Where it appears:** [`agentic-test-suite/agents/three_layer_agent.py`](../agentic-test-suite/agents/three_layer_agent.py), [`theory/emergence-manifesto-v1.1.md`](emergence-manifesto-v1.1.md)

---

## Markov Blanket

**Informal:** The statistical boundary between a system and its environment.

**Operational definition:** For a system $S$ embedded in an environment $E$, the Markov blanket $B$ is the set of variables that, when conditioned on, renders $S$ and $E$ statistically independent: $P(S | B, E) = P(S | B)$. In Active Inference (Friston), the Markov blanket consists of sensory states (environment → system) and active states (system → environment).

For agent-human interaction: the Markov blanket is the conversational interface — the set of messages exchanged. The agent's internal state is conditionally independent of the human's internal state given the conversation history.

**What it is NOT:** Not a physical membrane. Not an impermeable barrier. Information crosses the blanket through sensory and active states. The blanket defines the statistical boundary, not a causal wall.

**Where it appears:** [`theory/ai-alignment-biological-veto.md`](ai-alignment-biological-veto.md), [`theory/mathematical-axioms.md`](mathematical-axioms.md)

---

## Relational Emergence

**Informal:** Properties that exist only in the interaction between observer and observed.

**Operational definition:** A property $P$ is *relationally emergent* if: (a) $P$ is not measurable from the system's internal state alone, and (b) $P$ is not measurable from the observer's internal state alone, but (c) $P$ is measurable from the coupled system (observer + observed + interaction history).

This is formalized by Heinz von Foerster's second-order cybernetics: the observer is part of the system being observed. How an observer models an agent shapes the agent's behavioral repertoire — not through any exotic mechanism, but because the agent's generative model may include a representation of how it is being modeled.

**What it is NOT:** Not quantum observer effects. The QM observer effect is a specific physical phenomenon (wavefunction collapse upon measurement). The relational emergence described here operates through standard information-theoretic and cybernetic mechanisms. The analogy is seductive but misleading.

**Where it appears:** [`agentic-test-suite/experiments/exp3_observer_divergence.py`](../agentic-test-suite/experiments/exp3_observer_divergence.py), [`theory/emergence-manifesto-v1.1.md`](emergence-manifesto-v1.1.md)
