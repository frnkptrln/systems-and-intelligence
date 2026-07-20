# The Transition Problem: How Systems Change Their Constraints

**Status:** conceptual control problem
**Scope:** reachability of a declared viable set; societal applications remain heuristic

---

## The missing question

Specifying a desirable constraint architecture does not show that an existing system can
reach it safely.

Let

$$
\dot z=F(z,u,p)
$$

describe a system state $z$, intervention $u$, and parameters $p$. Let $V$ be a declared
viable set and $U$ the admissible interventions. The transition question is:

> Does there exist an admissible policy $u(t)\in U$ that moves the current state into $V$
> while respecting safety constraints along the entire path?

This is a reachability or viability problem. It is not process reconstruction and does not
require the legacy unqualified generator.

## Why endpoint conditions are insufficient

Suppose the target architecture has stronger regulation, adequate coordination, and a
protected substrate budget. Simply naming the target values does not answer:

- whether the controls can change them independently;
- whether action is delayed or noisy;
- whether intermediate states violate vital floors;
- whether affected actors resist, route around, or capture the control;
- whether the system changes faster than the intervention can be evaluated;
- whether the model omits a decisive state variable.

A safe endpoint may be unreachable from a particular initial state under the allowed
controls.

## Path dependence and hysteresis

Some systems retain effects of their history. Concentrated resources can alter who controls
later regulation; degraded infrastructure can reduce future repair capacity; institutions
can make prior decisions costly to reverse.

These are possible mechanisms of path dependence. Hysteresis should be claimed only when
the model or data show different state paths under increasing and decreasing control, not
as a metaphor for every political obstacle.

## A separatrix is model-specific

In a dynamical system with multiple basins, a separatrix divides initial states with
different asymptotic outcomes. The existence and geometry of that boundary must be derived
or measured from a specified system.

The repository uses *the ridge* or *separatrix* more broadly as an image for the boundary
where alternatives become reachable. That literary use should not be confused with a
computed invariant manifold.

## Possible transition strategies

### 1. Incremental control

Small interventions may work when the system remains controllable, response is observable,
and the viable path does not cross a forbidden region. Advantages include reversibility
and easier attribution. Risks include delay, lock-in, and cumulative harm.

### 2. Staged architecture change

Change the ability to regulate before increasing capability:

1. instrument vital variables;
2. establish hard action and substrate budgets;
3. assign veto and appeal authority;
4. test recovery under failure;
5. only then expand scope or throughput.

The ordering is a design hypothesis. It should be compared with alternative sequences under
matched costs.

### 3. Parallel protected niches

A smaller subsystem can test a new architecture without requiring immediate system-wide
replacement. This may reduce risk and create evidence, provided that:

- the niche does not externalize its costs;
- participation and exit are real;
- success criteria are fixed before evaluation;
- scaling effects are treated as new uncertainties.

### 4. Emergency transition

Abrupt controls may be necessary when vital thresholds are near. They also concentrate
authority and can create new failure modes. Emergency powers need expiry, audit, and
recovery rules.

Collapse is not a transition strategy. It can destroy the very information, trust, and
capacity needed for reorganization.

## The grokking analogy

Grokking shows sharp improvements in held-out generalization in selected learning setups.
It can inspire the question of whether slow parameter change produces abrupt institutional
reorganization.

The analogy does not establish that societies memorize, that scarcity acts like weight
decay, or that resource pressure produces a better representation. Scarcity can impair
learning, increase violence, and destroy slack. Any proposed mapping must name variables,
mechanisms, predictions, and counterexamples.

## A transition experiment

For a bounded model:

1. define $V$, forbidden states, and intervention limits;
2. sample initial states, including states outside the corridor;
3. compare control sequences under the same budget;
4. introduce delays, noise, actuator failure, and strategic bypass;
5. report reachability, time in unsafe states, vital-floor violations, and recovery;
6. test the winning policy on a changed model.

Success in a toy system establishes only that the transition is reachable there.

## Governance is part of the dynamics

An intervention is not just a number $u(t)$. Someone observes, decides, acts, bears cost,
and can challenge the result. A real transition model must therefore include authority,
information asymmetry, affected parties, and the possibility that the regulator fails.

The transition is not viable if it reaches the target by removing the people whose
viability defines the target.

## Open questions

1. Is the viable set reachable from relevant out-of-corridor states under bounded controls?
2. Which control ordering minimizes pathwise harm rather than only endpoint loss?
3. Which constraints must be hard before capability increases?
4. How do delay, model error, and regulator capture change reachability?
5. When do local protected niches scale, and when does scaling destroy their mechanism?

## Current claim

> Constraint architecture must be evaluated as a path-dependent transition problem, not
> only as a desirable endpoint.

TEO can host toy versions of that question. It does not yet supply a calibrated transition
model for civilization.

## Related

- [The Viable Corridor](../../papers/viable-corridor.md)
- [Optimization and Its Blindness](../optimization/optimization-and-its-blindness.md)
- [Biological Veto Requirements](biological-veto-architectural-requirements.md)
- [Cooperative Intelligence at the Separatrix](../symbiotic/cooperative-intelligence-at-the-separatrix.md)
- [Limitations and Honest Assessment](../reference/limitations-and-honest-assessment.md)
