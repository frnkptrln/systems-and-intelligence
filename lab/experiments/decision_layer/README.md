# Decision Layer on the Witness-Generation Benchmark

**Status:** Bounded working experiment — exact, deterministic, standard library; not a repository claim. Candidate C1 of the identification register stays a candidate until the maintainer decides otherwise.
**Origin:** [Identification Claims, Candidate C1](../../../meta/repository-meta/identification-claims.md#candidate-c1-class-size-is-not-decision-risk-information-gain-is-not-value-of-information) ("Class Size Is Not Decision Risk; Information Gain Is Not Value of Information") and [Decision-Relevant Identifiability §7](../../../theory/core/decision-relevant-identifiability.md#7-immediate-empirical-consequence), which asks for a task and value layer on the witness benchmark.
**Instrument:** the witness-generation benchmark, [`lab/benchmarks/witness-generation/witness_benchmark.py`](../../benchmarks/witness-generation/witness_benchmark.py), loaded by path and used unchanged for candidate classes, admissible queries, outcomes, partitions, and coverage signatures.

## Question

The essay separates two things the benchmark's own scores run together: the size of the class a query leaves behind is not the decision risk of that class, and the bits a query yields are not the value of the information for a task. The register lists both as Candidate C1 because nothing measured them. This experiment attaches declared value cards to the witness benchmark and asks, for each candidate class, card, and query cost, whether the query the benchmark's selectors pick (smallest worst-case block, then smallest expected class; or most bits) is strictly worse in decision value than another query of the same cost.

## Setting

**Candidate classes.** A *cube* over three neighborhood coordinates is the set of eight rules that differ exactly there; the essay's (decision coordinate, two nuisance coordinates) structure. All 56 coordinate triples with each of their three coordinates as decision coordinate give 168 cube classes. Four named classes: `K1` = cube {010, 101, 111} with decision coordinate 111 (rules 0, 4, 32, 36, 128, 132, 160, 164); `K2` = cube {000, 010, 101} with decision coordinate 000 (negative control: a cost-2 row exposes all three coordinates); `K3` = {0, 128} (the benchmark's pair) with 111; `K4` = all 256 rules with 111.

**Queries.** The benchmark's: a width-8 binary row at exact Hamming cost 0–4 from the all-zero row; the outcome is the complete successor row; a query partitions the class into blocks by outcome. Uniform prior over the class.

**Value cards** (integer tables over rule × action):

- `U` identification: actions = the class; value 1 when the guessed rule is the true one. Control: every distinction worth the same.
- `D1` decision bit: actions {0, 1}; value 10 when the action equals the rule's table bit at the decision coordinate (the essay's Case B).
- `D2` safe option: `D1` plus a third action paying 6 whatever the rule.
- `D3` harmless: one action pays 1 for every rule, the other 0 (the essay's Case A).

**Quantities, all exact.** Value before the query `EV(B) = max_a mean_θ V_θ(a)`; value after `EV(q) = Σ_blocks max_a Σ_{θ∈b} V_θ(a) / |B|`; value of information `VoI(q) = EV(q) − EV(B)`. Regret radius of a block, the essay's decision risk of a posterior class: `ρ(b) = min_a max_{θ∈b} (max_a' V_θ(a') − V_θ(a))`; expected regret `Σ_b |b|/|B| · ρ(b)`. Class-size scores as in the benchmark: worst-case block and expected remaining `Σ|b|²/|B|`. Information gain ranked by the integer entropy product `Π|b|^{|b|}` (smaller product, more bits); bits reported for display.

**Selectors at one cost.** SIZE: the benchmark's key (worst case, then expected remaining). IG: smallest entropy product. VOI: largest value of information. A cell (class, card, cost) is **size-strict** when the best VoI among all size-optimal rows is strictly below the cost's maximal VoI, **IG-strict** likewise for the IG-optimal rows; the criticized arm always receives the best VoI among its tied optima, the benchmark's own device against tie-breaking artifacts. A **full reversal** is an IG-strict cell whose representatives also have more bits and a smaller expected class on the losing side. A **risk-inversion pair** is two blocks of one (class, card), the smaller carrying the larger regret radius.

**Coverage criterion (P4).** For a cube class, a cell is predicted strict from coverage signatures alone: some cost-c row exposes the decision coordinate, and every row that exposes the most cube coordinates omits it.

**Grid.** 172 classes × 4 cards × 5 costs = 3,440 cells. CI subgrid: `K1`–`K4` × 4 cards × costs 0–4, without `K4|U|4` (the one expensive cell).

## Measures

Per cell: the three selected rows, the cost's maximal VoI, the VoI each arm achieves, the three flags, and for each selected row its worst-case block, expected remaining, entropy product, bits, VoI, expected regret, and the list of (block size, regret radius). Per (class, card): the risk-inversion pairs over all rows of all costs. The regret radius of the whole class for `K4|D3` and `K3|D1`. A summary with strict-cell counts per card and cost and the P4 check.

## Prediction (declared before the result files are committed)

- **P1.** `K1|D1|3` and `K4|D1|3` are size-strict, IG-strict, and full reversals. The size and IG arm select `00001011` (blocks 2, 2, 2, 2; 2 bits; VoI 0; regret radius 10 in every block); the VOI arm selects `00000111` (blocks 4, 4; 1 bit; VoI 5; regret radius 0). `K1|D2|3` is strict with maximal VoI 4.
- **P2.** `K4|U` is never strict, and its maximal VoI at cost c is (2^k − 1)/256 with k the coordinates exposed: 1/256, 15/256, 31/256, 127/256 at costs 0–3.
- **P3.** `K1|D1` has a risk-inversion pair: a size-2 block with radius 10 and a size-4 block with radius 0. The class radius is 0 for `K4|D3` (256 rules) and 10 for `K3|D1` (2 rules): the essay's Cases A and B.
- **P4.** On every (cube, `D1`, cost) cell the coverage criterion equals the enumerated size-strictness.
- **P5.** `K2` is never strict under any card at any cost.

**Disclosure.** None of these predictions is blind. P1–P3 and P5 were computed by a probe during the design pass, and the finished module was smoke-run on the CI subgrid and the full grid on 2026-09-03 before this README was committed; that run also checked P4 and counted the strict cells. The experiment's value is the exact, pinned receipt for Candidate C1, not a surprise. The smoke record is `results/smoke-2026-09-03.md`.

## Failure condition

- If any P1 flag is false or any number in the P1 table differs, the layer's value-of-information or selector code contradicts a hand computation; the result files are not evidence until this is explained.
- If any `K4|U` cell is strict, the control fails: the layer measures something other than decision value.
- If `K1|D1` has no risk-inversion pair, the first half of C1 has no witness here.
- If the coverage criterion disagrees with the enumeration on any cube cell, dominance is not fully explained by access geometry in this setting; P4 is false and the other results stand.
- If `K2` is strict anywhere, the negative control fails.

What the experiment cannot show, whatever the numbers: anything about learned witness generators, adaptive multi-query policies, noise or partial observation, non-uniform priors, real losses, viability, or whether a query is safe or permissible. The cards are declared, not derived. Strict cells are rare here; that is a fact about this access geometry, not a rate for anything else. No decision theory is added; whether C1 becomes a claim is the maintainer's status decision.

## How to run

```bash
python lab/experiments/decision_layer/decision_layer.py --save
python -m pytest tests/test_decision_layer.py -q
```

The first command writes `results/decision_layer.json` (the full grid, about 30 s on one CPU) and `results/ci_subgrid.json` (about 10 s). Fractions are serialized as strings so exactness survives the JSON round trip. The test pins the P1 table, the P2 control, the P3 radii, P5, the P4 equality on the CI classes, agreement of the exact expected-remaining score with the benchmark's float, and the committed CI subgrid.

## Results (full grid, run 2026-09-03)

`results/decision_layer.json`: 3,440 cells, 42 s on one CPU. The full-grid file keeps the selected rows, the arm values, and the flags per cell; the per-row measures and block lists are in `results/ci_subgrid.json`.

- **P1 holds.** `K1|D1|3` and `K4|D1|3` are size-strict, IG-strict, and full reversals, with the declared table: the size and IG arms select `00001011` (blocks 2, 2, 2, 2; 2 bits; VoI 0; regret radius 10 in every block), the VOI arm selects `00000111` (blocks 4, 4; 1 bit; VoI 5; regret radius 0). `K1|D2|3` and `K4|D2|3` are strict with maximal VoI 4.
- **P2 holds.** `K4|U` is never strict; its maximal VoI is 1/256, 15/256, 31/256, 127/256, 255/256 at costs 0–4.
- **P3 holds.** `K1|D1` contains the pair (size 2, radius 10) against (size 4, radius 0); the class radius is 0 for `K4|D3` at 256 rules and 10 for `K3|D1` at 2 rules.
- **P4 holds.** The coverage criterion equals the enumerated size-strictness on all 850 (cube, `D1`, cost) cells.
- **P5 holds.** `K2` is never strict under any card at any cost.

Strict cells in the whole grid: 14 of 3,440, every one a full reversal; 7 under `D1` and the same 7 under `D2`, none under `U` or `D3`. Cube names read `C<coordinates>d<decision coordinate>` with neighborhood codes 0–7.

| Cell (`D1`; `D2` identical with VoI 0 → 4) | Size and IG arms | VOI arm | VoI arm → maximum |
|:---|:---|:---|---:|
| `K1\|D1\|3`, `K4\|D1\|3`, `C257d7\|D1\|3` | `00001011` | `00000111` | 0 → 5 |
| `C235d3\|D1\|2`, `C256d6\|D1\|2` | `00000101` | `00000011` | 0 → 5 |
| `C236d2\|D1\|2`, `C356d5\|D1\|2` | `00000011` | `00000101` | 0 → 5 |

What this shows, and no more: in this access geometry the benchmark's selectors and the decision-value selector disagree strictly in exactly the cells the coverage criterion names, where every cheapest row that exposes the most cube coordinates misses the decision coordinate while some row of the same cost exposes it; everywhere else they agree or tie. A size-2 block can carry regret radius 10 while a size-4 block carries 0, and 2 bits can be worth 0 while 1 bit is worth 5. Both halves of Candidate C1 now have an exact, pinned receipt in one declared setting. Whether that promotes C1 is the register's status decision, reserved for the maintainer.
