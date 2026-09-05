# Collective Agency Benchmark

**Status:** preregistration draft — full benchmark not implemented; separate exact calibration controls are available  
**Question:** When does a collection become an agent?

This benchmark asks a bounded systems question. It does **not** attempt to decide whether a collective is conscious, has phenomenal experience, or is ontologically irreducible. It tests whether a declared collective description gains predictive and interventionally useful structure beyond matched component-wise descriptions.

## 1. Target distinction

A coordinated collection is not automatically a collective agent. The benchmark separates at least four regimes:

1. **independent components** — little coupling and no stable macro-organization;
2. **coordinated collection** — coupling improves task performance but predictive/control structure remains local or centrally imposed;
3. **joint-information regime** — joint state carries information unavailable from components individually; this alone does not establish causal integration;
4. **candidate collective agent** — collective organization additionally supports stable macro-level prediction/control under perturbation.

These are candidate distinctions, not a demonstrated progression: joint information can occur under uncoupled dynamics, and robust readout need not involve repair. The [exact calibration controls](../../experiments/collective-agency-control/README.md) make these limits explicit.

Viability is measured separately. A tightly integrated system may be powerful and persistent while becoming brittle, uncorrectable, or resource-unstable.

## 2. Experimental family

Use the same local component class while varying organization rather than raw component capability. Candidate factors:

- number of components;
- coupling strength and topology;
- communication bandwidth and latency;
- private versus shared memory;
- fixed versus adaptive connectivity;
- local versus shared goals;
- centralized coordinator versus distributed coupling;
- resource and action budgets;
- environmental shock rate;
- membership replacement or dropout.

The first implementation should use a synthetic dynamical system or small agent ecology whose complete state is observable. Language-model agents are a later validation target, not the first testbed.

## 3. Candidate measurements

No single metric is constitutive. Each addresses a different question.

### 3.1 Component predictive power

For component `i`, estimate how much its current state predicts its own or the system's next state under a declared estimator and horizon.

Purpose: establish the component-wise baseline.

### 3.2 Collective predictive gain

Compare prediction from a declared macro/collective state against matched component-wise and centralized-summary baselines. Report held-out log loss or another preregistered proper score.

A macro representation counts as useful only if its gain survives matched capacity and information budgets. A difference between joint and best-single mutual information is a separate diagnostic: it is neither a PID definition nor evidence of an advantage over an equally informed centralized predictor.

### 3.3 Synergistic predictive information

Use Partial Information Decomposition or a justified approximation to estimate information about the system's own next state that is available only from components jointly rather than separately.

This is inspired by uncommon self-knowledge, but the benchmark treats synergy as an architectural diagnostic, not a consciousness criterion.

Declare the target, source partition, source order and every measured pair, not only an average. The candidate's adjacent-pair PID measures two-source structure; zero pairwise synergy cannot exclude information available only from three or more sources. The [three-of-three static control](../../experiments/collective-agency-control/README.md#information-distribution-and-known-erasures) has zero target information in every pair and full target information in the triple. Its coalition decoding profile is not a replacement for a higher-order PID or for the benchmark's temporal estimator.

### 3.4 Information closure / NTIC candidate

Measure where predictive organization is localized under a declared partition into component and context states. Ikegami et al.'s NTIC work motivates this axis.

Important boundary: the published Tetrahymena result studies situated individual autonomy inside a coupled community; stronger claims about negative NTIC identifying collective agency should be tested rather than assumed. The exact estimator, conditioning variables, finite-sample correction, and PID formalism must be frozen before implementation.

### 3.5 Macro intervention / downward-control gain

Define at least one realizable macro intervention and compare its downstream local effects with matched micro-level perturbations.

A macrovariable that only compresses microstate but adds no interventionally useful prediction does not satisfy the stronger macro-agency criterion used here.

### 3.6 Viability

Track resource use, recovery after shocks, concentration of control, correction bandwidth, and other Viable Corridor quantities already defined elsewhere in the repository.

Agency and viability are separate axes. A pathological singleton is an admissible outcome: high integration and control with poor survivability or correctability.

Distinguish preservation of the chosen readout, reconstruction from surviving components, and restoration of the perturbed component state. Compare perturbed and unperturbed successors at the same horizon; a stable macro reading alone does not demonstrate repair. Declare the perturbation class (known erasure, unknown error, replacement, or transient state perturbation), report loss locations separately, and identify which source subsets retain the target information where feasible. Do not call a decoder's erasure tolerance system self-maintenance or general viability.

## 4. Controls

At minimum include:

- **independent control:** identical components without coupling;
- **broadcast control:** shared information without joint constraint formation;
- **centralized aggregator:** a single coordinator with the same information budget as the distributed system;
- **synchronization control:** strong coupling that produces trivial lockstep dynamics;
- **random-coupling control:** matched communication volume without adaptive organization;
- **capacity-matched control:** additional compute or memory without organizational change.

These controls are intended to prevent coordination, bandwidth, or raw capacity from being mistaken for collective agency.

### Existing exact calibration controls

Two executable controls now share [one result page](../../experiments/collective-agency-control/README.md#reading-the-controls-together):

- **Predictive parity:** equal joint and macro temporal information across uncoupled, locally repairing and cross-group-repairing rules; majority readout remains correct even when no component errors are repaired.
- **Information distribution:** broadcast, essential-component, two-of-three and three-of-three encodings separate joint-over-single gain, pairwise PID, minimal reconstructing coalitions and known-erasure tolerance.

Use these as interpretation checks, not as substitutes for the six budget-matched controls above. They use different targets, partitions and perturbations and must not be pooled into one agency score. Neither runs the proposed oscillator benchmark or confirms H1–H5.

## 5. Preregistered candidate hypotheses

### H1 — Synergy without agency is possible

Some coupled systems will show positive synergistic predictive information without macro intervention gain. If observed, synergy is diagnostic but not sufficient.

### H2 — Coordination and collective agency dissociate

Task performance can improve before predictive responsibility or control shifts to the collective level.

### H3 — Macro-agency requires an intervention advantage

Candidate collective-agent regimes should show a reproducible held-out effect of realizable macro interventions beyond matched micro perturbations and summary-only baselines.

### H4 — Agency and viability dissociate

Increasing integration can increase predictive/control concentration while reducing resilience, correction bandwidth, or recovery after shocks.

### H5 — Closure may create a new operational level

If an organizational transition produces a new macrostate with stable predictive and control value under membership perturbation, treat that as evidence for a new effective level — not for ontological irreducibility.

## 6. Failure conditions

The benchmark framing weakens if:

1. all apparent collective effects vanish after capacity, bandwidth, and centralization controls;
2. macro predictive gain disappears out of sample;
3. macro interventions add no effect beyond matched micro perturbations;
4. synergy or NTIC-like quantities are dominated by estimator choice or finite-sample bias;
5. the claimed phase boundary moves arbitrarily with coarse-graining;
6. the same label is applied to trivial synchronization and adaptive collective organization;
7. functional results are promoted to claims about phenomenal experience;
8. a pairwise null is used to rule out all higher-order joint information;
9. macro readout preservation or static reconstruction is counted as active component repair.

## 7. Reporting shape

Report a profile rather than a binary verdict:

| Axis | Question |
|---|---|
| Local prediction | How much future structure remains component-local? |
| Collective gain | Does a macro/collective representation improve held-out prediction? |
| Synergy | At which declared source order is predictive information available only jointly? |
| Closure | Where is predictive organization localized under the declared partition? |
| Downward control | Do macro interventions change later local dynamics beyond controls? |
| Persistence | Which source subsets and readouts survive each declared loss or perturbation, and do components actually recover? |
| Viability | Does the organization remain resource-stable, recoverable, and correctable? |

The benchmark should not collapse these dimensions into one scalar until evidence shows that such a reduction preserves the distinctions that matter.

## 8. Source boundary and related work

The design is motivated by several external proposals but does not inherit their consciousness claims:

- Takashi Ikegami, Hiroki Kojima & Akiko Kashiwagi (2026), *Community First Theory: How Collective Organization Generates Individual Diversity*, Entropy 28(5):523, DOI `10.3390/e28050523` — NTIC and situated autonomy in Tetrahymena.
- Krti Tallam (2026), *Consciousness as Uncommon Self-Knowledge: A Synergistic Information Framework*, arXiv:`2605.13884` — self-directed synergistic information as a candidate operational criterion.
- Michael Levin's multiscale collective-intelligence work — motivates separating macro goal/control descriptions from local cellular dynamics.
- Armando Vieira & Liane Gabora (2026), *Autocatalytic Constraint Closure as an Organizational Principle for Machine Consciousness*, DOI `10.1609/aaaiss.v8i1.42568` — RAF closure as a candidate organizational transition.

For this repository, these are inputs to a test of collective organization, not evidence that any tested system is conscious.

## 9. Next implementation decision

Before code is written, freeze:

1. one fully observable synthetic system;
2. one macro-state construction rule;
3. one prediction score;
4. one PID/synergy estimator;
5. the exact NTIC definition and conditioning variables;
6. one realizable macro intervention plus matched micro controls;
7. viability variables and perturbation schedule;
8. null thresholds and seed count.

Only after those choices are fixed should the first executable benchmark be added.

Options for each of the eight, with the existing code they would reuse and a recommended default, are collected in [`freeze-options.md`](freeze-options.md) (2026-09-03; nothing frozen there).

Those defaults are now transcribed into [`freeze-candidate.json`](freeze-candidate.json) for review. The candidate is machine-checked by `freeze_contract.py`, keeps all six maintainer questions explicit, and sets both implementation and execution authorization to `false`; it is not a preregistration freeze.

The calibration controls refine measurement interpretation only. They do not change `freeze-candidate.json`, resolve its open implementation choices, or authorize its execution.

## Related

- [When Does a Collection Become an Agent?](../../../ideas/2026-09-03-when-does-a-collection-become-an-agent.md)
- [Collective Self-Knowledge May Require Synergy](../../../ideas/2026-09-03-collective-self-knowledge-may-require-synergy.md)
- [Macro Agency Needs Downward Control](../../../ideas/2026-09-03-macro-agency-needs-downward-control.md)
- [Closure Can Open a New Possibility Space](../../../ideas/2026-09-03-closure-can-open-a-new-possibility-space.md)
- [Open Problems](../../../theory/reference/open-problems.md)
- [Machine Consciousness as Generator Coherence](../../../theory/identity/machine-consciousness-as-generator-coherence.md)
