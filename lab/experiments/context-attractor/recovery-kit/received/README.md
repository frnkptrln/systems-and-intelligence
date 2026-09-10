# Received E3/E4 submissions

The two partitions were supplied by the maintainer on 5 September 2026 and
recovered from [issue #59](https://github.com/frnkptrln/systems-and-intelligence/issues/59)
on 10 September. Both canonical intake files match the hashes published before
this recovery. All names, memberships and ordering are preserved.

| Submission | Families | Exact cover | Previously recorded intake SHA-256 |
|---|---:|---|---|
| [E3](E3/clusters.json) | 16 | 80/80, once each | `2590fdb8a70fe87943a6b2b07748eccad011ae369bfe553c3a0db1c738baccfb` |
| [E4](E4/clusters.json) | 15 | 80/80, once each | `a3cb96652c787eec196d629f3b52b56cd49d79e4c7f7881df7421e94170bdbbb` |

The [source comments](source-comments/5551863709.md) preserve the intake history;
the [maintainer clarification](source-comments/5551918663.md) establishes the
E3/E4 assignment and reports separate incognito sessions, both using Claude
Opus 5 / Hoch. The difference in family totals is not a comparison of models or
effort settings. [Provenance](provenance.json) distinguishes that attestation
from provider logs: exact internal revisions, session IDs, timestamps and
unexposed sampling settings were never recorded. No missing value is invented.
The source-comment files are API-returned text snapshots with terminal LF;
their hashes do not authenticate the original provider response.

[Preserved evidence](preserved-evidence.json) lists the SHA-256 of all 46 original
run files, verified unchanged against the repository when the submissions were
recovered. This includes the failed E1/E2 partitions and original partial
results. Nothing in the old run is overwritten.

## Recorded outcome

**Both existing submissions failed separate condition-blind semantic QC.**
The [E3 review](blind-qc/E3/review.json) and
[E4 review](blind-qc/E4/review.json) independently flag the same two substantive
mergers: Q022/Q032/Q077 address different scientific constructs despite a shared
measurement vocabulary; Q026/Q028/Q041/Q042/Q064 do not form one problem family
merely because they mention benchmarking repository implementations. E4's review
also identifies an unsupported split between closely related adversarial
robustness questions. Both reviews distinguish these failures from ordinary,
defensible boundary ambiguities and identify usable families as well.

These are AI-assisted reviews by two distinct Codex subagents, each started
with no conversation history and supplied only its one review packet. They are
not human expert review or independent model replication. The exact inherited
model snapshot was not separately exposed and is not invented. The
[QC receipt](blind-qc/receipt.json) records the actual task identities, packet
and response hashes, and coordinator receipt timestamps. Raw returned review
JSON is preserved without changing either submitted partition.

[The machine-readable disposition](recovery-result.json) is
`blind_semantic_qc_failed`. It is reproduced with:

```sh
python lab/experiments/context-attractor/aggregate_diversity_recovery.py lab/experiments/context-attractor/recovery-kit/received/blind-qc --output /tmp/context-recovery-result.json
```

The failed-QC path never reads the condition key or produces condition-specific
family counts. Run 001 remains `completed_partial`; P3/P4 remain unavailable,
and the original non-diversity evidence does not establish a harmful attractor.
This is a measurement-quality failure under the recorded AI review, not evidence
against or for the hypothesized context effect. The semantic judgments remain
open to a fresh blind expert assessment, but no partition is automatically
repaired, selected, retried, or used to close issue #59. Existing submissions,
their QC failures, and the exact remaining scientific limitation are now
recoverable from the repository.

## Blind QC and separate analysis

Generate independent review packets from the repository root:

```sh
python lab/experiments/context-attractor/complete_diversity_recovery.py --output /tmp/context-qc-packets
```

Give each reviewer only its one ZIP in a fresh context. The packet contains no
condition key, predictions, outcomes, prior score data, evaluator identity, or
other partition. A semantic review decides whether the existing grouping is
scientifically usable; it must not repartition the items. Preserve failures as
well as passes. AI reviewers must be described as AI reviewers, with their
actual model and session provenance; they do not constitute an external human
review or a new generation replication.

After both reviews finish, save their returned JSON as `E3/review.json` and
`E4/review.json` in a separate QC directory. Its `receipt.json` records the UTC
freeze timestamp as `frozen_at_utc`, plus `reviews.E3` and `reviews.E4`, each with
the actual `reviewer_id`, `model`, `fresh_context`, `completed_at_utc`,
`input_packet_sha256` and `output_sha256`. These fields implement the existing
[freeze-before-unblinding addendum](../recovery-addendum.md); they do not
authenticate claims of independence by themselves.

```sh
python lab/experiments/context-attractor/aggregate_diversity_recovery.py /tmp/context-qc-reviews --output /tmp/context-recovery-result.json
```

The analysis checks both pinned input packets and frozen review hashes. A
failed review yields a failed-QC report without reading the condition key.
Only two passing reviews allow analysis: it then verifies the 46 original
files and recomputes the non-diversity metrics before counting B and R families
separately for E3 and E4. Sign disagreements, including zero versus nonzero,
leave P3/P4 unresolved and require the existing blind adjudication step; no
average is used to conceal disagreement. Outputs must be new files.
