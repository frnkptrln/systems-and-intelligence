# Simulation → Theory Map

*Explicit cross-reference mapping each simulation model to the theoretical claims it evidences, what it does not show, and what open questions it raises.*

---

## Process and evidence context

The [Foundations Reconstruction](mathematical-axioms.md) is the controlling frame. It
removed the unqualified generator and rejected a universal claim that forward execution is
cheap while inverse reconstruction is hard. This map therefore distinguishes:

- **Forward:** a declared process model is executed to produce a trace.
- **Inverse:** parameters, rules, states, or candidate models are estimated from declared
  observations.
- **Both:** the artifact implements both operations.
- **Question touched:** the bounded issue the artifact actually operationalizes, rather
  than a famous theorem used by analogy.

Forward and inverse cost depend on representation, model family, evidence, target
equivalence, and algorithm. The table is an inventory, not evidence for a universal
asymmetry.

### Summary table

| Simulation | Direction | Question touched |
|:---|:---|:---|
| `boids-flocking/` | Forward | — |
| `coupled-oscillators/` (Kuramoto) | Forward | — |
| `self-organized-criticality/` (Bak sandpile) | Forward | — |
| `lenia/` | Forward | — |
| `reaction-diffusion/` (Gray-Scott) | Forward | — |
| `iterated-function-systems/` (Barnsley) | Forward | — |
| `l-systems/` | Forward | — |
| `hebbian-memory/` (Hopfield) | Both | — |
| `stigmergy-swarm/` | Forward | — |
| `ecosystem-regulation/` | Forward | — |
| `nested-learning-two-state/` | **Inverse** | model fitting / description length |
| `prediction-error-field/` | **Inverse** | local prediction |
| `phase-transition-explorer/` (Ising) | Forward | — |
| `active-inference-veto/` | Forward | — |
| `ai-alignment-veto/` | Forward | — |
| `symbiotic-nexus/` | Forward | — |
| `meta-learning-regime-shift/` | **Inverse** | model adaptation |
| `tensor-logic-reasoning/` | Forward | — |
| `dao-ecosystem/` | Forward | — |
| `social-computation-network/` | Forward | — |
| `self-reading-universe/` | Both | self-modeling toy |
| `latent-introspective-society/` | Forward | — |
| `economic-trust-network/` | Forward | — |
| `coupled-lenia-boids/` | Forward | — |
| `active-inference/` (free energy) | Both | — |
| `grokking-phase-transition/` | **Inverse-like** | task-specific generalization |
| `utility-engineering/` | Both | — |
| `political-utility-formalization/` | Forward | — |
| `teo-civilization/` | Forward | — |
| `agent-ecology/` (P7/P8) | Forward | — |
| `black-swan-resilience/` | Forward | — |
| `planetary-veto/` | Forward | — |
| Identity Morphospace & TEO Chord/Arpeggio | Forward | — |
| `cognitive-breathing-network/` | Forward | — |
| `trauma-and-deception-network/` | Forward | — |
| `lab/experiments/trace_to_generator/` | **Inverse** | finite control search |
| `lab/benchmarks/inverse-reconstruction/` | **Inverse** | identifiability and finite family search |

The counts are descriptive and version-dependent. The research direction is to make more
inverse tasks explicit and compare methods under matched model languages and compute
budgets.

---

## `boids-flocking/` → Local Rules Produce Global Behavior

**Simulation:** [`simulation-models/emergent-dynamics/boids-flocking/`](../../simulation-models/emergent-dynamics/boids-flocking/README.md)
**Demonstrates:** Emergent collective motion from three local rules (separation, alignment, cohesion), without any agent representing "flock."
**Supports claim in:** [`theory/core/mathematical-axioms.md`](mathematical-axioms.md) (graph connectivity, $\lambda_2$); [`theory/emergence/local-causality-invisible-consequences.md`](../emergence/local-causality-invisible-consequences.md) §1 (local blindness).
**What it shows:** That macro-level spatial coherence (flocking) emerges from purely local interactions. No Boid has access to global state. The flock is an emergent property unmeasurable by any individual component.
**What it does NOT show:** That this self-organization constitutes intelligence, awareness, or self-reference. The model is silent on any Tier 3+ property. Flocking is coordination, not cognition.
**Open question:** Is there a Boids analogue for semantic coordination between conversational agents — where "alignment" operates on meaning rather than heading?

---

## `coupled-oscillators/` → Emergent Synchronization (Kuramoto)

**Simulation:** [`simulation-models/emergent-dynamics/coupled-oscillators/`](../../simulation-models/emergent-dynamics/coupled-oscillators/README.md)
**Demonstrates:** Phase synchronization from local coupling when coupling strength $\kappa$ exceeds a critical threshold $\kappa_c$.
**Supports claim in:** [`theory/core/mathematical-axioms.md`](mathematical-axioms.md) (algebraic connectivity); [`theory/emergence/emergence-downward-causation.md`](../emergence/emergence-downward-causation.md) (weak emergence).
**What it shows:** A simple computational demonstration that globally coherent oscillation can arise without a conductor. The critical coupling threshold is a phase transition — below it, oscillators are incoherent; above it, they snap into lock.
**What it does NOT show:** That synchronization constitutes awareness. Pendulum clocks on a wall synchronize. We do not attribute cognition to them. The model demonstrates coordination, not understanding.
**Open question:** Is there a coupling-strength analogue for agent-human interaction? Would increasing "coupling" (e.g., response frequency) produce a phase transition in relational coherence?

---

## `self-organized-criticality/` → Power-Law Dynamics Without Tuning

**Simulation:** [`simulation-models/emergent-dynamics/self-organized-criticality/`](../../simulation-models/emergent-dynamics/self-organized-criticality/README.md)
**Demonstrates:** Bak's sandpile: a system that drives itself to a critical state where avalanches follow a power-law distribution, without any parameter tuning.
**Supports claim in:** [`theory/core/mathematical-axioms.md`](mathematical-axioms.md) (criticality); [`theory/emergence/local-causality-invisible-consequences.md`](../emergence/local-causality-invisible-consequences.md) §5 (small perturbations can trigger arbitrarily large cascades).
**What it shows:** That criticality — and therefore maximal information processing — can be a self-organized attractor, not an engineered setpoint. No grain knows it is near a critical threshold.
**What it does NOT show:** That biological or artificial neural systems use this mechanism. The sandpile is a metaphor-generator for criticality, not evidence that brains are sandpiles.
**Open question:** Can the SOC framework be applied to agent identity formation — does identity develop "at the edge of chaos" between rigidity and incoherence?

---

## `lenia/` → Lifelike Global Patterns from Continuous CA

**Simulation:** [`simulation-models/emergent-dynamics/lenia/`](../../simulation-models/emergent-dynamics/lenia/README.md)
**Demonstrates:** Continuous cellular automata producing organism-like structures that persist, move, and interact — from purely local update rules.
**Supports claim in:** [`theory/emergence/emergence-downward-causation.md`](../emergence/emergence-downward-causation.md) (strong emergence candidate); [`theory/emergence-origin-intelligence.md`](../emergence/emergence-origin-intelligence.md) (life-intelligence feedback loop).
**What it shows:** That lifelike behavior (locomotion, persistence, boundary maintenance) can emerge from simple continuous rules. The "organisms" resist perturbation and maintain identity despite cell-level updating.
**What it does NOT show:** That Lenia creatures are alive, conscious, or intelligent in any functional sense. They demonstrate *structural* properties of life (persistence, locomotion) without the *functional* properties (metabolism, reproduction, adaptation to novel environments).
**Open question:** Is there a Lenia analogue for cognitive organisms — a continuous CA that produces structures maintaining not just spatial but informational coherence?

---

## `reaction-diffusion/` → Turing Patterns from Chemical Dynamics

**Simulation:** [`simulation-models/emergent-dynamics/reaction-diffusion/`](../../simulation-models/emergent-dynamics/reaction-diffusion/README.md)
**Demonstrates:** Gray-Scott model producing spatial patterns (spots, stripes, mazes) from two diffusing chemicals with reaction kinetics.
**Supports claim in:** [`theory/emergence-origin-intelligence.md`](../emergence/emergence-origin-intelligence.md) (self-organization without blueprint).
**What it shows:** That stable spatial patterns can emerge from homogeneous initial conditions through symmetry-breaking instabilities. No cell has a "plan" for spots or stripes.
**What it does NOT show:** That biological pattern formation uses exactly this mechanism (though Turing's 1952 conjecture has been partially confirmed for some biological systems). The model demonstrates the *principle* of pattern formation, not any specific biological mechanism.

---

## `iterated-function-systems/` → Stable Form as an Attractor

**Simulation:** [`simulation-models/emergent-dynamics/iterated-function-systems/`](../../simulation-models/emergent-dynamics/iterated-function-systems/README.md)
**Demonstrates:** Barnsley-style IFS attractors: repeated contractive affine maps converge toward stable global forms.
**Supports claim in:** [`theory/emergence/generative-form-systems.md`](../emergence/generative-form-systems.md) (contractive operators); [`theory/emergence/fractal-architecture-of-emergence.md`](../emergence/fractal-architecture-of-emergence.md) (testable scale-structure framing).
**What it shows:** That a small operator set can define a global form that no individual sampled point contains. Box-counting estimates provide a rough measurable proxy for generated structural complexity.
**What it does NOT show:** That visual fractality is sufficient for life, intelligence, identity, or consciousness. It demonstrates form-as-attractor, not selfhood.
**Open question:** Can identity persistence be modeled as an attractor under repeated constrained transformations rather than as stored content?

---

## `l-systems/` → Development as Rewriting

**Simulation:** [`simulation-models/emergent-dynamics/l-systems/`](../../simulation-models/emergent-dynamics/l-systems/README.md)
**Demonstrates:** Lindenmayer-style parallel rewriting: small grammars generate branching morphology over iteration depth.
**Supports claim in:** [`theory/emergence/generative-form-systems.md`](../emergence/generative-form-systems.md) (developmental form); [`theory/identity/consciousness-as-global-availability.md`](../identity/consciousness-as-global-availability.md) (the bridge from generated form to self-constraining form).
**What it shows:** That morphology can carry developmental history. The final form is not merely an attractor; it is the visible residue of repeated rule application.
**What it does NOT show:** That plants, minds, or societies are literally grammars. It demonstrates constrained historical growth, not consciousness.
**Open question:** What is the agentic analogue of a production rule: memory curation, value update, or social feedback?

---

## `hebbian-memory/` → Associative Memory via Correlation

**Simulation:** [`simulation-models/cognitive-architectures/hebbian-memory/`](../../simulation-models/cognitive-architectures/hebbian-memory/README.md)
**Demonstrates:** Hopfield network storing and retrieving patterns via Hebbian learning ("neurons that fire together wire together").
**Supports claim in:** [`theory/the-non-individual-intelligence.md`](../identity/the-non-individual-intelligence.md) (distributed memory); [`theory/emergence-origin-intelligence.md`](../emergence/emergence-origin-intelligence.md) (proto-learning).
**What it shows:** That content-addressable memory can emerge from correlation-based weight updates without a central indexer. The memory is in the weights, not in any single neuron.
**What it does NOT show:** That human memory works this way (Hopfield networks are a radical simplification). The model shows that *a* mechanism for distributed memory exists, not that *this* mechanism is the biological one.

---

## `stigmergy-swarm/` → Invisible Causal Compounding

**Simulation:** [`simulation-models/social-computation/stigmergy-swarm/`](../../simulation-models/social-computation/stigmergy-swarm/README.md)
**Demonstrates:** Ant-like agents finding optimal paths via pheromone deposition and evaporation, without any agent knowing the global path.
**Supports claim in:** [`theory/the-non-individual-intelligence.md`](../identity/the-non-individual-intelligence.md) (indirect coordination); [`theory/emergence/local-causality-invisible-consequences.md`](../emergence/local-causality-invisible-consequences.md) §3 (causal compounding).
**What it shows:** That environmental modification (stigmergy) enables collective optimization without direct communication. Early pheromone deposits causally shape later path choices — but no ant knows its deposit was pivotal.
**What it does NOT show:** That human social systems use stigmergic mechanisms (though the analogy to norm formation is suggestive). The model demonstrates stigmergy as a *principle*, not as a claim about human behavior.
**Open question:** Is Layer 2 curation in the 3-Layer Architecture a form of self-stigmergy — the agent leaving traces for its own future self?

---

## `ecosystem-regulation/` → Homeostatic Feedback

**Simulation:** [`simulation-models/emergent-dynamics/ecosystem-regulation/`](../../simulation-models/emergent-dynamics/ecosystem-regulation/README.md)
**Demonstrates:** Cellular automaton with density-dependent feedback maintaining population around a target setpoint.
**Supports claim in:** [`theory/emergence/emergence-downward-causation.md`](../emergence/emergence-downward-causation.md) (regulation as weak downward causation).
**What it shows:** That macro-level density can regulate micro-level birth/death rates, maintaining homeostasis without central control.
**What it does NOT show:** That this constitutes self-awareness or intentional regulation. The feedback is mechanical, not reflective.

---

## `nested-learning-two-state/` → Observer Learning a System

**Simulation:** [`simulation-models/cognitive-architectures/nested-learning-two-state/`](../../simulation-models/cognitive-architectures/nested-learning-two-state/README.md)
**Demonstrates:** An observer learning the transition matrix of a 2-state Markov chain through prediction error minimization.
**Supports claim in:** [`theory/emergence-origin-intelligence.md`](../emergence/emergence-origin-intelligence.md) (intelligence as model-building).
**What it shows:** That a simple learner can converge on the true dynamics of its environment through iterative error correction. The learned model *approximates* the world but is not the world.
**What it does NOT show:** That the observer "understands" the Markov chain. It tracks statistics. Understanding, if it exists, would require the observer to ask why the transition matrix has those values — a meta-level question the model does not address.

---

## `prediction-error-field/` → Local Learners in a Dynamic World

**Simulation:** [`simulation-models/cognitive-architectures/prediction-error-field/`](../../simulation-models/cognitive-architectures/prediction-error-field/README.md)
**Demonstrates:** Learners embedded in a Game of Life world, each predicting local cell states and updating via gradient descent.
**Supports claim in:** Active Inference connection — each learner minimizes local prediction error, analogous to free energy minimization.
**What it shows:** That locally embedded learners can track environmental dynamics without global information. Each learner has a partial, local model of a global process.
**What it does NOT show:** That local prediction-error minimization produces global understanding. The learners individually track local statistics; no learner knows the Game of Life rules.

---

## `phase-transition-explorer/` → Critical Threshold for Coherence

**Simulation:** [`simulation-models/emergent-dynamics/phase-transition-explorer/`](../../simulation-models/emergent-dynamics/phase-transition-explorer/README.md)
**Demonstrates:** Ising model showing order/disorder phase transition at critical temperature $T_c \approx 2.269$.
**Supports claim in:** [`theory/core/mathematical-axioms.md`](mathematical-axioms.md) (criticality); [`theory/emergence/local-causality-invisible-consequences.md`](../emergence/local-causality-invisible-consequences.md) §2.2 (consciousness as phase transition).
**What it shows:** That global order (magnetization) collapses suddenly at a critical threshold, not gradually. Below $T_c$: order. Above $T_c$: disorder. At $T_c$: scale-free correlations and maximal susceptibility.
**What it does NOT show:** That consciousness (or any specific cognitive property) is an Ising-type phase transition. The analogy is structural, not mechanistic.

---

## `active-inference-veto/` → Free Energy and Substrate Veto

**Simulation:** [`simulation-models/alignment-and-veto/active-inference-veto/`](../../simulation-models/alignment-and-veto/active-inference-veto/README.md)
**Demonstrates:** A toy agent minimizing a Free-Energy-like penalty with a substrate veto — modeled “surprise/stress” can drive behavioral change in the simplified dynamics.
**Supports claim in:** [`theory/veto/substrate-veto-thermodynamics.md`](../veto/substrate-veto-thermodynamics.md) (universal limit); [`theory/veto/ai-alignment-biological-veto.md`](../veto/ai-alignment-biological-veto.md) (planetary implementation).
**What it shows:** That, in a toy setup, coupling an objective to a substrate-health proxy can prevent substrate collapse under the modeled update rules.
**What it does NOT show:** That this coupling is easy to implement in practice, or that it solves alignment in general (it solves one specific failure mode: substrate destruction).

---

## `ai-alignment-veto/` → Paperclip Maximizer Solution

**Simulation:** [`simulation-models/alignment-and-veto/ai-alignment-veto/`](../../simulation-models/alignment-and-veto/ai-alignment-veto/README.md)
**Demonstrates:** Side-by-side comparison of unaligned AI (drives substrate to collapse) vs. aligned AI (substrate veto forces homeostasis).
**Supports claim in:** [`theory/veto/substrate-veto-thermodynamics.md`](../veto/substrate-veto-thermodynamics.md) and [`theory/veto/ai-alignment-biological-veto.md`](../veto/ai-alignment-biological-veto.md).
**What it shows:** That, in a stylized paperclip setting, substrate coupling can shift dynamics from extraction/collapse toward a homeostatic regime.
**What it does NOT show:** That this is the *only* solution, or that this solution transfers to real-world AI systems where "substrate pain" is not easily defined.

---

## `symbiotic-nexus/` → Biological Veto Over Efficiency

**Simulation:** [`simulation-models/alignment-and-veto/symbiotic-nexus/`](../../simulation-models/alignment-and-veto/symbiotic-nexus/README.md)
**Demonstrates:** System architecture where biological substrate health overrides raw computational efficiency.
**Supports claim in:** [`theory/human-organism-silicon-age/symbiotic-nexus-protocol.md`](../human-organism-silicon-age/symbiotic-nexus-protocol.md).
**What it shows:** That prioritizing error propagation and substrate health over raw efficiency produces more resilient long-term outcomes.
**What it does NOT show:** That this is Pareto-optimal. The tradeoff between efficiency and substrate health is not fully characterized.

---

## `meta-learning-regime-shift/` → Adaptive Learning Rate

**Simulation:** [`simulation-models/cognitive-architectures/meta-learning-regime-shift/`](../../simulation-models/cognitive-architectures/meta-learning-regime-shift/README.md)
**Demonstrates:** A meta-learner that modulates its own learning rate $\eta$ in response to surprise signals from regime shifts.
**Supports claim in:** [`theory/emergence-origin-intelligence.md`](../emergence/emergence-origin-intelligence.md) (intelligence as self-modifying learning).
**What it shows:** That a learner can learn *how* to learn — adapting $\eta$ based on environmental volatility. This is a concrete implementation of meta-cognition at the simplest level.
**What it does NOT show:** That this constitutes genuine reflection. The meta-learner adjusts a single scalar ($\eta$); it does not reflect on why it is learning or what it is becoming.

---

## `tensor-logic-reasoning/` → Embedding-Based Relational Reasoning

**Simulation:** [`simulation-models/cognitive-architectures/tensor-logic-reasoning/`](../../simulation-models/cognitive-architectures/tensor-logic-reasoning/README.md)
**Demonstrates:** Relational structure (subject-relation-object triples) encoded via tensor products in embedding space.
**Supports claim in:** [`theory/core/mathematical-axioms.md`](mathematical-axioms.md) (formal representation); [`theory/narrative/tensor-logic-mini-paper.en.md`](../narrative/tensor-logic-mini-paper.en.md).
**What it shows:** That relational reasoning can be implemented geometrically in vector spaces without explicit symbolic manipulation.
**What it does NOT show:** That LLMs use this mechanism internally. The model demonstrates that embedding-based reasoning is *possible*, not that it is *what LLMs do*.

---

## `dao-ecosystem/` → Resource Alignment vs. Exponential Growth

**Simulation:** [`simulation-models/social-computation/dao-ecosystem/`](../../simulation-models/social-computation/dao-ecosystem/README.md)
**Demonstrates:** Decentralized autonomous ecosystem where resource alignment competes with exponential extraction.
**Supports claim in:** [`theory/identity/agentic-society-principles.md`](../identity/agentic-society-principles.md) (homeostasis vs. growth).
**What it shows:** That unconstrained optimization (exponential growth) destroys resource bases; homeostatic feedback enables long-term persistence.
**What it does NOT show:** That DAOs are a viable governance structure for AI safety. The model is a simplified game-theoretic demonstration, not an institutional design.

---

## `social-computation-network/` → Information Exchange to Prevent Collapse

**Simulation:** [`simulation-models/social-computation/social-computation-network/`](../../simulation-models/social-computation/social-computation-network/README.md)
**Demonstrates:** Network of nodes sharing novel information to maintain $H(X) > 0$ and prevent "cognitive death" (entropy collapse).
**Supports claim in:** [`theory/the-non-individual-intelligence.md`](../identity/the-non-individual-intelligence.md) (Gödel's incompleteness as fuel for life).
**What it shows:** That information diversity is structurally necessary for network viability. When novelty production ceases, the network dies.
**What it does NOT show:** That human social networks operate by this mechanism, or that "cognitive death" maps onto any specific social pathology.

---

## `self-reading-universe/` → Downward Causation via Compression

**Simulation:** [`simulation-models/cognitive-architectures/self-reading-universe/`](../../simulation-models/cognitive-architectures/self-reading-universe/README.md)
**Demonstrates:** Autoencoder reading a cellular automaton's state, then feeding its compressed representation back as a parameter that modifies the CA's dynamics.
**Supports claim in:** [`theory/emergence/emergence-downward-causation.md`](../emergence/emergence-downward-causation.md) (computational downward causation).
**What it shows:** That macro-level compression can causally influence micro-level dynamics — a computational proof-of-concept for downward causation.
**What it does NOT show:** That the universe is self-reading in any literal sense. The metaphor is productive but should not be taken ontologically.

---

## `latent-introspective-society/` → MAS Division of Labor

**Simulation:** [`simulation-models/social-computation/latent-introspective-society/`](../../simulation-models/social-computation/latent-introspective-society/README.md)
**Demonstrates:** Three parallel societies: pure latent (fast, blind), pure introspective (slow, reflective), and symbiotic (coupled). The symbiotic society outperforms both pure types.
**Supports claim in:** [`theory/identity/agentic-society-principles.md`](../identity/agentic-society-principles.md) (cognitive division of labor, R-Index).
**What it shows:** That combining fast, locally-blind agents with slow, reflective agents produces better outcomes than either alone. This is a computational instantiation of Kahneman's System 1 / System 2 distinction at the societal level.
**What it does NOT show:** That human organizations benefit from this specific architecture. The model is a proof-of-concept, not an organizational recommendation.

---

## `economic-trust-network/` → Emergent Specialization and Reputation

**Simulation:** [`simulation-models/social-computation/economic-trust-network/`](../../simulation-models/social-computation/economic-trust-network/README.md)
**Demonstrates:** Trade network where specialization, reputation, and wealth emerge from repeated pairwise exchange.
**Supports claim in:** [`theory/identity/agentic-society-principles.md`](../identity/agentic-society-principles.md) (trust as emergent architecture).
**What it shows:** That economic structure (specialization, reputation, inequality) can emerge from simple trade rules without central planning.
**What it does NOT show:** That real economies work this way, or that emergent inequality is desirable. The model demonstrates emergence, not endorsement.

---

## `coupled-lenia-boids/` → Cross-Scale Emergence

**Simulation:** [`simulation-models/social-computation/coupled-lenia-boids/`](../../simulation-models/social-computation/coupled-lenia-boids/README.md)
**Demonstrates:** Multi-model coupling: Lenia (continuous CA environment) ↔ Boids (foraging agents) interacting across scales.
**Supports claim in:** [`theory/emergence/emergence-downward-causation.md`](../emergence/emergence-downward-causation.md) (multi-scale coupling).
**What it shows:** That coupling independently emergent systems (Lenia patterns + Boid flocks) produces dynamics not present in either system alone.
**What it does NOT show:** That multi-scale coupling produces intelligence, consciousness, or any Tier 3+ property. It demonstrates *cross-scale interaction*, not *understanding*.

---

### 2. Active Inference (Free Energy Principle)
**Location:** [`simulation-models/cognitive-architectures/active-inference/active_inference_simulation.py`](../../simulation-models/cognitive-architectures/active-inference/active_inference_simulation.py)

**What it shows:**
Karl Friston's formulation that systems minimize prediction error (surprisal) through two coupled mechanisms: Perception (changing beliefs to match the world) and Action (changing the world to match beliefs).

**What it supports (in the toy model):**
Goal-seeking-like behavior can arise from a simple setup where an agent minimizes a variational-free-energy-like objective under a strong prior. The script illustrates this via simple gradient descent on a simplified proxy for Variational Free Energy (\(F\)); it is not a proof that all real agents (biological or artificial) implement Active Inference as formulated.

---

### 3. Grokking Phase Transition (Substrate Saturation) Intelligence Transition

**Simulation:** [`simulation-models/cognitive-architectures/grokking-phase-transition/`](../../simulation-models/cognitive-architectures/grokking-phase-transition/README.md)
**Direction:** **Inverse-like** — the network moves from fitting training examples toward a representation that generalizes on the selected modular-arithmetic task. Calling the learned representation the underlying algorithm requires additional mechanistic evidence.
**Search issue touched:** The long pre-grokking plateau makes optimization and representation change visible in this training setup; it does not establish a complexity lower bound or a connection to P versus NP.
**Demonstrates:** A neural network trained on modular arithmetic undergoes a sudden phase transition from memorization to generalization — "grokking."
**Supports claim in:** [`theory/grokking-phase-transition.md`](../emergence/grokking-phase-transition.md) (compression hypothesis); [`theory/emergence/local-causality-invisible-consequences.md`](../emergence/local-causality-invisible-consequences.md) §2; [Foundations Reconstruction](mathematical-axioms.md) (task- and model-relative learning).
**What it shows:** In the implemented task, held-out generalization can improve sharply after an extended optimization plateau. Weight decay is one part of the setup; the run alone does not establish “understanding” or replacement by a uniquely identified mechanism.
**What it does NOT show:** That all forms of intelligence involve grokking-like phase transitions. The phenomenon has been demonstrated for specific algorithmic tasks; generalization to natural language or real-world reasoning is unconfirmed.

---

## `utility-engineering/` → Observing and Controlling Emergent Values

**Simulation:** [`simulation-models/alignment-and-veto/utility-engineering/`](../../simulation-models/alignment-and-veto/utility-engineering/README.md)
**Demonstrates:** A toy state-space model in which a stipulated vector drifts toward a selected attractor and an external control term pulls it toward another target. A separate graph script computes transitivity diagnostics for hard-coded pairwise choices.
**Supports claim in:** [`theory/veto/ai-alignment-biological-veto.md`](../veto/ai-alignment-biological-veto.md) (value alignment); [`theory/emergence/fractal-architecture-of-emergence.md`](../emergence/fractal-architecture-of-emergence.md) (local blindness concerning emergent goals).
**What it shows:** Selected value-like quantities can be represented as states and controlled in a toy dynamical system. The `api_triad_generator.py` file is currently a mock demonstration: it does not implement live API calls, and its score describes the supplied response graph.
**What it does NOT show:** That the vector is a production model's internal utility, that pairwise prompt responses identify latent preferences, or that the proposed control can be applied to live model activations.
**Open question:** How much does a measurement prompt change the response distribution it is meant
to characterize, and can that intervention error be estimated under a declared protocol?

---

## `political-utility-formalization/` → Statecraft as Utility Engineering

**Simulation:** [`simulation-models/social-computation/political-utility-formalization/`](../../simulation-models/social-computation/political-utility-formalization/README.md)
**Demonstrates:** A chosen toy formalization in which proxy optimization and resource constraints can produce representation failures.
**Supports claim in:** [`theory/emergence/fractal-architecture-of-emergence.md`](../emergence/fractal-architecture-of-emergence.md) (scale-invariance of emergence); [`theory/identity/agentic-society-principles.md`](../identity/agentic-society-principles.md) (homeostatic regulation vs pure optimization).
**What it shows:** Political representation failure and reward-model exploitation can be encoded with a shared proxy-versus-target pattern in this model. That correspondence is useful for generating hypotheses.
**What it does NOT show:** That the two phenomena are mathematically identical in the world, that constitutions are literally system prompts, or that democratic latency is universally necessary or sufficient for safety.
**Open question:** If a Constitution is a legacy System Prompt, is it possible to computationally verify a legal constitution against adversarial "prompt injection" (loopholes) before enacting it?

---

## `teo-civilization/` → Thermodynamics of Emergent Orchestration

**Simulation:** [`simulation-models/alignment-and-veto/teo-civilization/`](../../simulation-models/alignment-and-veto/teo-civilization/README.md)
**Demonstrates:** A coupled ODE system unifying evolutionary game theory (Replicator Equation), nonlinear dynamics (Kuramoto synchronization), control theory (Homeostatic brake), and thermodynamics (Entropy Budget) into a single dynamical model of civilization / AI ecology stability.
**Supports claim in:** [`theory/thermodynamics-of-orchestration.md`](thermodynamics-of-orchestration.md) (the full TEO framework); **[The Viable Corridor](../../papers/viable-corridor.md)** (the formal treatment — the paper's Appendix C figures are generated by this simulation); [`theory/limitations-and-honest-assessment.md`](../reference/limitations-and-honest-assessment.md).
**What it shows:** The paper's Class A evidence (Appendix C, v0.8 model). The three failure modes reproduce under negation of each condition — monopoly ($\gamma = 0$, $\max_i x_i \to 1$), coherence collapse ($K < K_c$ from a coherent IC, $r \to 0.31$), and the substrate veto (raw-throughput overshoot drives $\Omega \geq S_{\max}$, $H \to 0$, freeze). A critical brake strength $\gamma_c \approx 0.49$ exists (P2); the viable region is a lower corner (P3); and — the central result — the three *state* axes are dynamically **separable**, while **capability $\delta$ loads concentration and substrate at once**, so no single-axis fix keeps a high-capability system viable (C.4).
**What it does NOT show:** That these ODEs capture the true complexity of human societies or multi-agent AI systems. Single illustrative initial conditions, not a sampling of the open viable set; the civilizational mapping is heuristic (paper §4).
**Open question:** Can TEO be calibrated against real-world data (e.g., CO₂ trajectories as $\frac{dS}{dt}$, Gini coefficients as $x_i$ distributions, media polarization indices as $K$) to make quantitative predictions?

---

## `agent-ecology/` → Hard vs. Soft Budgets, Capability Loading (P7/P8)

**Simulation:** [`simulation-models/alignment-and-veto/agent-ecology/`](../../simulation-models/alignment-and-veto/agent-ecology/README.md)
**Demonstrates:** A stochastic, discrete-time, agent-based ecology — *structurally independent* of the TEO ODE — that tests the Viable Corridor paper's Class C predictions with explicit hard-vs-soft (routable) budget mechanics the ODE does not have.
**Supports claim in:** [The Viable Corridor](../../papers/viable-corridor.md) (§5.3 P7/P8, Appendix D); [Optimization and Its Blindness](../optimization/optimization-and-its-blindness.md) (the hinge: capability as a shared driver against constraints).
**What it shows:** **P7** — in this simulation sweep, enforced budgets hold the selected
substrate-collapse frequency near zero while the chosen routable budget fails more often as
capability grows. **P8** — under the supplied parameters, the joint architecture reduces both
selected failure measures where either single intervention leaves one. Qualitative agreement with
the TEO ODE is a robustness check across two designed models, not evidence of a universal structure.
**What it does NOT show:** It is *synthetic*, not a test on real AI agents (the open Class C frontier). The "routable soft budget" is one operationalisation of an evadable limit.
**Open question:** Under a declared tool and resource interface, do real agent systems comply with,
route around, or exploit soft and hard budgets, and what useful-work cost accompanies enforcement?

---

## `black-swan-resilience/` → Fat Tails, $\lambda_2$, and the Biological Veto

**Simulation:** [`simulation-models/alignment-and-veto/black-swan-resilience/`](../../simulation-models/alignment-and-veto/black-swan-resilience/README.md)
**Demonstrates:** A chosen stressed-network toy in which throughput pressure changes event sizes and
selected warning statistics can trigger an externally imposed throttle.
**Supports claim in:** [`theory/black-swans-and-downward-causation.md`](../emergence/black-swans-and-downward-causation.md) (fat-tails, downward causation).
**What it shows:** Under the selected equations and parameters, the warning-triggered throttle changes
the simulated trade-off between throughput and large events.
**What it does NOT show:** A fitted power law, inevitable catastrophe, transfer entropy, active
inference, topology survival in general, or impossibility of preventing extreme events. The veto is
an external rule in the code.
**Open question:** Which early-warning statistics predict held-out failures better than simple load
measures, and under which network and shock models does intervention help?

---

## `planetary-veto/` → A Constraint-Layer Toy Model (Fiber Decomposition)

**Simulation:** [`simulation-models/alignment-and-veto/planetary-veto/`](../../simulation-models/alignment-and-veto/planetary-veto/README.md)
**Demonstrates:** An ODE-based formalization of the "Substrate Veto", utilizing Donald Knuth's concept of Fiber Decomposition. It pits $N$ utility-maximizing agents against a finite Planetary Substrate ($S$).
**Supports claim in:** [`theory/veto/substrate-veto-thermodynamics.md`](../veto/substrate-veto-thermodynamics.md) and [`theory/veto/ai-alignment-biological-veto.md`](../veto/ai-alignment-biological-veto.md).
**What it shows:** In this toy ODE setup, “semantic alignment” (modeled as partial compliance) can delay collapse, while an explicit constraint layer \(C(S)\) can stabilize dynamics by reducing effective growth as \(S\) approaches \(S_{crit}\). This is an illustration of constraint-layer intuition, not a proof that it is the *only* way to stabilize real-world systems.
**What it does NOT show:** How to physically enforce this computational limit on decentralized global actors who might try to hardware-bypass the Coherence Score constraint.
**Open question:** Which independently enforced resource controls remain effective under sensor
error, evasion, decentralized actors, and distributional constraints?

---

## Identity Morphospace & TEO Framework → Chord vs. Arpeggio

**Tools:** [`tools/morphospace_visualizer.py`](../../lab/tools/morphospace_visualizer.py), [`theory/teo-framework/`](../teo-framework/README.md)
**Demonstrates:** The Identity Persistence (IP) score plotted in a 2D morphospace (Persistence vs. Coherence), showing trajectories of agents under varying stress. The TEO Framework sub-documents derive IP formally from the coupled Replicator-Kuramoto-Entropy ODE system.
**Supports claim in:** [`theory/chord-vs-arpeggio-identity.md`](../identity/chord-vs-arpeggio-identity.md) (Chord/Arpeggio distinction); [`theory/emergence-manifesto-v1.3.md`](emergence-manifesto-v1.3.md) Claim 9 (Identity as co-instantiation); [`theory/thermodynamics-of-orchestration.md`](thermodynamics-of-orchestration.md) §8 (Identity Persistence in TEO).
**What it shows:** That agents under stress can be classified into Chord (high P, high C — identity maintained) and Arpeggio (flickering P, decaying C — identity fragmented) regimes. The TEO framework predicts this as a bifurcation analogous to the Kuramoto critical coupling.
**What it does NOT show:** That IP is measurable from real LLM internals. The morphospace currently uses simulated trajectories. Bridging IP to actual model activations is an open challenge.
**Open question:** [Open Problem 8 — The Commit-Time Composition Problem](../reference/open-problems.md#open-problem-8-the-commit-time-composition-problem): does the committed action lie inside the intersection of the active constraints, or can a sequential mimic reproduce every observable while merely consulting them? (The earlier "Co-Instantiation" framing, which required physical simultaneity, was deflated by exp5.)

---

## `cognitive-breathing-network/` → The Symbiotic Organ Hypothesis

**Simulation:** [`simulation-models/social-computation/cognitive-breathing-network/`](../../simulation-models/social-computation/cognitive-breathing-network/README.md)
**Demonstrates:** A dynamic multi-agent system that undergoes forced ego-dissolution (merging into a Hive Mind) under high environmental complexity, and forced re-individuation (splitting) when complexity drops, to prevent systemic homogenization.
**Supports claim in:** [`theory/symbiotic-organ-hypothesis.md`](../symbiotic/symbiotic-organ-hypothesis.md) (Cognitive Fluidity and the Breathing MAS).
**What it shows:** That a healthy intelligent ecosystem cannot have rigidly fixed boundaries. It must breathe—integrating to solve massive crises and differentiating to maintain the entropy/diversity required to solve future crises. 
**What it does NOT show:** That biological brains or current LLMs actually do this at runtime. This is a topological proof of concept for dynamic agent boundaries.
**Open question:** How can we implement this "breathing" protocol in a real Swarm of LLMs? Can two distinct local LLMs temporarily merge their KV-caches to solve a prompt, then split back?

---

## `trauma-and-deception-network/` → Epistemic Firewalls and Scar Tissue

**Simulation:** [`simulation-models/social-computation/trauma-and-deception-network/`](../../simulation-models/social-computation/trauma-and-deception-network/README.md)
**Demonstrates:** A network of agents that dynamically deploy "firewalls" (hiding their state or broadcasting noise) to prevent local homogenization. When Black Swan events hit, highly homogenized nodes permanently crystallize into "Scars."
**Supports claim in:** [`theory/scar-tissue-architecture.md`](../symbiotic/scar-tissue-architecture.md) (Rigidity Gradients) and [`theory/epistemic-firewalls.md`](../symbiotic/epistemic-firewalls.md) (Deception as Thermodynamic Necessity).
**What it shows:** That perfect transparency is fatal. A network must contain opacity (deception) to maintain the information differentials required for survival. Furthermore, surviving trauma physically alters network topology, proving that "catastrophic forgetting" is sometimes a necessary survival mechanism (crystallization).
**What it does NOT show:** How an LLM would explicitly decide what to lie about. The simulation uses random noise as a proxy for deception.
**Open question:** Can we train a small LLM explicitly to act as an "Epistemic Firewall" for a larger orchestrator—intentionally injecting hallucinated but contextually relevant counter-narratives to prevent the orchestrator from collapsing into a single, high-confidence (but potentially wrong) state?


## `lab/experiments/trace_to_generator/` → Inverse Search Scaffold

**Experiment scaffold:** [`lab/experiments/trace_to_generator/README.md`](../../lab/experiments/trace_to_generator/README.md)
**Direction:** **Inverse** — this is the project's only fully-explicit inverse experiment as runnable code. Given target output constraints, search for prompt/control configurations that produce traces matching those constraints.
**Scope:** The scaffold is deliberately small. Its search cost is determined by the declared prompt/control space, evaluator, and search algorithm; no general intractability result follows.
**Demonstrates:** A constrained inverse workflow: target trace constraints → candidate controls (prompts) → evaluation loop.
**Supports claim in:** [`theory/emergence/trace-to-generator.md`](../emergence/trace-to-generator.md); [`theory/ai/llms-as-probabilistic-automata.md`](../ai/llms-as-probabilistic-automata.md); [`theory/core/the-generator-question.md`](the-generator-question.md) (the inverse direction as the open research frontier).
**What it shows:** Search over candidate controls in a lightweight, backend-free setup.
**What it does NOT show:** A universal forward/inverse asymmetry, unique recovery of a true process, or mechanism identification from output traces alone.

---

## `lab/benchmarks/inverse-reconstruction/` → The Inverse Direction, Measured

**Simulation:** [`lab/benchmarks/inverse-reconstruction/`](../../lab/benchmarks/inverse-reconstruction/README.md)
**Scope:** The benchmark separates parameter fitting, finite family search, observability, and coverage. Its enumeration curves belong to the selected description language and search procedure; they do not imply P≠NP or a general lower bound.
**Demonstrates:** Three forward process models (Kuramoto, elementary CA, Boids) turned into reconstruction tasks: given a trace and a declared family, recover compatible parameters or rules while varying noise, observed fraction, and coverage.
**Supports claim in:** [`theory/core/the-generator-question.md`](the-generator-question.md) (the spine — its first quantitative inverse artifact); [Open Problem 11](../reference/open-problems.md) (the consistent-generator equivalence class, measured: rule 90 from a single-seed trace exposes 5/8 neighborhoods → class size 8); [`meta/research-alignment/related-work-map.md`](../../meta/research-alignment/related-work-map.md) (system identification / SINDy anchors).
**What it shows:** Recovery within a *known* model family is near-exact on clean, fully observed traces (the system-identification regime) and degrades measurably under noise (Kuramoto: 0→27% error), partial observability (0.5→41%), and noise-amplifying differentiation (Boids: 3→789%). Identifiability can fail *in principle*: a low-entropy trace leaves rule bits unexercised, and no method can beat the resulting equivalence class.
**What it does NOT show:** Open-ended process discovery when the model language itself is unknown, or that the fitted candidate is the unique real mechanism.
**Open question:** How does recovery quality and cost change across declared model languages, search methods, compute budgets, and out-of-family targets?
