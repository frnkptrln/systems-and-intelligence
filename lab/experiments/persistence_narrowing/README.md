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

## Results (full grid, run 2026-09-02)

`results/persistence_narrowing.json`: 24,576 runs, 13 s on one CPU. Means over 4,096 runs per cell.

| Family | Condition | Observed | Held-out | Distinct proposals | Distinct accepted | Pull | Recalls | Invalidated |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|
| full | none | 1.0000 | 0.8594 | 35.81 | 12.00 | 1.534 | 0.0 | 0.0 |
| full | memory | 1.0000 | 0.8594 | 42.01 | 11.19 | 1.446 | 63.3 | 0.0 |
| full | invalidation | 1.0000 | 0.8594 | 42.32 | 11.04 | 1.337 | 31.9 | 15.6 |
| affine | none | 0.7936 | 0.7061 | 6.71 | 2.88 | 0.242 | 0.0 | 0.0 |
| affine | memory | 0.8665 | 0.7561 | 12.32 | 3.92 | 0.177 | 66.4 | 0.0 |
| affine | invalidation | 0.8661 | 0.7562 | 12.18 | 3.84 | 0.173 | 28.5 | 15.6 |

Against the declared predictions:

- **P1 holds.** `heldout_equals_ceiling_identity` is true in all three conditions; mean held-out equals mean ceiling (0.8594) in every condition of the `full` family. The memory is target-independent, and held-out cannot move there.
- **P2 fails on the diversity measures and holds on pull.** Distinct proposals *rise* under `memory` in both families: a remembered artifact fitted to another world is usually a table the one-bit walk would not have proposed. Distinct accepted falls in the `full` family (12.00 → 11.19) but rises in the `affine` family (2.88 → 3.92), so the failure condition for P2 is met and P2 is false in this setting. Pull falls in both families: the final artifact ends closer to a remembered one.
- **P3 holds.** In the `affine` family, observed rises from 0.7936 to 0.8665 under `memory`, and held-out rises with it from 0.7061 to 0.7561.
- **P4 fails on "between".** Invalidation discards 15.6 remembered artifacts per run (of 16), so the memory is nearly emptied within the budget and the run continues as flips. Its measures do not lie between `none` and `memory`: distinct accepted and pull move slightly further from `none` than `memory` does, while the observed gain of P3 is kept in full (0.8661). Revocation of artifacts that fail visible tests gives nothing back here, because in this toy the memory took no diversity away.

What this shows, and no more: under a frozen referee, a target-independent memory of earlier accepted artifacts widens the proposal set, pulls the endpoint toward remembered artifacts, and in the constrained family raises both the visible score and the hidden-rule agreement. "Narrowing" in the sense of the persistence note, if it exists, is not what counting distinct artifacts measures in this setting. A memory built from the *same* world would model the note's situation more closely, and would break the identity by construction; that is the boundary this experiment did not cross.

## Archive-content control — 19 October 2026

**Status:** Post-hoc control of the result above, not a preregistered prediction.
The original experiment and its archived results are unchanged.

Remembered artifacts replace half of the local proposal opportunities with
potentially larger jumps. Does the earlier fitting of those artifacts help
beyond a generic global proposal reservoir? Does moving the same archive in
state space change its effect while retaining its internal geometry?

[`archive_control.py`](archive_control.py) reuses `run_loop` unchanged and
compares four arms:

- `none`: the original memory-free walk.
- `fitted`: the original 16 prior-world artifacts, including their order and
  duplicates; this reproduces the original `memory` condition.
- `uniform`: 16 independent, uniform state vectors drawn **with replacement**.
- `translated`: one common nonzero XOR mask applied to every fitted entry.
  The mask is drawn once per family/seed, independently of evaluation targets.
  It preserves duplicate indices and every pairwise parameter-space and
  rule-table Hamming distance, including in the affine family.

The uniform and translation streams are respectively
`archive-control:uniform:{family}:{seed}` and
`archive-control:xor:{family}:{seed}`. All three archive arms keep 16 entries
and use exactly the same recall decisions, sampled entry indices and flip
slots within each seed/row. Recall probability is `1/2`, not a fixed quota of
64 calls. No invalidation or deduplication changes the schedule. The original
referee, acceptance rule, zero start, evidence and 128-proposal evaluation
budget stay fixed.

The full grid is two families, four arms, two archive seeds, eight rows and
all 256 hidden rules: **32,768 evaluation runs**, 4,096 per family/arm.
There are only **two archive draws per family**. Reusing an archive across
many rows and rules does not create independent archive replications.
Fitted archives require 16 earlier fits of 128 proposals (2,048 prior
proposals each); translated archives reuse that work. Preparation cost is
not matched to uniform draws, so the comparison is not a total-compute or
sample-efficiency result.

### Fixed-grid results

| Family | Archive | Observed | Held-out | Distinct proposals | Distinct accepted |
|:---|:---|---:|---:|---:|---:|
| full | none | 1.0000 | 0.8594 | 35.81 | 12.00 |
| full | fitted | 1.0000 | 0.8594 | 42.01 | 11.19 |
| full | uniform | 1.0000 | 0.8594 | 41.90 | 11.37 |
| full | translated | 1.0000 | 0.8594 | 41.76 | 11.32 |
| affine | none | 0.7936 | 0.7061 | 6.71 | 2.88 |
| affine | fitted | 0.8665 | 0.7561 | 12.32 | 3.92 |
| affine | uniform | 0.8812 | 0.7661 | 13.06 | 4.05 |
| affine | translated | 0.8686 | 0.7575 | 12.45 | 3.89 |

The original `none` and `memory` cells reproduce exactly. On this fixed grid,
the uniform reservoir exceeds the fitted archive's mean affine visible
score in both archive seeds, and its pooled held-out score is higher too.
Thus the earlier improvement over a local walk does not establish a special
advantage of fitting prior-world artifacts: a generic global proposal
reservoir also helps here. This is not a population estimate from two
archives, nor evidence that prior experience is generally unhelpful.

Translation changes outcomes despite preserving internal geometry. It also
changes the archive's position relative to the unchanged zero start and
visible target values; it does not isolate a semantic or training effect.
The affine fitted/uniform/translated banks contain respectively 10/10/10
unique states at seed 0 and 9/11/9 at seed 1. Uniform replacement therefore
does not control duplicate multiplicity or geometry. The JSON preserves the
ordered entries, multiplicities, pair-distance histograms, masks and
per-seed contrasts. `pull` is omitted because each native loop result uses
its own archive as reference, which would change across arms.

### Information and execution checks

Saturation and the information identity are checked separately. For each
family/seed/row/arm, write `H` for summed held-out correct coordinates, `P`
for summed visible passes and `T` for summed visible test counts over all
256 rules. With target-independent archives and random streams, the unseen
rule bits remain free, giving

$$
2H = 2P + 256\cdot 8 - T.
$$

The earlier ceiling formula `2H = T + 256*8` additionally assumes `P = T`.
A failure to fit every visible test is not by itself evidence of target
leakage. Every new block passes the general identity; all four full-family
arms also saturate visible evidence. This identity is a design check, not a
complete proof that an arbitrary implementation has no information leak.

Tests compare the actual RNG call traces across archive arms, transport the
complete pairwise geometry, exercise an unsaturated zero-budget case and a
corrupted information check, and compare the reproduced original cells.
The [dated result](results/archive-control-2026-10-19.json) records exact
fractional means, per-seed contrasts, row checks and hashes of all three
source modules. The run uses only the Python standard library; it makes no
model calls and makes no claim about semantic novelty or LLM research.

```bash
python lab/experiments/persistence_narrowing/archive_control.py --seeds 2 --rows 8
python lab/experiments/persistence_narrowing/archive_control.py --format markdown
python -m pytest tests/test_persistence_archive_control.py -q
```
