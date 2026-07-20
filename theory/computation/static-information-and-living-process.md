# Static Information, Living Process, and the Runtime Boundary

**Status:** working reading aid after the foundations audit

**Scope:** Places Shannon information, algorithmic description, effect, execution, and
composition beside one another without treating them as stages of a universal ladder.

---

## Different questions called “information”

### Shannon: statistical dependence and uncertainty

Given declared random variables and a joint law, entropy and mutual information quantify
uncertainty and dependence. They are silent about meaning, purpose, life, and the unique
mechanism that produced an observation.

The [Foundations Reconstruction](../core/mathematical-axioms.md) derives these quantities
only after a state and variables have been selected. High entropy is not intelligence, and
mutual information is not causal influence.

### Kolmogorov: description length

Kolmogorov complexity asks for the length of a shortest program producing an object relative
to a universal machine. It is uncomputable in general and defined only up to an
machine-dependent additive constant.

The repository benchmark does **not** measure general Kolmogorov complexity. It measures
description length and enumeration cost inside finite declared languages. Those are useful
engineering quantities with a narrower scope.

### Bateson: an effective difference

Bateson's phrase “a difference that makes a difference” points toward a receiver or process
for which a distinction has an effect. The phrase is conceptual, not a replacement for
mutual information or causal inference.

In the inverse-reconstruction benchmark, a query is useful when candidate models predict
different returned traces. That gives one operational example: the result changes the
consistent-model class. Other uses of Bateson's phrase may require different
operationalizations.

### Computation: description plus execution conditions

A program listing is not an executed process. Initial state, runtime, scheduling,
environment, randomness, resources, and observation map can all change the resulting
trace.

Earlier versions called this whole bundle a *generator*. The reconstruction removed that
unqualified term because its parts have different mathematical types. The precise rule is:

> Name the process, state, runtime, environment, history, and observation map that the
> claim actually needs.

## Composition

Processes can be coupled so the resulting trace no longer fits a simpler component family.
Benchmark v1.8 demonstrates this in a finite cellular-automaton setup:

- data from a coupled process can leave the declared single-rule family empty;
- supplying the coupled family can restore consistency;
- some coupling remains invisible when the observed update ignores the coupled input.

An empty class diagnoses misspecification of the declared family. It does not prove that the
supplied coupled mechanism is uniquely true or that a new ontological level has emerged.

Later experiments ask stronger questions:

- **v1.9:** simple substitutive dependency does not establish mutual support;
- **v1.10:** a designed, budget-matched repair network can improve viability under sparse
  shocks;
- **v1.11:** useful support can improve the present collective while selection drives the
  support trait downward.

These results separate three properties that should not be collapsed:

1. coupled dynamics;
2. functional benefit;
3. retention or reproduction of the coupling conditions.

## Relation to life

Symbiogenesis and computational-life experiments motivate comparisons with composing
processes. The current repository artifacts do not derive life, self-maintenance, or agency
from composition alone.

A stronger claim would need operational criteria for:

- boundary maintenance;
- resource acquisition and transformation;
- repair;
- reproduction or continuation;
- heritable variation;
- persistence under environmental intervention.

The v1.10 and v1.11 results touch support and retention in toy settings. Ecological
self-maintenance remains open.

## Relation to culture

Repeated practices can also compose: one routine changes the conditions under which another
is learned or enacted. [From Action to Culture](../emergence/from-action-to-culture.md)
treats this as a research hypothesis about recurrence, transmission, correction, materials,
norms, and power. A network of recurrent practices is not automatically alive, conscious,
or reducible to program composition.

## Relation to consciousness

Static information does not entail experience. Neither does execution, coupling,
self-replication, recurrence, or self-maintenance.

Functional global availability and commit-time binding can be modeled and tested. The
repository adopts no bridge from those functions to phenomenal consciousness.

## Open questions

1. Which support mechanisms make a beneficial trait evolutionarily stable under matched
   resource accounting?
2. When does a coupled model improve held-out prediction enough to justify its added
   description length?
3. Which interventions distinguish mutual support from one-way subsidy?
4. Can recurrence and transmission explain stable practice beyond knowledge, incentives,
   and resource access?
5. Which parts of a runtime must be included for two executions to count as the same
   process under a declared test family?

## Boundary

This note prevents category errors:

- a trace is not its unique cause;
- a short description is not an executed process;
- statistical dependence is not causal influence;
- coupling is not life;
- functional organization is not phenomenal consciousness.

## Related

- [Foundations Reconstruction](../core/mathematical-axioms.md)
- [Inverse-Reconstruction Benchmark](../../lab/benchmarks/inverse-reconstruction/README.md)
- [Measurement as Weak Intervention](../core/measurement-as-weak-intervention.md)
- [From Action to Culture](../emergence/from-action-to-culture.md)
- [Limitations and Honest Assessment](../reference/limitations-and-honest-assessment.md)
