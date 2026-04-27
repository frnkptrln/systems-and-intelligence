# Human Vital Systems Control Plane Simulation

**Mode:** Thinking Space  
**Status:** Proof artifact  
**Claim:** Vital-floor governance should reduce red-line harm compared with naive efficiency optimization, while accepting lower throughput and higher review load.

---

## Purpose

This toy model operationalizes [Log 005: Human Vital Systems Control Plane](../../logs/human-vital-systems-control-plane.md).

It compares two planners under the same shock sequence:

1. **Naive efficiency planner:** selects the policy with the highest immediate efficiency score.
2. **Vital-floor planner:** selects policies using a Vital Impact Card that penalizes threshold violations, worst-case floor gaps, low reversibility, and review burden.

The model is deliberately small. It is not a city policy model. It is a proof artifact for the repository's architecture claim.

---

## Inputs

The simulation tracks five vital indicators plus aggregate efficiency:

- food access
- indoor heat
- care access
- utility continuity
- institutional trust
- efficiency

It injects repeatable shocks:

- cold fronts,
- logistics delays,
- clinic overload,
- trust crises.

---

## Parameters

The key parameters are:

- red-line floors per vital indicator,
- policy deltas for each intervention,
- review load,
- reversibility,
- shock schedule and random seed.

The defaults are intentionally visible in `vital_floor_simulation.py`.

---

## Run

```bash
python simulation-models/human-vital-systems/vital_floor_simulation.py
```

The script prints a Markdown table comparing:

- red-line indicator-days,
- irreversible events,
- worst floor gap,
- mean efficiency,
- review load.

---

## Expected Behavior

The naive planner should achieve higher mean efficiency while accumulating more vital-floor violations.

The vital-floor planner should reduce red-line violations by choosing slower, more reversible, more human-review-heavy interventions such as heat zones, clinic surge, community compensation, and compute throttling.

---

## Failure Condition

The architecture claim weakens if the vital-floor planner:

- does not reduce red-line violations,
- reduces visible violations only by hiding harm in unmeasured indicators,
- collapses under review latency,
- or performs no better than naive planning after shocks.

---

## Related

- [Core Claims](../../theory/core-claims.md)
- [Human Vital Systems Control Plane](../../logs/human-vital-systems-control-plane.md)
- [The Vital Floor](../../fiction/05_the_vital_floor.md)
