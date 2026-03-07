# Part 2: Measuring the Mind

If intelligence is a property of continuous dynamical systems, how do we measure it without relying on discrete benchmarks like MMLU or HumanEval?

This repository proposes moving away from measuring *knowledge retrieval* toward measuring **structural integrity**. 

## The Systemic Intelligence Index (SII)
The [SII Dashboard](../data-analysis/README.md) uses information theory to evaluate a system across four dimensions:
1. **Predictive Capacity (P)**: The system's ability to minimize surprise (Free Energy Principle).
2. **Resilience (R)**: The system's ability to maintain homeostasis under perturbation.
3. **Autonomy (A)**: The system's independence from its immediate inputs (Markov Blankets).
4. **$\Delta$-Coherence ($\Omega$)**: The stability of the system's identity vector over time.

## The Agentic Test Suite
To push these metrics into practice, we built the [Agentic Test Suite](../agentic-test-suite/README.md).

It empirically tests the difference between a "stateless" prompt-response loop and a "stateful" agent. By implementing a 3-Layer Memory Architecture, we observe that identity coherence ($\Omega$) rises exponentially compared to flat storage. 

We no longer ask "Is this AI smart?" We ask "Does this AI maintain structural coherence over time?"
