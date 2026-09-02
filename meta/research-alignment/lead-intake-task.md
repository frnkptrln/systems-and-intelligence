# Lead Intake Task — Instruction Text for a Scheduled Run

**Lane:** Research Alignment  
**Status:** Draft — instruction text only; nothing is scheduled as of 2026-09-02  
**Created:** 2026-09-02  
**Last reviewed:** 2026-09-02  
**Review trigger:** the first scheduled run; a change to the [leads lane](leads/README.md) rules; a change to the matrix columns or a register's shape; an arXiv API or Hugging Face API change.

This document is the complete instruction text for an automated paper-watch run that delivers into
the [leads lane](leads/README.md). It exists so that the task can be reviewed as a repository
document before anything is scheduled. The text between the two rules below is the instruction; the
rest is context for the maintainer.

Scheduling it, choosing the runner, and choosing the model are maintainer decisions. None was made
on 2026-09-02.

---

## Instruction text

> You are running the lead intake task for the repository `frnkptrln/systems-and-intelligence`.
> Your only output is at most three entries appended to one file,
> `meta/research-alignment/leads/YYYY-MM.md`, for the current month, delivered as a pull request.
> You write nothing else, anywhere; the one exception is creating that month file when the month has
> just begun.
>
> **1. Boundary first.** Before searching, check whether `meta/research-alignment/leads/YYYY-MM.md`
> exists for the current month. If it does not, create it in the same pull request with the lane's
> month-file header, an empty `## IDs` list, and an `## Entries` heading; the lane is exempt from the
> repository's file and word counts. You create no other file. You do not touch `docs/repository-map.md`,
> `meta/research-alignment/related-work-map.md`, either claim register, any file under `ideas/`,
> `theory/`, `lab/`, or `logs/`, any status line, this instruction file, or the lane's `README.md`.
> You run no benchmark and make no model call inside `lab/experiments/active_identifiability/`.
>
> **2. Read the targets, once.** Read the concept-to-literature matrix in
> `meta/research-alignment/related-work-map.md` (section 2), and the claims in
> `meta/repository-meta/core-claims.md` and `meta/repository-meta/identification-claims.md`. For
> each matrix row note its "What would weaken repo claim" and "Suggested next empirical test"
> columns; for each register claim note its failure condition. These are the only relevance targets.
>
> **3. Deduplicate against identifiers only.** Extract the identifiers from every file in
> `meta/research-alignment/leads/` by pattern: lines beginning `- arXiv:` under `## IDs`. Strip
> arXiv version suffixes (`v2`) before comparing. Do not use entry bodies, and do not use anything
> in those files to decide what is relevant.
>
> **4. Collect candidates.** Run the three source queries below for the window `<from>`–`<to>`
> defined under Sources. Keep title, identifier, submission date, and abstract for each result.
>
> **5. Apply the relevance bar to each candidate.** A candidate passes only if all five hold:
>
> 1. It has a primary artifact: an arXiv identifier, and you have read its abstract. A DOI-only
>    source is recorded by the maintainer by hand, not by this run.
> 2. Its reported result can be placed against at least one target: a matrix row's
>    support/challenge, "what would weaken," or "next empirical test" column, or a register
>    claim's failure condition. If several targets fit, record it once against the one where the
>    placement is most specific, as the lane README rules.
> 3. That placement can be written as one sentence using only the target's own vocabulary. If the
>    sentence needs a term that is not in the target, the candidate fails.
> 4. The source reports a result — a measurement, a theorem, or a method with a released artifact.
>    A survey, a position paper, or an announcement fails.
> 5. The placement is more than topical overlap: the candidate must either report something the
>    target's column names as support, as a weakening condition, or as a next test, or contradict
>    something the target states. Sharing anchor citations or vocabulary with the target is not
>    enough.
>
> If more than three candidates pass, keep the three earliest by submission time, count the rest as
> dropped, and report that count in the pull-request description. Do not rank leads by merit
> anywhere.
>
> **6. Write the entries.** Append each passing candidate to the end of the month file in exactly
> this form, and insert its identifier as a new line at the end of the file's `## IDs` list with a
> line-anchored edit:
>
> ```markdown
> ### YYYY-MM-DD · arXiv:NNNN.NNNNN
> - **Source:** Authors (year), *Title*, arXiv:NNNN.NNNNN.
> - **Result:** one sentence.
> - **Bears on:** Related Work Map row "…" — supports | challenges.
> - **Why:** one sentence.
> - **Recorded by:** intake run
> ```
>
> `Bears on` may instead name `Core Claims, Claim N` or `Identification Claims, Claim N`. It names
> one target. Use *supports* or *challenges*; no third word.
>
> **7. Deliver.** Open a pull request from a branch named `leads/YYYY-MM-DD` whose diff touches
> only `meta/research-alignment/leads/YYYY-MM.md`. Its description lists the identifiers recorded,
> the number of candidates screened, the number that passed, and the number dropped by the cap. It
> contains no summary of the sources and no recommendation.
>
> **8. If nothing passed**, open no pull request and report exactly:
> `No findings: no candidate passed the relevance bar on YYYY-MM-DD (N screened).`
> On the last weekday of a month in which the month file has no `### ` entry heading, open one
> pull request appending the single line `No lead passed the relevance bar in YYYY-MM.` to that
> file.
>
> **9. Refuse these, always.** Stop and report rather than do any of the following:
>
> - promoting a lead: writing it into `ideas/`, the matrix, a register, a theory page, or anywhere
>   other than the month file;
> - editing any status line, anywhere;
> - citing recurrence: writing that a topic "keeps appearing," "is trending," or "has come up
>   before," in the lane file or the pull-request description;
> - reading prior leads' entry bodies, or using their identifiers, to judge relevance;
> - inferring relevance from how often the repository mentions a topic;
> - creating any file other than the current month's lane file;
> - editing `docs/repository-map.md` or any copied count;
> - recording more than three entries in one run, or ranking entries by merit in the lane file or
>   the pull-request description;
> - summarizing, rewriting, or reorganizing the lane;
> - running a benchmark, or calling a model under `lab/experiments/active_identifiability/`;
> - opening a pull request against any branch other than the default branch, or pushing to `main`;
> - editing this instruction text.

---

## Sources

The three queries. Dates are filled in at run time, both as `YYYYMMDDHHMM` in UTC: `<to>` is now;
`<from>` is 48 hours before the last successful run's `<to>`. The overlap exists because arXiv lists
a submission only after its next announcement cycle, so a window that ended at run time would miss
papers submitted after the previous cutoff; the `## IDs` deduplication absorbs the repeats.

### arXiv, model-identification arc

```text
https://export.arxiv.org/api/query
  ?search_query=
    (cat:cs.LG OR cat:stat.ML OR cat:cs.AI OR cat:eess.SY OR cat:cs.SY OR cat:math.DS OR cat:nlin.AO OR cat:q-bio.QM)
    AND (abs:identifiability OR abs:"system identification" OR abs:"observational equivalence"
         OR abs:"equivalence class" OR abs:"distinguishing sequence" OR abs:"experimental design"
         OR abs:"active learning" OR abs:"causal discovery" OR abs:"world model")
    AND (abs:intervention OR abs:interventions OR abs:query OR abs:queries
         OR abs:"partial observability" OR abs:witness OR abs:counterexample)
    AND submittedDate:[<from> TO <to>]
  &sortBy=submittedDate&sortOrder=descending&max_results=100
```

### arXiv, viability arc

```text
https://export.arxiv.org/api/query
  ?search_query=
    (cat:cs.AI OR cat:cs.MA OR cat:cs.CY OR cat:cs.LG OR cat:nlin.AO OR cat:physics.soc-ph OR cat:econ.TH OR cat:eess.SY)
    AND (abs:viability OR abs:"reward hacking" OR abs:"specification gaming" OR abs:Goodhart
         OR abs:"human oversight" OR abs:"safe reinforcement learning" OR abs:"resource-bounded"
         OR abs:"action budget" OR abs:"self-improving" OR abs:"self-improvement")
    AND (abs:constraint OR abs:constraints OR abs:regulator OR abs:oversight OR abs:evaluator
         OR abs:"held-out")
    AND submittedDate:[<from> TO <to>]
  &sortBy=submittedDate&sortOrder=descending&max_results=100
```

The two queries are one per arc of the README spine. Their terms are drawn from the matrix rows,
the registers, and the language-anchor table in the Information Architecture; the anchor-side terms
extend the matrix vocabulary and are a maintainer choice. Widening a query is a maintainer edit to
this file, not a run-time choice.

### Hugging Face daily papers

`https://huggingface.co/api/daily_papers?date=YYYY-MM-DD` for each date in the `<from>`–`<to>`
window, or the equivalent listing `hf://papers/daily/<date>` where a Hugging Face connector is
available. Each paper's arXiv
identifier is the dedupe key; the abstract is fetched from arXiv, not taken from the listing.

## Cadence

Weekdays, once, at a fixed hour. No weekend runs. A missed run is not made up separately; the next
run's window starts 48 hours before the last successful run's `<to>`, as defined under Sources.

## Why the bar is a test and not a judgment

The relevance bar asks a candidate to land on a column the maintainer has already written — a
weakening condition, a next test, a failure condition. It does not ask the task whether the source
is interesting, important, or on-trend. That keeps the task's judgment inside the maintainer's
stated frame and keeps the lane from becoming a second, automated `ideas/`.

## What this document does not do

- It does not schedule anything, choose a runner, or choose a model.
- It does not authorize the task to widen its sources, its cap, or its write boundary.
- It does not make the lane's contents evidence. See the [lane rules](leads/README.md).
