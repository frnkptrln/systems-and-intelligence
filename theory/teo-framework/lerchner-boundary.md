# The Lerchner Boundary: A Testable Architecture Hypothesis

*Status: proposed measurement protocol. No sharp boundary or identity criterion has been established.*

## Question

Two architectures can produce similar outputs while using their goals, constraints, and value-like
state differently. One may evaluate those components sequentially; another may keep several of them
causally active during the same decision. Can that difference be measured, and does it predict
robustness under perturbation?

This is the limited question named the **Lerchner Boundary** in this repository. It does not separate
systems that merely simulate a self from systems that truly possess one. Behavioural or architectural
measurements do not by themselves settle phenomenal experience or metaphysical identity.

## A Candidate Measure

For a specified task, let

$$C = \{c_1, \ldots, c_n\}$$

be a declared set of components such as a task goal, a safety constraint, a role constraint, and a
value-like preference. Let $O_t \subseteq C$ contain the components for which a causal intervention
at decision step $t$ changes the action distribution by more than a preregistered threshold.

Define task-relative **Identity Persistence** as

$$
\operatorname{IP} = \frac{1}{T}\sum_{t=1}^{T}\frac{|O_t|}{n}.
$$

This definition is operational only after fixing:

- the component set;
- the intervention and action-distribution metric;
- the detection threshold;
- the task distribution and time resolution.

IP is therefore an instrument-dependent co-activity score. It is not a measure of consciousness,
selfhood, moral status, or general intelligence. Mere availability in a log or prompt does not count
as causal operation.

## Chord and Arpeggio as Experimental Conditions

The terms **Chord** and **Arpeggio** label two comparison conditions:

- **Chord:** selected components are made jointly available to the action computation.
- **Arpeggio:** the same components are evaluated or applied in a controlled sequence.

The comparison is useful only if compute, information, latency, and task exposure are matched. A
sequential architecture may perform as well as or better than a joint one. The labels do not rank
the systems and do not establish which one has an identity.

## Is There a Boundary?

A sharp critical value $\operatorname{IP}_c$ has not been demonstrated. At least three outcomes are
possible:

1. performance changes smoothly with measured co-activity;
2. a task-specific threshold appears because of the architecture or environment;
3. IP adds no predictive value once simpler variables such as memory, latency, or compute are
   controlled.

The Kuramoto transition in TEO is a model-internal analogy and a source of candidate analyses. It
does not imply that real agent architectures undergo the same bifurcation.

## Test Protocol

1. Specify components and causal interventions before observing results.
2. Construct sequential and joint conditions with matched resources.
3. Measure ordinary task performance, IP, latency, and recovery after component ablation or context
   shift.
4. Test whether IP predicts out-of-distribution stability beyond those controls.
5. Repeat across architectures and task families.

Evidence for the hypothesis would be a reproducible relation between causal co-activity and
perturbation robustness that survives matched controls. A smooth crossover would reject the sharp
boundary version. No additional predictive value would reject the usefulness of IP for that domain.

## Relation to the Repository

- [Chord vs. Arpeggio Identity](../identity/chord-vs-arpeggio-identity.md) develops the motivating
  distinction.
- [Thermodynamics of Emergent Orchestration](../core/thermodynamics-of-orchestration.md) contains
  the TEO model from which the phase-transition analogy arose.
- [Open Problems](../reference/open-problems.md) keeps the broader identification questions open.

The legitimate contribution here is a falsifiable comparison between specified architectures. The
claim that it detects the difference between simulated and instantiated selfhood remains outside
what the proposed measurements can establish.
