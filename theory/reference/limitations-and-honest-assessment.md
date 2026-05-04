# Limitations, Honest Assessment & Future Directions

*An honest accounting of what this project is, what it isn't, and where it must go.*

---

## What This Project Is

This repository is a **synthesis project**. It takes established mathematical tools from separate disciplines — game theory (1944), network science (1975), thermodynamics, control theory — and applies them to the emerging problem of multi-agent AI alignment.

The contribution is not novel mathematics. It is a **novel diagnosis**: that AI alignment is fundamentally a complex systems control problem, not a natural language processing problem, and that the tools to address it already exist in physics, biology, and economics.

## What This Project Is Not

We do not claim to have invented:

- **The VNM Utility Theorem** — Von Neumann & Morgenstern, 1944. Our Coherence Score $C$ is a standard transitivity coefficient applied to directed preference graphs, a technique used in sociometry since the 1970s.
- **PageRank centrality** — Page & Brin, 1998. Our derivation of the Utility Vector $U$ via the dominant eigenvector of a stochastic matrix is standard linear algebra.
- **Cosine similarity** — The "Harmonic Resonance" between agent vectors is the most elementary measure in vector mathematics.
- **The Kuramoto Model** — Kuramoto, 1975. Our synchronization dynamics are borrowed directly from nonlinear physics.
- **The Replicator Equation** — Taylor & Jonker, 1978. Our market dynamics are textbook evolutionary game theory.

Each individual component is well-established. The claim of this project is that their **coupling** — into a single dynamical system governing both AI ecologies and human civilizations — is new and useful.

## The Central Open Question

> **Does an LLM actually behave like a rational VNM agent?**

Our framework assumes that by querying an LLM pairwise, we extract genuine "preferences" that reveal an underlying utility function. This assumption is questionable:

- A Transformer has no internal "utility function." It has attention weights and learned distributions.
- Pairwise responses may reflect **training data statistics** filtered through RLHF, not coherent goals.
- The same model may yield different preference orderings depending on prompt framing, temperature, or context window — violating the stability assumptions of VNM theory.

Our Coherence Score $C$ may therefore measure **RLHF consistency** rather than **emergent rationality**. This distinction is critical and remains empirically unresolved.

## The Tensor Logic Horizon

Recent work by Pedro Domingos (2025) on **Tensor Logic** demonstrates that logical deduction and neural network operations are mathematically isomorphic. If this architecture matures:

- Our *external* Coherence Score $C$ could become unnecessary — logical consistency would be guaranteed *internally* by the network weights.
- The Multi-Paradigm Orchestrator would shift from a *corrective* role (fixing broken agents) to a *coordinative* role (managing healthy agents with competing goals).

This does not invalidate our framework. It evolves it. If Tensor Logic matures into a practical architecture with strong internal consistency guarantees, it could reduce the need for some *single-agent* external alignment scaffolding. Our orchestration architecture is aimed at *multi-agent* coordination dynamics; the two directions are plausibly complementary rather than competing.

## What Must Come Next

1. **Empirical validation**: Running the API Triad Generator against live commercial models (GPT-4, Claude, Gemini) to produce real $C$-Scores rather than theoretical ones.
2. **TEO simulation**: Numerically solving the coupled ODE system (Replicator + Kuramoto + Homeostatic + Entropy) and calibrating it against real-world data (CO₂ trajectories, Gini coefficients).
3. **Peer review**: Submitting the formal paper to arXiv and inviting critical feedback from the alignment research community.

## References

1. Domingos, P. (2025). *Tensor Logic.* Preprint.
2. Mazeika, M. et al. (2025). *Utility Engineering.* Preprint.
