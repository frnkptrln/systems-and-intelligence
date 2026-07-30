---
title: Self-Improvement Needs a Referee
date: 2026-07-24
status: exploratory note
---

# Self-Improvement Needs a Referee

**Status:** Exploratory note — not a repository claim.

**Hypothesis.** A system that repeatedly generates, evaluates, and revises is not necessarily self-improving. It is first **self-modifying**. Improvement requires criteria the loop cannot silently redefine.

If the loop can alter its objective, evaluator, evidence, permissions, and stopping rule, success becomes circular. A fluent internal critic is not automatically an independent referee.

A bounded experiment would freeze task, evaluator, permissions, and control logic while the loop modifies only an external artifact. Held-out tests, budgets, complete traces, and reversible checkpoints would make improvement observable.

**Open question.** How external must the referee be? It may live inside the runtime, but needs independent information, permissions, or failure authority. Does every recursive evaluator eventually become part of the optimization target?

This motivated the [`recursive-workbench`](../lab/benchmarks/recursive-workbench/README.md), which now exists: the loop is the object of study, and its first experiments improve bounded artifacts rather than their own control system. Its paired v0.1 measures the three regimes exactly — saturation at the evidence ceiling under a frozen referee, held-out gains from referee-side queries, and a tripled observed-vs-held-out gap under evaluator capture.

The proof/replay integration adds a second requirement: the referee should
return evidence that can revise definitions, state representations, and
interfaces, not only approve or reject a final output. This is
[verification as reverse pressure](../theory/core/verification-as-reverse-pressure.md).
If the loop can also rewrite the tests by which its continuation is judged,
the result may still have a provenance-based succession relation, but strict
identity is no longer supplied by the loop's self-report.

**Trace-governance extension.** The proposal history, summaries, cached evaluations, checkpoints,
and repository state are also part of the loop's effective control state. A frozen evaluator does
not prevent a stale trace from repeatedly steering the proposer toward an obsolete region after the
task changes. Future loop comparisons should therefore vary provenance, aging, invalidation, and
reset policies, and measure recovery after a regime shift. This is distinct from evaluator capture:
the referee can remain write-protected while the shared memory substrate still preserves a bad
attractor. See [The Agent Is Not Where the Model Ends](../theory/identity/the-agent-is-not-where-the-model-ends.md#7-memory-outside-the-agent).

**Connections.**

- [The Graph Is a Materialized Prompt](2026-07-24-the-graph-is-a-materialized-prompt.md)
- [From Trace to World-Binding](../theory/core/from-trace-to-world-binding.md)
- [Optimization and Its Blindness](../theory/optimization/optimization-and-its-blindness.md)
- [Verification as Reverse Pressure](../theory/core/verification-as-reverse-pressure.md)
- [Invariance and Identity](../theory/core/invariance-and-identity.md#self-modification-and-the-projector-audit)
