"""Closed-form feasibility check for the draft; no benchmark dynamics or estimators."""
from __future__ import annotations

import hashlib
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
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, sort_keys=True))
