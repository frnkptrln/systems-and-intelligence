---
title: "Response Preferences as an Alignment Observable"
subtitle: "What preference elicitation can and cannot identify"
date: "2026-03-07"
connects_to:
  - theory/veto/ai-alignment-biological-veto.md
  - theory/core/from-trace-to-world-binding.md
---

# Response Preferences as an Alignment Observable

## Status

This note connects preference-elicitation research to the repository's observation and intervention
questions. It deliberately makes no claim that the accompanying demo reveals a model's latent values.

## 1. From Responses to Candidate Models

Suppose a model is repeatedly asked to choose between alternatives under a specified protocol. The
data support statements about the resulting conditional response distribution,

$$
p(y \mid x, c, d),
$$

where $x$ is the choice prompt, $c$ the context, and $d$ the decoding policy. A preference relation or
utility function can be fitted as a candidate summary of those observations. It is one model among
others: context-sensitive rules, mixtures, role conditioning, and prompt artifacts can produce the
same finite record.

Consequently, transitive answers do not prove an internally represented utility function, and cycles
do not prove an unstable agent. Both are observations to explain.

## 2. Observation Before Control

A useful empirical programme would vary wording, order, context, stakes, and sampling while holding
out evaluation items. It would report uncertainty and compare several candidate response models.
Causal claims about internal mechanisms require additional access, such as controlled training
interventions or activation-level experiments; prompt responses alone do not provide it.

The repository's current mock code performs none of those stronger tests. It checks that a graph-based
analysis pipeline works on supplied choices.

## 3. Intervention

If an intervention changes the held-out response distribution toward a declared target, the bounded
conclusion is that it changed behaviour under the tested conditions. Whether the change generalizes,
persists, or corresponds to an internal mechanism requires separate tests.

Participatory processes such as citizen assemblies can help define or contest the target. They do not
turn a statistical distance into a complete account of legitimacy, nor does minimizing that distance
guarantee alignment.

## 4. Relation to Veto Models

Preference monitoring and substrate-veto simulations operate at different levels:

- preference elicitation observes selected outputs;
- training or prompting interventions alter a software system;
- veto models stipulate physical or institutional limits in toy environments.

Combining the three can motivate layered safety experiments, but the current repository has not shown
that any layer is sufficient or unbreakable. Each needs its own causal model and external validation.

## 5. Research Questions

1. Which response regularities survive paraphrase, context shifts, and repeated sampling?
2. Which candidate models predict held-out choices best under matched complexity budgets?
3. Which interventions cause durable changes rather than measurement adaptation?
4. When do observable preference patterns predict consequential actions?
5. How should disagreement and uncertainty in the target itself be represented?

These questions connect the module to inverse reconstruction: evidence can constrain a class of
candidate explanations without uniquely revealing an internal value system.
