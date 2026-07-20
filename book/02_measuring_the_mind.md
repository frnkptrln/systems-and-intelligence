# Part 2: Measurement Without Reification

**Status:** Current reader chapter.

Terms such as intelligence, identity, and consciousness do not become measurable merely by
attaching a scalar to them. A valid instrument must state what system is being tested, under which
tasks and perturbations, through which observations, against which baseline, and with what failure
criterion.

## The System Intelligence Index as a selected instrument

The [System Intelligence Index](../theory/core/system-intelligence-index.md) combines four chosen
dimensions:

| Dimension | Symbol | Operational question |
|:---|:---|:---|
| Predictive performance | $P$ | How accurately does the selected model predict the declared target? |
| Regulation | $R$ | How well is a declared variable maintained under perturbation? |
| Adaptation | $A$ | How quickly does performance recover after a declared change? |
| Identity persistence | $\mathrm{IP}$ | Are the declared constraints jointly satisfied at commitment? |

The proposed aggregate is

$$
\mathrm{SII}=P\times R\times A\times \mathrm{IP}.
$$

This multiplication is a design choice: it makes any zero dimension decisive. It can be useful when
the evaluator intends all four dimensions to be necessary. It is not a theorem that intelligence
has four factors, nor a universal ranking of people, organizations, or AI systems. Different task
distributions, costs, and weightings produce different instruments.

## Identity requires a test family

Identity is not inferred from fluent self-description or one stable output. The current formal
question is whether selected properties remain invariant under declared transformations:

- changes of context, time, role, or tool;
- bounded perturbations and recovery;
- changes of observer or interaction partner;
- interventions that separate rehearsed description from action.

The Chord/Arpeggio work narrows one such test. Physical simultaneity is not required; a sequential
system may compose several constraints before committing an action. The measurable question is
whether the committed action lies inside their intersection. Even that establishes only functional
persistence under the chosen tests, not a metaphysical self.

## Functional organization is not phenomenal consciousness

Global broadcast, binding, self-model influence, memory access, and perturbation response can be
specified and tested. The repository calls these **functional** properties. None entails subjective
experience. Moving from organization to phenomenal consciousness would require an independent
bridge principle that the project does not possess.

## What the current lab actually tests

The [Agentic Identity Suite](../lab/AGENTIC_README.md) currently uses constructed agents and
deterministic mock embeddings. Experiments 5–7 test whether selected architectures leave different
behavioral signatures and whether hand-built mimics can fool the metrics. They are useful unit
tests of operational definitions, not evidence about the inner identity or consciousness of a
commercial language model.

[Experiment 8](../lab/experiments/exp8_reflexive_depth.py) compares raw observation, a fixed
Kalman filter, and an adaptive process-noise estimator. Its numerical result concerns adaptive
tracking after a volatility shift. “Reflexive depth” is an interpretation to be tested, not the
measured variable.

The practical rule is simple:

> Name the task, interface, perturbation, baseline, resource budget, and success criterion before
> naming the capacity.
