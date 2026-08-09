# Identity Abduction: Minimal Finite-System Sanity Check

**Status:** First executable sanity check  
**Scope:** Toy example for explicit correspondence, invariant preservation, and adversarial rejection  
**Epistemic status:** Demonstrates the verification pattern only; it is not evidence for general scientific abduction.

## Question

Can we separate three things that are easy to blur together?

1. **surface similarity**;
2. **shared weak invariants**;
3. **an explicit equivalence witness**.

The smallest useful example is a finite graph represented by an adjacency matrix.

Let `A` be the adjacency matrix of a 6-cycle. Create `B` by permuting the vertex labels with a known permutation matrix `P`:

```text
B = P . A . Transpose[P]
```

`A` and `B` are the same structure under an explicit correspondence. The permutation is the witness.

For an adversarial decoy, let `D` be two disconnected triangles. `A` and `D` have the same degree sequence — every vertex has degree 2 — so that weak invariant cannot distinguish them. Stronger checks reject the identity claim: their spectra differ, and one graph is connected while the other is not.

## Wolfram verification

The following was evaluated independently with Wolfram Language on 2026-08-09:

```wl
a = {
  {0,1,0,0,0,1},
  {1,0,1,0,0,0},
  {0,1,0,1,0,0},
  {0,0,1,0,1,0},
  {0,0,0,1,0,1},
  {1,0,0,0,1,0}
};

perm = {3,6,2,5,1,4};
p = IdentityMatrix[6][[perm]];
b = p . a . Transpose[p];

d = {
  {0,1,1,0,0,0},
  {1,0,1,0,0,0},
  {1,1,0,0,0,0},
  {0,0,0,0,1,1},
  {0,0,0,1,0,1},
  {0,0,0,1,1,0}
};

<|
  "positivePermutationWitness" -> (b === p . a . Transpose[p]),
  "positiveDegreeSequenceEqual" -> (Sort[Total[a]] === Sort[Total[b]]),
  "positiveSpectrumEqual" -> (Sort[Eigenvalues[a]] === Sort[Eigenvalues[b]]),
  "negativeDegreeSequenceEqual" -> (Sort[Total[a]] === Sort[Total[d]]),
  "negativeSpectrumEqual" -> (Sort[Eigenvalues[a]] === Sort[Eigenvalues[d]]),
  "spectrumCycle6" -> Sort[Eigenvalues[a]],
  "spectrumTwoTriangles" -> Sort[Eigenvalues[d]],
  "negativeConnectednessDiffers" -> {
    MatrixPower[a,5][[1,4]] > 0,
    MatrixPower[d,5][[1,4]] > 0
  }
|>
```

Observed result:

```text
positivePermutationWitness   -> True
positiveDegreeSequenceEqual  -> True
positiveSpectrumEqual        -> True
negativeDegreeSequenceEqual  -> True
negativeSpectrumEqual        -> False
spectrumCycle6               -> {-2,-1,-1,1,1,2}
spectrumTwoTriangles         -> {-1,-1,-1,-1,2,2}
negativeConnectednessDiffers -> {True,False}
```

## What this establishes

Only a very small point:

- a proposed identity can be made explicit as a mapping;
- invariant checks can support that mapping;
- a weak shared invariant is insufficient;
- an adversarial decoy can be rejected by a stronger invariant;
- verification is downstream of the hypothesis rather than a substitute for generating it.

This mirrors the discipline proposed for identity abduction without importing the stronger claim that a model can discover useful cross-domain correspondences autonomously.

## What it does not establish

It does not show that:

- representational transformation is necessary for the positive case;
- a language or multimodal model can recover `P` from unfamiliar representations;
- graph spectra are complete invariants (they are not in general);
- finite graph isomorphism captures scientific identity;
- any mechanistic explanation has been discovered.

## Next experiment: representation ablation

The useful version should hide the witness and vary what the reasoner receives.

Candidate conditions:

1. raw adjacency matrices with unrelated labels;
2. edge lists;
3. rendered diagrams;
4. weak invariant summary only (degree sequence);
5. richer invariant summary;
6. mixed representations across source and target.

For each condition, ask for an explicit vertex correspondence and then verify it independently. Include decoys chosen to preserve some weak invariants. Measure:

- correspondence recovery rate;
- false-positive identity claims;
- abstention rate;
- verification success;
- inference cost / number of attempts.

The interesting hypothesis is not that one representation is universally best. It is that some transformations make the task-relevant invariant materially more accessible while preserving what correctness requires.

## Related

- `ideas/2026-08-09-representational-grounding-and-mechanistic-world-models.md`
- `theory/emergence/trace-to-generator.md`
- `theory/core/the-generator-question.md`
- `theory/core/competence-constraint-and-verification.md`
