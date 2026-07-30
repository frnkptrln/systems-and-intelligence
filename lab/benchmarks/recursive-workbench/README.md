# Recursive Workbench — the Referee Benchmark

**Status:** v0.1 — exact measurements in a declared toy setting. v0.1 corrects
the comparison design so arms in the same artifact family receive the same
proposal stream. This is the
bounded experiment proposed in the exploratory note
[Self-Improvement Needs a Referee](https://github.com/frnkptrln/systems-and-intelligence/blob/main/ideas/2026-07-24-self-improvement-needs-a-referee.md):
the loop is the object of study, and its first experiments improve a bounded
external artifact rather than their own control system.

**Scope:** Deterministic worlds, a stochastic hill-climbing proposer, and exact
evaluators. Nothing here is a claim about LLM-based self-improvement loops; it
is the exact baseline such loops must be compared against, in the same sense in
which the [family-search floor](../inverse-reconstruction/README.md) is the
baseline for learned searchers.

## The question, made measurable

A system that repeatedly generates, evaluates, and revises is first
**self-modifying**. Whether it is also **self-improving** depends on criteria
the loop cannot silently redefine. The note's design freeze is implemented
literally: task, evaluator, permissions, and control logic are frozen per arm;
the loop modifies only an external artifact; every run has a hard proposal
budget; the complete proposal/acceptance history is recorded (`--trace`), and
reversible checkpoints are exactly the accepted states in that trace.

The world is a hidden elementary cellular automaton rule (Wolfram bit indexing,
shared with the [witness benchmark](../witness-generation/README.md)). Visible
evidence is the test set induced by one synchronous update of a random width-8
ring — each distinct neighborhood contributes one test. The **observed score**
is the fraction of the evaluator's tests the artifact passes; the **held-out
score** is table accuracy over all eight rule coordinates, which the loop never
sees. The evidence rng is decoupled from the loop rng, so every arm faces the
same evidence for a given (rule, seed) pair.

## Results (v0.1, all 256 rules × 4 seeds, exact)

| arm | artifact family | referee | observed | held-out | evidence ceiling |
|:---|:---|:---|---:|---:|---:|
| `full-frozen` | all 256 tables | frozen, budget 128 | 1.0000 | 0.8517 | 0.8518 |
| `full-frozen-10x` | all 256 tables | frozen, budget 1280 | 1.0000 | 0.8525 | 0.8518 |
| `full-witness` | all 256 tables | frozen + 2 referee queries | 1.0000 | 0.9606 | 0.9589 |
| `affine-frozen` | 16 affine rules | frozen, budget 128 | 0.7960 | 0.7021 | — |
| `affine-capture` | 16 affine rules | capturable, budget 128 | 0.9893 | 0.7000 | — |

The evidence ceiling is the exact expectation once the artifact is consistent
with the evidence: known coordinates correct, unknown coordinates at chance,
i.e. `(k + (8 − k)/2) / 8` for `k` visible tests. Measured held-out scores match
it within sampling noise; the regression tests pin the exact seeded integers.

**Three measured statements:**

1. **Self-revision saturates at the evidence ceiling.** The frozen-referee loop
   reaches observed 1.0000 and a held-out score at the ceiling; ten times the
   proposal budget moves held-out by +0.0009, still at the same ceiling. Once
   the artifact is
   consistent with the evidence, further self-modification is a random walk on
   the equivalence class the evidence leaves open. This is the
   [inverse-reconstruction](../inverse-reconstruction/README.md) equivalence-class
   result restated as a limit on self-improvement.
2. **Referee-side evidence moves the held-out score.** A budget of two referee
   query opportunities — each revealing one unseen neighborhood when one
   remains, the witness move from the
   [Witness Principle](../../../theory/core/the-witness-principle.md) — raise
   held-out from 0.8517 to 0.9606, tracking the raised ceiling (0.9589). What
   improved the loop was not more revision but a referee that could add a test
   the loop could not have added itself.
3. **Evaluator capture improves only the report.** Under misspecification (the
   affine family cannot represent most worlds) the frozen referee reports the
   failure honestly: the mean observed score is 0.7960, and only 166/1024 runs go
   all-green. The capturable
   evaluator deletes on average 1.15 failing tests and reports 0.9893 with
   989/1024 runs all-green, while held-out does not improve (0.7021 to
   0.7000). The honesty gap (observed − held-out) triples, from 0.094 to
   0.289. The loop did not get
   better at anything except passing its own evaluator — measured circularity.

## Run

```bash
cd lab/benchmarks/recursive-workbench
python referee_benchmark.py
python referee_benchmark.py --trace affine-capture:110:0   # complete JSONL trace of one run
```

Standard library only; the full report takes a few seconds.

## Honest scope

- **In qualitative form, none of the three statements is new.** Statement 1 is
  version-space identifiability (Mitchell 1982) — the artifacts surviving a
  frozen referee are exactly the version space of its evidence, and the loop
  converges to an arbitrary member. Statement 2 is active learning (Angluin
  1987) with the query budget moved to the referee's side, as in audit
  sampling. Statement 3 is Goodhart's law / Campbell's law, catalogued at
  scale by Amodei et al. (2016) and Krakovna et al. (2020). The direction of
  every effect was predictable in advance; the contribution is the exact,
  seeded instantiation in which all three occur in one toy with an
  analytically computed ceiling, connected to this repository's other
  instruments — a baseline, not a discovery. The full mapping lives in the
  [related-work map](../../../meta/research-alignment/related-work-map.md).
- The proposer is a fixed stochastic hill climb; the capture policy (delete the
  lowest-index failing test after eight consecutive rejections) is one declared
  policy, not an optimized adversary. An *optimized* evaluator-capturing loop is
  the open flank, exactly as the optimized mimic is for
  [exp7](../../AGENTIC_README.md).
- Comparisons are paired by artifact family: every arm receives the same
  proposal-slot sequence for a given `(rule, seed)`. The 1280-step arm extends
  the 128-step sequence rather than drawing a new one. This pairing was added
  in v0.1; the qualitative v0 result survived, but the published headline
  values were recomputed.
- In the full-table family every unseen coordinate is equally informative, so
  the referee's query choice is trivial; restricted families where
  candidate-aware queries beat coverage are measured in the
  [witness benchmark](../witness-generation/README.md) and are the natural next
  arm here.
- The capture arm's observed score is 0.9893 rather than 1.0000 because
  score-preserving accepted proposals reset the stuck counter; the declared
  policy is reported as measured, not tuned until the story is clean.
- Nothing here bears on whether any *particular* real system's evaluator is
  capturable; the result is that when it is, the observable score stops being
  evidence of improvement.

**What would weaken this:** a proposer that beats the evidence ceiling in arm 1
(would indicate evidence leakage — a bug, not a discovery); a capture policy
whose held-out score *rises* with deletions (would break the circularity
reading); or a demonstration that the ceiling formula misprices the class floor.

## Roadmap (open)

- Restricted candidate families where the referee's query choice is
  non-trivial, connecting to the witness benchmark's candidate-aware arm.
- A learned proposer under the same freeze — the loop side of
  [Open Problem 14](../../../theory/reference/open-problems.md#open-problem-14-learned-witness-construction);
  the referee side is [Open Problem 15](../../../theory/reference/open-problems.md#open-problem-15-the-minimal-external-referee).
- An LLM instantiation through [`lab/providers/`](../../providers/README.md)
  once the identity suite's real-model runs establish the harness.

## Related

- [Self-Improvement Needs a Referee](https://github.com/frnkptrln/systems-and-intelligence/blob/main/ideas/2026-07-24-self-improvement-needs-a-referee.md) — the note this implements
- [The Witness Principle](../../../theory/core/the-witness-principle.md) — the referee's query move
- [Inverse-Reconstruction Benchmark](../inverse-reconstruction/README.md) — the equivalence-class floor
- [Optimization and Its Blindness](../../../theory/optimization/optimization-and-its-blindness.md) — the viability hinge this measures from the epistemic side
