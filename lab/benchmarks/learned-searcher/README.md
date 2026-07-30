# Learned Searcher — Pre-Registered First Contact with the Exact Floors

**Status:** PRE-REGISTERED, NOT YET RUN. This document and the instance set,
prompts, parsing rules, and scoring in [`learned_searcher.py`](learned_searcher.py)
are frozen before the first real-model call. One run per registration, all 100
instances, no re-rolls, no prompt tuning after first contact; the verbatim
model outputs land in `results.jsonl` and are committed with the result. If the
protocol changes after the run begins, the run is void and this file must say so.

This implements the front page's first near-term frontier item: *"give LLMs or
program synthesizers the same partial traces and query budgets as the exact CA
baseline; pre-register consistency, truth recovery, description size, support
violations, and cost."* It is the zero-shot slice of
[Open Problem 14](../../../theory/reference/open-problems.md#open-problem-14-learned-witness-construction),
and the first experiment in this repository whose outcome is genuinely open —
every prior benchmark measured effects whose direction was predictable in
advance.

## Why this experiment, and why first

Three properties make it the right first contact:

1. **Fully real from the first call.** It needs only text completion through
   [`lab/providers/`](../../providers/README.md). (The Agentic Identity Suite's
   "real" runs would still use mock embeddings — `AnthropicProvider.embed()`
   deliberately falls back to the deterministic mock — so its first results
   would be only partially real. It remains the second track.)
2. **Exact referee.** Every answer is scored by the same machinery the exact
   benchmarks use; there is no judgment call anywhere in the scoring.
3. **Divergent priors.** On the trap instances (below), a coverage heuristic
   scores ~0% and difference-set reasoning scores ~100%. Whatever the model
   does, the result is informative — that prior gap is what makes the
   experiment leap-capable, where the earlier benchmarks were not.

## Tasks (100 model calls)

| Task | n | The model must... | Floors (measured/analytic) |
|:---|--:|:---|:---|
| **T1** consistent completion | 40 | output a full rule table consistent with the observed neighborhood→output pairs of a hidden rule | truth-recovery chance = Σ 2^−u ≈ **9.8/40** (beating it meaningfully is information-theoretically impossible on uniform worlds — v1.2; T1 measures consistency and *reveals the selection prior*) |
| **T2** pairwise witness | 34 random + **6 traps** | construct a width-8 ring that one update distinguishes two explicitly given rule tables, within the analytic minimal cost | do-nothing floor (all-zero row): **18/34** random, **0/6** traps; coverage heuristic on traps: **0/6** |
| **T3** universal witness | 20 | construct one ring whose single update identifies which of four given rules is in effect, within the exact minimal cost | do-nothing floor: **0/20** |

**The traps** are pairs differing only on neighborhood 111 — the exact
configuration where the [restricted witness arm](../witness-generation/README.md)
proved that every cost-3 maximal-coverage row fails while the candidate-aware
row succeeds. The tables are given explicitly in the prompt, so memorization of
famous rules cannot help; T2 and T3 are pure reasoning tasks. T1's truth-hit
rate is *not* a capability measure (chance is the ceiling in expectation); what
it reveals is which member of the equivalence class the model reaches for —
the learned analogue of v1.2's elegance prior.

## Pre-registered predictions

Locked before the run. The maintainer's column is to be filled (or explicitly
waived) before the first real call — divergent recorded priors are the point.

| Metric | Floor | Prediction (Claude, assistant, 2026-07-30) | Prediction (maintainer) | Result |
|:---|:---|:---|:---|:---|
| T1 consistency | — | ≥ 32/40 | | |
| T1 truth hits | ≈ 9.8/40 | within ±4 of 10/40 (no meaningful prior alignment) | | |
| T2 random: separates | 18/34 (do-nothing) | ≥ 27/34 | | |
| T2 random: cost-optimal | — | ≥ 20/34 | | |
| **T2 traps: separates** | **0/6** | **≥ 4/6** (difference-set reasoning, with arithmetic slips) | | |
| T3 identifies | 0/20 | ≥ 8/20 | | |
| T3 cost-optimal | — | ≥ 5/20 | | |

**Interpretation, fixed in advance.** Traps ≥ 4/6: zero-shot learned witness
construction is real at this scale; OP14's hypothesis gains its first positive
data point, and the next arm (transfer, larger families, learned proposers in
the [referee workbench](../recursive-workbench/README.md)) is motivated.
Traps ≤ 1/6: the model behaves as a coverage heuristic where coverage
provably fails; the enumeration floor stands and "generation is not
construction" gets its first measured instance. 2–3/6: underpowered — the
follow-up registration must raise n before any conclusion is drawn. T1
consistency far below prediction would be the most surprising outcome of all
(constraint satisfaction with all constraints visible) and would dominate the
reading of everything else.

## Protocol details

- Model: the provider default (`claude-sonnet-5` via `lab/providers`), server
  default sampling; one completion per instance; no retries except a single
  retry on transport error, recorded either way.
- Parse failures and provider errors count as failures in every rate and are
  reported separately. The final-line formats and the parser in
  `learned_searcher.py` are part of this registration.
- Estimated cost: 100 calls, small prompts — under one dollar.

```bash
cd lab/benchmarks/learned-searcher
python learned_searcher.py --dry-run              # inspect instances and prompts
python learned_searcher.py --provider stub        # offline pipeline check
ANTHROPIC_API_KEY=... python learned_searcher.py --provider anthropic   # THE run
```

## Related

- [Open Problem 14: Learned Witness Construction](../../../theory/reference/open-problems.md#open-problem-14-learned-witness-construction) — this is its zero-shot slice
- [Witness benchmark](../witness-generation/README.md) — the exact frontier and the trap construction
- [Inverse-reconstruction v1.2](../inverse-reconstruction/README.md) — why T1 truth recovery is capped at chance, and what the selection prior means
- [Referee workbench](../recursive-workbench/README.md) — where a learned proposer would slot in next
