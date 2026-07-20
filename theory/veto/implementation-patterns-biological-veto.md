# Implementation Patterns for Bounded AI Actions

*Status: candidate defense-in-depth patterns. They reduce selected risks under a threat model; they
do not ensure deterministic control, human consensus, or an unbreakable biological veto.*

## 1. Action Budgets

Limit tokens, tool calls, money, runtime, data access, and state-changing operations per task. Enforce
the budget outside the proposing model and define what happens when it is exhausted.

These are engineering and authorization limits, not thermodynamic bounds. A centralized budget
manager can itself fail or be bypassed, and an agent may cause high impact with few actions. Test
counter resets, parallel sessions, delegated tools, race conditions, and denial-of-service effects.

## 2. Staged High-Impact Commits

Place destructive, costly, or difficult-to-reverse actions in a review queue. Use out-of-band
authorization, explicit diffs, time windows, cancellation, and two-person control where the risk
justifies them.

A hardware touch or signature proves control of a credential, not understanding or legitimate
consent. Review interfaces must expose consequences, uncertainty, and alternatives, and must resist
habitual approval, coercion, compromised devices, and emergency pressure.

## 3. A Separate Execution Gate

Require a lower-privilege component to validate typed commands against an allowlist, constrain
arguments, and execute them in a sandbox. Keep the proposing model unable to modify the validator or
its policy.

JSON, schemas, containers, and local execution shrink the attack surface but do not make it
immutable. Parsers, allowed functions, dependencies, kernels, and update channels remain part of the
trusted computing base. Prompt injection can also exploit an allowed action rather than request
arbitrary code.

## 4. Provenance, Revocation, and Recovery

Log proposals, evidence, approvals, executed effects, and policy versions. Make credentials and
capabilities revocable. Provide idempotency, rollback where possible, incident containment, and a
way to restore safe service after a false block.

Open implementations can improve inspection and reuse, while centralized and decentralized designs
have different correlated-failure and governance risks. Neither topology guarantees human agency.

## Evaluation Contract

Define protected assets, attacker access, acceptable failure, and the action classes in scope.
Red-team bypass, confused-deputy attacks, compromised approvers, validator bugs, concurrent agents,
and recovery. Compare the full pattern set with simpler least-privilege and ordinary change-control
baselines.

The useful claim is modest: independent budgets, staged commitments, typed execution gates, and
recoverable audit trails can reduce specific autonomous-action risks when correctly implemented and
governed.
