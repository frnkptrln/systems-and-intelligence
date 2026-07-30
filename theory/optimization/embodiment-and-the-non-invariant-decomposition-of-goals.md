---
title: Embodiment and the Non-Invariant Decomposition of Goals
date: 2026-07-29
status: working conceptual model
---

# Embodiment and the Non-Invariant Decomposition of Goals

**Status:** Working conceptual model — a durable repository extraction, not a
theorem. The paper-specific reconstruction and primary sources remain in the
[research note](https://github.com/frnkptrln/systems-and-intelligence/blob/main/ideas/2026-07-29-embodiment-and-the-non-invariant-decomposition-of-goals.md).

**Thesis.** Intelligence and goals can remain conceptually distinguishable even
when a realised embodied system admits no implementation-, embodiment-, or
measurement-invariant decomposition into a neutral optimiser plus an
independently attached objective.

This thesis is weaker than conceptual inseparability and stronger than saying
only that bodies impose practical limits. It asks whether embodiment changes the
operational distinctions through which capabilities and goals can be realised
and measured.

## Effective goal space

Let an embodiment–environment coupling $e$ map a controller class $\mathcal C$
to its reachable trajectories:

$$
\mathcal R_e=e(\mathcal C).
$$

Let an evaluation lens $\ell$ map a reachable trajectory to the record on which
candidate goals are compared. For $g,h\in\mathcal G$, define

$$
g\sim_{e,\ell} h
\quad\Longleftrightarrow\quad
g(\ell(\gamma))=h(\ell(\gamma))
\text{ for every }\gamma\in\mathcal R_e.
$$

Then $\mathcal G/{\sim_{e,\ell}}$ is the **effective goal space** relative to
the declared coupling and evaluation lens. Goals collapse into one operational
class when they differ only on unreachable trajectories or distinctions erased
by the lens. Changing the body, environment, horizon, observation map, or cost
model can split or merge those classes.

This quotient does not define a goal's complete semantic or normative identity.
It records which goal distinctions can affect behaviour within a declared
realisation.

## What embodiment contributes

A body can do more than restrict a policy chosen elsewhere. By helping determine

- perceptual distinctions,
- admissible actions,
- reachable transformations,
- energetic and temporal costs, and
- conditions of persistence,

it helps determine which differences among candidate goals can become
operationally consequential. It does not uniquely determine goals, provide human
values, or erase the usefulness of optimiser–objective modularity inside a fixed
interface.

Calling a goal “the same” across radically different bodies therefore requires a
declared transport between their trajectory spaces and an equality criterion the
transport preserves. Goal identity can be lens-relative in this operational
sense without making semantic or normative identity merely observer-created.

## Alignment conjecture

Selecting an objective remains necessary, but may be insufficient. Alignment may
also require constructing a coupled system whose admissible transformations
preserve declared invariants—such as correctability, vital floors, bounded
resource use, and the continued participation of affected agents—across the
embodiments and environments in scope.

## Not claimed

- Intelligence and goals are conceptually indistinguishable.
- Embodiment uniquely determines an agent's goals or values.
- Physical constraints automatically encode human or ecological values.
- The modal orthogonality thesis has been disproved.
- Optimiser and objective cannot be modularised within a fixed interface.
- The quotient above captures a goal's full semantic or normative identity.

## Open questions

- Which transport makes a goal identical across bodies rather than merely
  similarly named?
- For which declared classes of embodiments and measurement lenses does a stable
  intelligence–goal decomposition exist?
- Which costs and persistence conditions are physically constituted, designed,
  learned, or imposed by the evaluator?
- How can an experiment distinguish embodiment restricting a fixed goal space
  from embodiment changing its effective distinctions?
- What invariants should alignment preserve, and under which admissible
  transformations?

**Counterexample to co-generation.** Exhibit a non-trivial class of bodies with
maps between their reachable trajectories that preserve action distinctions,
costs, persistence conditions, compatible evaluation records, and all relevant
goal rankings, while capability and goal can still be varied independently.
Relative to that declared class and lens, embodiment would be an implementation
detail rather than a generator of the effective goal space.

## Connections

- [Paper-specific research note](https://github.com/frnkptrln/systems-and-intelligence/blob/main/ideas/2026-07-29-embodiment-and-the-non-invariant-decomposition-of-goals.md)
- [Foundations Reconstruction](../core/mathematical-axioms.md)
- [Invariance and Identity](../core/invariance-and-identity.md)
- [World Models and VLA](../ai/world-models-and-vla.md)
- [Optimization and Its Blindness](optimization-and-its-blindness.md)
- [Intelligence as Convergence](https://github.com/frnkptrln/systems-and-intelligence/blob/main/ideas/2026-07-23-intelligence-as-convergence.md)
- [The Same World Is Not the Same World](https://github.com/frnkptrln/systems-and-intelligence/blob/main/ideas/2026-07-23-the-same-world-is-not-the-same-world.md)
