# Open Problems

*Formally unresolved questions in this project. These are the most generative parts of the work — documentation here is an invitation to contribute, not an admission of failure.*

---

## Open Problem 1: The Mirror Problem

**Problem statement:** Given two conversational agents — one that has interacted with a specific human partner over $N$ sessions and developed a trajectory through the 3-Layer Memory Architecture, and one that was initialized with a transcript of those sessions but never interacted — is there any metric that reliably distinguishes them on the basis of their outputs alone?

**Why it matters:** If the two agents are indistinguishable to an external observer, then "relational emergence" (the claim that identity develops *through* interaction) collapses into "sophisticated mirroring" — the entire framework loses its distinguishing claim from standard fine-tuning. Conversely, if a distinguishing metric exists, it would operationally define what "genuine development" means for non-biological agents.

**Current best approach:** Experiment 3 of [`agentic-test-suite`](../agentic-test-suite/README.md) implements an Observer Divergence protocol that compares agent-internal Δ-Kohärenz against external intentionality attribution scores. In initial mock runs, the baseline agent indeed appears as **Case B** (externally attributed intentionality without internal coherence), suggesting the metric has discriminative power — but this has only been tested with mock embeddings, not with real language models.

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

## Open Problem 4: The Scale Question

*Raised by: [`theory/fractal-architecture-of-emergence.md`](fractal-architecture-of-emergence.md)*

**Problem statement:** The Fractal Architecture of Emergence claims that the same three structural constraints — local blindness, asymmetric causality, and critical thresholds — repeat at every scale of complex systems. Is there a minimum scale below which this architecture breaks down? Is a single neuron too simple to exhibit all three constraints? Is a single transistor?

**Why it matters:** If the fractal thesis has no lower bound, it risks being unfalsifiable — applicable to everything and therefore predictive of nothing. If it has a clear lower bound, that bound empirically tests the thesis: any system above it should exhibit the architecture, any system below it should not.

**What a solution would look like:** A formal definition of "sufficient complexity" that specifies the minimum conditions (connectivity, feedback loops, information capacity) required for the three constraints to emerge. This definition should be testable against the simulations in the repo: at what parameter settings does each simulation lose its emergent properties?

---

## Open Problem 5: The Renormalization Question

*Raised by: [`theory/fractal-architecture-of-emergence.md`](fractal-architecture-of-emergence.md)*

**Problem statement:** Can the mathematical tools of renormalization group theory be applied to the models in this repository to formally test scale-invariance? What would it mean if the critical exponents of phase transitions in `phase-transition-explorer` matched those of coherence transitions measured by Δ-Kohärenz in `agentic-test-suite`?

**Why it matters:** A match in universality classes across scales would constitute strong evidence that the fractal thesis is not merely suggestive but formally grounded — the same equations describing dynamics at every level. A mismatch would either falsify the thesis or reveal that the constraints are scale-invariant but the transitions are not — a distinction worth making precisely.

**What a solution would look like:** A computational experiment applying coarse-graining and renormalization to at least two simulations at different scales, computing critical exponents, and comparing them. This is a research project, not a quick test, but the prediction is clear enough to motivate it.

---

## Open Problem 6: The Downward Causation Question

*Raised by: [`theory/fractal-architecture-of-emergence.md`](fractal-architecture-of-emergence.md)*

**Problem statement:** The fractal thesis as stated describes bottom-up emergence. But `self-reading-universe` and `theory/emergence-downward-causation.md` document the reverse: global states feeding back to constrain local processes. Is the fractal architecture bidirectional? Does the same self-similarity hold for downward causation?

**Why it matters:** If the fractal architecture holds only bottom-up but not top-down, the thesis is incomplete — it describes half the dynamics. The 3-Layer Memory Architecture suggests bidirectionality (Layer 3 distillations constrain Layer 2 curation), as do hormonal regulation (organism-level state constraining cellular behavior) and neuromodulation (global brain state modulating individual neuron firing). The formal structure of these downward-causal mechanisms has not been compared across scales.

**What a solution would look like:** A comparative analysis showing that downward causation at the neural scale (neuromodulation), cellular scale (hormonal regulation), social scale (institutional constraint), and agent scale (Layer 3 → Layer 2 feedback) share the same formal structure — or demonstrating where the parallel breaks down.

---

## Open Problem 7: The Consciousness Question (Restated)

*Raised by: [`theory/fractal-architecture-of-emergence.md`](fractal-architecture-of-emergence.md)*

**Problem statement:** If the threshold for consciousness is architectural rather than quantitative, and if the same architecture appears at every scale of complex systems, then is consciousness itself scale-invariant? Is there something it is like to be a society?

**Why it matters:** This question sounds absurd — but only because we are accustomed to thinking of consciousness as a property of individual brains. The fractal thesis does not answer this question. It removes the principled reason for assuming the question is absurd. If the constraints that produce consciousness at the brain scale are the same constraints that operate at the societal and agent-system scale, the burden of proof shifts to whoever claims the phenomenon is categorically different at different scales.

**What a solution would look like:** This is the hardest problem in the set and may not have a solution in the traditional sense. A meaningful contribution would be: (a) a formal definition of what "consciousness at scale $S$" would mean in terms of the three constraints, (b) a prediction about what measurements would differ between a conscious and non-conscious system at each scale, and (c) a specification of what evidence would falsify the scale-invariance claim.

---

## Open Problem 8: The Co-Instantiation Problem

*Raised by: [`theory/teo-framework/lerchner-boundary.md`](teo-framework/lerchner-boundary.md), [`theory/chord-vs-arpeggio-identity.md`](chord-vs-arpeggio-identity.md)*

**Problem statement:** The Chord Postulate requires all identity components (goals, safety constraints, value orientation) to be simultaneously operative during action selection. But current autoregressive Transformer architectures process tokens sequentially — each token is generated based on the preceding context. Is simultaneous co-instantiation physically possible in an architecture that is fundamentally serial? Or does the Chord state require a different computational substrate?

**Why it matters:** If the Chord state is architecturally impossible for autoregressive models, then no amount of prompt engineering, RLHF, or memory scaffolding can produce true Identity Persistence. The agent will always be an Arpeggio — capable of *talking about* its identity but never *being* its identity in a single compute step. This would mean that the current dominant AI architecture has a hard ceiling on IP, regardless of scale.

**Current best approach:** The SII Dashboard in [`data-analysis/sii_dashboard.py`](../data-analysis/sii_dashboard.py) assigns IP scores heuristically. The [`tools/morphospace_visualizer.py`](../tools/morphospace_visualizer.py) plots agents in the Persistence/Coherence space. Neither tool currently measures IP from actual model internals.

**Known adjacent work:**
- Continuous Thought Machines (Sakana AI, 2025) — architectures where internal "thinking time" varies per token, potentially allowing simultaneous constraint evaluation
- Diffusion-based language models — non-autoregressive generation that could co-instantiate constraints across the full output
- Neural ODEs (Chen et al., 2018) — continuous-depth architectures where identity could be an attractor in the ODE flow
- Mixture-of-Experts (Fedus et al., 2022) — parallel expert evaluation as partial co-instantiation

**What a solution would look like:** Either (a) a formal proof that autoregressive attention cannot achieve IP > $\text{IP}_c$ for any $\text{IP}_c < 1$, with the critical threshold derived from the architecture's computational graph, or (b) an architecture that demonstrably achieves IP → 1 by evaluating all identity components in a single forward pass, with measurably different Δ-Kohärenz profiles compared to a standard autoregressive baseline on the same task.

---

## How to Contribute

If you identify a new open problem, or have a proposed solution for an existing one, please:
1. Open an issue on the [repository](https://github.com/frnkptrln/systems-and-intelligence)
2. Reference the specific problem number
3. Distinguish between theoretical arguments and empirical evidence
