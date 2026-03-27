---
status: "Formalized / Demonstrated"
note: "Maps the TEO framework variables to executable code and benchmarked environments."
---

# Minimal Thermodynamic Agent Framework

## Conceptual Mapping to Code

The Thermodynamics of Orchestration (TEO) framework proposes that intelligence cannot be purely unconstrained optimization; it must be physically and mathematically grounded in dynamic stability.

This minimal implementation operationalizes those abstract concepts into explicitly measurable and executable code defined in `core/constraints.py` and `core/minimal_agent.py`.

### 1. Thermodynamic Variables

*   **Energy (`energy`):**
    *   *Theory:* The physical or computational work required to displace a state.
    *   *Implementation:* A continuous float representing resource usage (e.g., compute steps or budget). Actions like `aggressive_optimize` consume high energy (15.0), whereas a simple `stabilize` act consumes minimal energy (2.0).

*   **Entropy (`entropy`):**
    *   *Theory:* The measure of disorder, unpredictability, or state variance in a system.
    *   *Implementation:* Accumulates naturally over time (+1.0 per step) and sharply increases when undertaking aggressive optimization (+10.0).

*   **Stability (`stability_score`):**
    *   *Theory:* Maintaining the system state within bounded attractors.
    *   *Implementation:* Calculated as the inverse of entropy (`1.0 / (entropy + 1e-6)`). The constrained agent aims to keep this high.

*   **Task Success (`task_success`):**
    *   *Theory:* The functional directive or goal.
    *   *Implementation:* Standard reinforcement reward. Aggressive optimization yields high success (+10.0), but at steep thermodynamic costs.

### 2. Free Energy Objective

*   *Theory:* Systems implicitly minimize "Free Energy" by balancing their goals against internal disorder.
*   *Implementation:* `F = Entropy + Energy - Reward`. By explicitly coding the Biological Veto, the Constrained Agent effectively minimizes this function, contrasting with standard models that only maximize reward.

### 3. Biological Veto

*   *Theory:* A hard physiological or structural boundary that overrides abstract goal optimization when systemic integrity is threatened.
*   *Implementation:* The `evaluate_constraints()` check in `ConstrainedAgent`. If energy > `energy_threshold` or entropy > `entropy_threshold`, the agent abandons its goal tracking (`task_success`) to execute a `stabilize` action, reducing entropy significantly until safe boundaries are restored.

---

## Running the Benchmark

The framework comes with a minimal executable benchmark comparing a `NaiveMaximizer` (which purely optimizes for `task_success`) against a `ConstrainedAgent` (which utilizes the Biological Veto).

To run the comparison baseline, execute the following from the root directory:

```bash
python3 benchmarks/minimal_teo_benchmark.py
```

### Expected Results
*   **Naive Maximizer:** Quickly accumulates `task_success` points but easily breaches critical thermodynamic thresholds (e.g., Entropy > 100), triggering a catastrophic system collapse and resulting in negative total success and low stability.
*   **Constrained Agent:** Actively monitors its `.evaluate_constraints()` function. When it detects rising entropy (approaching the threshold of 50.0), it fires the **Biological Veto**, overriding normal actions to `stabilize`. The result is a system that maintains high stability, successfully completes the task over the given horizon, and utilizes far less chaotic energy.
