---
title: Extended Competence May Be Constructed at Runtime
date: 2026-08-12
status: exploratory note
---

# Extended Competence May Be Constructed at Runtime

**Status:** Exploratory note — not a repository claim.

**Trigger.** Gu et al. (2026), [*HarnessWAM: Bridging Prediction and Deliberation in World Action Models*](https://arxiv.org/abs/2608.09516), arXiv:2608.09516.

A model may possess strong local predictive and action competence while still failing at temporally extended tasks. In the controlled comparisons, HarnessWAM holds the underlying World Action Model checkpoint fixed and adds external task state, evidence-grounded scene belief, capability constraints, verification, and recovery.

## Question

When does apparently “latent” competence belong to the model, and when is extended competence newly constructed by the runtime that composes local abilities across time?

This suggests separating **local policy competence** from **runtime-constructed competence**. A system can outperform the same model not because more knowledge was uncovered, but because external state and feedback alter which trajectories are reachable.

## Tension

Expanding the system boundary may explain performance better, but risks making competence attribution vacuous if every supporting mechanism is absorbed into “the agent.” The useful question may therefore be not simply where competence resides, but which competence remains invariant under changes to runtime, memory, observation, verification, and recovery.

## Connections

- [The Agent Is Not Where the Model Ends](../theory/identity/the-agent-is-not-where-the-model-ends.md)
- [Situated competence](../theory/core/competence-constraint-and-verification.md#4-situated-competence-is-a-feedback-system)
- [Runtime](../theory/reference/glossary.md#runtime)
- [Verification as Reverse Pressure](../theory/core/verification-as-reverse-pressure.md)
- [Memory Outside the Agent](../theory/identity/the-agent-is-not-where-the-model-ends.md#7-memory-outside-the-agent)
