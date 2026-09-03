# Collective Agency Benchmark — Options for the Eight Freeze Decisions

**Status:** Options for the maintainer's eight freeze decisions — nothing frozen, no implementation.
**Prepared:** 2026-09-03, for §9 of [`README.md`](README.md); every option keeps the boundary in [Information Architecture §1.F](../../../meta/repository-meta/repository-information-architecture.md#f-lab-simulation-models-executables) (deterministic, toy-scale, no model agents, no self-revising loop).

The benchmark asks whether a declared collective description gains predictive and interventionally useful structure beyond matched component-wise descriptions, and reports a profile (local prediction, collective gain, synergy, closure, downward control, persistence, viability) rather than a scalar. It must not decide consciousness, phenomenal experience, or ontological irreducibility; it must survive the §4 controls; and it fails if synergy or closure quantities are dominated by estimator choice or move arbitrarily with coarse-graining (§6). Every option below keeps the repository boundary: deterministic given a seed, numpy or standard library, toy-scale, no model agents, no self-revising loop.

Survey summary. Seeded, importable and fast today: `kuramoto_forward` (RK4, N=20, 2000 steps, 0.24 s, repeat run bit-identical), `ca_forward` (exact, 0.00 s) and `boids_forward` (0.34 s) in `inverse_benchmark.py`; `agent_budget_sim.run_once` (seeded, returns flags, not trajectories); `teo_simulation.run` (scipy `solve_ivp`, adaptive steps, ~0.6 s). Not usable as-is: `coupled_oscillators.py`, `boids.py`, `nested_emergence_demo.py` (interactive or scipy loops), `nested_emergence.py`, `cognitive_breathing.py` (unseeded), `symbiotic_breathing.py` (no components), `lab/core/minimal_agent.py` (no dynamics). `info_measures.py` has histogram entropy, MI, transfer entropy and active information storage via a `count_entropy` row-hash pattern; no PID, synergy or NTIC code exists in the repository, and its `scipy.special.digamma` import is unused.

## 1. One fully observable synthetic system

- **1A Kuramoto graph.** `kuramoto_forward` extended with an adjacency matrix `A_ij` (the form of TEO eq. 2 in `teo_simulation.py`), N=16, K and topology (all-to-all, ring, seeded random with matched degree) as the §2 organization dials. Reuses `kuramoto_forward`, `order_parameter`. ~40 new lines; 0.2 s per 2000-step run. Measurable: every §3 axis; the synchronization control is the K≫K_c arm. Risk: continuous phases must be binned for every information quantity.
- **1B Elementary CA ring.** `ca_forward` with a per-cell coupling probability p (neighbourhood rule with probability p, own one-input rule otherwise, seeded). ~30 lines; exact, milliseconds. Measurable: plug-in estimators on a binary alphabet without binning bias; all 256 rules enumerable as in `referee_benchmark.py`. Risk: p is not a dial the README lists, and the macro state is only a coarse-graining, so failure condition 5 is the whole result.
- **1C Agent ecology.** `agent_budget_sim.run_once` re-implemented to return `(w_t, Ω_t, H_t)`. ~60 lines; milliseconds. Measurable: viability natively. Risk: coupling only through the population mean and H, i.e. already the centralized-aggregator control; no topology dial.

**Default: 1A.** It has a macro variable the model itself defines, a continuous coupling dial with a known incoherent/coherent boundary, and stays deterministic in well under a second.

## 2. One macro-state construction rule

- **2A Order parameter.** Macro state = `(r, ψ)` from `order_parameter`, binned (8 bins each). 5 lines. Risk: one complex number, so capacity matching is easy but the "collective" is trivially the mean field.
- **2B Block order parameters.** Components partitioned by index into b blocks; macro state = `(r_b, ψ_b)` for b ∈ {1, 2, 4}; b=1 is 2A. 15 lines. Measurable: failure condition 5 directly, by reporting each quantity at every b.
- **2C Fitted linear summary.** Top-2 principal components of `[cos θ, sin θ]`, fitted on training seeds only. 20 lines. Risk: fit leakage into held-out seeds unless seeds are split before fitting.

**Default: 2A reported at 2B's three levels**, since 2B contains 2A and the coarse-graining sweep is a declared failure condition.

## 3. One prediction score

- **3A Discretized held-out log loss.** Next-state bin of θ_i (8 bins) predicted from a count table conditioned on the predictor's binned state, Laplace-smoothed, fitted on training seeds, scored in bits on held-out seeds. Reuses the `count_entropy` pattern in `info_measures.transfer_entropy`. 40 lines. Risk: the bin count is arbitrary; 8 is a declared choice.
- **3B Gaussian log score of a least-squares predictor** on `(cos θ, sin θ)`, as in `kuramoto_inverse`. 40 lines. Risk: residuals are not Gaussian near r≈0.
- **3C Squared circular error** `1 − cos(θ̂ − θ)`. 5 lines. Risk: proper for the mean only.

**Default: 3A**, because it shares one alphabet and one count table with the PID and NTIC estimators, so §3.2, §3.3 and §3.4 cannot disagree through discretization.

## 4. One PID/synergy estimator

- **4A Two-source plug-in decomposition, redundancy = minimum specific information.** Sources: a pair of components (i, j), binned; target: next macro bin (2A) or next θ_i bin. Redundancy = expectation over the target of the minimum over the two sources of the specific information; synergy = joint MI − both uniques − redundancy. Averaged over adjacent pairs. 60 lines, `collections.Counter` or numpy. Risk: plug-in bias grows with alphabet size; kept at 8 bins, ≥2000 samples per seed.
- **4B Co-information only:** `I(S_i, S_j; T) − I(S_i; T) − I(S_j; T)`. 20 lines. Measurable: sign of net synergy minus redundancy. Risk: cannot separate the two; §3.3 asks for synergy.
- **4C 4A plus shuffle surrogates:** time-permute one source (seeded), 20 surrogates, report plug-in minus surrogate mean. +15 lines; ×20 estimator runtime.

**Default: 4A with 4C's correction**, because the README names finite-sample bias as a failure condition and 4C is the cheapest way to show it was measured.

## 5. Exact NTIC definition and conditioning variables

The candidate quantity for a partition (system X, context E), one-step horizon, binned states: `I(X_{t+1}; X_t) − I(X_{t+1}; X_t | E_t)`, computed from the same counts as item 3, contemporaneous `E_t` only.

- **5A Component versus rest.** X = θ_i; E = the order parameter of the other N−1 (the situated-individual reading the README says the published result actually studies). Averaged over i; 30 lines.
- **5B Collective versus exogenous drive.** X = macro state (2A); E = the perturbation signal of item 7 (a declared external input). 10 more lines. Measurable: whether closure sits at the collective level at all.
- **5C Block versus rest**, X = block b's `(r_b, ψ_b)`, E = the other blocks (aligns with 2B). 10 more lines.

**Default: 5A primary, 5B alongside**, from the same count tables, because the README separates the published individual-level result from the untested collective-level extension.

## 6. One realizable macro intervention plus matched micro controls

- **6A Phase contraction (state reset).** At t₀: `θ_i ← ψ + (1−λ)(θ_i − ψ)` for all i, λ=0.5, which changes r by a computable amount. Micro controls with the same displacement budget `Σ|Δθ_i|`: (i) random-direction kicks to the same oscillators, (ii) the whole budget on one oscillator, (iii) the contraction on a random half. Outcome: held-out log loss (3A) of local next states over [t₀, t₀+h]. 50 lines. Risk: above K_c any rise in r is followed by faster locking, so only the micro-matched comparison is informative, never the raw effect.
- **6B External field pulse.** Add `h·sin(ψ_ext − θ_i)` for τ steps through the coupling channel; micro control: independent fields with random `ψ_i` of equal summed magnitude. 40 lines. A dynamical term rather than a reset.
- **6C Coupling change.** K raised for τ steps; micro control: the same total edge-weight change on one oscillator's edges. 30 lines. Intervenes on organization, not state.

**Default: 6A**, because the intervened variable is exactly the declared macro state and the displacement budget gives an exact matching rule; 6B if the maintainer requires interventions to be dynamical terms.

## 7. Viability variables and perturbation schedule

- **7A TEO margins.** V2 coherence margin `r − r_min` (V1/V3 only with 1C or the TEO ODE), as in `viability_report` in `teo_simulation.py`. 10 lines. Risk: for 1A only V2 applies.
- **7B Recovery and membership.** Recovery time to within ε of pre-shock r after (i) phase scramble of fraction f ∈ {0.1, 0.25}, (ii) dropout of k ∈ {1, N/4} components removed from the mean field, (iii) replacement of k components with new seeded ω. Fixed schedule at t ∈ {T/4, T/2, 3T/4}. 50 lines. Measurable: the persistence row of §7 directly.
- **7C Agent-ecology flags** (monopoly, collapse, `Ω/S_max`) — only with 1C.

**Default: 7B with 7A's coherence margin.** "Correction bandwidth" and "concentration of control" have no implementation in the repository that I found; they would be new definitions.

## 8. Null thresholds and seed count

- **8A Control-arm null.** Threshold for every quantity = maximum over seeds of that quantity in the K=0 arm (§4's independent control). Zero extra cost; the null is a declared arm, matching the workbench style of exact arms rather than statistics.
- **8B Surrogate null** from 4C: threshold = surrogate mean + 3 sd. Estimator cost ×20.
- **8C Exact enumeration** (1B only): all 256 rules × fixed ICs, exact means as in `referee_benchmark.py`.

**Default: 8A as the threshold, 8B as the bias report.** Seeds: 16 per cell (8 train, 8 held-out); grid K ∈ {0, ½K_c, K_c, 2K_c, 4K_c} × 3 topologies = 240 forward runs (~1 min) plus intervention arms and estimators, under 10 CPU-minutes; CI subgrid 1 seed × 3 K values pinned by a test as in `tests/test_persistence_narrowing.py`; a dated smoke record as in `results/smoke-2026-09-02.md`.

## Out of scope here

Language-model agents (§2 defers them); the unseeded or scipy-bound simulations named in the survey as testbeds; the TEO ODE unless re-integrated with fixed-step RK4; estimators with tuned bandwidths, nearest-neighbour or learned mutual-information estimators, and PID definitions that require an optimization over distributions; any loop that re-selects the macro variable, bin count or intervention after seeing results.

## Open questions for the maintainer

1. Is scipy acceptable in `lab/` code, or must the new module avoid it (and should the unused import in `info_measures.py` go)?
2. Does a state reset (6A) count as "realizable", or must the intervention be a dynamical term (6B)?
3. Continuous testbed with binning (1A) or discrete testbed with exact counts (1B) first?
4. Which coarse-graining levels b are reported: {1, 2, 4} or {1, 4} only?
5. One-step horizon only, or horizons {1, 10} for prediction and NTIC?
6. Drop "correction bandwidth" and "concentration of control" from the first implementation, since no definition exists in code?

## Sources read

- `lab/benchmarks/collective-agency/README.md`
- `ideas/2026-09-03-when-does-a-collection-become-an-agent.md`
- `ideas/2026-09-03-collective-self-knowledge-may-require-synergy.md`
- `ideas/2026-09-03-macro-agency-needs-downward-control.md`
- `ideas/2026-09-03-closure-can-open-a-new-possibility-space.md`
- `lab/experiments/representation_reconstruction/README.md`
- `lab/experiments/persistence_narrowing/README.md`
- `lab/experiments/persistence_narrowing/results/smoke-2026-09-02.md`
- `tests/test_persistence_narrowing.py`
- `lab/benchmarks/recursive-workbench/README.md`
- `lab/benchmarks/inverse-reconstruction/inverse_benchmark.py` (forward models; timed)
- `simulation-models/alignment-and-veto/agent-ecology/README.md`, `agent_budget_sim.py`
- `simulation-models/emergent-dynamics/coupled-oscillators/README.md`, `coupled_oscillators.py`
- `simulation-models/social-computation/nested-emergence-demo/README.md`, `nested_emergence.py`, `nested_emergence_demo.py`
- `simulation-models/social-computation/symbiotic-breathing/README.md`, `symbiotic_breathing.py`
- `simulation-models/emergent-dynamics/boids-flocking/README.md`, `boids.py`
- `simulation-models/social-computation/cognitive-breathing-network/README.md`, `cognitive_breathing.py`
- `simulation-models/alignment-and-veto/teo-civilization/README.md`, `teo_simulation.py` (docstring, parameters, structure), `separability_grid.py` (header)
- `simulation-models/social-computation/rhythm-locks/README.md`, `stigmergy-swarm/README.md`, `emergent-dynamics/self-organized-criticality/README.md` (skimmed)
- `lab/core/minimal_agent.py`, `constraints.py`, `utility.py`
- `lab/data-analysis/info_measures.py`, `analyse_emergence.py` (header)
- `lab/tools/viable_corridor.py` (header), `lab/benchmarks/teo-framework/README.md`
- `papers/viable-corridor.md` (grep for V1–V3 and the named viability terms)
- `requirements.txt`, `requirements-dev.txt`
