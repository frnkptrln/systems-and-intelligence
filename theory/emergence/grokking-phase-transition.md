# Grokking: Delayed Generalization After Overfitting

*A task-specific learning phenomenon, not a transition from memory to proven
understanding.*

---

## The phenomenon

Power et al. (2022) reported training runs on small algorithmic datasets in which a model
first reached near-perfect training performance while held-out performance remained poor.
With continued optimization, held-out performance improved much later.

That delayed improvement is called *grokking*. It is a real empirical pattern under
selected tasks, architectures, optimizers, data fractions, and regularization settings.
The timing and sharpness vary, and later work has identified several regimes and mechanisms.

## What a loss curve establishes

A run with falling held-out loss establishes improved generalization on the selected test
distribution. It does not by itself establish that:

- the model formed a unique underlying algorithm;
- memorization circuits were destroyed;
- the internal change was discontinuous;
- the model understands the task;
- the same mechanism applies to language, identity, or society.

Those stronger claims need representational and causal analysis inside the network.

## Possible mechanisms

Regularization, optimization geometry, feature formation, data fraction, and competition
between memorizing and generalizing solutions can all affect grokking. Weight decay often
matters, but “random walk until the true algorithm is found” is not a general established
mechanism.

For modular-arithmetic networks, mechanistic studies have identified interpretable
representations and circuits in specific trained models. That is stronger evidence than the
loss curve alone. It remains model- and task-specific.

## Compression reading

A compact representation can generalize better than an example-specific solution when the
target distribution has the corresponding structure. This makes grokking relevant to a
compression hypothesis:

> Simplicity pressure can sometimes favor a representation that supports held-out
> prediction.

The statement is not “intelligence is compression.” Noise can be incompressible without
being intelligent, and a short model can be wrong. Compression requires a declared
description language and must be evaluated by prediction or task loss.

## Relation to process identification

Earlier repository versions treated grokking as evidence for a universal forward/inverse
asymmetry: easy execution, hard recovery of a hidden generator. That reading is retired.

A safer connection is:

- training observations constrain many parameter settings;
- optimization and inductive bias select among them;
- held-out data test whether the selected representation extrapolates;
- internal analysis may identify which computation the network implements.

This is learning and mechanistic analysis under a declared task. It is not recovery of a
unique historical mechanism from an output trace, and it has no generic connection to
P versus NP.

## What the repository simulation can show

The checked-in simulation can reproduce a delayed-generalization curve under its chosen
configuration. It can support:

- measurement of train/test loss over time;
- sensitivity to regularization, data fraction, and seed;
- comparisons of early stopping and continued training;
- later representational probes if added.

Without those probes, the simulation should not say that a lookup table was replaced by an
algorithm. Its current strongest output is a learning curve.

## Better experiment

1. repeat across seeds and report uncertainty in grokking time;
2. sweep data fraction, weight decay, optimizer, and model size;
3. include no-regularization and matched-training-time controls;
4. track internal progress measures;
5. intervene on the proposed circuit or representation;
6. test out-of-distribution inputs that separate competing algorithms;
7. report runs that never grok.

The mechanism earns support if its progress measure predicts held-out improvement and the
targeted intervention changes that improvement while simpler explanations fail.

## Why the idea still matters

Grokking is a useful warning against treating one moment of poor generalization as a final
description of a learner. It is also a warning against reading too much into a dramatic
curve. Sudden behavioural improvement may reflect a gradual internal change, a thresholded
measurement, or a competition between solutions.

The phenomenon belongs in this repository as a concrete example of learning dynamics and
representation change — not as proof of understanding or a civilizational transition.

## Related

- [Foundations Reconstruction](../core/mathematical-axioms.md)
- [Inverse-Reconstruction Benchmark](../../lab/benchmarks/inverse-reconstruction/README.md)
- [Generative Compression](generative-compression.md)
- [Simulation](../../simulation-models/cognitive-architectures/grokking-phase-transition/README.md)
- Power et al. (2022), *Grokking: Generalization Beyond Overfitting on Small Algorithmic
  Datasets*
