# Lab

**Status:** Directory index, corrected 2026-09-02. Until then this README described only the multi-paradigm orchestration package, which is now one section below.

`lab/` is the executable side of the repository: benchmarks with frozen headlines, bounded experiments, metrics, the validators and build tools that CI runs, provider adapters, and the orchestration package. The benchmark result pages are published on the site; the machinery that produces them lives here. Bounded means: prediction and failure condition committed before the result, results in new files, a test that pins the headline (the rule is [Information Architecture §1.F](../meta/repository-meta/repository-information-architecture.md#f-lab-simulation-models-executables)).

## What is here

| Path | What it holds |
|:---|:---|
| `benchmarks/` | The benchmark suites, each with a README that is its result page: [inverse-reconstruction](benchmarks/inverse-reconstruction/README.md) (v0–v1.13), [witness-generation](benchmarks/witness-generation/README.md), [situated-stack](benchmarks/situated-stack/README.md), [constraint-release](benchmarks/constraint-release/README.md), [recursive-workbench](benchmarks/recursive-workbench/README.md) (the referee benchmark), [learned-searcher](benchmarks/learned-searcher/README.md) (protocol frozen, not run), [collective-agency](benchmarks/collective-agency/README.md) (preregistration draft, not implemented), [cognitive-stress-tests](benchmarks/cognitive-stress-tests/README.md) (scenario suite, not yet run), [teo-framework](benchmarks/teo-framework/README.md) (a superseded early stub, kept as history), and the top-level script `minimal_teo_benchmark.py`, which compares a naive maximizer with the constrained agent from `core/minimal_agent.py`. |
| `experiments/` | Bounded experiments: the Agentic Identity Suite scripts `exp1`–`exp3` and `exp5`–`exp8` (indexed in [`AGENTIC_README.md`](AGENTIC_README.md)), plus `exp4_coupling_phase_transition.py` and `mirror_problem.py`, which that index lists only briefly, [active_identifiability](experiments/active_identifiability/README.md), [context-attractor](experiments/context-attractor/README.md), [identity_abduction](experiments/identity_abduction/README.md), [trace_to_generator](experiments/trace_to_generator/README.md), [trace_to_generator_small](experiments/trace_to_generator_small/README.md), and the five bounded experiments with committed result files, [persistence_narrowing](experiments/persistence_narrowing/README.md), [representation_reconstruction](experiments/representation_reconstruction/README.md), [decision_layer](experiments/decision_layer/README.md), and [collective-agency-control](experiments/collective-agency-control/README.md) (exact parity control; macro prediction versus coupling and repair), plus [coherence_margin](experiments/coherence_margin/README.md) (synchronization onset versus a required coherence floor). [witness_machine](#witness-machine-interface) adds a model-free ProblemSpec/proposal/referee interface with exact ECA controls. `config.yaml` holds the Agentic Identity Suite and provider configuration. |
| `metrics/` | Identity Persistence, Δ-Kohärenz, persistence scores, Generative Surprise (normalized, with the historical product retained for its regression test), embedding distance, observer attribution. |
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


## Witness Machine interface

**Status: model-free interface and exact controls, 10 October 2026.** This implements the next bounded step from the Witness Machine handover. It does not train a generator or run the frozen [Learned Searcher](benchmarks/learned-searcher/README.md) protocol. Its registration and 100 tasks remain unchanged.

The question is operational: given competing deterministic ECA rules, existing observations, legal interventions and a measurement map, construct one experiment, then compare its prediction with a separately supplied target process. A response outside every candidate is **family failure**.

### Run the complete local demonstration

Python 3.10+; standard library only. From the repository root:

```bash
python lab/experiments/witness_machine/demo.py --output /tmp/witness-machine-first-run
pytest tests/test_witness_machine.py tests/test_witness_benchmark.py tests/test_learned_searcher.py -q
```

The output directory must not already exist. Ten open control problems run with three proposers: one random legal query, budgeted randomized enumeration, and lexicographic enumeration. Each of the 30 episodes invokes the proposer and referee in **separate Python processes**. Files include the public problem, an explicitly open demonstration target, frozen proposal, receipt and summary. No API calls, downloads, training or credentials are involved.

For an individual problem from that output:

```bash
python lab/experiments/witness_machine/witness_machine.py propose \
  --spec /tmp/witness-machine-first-run/pair/problem.json \
  --strategy budgeted --seed 42 --out /tmp/new-proposal.json

python lab/experiments/witness_machine/witness_machine.py referee \
  --spec /tmp/witness-machine-first-run/pair/problem.json \
  --proposal /tmp/new-proposal.json \
  --target /tmp/witness-machine-first-run/pair/open-demo-target.json \
  --out /tmp/new-receipt.json
```

Output files are created exclusively. Reusing a filename fails without replacing its bytes.

### Contract

| Component | Implemented behavior |
|---|---|
| `ProblemSpec` | Immutable candidate rules, positive integer prior weights, prior observations, width, baseline, writable cells, observed cells, update steps, exact/at-most cost, proposal simulation budget and separate world budgets. Contains no target identity. |
| Candidate simulator | Predicts declared candidates only. Every rule/query simulation, including filtering prior observations, costs one call. A simulation includes the declared number of updates. |
| Proposal | Query, per-candidate predictions, induced partition, actual declared intervention cost, simulation count, examined queries and stop reason. Frozen before the world response. |
| Referee | Independently checks problem binding, legality, cost, predictions and partition. Evaluates the same primary objective over the full legal query family. Executes the target only after validation and budget checks. |
| Receipt | Proposal hash, source/baseline hashes, survivors or family failure, exact frontier, lexicographic regret, separately reported proposer/referee work, and world spending. Includes the next observation for an explicitly constructed follow-up problem. |

Queries prepare a binary ring. Cost is Hamming distance from the declared baseline; locked cells cannot change. The observation map projects the successor after one to four updates onto an ordered subset of cells, which may be empty. Width is bounded to 3–12 to keep exhaustive auditing tractable.

The primary score is lexicographic `(worst remaining class size, expected remaining class size, cost)`, with row order used only as a deterministic tie-break. Expected size uses the declared prior conditioned on existing evidence, computed as an exact rational. Under uniform weights it is the original sum of squared block sizes divided by candidate count. Regret reports the first worse objective component; equally scored alternative rows have zero regret.

The query-cost convention and world budget are distinct. A legal cost-three proposal can exceed a remaining world budget of two. A zero-cost intervention still consumes one world query. Prior observations are given evidence, not newly charged world executions. A referee instance tracks spending within one episode; this is not a persistent account across CLI invocations or an adaptive policy evaluator.

### Results of the open controls

The committed [summary](experiments/witness_machine/results/open-controls.json) contains 30 actual local executions. For exhaustive enumeration:

| Control | Result |
|---|---|
| Pair `{0,128}`, exact cost 3 | `00000111`; both candidates separated. |
| Same pair, exact cost 2 | No informative legal query; remaining class size 2. |
| `{0,64,128,192}`, exact cost 3 | Same candidate-aware witness identifies all four. |
| All 256 rules, exact cost 4 | `00010111`; universal identification. |
| Empty measurement map | Two candidates remain observationally indistinguishable. |
| `{0,1}`, zero cost | Identified after one world query with zero intervention cost. |
| Target outside the declared pair | `family_failure`, zero survivors. |
| Prior evidence already outside the family | `family_failure` before any new world query. |
| Only two proposal simulation calls | One query examined; no exhaustive-search claim. |
| Width 5, nonzero baseline, two writable cells, two measured cells, two updates | Legal optimum at cost 1; worst remaining size 2, expected size 7/5. The particular open target is identified, which is weaker than universal identification. |

Regression tests also recover all five original full-family frontier values `128,16,8,2,1`; compare restricted geometry against a separate string-based update; check weighted priors, evidence filtering, budget boundaries, forged proposals, save-file exclusivity and target-independent CLI handoff. The original exact Witness Benchmark and frozen Learned Searcher tests run alongside these controls.

### Evidence and limits

All problems and targets here are open fixtures selected with knowledge of the original benchmark. These are implementation controls, not a new preregistration, blind test, training result or transfer finding. Random is one deterministic seeded draw per problem; this demonstration is not a statistically powered algorithm comparison. When enough calls are available, both search strategies enumerate the same legal family and must agree on its optimum.

Process separation makes the input handoff explicit. It **does not** protect target files from a hostile process running as the same user. A blind evaluation needs an independently controlled target service or filesystem boundary and a documented information policy. Hashes bind bytes; they are not execution attestations. Reported proposer compute is measured by the supplied implementation, but cannot be independently verified for an externally submitted proposal. The referee's exhaustive audit cost is always separate and is not free proposer access.

The model family remains deterministic ECA. No hypothesis generation from raw traces, stochastic tolerance relation, information-gain/VOI objective, learned proposer, cross-family generalization, hardware experiment or distributed execution is implemented. Full external model evaluation remains subject to its separate execution registration.

The next research design is in [the transfer design](#next-experiment-construction-under-changing-access). It is a proposal for a later experiment, not a retroactive registration of these controls.

### Next experiment: construction under changing access

**Design proposal, 10 October 2026. No model selected, trained or evaluated.** The implementation controls in this directory were developed with access to their answers.

First task: construct a query from a **given candidate family**, using the same budgeted candidate simulator as every baseline. Candidate generation from traces remains a separate task. The target identity and future answer must be served only to an independently controlled referee.

Before training or drawing evaluation targets, register the generator, training budget, information access, split assignment, model identity, seed policy, primary score and failure treatment in a new experiment. Preserve the existing Learned Searcher first-contact protocol as its own experiment.

#### Proposed split axes

1. Training: width-eight, one-update rings, zero baseline and complete observation; multiple candidate relations rather than copies of the `111` trap.
2. Validation: disjoint candidate relations under the same interface, including impossible and zero-cost witnesses.
3. Access holdout: fixed declared families under previously withheld writable/observed masks and nonzero baselines.
4. Dynamics holdout: different widths and multi-update observations. This tests a changed ECA task, not transfer beyond cellular automata.
5. Representation controls: candidate renaming, query-coordinate remapping and equivalent surface encodings; success here is equivariance, not new-dynamics transfer.

These axes alone do not guarantee structural separation. Before freezing a split, enumerate each finite task's achievable candidate partitions and minimum realization costs; check train/test overlap modulo the declared candidate and coordinate symmetries. Count repeated structure once in the primary analysis. A graph-isomorphism or equivalent canonicalization check must itself be validated. No such automatic split certificate is claimed by the current code.

#### Matched comparisons

Compare a learned direct proposer, a learned predictor with search, random legal queries, budgeted search and an exhaustive oracle under the same stated objective. Charge candidate-simulator calls for evidence filtering and all query evaluation; separately report training, data generation, runtime and memory. The exact referee frontier is evaluator-only access. An information-gain arm can be a diagnostic, never a replacement oracle for the declared minimax objective.

Report legal-query rate, abstention, family failure and lexicographic regret as separate quantities. For successful queries also report actual remaining class size and world spending. Use multiple predeclared independent task structures and seeds; repeated surface variants are paired controls. Specify confidence intervals and sample size before outcome inspection.

Stop conditions include exhausted proposal/world budgets and empty candidate families. An unsuccessful bounded search cannot certify impossibility; the independent exhaustive frontier can certify it only within the declared finite interface. A useful negative result is parity with budgeted search after accounting for training and simulation costs.

The current author and supplied controls are informed. A future blind test needs fresh task construction and an information boundary that was not available during implementation.
