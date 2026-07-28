# Witness-Generation Benchmark — Candidate Class → Distinguishing Query

**Status:** exact finite lemma and exhaustive cross-check

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
| analytical check | neighborhood coverage and rule-table difference layers |

The generator is exact enumeration, not a learned model. It establishes the finite floor
that a learned system must match before claims about reusable witness construction become
interesting. The analytical route is independent of the query search.

## Run

```bash
cd lab/benchmarks/witness-generation
python witness_benchmark.py
python witness_benchmark.py --candidates 0,128
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

## Coverage–distinction receipt

The enumeration has a closed-form explanation.

For deterministic lookup-table candidates, let $C(q)$ be the table coordinates exposed
by query $q$, and let $D(\theta,\theta')$ be the coordinates on which two candidates
differ. Then

$$
q\text{ separates }\theta,\theta'
\quad\Longleftrightarrow\quad
C(q)\cap D(\theta,\theta')\ne\varnothing.
$$

An identifying query must therefore hit every remaining pairwise difference set. This
decomposes the problem into the **distinction geometry** of the candidate class and the
**access geometry** of admissible interventions.

For the full ECA family, a row containing $k$ distinct neighborhoods reveals exactly $k$
of the eight rule-table bits. Every resulting candidate block has size

$$
2^{8-k}.
$$

Thus worst-case and uniform expected residuals are both $2^{8-k}$. The code checks this
identity for every width-eight row.

This also quotients the raw action space. Two queries are equivalent for the full family
exactly when they expose the same neighborhood set and therefore induce the same
candidate partition. The 256 width-eight rows collapse to 21 such query classes. Search
can operate on those structural classes and retain only the cheapest representative,
rather than treating rotations or other surface variants as independent discoveries.

A width-eight ring exposes all eight neighborhoods exactly when it is a binary de Bruijn
cycle of order three. Exactly four of the eight three-bit words have a central one, so
every universal width-eight query has cost four. The exhaustive route finds 16 such
linear rows: the rotations of the two binary de Bruijn cycles. This makes the cost-four
optimum necessary and sufficient.

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

This distribution also follows without searching rows. The lookup coordinates form
Hamming-weight layers of sizes 1, 3, 3, and 1. After revealing the layers through costs
0, 1, 2, and 3, the numbers of still-unresolved pairs are respectively
$16{,}256$, $1{,}920$, $128$, and $0$. Successive differences from the initial
$32{,}640$ pairs give exactly the table above. The implementation asserts that the
analytical profile equals the exhaustive profile.

This profile is relative to the all-zero reference state, width-eight query language,
complete successor observation, deterministic rule family, and Hamming cost. Change any
of those and the witness profile may change.

## Restricted candidate classes: where coverage stops being enough

The same exact machinery accepts any declared subset through `--candidates` or the
`restricted_frontier()` API. This exposes the distinction that the full 256-rule family
hides: a query should cover coordinates on which the *remaining candidates differ*, not
simply as many coordinates as possible.

At exact cost three:

| candidate class | candidate-aware query | coordinates seen | worst-case remaining | strongest maximal-coverage query | coordinates seen | worst-case remaining |
|:---|:---:|---:|---:|:---:|---:|---:|
| `{0, 128}` | `00000111` | 6 | **1** | `00001011` | 7 | 2 |
| `{0, 64, 128, 192}` | `00000111` | 6 | **1** | `00001011` | 7 | 2 |

Rules 0 and 128 differ only at table coordinate `111`. The candidate-aware query spends
its three prepared bits to expose that coordinate. Every cost-three query with maximal
seven-coordinate coverage omits `111`; there are 16 such maximizers, and none separates
the pair. The coverage arm in the code receives the best candidate score among all tied
maximizers, so this is not a tie-breaking artifact.

The divergence has an exact full-family count. At cost three, some query separates every
one of the 32,640 unordered rule pairs. Maximal-coverage queries separate 32,512. The
remaining **128 pairs** differ only on coordinate `111`. This is the measured collapse
boundary: full-family witness generation is coordinate coverage, while restricted-class
witness generation is hitting the declared class's actual difference sets.

For the full 256-rule product family, adaptivity cannot improve this objective. After any
observation, every unobserved rule-table coordinate remains an independent free bit, so
the residual class depends only on the union of coordinates exposed, not on the observed
values or the branch taken. A two-query adaptive policy and a non-adaptive pair with the
same reachable coverage therefore have the same residual class. Restricted families can
break that symmetry; an adaptive comparison needs a separately declared total-cost and
branch-cost convention and is left as a follow-up rather than silently choosing one.

## Interpretation

The benchmark demonstrates four bounded statements:

1. a consistent candidate class can be treated as the input to a constructive query
   problem;
2. query cost and identifying power are separate quantities;
3. at matched cost, arrangement can determine whether a query merely reduces a class or
   identifies one member;
4. identifiability depends jointly on where candidates differ and what the intervention
   interface can reach.

It does **not** demonstrate:

- a new result in automata learning or experimental design;
- that exhaustive search scales;
- that the full-family task is a sufficient learned-witness benchmark;
- that a neural system can learn the generator;
- that every useful abstraction has a cheap witness;
- that witness construction is sufficient for intelligence;
- that a query is safe or permissible merely because it is informative.

## Next falsifiable step

The exact restricted-class arm now measures where coverage and distinction diverge. The
next benchmark should sample disjoint candidate subsets and access constraints, then
compare:

1. random equal-cost queries;
2. exact information-gain search;
3. a learned witness generator trained on disjoint rule pairs;
4. a predictive model whose queries are selected only through rollout search.

The learned generator matters only if it approaches the exact frontier on unseen
candidate subsets and access geometries with less search, and the advantage survives
accounting for training compute, query cost, noise, and model-family misspecification.
Equivalent query classes should receive equal credit; reproducing the exact benchmark row
is not the target.

## Related

- [The Witness Principle](../../../theory/core/the-witness-principle.md)
- [From Trace to World-Binding](../../../theory/core/from-trace-to-world-binding.md)
- [Measurement as Weak Intervention](../../../theory/core/measurement-as-weak-intervention.md)
- [Inverse-Reconstruction Benchmark](../inverse-reconstruction/README.md)
- [Open Problem 14: Learned Witness Construction](../../../theory/reference/open-problems.md#open-problem-14-learned-witness-construction)
