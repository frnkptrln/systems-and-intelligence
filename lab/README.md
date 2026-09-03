# Lab

**Status:** Directory index, corrected 2026-09-02. Until then this README described only the multi-paradigm orchestration package, which is now one section below.

`lab/` is the executable side of the repository: benchmarks with frozen headlines, bounded experiments, metrics, the validators and build tools that CI runs, provider adapters, and the orchestration package. The benchmark result pages are published on the site; the machinery that produces them lives here. Bounded means: prediction and failure condition committed before the result, results in new files, a test that pins the headline (the rule is [Information Architecture §1.F](../meta/repository-meta/repository-information-architecture.md#f-lab-simulation-models-executables)).

## What is here

| Path | What it holds |
|:---|:---|
| `benchmarks/` | The benchmark suites, each with a README that is its result page: [inverse-reconstruction](benchmarks/inverse-reconstruction/README.md) (v0–v1.13), [witness-generation](benchmarks/witness-generation/README.md), [situated-stack](benchmarks/situated-stack/README.md), [constraint-release](benchmarks/constraint-release/README.md), [recursive-workbench](benchmarks/recursive-workbench/README.md) (the referee benchmark), [learned-searcher](benchmarks/learned-searcher/README.md) (protocol frozen, not run), [collective-agency](benchmarks/collective-agency/README.md) (preregistration draft, not implemented), [cognitive-stress-tests](benchmarks/cognitive-stress-tests/README.md) (scenario suite, not yet run), [teo-framework](benchmarks/teo-framework/README.md) (a superseded early stub, kept as history), and the top-level script `minimal_teo_benchmark.py`, which compares a naive maximizer with the constrained agent from `core/minimal_agent.py`. |
| `experiments/` | Bounded experiments: the Agentic Identity Suite scripts `exp1`–`exp3` and `exp5`–`exp8` (indexed in [`AGENTIC_README.md`](AGENTIC_README.md)), plus `exp4_coupling_phase_transition.py` and `mirror_problem.py`, which that index lists only briefly, [active_identifiability](experiments/active_identifiability/README.md), [context-attractor](experiments/context-attractor/README.md), [identity_abduction](experiments/identity_abduction/README.md), [trace_to_generator](experiments/trace_to_generator/README.md), [trace_to_generator_small](experiments/trace_to_generator_small/README.md), and the two bounded experiments with committed result files, [persistence_narrowing](experiments/persistence_narrowing/README.md) and [representation_reconstruction](experiments/representation_reconstruction/README.md). `config.yaml` holds the Agentic Identity Suite and provider configuration. |
| `metrics/` | Identity Persistence, Δ-Kohärenz, persistence scores, embedding distance, observer attribution. |
| `tools/` | The validators and build tools CI runs (`validate_links.py`, `validate_nav.py`, `validate_math.py`, `validate_katex.js`, `audit_repository_freshness.py`, `build_paper_pdf.py`, `mkdocs_repo_links.py`), the benchmark and paper figures, the web explorer, and helper scripts; see [`tools/README.md`](tools/README.md). |
| `providers/` | Provider adapters (Anthropic, mock) behind one factory; see [`providers/README.md`](providers/README.md). |
| `agents/` | The baseline mirror agent, the three-layer agent, and the manager that translates model output into the orchestration variables. |
| `core/`, `orchestration/` | The multi-paradigm orchestration package described below. |
| `data-analysis/`, `dashboard/`, `data/` | Emergence analysis and information measures ([`data-analysis/README.md`](data-analysis/README.md)), the SII dashboards, and session data. |
| `live_demo.py`, `paradigm_wars.py` | Demonstration entry points for the orchestration package. |

Tests live at the repository root in `tests/`. They pin the benchmark headlines, the corridor paper's appendix values, the held-out == ceiling invariant of the referee benchmark, and the validators themselves; CI runs `pytest tests/` together with the validators in `tools/` on every push. New results go to new files; a pinned number does not change.

## Multi-paradigm orchestration (`core/`, `orchestration/`, `agents/manager.py`)

*An architecture for routing and combining LLM nodes using Physics, Biology, Economics, and Music.*

Rather than viewing LLM agents as isolated chat interfaces or sequential tool-chain links, this package orchestrates them as components of a dynamic, multi-paradigm system. The architecture routes compute and handles consensus via four paradigms:

1. **Harmonic (Music):** Agents are oscillators. The system calculates the pairwise cosine similarity of their hidden utility vectors (Interaction Matrix $\mathbf{M}$) and runs eigenvalue analysis to find the "dominant melody." Used for consensus and brainstorming.
2. **Homeostatic (Biology):** Agents are cells. The system audits their Von Neumann-Morgenstern (VNM) Transitivity. If Coherence $C$ drops, restorative feedback enforces stability.
3. **Market (Economy):** Agents are bidders. Compute resources are allocated based on marginal utility per task.
4. **Flow (Physics):** Agent communication is a gradient field seeking the path of least entropy.

Module structure:

- `core/utility.py`: The mathematics. Calculates VNM Coherence ($C$) from preference graphs, derives the Utility Vector $U$, and computes Harmonic Resonance matrices.
- `orchestration/conductor.py`: The routing mechanism. Contains the `ParadigmSwitcher` meta-controller which takes a `task_context` and dynamically routes execution to the `Harmonic`, `Homeostatic`, `Market`, or `Flow` implementations.
- `agents/manager.py`: The LLM interface. Translates raw textual preferences out of an LLM into the structural variables ($U$ and $C$) used by the orchestrator.

To see the multi-paradigm architecture in action, run the live demonstration script. It spins up three virtual LLM agents (with diverging utility functions) and routes tasks dynamically between the Harmonic, Homeostatic, Market, and Flow paradigms:

```bash
python3 live_demo.py
```
