Tensor Logic as a Unified Model for Symbolic and Continuous Reasoning
Frank Peterlein — 2025

Abstract

This document provides a concise conceptual and computational introduction to Tensor Logic, a framework introduced by Pedro Domingos that unifies symbolic reasoning, neural embeddings, and probabilistic inference into a single mathematical system: tensor algebra.

Logical relations become Boolean tensors.
Logical rules become tensor contractions.
Embeddings transform these relations into smooth operators that interpolate between strict logic and graded analogy.

The accompanying Python code in this repository (simulation-models/tensor-logic-reasoning) demonstrates the framework in a minimal four-entity world with a simple Parent relation.


# 1. Introduction

Contemporary AI is commonly divided into two paradigms:

Symbolic AI — discrete, rule-based, explainable, but brittle

Neural AI — continuous, learned, robust, but opaque

Tensor Logic suggests that this bifurcation is artificial.
At the appropriate level of abstraction:

Relations, rules, embeddings, and reasoning share the same tensor structure.

A logical rule such as:

Ancestor(x, z) ← Parent(x, y), Parent(y, z)

can be expressed as a tensor contraction over the Boolean adjacency matrix of the Parent relation.

This note aims to:

• isolate the core of Tensor Logic
• illustrate it through minimal code
• connect it to a systems-theoretic perspective on intelligence

# 2. Relations as Tensors

## 2.1 Symbolic level

Any binary relation R(x, y) over a finite set of entities can be expressed as a Boolean matrix:

R_xy = 1 if (x, y) is in the relation
R_xy = 0 otherwise

Logical inference steps, such as joins and projections, correspond to algebraic operations on these matrices.

For example, if Parent is represented as a matrix P_xy, then a one-step ancestor relation can be computed by summing over the shared intermediate variable y and applying a threshold.

Repeated application yields the transitive closure.

Symbolic reasoning is Boolean tensor algebra.

## 2.2 Continuous Level

Now assume that each entity x is represented by a continuous embedding vector Emb[x] in R^d.

In this setting, a relation R can be mapped to a real-valued matrix (a rank-2 tensor) by summing outer products of embeddings for each fact in the relation:

EmbR = Σ over all (x, y) in R of (Emb[x] ⊗ Emb[y])

Each individual fact contributes a small "patch" to the relation tensor.
The full relation becomes the superposition of all these patches.

This construction is closely related to a Tucker decomposition:

• entity embeddings form the factor matrices
• the relation tensor EmbR acts as the core tensor

The result:

Relations = superpositions of embedding outer products.

This provides the first bridge between symbolic and continuous representations.


# 3. Reasoning in Embedding Space

Given:

• a relation tensor EmbR
• embeddings for all entities

we can evaluate a candidate pair (a, b) by computing a reasoning score:

Score(a, b) = Emb[a]^T · EmbR · Emb[b]

High scores indicate that the pair (a, b) aligns well with the learned relation structure.
Low or negative scores indicate incompatibility.

To convert this score into a probability, we subtract a baseline μ (for example, the mean score across all pairs) and apply a logistic function with temperature T:

p(a, b) = σ( (Score(a, b) − μ) / T )

where σ(z) = 1 / (1 + exp(−z)).

Temperature T controls the sharpness of the decision boundary:

• T → 0 reproduces hard Boolean logic
• Larger T yields soft, graded, analogy-like reasoning

Thus:

Reasoning = similarity-weighted tensor contraction with temperature.
Logic appears as the special case where T approaches zero.


# 4. Toy Experiment

The script in simulation-models/tensor-logic-reasoning/tensor_logic_demo.py constructs a minimal world containing four entities:

• Alice
• Bob
• Charlie
• David

with the following parenthood structure:

Alice → Bob → Charlie → David

This yields three facts in the Parent relation:

Parent(Alice, Bob)
Parent(Bob, Charlie)
Parent(Charlie, David)

From this, the script performs the following steps:

Construct the Boolean matrix representation of the Parent relation.

Compute the logical Ancestor relation by calculating the transitive closure.

Sample random unit-norm embeddings for the four entities.

Construct the embedding-based relation tensor EmbParent by summing outer products.

Evaluate several Parent queries using:
• pure logical lookup (0 or 1)
• embedding-based score
• probability using a logistic with temperature

Below is an example outcome from a typical run, using centered scores and T = 1.0:

Parent(Alice, Bob):
Logical truth = 1
Centered score = +0.54
Probability ≈ 0.63

Parent(Bob, Charlie):
Logical truth = 1
Centered score = +0.62
Probability ≈ 0.65

Parent(Alice, Charlie):
Logical truth = 0
Centered score = +0.29
Probability ≈ 0.57

Parent(Alice, David):
Logical truth = 0
Centered score = −0.18
Probability ≈ 0.46

Interpretation:

• Direct parent pairs receive the strongest positive scores.
• Indirect ancestor pairs (like Alice → Charlie) still receive positive scores,
revealing latent structure not visible in the strict Parent relation.
• Pairs unsupported by the relation remain near baseline or below.

This tiny example already shows the main idea of Tensor Logic:
symbolic structure emerges naturally from geometric alignment in embedding space.


# 5. A Systems-Theoretic View

Tensor Logic provides a way to reinterpret intelligent behavior from a systems perspective.

Rather than locating intelligence in:

• symbolic rules, or
• neural weights

Tensor Logic suggests that intelligence emerges from the interaction of three components:

Embeddings — represent the states of a system

Relation tensors — encode constraints between states

Tensor contractions — define the operations that propagate and combine information

Reasoning is then the projection of these interactions into observable outputs (scores or decisions).

In this interpretation:

Intelligence is not a property of components,
but a property of their couplings.

This fits naturally with ideas from systems theory, where:

• structure (constraints),
• state (embeddings), and
• dynamics (operations)

jointly shape the behavior of a system.

Tensor Logic becomes a formal language for describing such coupled systems — a way to express how local interactions give rise to global reasoning patterns.


# 6. Conclusion

Tensor Logic offers a unified mathematical lens through which symbolic and neural approaches to AI can be seen as two regimes of the same underlying machinery.

Its core insights can be summarized as:

Logical relations are Boolean tensors.

Logical rules correspond to tensor contraction patterns.

Embeddings factorize these tensors into continuous spaces.

Temperature-controlled logistic functions interpolate between strict logic and graded analogy.

This perspective suggests that the divide between symbolic reasoning and neural computation is not fundamental.
Instead, discrete logic arises as the limit case of continuous tensor algebra as temperature approaches zero.

Tensor Logic therefore becomes a promising candidate for a unified reasoning framework in future AI systems — expressive enough for logical structure, flexible enough for analogy, and mathematically coherent across both.

Future extensions may include:

• learning embeddings directly via Tensor-Logic objectives
• handling higher-arity relations and temporal dynamics
• modeling context-dependent or hierarchical temperatures
• connecting Tensor Logic to ecological or multi-agent systems
• embedding Tensor Logic within larger architectures (transformers, GFlowNets, etc.)

Appendix: Repository Context

This mini-paper is part of the systems-and-intelligence project.

Files of interest:

• theory/tensor-logic-mini-paper.en.md — this document
• theory/tensor-logic-mini-paper.de.md — German version
• theory/tensor-logic-visual.html — interactive visualization of core concepts
• simulation-models/tensor-logic-reasoning/ — Python implementation of the toy example

The goal of this structure is to combine:

• theoretical exposition
• executable simulation
• visualization
• systems-theoretic interpretation

into one coherent framework.
