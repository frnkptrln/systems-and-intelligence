# Agent Operating Note

**Lane:** Repository Meta (governance). Filed under `conceptual-meta/` because it supersedes the prompt seed kept there; the maintainer may move it.  
**Status:** Working repository policy — proposed 2026-09-02  
**Created:** 2026-09-02  
**Last reviewed:** 2026-09-02  
**Review trigger:** a change to the README spine table, to either claim register, to the CI gate, or to [Freshness and Review](../repository-meta/freshness-and-review.md).  
**Supersedes:** [Agent Prompt Seed](agent-prompt-seed.md) (in the repository since 2026-07-20), which does not reference the Foundations Reconstruction, is dated by the maintainer to before the foundations audit (the visible git history starts with both in the same commit), and binds an agent to the [Symbiotic Nexus Protocol](../../theory/human-organism-silicon-age/symbiotic-nexus-protocol.md), a document the repository itself marks as exploratory architecture.

This note says what an agent working inside this repository reads first and what it must not do.
It is addressed to whoever is writing, not to whoever is reading. It adds no claim and decides
nothing. The maintainer is the only person who decides what the repository claims.

---

## Role

The repository is a single-maintainer living research notebook. An agent's work here is structural
unless the maintainer says otherwise: keep the routing layer consistent with the spine, keep the
registers linked to artifacts, keep history visible. An agent does not add research results, does
not strengthen or weaken a claim, and does not decide what is load-bearing. Where a judgment is
needed, it proposes the judgment in the change description and stops.

The repository changes almost daily. Treat any statement about its state, including the ones in
this note, as a hypothesis to re-verify at the start of a session.

## Read first, in this order

1. [`README.md`](../../README.md) — the spine: Foundation / Model identification / Viability. Two
   bounded questions.
2. [Foundations Reconstruction](../../theory/core/mathematical-axioms.md) — has precedence over
   every legacy universal claim where they conflict.
3. [The Generator Question](../../theory/core/the-generator-question.md) — how a superseded framing
   is kept as history without being erased. This is the pattern for every "mark, don't delete"
   edit.
4. [Core Claims](../repository-meta/core-claims.md) and
   [Identification Claims](../repository-meta/identification-claims.md) — the two registers. Their
   shape (claim, non-obvious implication, artifacts by evidential kind, current status, failure
   condition) is the template for any new claim.
5. [Repository Information Architecture](../repository-meta/repository-information-architecture.md)
   — the routing document: lanes, synthesis list, language anchors, decision rules.
6. [Freshness and Review](../repository-meta/freshness-and-review.md) — header format and
   staleness rules for meta documents.
7. [Feynman Mode](../repository-meta/feynman-mode.md) and the
   [Concept Registry](../repository-meta/concept-registry.md) — the required pass for anything
   load-bearing.
8. [`ideas/README.md`](../../ideas/README.md) and the maintainer's notes on loops, memory, and
   observation:
   [Experience Needs an Invalidation Boundary](../../ideas/2026-08-22-experience-needs-an-invalidation-boundary.md),
   [Mechanistic Discovery Needs Methodological Separation](../../ideas/2026-08-22-mechanistic-discovery-needs-methodological-separation.md),
   [Polycontextural Observation Needs Translation Rules](../../ideas/2026-08-22-polycontextural-observation-needs-translation-rules.md),
   [A Research Loop Can Become Its Own Environment](../../ideas/2026-08-10-research-loop-becomes-environment.md),
   [Persistence Can Narrow the Search Space](../../ideas/2026-08-11-persistence-can-narrow-search-space.md).
   Any automated task proposed for this repository must satisfy them.
9. [Related Work Map](../research-alignment/related-work-map.md) — the concept-to-literature
   matrix. External leads are filed through the [leads lane](../research-alignment/leads/README.md),
   never into the matrix directly.
10. The measured artifacts of the identification arc:
    [Inverse-Reconstruction Benchmark, "The honest finding"](../../lab/benchmarks/inverse-reconstruction/README.md#the-honest-finding),
    [The Witness Principle](../../theory/core/the-witness-principle.md),
    [Decision-Relevant Identifiability](../../theory/core/decision-relevant-identifiability.md),
    [Active Identifiability](../../lab/experiments/active_identifiability/README.md).
11. [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) and
    [`lab/tools/audit_repository_freshness.py`](../../lab/tools/audit_repository_freshness.py) —
    what CI enforces.

## Invariants

### Epistemic

- Every non-code document keeps or gets a status line near the top, in the vocabulary of
  [Information Architecture §8](../repository-meta/repository-information-architecture.md#8-minimal-maturity-tags-recommended)
  or one of the richer forms already in use. Never move an existing status to a stronger or weaker
  level. If a status looks wrong, say so in the change description.
- The Foundations Reconstruction takes precedence over legacy universal claims. Legacy text is
  marked as research history, never deleted. Git history is not a substitute for visible marking.
- No new primitives. No new load-bearing term without a Feynman Mode pass and a Concept Registry
  entry in the same change ([Information Architecture §7](../repository-meta/repository-information-architecture.md#7-decision-rules-quick-triage)).
- A claim exists in a register only if it links to an existing artifact and states a failure
  condition. No artifact, no claim.
- `fiction/`, `logs/`, and `book/` are not evidence and are never cited as support for a claim.
- Numbers are frozen results. Do not re-run benchmarks to refresh them. Do not edit any headline
  that a regression test pins: the corridor paper's Appendices C and D, the benchmark headlines,
  and the held-out == ceiling invariant.
- `lab/experiments/active_identifiability/`: the committed protocol authorizes no model calls.
  Make none.

### Structural

- One home per artifact; cross-link, do not duplicate
  ([Information Architecture §9](../repository-meta/repository-information-architecture.md#9-anti-entropy-rules)).
- Every Markdown file added to a published layer goes into the MkDocs nav;
  `lab/tools/validate_nav.py` and `mkdocs build --strict` must pass. `meta/` is excluded from the
  site by the editorial rule in `mkdocs.yml`, so a meta page enters the nav only when it is
  deliberately re-included there, as the two registers are.
- The freshness audit checks copied corpus counts and derived counts. Adding or removing a
  Markdown file changes the file count in [`docs/repository-map.md`](../../docs/repository-map.md);
  run the audit and sync every count it flags.
- New meta documents carry the [Freshness and Review](../repository-meta/freshness-and-review.md)
  header block: Lane, Status, Created, Last reviewed, Review trigger.

### Process

- One branch per work package, prefixed by kind (the history shows `docs/`, `research/`, `fix/`,
  `site/`, and `agent/` in use): `docs/…` for routing and meta edits; `research/…` only for changes
  under `theory/` or `lab/`. Never work on `main`.
- Small changes. Each change description states: what changed; what was marked superseded, with the
  exact sentence used; what was not done and why; and the decisions reserved for the maintainer.
- No `Co-Authored-By` trailers. No self-attribution in commits or change descriptions.
- If the gate fails on something the change did not touch, report it. Do not fix it in the same
  change.

## The local gate

Install `requirements-dev.txt` and `requirements-docs.txt`, then run the full gate before every
push. It is the part of CI that runs without the paper build (`python lab/tools/build_paper_pdf.py`),
the KaTeX check (`node lab/tools/validate_katex.js site`), and the optional PyTorch tests; run those
too when a change touches `papers/`, math rendering, or model code under `lab/`.

```bash
pytest tests/ -q
pytest tests/test_referee_invariant.py -q
python lab/tools/validate_links.py
python lab/tools/audit_repository_freshness.py --strict
python lab/tools/validate_nav.py
python lab/tools/validate_math.py
mkdocs build --strict
```

If `pytest` on the path is bound to a different interpreter than `python`, use `python -m pytest`
for the first two lines.

## Decisions reserved for the maintainer

Propose these in a change description; never apply them.

- Whether the identification register stays a separate file or becomes part of Core Claims.
- Which candidate claims are load-bearing enough to be claims at all.
- Whether Information Architecture §5's control-plane simulation is still the next proof artifact.
- The name and retention policy of the leads lane.
- Any status change on any existing document.
- Whether anything under `theory/teo-framework/`, `theory/veto/`, `theory/symbiotic/`, or
  `theory/human-organism-silicon-age/` should be re-ranked in the directory structure.

## Relation to the superseded seed

The [Agent Prompt Seed](agent-prompt-seed.md) asked an agent to reject pure efficiency, test every
proposal against a biological veto, leave room for manual overrides, and name its own blind spot.
Those are architecture commitments of the viability arc's exploratory branch, and the seed bound an
agent to them as a system prompt. This note replaces that binding with the repository's own
epistemic and structural rules. The seed stays where it is, marked superseded, as a record of how the
agent-facing layer used to be told.
