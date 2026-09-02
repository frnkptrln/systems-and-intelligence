# Representation and Reconstruction Difficulty in the ECA Testbed

**Status:** Bounded working experiment — a toy-scale, deterministic run on the inverse-reconstruction benchmark's testbed; not a repository claim.
**Origin notes:** [Representation Changes Reconstruction Difficulty](../../../ideas/2026-08-09-representation-changes-reconstruction-difficulty.md) (primary), [Mechanism as a Reconstruction Target](../../../ideas/2026-08-09-mechanism-as-reconstruction-target.md), [Representational Grounding and Mechanistic World Models](../../../ideas/2026-08-09-representational-grounding-and-mechanistic-world-models.md).
**Instrument:** the inverse-reconstruction benchmark, [`lab/benchmarks/inverse-reconstruction/inverse_benchmark.py`](../../benchmarks/inverse-reconstruction/inverse_benchmark.py) (forward model, tabulating reconstructor, coverage and noise dials) and [`family_search.py`](../../benchmarks/inverse-reconstruction/family_search.py) (the v1.2 enumeration-cost dial), both reused unchanged.

## Question

The representation note asks whether a change of representation can make trace → generator reconstruction easier without adding evidence, and proposes separating *identifiability* from *representational accessibility*; it warns that a non-invertible representation may discard distinctions and manufacture apparent identity. The identity-abduction sanity check ([`lab/experiments/identity_abduction/`](../identity_abduction/README.md)) showed the verification pattern on one graph. This experiment asks the same question on the benchmark's full rule family with exact accounting: hold the family, the evidence, and the reconstructor fixed; change only the representation of the trace the reconstructor receives; measure what moves.

## Setting

The benchmark's elementary cellular automata: 256 rules, width 64, 64 steps, two initial conditions (`random`, `single`) and three bit-flip noise levels (0, 0.1, 0.2), two seeds. The reconstructor is the benchmark's majority-vote tabulation over observed neighborhood → successor pairs; the consistent class has size `2 ** (unseen neighborhoods)`, as in the benchmark. Grid: 2 seeds × 256 rules × 2 initial conditions × 3 noise levels × 6 representations = 18,432 runs.

**Representations of the received trace.**

- `raw` — the space-time grid as produced.
- `complement` — every cell `x → 1 − x` (invertible).
- `reflect` — every row reversed (invertible).
- `both` — complement, then reflect (invertible).
- `block_or2` — adjacent cell pairs → OR; the width halves (lossy).
- `majority3` — every cell → majority of its 3-neighborhood (lossy).

Under an invertible re-encoding the received trace is exactly the trace of another rule in the same family (the complement conjugate, the mirror rule, or both); the reconstructor is expected to recover that *transformed truth*, and its identity is known in closed form (`complement_rule`, `reflect_rule`, both involutions). Under a lossy encoding there is in general no rule whose trace the reconstructor receives.

**Search cost.** The benchmark's own v1.2 measure: the number of syntactic formulas a size-ordered enumerator over the benchmark's Boolean DSL generates before reaching the minimal description size of the shortest table consistent with the observed bits. Verification of a candidate costs eight comparisons in every representation; only the construction cost can change.

## Measures (per cell of the grid, exact means)

- **bit accuracy** and **truth-in-class fraction** — agreement of the reconstructed bits with the transformed truth on seen neighborhoods (invertible representations only; undefined for lossy ones, where no transformed truth exists).
- **class size** — `2 ** unseen`, and the fraction of runs in which it equals the `raw` class size for the same (seed, rule, initial condition, noise).
- **contradiction fraction** — runs in which one neighborhood was observed with both successors. The benchmark's majority vote hides these; they are reported here.
- **search cost** — as above, and the fraction of runs in which it equals the `raw` cost.
- **description-size shift** — over all 256 rules, how many rules change minimal description size under each invertible map, in which direction, and by how much at most.

## Prediction (declared before the full grid is run)

- **P1, invertibility preserves identifiability.** Under `complement`, `reflect`, and `both`, class size equals the `raw` class size in every run, and at noise 0 the transformed truth is in the class in every run. This is exact: `invertibility_check.<condition>.exact` must be `true` for all three.
- **P2, invertibility does not preserve accessibility.** The minimal description size of the transformed truth differs from the raw truth's for some rules under `complement` (negation is not free in the DSL), and for no rule under `reflect` (the DSL treats the left and right neighbors symmetrically, so a mirrored formula has the same size). So search cost moves while class size does not — the separation the note asks for, exhibited in one declared DSL.
- **P3, lossy encodings manufacture contradiction.** At noise 0, the contradiction fraction is 0 for `raw` and the invertible representations and positive for `block_or2` and `majority3` on random initial conditions: the received trace is not the trace of any rule in the family, and the majority-vote class size is then not an identifiability measure at all.

No direction is predicted for the mean search cost under lossy encodings; it is reported.

**Disclosure.** A smoke run of the declared CI subgrid (1 seed, every eighth rule, both initial conditions, noise 0 and 0.1) was made on 2026-09-02 while the code was being written, before this README was committed. It showed P1 holding in every run of the subgrid, a nonzero size shift under `complement` and none under `reflect`, and contradictions under the lossy encodings. The predictions above are therefore not blind as to direction; the full-grid numbers were not inspected. The smoke record is `results/smoke-2026-09-02.md`. *(Correction, added with the results commit on 2026-09-02: the smoke run covered all 256 rules of one seed at all three noise levels, as the smoke record states, not only the CI subgrid; the sentence above is left as declared.)*

## Failure condition

- If `invertibility_check` is not exact for any invertible map, P1 is false: either the reconstructor is representation-sensitive in a way the note did not anticipate, or the conjugate rule maps are wrong. Either way the result files are not evidence until this is explained.
- If no rule changes minimal description size under any invertible map, P2 is false: in this DSL, representation does not separate accessibility from identifiability, and the note's hypothesis has no witness here.
- If the lossy encodings produce no contradictions at noise 0 on random initial conditions, P3 is false.

What the experiment cannot show, whatever the numbers: anything about language-model or human reasoners, about semantic or cross-domain representations, about identity abduction between different systems, or about "mechanism". Search cost is enumeration cost in one declared DSL, the benchmark's v1.2 dial, not a statement about search in general.

## How to run

```bash
python lab/experiments/representation_reconstruction/representation_reconstruction.py --seeds 2 --save
python -m pytest tests/test_representation_reconstruction.py -q
```

The first command writes `results/representation_reconstruction.json` (the full grid) and `results/ci_subgrid.json` (the declared subgrid). The test checks that the rule maps are involutions, that the transformed truth is recovered on a covered trace, that class size is equal under the invertible maps on a sample, that a lossy encoding produces contradictions, and that the CI subgrid reproduces the committed file. Requires numpy (the repository's `requirements.txt`); a few minutes on one CPU for the full grid.

## Results (full grid, run 2026-09-02)

`results/representation_reconstruction.json`: 18,432 runs, 144 s on one CPU. Means over 512 runs per cell (2 seeds × 256 rules).

**Invertibility check** (all cells, 3,072 runs per map): class size equal to `raw` in 3,072 of 3,072 runs for `complement`, `reflect`, and `both`. At noise 0 the transformed truth is in the class in every run of every invertible representation, on both initial conditions.

**Description-size shift** over the 256 rules:

| Map | Rules whose minimal size changes | Cheaper | Dearer | Largest shift |
|:---|---:|---:|---:|---:|
| complement | 98 | 49 | 49 | 1 |
| reflect | 0 | 0 | 0 | 0 |
| both | 98 | 49 | 49 | 1 |

**Cells at noise 0:**

| IC | Representation | Class size | Contradiction fraction | Truth in class | Search cost | Cost = raw |
|:---|:---|---:|---:|---:|---:|---:|
| random | raw | 1.00 | 0.000 | 1.000 | 47,074 | — |
| random | complement | 1.00 | 0.000 | 1.000 | 47,074 | 0.617 |
| random | reflect | 1.00 | 0.000 | 1.000 | 47,074 | 1.000 |
| random | both | 1.00 | 0.000 | 1.000 | 47,074 | 0.617 |
| random | block_or2 | 1.24 | 0.938 | — | 1,546 | 0.186 |
| random | majority3 | 1.00 | 0.912 | — | 18,684 | 0.475 |
| single | raw | 5.89 | 0.000 | 1.000 | 30,684 | — |
| single | complement | 5.89 | 0.000 | 1.000 | 29,511 | 0.711 |
| single | reflect | 5.89 | 0.000 | 1.000 | 30,684 | 1.000 |
| single | both | 5.89 | 0.000 | 1.000 | 29,511 | 0.711 |
| single | block_or2 | 6.70 | 0.672 | — | 727 | 0.484 |
| single | majority3 | 44.26 | 0.594 | — | 3,981 | 0.445 |

With noise (0.1 and 0.2) every representation shows contradictions in every run, because the noise itself produces them; class size is 1 throughout; and the invertible representations' bit accuracy differs from `raw` only through the noise draw landing on different cells of the re-encoded grid (random ICs, noise 0.1: 0.907 raw, 0.907 complement, 0.912 reflect, 0.911 both). The full cell table is in the result file.

Against the declared predictions:

- **P1 holds, exactly.** Identifiability, measured as class size, did not move under any invertible re-encoding in any of the 9,216 runs.
- **P2 holds.** Under `complement` the transformed truth's minimal description size changes for 98 rules (49 cheaper, 49 dearer, by one size step); under `reflect` for none. At full coverage the per-run search cost differs from `raw` in 38% of runs under `complement` while the family mean is unchanged (the map permutes the rules, so the mean over all 256 is invariant); under partial coverage (`single`) the mean itself moves (30,684 → 29,511), because the shortest consistent table changes non-uniformly. Construction cost moved; identifiability did not.
- **P3 holds.** At noise 0 there are contradictions in 0 of 512 runs for `raw` and the invertible maps, in 94% (`block_or2`) and 91% (`majority3`) of random-IC runs, and in 67% and 59% of single-IC runs.
- **Lossy search cost, not predicted:** far below `raw` at noise 0 (1,546 and 18,684 against 47,074 on random ICs). The majority-voted table of a lossy trace is a cheaper formula than the true rule. On single ICs `majority3` also leaves more neighborhoods unseen (mean class size 44.3 against 5.9). A lossy encoding makes the process look simpler and, there, less identified than it is; the "apparent identity" the origin note warned about shows up here as apparent simplicity with hidden contradictions.

What this shows, and no more: in one declared family and one declared DSL, identifiability is invariant under invertible re-encoding and construction cost is not, which is the separation the origin note proposed; lossy re-encoding does not lower the cost of identifying the true rule, it changes the problem and hides that it did. Nothing here concerns representations chosen by a reasoner, or transfer between domains.
