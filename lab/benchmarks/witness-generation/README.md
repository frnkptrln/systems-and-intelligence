# Witness-Generation Benchmark — Candidate Class → Distinguishing Query

**Status:** exact finite baseline

*Given a declared candidate class and an intervention budget, can an observer construct a
low-cost query under which the candidates disagree?*

## Why this exists

The [inverse-reconstruction
benchmark](../inverse-reconstruction/README.md) already measures a strict hierarchy in
selected toy systems: passive watching can plateau, local perturbations can shrink the
candidate class, and a designed preparation can identify the rule in one step.

Those interventions were supplied by the experimenter. This benchmark makes their
construction explicit. It is the first finite instrument for the
[Witness Principle](../../../theory/core/the-witness-principle.md).

## Declared problem

| Component | Declaration |
|:---|:---|
| candidate family | all 256 elementary cellular-automaton rule tables |
| query | prepare one binary ring row of width 8 |
| outcome | observe the complete successor row |
| reference state | the all-zero row |
| query cost | Hamming distance from the reference state |
| primary score | largest candidate block remaining after the query |
| secondary score | expected remaining class size under a uniform prior |
| generator | exhaustive search over every row at the declared cost |
| baseline | exact mean over all rows at the same cost |

The generator is exact enumeration, not a learned model. It establishes the finite floor
that a learned system must match before claims about reusable witness construction become
interesting.

## Run

```bash
cd lab/benchmarks/witness-generation
python witness_benchmark.py
```

The code uses only the Python standard library.

## Exact result

| preparation cost | queries enumerated | neighborhoods exposed by best query | worst-case class after best query | mean class after an equal-cost query |
|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 128 | 128.00 |
| 1 | 8 | 4 | 16 | 16.00 |
| 2 | 28 | 5 | 8 | 11.43 |
| 3 | 56 | 7 | 2 | 5.71 |
| 4 | 70 | 8 | 1 | 5.71 |

At cost four the best row is `00010111`, a cyclic de Bruijn sequence for three-bit
neighborhoods. It exposes all eight rule-table entries in one update, so every outcome
block is a singleton. An unstructured equal-cost row leaves 5.71 candidates on average.

The result isolates the contribution of **query arrangement**. At cost one every possible
query is rotationally equivalent, so structured and unstructured selection tie. The gap
appears only when the same number of prepared bits can be arranged in more or less
discriminating patterns.

## Pairwise witness profile

For every unordered pair of distinct ECA rules, the benchmark also finds the cheapest row
on which their successor traces differ:

| minimal cost | rule pairs |
|---:|---:|
| 0 | 16,384 |
| 1 | 14,336 |
| 2 | 1,792 |
| 3 | 128 |
| **total** | **32,640** |

This profile is relative to the all-zero reference state, width-eight query language,
complete successor observation, deterministic rule family, and Hamming cost. Change any
of those and the witness profile may change.

## Interpretation

The benchmark demonstrates three bounded statements:

1. a consistent candidate class can be treated as the input to a constructive query
   problem;
2. query cost and identifying power are separate quantities;
3. at matched cost, arrangement can determine whether a query merely reduces a class or
   identifies one member.

It does **not** demonstrate:

- a new result in automata learning or experimental design;
- that exhaustive search scales;
- that a neural system can learn the generator;
- that every useful abstraction has a cheap witness;
- that witness construction is sufficient for intelligence;
- that a query is safe or permissible merely because it is informative.

## Next falsifiable step

Hold the candidate family and intervention budget fixed, then compare:

1. random equal-cost queries;
2. exact information-gain search;
3. a learned witness generator trained on disjoint rule pairs;
4. a predictive model whose queries are selected only through rollout search.

The learned generator matters only if it approaches the exact frontier on unseen pairs
with less search, and the advantage survives accounting for training compute, query cost,
noise, and model-family misspecification.

## Related

- [The Witness Principle](../../../theory/core/the-witness-principle.md)
- [From Trace to World-Binding](../../../theory/core/from-trace-to-world-binding.md)
- [Measurement as Weak Intervention](../../../theory/core/measurement-as-weak-intervention.md)
- [Inverse-Reconstruction Benchmark](../inverse-reconstruction/README.md)
- [Open Problem 14: Learned Witness Construction](../../../theory/reference/open-problems.md#open-problem-14-learned-witness-construction)
