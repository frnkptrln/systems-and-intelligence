# What Stays in the Repository

**Status:** Orientation page. It describes the boundary between this site and the repository behind it.

This site is not the repository. The repository holds roughly 250,000 words across 272 Markdown files — about twenty hours of reading. Publishing all of it was the old arrangement, and it made the site unreadable: a first-time reader had no way to tell which five percent carried the argument.

So the site now publishes the part that is finished enough for someone who has not been following along. Everything else stays where it was written, next to the code it describes, and stays linked — any link on this site that points at an unpublished page goes to the file on GitHub instead of breaking.

Nothing here is hidden. It is simply not competing for your attention.

## What the site publishes

| Layer | On the site | Why |
|---|---|---|
| Theory | 34 essays of 84 | The ones the project's own claim documents actually cite |
| Reference | 4 | Glossary, open problems, limitations, and the negative space |
| Papers | 2 of 2 | Bounded, citable, with a frozen claim set |
| Stories | 19 of 19 | Self-contained and written for outside readers |
| Benchmarks | 6 result pages | The measured evidence behind the claims |
| Interactive | 3 | They only work on the web |

## What stays in the repository

### Simulation models — 45 READMEs

[`simulation-models/`](https://github.com/frnkptrln/systems-and-intelligence/tree/main/simulation-models)

Run instructions and short notes averaging under 300 words each: Boids, Kuramoto, self-organized criticality, Lenia, IFS, L-systems, TEO Civilization, the agent ecology, and the rest. They belong beside the code they start, not in a reading sequence. Where the simulations bear on a claim, that connection is made on the site in [Simulation → Theory Map](../theory/core/simulation-theory-map.md).

### Architecture logs — 21 notes

[`logs/`](https://github.com/frnkptrln/systems-and-intelligence/tree/main/logs)

Dated working notes on system design — the planetary compiler, provenance depth, latency as mercy, who pays for the veto. They are a thinking record, and they read like one. Numbered in the order they were written.

### Lab tooling and scaffolds

[`lab/`](https://github.com/frnkptrln/systems-and-intelligence/tree/main/lab)

The orchestration layer, the provider layer, the inverse-search scaffold, the benchmark scenario schemas, and the six cognitive stress-test scenarios. The benchmark *results* are published; the machinery that produces them is here.

### Repository meta

[`meta/`](https://github.com/frnkptrln/systems-and-intelligence/tree/main/meta)

The information architecture, the concept registry, the agent operating note and the prompt seed it superseded, the red-team manual, the canonical path, the research-alignment map, and the leads lane. These are instructions to the author and to the agents working on the repository — addressed to whoever is writing, not to whoever is reading.

### Early book chapters

[`book/`](https://github.com/frnkptrln/systems-and-intelligence/tree/main/book)

Ten short chapters, about 500 words each, written before the foundations audit. [From Rule to Mind](../book/09_from_rule_to_mind.md) survives on the site as the linear route through the current material; the earlier chapters remain as a record of how the argument used to be told.

### Theory essays not on the reading path — 50

[`theory/`](https://github.com/frnkptrln/systems-and-intelligence/tree/main/theory)

Sketches, speculative branches, and essays whose vocabulary the foundations audit superseded. Close to half of the theory files are under 800 words. Some will grow into published essays; some are notes that did their work by being written. The ones marked `legacy` or `superseded` are kept because the audit trail matters, not because they should be read first.

### Exploratory notes

[`ideas/`](https://github.com/frnkptrln/systems-and-intelligence/tree/main/ideas)

Dated first drafts of thoughts, never part of the site.

## How to read the boundary

If a page is on this site, it is being offered as ready. If it is in the repository only, it is working material — real, kept, and available, but not yet something the project is asking anyone to read in order.

That distinction is the whole point. A research notebook that publishes everything cannot say *this part is finished*, because publishing is the only way it has to say it.
