# Recursive Workbench — the Referee Benchmark

**Status:** v0.1 — exact measurements in a declared toy setting. The benchmark
implements the bounded experiment proposed in [Self-Improvement Needs a
Referee](../../../ideas/2026-07-24-self-improvement-needs-a-referee.md): the loop
is the object of study, and it improves a bounded external artifact rather than
its own control system.

**Scope:** deterministic hidden ECA rules, a stochastic hill-climbing proposer,
and exact evaluators. Nothing here is a claim about LLM-based self-improvement
loops; this is a baseline such loops can be compared against.

## The question, made measurable

A system that repeatedly generates, evaluates, and revises is first
**self-modifying**. Whether it is also **self-improving** depends on criteria the
loop cannot silently redefine. Task, evaluator, permissions, and control logic
are frozen per arm; every run has a hard proposal budget; and the complete
proposal/acceptance history can be recorded with `--trace`.

The world is a hidden elementary cellular automaton rule (Wolfram bit indexing).
Visible evidence is induced by one synchronous update of a random width-8 ring:
each distinct neighborhood contributes one test. The **observed score** is the
fraction of evaluator tests passed; the **held-out score** is table accuracy over
all eight rule coordinates.

Crucially, randomness is target-independent. For a fixed seed the evidence row
is generated from `world:{seed}`, and for a fixed artifact family the proposal
stream is generated from `loop:{family}:{seed}`. The hidden rule determines only
the target outputs. Thus neither the evidence mask nor the proposal sequence can
act as a side channel for the target rule.

## Results (all 256 rules × 4 seeds, exact)

| arm | artifact family | referee | observed | held-out | evidence ceiling |
|:---|:---|:---|---:|---:|---:|
| `full-frozen` | all 256 tables | frozen, budget 128 | 1.0000 | 0.84375 | 0.84375 |
| `full-frozen-10x` | all 256 tables | frozen, budget 1280 | 1.0000 | 0.84375 | 0.84375 |
| `full-witness` | all 256 tables | frozen + 2 referee queries | 1.0000 | 0.96875 | 0.96875 |
| `affine-frozen` | 16 affine rules | frozen, budget 128 | 0.7897 | 0.6968 | — |
| `affine-capture` | 16 affine rules | capturable, budget 128 | 0.9953 | 0.6914 | — |

For the unrestricted family, if `k` rule coordinates are visible, the exact
conditional expectation without further target information is

`(k + (8 - k)/2) / 8`.

Because the random streams and evidence mask are independent of the hidden rule,
full enumeration of all 256 rules now realizes that expectation **exactly**, not
merely within sampling tolerance. Once the artifact fits the evidence, accepted
flips of unseen coordinates form a lazy random walk over the evidence-equivalent
hypercube; flips that break visible coordinates are rejected.

**Three measured statements:**

1. **Self-revision saturates exactly at the evidence ceiling.** `full-frozen`
   reaches observed 1.0000 and held-out 0.84375; ten times the proposal budget
   leaves held-out exactly unchanged at 0.84375. More revision supplies no new
   information about unseen target bits.
2. **Referee-side evidence moves the ceiling.** Two query opportunities reveal
   unseen coordinates and raise both the analytic ceiling and held-out accuracy
   to exactly 0.96875. The improvement comes from added evidence, not additional
   self-revision.
3. **Evaluator capture improves the report, not the artifact.** Under the
   misspecified affine family, the frozen referee reports mean observed 0.7897
   and held-out 0.6968. The capturable evaluator reports 0.9953 after deleting
   1,252 failing tests across 1,024 runs, while held-out falls slightly to
   0.6914. The observable score therefore ceases to be evidence of improvement
   once the evaluator can be rewritten by the loop.

## Run

```bash
cd lab/benchmarks/recursive-workbench
python referee_benchmark.py
python referee_benchmark.py --trace affine-capture:110:0
```

Standard library only.

## Regression guards

`tests/test_referee_benchmark.py` checks the exact seeded aggregates and, more
importantly, the information boundary itself:

- for each fixed seed, the evidence mask is identical across all 256 hidden rules;
- proposal slots are independent of the hidden rule;
- the 1280-step arm extends the same proposal stream as the 128-step arm;
- after all unrestricted frozen runs fit their visible evidence, full 256-rule
  ensemble held-out accuracy equals the analytic evidence ceiling exactly;
- the witness arm likewise equals its raised ceiling exactly.

These guards make target-dependent randomness a regression failure rather than a
small numerical discrepancy that could be mistaken for sampling noise.

## Honest scope

The qualitative effects are standard: version-space identifiability, active
learning, and Goodhart/Campbell-style evaluator failure. The contribution here is
an exact, seeded instantiation that connects those effects in one toy benchmark.
The proposer remains a fixed stochastic hill climb; the capture policy is one
declared policy rather than an optimized adversary; and nothing here establishes
that any particular real-world evaluator is capturable.

A proposer that beats the unrestricted evidence ceiling without new evidence
would now indicate leakage or another bug, not a discovery.

## Related

- [Self-Improvement Needs a Referee](../../../ideas/2026-07-24-self-improvement-needs-a-referee.md)
- [The Witness Principle](../../../theory/core/the-witness-principle.md)
- [Inverse-Reconstruction Benchmark](../inverse-reconstruction/README.md)
- [Optimization and Its Blindness](../../../theory/optimization/optimization-and-its-blindness.md)
