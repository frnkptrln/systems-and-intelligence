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

This motivated the [`recursive-workbench`](../lab/benchmarks/recursive-workbench/README.md), which now exists: the loop is the object of study, and its first experiments improve bounded artifacts rather than their own control system. Its v0 measures the three regimes exactly — saturation at the evidence ceiling under a frozen referee, held-out gains from referee-side queries, and a tripled observed-vs-held-out gap under evaluator capture.

**Connections.**

- [The Graph Is a Materialized Prompt](2026-07-24-the-graph-is-a-materialized-prompt.md)
- [From Trace to World-Binding](../theory/core/from-trace-to-world-binding.md)
- [Optimization and Its Blindness](../theory/optimization/optimization-and-its-blindness.md)
