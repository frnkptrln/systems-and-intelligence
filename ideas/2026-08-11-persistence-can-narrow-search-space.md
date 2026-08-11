---
title: Persistence Can Narrow the Search Space
date: 2026-08-11
status: exploratory note
---

# Persistence Can Narrow the Search Space

**Status:** Exploratory note — not a repository claim.

**Trigger.** Tang & Yang (2026), *AI Research Agents Narrow Scientific Exploration*, arXiv:2605.27905. The paper reports that current AI research agents produce idea distributions that are more concentrated and remain closer to seed literature than human follow-on research. SciAgentArena independently reports weak self-directed exploration on open-ended scientific tasks.

Persistent context is usually treated as an advantage: previous observations, concepts, failures, and hypotheses can be reused instead of rediscovered. But memory also changes the distribution from which later questions are generated. A research system may therefore become locally more competent while globally exploring less.

**Open question.** Does accumulated research context improve the quality and specificity of generated questions while simultaneously pulling them toward existing conceptual attractors?

The opposite result is possible and important: a structured memory may expose distant dormant connections that a context-free pass would miss. The claim therefore needs a paired test rather than intuition.

A preregistered protocol lives in [`lab/experiments/context-attractor/`](../lab/experiments/context-attractor/README.md).

**Connections.**

- [A Research Loop Can Become Its Own Environment](2026-08-10-research-loop-becomes-environment.md)
- [The Graph Is a Materialized Prompt](2026-07-24-the-graph-is-a-materialized-prompt.md)
- [Self-Improvement Needs a Referee](2026-07-24-self-improvement-needs-a-referee.md)
- [Intelligence as Convergence](2026-07-23-intelligence-as-convergence.md)
