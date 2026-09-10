"""Closed-form feasibility check for the draft; no benchmark dynamics or estimators."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent


def wrap(angle: float) -> float:
    """Principal signed angle in [-pi, pi)."""
    return (angle + math.pi) % (2 * math.pi) - math.pi


def contraction_budget(phases: list[float], strength: float) -> dict:
    if not phases or not all(math.isfinite(x) for x in phases):
        raise ValueError("phases must be nonempty and finite")
    if not math.isfinite(strength) or not 0 <= strength <= 1:
        raise ValueError("strength must be in [0, 1]")
    real = sum(math.cos(x) for x in phases) / len(phases)
    imag = sum(math.sin(x) for x in phases) / len(phases)
    coherence = math.hypot(real, imag)
    if coherence < 1e-12:
        raise ValueError("mean phase is undefined at zero coherence")
    mean = math.atan2(imag, real)
    distances = [abs(strength * wrap(x - mean)) for x in phases]
    budget = sum(distances)
    return {
        "coherence": coherence,
        "mean_phase": mean,
        "macro_budget_rad": budget,
        "one_oscillator_max_geodesic_budget_rad": math.pi,
        "one_oscillator_match_feasible": budget <= math.pi + 1e-12,
        "component_displacements_rad": distances,
    }


def matching_capacity(phases: list[float], support: list[int]) -> dict:
    """Static budget limits, allowing each contraction strength in [0, 1].

    For a support H, D_H = sum_H |wrap(theta_i - psi)|. A contraction
    spends exactly alpha * D_H; its endpoint budget ranges over [0, D_H].
    The same-oscillator random-direction arm can copy the macro magnitudes.
    A free single-oscillator kick has capacity pi. Therefore the four arms
    have common budgets [0, min(D_H, pi)]. This characterizes feasibility;
    it does not select a budget, support distribution, or intervention rule.
    """
    full = contraction_budget(phases, 1)
    if (not support or any(type(i) is not int or not 0 <= i < len(phases)
                           for i in support) or len(set(support)) != len(support)):
        raise ValueError("support must contain distinct valid component indices")
    capacity = sum(full["component_displacements_rad"][i] for i in support)
    return {
        "full_contraction_capacity_rad": full["macro_budget_rad"],
        "support_contraction_capacity_rad": capacity,
        "common_budget_max_rad": min(capacity, math.pi),
    }


def half_support_report(phases: list[float], strength: float) -> dict:
    """Enumerate every half-support at one fixed state; no dynamics or RNG."""
    if len(phases) % 2:
        raise ValueError("half-support enumeration requires an even component count")
    macro = contraction_budget(phases, strength)
    # The pi/2 cap is a proposed alternative in the review, not a freeze choice.
    proposed_budget = min(macro["macro_budget_rad"], math.pi / 2)
    limits = [matching_capacity(phases, list(support))
              for support in itertools.combinations(range(len(phases)), len(phases) // 2)]
    return {
        "coherence": macro["coherence"],
        "requested_macro_budget_rad": macro["macro_budget_rad"],
        "half_supports": len(limits),
        "minimum_half_contraction_capacity_rad": min(
            item["support_contraction_capacity_rad"] for item in limits),
        "maximum_half_contraction_capacity_rad": max(
            item["support_contraction_capacity_rad"] for item in limits),
        "supports_unable_to_match_requested_budget": sum(
            macro["macro_budget_rad"] > item["common_budget_max_rad"] + 1e-12
            for item in limits),
        "proposed_pi_over_two_capped_budget_rad": proposed_budget,
        "supports_unable_to_match_proposed_capped_budget": sum(
            proposed_budget > item["common_budget_max_rad"] + 1e-12
            for item in limits),
        "maximum_budget_feasible_for_every_half_rad": min(
            item["common_budget_max_rad"] for item in limits),
    }


def report() -> dict:
    source = HERE / "freeze-candidate.json"
    candidate = json.loads(source.read_text())
    # Analytic certificate: r = sqrt(2)/2, each kick = pi/8,
    # total = 2*pi, while one endpoint displacement is at most pi.
    phases = [math.pi / 4] * 8 + [-math.pi / 4] * 8
    result = contraction_budget(phases, candidate["intervention"]["lambda"])
    return {
        "kind": "conditional_geometric_feasibility_certificate",
        "candidate_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "budget_convention": "sum of shortest endpoint angular displacements on S1",
        "fixture": {"components": 16, "phases": "eight +pi/4, eight -pi/4"},
        "result": result,
        "same_strength_half_control_budget_rad": sum(result["component_displacements_rad"][:8]),
        "conclusion": "under this convention the fixed-strength macro and whole-budget-one-oscillator control cannot always be budget matched",
        "benchmark_implemented": False,
        "benchmark_run": False,
        "implementation_authorized": candidate["implementation_authorized"],
        "execution_authorized": candidate["execution_authorized"],
        "required_review_decision": "freeze the circular/path budget convention and revise the control or strength rule before benchmark implementation",
        "half_control_feasibility": {
            "assumption": "nonovershooting contractions with separately adjustable strengths in [0,1]; shortest endpoint angular budget",
            "common_budget_interval": "[0, min(pi, sum_H |wrap(theta_i-psi)|)] for selected half H",
            "original_fixture": half_support_report(phases, candidate["intervention"]["lambda"]),
            "aligned_half_fixture": {
                "phases": "eight zero, four +pi/4, four -pi/4",
                **half_support_report([0.0] * 8 + [math.pi / 4] * 4 + [-math.pi / 4] * 4,
                                      candidate["intervention"]["lambda"]),
            },
            "conclusion": "a pi/2 cap fixes the original fixture but cannot ensure positive budget matching for every random half at nonzero coherence",
        },
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, sort_keys=True))
