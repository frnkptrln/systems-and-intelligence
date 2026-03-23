# Part 2: Measuring the Mind

If intelligence is a property of continuous dynamical systems, how do we measure it without relying on discrete benchmarks like MMLU or HumanEval?

This repository proposes moving away from measuring *knowledge retrieval* toward measuring **structural integrity**.

---

## The System Intelligence Index (SII)

The [SII Framework](../theory/system-intelligence-index.md) evaluates a system across four dimensions, each normalized to $[0,1]$:

| Dimension | Symbol | Measures | Score 0 | Score 1 |
|:----------|:-------|:---------|:--------|:--------|
| **Predictive Power** | $P$ | Accuracy of internal model vs. environment | Random guessing | Perfect tracking |
| **Regulation** | $R$ | Stability under perturbation | Unbounded drift | Zero-variance maintenance |
| **Adaptation** | $A$ | Recovery after regime shift | No recovery | Instant re-convergence |
| **Identity Persistence** | $\text{IP}$ | Simultaneous co-instantiation of governing constraints | Time-multiplexed (Arpeggio) | All operative (Chord) |

$$\text{SII} = P \times R \times A \times \text{IP}$$

The multiplicative form is deliberate: a zero in any dimension collapses the overall score. A system that predicts perfectly but cannot regulate ($R = 0$) has SII = 0. A system that predicts, regulates, and adapts but has no unified identity ($\text{IP} = 0$) has SII = 0 — it is a sophisticated tool, not a system with integrated intelligence.

The [SII Dashboard](../data-analysis/sii_dashboard.py) runs headless mini-simulations and generates comparative radar charts across all four dimensions.

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

The [Identity Morphospace](../tools/morphospace_visualizer.py) plots agent trajectories in the IP/Coherence plane, revealing which agents maintain the Chord state under stress and which fragment into Arpeggio.

---

## The Agentic Test Suite

To push these metrics into practice, we built the [Agentic Test Suite](../agentic-test-suite/README.md). It empirically tests the difference between a "stateless" prompt-response loop and a "stateful" agent:

- **3-Layer Memory Architecture**: Logs → Curated Memory → Distilled Principles
- **Δ-Kohärenz (Ω)**: Measures how coherently an agent's self-representation changes over time — distinguishing *development* (directional evolution) from *noise* (random fluctuation) from *mirroring* (static resonance)
- **Observer Divergence**: Tests whether two different observers interacting with the same agent produce measurably different developmental trajectories — probing the relational emergence of identity

We no longer ask "Is this AI smart?" We ask: "Does this AI maintain structural coherence over time — and does all of its identity sound at once?"
