# Inverse-Reconstruction Benchmark (v0) — Trace → Generator, Measured

*The first runnable artifact on the inverse side of the project's spine: given N steps of trace, reconstruct the generator — with noise, observability, and coverage as dials.*

## Why this exists

[The Generator Question](../../../theory/core/the-generator-question.md) claims an asymmetry: forward (generator → trace) is cheap, inverse (trace → generator) is structurally hard. The repository demonstrates the forward direction ~26 times; until this benchmark, the inverse direction existed only as framing and a prompt-search scaffold. This benchmark turns the asymmetry from a claim into a **measurable curve** — and, in doing so, *sharpens* the claim (see "The honest finding" below).

## The three testbeds

Each testbed reuses one of the repo's own forward generators. In all three, the **model family is known** to the reconstructor — it lacks only parameters / rule bits. This is deliberately the standard *system-identification / SINDy* setting (Ljung 1999; Brunton, Proctor & Kutz 2016): the cheap regime, against which the dials measure where hardness actually enters.

| Testbed | Generator | Inverse method | Dials |
|---|---|---|---|
| **Kuramoto** | mean-field ODE, $\dot\theta_i = \omega_i + Kr\sin(\psi-\theta_i)$ | finite-difference $\dot\theta$, least squares on the known library $\{1,\, r\sin(\psi-\theta_i)\}$ → all $\omega_i$ and shared $K$ | angle noise; **observed fraction** (mean field then computed from the observed subset only — a biased field) |
| **Elementary CA** | one of the 256 Wolfram rules on a ring | tabulate neighborhood → successor, majority vote | bit-flip noise; **IC entropy** (a single-seed IC may never exercise some neighborhoods) |
| **Boids** | cohesion/alignment/separation with weights $(w_c, w_a, w_s)$ | velocities + accelerations by differencing **noisy positions**, features recomputed from the noisy state, least squares | position noise (double differencing amplifies it by $\sim 1/dt^2$) |

## Results (v0, seeds averaged)

```
KURAMOTO  — rel. error on K
  vs noise (full obs.):   σ=0: 0.0%   σ=0.03: 0.5%   σ=0.1: 5.2%   σ=0.3: 27%
  vs observed fraction:   f=1: 0.5%   f=0.6: 13%     f=0.3: 21%    f=0.15: 41%
CA        — rule-bit accuracy (observed bits), random IC
  p=0 … 0.2: 100%   p=0.3: 93%      (majority vote is noise-robust)
  single-seed IC:  rule 110: 8/8 seen → class 1;  rule 30: 8/8 → class 1
                   rule 90:  5/8 seen → consistent-generator CLASS SIZE 8
BOIDS     — rel. error on (w_c, w_a, w_s) from positions only
  σ=0: 3%   σ=0.003: 35%   σ=0.01: 226%   σ=0.03: 789%
```

![Inverse benchmark v0](../../tools/inverse_benchmark.png)

## The honest finding

**With a known family, full observability and clean data, inversion is cheap** — exact rule tables, sub-percent parameter errors. The benchmark therefore does *not* support a uniform "inverse is hard" reading. What it supports — measurably — is where hardness actually lives:

1. **Noise × differentiation** (Boids): observing *state* instead of derivatives means differencing, and differencing amplifies noise; recovery degrades from 3% to ~800% error within $\sigma = 0.03$.
2. **Partial observability** (Kuramoto): an unobserved part of the system biases the reconstructed mean field; error grows monotonically as coverage shrinks.
3. **Coverage / identifiability** (CA): a low-entropy trace may never exercise parts of the rule. Rule 90 from a single seed exposes only 5/8 neighborhoods — the remaining 3 bits are unidentifiable **in principle**, leaving a *consistent-generator equivalence class* of size $2^3 = 8$. No method, however clever, can do better than the class. This is [Open Problem 11](../../../theory/reference/open-problems.md)'s "equivalence class of viable generators", measured for the first time in this repo.
4. **Family search** (not in v0): the genuinely hard regime — recovering the generator when the *model class itself* is unknown — is the program-induction / open-ended symbolic-regression setting (Schmidt & Lipson 2009; Cranmer's PySR; Lake et al. 2015; Ellis et al. 2021). That is the v1 frontier.

This sharpens the spine rather than weakening it: the P≠NP framing of [The Generator Question](../../../theory/core/the-generator-question.md) is about the *search over candidate generators*, not about fitting parameters inside a family someone already handed you.

## v1, part 1 — the intervention experiment (run)

[`intervention_experiment.py`](intervention_experiment.py) answers the open thread raised in [Construction vs. Deduction](../../../theory/computation/construction-vs-deduction.md): **does the consistent-generator equivalence class collapse when observation is replaced by intervention?** Experiments are *queries*, not traces — the observer chooses states and makes the generator answer. Results:

- **CA (rule 90, single-seed start, class 8):** *passive* observation plateaus at class 8 **forever** — the orbit's neighborhood distribution is exhausted, more watching buys nothing. *One-bit flips* collapse the class within ~10 queries. A single *prepared state* (a de Bruijn row containing every neighborhood) collapses it to 1 **in one step**. The hierarchy is strict: watching < perturbing < preparing.
- **The frozen exception (rule 0, class 16):** on a dead background, a one-bit flip only produces the four neighborhoods already known — *single-bit interventions never collapse the class*. Only the prepared state does. **The deader the dynamics, the more structure the query itself must supply** — if the system's own dynamics carry no information, the experimenter's design must. (In TEO terms: a frozen system, $H \to 0$, is also epistemically opaque.)
- **Kuramoto on its locked attractor:** observing a *synchronized* system, $K$ is unidentifiable **in principle**, not for lack of data — in the locked state $\Omega = \omega_i + K r \sin(\psi - \theta_i)$ with all right-hand quantities constant, so every $K'$ has an $\omega_i'$ reproducing the trace exactly: a one-parameter generator family. Measured: passive error on $K$ ≈ 83% (noise-fitting); **one phase kick: 3%**; eight kicks: 0.3%.

**Reading.** Attractors hide generators: a relaxed system — synchronized, frozen, converged — is generator-degenerate, and no amount of passive observation resolves it. Facts about the generator can be *created* by intervention that observation alone cannot reach (the constructivist half) — though what the query exposes was the rule's content all along (the Platonist half). This is also the first-principles justification for an existing repo methodology: the identity instruments (Δ-Kohärenz, Observer Divergence) are **perturbation protocols** precisely because you cannot read a generator off an attractor — a system at rest, like a mirror at rest, reveals nothing but the room.

## Running

```bash
python inverse_benchmark.py              # v0: console summary, three testbeds (~10 s)
python inverse_benchmark.py --save       # also write the v0 figure (to lab/tools/)
python intervention_experiment.py        # v1.1: interventions vs. observation (~5 s)
python intervention_experiment.py --save # also write the intervention figure
```

Requires `numpy`, `matplotlib` only (repo `requirements.txt`).

## v1 roadmap (open)

*(Part 1 — interventions vs. observation — is done; see above. The items below remain open.)*

- **Family-search testbed**: a small DSL of update rules; reconstructor must find the family *and* the parameters (program induction; success vs. DSL size = the measurable wall).
- **Re-simulation divergence** as a behavioral metric (does the recovered generator *behave* identically, even when parameters differ?) — connects to the equivalence-class framing.
- **IFS testbed**: recover contractive affine maps from an attractor point cloud (hard even with known family — no time ordering).
- Cross-method comparison: hand-rolled least squares (v0) vs. SINDy/PySR as external baselines (would add dependencies; deliberately out of v0).

## Related

- [The Generator Question](../../../theory/core/the-generator-question.md) — the spine; this benchmark is its first inverse-direction artifact.
- [Open Problems](../../../theory/reference/open-problems.md) — Open Problem 11 (bounded inverse reconstruction).
- [Related Work Map](../../../meta/research-alignment/related-work-map.md) — SINDy / system identification / program induction anchors.
- [`lab/experiments/trace_to_generator/`](../../experiments/trace_to_generator/) — the earlier inverse-prompting scaffold.
