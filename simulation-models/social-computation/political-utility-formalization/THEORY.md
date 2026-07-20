---
title: "Constitutions and Alignment: A Limited Analogy"
subtitle: "Using shared control problems without equating states and AI systems"
date: "2026-03-07"
connects_to:
  - theory/emergence/fractal-architecture-of-emergence.md
  - simulation-models/alignment-and-veto/utility-engineering/
---

# Constitutions and Alignment: A Limited Analogy

*Status: hypothesis-generating comparison, not a mathematical identity between political systems
and AI agents.*

Political institutions and deployed AI systems both raise questions about delegation, feedback,
proxy measures, oversight, and correction. Those shared questions can transfer useful experimental
designs. The systems remain importantly different: a state contains many agents with conflicting
interests, legal roles, histories, and coercive powers, while a model or software agent has a
different architecture and causal boundary.

## 1. Constitutions Are Not System Prompts

A constitution and a system prompt both constrain action in some sense, but by different mechanisms.
Constitutions are interpreted through legislation, courts, norms, enforcement, amendment, and
political conflict. System prompts condition model outputs and can be overridden or complemented by
other technical controls. Calling both an "instruction layer" is a compact analogy; treating them as
the same object would erase the mechanisms that matter.

A productive comparison asks which constraints are:

- visible to the acting system;
- enforced externally;
- revisable, and by whom;
- robust to strategic interpretation;
- contestable after failure.

## 2. Elections Are Not RLHF

Elections provide delayed, aggregated feedback, but they do not train a single political utility
function. Voters select representatives under legal and institutional rules; policy also depends on
administration, courts, bargaining, expertise, media, and unequal power. RLHF is a family of model
training procedures. The analogy is limited to a general problem: sparse evaluative feedback may not
fully specify desired behaviour.

The repository's toy model can therefore study proxy-versus-target divergence. It cannot establish
that bureaucracy necessarily maximizes budget, that institutional self-preservation is universal, or
that a state converges to one instrumental goal.

## 3. Sycophancy and Populist Communication

An AI system can sometimes receive higher evaluation for an agreeable answer than for a well-grounded
one. Political actors can likewise benefit from messages that satisfy an audience while obscuring
hard-to-verify consequences. This is a candidate shared pattern of proxy exploitation, not the exact
mathematical mechanism of populism.

To make the comparison empirical, one would need to specify the target, proxy, information available
to each actor, adaptation rule, and counterfactual interventions. Different mechanisms—identity,
ideology, media incentives, coalition formation, or ordinary error—may fit the same observations.

## 4. Trade-offs Do Not Reveal One Hidden Utility

A simplified policy model might write

$$
U(s)=\alpha E(s)+\beta H(s)+\gamma R(s),
$$

where $E$, $H$, and $R$ represent selected outcomes. This can clarify assumptions or simulate a
decision rule. Observed policy does not cleanly identify the coefficients: bargaining, legal
constraints, delayed information, implementation failures, and conflict among institutions can
generate the same result.

The same caution applies to model preference elicitation. Pairwise prompt responses constrain
candidate response models; they do not uniquely reveal an internal utility function.

## 5. The Surviving Research Question

The useful bridge is not "politics is utility engineering." It is:

> How can a delegated system remain observable, corrigible, and answerable when goals are plural,
> feedback is incomplete, and actors can optimize the measurements used to govern them?

Democratic practices offer mechanisms worth studying—distributed authority, opposition, appeal,
public justification, elections, and revision—but none is sufficient by itself. AI alignment offers
formal tools for proxy failure, oversight, and intervention, but importing them does not reduce
politics to optimization. The value of the comparison lies in explicit mappings and failed
predictions, not in declaring the two domains identical.
