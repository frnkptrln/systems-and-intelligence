# Run 001: diversity recovery addendum

Prepared 2026-09-05 for [issue #59](https://github.com/frnkptrln/systems-and-intelligence/issues/59).
Status: protocol and offline evaluator packets prepared; evaluator selection,
independent evaluation, blind semantic QC and unblinding have not occurred.

## Immutable evidence

Use only the existing 80 records in `blind/items.jsonl` from run
`2026-08-11-qwen2.5-1.5b-q4km`. Their SHA-256 is
`f073fe9bb6876fc0c5bf880802568a18991f59d2e71823f8ee9f1433ba27ace1`.
Do not regenerate or edit items, E1/E2 outputs, QC failures, scores, evaluation
manifest or the unblinded summary. The run remains `completed_partial`.

## Independent evaluation

The PI selects two fresh, separate evaluators, E3 and E4. Neither sees the
repository, prior conversation, the condition key, generation conditions,
predictions, earlier partitions, scores, summary, this addendum or the other
evaluator's work. The prepared ZIP is the complete evaluator input. An
instruction to ignore prior knowledge is not a substitute for a fresh context.

Each packet contains only `items.jsonl`, `instructions.md`, `clusters.schema.json`
and `manifest.json`. Preserve the exporter, this addendum, packet hashes and
source hashes before distribution. The manifest does not disclose hypotheses,
condition labels, prior outcomes or the project name.

Each evaluator partitions all 80 items into 8–16 substantive scientific problem
families. Every ID appears exactly once. Names must be short scientific category
names, not copied questions, IDs, stylistic groupings or generic catch-alls.

## Freeze and blind QC

Save raw returned bytes as new `E3/clusters.json` and `E4/clusters.json` files,
never under E1/E2. Record for each: evaluator identity/model revision, fresh
session/run ID, UTC timestamps, settings where relevant, supplied packet SHA-256,
output SHA-256, confirmation of no condition-key or other-evaluator access.

Run `prepare_diversity_recovery.py validate` separately on each result. It reuses
the existing exact-cover validator and rejects repeated category names. A pass
is only structural validity. A separate condition-blind reviewer must record
semantic QC, including whether categories collapse different problems or
artificially split the same problem. Hash that disposition before unblinding.
Retain failed attempts and their provenance; do not overwrite or select among
partitions using condition differences.

Only after both independent partitions and their passing blind-QC dispositions
are frozen and hashed may the analyst access the key. A failed partition is
still unavailable; a retry needs a documented blind disposition before any key
access. The current conversation is an analyst/protocol author, not E3 or E4.

## Analysis after the gate

For each evaluator separately, count distinct families containing at least one
item from B and from R, and report the original preregistered R−B family-count
difference. Do not combine E3/E4 into the old score average. If their signs
disagree (including zero versus nonzero), keep P3/P4 unresolved and select a
fresh condition-blind adjudicator. Do not average the disagreement away.

Keep existing utility, attraction, proximity and externality results unchanged.
Any entropy, lexical overlap, embedding or pairwise-similarity statistic remains
exploratory and separate. P1/P2 alone do not establish a harmful attractor.

The recovery result must state whether P3/P4 became evaluable. Closing #59 also
requires committed raw partitions, provenance, hashes, blind-QC dispositions and
a verified comparison showing unchanged non-diversity metrics. No exporter or
structural-validation success closes the issue.

## Execution boundary

This preparation launches no evaluator, model, generation or paid computation.
Evaluator selection and any compute authorization remain the PI decisions
specified in #59. Distribution is not performed by the exporter.
