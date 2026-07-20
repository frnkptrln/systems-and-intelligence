# Adversarial TEO: Resource Control Under a Threat Model

*Status: security hypothesis. TEO equations do not prevent an attacker by themselves, and a
computational workload need not expose a unique, easily detected thermodynamic signature.*

## Threat

Suppose an unauthorized controller can request compute, energy, network access, tools, or physical
actuation while bypassing an ordinary policy layer. A surrounding infrastructure may still restrict
those capabilities if authorization is enforced independently.

This is a familiar defense-in-depth pattern. The TEO vocabulary adds a resource budget, but does not
guarantee detection or isolation.

## Candidate Controls

- capability-based access to tools and data;
- independently metered compute and energy budgets;
- network segmentation and egress controls;
- anomaly detection with explicit false-positive costs;
- signed workload provenance and revocation;
- physical and organizational separation of approval from execution.

Heat and power measurements can contribute evidence, but attackers can distribute workloads, imitate
normal traffic, use stolen credentials, compromise meters, or cause harm with modest compute.
Resource starvation also risks interrupting hospitals, communications, or other vital services.

## Evaluation

Specify attacker access, defender knowledge, protected assets, and acceptable collateral failure.
Red-team evasion, meter compromise, insider authorization, workload distribution, and recovery after
false isolation. Compare the resource-control layer with simpler least-privilege baselines.

The immune-system metaphor is useful only as a prompt for detection, isolation, memory, and repair.
It is not evidence that a TEO-governed network will automatically recognize or defeat an uncoupled
agent.
