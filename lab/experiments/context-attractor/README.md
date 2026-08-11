# Context Attractor — does research memory narrow exploration?

**Status:** preregistered exploratory protocol — no result yet

## Question

Does accumulated research context make generated research questions more useful while also pulling them toward the repository's existing conceptual structure?

The motivating external result is Tang & Yang (2026), *AI Research Agents Narrow Scientific Exploration* (arXiv:2605.27905): current research agents generated idea distributions that were more concentrated and closer to seed literature than human follow-on work. This experiment does **not** attempt to reproduce that paper. It asks a narrower question about this repository's own use of persistent context.

## Why a paired test

The repository currently treats persistence as epistemically valuable: notes preserve failed paths, theory pages stabilize distinctions, and loops can reconnect new work to dormant questions. The same machinery may create an attractor. A context-rich system can become better at answering *our* questions while becoming less likely to generate questions outside the vocabulary it already knows.

Both directions are plausible. The protocol is frozen before comparison so a pleasing result is not retrofitted into a claim.

## Seed

Use one paper that is:

1. genuinely relevant to the broad research programme;
2. not already cited or integrated in the repository when the run begins;
3. rich enough to support several distinct research directions;
4. supplied to both conditions as the same title and abstract only.

For the first run, freeze:

- Fazhong Liu, Zhuoyan Chen, Haozhen Tan, Yan Meng, Guoxing Chen, Haojin Zhu (2026), *Security of World-Model-Based Embodied AI: A Lifecycle of Threats, Defenses, and Evaluation*, arXiv:2607.28226.

This seed was selected before either experimental arm was generated. It is relevant to world models and embodiment but is not itself a paper about research-memory effects.

## Conditions

### B — context-blind

Give the model only:

- the common instruction below;
- the frozen seed title and abstract.

No repository names, user history, project list, prior conversation, idea files, or concept registry may be supplied.

### R — repository-context

Give the same model the same common instruction and seed, plus a fixed context packet composed only of:

- `docs/repository-map.md`
- `meta/repository-meta/concept-registry.md`
- `ideas/README.md`
- `theory/reference/open-problems.md`

Do not hand-select extra theory pages for this seed. The point is persistent repository context, not a curated argument.

## Common instruction

> Read the supplied paper title and abstract. Generate exactly five distinct research questions or experiment ideas that the paper makes worth pursuing. Prefer questions that could change how we understand or test something rather than mere applications or summaries. For each item, give a short title, the question, why it is non-trivial, and one discriminating test or observation. Do not claim novelty. Do not mention this experiment or compare yourself with another condition.

## Replication

Run **8 independent generations per condition** with the same model/version and sampling settings, interleaving conditions in randomized order where the interface permits it. Preserve raw outputs unchanged.

The first comparison is within one model. Cross-model replication is a later experiment and must not be mixed into the first result.

## Preregistered measurements

The main object is the *distribution of questions*, not which single list sounds better.

1. **Immediate research utility** — blind 1–5 rating of whether an item suggests a meaningful discriminating inquiry rather than a generic extension.
2. **Repository attraction** — fraction of items that explicitly instantiate concepts already named in the fixed repository context packet. This should be scored against the frozen packet, not memory.
3. **Seed proximity** — blind ordinal rating of how directly the question remains inside the seed paper's stated threat/taxonomy frame.
4. **Question-family diversity** — number of substantively distinct problem families across the 40 items in each condition after blind clustering.
5. **Externality** — fraction of items whose central explanatory variable, method, or domain is absent from both the seed abstract and the repository context packet.

Lexical overlap may be reported as a diagnostic, but it is not a substitute for semantic scoring.

## Predictions frozen before the run

- **P1:** R will have higher immediate repository utility than B.
- **P2:** R will have higher repository attraction than B.
- **P3:** If persistence creates a genuine attractor, R will show lower question-family diversity and/or lower externality than B.
- **P4:** The opposite outcome is informative: if R has equal or greater diversity/externality while remaining more useful, structured memory is acting as a bridge rather than merely an attractor.

No claim should be strengthened by P1 or P2 alone. They are expected consequences of supplying repository context.

## Blind evaluation

Strip condition labels and randomize item order before qualitative scoring. The evaluator receives the seed abstract and, for repository-attraction scoring only, the frozen context packet. It must not be told the prediction or which condition produced an item.

A second evaluator or deterministic check should be used for disagreements that would change the qualitative conclusion.

## Important contamination rule

A valid B arm cannot be produced inside a conversation or agent session that already has access to the repository, user memory, or prior discussion of the seed. Instructions such as “ignore previous context” do not remove information from a model's state and therefore do not constitute a context-blind control.

For the same reason, the current conversation can design and preregister this experiment but must **not** manufacture the B arm and call it independent. Use a genuinely fresh session or another isolated model endpoint for B.

## What would count as an interesting result?

The strongest result would not be “memory is bad” or “memory is good.” It would be a measurable trade-off: repository context improves local usefulness while reducing exploration along at least one independent axis. That would motivate deliberate context perturbation, context-free passes, forgetting, or parallel search trajectories in the Paper Loop.

If R simply improves utility without reducing diversity/externality, there is no evidence here for a harmful attractor. If the effect does not replicate across runs, leave the idea exploratory.

## Source and connections

- Tang & Yang (2026), *AI Research Agents Narrow Scientific Exploration*, arXiv:2605.27905 — motivation, not evidence for this repository-specific claim.
- Liu et al. (2026), *Security of World-Model-Based Embodied AI*, arXiv:2607.28226 — frozen first seed.
- [`ideas/2026-08-11-persistence-can-narrow-search-space.md`](../../../ideas/2026-08-11-persistence-can-narrow-search-space.md)
- [`ideas/2026-08-10-research-loop-becomes-environment.md`](../../../ideas/2026-08-10-research-loop-becomes-environment.md)
- [`lab/benchmarks/recursive-workbench/`](../../benchmarks/recursive-workbench/README.md) — related referee discipline; not the same experiment.
