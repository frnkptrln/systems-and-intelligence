# Developmental Constraints and TEO: A Comparison Protocol

*Status: analogy and proposed experiment. Developmental language learning does not validate TEO, and
TEO variables are not identified with infant learning mechanisms.*

## External Anchor

Research on language acquisition studies how perceptual biases, prior structure, statistical
learning, embodiment, and social interaction shape what children learn from limited and uneven
data. The strength, origin, and specificity of particular constraints remain empirical questions.
The broad lesson is that learning outcomes depend on both the hypothesis space and the data regime.

## TEO Conditions

The repository can construct three synthetic conditions:

1. **Selection-only:** replicator-like competition among alternatives.
2. **Externally bounded:** the same dynamics plus a stipulated homeostatic penalty.
3. **Coupled:** competition and bounds plus a Kuramoto-like interaction term.

These are mathematical components of a toy ODE. Selection is not raw infant exposure, the
homeostatic brake is not an innate phoneme category, and Kuramoto coupling is not social
contingency. Similar words such as constraint and coupling do not make the mechanisms equivalent.

## Testable Questions Inside the Model

- Does adding the brake or coupling improve a preregistered task score under matched parameter
  budgets?
- Does the order in which terms are introduced change the final basin?
- Are results robust across initial conditions, network structures, and noise?
- Can a simpler regularizer or ordinary communication model match the outcome?
- Do abrupt transitions exist in finite systems, or only smooth crossovers?

Results would establish properties of the TEO equations. A bridge to development would additionally
need operational mappings from data, fitted parameters, held-out predictions, and comparison with
developmental baselines.

## A Responsible Cross-Domain Prediction

The shared, falsifiable proposition is modest:

> In some learning tasks, the timing and form of inductive constraints and interaction alter
> generalization under fixed data and compute.

That proposition is already compatible with many learning theories and is not novel to TEO. The
repository's possible contribution is an explicit controlled comparison, not a claim that
development follows replicator, Kuramoto, and dissipation equations.

See [Thermodynamics of Emergent Orchestration](../core/thermodynamics-of-orchestration.md) for the
model and [Fractal Architecture of Emergence](../emergence/fractal-architecture-of-emergence.md) for
the mapping contract required before cross-scale analogies count as evidence.
