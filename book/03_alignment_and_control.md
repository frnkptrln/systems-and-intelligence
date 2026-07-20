# Part 3: Alignment and Control

**Status:** Current reader chapter.

Alignment is not solved by one prompt, one metric, or one physical limit. It is a control and
governance problem whose answer depends on the system boundary, possible actions, disturbances,
objectives, affected parties, and available feedback.

## Requisite variety is a design constraint, not an impossibility theorem

Ashby's law of requisite variety says that a regulator needs enough effective variety to handle
the disturbances relevant to the variables it regulates. It does not prove that humans cannot
control a more capable AI system, that every rule will be outmaneuvered, or that semantic alignment
must be replaced by thermodynamics.

Real systems can combine several layers:

- semantic instructions and learned policies;
- architectural limits and permission boundaries;
- monitoring, evaluation, and incident response;
- institutional authority, appeal, and refusal;
- rate limits, resource budgets, and physical containment.

No layer is sufficient by itself. Physical limits constrain what can happen; they do not choose
whose goals, rights, or losses matter.

## Utility engineering: present status

The utility-engineering module constructs pairwise dilemmas and computes a graph-based transitivity
score. Its current API script runs a hard-coded mock query. The live OpenAI, Anthropic, and Gemini
calls described in older pages are not implemented in that script. A transitivity score would in
any case measure consistency of elicited choices under a prompt protocol, not reveal a unique
internal utility function.

The empirical program therefore remains open: preregister prompts and sampling, repeat across
contexts and model versions, compare against appropriate baselines, and test whether the score
predicts behavior outside the elicitation set.

## Three useful constraint families

The earlier TEO work grouped several concerns under one architecture. They remain useful when their
scope is explicit:

1. **Network continuity.** The Fiedler value $\lambda_2$ describes algebraic connectivity for a
   specified graph. Positive $\lambda_2$ means a finite undirected graph is connected. Resilience
   requires a declared failure model, capacities, directionality, and post-failure criterion; it
   does not follow from one spectral value.
2. **Resource and dissipation limits.** Any physical implementation has finite resources and must
   manage heat and material throughput. A model-specific ceiling can test overload. Landauer's
   principle supplies a lower bound for logically irreversible operations, not a universal
   ecological loss function or moral veto.
3. **Commit-time constraint composition.** Safety conditions that are never operative during
   action selection cannot affect the action. Whether sequential or parallel computation composes
   them adequately is an architectural and empirical question.

## The Viable Corridor is conditional

[The Viable Corridor](../papers/viable-corridor.md) defines a viable region using regulation,
coupling, and bounded cumulative substrate overshoot. Its necessity statement is nearly
definitional: trajectories outside the region violate one of the conditions used to define it.
The substantive in-model results concern capability loading and the failure of single-axis
repairs. Joint sufficiency is still a conjecture, and the social mapping is not calibrated.

The phrase *love as constraint* names the normative intuition that optimization should not consume
its substrates, relationships, or capacity for correction. It is not a theorem and not the only
possible alignment architecture.

## The transition remains a real problem

Even after desirable constraints are specified, a system may not be able to reach them safely.
Transition paths can impose temporary losses, shift burdens, or disable the feedback needed for
correction. This motivates experiments on sequencing, latency, repair, and veto authority—always
inside an explicit model rather than as a universal prescription.
