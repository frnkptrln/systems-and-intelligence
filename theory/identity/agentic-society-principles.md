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

Let \(R\in[0,1]\) be a task-specific allocation parameter:

- low \(R\): more budget for immediate action from local observations;
- high \(R\): more budget for model comparison, review, and revision before action.

\(R\) is not introspection, wisdom, or consciousness. Its operational definition must name the
compute counted as review and the action latency or opportunity it displaces.

A heterogeneous team may combine agents with different \(R\) values. The hypothesis is that such a
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
or misleading traces. The artifact needs versioning, attribution, correction, and expiration rules.

## Evaluation

Compare heterogeneous and generalist baselines under matched total compute and information. Measure
task reward, harmful actions, latency, recovery after role failure, diversity of independent errors,
and communication overhead. Vary whether the environment rewards specialization.

The proposal fails as a general principle if specialization offers no held-out advantage, if
firewalls systematically hide safety-critical evidence, or if the coordination cost exceeds the
benefit. Its value is a testable architecture family—not a mandate to keep agents ignorant.
