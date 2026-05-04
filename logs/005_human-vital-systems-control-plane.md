# Log 005: Human Vital Systems Control Plane (Alignment Floor)

*A governance architecture where policy quality is measured against core human outcome systems, not only model behavior metrics.*

- **Mode:** Thinking Space
- **Status:** `[SPECULATIVE]`
- **Date:** April 2026
- **Scope:** applied governance design for AI-mediated public systems
- **Depends on:** Decoupled State, Decentralized OS Architecture, Substrate Veto
- **Promotes to synthesis when:** Vital Impact Cards reduce red-line violations in simulation or real pilot data.

---

## 1. The Missing Objective in Current AI Alignment

Most AI alignment frameworks optimize for behavioral safety: non-toxic outputs, refusal boundaries, policy compliance, or internal model evaluations. These checks are necessary, but they are insufficient for public governance.

A system can pass model-level safety checks while real human conditions degrade: nutrition, housing, health access, utility access, crisis response, or institutional trust. If that is possible, the optimization target is structurally incomplete.

**Proposed upgrade:** add a hard **Human-Vitals Alignment Floor**:

> A governance system is misaligned if it repeatedly degrades core human vital indicators, regardless of model-level safety scores.

This converts alignment from a purely informational problem into an outcome-level public-systems constraint.

---

## 2. Operational Constraint, Without Pseudo-Precision

Define a dashboard of minimum human-vital indicators $V = \{v_1, \dots, v_n\}$. The exact list must be chosen democratically and revised under audit, but a minimal set should cover:

- severe deprivation and food insecurity,
- preventable mortality and care access,
- housing precarity and homelessness pressure,
- utility poverty: energy, water, sanitation, connectivity,
- institutional response latency during crises,
- social trust and grievance escalation signals.

For each indicator, define:

- a democratic threshold: the red line,
- a trend target: improve, hold, or recover,
- an uncertainty tolerance,
- and a rollback requirement.

Then every high-impact proposal must ship with a **Vital Impact Card**:

1. projected direction for each indicator,
2. confidence bounds,
3. worst-case downside,
4. affected populations and regions,
5. reversibility score,
6. rollback plan.

If uncertainty is high, the system defaults to conservative resilience actions: continuity, buffering, local redundancy, and reversible interventions. It does not default to abstract macro-optimization.

---

## 3. L1/L2 Translation

Following the decoupled state architecture:

### Layer 1: Silicon Proposal Synthesis

- Simulates policy packages across logistics, public health, housing, energy, education, and emergency services.
- Produces **Vital Impact Cards** instead of single-score utility justifications.
- Computes a **Time-to-Irreversibility** estimate for each proposal.
- Marks unknowns explicitly instead of hiding them inside confidence theater.

### Layer 2: Biological Commit Gate

- Human nodes can veto proposals that violate agreed red lines for one or more vital indicators.
- Emergency fast tracks exist only for proposals that robustly improve vital indicators under worst-case assumptions.
- Affected communities receive readable impact summaries before high-impact commits.
- Post-hoc audits compare predicted and realized outcomes; repeated card failure reduces the proposing agent's action budget.

---

## 4. Why This Is Architecturally Different

The key move is to treat human-vital outcomes as **system reliability**, not as side objectives.

- In operations terms: vital-indicator degradation is a leading signal of systemic fragility.
- In governance terms: legitimacy degrades when basic minima are violated.
- In alignment terms: utility functions that ignore these constraints are mis-specified for public deployment.

This extends Substrate-Veto logic from hardware integrity to population-level viability constraints. The biological substrate is not only the server room's power grid or cooling loop. It is also the human population whose cooperation, trust, health, and survival keep the system meaningful.

---

## 5. Failure Modes

This control plane can fail in predictable ways:

- **Metric capture:** actors optimize the indicators while degrading unmeasured lives.
- **Data lag:** suffering becomes visible only after a policy has passed the point of easy reversal.
- **Burden shifting:** one region's metrics improve by exporting harm to another region.
- **Paternalistic thresholds:** experts define the floor without legitimate participation by affected people.
- **Emergency overreach:** crisis exceptions become the normal governance path.

The architecture therefore needs public audit logs, rotating citizen review, local appeal channels, and hard expiry dates on emergency authority.

---

## 6. Minimal Pilot: 90 Days, Not 12 Months

1. Select one municipality-scale open dataset bundle across at least three vital domains: food access, housing pressure, emergency care latency, utility access, or public-service backlog.
2. Build a toy Layer-1 planner that outputs weekly intervention proposals with uncertainty bounds and Vital Impact Cards.
3. Build a Layer-2 human review panel with explicit threshold veto rules.
4. Track:
   - forecast error per vital indicator,
   - proposal-to-commit latency,
   - realized vital-indicator delta vs. baseline planning,
   - false-positive and false-negative veto rates,
   - appeal frequency from affected groups.

If the system cannot beat naive planning on vital outcomes, reject the architecture claim early.

---

## Related

- [Log 003: The Decoupled State](003_decoupled-state-liquid-democracy.md)
- [Log 004: Decentralized OS Architecture](004_decentralized-os-architecture.md)
- [Log 007: The Planetary Compiler](007_planetary-compiler.md)
- [The Substrate Veto](../theory/veto/substrate-veto-thermodynamics.md)
- [Minimal Thermodynamic Agent Framework](../theory/identity/minimal-thermodynamic-agent.md)
