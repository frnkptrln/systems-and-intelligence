# Part 2: Measuring the Mind

If intelligence is a property of continuous dynamical systems, how do we measure it without relying on discrete benchmarks like MMLU or HumanEval?

This repository proposes moving away from measuring *knowledge retrieval* toward measuring **structural integrity**.

---

## The System Intelligence Index (SII)

The [SII Framework](../theory/core/system-intelligence-index.md) evaluates a system across four dimensions, each normalized to $[0,1]$:

| Dimension | Symbol | Measures | Score 0 | Score 1 |
|:----------|:-------|:---------|:--------|:--------|
| **Predictive Power** | $P$ | Accuracy of internal model vs. environment | Random guessing | Perfect tracking |
| **Regulation** | $R$ | Stability under perturbation | Unbounded drift | Zero-variance maintenance |
| **Adaptation** | $A$ | Recovery after regime shift | No recovery | Instant re-convergence |
| **Identity Persistence** | $\text{IP}$ | Simultaneous co-instantiation of governing constraints | Time-multiplexed (Arpeggio) | All operative (Chord) |

$$\text{SII} = P \times R \times A \times \text{IP}$$

The multiplicative form is deliberate: a zero in any dimension collapses the overall score. A system that predicts perfectly but cannot regulate ($R = 0$) has SII = 0. A system that predicts, regulates, and adapts but has no unified identity ($\text{IP} = 0$) has SII = 0 — it is a sophisticated tool, not a system with integrated intelligence.

The [SII Dashboard](https://github.com/frnkptrln/systems-and-intelligence/blob/main/lab/data-analysis/sii_dashboard.py) runs headless mini-simulations and generates comparative radar charts across all four dimensions.

---

## Identity Persistence: The Fourth Dimension

The first three SII dimensions (P, R, A) measure *what* a system does. The fourth — Identity Persistence — measures *whether the system's governing principles are simultaneously operative* during action.

Consider an agent that:

1. Checks its safety constraints at time $t_1$
2. Pursues its goal at time $t_2$
3. Verifies value alignment at time $t_3$

This agent scores well on P, R, A — it can predict, regulate, and adapt. But no single compute step integrates all its governance. It is an **Arpeggio**: identity components sounding sequentially, never simultaneously.

The **Chord Postulate** (Perrier & Bennett, 2026) requires all governing components to be operative in a single compute step $\Delta t$:

$$\text{IP}(t) = \frac{|\mathcal{O}(t)|}{n}$$

where $\mathcal{O}(t)$ is the operative set and $n$ is the total number of governing components.

- $\text{IP} \to 1$: **Chord** — unified self, all constraints co-instantiated
- $\text{IP} \to 0$: **Arpeggio** — simulated self, constraints time-multiplexed

The [Identity Morphospace](https://github.com/frnkptrln/systems-and-intelligence/blob/main/lab/tools/morphospace_visualizer.py) plots agent trajectories in the IP/Coherence plane, revealing which agents maintain the Chord state under stress and which fragment into Arpeggio.

---

## Consciousness as Global Availability

This book does not need to solve consciousness to use the concept responsibly. The narrow question is architectural: when does local processing become globally available, integrated, self-referential, and behaviorally binding?

[Consciousness as Global Availability](../theory/identity/consciousness-as-global-availability.md) connects three external anchors to the repo's own metrics:

- Global Workspace: local signals become globally broadcast.
- Integrated Information: a system state is not reducible to independent parts.
- Active Inference / Markov Blankets: the system maintains a boundary while acting to preserve viable states.

This keeps consciousness from becoming a decorative claim. It becomes a testable design question: do private modules, broadcast modules, and chord-style integrated modules behave differently under perturbation?

---

## The Agentic Identity Suite

To push these metrics into practice, we built the [Agentic Identity Suite](../lab/AGENTIC_README.md). It empirically tests the difference between a "stateless" prompt-response loop and a "stateful" agent:

- **3-Layer Memory Architecture**: Logs → Curated Memory → Distilled Principles
- **Δ-Kohärenz (Ω)**: Measures how coherently an agent's self-representation changes over time — distinguishing *development* (directional evolution) from *noise* (random fluctuation) from *mirroring* (static resonance)
- **Observer Divergence**: Tests whether two different observers interacting with the same agent produce measurably different developmental trajectories — probing the relational emergence of identity

We no longer ask "Is this AI smart?" We ask: "Does this AI maintain structural coherence over time — and does all of its identity sound at once?"
