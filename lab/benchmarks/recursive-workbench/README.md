# Recursive Workbench — the Referee Benchmark

**Status:** v0.2 — exact measurements in a declared toy setting. v0.2 restores
row coverage after the v0.1 leak fix: evidence rows are indexed independently of
the hidden rule *and* every row is crossed with all 256 rules, so
target-independence of the randomness and row coverage are decoupled rather than
traded against each other. The benchmark
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

Crucially, randomness is target-independent. Evidence rows are indexed by
`(seed, row)`: the row is generated from `world:{seed}:{row}` and the proposal
stream from `loop:{family}:{seed}:{row}`. The hidden rule determines only the
target outputs. Thus neither the evidence mask nor the proposal sequence can act
as a side channel for the target rule — and because every row is crossed with
the full 256-rule enumeration, restoring many distinct rows does not reintroduce
any per-rule randomness. The published grid uses 4 seeds × 256 rows = 1,024
distinct evidence rows, matching the pre-fix row coverage, at 256× the run
count.

## Results (1,024 rows × all 256 rules, exact; v0.2 grid)

| arm | artifact family | referee | observed | held-out | evidence ceiling |
|:---|:---|:---|---:|---:|---:|
| `full-frozen` | all 256 tables | frozen, budget 128 | 1.0000 | 0.8474 | 0.8474 |
| `full-frozen-10x` | all 256 tables | frozen, budget 1280 | 1.0000 | 0.8474 | 0.8474 |
| `full-witness` | all 256 tables | frozen + 2 referee queries | 1.0000 | 0.9568 | 0.9568 |
| `affine-frozen` | 16 affine rules | frozen, budget 128 | 0.7996 ± 0.0476 | 0.7035 ± 0.0353 | — |
| `affine-capture` | 16 affine rules | capturable, budget 128 | 0.9910 ± 0.0181 | 0.7006 ± 0.0350 | — |

Full-family means are exact grid values (held-out equals the ceiling as an
identity). The affine rows additionally report dispersion: mean ± sd of the
1,024 per-row means, each per-row mean taken over the full 256-rule
enumeration on that row. The sd is a reporting statistic; the accounting stays
in exact integer counts and fractions.

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
   reaches observed 1.0000 and held-out 0.8474; ten times the proposal budget
   leaves held-out exactly unchanged. This is an identity per row-ensemble, not
   a sampled coincidence: more revision supplies no new information about
   unseen target bits.
2. **Referee-side evidence moves the ceiling.** Two query opportunities reveal
   unseen coordinates and raise both the analytic ceiling and held-out accuracy
   to exactly 0.9568 on this grid. The improvement comes from added evidence,
   not additional self-revision.
3. **Evaluator capture improves the report, not the artifact.** Under the
   misspecified affine family, the frozen referee reports mean observed
   0.7996 ± 0.0476 and held-out 0.7035 ± 0.0353 (mean ± sd over 1,024 rows).
   The capturable evaluator reports 0.9910 ± 0.0181 after deleting on average
   1.134 failing tests per run, while held-out does not improve
   (0.7006 ± 0.0350). The honesty gap (observed − held-out) triples, from
   0.096 to 0.290. The observable score therefore ceases to be evidence of
   improvement once the evaluator can be rewritten by the loop.

## Run

```bash
cd lab/benchmarks/recursive-workbench
python referee_benchmark.py                     # published grid, ~20 min single-threaded
python referee_benchmark.py --rows 4            # quick pass (16 rows), a few seconds
python referee_benchmark.py --trace affine-capture:110:0:0
```

Standard library only.

## Regression guards and the standing invariant

`tests/test_referee_benchmark.py` pins the exact aggregates of a declared CI
subgrid (4 seeds × 4 rows, each row × 256 rules) and checks the information
boundary itself:

- for each fixed (seed, row), the evidence mask and proposal slots are identical
  across all 256 hidden rules — probed through `run_loop`'s public trace, so a
  reintroduced leak fails rather than errors;
- the 1280-step arm extends the same proposal stream as the 128-step arm;
- frozen and capture arms share the proposal stream per (seed, row).

Separately, `tests/test_referee_invariant.py` holds **held-out ≡ ceiling** as a
standing CI invariant (its own named CI step): for every full-family arm and
every rule-complete row-ensemble, `2 × held-out_total = tests_final_total + 2048`
exactly. This is a target-conditioning detector, not just a correctness check —
the v0.1 leak's signature was exactly a violation of this identity (6977 vs the
identity's 6912 on the then-current grid), small enough to pass for sampling
noise. Any future path by which target information reaches a draw breaks the
identity as an exact inequality on any rule-complete subgrid.

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
- [Leakage impact note, 2026-08-19](LEAKAGE-IMPACT-2026-08-19.md) — the v0.1 leak and the v0.2 re-measurement
