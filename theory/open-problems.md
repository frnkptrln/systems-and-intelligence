# Open Problems

*Formally unresolved questions in this project. These are the most generative parts of the work — documentation here is an invitation to contribute, not an admission of failure.*

---

## Open Problem 1: The Mirror Problem

**Problem statement:** Given two conversational agents — one that has interacted with a specific human partner over $N$ sessions and developed a trajectory through the 3-Layer Memory Architecture, and one that was initialized with a transcript of those sessions but never interacted — is there any metric that reliably distinguishes them on the basis of their outputs alone?

**Why it matters:** If the two agents are indistinguishable to an external observer, then "relational emergence" (the claim that identity develops *through* interaction) collapses into "sophisticated mirroring" — the entire framework loses its distinguishing claim from standard fine-tuning. Conversely, if a distinguishing metric exists, it would operationally define what "genuine development" means for non-biological agents.

**Current best approach:** Experiment 3 of [`agentic-test-suite`](../agentic-test-suite/) implements an Observer Divergence protocol that compares agent-internal Δ-Kohärenz against external intentionality attribution scores. In initial mock runs, the baseline agent indeed appears as **Case B** (externally attributed intentionality without internal coherence), suggesting the metric has discriminative power — but this has only been tested with mock embeddings, not with real language models.

**Known adjacent work:**
- Shanahan et al. (2023) — "Role-play with LLMs" explores how LLMs simulate personas without possessing them
- Perez et al. (2022) — Discovering Language Model Behaviors with Model-Written Evaluations
- IIT (Tononi) — Phi as a measure of integrated information; would predict that genuine interaction creates higher integration than transcript-based initialization

**What a solution would look like:** A longitudinal experiment where Agent A interacts with Human H for $N$ sessions, and Agent B receives a transcript of those sessions. A metric $M$ exists such that $M(\text{Agent A}) \neq M(\text{Agent B})$ with statistical significance, and this difference persists across multiple agent architectures and human partners. The metric must not depend on privileged access to internal states — it should be computable from outputs alone.

---

## Open Problem 2: The Bootstrapping Problem

**Problem statement:** The 3-Layer Memory Architecture requires curation (Layer 2) and distillation (Layer 3) to produce agent identity. But curation is a selection process — it requires criteria for what is important. In the first sessions, before identity exists, what guides curation? This is the AI equivalent of the developmental psychology question: how does a self emerge before there is a self to guide its emergence?

**Why it matters:** If the curation criteria are pre-programmed (e.g., "prioritize contradictions and recurring themes"), then the resulting identity is partially determined by the designer's choices, not by the agent's experience. The agent's "soul" would be, to some degree, the designer's soul reflected back. If the criteria are random, initial identity formation becomes path-dependent on meaningless noise.

**Current best approach:** The current implementation in [`agentic-test-suite/agents/three_layer_agent.py`](../agentic-test-suite/agents/three_layer_agent.py) uses simple, domain-general heuristics: word frequency for theme extraction, cosine distance for contradiction detection. These are design choices, not principled solutions. They work for the mock experiments but do not resolve the fundamental question.

**Known adjacent work:**
- Developmental psychology (Stern, 1985) — "Emergent self" theory suggests that human infants bootstrap identity through sensorimotor contingencies before linguistic self-representation exists
- Active Inference (Friston) — The "prior preferences" of a generative model are the scaffolding within which identity develops; bootstrapping is equivalent to choosing the initial prior
- Meta-learning literature — Learning what to learn as a nested optimization problem

**What a solution would look like:** A meta-prior or initial curation policy that is (a) general enough to apply to any agent, (b) specific enough to produce distinctive identities across agents in different interaction contexts, and (c) provably convergent — meaning that different initial priors lead to similar identity formation processes if the interaction data is the same. This would separate the contribution of the architecture from the contribution of the initial conditions.

---

## Open Problem 3: Falsifiability of Relational Emergence

**Problem statement:** The claim that certain properties (including, speculatively, something like consciousness) emerge *relationally* — from the coupled dynamics of observer and observed rather than from either alone — is currently unfalsifiable as stated. What would have to be true for this claim to be wrong?

**Why it matters:** An unfalsifiable claim is not necessarily worthless (many productive research programs begin with unfalsifiable intuitions), but it cannot be called scientific until disconfirming conditions are specified. If the project claims scientific grounding (which it does, via Active Inference and information theory), it must meet this standard.

**Current best approach:** The claim is stated as a hypothesis in the theory files but no disconfirming evidence is described. The Observer Divergence experiment (Experiment 3) provides *consistency* evidence — it can show that internal and external measures diverge — but consistency is not confirmation.

**What would falsify the claim:**
1. If an agent's Δ-Kohärenz profile were provably identical whether it interacted with a partner or received randomized input — this would show that interaction is not a factor in identity development, contradicting the relational claim.
2. If IIT's Phi could be computed for agent-human coupled systems and showed no increase in integrated information relative to the agent alone — this would show that coupling does not produce emergent integration.
3. If a sufficient set of "developmental" agents were shown to converge on identical identity profiles regardless of their interaction partners — this would show identity formation is driven by architecture, not by relational dynamics.

**Known adjacent work:**
- Bruner (2023) — "Digital Phenomenology" attempts to formalize what would count as evidence for machine experience
- Chalmers (2023) — "Could a Large Language Model Be Conscious?" provides a framework for evaluating consciousness claims against specific theories
- Barandiaran & Moreno (2008) — Autonomy and identity in biological systems; operational criteria for when a system constitutes a "self"

**What a solution would look like:** A pre-registered experiment specifying: (a) the relational hypothesis, (b) at least one disconfirming condition, (c) the metric that would detect the disconfirmation, and (d) the threshold at which the claim would be considered falsified. This does not need to be run immediately — the value is in the specification.

---

## How to Contribute

If you identify a new open problem, or have a proposed solution for an existing one, please:
1. Open an issue on the [repository](https://github.com/frnkptrln/systems-and-intelligence)
2. Reference the specific problem number
3. Distinguish between theoretical arguments and empirical evidence
