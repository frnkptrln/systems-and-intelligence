# Target-Leakage Impact Note — RNG seeding, fixed in PR #53

**Status:** blast-radius record for the target-leakage fix; not a results page.
**Last reviewed:** 2026-08-19
**Review trigger:** any further change to how `run_loop` constructs its random streams.

## The defect

From the benchmark's first commit (`a51bcc5`, 2026-07-30) through v0.1, `run_loop`
seeded both streams with the hidden rule —
`world:{rule}:{seed}` and `loop:{family}:{rule}:{seed}` — so the evidence row
(and with it the visible-test mask) and the proposal-slot sequence were
deterministic functions of the target. Every number this benchmark ever
published was produced under that seeding; there is no unaffected earlier
version. PR #53 reseeds both streams from public coordinates only
(`world:{seed}`, `loop:{family}:{seed}`).

Measured severity: the leak was structural, not exploited. The pre-fix
`full-frozen` held-out total (6977/8192 = 0.8517) matches the ceiling of its own
rule-conditioned evidence masks (0.8518) to within one coordinate in 8192. The
pre-fix numbers describe a target-conditioned ensemble that nothing can certify
as leak-free; they are not evidence that the loop beat its evidence.

## Affected results (produced from the leaky paths, 2026-07-30 → PR #53)

| Where | What | Disposition |
|:---|:---|:---|
| `README.md` (this directory) | results table and inline numbers: 0.8517, 0.8525, 0.9606, 0.9589, 0.8518, 0.7960, 0.9893, 0.7021, 0.7000, 166/1024, 989/1024, 1.15 deletions, gap 0.094 → 0.289 | recomputed in PR #53 |
| `tests/test_referee_benchmark.py` | pinned integers: 6977, 6984, 5764, 7519, 7869, 166, 684679/840, 5752, 989, 40521/40, 5734, 1179 | recomputed in PR #53 |
| `logs/020_the-referee-boundary.md` (report paragraph) | "the report went from 0.80 to 0.99"; "tripled" | **stale, marked here** — post-fix: 0.79 → 1.00 (0.9953); gap ratio 3.3, "tripled" survives |
| `fiction/19_the_green_board.md`, `fiction/README.md` (source pointers) | "observed 0.99, held-out 0.70, measured" | **stale, marked here** — post-fix: observed 0.9953, held-out 0.6914 |
| `ideas/2026-07-24-self-improvement-needs-a-referee.md` (workbench paragraph) | qualitative: "measures the three regimes exactly", "tripled observed-vs-held-out gap" | survives; re-derived from post-fix numbers |
| `meta/research-alignment/related-work-map.md` (referee-boundary row) | qualitative: "10x budget does not move performance beyond it", "measured tripling" | survives; post-fix the 10x claim is exact equality (6912 = 6912) |

No CSV, figure, or other result file was ever generated for this benchmark; the
directory has only ever contained `README.md` and `referee_benchmark.py`.

## What must be recomputed

Nothing beyond what PR #53 already recomputes: the benchmark runs in seconds and
the README and test file in that PR carry post-fix numbers. Remaining work is
editorial — update the two stale prose citations above where they live. They are
marked here rather than silently edited.

## What remains valid

- All three qualitative regime statements (saturation at the evidence ceiling,
  referee queries raise the ceiling and held-out follows, capture inflates only
  the report). Directions unchanged; post-fix the first two hold exactly.
- Everything outside `referee_benchmark.py`. No other module imports it
  (`git grep referee_benchmark` returns only its test). The other instruments
  draw their randomness independently: `witness-generation` uses no randomness
  at all (exact enumeration via `itertools`; the word "seed" does not occur in
  `witness_benchmark.py`), and the seeded experiments
  (`inverse-reconstruction`, `learned-searcher`, `constraint-release`,
  `context-attractor`) construct their own generators from their own seed
  material.
