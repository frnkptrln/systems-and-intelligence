# Biological Veto: Candidate Architectural Requirements

*A design hypothesis for human–AI systems, not a derivation of universally necessary
components.*

---

## Purpose

High-throughput proposal systems can exceed the attention, review time, and recovery
capacity of the people affected by them. A *biological veto* is any enforceable mechanism
that lets human or ecological limits restrict consequential action.

The name does not guarantee good design. A veto can be captured, triggered too late, or
used to block legitimate participation. Every implementation needs a threat model,
measurable protected variables, authority rules, and an appeal or repair path.

## 1. Separate proposal from authorization

An AI system may generate more options than a person can responsibly inspect. Generation
should therefore not automatically confer execution authority.

Candidate mechanisms include:

- explicit approval for high-impact actions;
- staged permissions and reversible trials;
- action-rate and scope budgets;
- independent validation for claims that enable execution;
- logs that let an affected person reconstruct what happened.

The human need not be a ceremonial click-through bottleneck. The design must keep review
load within realistic cognitive and temporal capacity, or delegate it through accountable
institutions.

## 2. Match regulatory variety to the threat

Ashby's law says that successful regulation requires enough relevant variety to counter the
disturbances that matter. It does not prove that control must be centralized, decentralized,
human, or edge-based.

Local regulators can be useful when they reduce latency, preserve privacy, or continue
operating during network failure. Central services can be useful when threats require
shared information. A defensible architecture tests a layered combination against a
declared disturbance set rather than calling one topology mathematically necessary.

## 3. Protect vital variables directly

Semantic rules can miss cumulative burdens such as interruption, fatigue, cost, heat,
energy use, maintenance backlog, or ecological damage. Systems should therefore monitor
the variables whose deterioration would make participation or recovery impossible.

Possible controls include:

- hard caps on action rate, spend, compute, or resource draw;
- minimum service and care floors;
- cooldown periods and review queues;
- circuit breakers based on measured stress;
- graceful degradation rather than all-or-nothing shutdown.

Thresholds and proxies are fallible. They should expose uncertainty and be tested for
Goodhart effects, displacement of harm, false positives, and delayed measurement.

## 4. Preserve independent challenge

Friction can be valuable when it gives disagreement time to surface. It can also be simple
waste or a barrier imposed on people with less power.

The relevant design property is not friction itself but **independent challenge with
effective authority**. Reviewers need sufficient information, time, and permission to
change or stop a plan. Modular systems and separated evaluators may reduce common-mode
failure; they do not do so automatically.

## 5. Make the veto difficult to route around

A soft warning is not a veto if the optimizing process can ignore it whenever compliance is
costly. Enforcement may therefore have to sit outside the component being regulated.

That does not mean every limit must be immutable. Safe architecture also needs:

- clearly assigned ownership;
- emergency override rules with audit;
- time-bounded constraints and scheduled review;
- recovery after a false trigger;
- protection against veto capture and denial-of-service.

## Relation to TEO

TEO offers one toy representation of homeostatic regulation, coupling, and a finite
substrate budget. The Viable Corridor paper shows conditional results inside that model and
a capability-loading pattern in two synthetic implementations.

Those results motivate, but do not mathematically derive, the architectural list above.
The mappings from human review to $\gamma$, institutional coordination to $K$, or vital
systems to $D_{\max}$ require empirical calibration.

## Evaluation protocol

A biological-veto design should be compared with a simpler baseline under:

1. ordinary workload;
2. adversarial pressure to bypass the limit;
3. delayed and noisy stress measurements;
4. correlated failures;
5. legitimate emergency use;
6. recovery after a mistaken veto.

Report protected-variable violations, missed beneficial actions, review load, response
latency, bypass rate, and who bears each error.

## Current claim

> Consequential human–AI systems should preserve enforceable, measurable ways for affected
> biological and ecological conditions to restrict action.

The particular implementation remains an engineering and governance question.

## Related

- [The Substrate Veto](substrate-veto-thermodynamics.md)
- [Implementation Patterns](implementation-patterns-biological-veto.md)
- [The Viable Corridor](../../papers/viable-corridor.md)
- [Machines of Loving Grace](../narrative/machines-of-loving-grace.md)
- [Human Vital Systems Control Plane](../../logs/005_human-vital-systems-control-plane.md)
