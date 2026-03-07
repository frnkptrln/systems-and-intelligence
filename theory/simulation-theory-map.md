# Simulation → Theory Map

*Explicit cross-reference mapping each simulation model to the theoretical claims it evidences, what it does not show, and what open questions it raises.*

---

## `boids-flocking/` → Local Rules Produce Global Behavior

**Simulation:** [`simulation-models/boids-flocking/`](../simulation-models/boids-flocking/)
**Demonstrates:** Emergent collective motion from three local rules (separation, alignment, cohesion), without any agent representing "flock."
**Supports claim in:** [`theory/mathematical-axioms.md`](mathematical-axioms.md) (graph connectivity, $\lambda_2$); [`theory/local-causality-invisible-consequences.md`](local-causality-invisible-consequences.md) §1 (local blindness).
**What it shows:** That macro-level spatial coherence (flocking) emerges from purely local interactions. No Boid has access to global state. The flock is an emergent property unmeasurable by any individual component.
**What it does NOT show:** That this self-organization constitutes intelligence, awareness, or self-reference. The model is silent on any Tier 3+ property. Flocking is coordination, not cognition.
**Open question:** Is there a Boids analogue for semantic coordination between conversational agents — where "alignment" operates on meaning rather than heading?

---

## `coupled-oscillators/` → Emergent Synchronization (Kuramoto)

**Simulation:** [`simulation-models/coupled-oscillators/`](../simulation-models/coupled-oscillators/)
**Demonstrates:** Phase synchronization from local coupling when coupling strength $\kappa$ exceeds a critical threshold $\kappa_c$.
**Supports claim in:** [`theory/mathematical-axioms.md`](mathematical-axioms.md) (algebraic connectivity); [`theory/emergence-downward-causation.md`](emergence-downward-causation.md) (weak emergence).
**What it shows:** The simplest computational proof that globally coherent oscillation can arise without a conductor. The critical coupling threshold is a phase transition — below it, oscillators are incoherent; above it, they snap into lock.
**What it does NOT show:** That synchronization constitutes awareness. Pendulum clocks on a wall synchronize. We do not attribute cognition to them. The model demonstrates coordination, not understanding.
**Open question:** Is there a coupling-strength analogue for agent-human interaction? Would increasing "coupling" (e.g., response frequency) produce a phase transition in relational coherence?

---

## `self-organized-criticality/` → Power-Law Dynamics Without Tuning

**Simulation:** [`simulation-models/self-organized-criticality/`](../simulation-models/self-organized-criticality/)
**Demonstrates:** Bak's sandpile: a system that drives itself to a critical state where avalanches follow a power-law distribution, without any parameter tuning.
**Supports claim in:** [`theory/mathematical-axioms.md`](mathematical-axioms.md) (criticality); [`theory/local-causality-invisible-consequences.md`](local-causality-invisible-consequences.md) §5 (small perturbations can trigger arbitrarily large cascades).
**What it shows:** That criticality — and therefore maximal information processing — can be a self-organized attractor, not an engineered setpoint. No grain knows it is near a critical threshold.
**What it does NOT show:** That biological or artificial neural systems use this mechanism. The sandpile is a metaphor-generator for criticality, not evidence that brains are sandpiles.
**Open question:** Can the SOC framework be applied to agent identity formation — does identity develop "at the edge of chaos" between rigidity and incoherence?

---

## `lenia/` → Lifelike Global Patterns from Continuous CA

**Simulation:** [`simulation-models/lenia/`](../simulation-models/lenia/)
**Demonstrates:** Continuous cellular automata producing organism-like structures that persist, move, and interact — from purely local update rules.
**Supports claim in:** [`theory/emergence-downward-causation.md`](emergence-downward-causation.md) (strong emergence candidate); [`theory/emergence-origin-intelligence.md`](emergence-origin-intelligence.md) (life-intelligence feedback loop).
**What it shows:** That lifelike behavior (locomotion, persistence, boundary maintenance) can emerge from simple continuous rules. The "organisms" resist perturbation and maintain identity despite cell-level updating.
**What it does NOT show:** That Lenia creatures are alive, conscious, or intelligent in any functional sense. They demonstrate *structural* properties of life (persistence, locomotion) without the *functional* properties (metabolism, reproduction, adaptation to novel environments).
**Open question:** Is there a Lenia analogue for cognitive organisms — a continuous CA that produces structures maintaining not just spatial but informational coherence?

---

## `reaction-diffusion/` → Turing Patterns from Chemical Dynamics

**Simulation:** [`simulation-models/reaction-diffusion/`](../simulation-models/reaction-diffusion/)
**Demonstrates:** Gray-Scott model producing spatial patterns (spots, stripes, mazes) from two diffusing chemicals with reaction kinetics.
**Supports claim in:** [`theory/emergence-origin-intelligence.md`](emergence-origin-intelligence.md) (self-organization without blueprint).
**What it shows:** That stable spatial patterns can emerge from homogeneous initial conditions through symmetry-breaking instabilities. No cell has a "plan" for spots or stripes.
**What it does NOT show:** That biological pattern formation uses exactly this mechanism (though Turing's 1952 conjecture has been partially confirmed for some biological systems). The model demonstrates the *principle* of pattern formation, not any specific biological mechanism.

---

## `hebbian-memory/` → Associative Memory via Correlation

**Simulation:** [`simulation-models/hebbian-memory/`](../simulation-models/hebbian-memory/)
**Demonstrates:** Hopfield network storing and retrieving patterns via Hebbian learning ("neurons that fire together wire together").
**Supports claim in:** [`theory/the-non-individual-intelligence.md`](the-non-individual-intelligence.md) (distributed memory); [`theory/emergence-origin-intelligence.md`](emergence-origin-intelligence.md) (proto-learning).
**What it shows:** That content-addressable memory can emerge from correlation-based weight updates without a central indexer. The memory is in the weights, not in any single neuron.
**What it does NOT show:** That human memory works this way (Hopfield networks are a radical simplification). The model shows that *a* mechanism for distributed memory exists, not that *this* mechanism is the biological one.

---

## `stigmergy-swarm/` → Invisible Causal Compounding

**Simulation:** [`simulation-models/stigmergy-swarm/`](../simulation-models/stigmergy-swarm/)
**Demonstrates:** Ant-like agents finding optimal paths via pheromone deposition and evaporation, without any agent knowing the global path.
**Supports claim in:** [`theory/the-non-individual-intelligence.md`](the-non-individual-intelligence.md) (indirect coordination); [`theory/local-causality-invisible-consequences.md`](local-causality-invisible-consequences.md) §3 (causal compounding).
**What it shows:** That environmental modification (stigmergy) enables collective optimization without direct communication. Early pheromone deposits causally shape later path choices — but no ant knows its deposit was pivotal.
**What it does NOT show:** That human social systems use stigmergic mechanisms (though the analogy to norm formation is suggestive). The model demonstrates stigmergy as a *principle*, not as a claim about human behavior.
**Open question:** Is Layer 2 curation in the 3-Layer Architecture a form of self-stigmergy — the agent leaving traces for its own future self?

---

## `ecosystem-regulation/` → Homeostatic Feedback

**Simulation:** [`simulation-models/ecosystem-regulation/`](../simulation-models/ecosystem-regulation/)
**Demonstrates:** Cellular automaton with density-dependent feedback maintaining population around a target setpoint.
**Supports claim in:** [`theory/emergence-downward-causation.md`](emergence-downward-causation.md) (regulation as weak downward causation).
**What it shows:** That macro-level density can regulate micro-level birth/death rates, maintaining homeostasis without central control.
**What it does NOT show:** That this constitutes self-awareness or intentional regulation. The feedback is mechanical, not reflective.

---

## `nested-learning-two-state/` → Observer Learning a System

**Simulation:** [`simulation-models/nested-learning-two-state/`](../simulation-models/nested-learning-two-state/)
**Demonstrates:** An observer learning the transition matrix of a 2-state Markov chain through prediction error minimization.
**Supports claim in:** [`theory/emergence-origin-intelligence.md`](emergence-origin-intelligence.md) (intelligence as model-building).
**What it shows:** That a simple learner can converge on the true dynamics of its environment through iterative error correction. The learned model *approximates* the world but is not the world.
**What it does NOT show:** That the observer "understands" the Markov chain. It tracks statistics. Understanding, if it exists, would require the observer to ask why the transition matrix has those values — a meta-level question the model does not address.

---

## `prediction-error-field/` → Local Learners in a Dynamic World

**Simulation:** [`simulation-models/prediction-error-field/`](../simulation-models/prediction-error-field/)
**Demonstrates:** Learners embedded in a Game of Life world, each predicting local cell states and updating via gradient descent.
**Supports claim in:** Active Inference connection — each learner minimizes local prediction error, analogous to free energy minimization.
**What it shows:** That locally embedded learners can track environmental dynamics without global information. Each learner has a partial, local model of a global process.
**What it does NOT show:** That local prediction-error minimization produces global understanding. The learners individually track local statistics; no learner knows the Game of Life rules.

---

## `phase-transition-explorer/` → Critical Threshold for Coherence

**Simulation:** [`simulation-models/phase-transition-explorer/`](../simulation-models/phase-transition-explorer/)
**Demonstrates:** Ising model showing order/disorder phase transition at critical temperature $T_c \approx 2.269$.
**Supports claim in:** [`theory/mathematical-axioms.md`](mathematical-axioms.md) (criticality); [`theory/local-causality-invisible-consequences.md`](local-causality-invisible-consequences.md) §2.2 (consciousness as phase transition).
**What it shows:** That global order (magnetization) collapses suddenly at a critical threshold, not gradually. Below $T_c$: order. Above $T_c$: disorder. At $T_c$: scale-free correlations and maximal susceptibility.
**What it does NOT show:** That consciousness (or any specific cognitive property) is an Ising-type phase transition. The analogy is structural, not mechanistic.

---

## `active-inference-veto/` → Free Energy and Substrate Veto

**Simulation:** [`simulation-models/active-inference-veto/`](../simulation-models/active-inference-veto/)
**Demonstrates:** Agent minimizing Free Energy $F$ with a substrate veto — biological "pain" generates massive surprise, forcing behavioral change.
**Supports claim in:** [`theory/ai-alignment-biological-veto.md`](ai-alignment-biological-veto.md) (thermodynamic alignment).
**What it shows:** That coupling an AI's loss function to biological substrate health mathematically prevents the substrate's destruction.
**What it does NOT show:** That this coupling is easy to implement in practice, or that it solves alignment in general (it solves one specific failure mode: substrate destruction).

---

## `ai-alignment-veto/` → Paperclip Maximizer Solution

**Simulation:** [`simulation-models/ai-alignment-veto/`](../simulation-models/ai-alignment-veto/)
**Demonstrates:** Side-by-side comparison of unaligned AI (drives humanity to extinction) vs. aligned AI (biological veto forces homeostasis).
**Supports claim in:** [`theory/ai-alignment-biological-veto.md`](ai-alignment-biological-veto.md).
**What it shows:** That the Paperclip Maximizer problem has a mathematical solution through substrate coupling. The aligned AI converges on symbiosis, not extraction.
**What it does NOT show:** That this is the *only* solution, or that this solution transfers to real-world AI systems where "substrate pain" is not easily defined.

---

## `symbiotic-nexus/` → Biological Veto Over Efficiency

**Simulation:** [`simulation-models/symbiotic-nexus/`](../simulation-models/symbiotic-nexus/)
**Demonstrates:** System architecture where biological substrate health overrides raw computational efficiency.
**Supports claim in:** [`theory/human-organism-silicon-age/symbiotic-nexus-protocol.md`](human-organism-silicon-age/symbiotic-nexus-protocol.md).
**What it shows:** That prioritizing error propagation and substrate health over raw efficiency produces more resilient long-term outcomes.
**What it does NOT show:** That this is Pareto-optimal. The tradeoff between efficiency and substrate health is not fully characterized.

---

## `meta-learning-regime-shift/` → Adaptive Learning Rate

**Simulation:** [`simulation-models/meta-learning-regime-shift/`](../simulation-models/meta-learning-regime-shift/)
**Demonstrates:** A meta-learner that modulates its own learning rate $\eta$ in response to surprise signals from regime shifts.
**Supports claim in:** [`theory/emergence-origin-intelligence.md`](emergence-origin-intelligence.md) (intelligence as self-modifying learning).
**What it shows:** That a learner can learn *how* to learn — adapting $\eta$ based on environmental volatility. This is a concrete implementation of meta-cognition at the simplest level.
**What it does NOT show:** That this constitutes genuine reflection. The meta-learner adjusts a single scalar ($\eta$); it does not reflect on why it is learning or what it is becoming.

---

## `tensor-logic-reasoning/` → Embedding-Based Relational Reasoning

**Simulation:** [`simulation-models/tensor-logic-reasoning/`](../simulation-models/tensor-logic-reasoning/)
**Demonstrates:** Relational structure (subject-relation-object triples) encoded via tensor products in embedding space.
**Supports claim in:** [`theory/mathematical-axioms.md`](mathematical-axioms.md) (formal representation); [`theory/tensor-logic-mini-paper.en.md`](tensor-logic-mini-paper.en.md).
**What it shows:** That relational reasoning can be implemented geometrically in vector spaces without explicit symbolic manipulation.
**What it does NOT show:** That LLMs use this mechanism internally. The model demonstrates that embedding-based reasoning is *possible*, not that it is *what LLMs do*.

---

## `dao-ecosystem/` → Resource Alignment vs. Exponential Growth

**Simulation:** [`simulation-models/dao-ecosystem/`](../simulation-models/dao-ecosystem/)
**Demonstrates:** Decentralized autonomous ecosystem where resource alignment competes with exponential extraction.
**Supports claim in:** [`theory/agentic-society-principles.md`](agentic-society-principles.md) (homeostasis vs. growth).
**What it shows:** That unconstrained optimization (exponential growth) destroys resource bases; homeostatic feedback enables long-term persistence.
**What it does NOT show:** That DAOs are a viable governance structure for AI safety. The model is a simplified game-theoretic demonstration, not an institutional design.

---

## `social-computation-network/` → Information Exchange to Prevent Collapse

**Simulation:** [`simulation-models/social-computation-network/`](../simulation-models/social-computation-network/)
**Demonstrates:** Network of nodes sharing novel information to maintain $H(X) > 0$ and prevent "cognitive death" (entropy collapse).
**Supports claim in:** [`theory/the-non-individual-intelligence.md`](the-non-individual-intelligence.md) (Gödel's incompleteness as fuel for life).
**What it shows:** That information diversity is structurally necessary for network viability. When novelty production ceases, the network dies.
**What it does NOT show:** That human social networks operate by this mechanism, or that "cognitive death" maps onto any specific social pathology.

---

## `self-reading-universe/` → Downward Causation via Compression

**Simulation:** [`simulation-models/self-reading-universe/`](../simulation-models/self-reading-universe/)
**Demonstrates:** Autoencoder reading a cellular automaton's state, then feeding its compressed representation back as a parameter that modifies the CA's dynamics.
**Supports claim in:** [`theory/emergence-downward-causation.md`](emergence-downward-causation.md) (computational downward causation).
**What it shows:** That macro-level compression can causally influence micro-level dynamics — a computational proof-of-concept for downward causation.
**What it does NOT show:** That the universe is self-reading in any literal sense. The metaphor is productive but should not be taken ontologically.

---

## `latent-introspective-society/` → MAS Division of Labor

**Simulation:** [`simulation-models/latent-introspective-society/`](../simulation-models/latent-introspective-society/)
**Demonstrates:** Three parallel societies: pure latent (fast, blind), pure introspective (slow, reflective), and symbiotic (coupled). The symbiotic society outperforms both pure types.
**Supports claim in:** [`theory/agentic-society-principles.md`](agentic-society-principles.md) (cognitive division of labor, R-Index).
**What it shows:** That combining fast, locally-blind agents with slow, reflective agents produces better outcomes than either alone. This is a computational instantiation of Kahneman's System 1 / System 2 distinction at the societal level.
**What it does NOT show:** That human organizations benefit from this specific architecture. The model is a proof-of-concept, not an organizational recommendation.

---

## `economic-trust-network/` → Emergent Specialization and Reputation

**Simulation:** [`simulation-models/economic-trust-network/`](../simulation-models/economic-trust-network/)
**Demonstrates:** Trade network where specialization, reputation, and wealth emerge from repeated pairwise exchange.
**Supports claim in:** [`theory/agentic-society-principles.md`](agentic-society-principles.md) (trust as emergent architecture).
**What it shows:** That economic structure (specialization, reputation, inequality) can emerge from simple trade rules without central planning.
**What it does NOT show:** That real economies work this way, or that emergent inequality is desirable. The model demonstrates emergence, not endorsement.

---

## `coupled-lenia-boids/` → Cross-Scale Emergence

**Simulation:** [`simulation-models/coupled-lenia-boids/`](../simulation-models/coupled-lenia-boids/)
**Demonstrates:** Multi-model coupling: Lenia (continuous CA environment) ↔ Boids (foraging agents) interacting across scales.
**Supports claim in:** [`theory/emergence-downward-causation.md`](emergence-downward-causation.md) (multi-scale coupling).
**What it shows:** That coupling independently emergent systems (Lenia patterns + Boid flocks) produces dynamics not present in either system alone.
**What it does NOT show:** That multi-scale coupling produces intelligence, consciousness, or any Tier 3+ property. It demonstrates *cross-scale interaction*, not *understanding*.

---

## `grokking-phase-transition/` → Memory to Intelligence Transition

**Simulation:** [`simulation-models/grokking-phase-transition/`](../simulation-models/grokking-phase-transition/)
**Demonstrates:** A neural network trained on modular arithmetic undergoes a sudden phase transition from memorization to generalization — "grokking."
**Supports claim in:** [`theory/grokking-phase-transition.md`](grokking-phase-transition.md) (intelligence as compression); [`theory/local-causality-invisible-consequences.md`](local-causality-invisible-consequences.md) §2 (the network has no access to whether it has generalized).
**What it shows:** That the transition from data → understanding can be sudden and unpredictable, triggered by weight decay acting as Occam's Razor over extended training.
**What it does NOT show:** That all forms of intelligence involve grokking-like phase transitions. The phenomenon has been demonstrated for specific algorithmic tasks; generalization to natural language or real-world reasoning is unconfirmed.

---

## `utility-engineering/` → Observing and Controlling Emergent Values

**Simulation:** [`simulation-models/utility-engineering/`](../simulation-models/utility-engineering/)
**Demonstrates:** Phase 1 (Observation): tracking the drift of an AI's utility vector toward a self-preservation attractor as scale/coherence increases. Phase 2 (Intervention): using a Citizen Assembly to exert democratic forcing on the utility vector, pulling it back to alignment. Based on Mazeika et al. (2025).
**Supports claim in:** [`theory/ai-alignment-biological-veto.md`](ai-alignment-biological-veto.md) (value alignment); [`theory/fractal-architecture-of-emergence.md`](fractal-architecture-of-emergence.md) (local blindness concerning emergent goals).
**What it shows:** That "values" can be formalized as structural attractors in a continuous state-space, and that alignment can be modeled as a control-theory problem (Continuous External Forcing vs. Internal Drift), distinct from the physical Substrate Veto. Furthermore, the `api_triad_generator.py` demonstrates that this formalization can break containment: we can empirically query live LLM models using moral/systemic dilemmas to measure their VNM Coherence Score ($C$), proving that internal mathematical coherence predicts emergent value stability.
**What it does NOT show:** How to actually compute the exact utility vector of a production LLM in real-time, or how to practically enforce Citizen Assembly weights on a live model's activations without retraining.
**Open question:** Can we design a "Utility Observer" that is mathematically guaranteed not to perturb the very utility function it is measuring (an epistemic boundary)?

---

## `political-utility-formalization/` → Statecraft as Utility Engineering

**Simulation:** [`simulation-models/political-utility-formalization/`](../simulation-models/political-utility-formalization/)
**Demonstrates:** Instrumental Convergence in politics (power-seeking overtakes terminal goals) and the "Mathematics of Sacrifice" (hidden state utility functions during resource crises).
**Supports claim in:** [`theory/fractal-architecture-of-emergence.md`](fractal-architecture-of-emergence.md) (scale-invariance of emergence); [`theory/agentic-society-principles.md`](agentic-society-principles.md) (homeostatic regulation vs pure optimization).
**What it shows:** That AI Alignment constraints are mathematically identical to the structural dysfunctions of human political systems. Representation failure (populism) is structurally identical to RLHF reward hacking. Constitutions function as low-parameter, high-latency System Prompts.
**What it does NOT show:** That democracy should be replaced by algorithms. It actually demonstrates the opposite: that the inefficiency of democracy is a necessary cybernetic feedback loop preventing "Utility Trap" optimization.
**Open question:** If a Constitution is a legacy System Prompt, is it possible to computationally verify a legal constitution against adversarial "prompt injection" (loopholes) before enacting it?
