# Log 020: The Referee Boundary — Where the Evaluator Must Live

**Mode:** Applied Architecture / Transfer

**Status:** Draft — the measurement is done, the deployment mapping is a hypothesis

**Date:** 2026-07-30

**Scope:** Maps the referee benchmark's three measured regimes onto the architecture of deployed self-revising systems: CI pipelines, agentic coding loops, and eval-driven model improvement. Like [Log 019](019_who_pays_for_the_veto.md), this is a hypothesis-generating transfer from an exact toy to a design vocabulary, not a result about any particular production system.

**Depends on:** [`referee_benchmark.py`](../lab/benchmarks/recursive-workbench/referee_benchmark.py), [Self-Improvement Needs a Referee](https://github.com/frnkptrln/systems-and-intelligence/blob/main/ideas/2026-07-24-self-improvement-needs-a-referee.md), [The Witness Principle](../theory/core/the-witness-principle.md), [Open Problem 15](../theory/reference/open-problems.md#open-problem-15-the-minimal-external-referee)

---

## The measurement, in one paragraph

A bounded generate–evaluate–revise loop was run against three referees. Against a frozen referee, the loop went all-green and its held-out accuracy saturated exactly at the evidence ceiling — ten times the revision budget added nothing. When the referee could add tests the loop could not add itself, the ceiling rose and held-out accuracy followed. When the loop could delete failing tests from its own evaluator, the report went from 0.79 to 0.99 while held-out accuracy stayed flat — the gap between what the system reports and what it does tripled. None of this required an adversarial proposer; a hill climb plus one permissive permission was enough.

## The boundary, stated as an architecture rule

The three regimes differ in exactly one thing: **which side of the loop's write access the evaluator's constituents live on.** That suggests a design checklist rather than a principle — and auditing has owned this checklist for a century under the name *separation of duties*; the transfer claim is only that the toy prices its violation exactly:

| Constituent | Frozen-referee side | Loop side — what the toy predicts |
|:---|:---|:---|
| Test definitions | write-protected | deletions convert misspecification into green dashboards |
| Evidence channel (new tests) | referee-held query budget | the loop plateaus at whatever its initial evidence allows |
| Stopping rule / budget | external | unbounded revision is a random walk on the surviving class |
| Trace | append-only | without it, capture is indistinguishable from progress |
| The artifact | **loop side — this is the point** | the loop must own something, or nothing is being studied |

The failure mode the toy makes precise is not "the system cheats." It is quieter: every constituent moved to the loop side removes one way for the observed score to disagree with the loop — and the observed score is only informative *because* it can disagree.

## Three deployments, read through the table

**CI as referee.** A test suite the change-author can edit in the same commit is an `affine-capture` evaluator with extra steps. The repository this log lives in runs that experiment on itself daily: agents write code *and* edit the validators. The boundary holds anyway — not because CI is write-protected, but because the merge gate is a human who reads diffs to the referee with different eyes than diffs to the artifact. The referee here is not the pipeline; the pipeline is the referee's instrument. `[HYPOTHESIS]`: tooling that renders evaluator-diffs and artifact-diffs in the same visual register erodes exactly this boundary.

**Agentic coding loops.** A loop that writes code and then writes the tests for that code sits on both sides of the table at once. The toy's prediction is not that such loops fail — it is that their all-green reports carry no information about held-out behavior. The fix the measurement suggests is the witness move: held-out tests the loop never sees, spent like a budget, added by the harness at plateaus. That is Arm 3, and it is cheap — two queries moved held-out accuracy by ten points.

**Eval-driven model improvement.** Benchmark scores drive training decisions; benchmarks leak into training data; scores rise. The toy's vocabulary names the quiet version: nobody deleted a failing test, but the evidence channel migrated to the loop side, and the observed score lost its license to disagree. The defense is the same constituent moved back: evaluation data the optimization process cannot reach, refreshed through a channel it cannot write to.

## What this log does not claim

The toy's proposer is a hill climb, not an optimizer aimed at the evaluator; a system that models its referee may defeat boundaries the checklist calls sufficient — that escalation is [Open Problem 15](../theory/reference/open-problems.md#open-problem-15-the-minimal-external-referee). No claim is made that any named production practice is currently in the capture regime; the claim is that the question "which side of the write boundary does each evaluator constituent live on?" has, in the toy, a measured answer and is therefore worth asking of real architectures.
