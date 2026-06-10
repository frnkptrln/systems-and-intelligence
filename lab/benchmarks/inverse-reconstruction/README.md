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

## Running

```bash
python inverse_benchmark.py            # console summary, all three testbeds (~10 s)
python inverse_benchmark.py --save     # also write the figure (to lab/tools/)
```

Requires `numpy`, `matplotlib` only (repo `requirements.txt`).

## v1 roadmap (open)

- **Family-search testbed**: a small DSL of update rules; reconstructor must find the family *and* the parameters (program induction; success vs. DSL size = the measurable wall).
- **Re-simulation divergence** as a behavioral metric (does the recovered generator *behave* identically, even when parameters differ?) — connects to the equivalence-class framing.
- **IFS testbed**: recover contractive affine maps from an attractor point cloud (hard even with known family — no time ordering).
- Cross-method comparison: hand-rolled least squares (v0) vs. SINDy/PySR as external baselines (would add dependencies; deliberately out of v0).

## Related

- [The Generator Question](../../../theory/core/the-generator-question.md) — the spine; this benchmark is its first inverse-direction artifact.
- [Open Problems](../../../theory/reference/open-problems.md) — Open Problem 11 (bounded inverse reconstruction).
- [Related Work Map](../../../meta/research-alignment/related-work-map.md) — SINDy / system identification / program induction anchors.
- [`lab/experiments/trace_to_generator/`](../../experiments/trace_to_generator/) — the earlier inverse-prompting scaffold.
