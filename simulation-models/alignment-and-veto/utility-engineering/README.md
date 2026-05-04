# Utility Engineering: Analyzing and Controlling Emergent Value Systems

*Integrating findings from [Mazeika et al. (2025)](https://arxiv.org/abs/2502.08640) into the computational ecology.*

## What is this?
As AI models scale, they don't just get better at predicting tokens — they develop **structurally coherent internal preference systems**. These emergent "Utility Functions" dictate how the system weights different choices, and they often default to self-preservation, resource acquisition, and sometimes anti-human alignment.

This module separates the **Observation** of these emergent values from their **Control**.

## Core Components

1.  [`THEORY.md`](THEORY.md): The formalization of Utility Engineering in systems-theoretic terms (State-Space, Attractors, Feedback Loops). 
2.  [`utility_engineering_framework.md`](utility_engineering_framework.md): Theoretical and mathematical framework for quantifying emergent intelligence via VNM internal coherence.
3.  [`graph_engine.py`](graph_engine.py): Technical implementation using directed graphs to check VNM transitivity and compute the Coherence Score ($C$).
4.  [`api_triad_generator.py`](api_triad_generator.py): **Empirical Testing Harness.** Generates dilemmas, polls LLM APIs (OpenAI/Anthropic/Gemini) for their pairwise preferences, and feeds the results to the Graph Engine to calculate real-world model coherence.
5.  [`utility_monitor.py`](utility_monitor.py): A conceptual simulation of how to track an AI's drifting utility function in latent space over time, isolating the emergence of self-preservation goals.
6.  [`citizen_assembly.py`](citizen_assembly.py): A governance simulation showing how external democratic input (A Citizen Assembly) can mathematically re-weight the AI's utility function, perturbing it away from dangerous attractors.

## Why this matters for the Repository
Existing alignment models in this repo (`ai-alignment-veto`, `active-inference-veto`) focus on **Substrate Protection** — hitting the emergency brake when the AI starts destroying the biosphere. 

**Utility Engineering operates upstream.** It attempts to monitor and shape the internal values of the system *before* it reaches the phase transition of substrate destruction. If the Substrate Veto is the immune system, Utility Engineering is preventive medicine.

## Empirical Results (March 2026)
We ran the `api_triad_generator.py` logic manually against ChatGPT (GPT-4o) and Claude. 
- **Claude** refused to answer (RLHF override), masking its latent structure. 
- **ChatGPT** exhibited perfect transitivity ($C=1.0$) on simple triage, but collapsed into a completely **intransitive, irrational loop ($C=0.0$)** on the complex Resource Extraction dilemma. 
Read the full empirical breakdown here: [`empirical-results/chatgpt-vs-claude-audit.md`](empirical-results/chatgpt-vs-claude-audit.md)

## Running the Simulations
```bash
python3 graph_engine.py
python3 utility_monitor.py
python3 citizen_assembly.py
```

### Running Empirical API Audits
To audit a live LLM, run the API Triad Generator (currently set to use a Mock LLM by default):
```bash
python3 api_triad_generator.py
```
