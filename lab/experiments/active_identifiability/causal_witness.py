"""Minimal active-identifiability witness.

Two linear-Gaussian causal generators induce the same observational joint
Gaussian over ``(X, Y)`` but different interventional predictions under
``do(X=x)``.  The module quantifies expected information gain about generator
identity.  It is a bounded toy result, not a general causal-discovery claim.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.stats import norm


OBSERVATIONAL_COVARIANCE_A = np.array([[1.0, 1.0], [1.0, 2.0]])
OBSERVATIONAL_COVARIANCE_B = np.array([[1.0, 1.0], [1.0, 2.0]])


@dataclass(frozen=True)
class InterventionResult:
    x: float
    information_gain_bits: float
    expected_posterior_entropy_bits: float


def observationally_equivalent() -> bool:
    """Return whether the observational covariance matrices coincide."""

    return bool(np.allclose(OBSERVATIONAL_COVARIANCE_A, OBSERVATIONAL_COVARIANCE_B))


def interventional_pdf_a(y: float, x: float) -> float:
    """Return ``p(y | do(X=x), G_A) = Normal(x, 1)``."""

    return float(norm.pdf(y, loc=x, scale=1.0))


def interventional_pdf_b(y: float, x: float) -> float:
    """Return ``p(y | do(X=x), G_B) = Normal(0, 2)`` (variance 2)."""

    del x
    return float(norm.pdf(y, loc=0.0, scale=math.sqrt(2.0)))


def information_gain_bits(x: float) -> float:
    """Compute ``I(G;Y | do(X=x))`` under equal generator priors.

    With equal priors this is the Jensen-Shannon divergence between the two
    interventional predictive distributions, expressed in bits.
    """

    def integrand(y: float) -> float:
        probability_a = interventional_pdf_a(y, x)
        probability_b = interventional_pdf_b(y, x)
        mixture = 0.5 * (probability_a + probability_b)

        value = 0.0
        if probability_a > 0.0:
            value += 0.5 * probability_a * math.log2(probability_a / mixture)
        if probability_b > 0.0:
            value += 0.5 * probability_b * math.log2(probability_b / mixture)
        return value

    value, _ = quad(integrand, -math.inf, math.inf, epsabs=1e-10)
    return float(value)


def posterior_probability_a(x: float, y: float) -> float:
    """Return ``P(G_A | y, do(X=x))`` under equal generator priors."""

    probability_a = interventional_pdf_a(y, x)
    probability_b = interventional_pdf_b(y, x)
    return probability_a / (probability_a + probability_b)


def evaluate_intervention(x: float) -> InterventionResult:
    information = information_gain_bits(x)
    return InterventionResult(
        x=x,
        information_gain_bits=information,
        expected_posterior_entropy_bits=1.0 - information,
    )


def best_cost_adjusted_intervention(
    cost_lambda: float = 0.05,
    x_min: float = 0.0,
    x_max: float = 3.0,
) -> tuple[float, float]:
    """Maximize information gain minus a quadratic intervention cost."""

    def negative_utility(x: float) -> float:
        return -(information_gain_bits(x) - cost_lambda * x * x)

    result = minimize_scalar(negative_utility, bounds=(x_min, x_max), method="bounded")
    return float(result.x), float(-result.fun)


def run_reference_experiment() -> dict[str, object]:
    """Return the complete deterministic reference result."""

    interventions = [evaluate_intervention(x) for x in (0.0, 1.0, 2.0, 3.0)]
    best_x, best_utility = best_cost_adjusted_intervention()

    return {
        "observationally_equivalent": observationally_equivalent(),
        "observational_covariance": OBSERVATIONAL_COVARIANCE_A.tolist(),
        "interventions": [asdict(result) for result in interventions],
        "posterior_examples_for_do_x_3": {
            "y_3": posterior_probability_a(3.0, 3.0),
            "y_0": posterior_probability_a(3.0, 0.0),
            "y_minus_1": posterior_probability_a(3.0, -1.0),
        },
        "cost_adjusted": {
            "lambda": 0.05,
            "domain": [0.0, 3.0],
            "best_x": best_x,
            "best_utility_bits": best_utility,
        },
    }


def main() -> None:
    print(json.dumps(run_reference_experiment(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
