# Persistence and Search Narrowing in a Referee Loop

**Status:** Bounded working experiment — a toy-scale, deterministic, standard-library run; not a repository claim.
**Origin notes:** [Persistence Can Narrow the Search Space](../../../ideas/2026-08-11-persistence-can-narrow-search-space.md) (primary), [A Research Loop Can Become Its Own Environment](../../../ideas/2026-08-10-research-loop-becomes-environment.md), [Experience Needs an Invalidation Boundary](../../../ideas/2026-08-22-experience-needs-an-invalidation-boundary.md); the design respects the information boundary that [Mechanistic Discovery Needs Methodological Separation](../../../ideas/2026-08-22-mechanistic-discovery-needs-methodological-separation.md) asks for, but does not test that note.
**Instrument:** the referee benchmark's loop, [`lab/benchmarks/recursive-workbench/referee_benchmark.py`](../../benchmarks/recursive-workbench/referee_benchmark.py), reused unchanged for its primitives; the loop body is re-implemented here so that the proposer can carry state.

## Question

The persistence note asks whether accumulated context makes a research loop locally more competent while pulling its proposals toward what it already holds. The invalidation note asks whether a revocation rule changes that. Both questions are about language-model research systems, which this repository does not run. This experiment asks the smallest mechanical version of the same question in a setting where every quantity is exact: what does a memory of earlier accepted artifacts do to a hill-climbing proposer under a frozen referee, and does invalidating remembered artifacts that fail visible tests give back what the memory took?

## Setting

Everything is the referee benchmark's: a hidden elementary cellular-automaton rule (256 of them), evidence induced by one update of a random width-8 ring, a frozen evaluator that only reports pass counts on the visible evidence, a proposer that flips one random slot of an artifact, an acceptance rule (accept when the candidate's pass count is at least the current one), and a hard budget. Two artifact families: `full` (the eight rule bits) and `affine` (four parameters, the benchmark's constrained family, which cannot represent most rules).

Fixed parameters: budget 128 proposals per run; 256 hidden rules; 8 evidence rows per seed; 2 seeds; memory of 16 remembered artifacts; recall probability 1/2. The grid is 2 families × 3 conditions × 2 seeds × 8 rows × 256 rules = 24,576 runs.

**Memory.** Before the evaluation rows are run, the memory-free loop is run on 16 *prior worlds* whose hidden rules come from the stream `memory:{family}:{seed}` and whose evidence and proposals come from `world-memory` and `loop-memory` streams. The final accepted artifact of each prior world is remembered. Nothing in the memory depends on the hidden rule of an evaluation run, so within one (seed, row) block the memory is identical for all 256 hidden rules. That is what keeps the benchmark's held-out == ceiling identity intact, and the identity is checked in every condition.

## Conditions

Same seeds, same budget, same referee, same evidence rows.

- `none` — the benchmark loop. Every proposal flips one random slot. This condition reproduces `referee_benchmark.run_loop` exactly; `tests/test_persistence_narrowing.py` asserts it.
- `memory` — with probability 1/2 (its own `recall` stream) a proposal is a remembered artifact instead of a flip; accepted under the same rule.
- `invalidation` — as `memory`, but a recalled artifact that fails at least one visible test is discarded from the run's copy of the memory. An emptied memory falls back to flips.

## Measures (per run, aggregated as exact means)

- **observed** — the final artifact's pass fraction on the visible evidence (the local score).
- **held-out** — the final artifact's agreement with the hidden rule on all eight neighborhoods.
- **distinct proposals** — number of distinct candidate tables proposed in the run.
- **distinct accepted** — number of distinct artifacts on the accepted path (the declared diversity measure: how much of the artifact space the accepted path covers).
- **pull** — Hamming distance from the final artifact to the nearest remembered artifact, computed against the same memory in all three conditions so that they are comparable.
- **recalls**, **invalidated**, **accepted** — counts of recalled proposals, of discarded memory entries, and of accepted proposals.

## Prediction (declared before the full grid is run)

- **P1, identity.** In the `full` family, `2 × Σ held-out correct = Σ visible tests + 256 × 8` per (seed, row) block in every condition. Memory is target-independent, so the benchmark's identity must survive its introduction. This is a design check, not a finding.
- **P2, narrowing.** Under `memory`, mean distinct proposals and mean distinct accepted are lower than under `none`, and mean pull is smaller (the final artifact sits closer to a remembered one), in both families. Part of this is built in: half of the proposals are drawn from a 16-element set. The experiment measures how large the effect is, not whether it exists.
- **P3, local usefulness.** In the `affine` family, mean observed is higher under `memory` than under `none`: a remembered artifact was already fitted to a prior world and beats the all-zero start. Whether held-out rises with it is left open; in the `full` family held-out is pinned by P1 and cannot move.
- **P4, invalidation.** Under `invalidation`, mean invalidated is positive, and the diversity and pull measures lie between `none` and `memory`, while the affine observed gain of P3 is at least partly kept.

**Disclosure.** A smoke run of the declared CI subgrid (1 seed, 2 rows) was made on 2026-09-02 while the code was being written, before this README was committed. It showed P1 holding and the directions of P2 and P3. The predictions above are therefore not blind as to direction; the magnitude on the full grid and P4 were not inspected. The smoke record is `results/smoke-2026-09-02.md`.

## Failure condition

- If P1 fails in any condition, the memory leaks target information and the result files are not evidence of anything; the experiment is invalid until the leak is explained.
- If mean distinct accepted under `memory` is not below `none` in both families, P2 is false in this setting.
- If mean observed in the `affine` family is not higher under `memory` than under `none`, P3 is false.
- If mean invalidated is zero, or the `invalidation` measures do not lie between `none` and `memory`, P4 is false.

What the experiment cannot show, whatever the numbers: anything about language-model research agents, about semantic novelty, or about the paper that triggered the persistence note. Narrowing here is a property of a proposal mixture under an exact referee in a toy where the ceiling is known.

## How to run

```bash
python lab/experiments/persistence_narrowing/persistence_narrowing.py --seeds 2 --rows 8 --save
python -m pytest tests/test_persistence_narrowing.py -q
```

The first command writes `results/persistence_narrowing.json` (the full grid) and `results/ci_subgrid.json` (1 seed, 2 rows). The test reproduces the `none` condition against the referee benchmark, checks P1 in every condition, and recomputes the CI subgrid against the committed file. Standard library only; a few minutes on one CPU for the full grid.

## Results

Not yet run on the full grid at the time this README was committed. The results summary is added in the commit that adds the result files.
