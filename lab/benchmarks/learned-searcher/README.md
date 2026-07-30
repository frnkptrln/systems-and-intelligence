# Learned Searcher — Pre-Registered First Contact with the Exact Floors

**Status:** PROTOCOL FROZEN; EXECUTION TARGET UNREGISTERED; NOT YET RUN. The
100 instances, prompts, strict final-line parser, and exhaustive scoring behavior
in [`learned_searcher.py`](learned_searcher.py) are locked by protocol digest
`5a64f4778a78063627c57c28215974057024793e5d385ee9554f3b5b0bda4963`.
The target system is deliberately *not* selected. A real run is refused until
[`execution-registration.json`](execution-registration.json) freezes a provider,
an exact model identifier, and the maintainer prediction in a separate commit.

One run per execution registration, all 100 instances, no alternate seed, no
re-rolls, and no prompt tuning after first contact. A real run has no alternate
output-path option: the runner opens canonical `results.jsonl` exclusively
rather than overwriting it. The verbatim outputs,
attempt history, source commit, model identity, response metadata, and available
usage accounting are committed with the result. If the protocol changes after a
run begins, that run is void and this file must say so.

This begins the front page's first near-term frontier item with a fixed-output,
zero-shot slice: consistency, truth recovery, witness validity, and witness
cost against exact CA floors. It does not yet train a searcher or measure learned
program description size. It is the zero-shot slice of
[Open Problem 14](../../../theory/reference/open-problems.md#open-problem-14-learned-witness-construction),
and the first experiment in this repository whose outcome is genuinely open —
every prior benchmark measured effects whose direction was predictable in
advance.

## Why this experiment, and why first

Three properties make it the right first contact:

1. **Fully real from the first call.** It needs only text completion through
   [`lab/providers/`](../../providers/README.md). The current repository has an
   Anthropic completion adapter, but the protocol does not select it; another
   text-completion adapter can be registered before execution. (The Agentic Identity Suite's
   "real" runs would still use mock embeddings — `AnthropicProvider.embed()`
   deliberately falls back to the deterministic mock — so its first results
   would be only partially real. It remains the second track.)
2. **Exact referee.** Every answer is scored by the same machinery the exact
   benchmarks use; there is no judgment call anywhere in the scoring.
3. **Divergent priors.** On the trap instances (below), a coverage heuristic
   scores ~0% and difference-set reasoning scores ~100%. Whatever the model
   does, the result is informative — that prior gap makes the experiment worth
   running where the earlier benchmarks mainly confirmed analytic expectations.

## Tasks (100 benchmark instances)

There are 100 nominal provider calls. The frozen one-retry policy permits at
most 200 calls only if every first attempt returns a provider/transport error;
all attempts are recorded.

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

The six traps vary their irrelevant table entries but share the same structural
difference. They are repeated opportunities to execute one deep witness pattern,
not six independent problem families. A positive result is therefore one bounded
data point, not evidence of general learned witness construction.

## Pre-registered predictions

Locked before the run. The maintainer's column is to be filled (or explicitly
waived) before the first real call — divergent recorded priors are the point.

| Metric | Floor | Forecast (Claude, protocol author, 2026-07-30) | Prediction (maintainer) | Result |
|:---|:---|:---|:---|:---|
| T1 consistency | — | ≥ 32/40 | | |
| T1 truth hits | ≈ 9.8/40 | within ±4 of 10/40 (no meaningful prior alignment) | | |
| T2 random: separates | 18/34 (do-nothing) | ≥ 27/34 | | |
| T2 random: cost-optimal | — | ≥ 20/34 | | |
| **T2 traps: separates** | **0/6** | **≥ 4/6** (difference-set reasoning, with arithmetic slips) | | |
| T3 identifies | 0/20 | ≥ 8/20 | | |
| T3 cost-optimal | — | ≥ 5/20 | | |

**Interpretation, fixed in advance.** Traps ≥ 4/6: zero-shot learned witness
construction succeeds on this registered pattern; OP14 gains one positive
bounded data point, and the next arm (transfer, multiple trap structures,
larger families, learned proposers in
the [referee workbench](../recursive-workbench/README.md)) is motivated.
Traps ≤ 1/6: the model behaves as a coverage heuristic where coverage
provably fails; the enumeration floor stands and "generation is not
construction" gets its first measured instance. 2–3/6: underpowered — the
follow-up registration must raise n before any conclusion is drawn. T1
consistency far below prediction would be the most surprising outcome of all
(constraint satisfaction with all constraints visible) and would dominate the
reading of everything else.

## Execution registration

The protocol and the execution target are separate freezes. The current
registration intentionally contains:

```json
{
  "status": "unregistered",
  "provider": null,
  "model": null,
  "maintainer_prediction": null
}
```

Choosing whether to run, and whom to call, is a later decision. Before the first
real call, one commit must set `status` to `frozen`, name the exact provider and
model, preserve the protocol digest above, and fill or explicitly waive the
maintainer prediction. Adding a provider adapter may change transport code, but
must not change the frozen task digest.

## Protocol details

- Model: selected only by the later execution registration; the exact model
  must come from that registration, never from an adapter default. One requested
  result per instance, with at
  most one recorded retry after a provider/transport error.
- Parse failures and provider errors count as failures in every rate and are
  reported separately. Only an exact eight-bit answer on the final non-empty
  line parses. The final-line formats and the parser in
  `learned_searcher.py` are part of this registration.
- Instance seed `0` is fixed in code and is not exposed by the CLI. The digest
  covers the system prompt, all rendered prompts, all instances, parser pattern
  and implementation, retry count, and exhaustive scores for every possible
  eight-bit answer.
- Token usage and request metadata are recorded when an adapter exposes them.
  Monetary cost is calculated after the run against the registered provider's
  price at the run date; no unsupported advance estimate is claimed.
- A real run requires a clean committed worktree and records its exact commit.

```bash
cd lab/benchmarks/learned-searcher
python learned_searcher.py --dry-run              # inspect instances and prompts
python learned_searcher.py --provider stub --out /tmp/learned-searcher-stub.jsonl

# Only after execution-registration.json is frozen for this exact target:
ANTHROPIC_API_KEY=... python learned_searcher.py --provider anthropic
```

## Related

- [Open Problem 14: Learned Witness Construction](../../../theory/reference/open-problems.md#open-problem-14-learned-witness-construction) — this is its zero-shot slice
- [Witness benchmark](../witness-generation/README.md) — the exact frontier and the trap construction
- [Inverse-reconstruction v1.2](../inverse-reconstruction/README.md) — why T1 truth recovery is capped at chance, and what the selection prior means
- [Referee workbench](../recursive-workbench/README.md) — where a learned proposer would slot in next
