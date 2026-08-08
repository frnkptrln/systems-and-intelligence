# Freshness and Review

**Lane:** Repository Meta  
**Status:** Working repository policy  
**Created:** 2026-08-08  
**Last reviewed:** 2026-08-08

This repository is a living research notebook. That makes **staleness an epistemic failure mode**, not
just a documentation problem. A statement can have been carefully sourced when written and still
become misleading later because a model changed, a company changed direction, a result was
replicated or weakened, or a provisional research programme became obsolete.

The goal is not to make every page permanently current. The goal is to make it clear **which claims
are meant to describe a changing present, when they were last checked, and what should cause them to
be checked again**.

---

## 1. What needs freshness handling

Freshness metadata is expected when a page relies on claims whose truth or interpretation can change
without the repository changing, including:

- current model capabilities, names, defaults, APIs, or product behavior;
- company strategies, governance structures, safety policies, or research programmes;
- laws, standards, institutional rules, prices, schedules, or deployment conditions;
- claims that a result is "new," "recent," "unreplicated," "state of the art," or the latest work;
- comparisons between active labs, vendors, models, benchmarks, or platforms; and
- synthesis whose argument depends on the current state of an external research field.

Freshness handling is normally unnecessary for:

- established mathematical definitions and proofs;
- frozen results produced by repository experiments with recorded code and parameters;
- historical claims stated with an absolute date; and
- explicitly version-locked research history.

---

## 2. Minimal metadata

A time-sensitive synthesis should carry, near the top:

```text
Last reviewed: YYYY-MM-DD
Review trigger: <event that would materially change the reading>
```

Frontmatter is preferred when the document already uses it. A visible status block is sufficient
otherwise.

`Last reviewed` means the time-sensitive external claims were checked against appropriate sources.
It does **not** mean every argument in the page was re-proved.

A review trigger should be concrete. Examples:

- a replication or failed replication of the cited result;
- a materially different interpretability instrument;
- a new model family that breaks the comparison;
- a provider changing an API or default model;
- a company replacing a published governance or safety framework; or
- a repository result that invalidates a dependency of the page.

---

## 3. Prefer absolute time over relative time

Avoid unqualified phrases such as:

- `today`
- `currently`
- `now`
- `recently`
- `weeks old`
- `the latest`

when the phrase is doing evidential work.

Prefer:

> As of 2026-08-08, the cited source reports ...

or:

> The result was published on 2026-07-06; this note last checked its external status on 2026-08-08.

Relative language is fine inside a dated log when its historical frame is unambiguous. It should not
silently survive into a synthesis that presents itself as current.

---

## 4. Separate snapshot, evidence, and interpretation

For changing external subjects, keep three layers distinct:

1. **Snapshot:** what a source or system said or did at a declared date.
2. **Evidence:** what was actually measured, released, or documented.
3. **Repository interpretation:** what the project infers from that evidence.

Do not turn a temporary company strategy into an ontology of its models. Do not turn one model
release into a permanent vendor characteristic. Do not turn a research instrument into the thing it
measures.

The 2026-03-07 version of
[Asimov's Paradox in the Age of AI](../../theory/narrative/asimov-ai-latent-thinking.md) is the first
explicit case study for this rule: a clean Anthropic/OpenAI symmetry became misleading within five
months even though the underlying questions about introspection and latent computation remained
useful.

---

## 5. Review by epistemic risk, not by file age

A page does not become wrong because it is old. Review priority depends on how much a stale claim can
misdirect later work.

### Tier A — load-bearing and time-sensitive

Examples: current vendor/model comparisons, active safety frameworks, claims of state of the art,
current legal or deployment assumptions.

- Add `Last reviewed` and a review trigger.
- Recheck before the claim is reused in a paper, canonical synthesis, benchmark protocol, or public
  comparison.
- A 90-day review interval is a useful default when no event trigger is better.

### Tier B — external research anchors

Examples: a recent interpretability result used to motivate an open problem.

- Record publication date and source.
- Recheck when a replication, critique, competing instrument, or relevant follow-up appears.
- A 180-day review interval is a useful fallback, not an expiry date.

### Tier C — historical or internally frozen

Examples: an Asimov reading, a mathematical theorem, or a repository experiment tied to a commit.

- Preserve the date and provenance.
- No periodic freshness review is required unless the page is promoted into a changing-present
  claim.

---

## 6. Preserve research history without letting it control the present

When a claim ages badly, do not silently erase the earlier reasoning if it is useful research
history.

Prefer one of three moves:

1. **Rewrite the canonical synthesis** and include a dated note explaining what changed.
2. **Version-lock the old artifact** and point readers to the replacement.
3. **Downgrade the claim** from current synthesis to historical or exploratory status.

The repository should remember corrections, but later retrieval should preferentially encounter the
corrected state rather than the superseded one.

This matters because the repository is itself part of the effective control state of the research
process: old terminology, summaries, and central links change what later human and AI work is likely
to retrieve.

---

## 7. Maintenance pass for a time-sensitive page

When reviewing one page:

1. Identify every claim that describes a changing present.
2. Recheck those claims against primary sources where possible.
3. Replace relative recency language with absolute dates.
4. Separate measured result from interpretation.
5. Check whether the page's organizing contrast still exists.
6. Inspect obvious downstream summaries and backlinks for the stale formulation.
7. Record `Last reviewed` and a useful review trigger.
8. If uncertainty remains, narrow or downgrade the claim instead of manufacturing freshness.

A freshness pass is not a request to rewrite everything. The smallest correct change is preferred.

---

## 8. First application: 2026-08-08

This policy was introduced while reviewing the March 2026 narrative essay that opposed Anthropic's
"visible introspection" to OpenAI's "latent thinking." By August 2026, Anthropic had published work
on introspection adapters and workspace-like internal representations, while OpenAI had a substantial
chain-of-thought monitorability programme. The durable distinction was therefore not between the two
companies but between different observation and intervention channels.

The revised essay now treats company research as dated evidence for a more stable taxonomy:

- external mechanistic interpretability;
- elicited introspective report;
- reasoning traces;
- causally effective self-models; and
- reflexive intervention.

That is the intended maintenance pattern: **keep the question when it survives; replace the snapshot
when it does not.**
