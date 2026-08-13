# Agentic Societies: Division of Cognitive Labor

*Status: multi-agent design hypotheses. No result here shows that omniscience causes paralysis or
that ignorance is necessary for life, intelligence, or action.*

## Question

When does a collection of specialized agents outperform a single broadly informed agent under a
fixed compute, communication, and tool budget?

The proposed architecture separates fast local action, slower review, memory, and rule revision.
This resembles cognitive division of labor in organizations, but it should be evaluated as an
engineering design rather than an account of consciousness.

## A Reflectivity Parameter

Let $R\in[0,1]$ be a task-specific allocation parameter:

- low $R$: more budget for immediate action from local observations;
- high $R$: more budget for model comparison, review, and revision before action.

$R$ is not introspection, wisdom, or consciousness. Its operational definition must name the
compute counted as review and the action latency or opportunity it displaces.

A heterogeneous team may combine agents with different $R$ values. The hypothesis is that such a
team can improve speed–error trade-offs when tasks genuinely differ in the value of review.

## Information Boundaries

Limited context can reduce distraction, leakage, correlated error, or manipulation. It can also
remove information required for a safe decision. An information firewall is therefore a policy with
costs, not a source of productive surprise by definition.

Useful designs specify:

- what each role can observe and change;
- how evidence crosses boundaries;
- who can challenge or override a decision;
- how omitted information is requested;
- how correlated failure is detected.

## Stigmergic Memory

Agents can coordinate through an external artifact such as a task board, repository, or shared
environment. This can reduce direct communication and preserve provenance. It can also amplify stale
or misleading traces. External memory therefore changes the effective control state rather than
merely storing information: later agents read earlier traces, those traces bias action, and the
resulting action writes the next substrate.

The trace ecology needs explicit governance:

- timestamp traces and retain their source;
- mark scope, confidence, and observation versus inference;
- support correction and invalidation rather than append-only authority;
- use multiple expiration or decay timescales;
- retain raw evidence where feasible;
- test recovery after an environmental regime change;
- challenge high-centrality traces that many later actions depend on; and
- treat summaries as revisable indexes, not irreversible truth.

The failure can be substrate-level. Every local agent may follow its declared objective while a
shared retrieval layer keeps presenting an obsolete attractor. Montes's 2026
[trace-field simulation](https://doi.org/10.1007/978-3-032-33195-3_7) is one bounded toy:
persistent traces improve selected coordination outcomes, but stale traces delay recovery after the
world changes; decay and targeted reset alter that recovery without modifying every agent.

This does not make every shared artifact part of one agent. It puts the artifact inside the
effective control model whenever counterfactual removal or corruption changes later behavior. The
larger boundary question is developed in
[The Agent Is Not Where the Model Ends](the-agent-is-not-where-the-model-ends.md#7-memory-outside-the-agent).

## Evaluation

Compare heterogeneous and generalist baselines under matched total compute and information. Measure
task reward, harmful actions, latency, recovery after role failure, diversity of independent errors,
communication overhead, and recovery after a stale-memory perturbation. Vary whether the environment
rewards specialization and whether trace provenance, decay, and invalidation are available.

The proposal fails as a general principle if specialization offers no held-out advantage, if
firewalls systematically hide safety-critical evidence, or if the coordination cost exceeds the
benefit. Its value is a testable architecture family—not a mandate to keep agents ignorant.
