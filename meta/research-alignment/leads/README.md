# Leads — Externally Sourced Material

**Lane:** Research Alignment  
**Status:** Working repository policy — lane proposed 2026-09-02; its name and its retention policy are maintainer decisions  
**Created:** 2026-09-02  
**Last reviewed:** 2026-09-02  
**Review trigger:** the first month in which an automated run feeds the lane; any change to the columns of the [Related Work Map](../related-work-map.md) or to the shape of a claim register.

This directory is the one place in the repository where externally sourced material is recorded
before anyone has judged it. Everything else — matrix rows, registers, status lines, `ideas/` —
changes only through a change the maintainer authors.

---

## What a lead is

A lead is a pointer to a paper, preprint, or result found outside the repository, recorded with:

- **Source:** the arXiv identifier or DOI. This is the deduplication key.
- **Result:** one sentence on what the source reports.
- **Bears on:** which row of the [Related Work Map](../related-work-map.md#2-concept-to-literature-matrix)
  or which claim in [Core Claims](../../repository-meta/core-claims.md) or
  [Identification Claims](../../repository-meta/identification-claims.md) it supports or
  challenges, in one word: *supports* or *challenges*.
- **Why:** one sentence.

A lead is not an idea, not evidence, not a claim, and not a status change. Recording a lead asserts
nothing about the repository; it records that a source exists and where it would land if the
maintainer took it up.

## Shape

One file per month, named `YYYY-MM.md`, append-only within the month. Each month file has two
parts:

1. an `## IDs` list — the identifiers of every lead in the file, one per line;
2. the entries, in the order they were recorded;
3. optionally, a `## Month-end note` written by the maintainer, or the single empty-month line
   from rule 4.

An entry has this form:

```markdown
### YYYY-MM-DD · arXiv:NNNN.NNNNN
- **Source:** Authors (year), *Title*, arXiv:NNNN.NNNNN.
- **Result:** one sentence.
- **Bears on:** Related Work Map row "…" — supports | challenges.
- **Why:** one sentence.
- **Recorded by:** maintainer | intake run | example (drafted for review)
```

`Bears on` may name a register claim instead of a matrix row. It names exactly one target. A source
that seems to bear on several rows is recorded once, against the row where the placement can be
stated most specifically; the maintainer can add the rest.

## Rules

1. **Leads never write outside the lane.** Matrix rows, registers, status lines, and `ideas/`
   change only through a maintainer-authored change. A lead entry may link to the row or claim it
   bears on; nothing links back until the maintainer decides.
2. **Recurrence is a prompt for the maintainer, not evidence.** The lane may record, in a
   maintainer-written month-end note, that a topic reappeared. Nothing else in the repository may
   cite that recurrence. The lane adopts the distinction that
   [A Research Loop Can Become Its Own Environment](../../../ideas/2026-08-10-research-loop-becomes-environment.md)
   proposes: a claim should become stronger only when something new crosses an evidence-bearing
   boundary, and a topic reappearing in the lane is internal propagation.
3. **Past leads are input to deduplication only, never to relevance judgment.** An intake run reads
   the `## IDs` lists to avoid recording a source twice. It does not use entry bodies, and it does
   not let earlier leads shape what counts as relevant now. Memory also changes the distribution
   from which later questions are generated
   ([Persistence Can Narrow the Search Space](../../../ideas/2026-08-11-persistence-can-narrow-search-space.md));
   the lane keeps that distribution out of the intake run's relevance judgment, so that the loop
   does not read its own prior output to decide what matters
   ([A Research Loop Can Become Its Own Environment](../../../ideas/2026-08-10-research-loop-becomes-environment.md)).
4. **Empty months are recorded as empty.** A month in which nothing passed the relevance bar ends
   with the single line `No lead passed the relevance bar in YYYY-MM.` Quiet is a valid result.
5. **Rolling retention.** At year end, each month file is either summarized into one paragraph or
   kept whole. The maintainer decides, file by file. Nothing is deleted before that decision, and a
   summarized file keeps its `## IDs` list verbatim so that deduplication still works.
6. **Who writes.** The maintainer, by hand, or an automated intake run following
   [Lead Intake Task](../lead-intake-task.md), which opens a change against the current month's
   file and nothing else. The intake run creates the month file on the first run of a month, with
   the header, an empty `## IDs` list, and an `## Entries` heading. This is a write inside the lane
   because the lane is exempt from the corpus and file counts that the freshness audit pins in
   [`docs/repository-map.md`](../../../docs/repository-map.md) (maintainer decision D4 of
   2026-09-02; the audit change lands in a separate change).

## Where a lead goes next

Nothing automatic. The maintainer may turn a lead into an edit of a matrix row, a note under a
register claim's failure condition, an `ideas/` note, or nothing. The lane keeps the record either
way, so a source that was seen and set aside is not mistaken later for a source that was never seen.

## Relation to the maintainer's notes on loops

The rules above are taken from the repository's own notes, not invented for the lane:

- write boundaries and an evaluator the loop cannot rewrite —
  [Self-Improvement Needs a Referee](../../../ideas/2026-07-24-self-improvement-needs-a-referee.md)
  and [Log 020](../../../logs/020_the-referee-boundary.md);
- internal recurrence is not external confirmation —
  [A Research Loop Can Become Its Own Environment](../../../ideas/2026-08-10-research-loop-becomes-environment.md);
- memory can narrow the search space —
  [Persistence Can Narrow the Search Space](../../../ideas/2026-08-11-persistence-can-narrow-search-space.md);
- accumulated traces need an invalidation boundary —
  [Experience Needs an Invalidation Boundary](../../../ideas/2026-08-22-experience-needs-an-invalidation-boundary.md);
- which information, write, and veto rights remain separated is the question that keeps a loop
  from validating its own preferred explanation —
  [Mechanistic Discovery Needs Methodological Separation](../../../ideas/2026-08-22-mechanistic-discovery-needs-methodological-separation.md).

## Files

- [`2026-09.md`](2026-09.md) — the first month file, with one example entry drafted for review.
- [Lead Intake Task](../lead-intake-task.md) — the instruction text for a scheduled run. Nothing is
  scheduled as of 2026-09-02.
