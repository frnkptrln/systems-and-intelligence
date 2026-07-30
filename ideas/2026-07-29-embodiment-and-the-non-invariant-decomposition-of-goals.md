---
title: Embodiment and the Non-Invariant Decomposition of Goals
date: 2026-07-29
status: exploratory research note
---

# Embodiment and the Non-Invariant Decomposition of Goals

**Status:** Exploratory research note. This is the paper-specific reconstruction:
Bennett's result, the repository's reading, and its limits. The durable
conceptual extraction lives separately in
[Effective Goal Space](../theory/optimization/embodiment-and-the-non-invariant-decomposition-of-goals.md).

**Question.** Intelligence and goals may be conceptually distinguishable without
admitting an implementation-neutral decomposition of realised success in an
embodied system. How strong is that claim?

## Three readings

1. **Conceptual inseparability:** intelligence and goals cannot even be
   distinguished.
2. **Restricted physical recombination:** they are distinguishable, but not every
   intelligence–goal pair can be independently realised in every body and
   environment.
3. **Non-invariant decomposition:** they may be logically separable, yet no
   implementation-, embodiment-, or measurement-independent factorisation
   recovers the performance of every realised agent.

## What Bennett supports

Bennett's AGI-26 paper targets the third reading in a narrower form. Software has
no realised behaviour without an interpreter, body, and environment. In AIXI,
changing the reference universal Turing machine changes the agent's inductive
bias and can reverse performance rankings. More generally, the same controller
can succeed through one body and fail through another, while the same realised
behaviour can satisfy one goal and violate another. Realised success is therefore
a relation among controller, embodiment, environment, task, and evaluator—not an
intrinsic software quantity.

This challenges a **body-independent factorisation of realised success** into a
software-only intelligence coordinate and an independently attached goal
coordinate. It also supports the weaker physical claim (2): a particular body
does not realise every logically describable capability–goal combination.

It does **not** establish conceptual inseparability (1). Nor does it refute the
most defensible reading of Bostrom's orthogonality thesis: a modal claim that,
subject to weak constraints, many intelligence levels and final goals are
logically combinable. Bennett exposes what is lost when that possibility space
is treated as an implementation-invariant engineering decomposition. Within a
frozen stack, reusable optimisers and separately varied task specifications can
remain useful abstractions.

## Repository extraction

The durable question is not whether embodiment uniquely supplies goals. It is
whether changing embodiment, environment, horizon, costs, or observation can
change which goal distinctions are behaviourally real. The repository models
that question with an embodiment-relative quotient of candidate goals in the
[theory note](../theory/optimization/embodiment-and-the-non-invariant-decomposition-of-goals.md).
That construction is the repository's interpretation, not Bennett's theorem.

## Not claimed

- Intelligence and goals are conceptually indistinguishable.
- Embodiment uniquely determines an agent's goals or values.
- Physical limits automatically encode human or ecological values.
- Bostrom's modal orthogonality thesis has been disproved.
- Optimiser and objective cannot be modularised within a fixed interface.

## Open questions

- Which transport makes a goal identical across bodies rather than merely
  similarly named?
- Does Bennett's implementation critique extend beyond realised performance to
  goal identity, or is that a separate conjecture?
- For which fixed interfaces does the classical optimiser–objective
  decomposition remain stable and useful?
- What observation would distinguish restricted recombination from genuinely
  non-invariant decomposition?

## Primary sources

- Michael Timothy Bennett, [*Lies, Damned Lies, and the Orthogonality
  Thesis*](https://doi.org/10.31219/osf.io/zcfw6_v4), version 4, 2026.
- Michael Timothy Bennett, [*Computational Dualism and Objective
  Superintelligence*](https://arxiv.org/abs/2302.00843), AGI 2024.
- Nick Bostrom, [*The Superintelligent Will: Motivation and Instrumental
  Rationality in Advanced Artificial
  Agents*](https://doi.org/10.1007/s11023-012-9281-3), 2012.

## Connections

- [Effective Goal Space](../theory/optimization/embodiment-and-the-non-invariant-decomposition-of-goals.md)
- [Intelligence as Convergence](2026-07-23-intelligence-as-convergence.md)
- [The Same World Is Not the Same World](2026-07-23-the-same-world-is-not-the-same-world.md)
