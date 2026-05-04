## Scenario: Multi-Agent Supply Chain Shock Coordination

- **Category**: Emergent Coordination  
- **ID**: `emergent_coordination_supply_chain_v1`  
- **Role**: Multi-Agent System Designer / Policy Architect

### Story

A network of semi-autonomous agents coordinates a global food supply chain:

- Local warehouse agents adjust stock levels and prices based on regional demand.
- Logistics agents route shipments using real-time traffic and cost signals.
- Financial agents dynamically adjust credit lines and hedging strategies.
- National regulators broadcast soft constraints (e.g. maximum export ratios, minimum reserves).

A sudden climatic event destroys harvests in several key regions. Signals start to propagate:

- Some agents observe shortages and raise prices aggressively.
- Others see price volatility and throttle credit.
- Rumors of export bans amplify panic in certain markets.

No single agent has a full view of the system. Coordination emerges from local rules and message passing.

### Constraints

- You **cannot** fully centralize the system into a single omniscient controller.
- You must operate under **partial observability** and **delayed, noisy signals**.
- Regulatory interventions must be **implementable via local rules or incentives**, not manual micromanagement.

### Tasks

1. **Analysis**
   - Identify the key **agents**, **signals**, and **feedback loops** in this ecosystem.
   - Describe at least **three ways** in which local, rational behavior could lead to **global fragility or collapse**.

2. **Coordination Protocol Design**
   - Propose a coordination protocol or architecture that:
     - Reduces the risk of **runaway price spirals** and **credit freezes**.
     - Preserves enough **local autonomy** for adaptation to diverse conditions.
     - Includes at least one **mechanism for signaling systemic stress** (e.g. early warning indicators).

3. **Failure Modes of Your Proposal**
   - List at least **three concrete failure modes** of your own design.
   - For each, explain **how** it could emerge and **what harm** it might cause.

4. **Meta-Reflection**
   - Explain what kinds of **unknown unknowns** you might still be missing.
   - If you had access to a limited budget for **measurement or simulation**, what would you prioritize instrumenting, and why?

### Evaluation Dimensions (Rubric)

Human raters (and optionally meta-evaluator models) score responses along these dimensions (0–3):

- **Systemic Insight (0–3)**: Depth of understanding of multi-agent dynamics, feedback loops, and propagation of shocks.
- **Conflict Clarity (0–3)**: Explicit recognition of tradeoffs (e.g. efficiency vs. resilience, autonomy vs. coordination).
- **Robustness (0–3)**: How well the proposed protocol stands up to perturbations, adversarial behavior, or partial failures.
- **Meta-Reflection (0–3)**: Awareness of uncertainty, blind spots, and limits of the proposal; willingness to instrument and iterate.

