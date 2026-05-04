"""Human Vital Systems Control Plane toy simulation.

Compares a naive efficiency planner with a vital-floor planner under the same
shock sequence. The model is intentionally small: it is a proof artifact for
the repository architecture, not a policy model.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import random
from typing import Dict, Iterable, List


INDICATORS = ("food", "heat", "care", "utilities", "trust")
FLOORS = {
    "food": 0.55,
    "heat": 0.55,
    "care": 0.55,
    "utilities": 0.55,
    "trust": 0.45,
}


@dataclass(frozen=True)
class State:
    food: float = 0.74
    heat: float = 0.74
    care: float = 0.72
    utilities: float = 0.74
    trust: float = 0.62
    efficiency: float = 0.62


@dataclass(frozen=True)
class Policy:
    name: str
    deltas: Dict[str, float]
    review_load: float
    reversibility: float


@dataclass(frozen=True)
class ImpactCard:
    policy: str
    violations: int
    worst_gap: float
    efficiency: float
    review_load: float
    reversibility: float


POLICIES = (
    Policy(
        "efficiency_routing",
        {"efficiency": 0.035, "food": -0.012, "heat": -0.012, "care": -0.010, "utilities": -0.008, "trust": -0.010},
        review_load=0.05,
        reversibility=0.45,
    ),
    Policy(
        "infrastructure_priority",
        {"efficiency": 0.020, "utilities": 0.025, "heat": -0.018, "food": -0.008, "care": -0.006, "trust": -0.006},
        review_load=0.15,
        reversibility=0.55,
    ),
    Policy(
        "food_buffer",
        {"efficiency": -0.004, "food": 0.035, "utilities": -0.006, "trust": 0.004},
        review_load=0.25,
        reversibility=0.78,
    ),
    Policy(
        "heat_zones",
        {"efficiency": -0.008, "heat": 0.045, "utilities": -0.010, "trust": 0.008},
        review_load=0.35,
        reversibility=0.80,
    ),
    Policy(
        "clinic_surge",
        {"efficiency": -0.006, "care": 0.040, "food": -0.004, "trust": 0.006},
        review_load=0.35,
        reversibility=0.75,
    ),
    Policy(
        "community_compensation",
        {"efficiency": -0.014, "food": 0.018, "heat": 0.018, "care": 0.012, "utilities": 0.008, "trust": 0.022},
        review_load=0.55,
        reversibility=0.90,
    ),
    Policy(
        "compute_throttle",
        {"efficiency": -0.016, "utilities": 0.018, "heat": 0.014, "trust": 0.010},
        review_load=0.30,
        reversibility=0.82,
    ),
)


def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def apply_delta(state: State, deltas: Dict[str, float]) -> State:
    values = state.__dict__.copy()
    for key, delta in deltas.items():
        values[key] = clamp(values[key] + delta)
    return State(**values)


def natural_drift(state: State) -> State:
    """Small recovery toward normal operating conditions."""

    values = state.__dict__.copy()
    for key in INDICATORS:
        values[key] = clamp(values[key] + 0.006 * (0.72 - values[key]))
    values["efficiency"] = clamp(values["efficiency"] + 0.020 * (0.66 - values["efficiency"]))
    return State(**values)


def shock_for_day(day: int, rng: random.Random) -> Dict[str, float]:
    """Generate repeatable stress events."""

    deltas: Dict[str, float] = {}
    if day in {12, 13, 14, 15, 52, 53, 54} or rng.random() < 0.08:
        deltas.update({"heat": deltas.get("heat", 0.0) - 0.075, "utilities": deltas.get("utilities", 0.0) - 0.035, "care": deltas.get("care", 0.0) - 0.012})
    if day in {28, 29, 67} or rng.random() < 0.07:
        deltas.update({"food": deltas.get("food", 0.0) - 0.070, "trust": deltas.get("trust", 0.0) - 0.010})
    if day in {38, 39, 40, 81} or rng.random() < 0.06:
        deltas.update({"care": deltas.get("care", 0.0) - 0.080, "trust": deltas.get("trust", 0.0) - 0.020})
    if day in {44, 72} or rng.random() < 0.04:
        deltas.update({"trust": deltas.get("trust", 0.0) - 0.060})
    return deltas


def impact_card(state: State, policy: Policy) -> ImpactCard:
    after = apply_delta(state, policy.deltas)
    gaps = [max(0.0, FLOORS[key] - getattr(after, key)) for key in INDICATORS]
    return ImpactCard(
        policy=policy.name,
        violations=sum(gap > 0 for gap in gaps),
        worst_gap=max(gaps),
        efficiency=after.efficiency,
        review_load=policy.review_load,
        reversibility=policy.reversibility,
    )


def choose_naive_efficiency(state: State) -> Policy:
    return max(POLICIES, key=lambda policy: impact_card(state, policy).efficiency)


def choose_vital_floor(state: State) -> Policy:
    def score(policy: Policy) -> float:
        card = impact_card(state, policy)
        return (
            card.efficiency
            - 3.0 * card.violations
            - 8.0 * card.worst_gap
            + 0.4 * card.reversibility
            - 0.15 * card.review_load
        )

    return max(POLICIES, key=score)


def simulate(strategy: str, days: int = 90, seed: int = 7) -> Dict[str, object]:
    rng = random.Random(seed)
    state = State()
    violations = 0
    irreversible_events = 0
    review_load = 0.0
    efficiency_total = 0.0
    worst_gap = 0.0
    chosen: List[str] = []

    chooser = choose_naive_efficiency if strategy == "naive" else choose_vital_floor

    for day in range(days):
        state = natural_drift(state)
        state = apply_delta(state, shock_for_day(day, rng))
        policy = chooser(state)
        state = apply_delta(state, policy.deltas)
        chosen.append(policy.name)

        gaps = [max(0.0, FLOORS[key] - getattr(state, key)) for key in INDICATORS]
        violations += sum(gap > 0 for gap in gaps)
        irreversible_events += sum(gap > 0.10 for gap in gaps)
        worst_gap = max(worst_gap, max(gaps))
        review_load += policy.review_load
        efficiency_total += state.efficiency

    return {
        "strategy": strategy,
        "violations": violations,
        "irreversible_events": irreversible_events,
        "worst_gap": worst_gap,
        "mean_efficiency": efficiency_total / days,
        "review_load": review_load,
        "final_state": state,
        "top_policies": policy_counts(chosen),
    }


def policy_counts(names: Iterable[str]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for name in names:
        counts[name] = counts.get(name, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def print_summary(results: List[Dict[str, object]]) -> None:
    print("| Strategy | Red-line indicator-days | Irreversible events | Worst floor gap | Mean efficiency | Review load |")
    print("|:---|---:|---:|---:|---:|---:|")
    for result in results:
        print(
            f"| {result['strategy']} | {result['violations']} | {result['irreversible_events']} | "
            f"{result['worst_gap']:.3f} | {result['mean_efficiency']:.3f} | {result['review_load']:.1f} |"
        )

    print("\nPolicy mix:")
    for result in results:
        print(f"- {result['strategy']}: {result['top_policies']}")


def main() -> None:
    results = [simulate("naive"), simulate("vital_floor")]
    print_summary(results)

    naive, vital = results
    if vital["violations"] >= naive["violations"]:
        print("\nFAILURE CONDITION: vital-floor governance did not reduce red-line violations.")
    else:
        print("\nEXPECTED RESULT: vital-floor governance reduces red-line violations by sacrificing throughput and adding review load.")


if __name__ == "__main__":
    main()
