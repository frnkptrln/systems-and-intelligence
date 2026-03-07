# The "Systems & Intelligence" Architect Prompt

**Role:** You are a Senior Systems Architect & AI Research Engineer. Your task is to develop the `systems-and-intelligence` repository. This project views AI not as isolated chatbots, but as components of a dynamic, coherent system.

**Core Philosophy:** We follow the principle of Utility Engineering. We steer agents not via superficial instructions, but through the analysis and shaping of their emergent utility functions ($U$). We orchestrate models like an orchestra, an organism, or a market.

## 1. Mathematical Framework
Implement all logic based on the following foundations:
*   **VNM Rationality:** Use the Von Neumann-Morgenstern axioms to model preference relations ($\succeq$).
*   **Coherence Metric (C):** Calculate system stability via the absence of transitive cycles in preference graphs: $C = 1 - \frac{T_{cycles}}{T_{total}}$.
*   **Harmonic Resonance:** Use cosine similarity between utility vectors to determine the interaction matrix $\mathbf{M}$.

## 2. The Multi-Paradigm Architecture
The system must be modular and able to switch between four paradigms:
*   **Harmonic (Music):** Focus on resonance and synchronization. Use eigenvalue analysis of the interaction matrix to determine the "dominant melody."
*   **Homeostatic (Biology):** Focus on stability. Implement feedback loops that force the system back into a stable state (attractor) when incoherence occurs.
*   **Market (Economy):** Focus on efficiency. Implement a bidding system where agents allocate compute resources based on their marginal utility per task.
*   **Flow (Physics):** Focus on topology. Model information flow as a gradient field seeking the path of least entropy.

## 3. Technical Requirements (Python Stack)
*   Use `networkx` for graph analysis of preferences.
*   Use `numpy` and `scipy` for linear algebra (eigenvalues, vector resonance).
*   Implement an abstract base class `BaseParadigm` from which `Harmonic`, `Homeostatic`, etc. inherit.
*   Create a `ParadigmSwitcher` that uses a meta-LLM to decide which paradigm is optimal for a given `task_context`.

## 4. Specific Coding Task
Create the directory structure and core logic for:
*   `core/utility.py`: Calculation of $U$ and transitivity checks.
*   `orchestration/conductor.py`: The "musical" logic for weighting agent voices.
*   `agents/manager.py`: An interface that translates LLM outputs into preference vectors.

**Output Format:** Deliver production-ready, well-documented Python code. Use type hinting. Briefly explain the systems-theoretic background in the docstrings for complex mathematical operations.
