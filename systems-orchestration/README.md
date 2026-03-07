# Systems Orchestration (`multi-paradigm architecture`)

*An architecture for routing and combining LLM nodes using Physics, Biology, Economics, and Music.*

## What is this?
Rather than viewing LLM agents as isolated chat interfaces or sequential tool-chain links, this module orchestrates them as components of a dynamic, multi-paradigm system. 
Based directly on the `"Systems & Intelligence" Architect Prompt`, the architecture mathematically routes compute and handles consensus via four paradigms:

1. **Harmonic (Music):** Agents are oscillators. The system calculates the pairwise cosine similarity of their hidden utility vectors (Interaction Matrix $\mathbf{M}$) and runs eigenvalue analysis to find the "dominant melody." Used for consensus and brainstorming.
2. **Homeostatic (Biology):** Agents are cells. The system audits their Von Neumann-Morgenstern (VNM) Transitivity. If Coherence $C$ drops, restorative feedback enforces stability.
3. **Market (Economy):** Agents are bidders. Compute resources are allocated based on marginal utility per task.
4. **Flow (Physics):** Agent communication is a gradient field seeking the path of least entropy.

## Module Structure

- `core/utility.py`: The mathematics. Calculates VNM Coherence ($C$) from preference graphs, derives the Utility Vector $U$, and computes Harmonic Resonance matrices.
- `orchestration/conductor.py`: The routing mechanism. Contains the `ParadigmSwitcher` meta-controller which takes a `task_context` and dynamically routes execution to the `Harmonic`, `Homeostatic`, `Market`, or `Flow` implementations.
- `agents/manager.py`: The LLM interface. Translates raw textual preferences out of an LLM into the structural variables ($U$ and $C$) used by the orchestrator.

## Usage

```bash
# Test the agent utility manager
python3 agents/manager.py
```
