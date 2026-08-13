# Situated-Stack Benchmark — Same Controller, Different Capability

**Status:** exact deterministic toy; repository construction

*When does “the same controller” license “the same intelligence”?*

## Why this exists

The repository treats intelligence as relative to a task family, an
observation/action interface, resources, and an evaluator.
[The Agent Is Not Where the Model Ends](../../../theory/identity/the-agent-is-not-where-the-model-ends.md)
sharpens the resulting implementation question: if the controller is held fixed
while its sensor, actuator, body, environment, or goal interface changes, which
capability comparison survives?

This benchmark makes that question finite. It does not search for a universal
measure of intelligence and cannot prove that no body-independent invariant
exists. It exhibits several inequivalent lenses that a separability claim must
choose among.

## Declared system

Every arm uses the same three-line policy:

```text
left  -> step-left
at    -> stay
right -> step-right
```

The world is the finite line $\lbrace-2,-1,0,1,2\rbrace$. The task family contains all
12 ordered start–target pairs with target in $\lbrace-1,0,1\rbrace$ and start different
from target. An episode has at most four actions. Success means ending at the
external task target.

Only one stack component changes at a time, except for the explicitly
coordinated mirror:

| arm | changed component | interpretation |
|:---|:---|:---|
| `canonical` | none | reference coupling |
| `coordinated-mirror` | sensor + actuator | both interface directions are relabelled together |
| `sensor-mismatch` | sensor | observation labels are reversed |
| `actuator-mismatch` | actuator | action-token effects are reversed |
| `coarse-sensor` | sensor | every non-target state looks “right” |
| `right-only-body` | body | leftward motion is unavailable |
| `barrier-world` | environment | a barrier blocks passage between $-1$ and $0$ |
| `goal-mirror` | goal interface | the supplied target is internally mapped to its reflection |
| `immobile-body` | body | no action changes position |

The controller source is not a member of the arm configuration, so the code
cannot silently specialize it per stack.

## Run

```bash
cd lab/benchmarks/situated-stack
python situated_stack.py
```

The benchmark uses only the Python standard library and has no random seed.

## Exact result

| stack | successes | tasks | success rate |
|:---|---:|---:|---:|
| `canonical` | 12 | 12 | 1.000 |
| `coordinated-mirror` | 12 | 12 | 1.000 |
| `sensor-mismatch` | 0 | 12 | 0.000 |
| `actuator-mismatch` | 0 | 12 | 0.000 |
| `coarse-sensor` | 6 | 12 | 0.500 |
| `right-only-body` | 6 | 12 | 0.500 |
| `barrier-world` | 5 | 12 | 0.417 |
| `goal-mirror` | 4 | 12 | 0.333 |
| `immobile-body` | 0 | 12 | 0.000 |

The same controller therefore spans the full selected score range. This is an
existence result in one declared task family, not evidence that controller
quality never transports across stacks.

## Equivalence depends on the lens

Let $\ell$ specify what the evaluator preserves. The implementation compares:

1. aggregate success;
2. the 12-task success vector;
3. the complete physical-position trace for every task; and
4. the controller action-token trace for every task.

| comparison | aggregate | task profile | physical traces | token traces |
|:---|:---:|:---:|:---:|:---:|
| `canonical` vs. `coordinated-mirror` | yes | yes | yes | no |
| `coarse-sensor` vs. `right-only-body` | yes | yes | no | no |

The coordinated mirror is a genuine symmetry under physical-behavior lenses:
the relabelled sensor and actuator cancel, yielding identical world
trajectories. An observer who treats controller tokens as privileged breaks
that equivalence.

The coarse sensor and right-only body have the same aggregate score and the
same task-wise successes, but generate different failures. A score-only or
success-profile lens identifies them; a trace-sensitive lens does not.

## What the result does and does not say

The result demonstrates:

- controller identity is insufficient to determine selected capability;
- coordinated stack changes can preserve capability;
- uncoordinated changes can destroy it;
- equal aggregate performance need not preserve task-wise mechanism or trace;
- an equivalence claim must name its task family and observer lens.

It does **not** demonstrate:

- that embodiment disproves every orthogonality thesis;
- that no representation-independent intelligence measure can exist;
- that biological bodies are required for intelligence;
- that the selected controller is adaptive or generally intelligent;
- that success is the uniquely correct evaluation lens;
- that two stacks equal under these tests are the same agent.

The strongest warranted conclusion is conditional: within this toy, “same
software” does not determine “same measured intelligence,” while a declared
coordinated transformation can preserve it.

## Next falsifiable step

Replace the hand-declared stack arms with a distribution of sensor/actuator
codes and ask whether a non-trivial representation learned on some stacks
predicts held-out capability on new stacks better than controller-only,
aggregate-score, and full-trace baselines. The comparison must freeze the task
transport and charge for information about the new interface.

## Related

- [The Agent Is Not Where the Model Ends](../../../theory/identity/the-agent-is-not-where-the-model-ends.md)
- [Embodiment and the Non-Invariant Decomposition of Goals](../../../theory/optimization/embodiment-and-the-non-invariant-decomposition-of-goals.md)
- [Invariance and Identity](../../../theory/core/invariance-and-identity.md)
- [World Models and VLA Systems](../../../theory/ai/world-models-and-vla.md)
- [Foundations Reconstruction](../../../theory/core/mathematical-axioms.md)
