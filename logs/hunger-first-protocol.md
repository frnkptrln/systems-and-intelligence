# Log 005: Human Vital Systems Control Plane (Alignment Floor)

*A governance architecture where policy quality is measured against core human outcome systems, not only model behavior metrics.*

**Status:** `[SPECULATIVE]`
**Date:** April 2026

---

## 1. The Missing Objective in Current AI Alignment

Most AI alignment frameworks optimize for behavioral safety (non-toxic outputs, refusal boundaries, policy compliance). This is necessary but insufficient for public governance.

A system can pass model-level safety checks while real human conditions degrade (nutrition, housing, health access, institutional trust). If that is possible, the optimization target is structurally incomplete.

**Proposed upgrade:** Add a hard **Human-Vitals Alignment Floor**:

> A governance system is misaligned if it repeatedly degrades core human vital indicators, regardless of model-level safety scores.

This converts alignment from a purely informational problem into an outcome-level public-systems constraint.

---

## 2. Operational Constraint (No pseudo-precision)

Define a dashboard of minimum human-vital indicators $V = \{v_1, \dots, v_n\}$, for example:

- severe deprivation and food insecurity
- preventable mortality and care access
- housing precarity / homelessness pressure
- utility poverty (energy/water access)
- institutional response latency in crises

For each indicator, define:
- a democratic threshold (red line),
- a trend target (improve / hold / recover),
- and an uncertainty tolerance.

Then every high-impact proposal must ship with a **Vital Impact Card**:
1. projected direction for each indicator,
2. confidence bounds,
3. worst-case downside,
4. rollback plan.

If uncertainty is high, the protocol defaults to conservative resilience actions (continuity, buffering, local redundancy), not abstract macro-optimization.

---

## 3. Protocol Translation (L1/L2)

Following the decoupled state architecture:

### Layer 1 (Silicon): Proposal Synthesis
- Simulates policy packages (trade, subsidy, logistics, storage, rationing contingencies).
- Produces **Vital Impact Cards**:
  - expected impact per vital indicator
  - uncertainty bounds
  - affected regions/populations
  - reversibility score

### Layer 2 (Biological): Commit Gate
- Human nodes can veto proposals that violate agreed red lines for one or more vital indicators.
- Fast-track lane for proposals that robustly improve multiple vital indicators under worst-case assumptions.
- Mandatory post-hoc audit: if realized outcomes violate the card, proposing agent budget is slashed.

---

## 4. Why This Is Architecturally Different

The key move is to treat human-vital outcomes as **system reliability**, not as side objectives.

- In operations terms: vital-indicator degradation is a leading signal of systemic fragility.
- In governance terms: legitimacy degrades when basic minima are violated.
- In alignment terms: utility functions that ignore these constraints are mis-specified for public deployment.

This extends Substrate-Veto logic from hardware integrity to population-level viability constraints.

---

## 5. Minimal Pilot (90 Days, not 12 months)

1. Select one municipality-scale open dataset bundle across at least 3 vital domains (e.g., food, housing, emergency care latency).
2. Build a toy Layer-1 planner that outputs weekly intervention proposals with uncertainty bounds.
3. Build a human-review panel (Layer 2) with explicit threshold veto rules.
4. Track:
   - forecast error per vital indicator
   - proposal-to-commit latency
   - realized vital-indicator delta vs baseline planning
   - false-positive/false-negative veto rate

If the system cannot beat naive planning on vital outcomes, reject the architecture claim early.

---

## Related

- [Log 003: The Decoupled State](decoupled-state-liquid-democracy.md)
- [Log 004: Decentralized OS Architecture](decentralized-os-architecture.md)
- [The Substrate Veto](../theory/substrate-veto-thermodynamics.md)
- [Minimal Thermodynamic Agent Framework](../theory/minimal-thermodynamic-agent.md)
