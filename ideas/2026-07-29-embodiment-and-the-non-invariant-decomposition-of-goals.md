---
title: Embodiment and the Non-Invariant Decomposition of Goals
date: 2026-07-29
status: exploratory research note
---

# Embodiment and the Non-Invariant Decomposition of Goals

**Status:** Exploratory research note — Bennett's result, the repository's
interpretation, and a new conjecture are separated below.

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

## What Bennett establishes

Bennett's AGI-26 paper targets the third reading in a narrower form. Software has
no realised behaviour without an interpreter, body, and environment. In AIXI,
changing the reference universal Turing machine changes the agent's inductive
bias and can reverse performance rankings. More generally, the same controller
can succeed through one body and fail through another, while the same realised
behaviour can satisfy one goal and violate another. Realised success is therefore
a relation among controller, embodiment, environment, task, and evaluator—not an
intrinsic software quantity.

This rejects a **body-independent factorisation of realised success** into a
software-only intelligence coordinate and an independently attached goal
coordinate. It also supports the weaker physical claim (2): a particular body
does not realise every logically describable capability–goal combination.

It does **not** establish conceptual inseparability (1). Nor does it refute the
most defensible reading of Bostrom's orthogonality thesis: a modal claim that,
subject to weak constraints, many intelligence levels and final goals are
logically combinable. Bostrom explicitly distinguishes logical possibility from
the practical ease of value loading. Bennett instead exposes what is lost when
that possibility space is treated as an implementation-invariant engineering
decomposition. Within a frozen stack, reusable optimisers and separately varied
task specifications can remain useful abstractions.

## Repository interpretation: an effective goal space

Let an embodiment–environment coupling $e$ map a controller class $\mathcal C$
to its reachable trajectories:

$$
\mathcal R_e=e(\mathcal C).
$$

For candidate goals $g,h\in\mathcal G$, define

$$
g\sim_e h
\quad\Longleftrightarrow\quad
g(\gamma)=h(\gamma)
\text{ for every }\gamma\in\mathcal R_e.
$$

Then $\mathcal G/{\sim_e}$ is the **effective goal space** relative to that
coupling and evaluation lens. Goals that differ on unreachable trajectories
collapse into one operational class; changing the body, environment, horizon,
observation map, or cost model can split or merge those classes.

This is the repository's interpretation, not Bennett's theorem. It makes precise
one sense in which a body can do more than constrain a fixed policy: by
determining perceptual distinctions, admissible actions, reachable
transformations, energetic and temporal costs, and persistence conditions, it
helps determine which goal differences can become behaviourally real. It does
not uniquely determine goals or supply human values.

Calling a goal “the same” across radically different bodies therefore requires a
declared transport between their trajectory spaces and an equality criterion
that the transport preserves. Goal identity can be lens-relative in the
operational sense, just as behavioural equivalence is relative to tests. That
does not make semantic or normative identity merely observer-created.

## Alignment conjecture

Selecting an objective remains necessary, but may be insufficient. Alignment may
also require constructing a coupled system whose admissible transformations
preserve declared invariants—such as correctability, vital floors, bounded
resource use, and the continued participation of affected agents—across the
embodiments and environments in scope.

## Not claimed

- Intelligence and goals are conceptually indistinguishable.
- Embodiment uniquely determines an agent's goals or values.
- Physical limits automatically encode human or ecological values.
- Bostrom's modal orthogonality thesis has been disproved.
- Optimiser and objective cannot be modularised within a fixed interface.
- The quotient above captures a goal's full semantic or normative identity.

## Open questions

- Which transport makes a goal identical across bodies rather than merely
  similarly named?
- For which declared classes of embodiments and measurement lenses does a stable
  intelligence–goal decomposition exist?
- Which costs and persistence conditions are physically constituted, designed,
  learned, or imposed by the evaluator?
- How can an experiment distinguish embodiment merely restricting a fixed goal
  space from embodiment changing its effective distinctions?
- What invariants should alignment preserve, and under which admissible
  transformations?

**Counterexample to co-generation.** Exhibit a non-trivial class of bodies with
maps between their reachable trajectories that preserve action distinctions,
costs, persistence conditions, and all relevant goal rankings, while capability
and goal can still be varied independently. Relative to that declared class and
lens, embodiment would be an implementation detail rather than a generator of
the effective goal space.

## Connections

- [Foundations Reconstruction](../theory/core/mathematical-axioms.md)
- [Invariance and Identity](../theory/core/invariance-and-identity.md)
- [World Models and VLA](../theory/ai/world-models-and-vla.md)
- [Optimization and Its Blindness](../theory/optimization/optimization-and-its-blindness.md)
- [Intelligence as Convergence](2026-07-23-intelligence-as-convergence.md)
- [The Same World Is Not the Same World](2026-07-23-the-same-world-is-not-the-same-world.md)

## Primary sources

- Michael Timothy Bennett, [*Lies, Damned Lies, and the Orthogonality
  Thesis*](https://doi.org/10.31219/osf.io/zcfw6_v4), version 4, 2026.
- Michael Timothy Bennett, [*Computational Dualism and Objective
  Superintelligence*](https://arxiv.org/abs/2302.00843), AGI 2024.
- Nick Bostrom, [*The Superintelligent Will: Motivation and Instrumental
  Rationality in Advanced Artificial
  Agents*](https://doi.org/10.1007/s11023-012-9281-3), 2012.
