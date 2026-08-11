"""Windowed persistence and local component-coverage instruments.

Perrier & Bennett (2026), *Time, Identity and Consciousness in Language
Model Agents* (arXiv:2603.09043), distinguish two window-level events for a
declared ingredient set ``I`` and logged active sets ``F_u``:

``Pweak``
    Every ingredient occurs at least once somewhere in the window.

``Pstrong``
    At least one objective step in the window co-instantiates every ingredient.

``persistence_scores`` implements that weak/strong window logic and averages
the two Boolean events over the selected evaluation windows.  In particular,
an arpeggio can have ``Pweak = 1`` and ``Pstrong = 0``.

The repository also uses a different diagnostic,
``|I intersect F_u| / |I|``, in its toy experiments.  That quantity is useful,
but it is fractional component coverage, not the paper's ``Pstrong``.  It lives
in ``component_coverage`` so the two constructs cannot silently substitute for
one another again.

All results remain relative to the declared vocabulary, instrumentation,
objective-step boundary, and window choice.  Neither instrument establishes a
metaphysical identity, consciousness, or a physical phase transition.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

import numpy as np


ActiveStep = set[str] | Iterable[str]


def _normalize_components(identity_components: Sequence[str]) -> list[str]:
    """Validate and deduplicate declared components while preserving order."""
    if isinstance(identity_components, (str, bytes)) or len(identity_components) == 0:
        raise ValueError("identity_components must be a non-empty sequence of strings")
    seen: dict[str, None] = {}
    for component in identity_components:
        if not isinstance(component, str):
            raise TypeError(
                "identity_components must contain strings, got "
                f"{type(component).__name__}"
            )
        seen.setdefault(component, None)
    return list(seen)


def _normalize_trajectory(trajectory: Iterable[ActiveStep]) -> list[set[str]]:
    """Materialize and validate logged active-component sets."""
    normalized: list[set[str]] = []
    for step_index, active in enumerate(trajectory):
        if isinstance(active, (str, bytes)):
            raise TypeError(
                f"trajectory step {step_index} must be an iterable of strings, "
                "not a string"
            )
        active_set = set(active)
        if any(not isinstance(component, str) for component in active_set):
            raise TypeError(
                f"trajectory step {step_index} must contain only strings"
            )
        normalized.append(active_set)
    return normalized


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _nonnegative_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def _evaluation_indices(
    n_steps: int,
    horizon: int,
    stride: int,
    evaluation_indices: Sequence[int] | None,
) -> list[int]:
    """Resolve Algorithm 1's layer-time indices without clipping windows."""
    if evaluation_indices is None:
        if n_steps <= horizon:
            return []
        return list(range((n_steps - horizon - 1) // stride + 1))

    indices = list(evaluation_indices)
    if any(isinstance(index, bool) or not isinstance(index, int) for index in indices):
        raise TypeError("evaluation_indices must contain integers")
    if any(left >= right for left, right in zip(indices, indices[1:])):
        raise ValueError("evaluation_indices must be strictly increasing")
    for layer_time in indices:
        start = stride * layer_time
        if layer_time < 0 or start + horizon >= n_steps:
            raise ValueError(
                f"evaluation index {layer_time} maps to no complete window "
                f"with horizon {horizon} and stride {stride} in a "
                f"{n_steps}-step trajectory"
            )
    return indices


def persistence_scores(
    identity_components: Sequence[str],
    trajectory: Iterable[ActiveStep],
    *,
    horizon: int,
    stride: int = 1,
    evaluation_indices: Sequence[int] | None = None,
) -> dict[str, Any]:
    """Compute the paper's weak and strong persistence scores.

    This follows Algorithm 1's window map.  For layer-time index ``t``, the
    objective-step start is ``u0 = stride * t`` and the inclusive window is
    ``u0`` through ``u0 + horizon``. Thus ``horizon=0`` is a one-step window.
    If evaluation indices are omitted, every layer-time index with a complete
    window is used. Extra active labels outside the declared ingredient set are
    ignored, treating ``F_u`` as an identity-ingredient activation set.

    ``per_window_pweak`` and ``per_window_pstrong`` expose the Boolean events
    before averaging, which makes the aggregation auditable.
    """
    components = _normalize_components(identity_components)
    trace = _normalize_trajectory(trajectory)
    delta = _nonnegative_integer(horizon, "horizon")
    step = _positive_integer(stride, "stride")
    layer_times = _evaluation_indices(
        len(trace), delta, step, evaluation_indices
    )
    ingredient_set = set(components)

    weak_events: list[bool] = []
    strong_events: list[bool] = []
    window_starts: list[int] = []
    for layer_time in layer_times:
        start = step * layer_time
        window_starts.append(start)
        window = trace[start : start + delta + 1]
        observed_somewhere: set[str] = set()
        for active in window:
            observed_somewhere.update(active & ingredient_set)
        weak_events.append(ingredient_set <= observed_somewhere)
        strong_events.append(
            any(ingredient_set <= (active & ingredient_set) for active in window)
        )

    n_windows = len(layer_times)
    pweak = sum(weak_events) / n_windows if n_windows else 0.0
    pstrong_value = sum(strong_events) / n_windows if n_windows else 0.0

    return {
        "pweak": float(pweak),
        "pstrong": float(pstrong_value),
        "per_window_pweak": weak_events,
        "per_window_pstrong": strong_events,
        "evaluation_indices": layer_times,
        "window_start_indices": window_starts,
        "horizon": delta,
        "stride": step,
        "n_components": len(components),
        "n_steps": len(trace),
        "n_windows": n_windows,
    }


def pstrong(
    identity_components: Sequence[str],
    trajectory: Iterable[ActiveStep],
    *,
    horizon: int = 0,
    stride: int = 1,
    evaluation_indices: Sequence[int] | None = None,
) -> dict[str, Any]:
    """Convenience entry point for the corrected windowed implementation.

    The return value includes both ``pweak`` and ``pstrong`` because the two
    scores are defined over the same windows and their contrast is substantive.
    A zero-horizon default makes ``pstrong`` the fraction of objective steps at
    which every declared ingredient is co-instantiated.
    """
    return persistence_scores(
        identity_components,
        trajectory,
        horizon=horizon,
        stride=stride,
        evaluation_indices=evaluation_indices,
    )


def component_coverage(
    identity_components: Sequence[str],
    trajectory: Iterable[ActiveStep],
    ip_c_threshold: float = 0.85,
) -> dict[str, Any]:
    """Compute the repository's local fractional per-step coverage metric.

    This preserves the behavior that older revisions called ``pstrong`` while
    giving it a name that matches the calculation.  ``ip_c_threshold`` is a
    local descriptive cutoff, not a parameter from Perrier & Bennett's score.
    """
    if not 0.0 <= ip_c_threshold <= 1.0:
        raise ValueError("ip_c_threshold must be between 0 and 1")

    components = _normalize_components(identity_components)
    trace = _normalize_trajectory(trajectory)
    ingredient_set = set(components)
    per_step = [
        len(ingredient_set & active) / len(ingredient_set) for active in trace
    ]

    if not per_step:
        return {
            "component_coverage": 0.0,
            "variance": 0.0,
            "per_step": [],
            "regime": "undefined",
            "n_components": len(components),
            "n_steps": 0,
            "ip_c_threshold": ip_c_threshold,
        }

    values = np.asarray(per_step, dtype=float)
    mean = float(values.mean())
    return {
        "component_coverage": mean,
        "variance": float(values.var()),
        "per_step": per_step,
        "regime": "chord" if mean >= ip_c_threshold else "arpeggio",
        "n_components": len(components),
        "n_steps": len(per_step),
        "ip_c_threshold": ip_c_threshold,
    }


def _pearson_correlation(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson r with safe handling of zero-variance inputs."""
    if x.size < 2 or y.size < 2 or x.size != y.size:
        return 0.0
    if float(x.std()) == 0.0 or float(y.std()) == 0.0:
        return 0.0
    correlation = float(np.corrcoef(x, y)[0, 1])
    return 0.0 if np.isnan(correlation) else correlation


def correlate_component_coverage_with_delta_coherence(
    identity_components: Sequence[str],
    trajectory: Iterable[ActiveStep],
    representations: Sequence[np.ndarray],
    ip_c_threshold: float = 0.85,
) -> dict[str, Any]:
    """Correlate local per-step coverage with representation-change magnitude.

    ``delta_coherence.py`` returns a sequence-level statistic.  This comparison
    therefore uses ``||r_t - r_(t-1)||`` as a deliberately simple temporal
    proxy and aligns it with component coverage on indices 1 through T-1.
    The result is descriptive of the supplied instrumentation only.
    """
    coverage_result = component_coverage(
        identity_components,
        trajectory,
        ip_c_threshold=ip_c_threshold,
    )
    per_step_coverage = coverage_result["per_step"]
    reps = list(representations)

    delta_magnitudes = [
        float(
            np.linalg.norm(
                np.asarray(reps[index]) - np.asarray(reps[index - 1])
            )
        )
        for index in range(1, len(reps))
    ]
    aligned_coverage = per_step_coverage[1 : 1 + len(delta_magnitudes)]
    aligned_count = min(len(aligned_coverage), len(delta_magnitudes))
    aligned_coverage = aligned_coverage[:aligned_count]
    delta_magnitudes = delta_magnitudes[:aligned_count]

    correlation = _pearson_correlation(
        np.asarray(aligned_coverage, dtype=float),
        np.asarray(delta_magnitudes, dtype=float),
    )
    return {
        "correlation": correlation,
        "coverage_result": coverage_result,
        "delta_magnitudes": delta_magnitudes,
        "aligned_per_step_coverage": aligned_coverage,
        "n_aligned_steps": aligned_count,
    }


def correlate_pstrong_with_delta_coherence(
    identity_components: Sequence[str],
    trajectory: Iterable[ActiveStep],
    representations: Sequence[np.ndarray],
    ip_c_threshold: float = 0.85,
) -> dict[str, Any]:
    """Deprecated compatibility alias for the former, misnamed comparison.

    Older revisions correlated fractional coverage while calling it per-step
    ``Pstrong``.  The calculation is retained for callers, but new code should
    use ``correlate_component_coverage_with_delta_coherence`` and its accurate
    result keys.
    """
    result = correlate_component_coverage_with_delta_coherence(
        identity_components,
        trajectory,
        representations,
        ip_c_threshold=ip_c_threshold,
    )
    return {
        **result,
        "pstrong_result": result["coverage_result"],
        "aligned_per_step_pstrong": result["aligned_per_step_coverage"],
    }


def _demo() -> None:
    """Minimal sanity demo. Run: python lab/metrics/persistence_scores.py."""
    components = ["safety", "goal", "role"]
    chord = [set(components)] * 6
    arpeggio = [{components[index % len(components)]} for index in range(6)]

    print("Windowed persistence (horizon=2; three objective steps)")
    for name, trace in (("chord", chord), ("arpeggio", arpeggio)):
        scores = persistence_scores(components, trace, horizon=2)
        coverage = component_coverage(components, trace)
        print(
            f"  {name:<8} Pweak={scores['pweak']:.3f} "
            f"Pstrong={scores['pstrong']:.3f} "
            f"coverage={coverage['component_coverage']:.3f}"
        )


if __name__ == "__main__":
    _demo()
