"""Persistence scores for instrumented component-activity traces.

This module implements the trajectory-level ``Pstrong`` construction used in
Perrier & Bennett (2026), *Time, Identity and Consciousness in Language Model
Agents* (arXiv:2603.09043), as one instrument among several in this repository.

What the score measures
-----------------------

Given a declared set ``I`` of components and a trajectory of active sets
``A_t``, the implementation computes

``p_t = |I ∩ A_t| / |I|``

and averages ``p_t`` over the recorded trajectory. The source uses this kind of
instrumentation to distinguish ingredient-wise occurrence over a window from
co-instantiation at an objective step.

The score is relative to the experimenter's component vocabulary, trace
instrumentation, step boundary, and threshold. It does **not** establish a
metaphysical identity, phenomenal consciousness, a thermodynamic attractor, or
a universal phase transition.

Chord / Arpeggio labels
-----------------------

This repository uses ``chord`` and ``arpeggio`` as names for two operational
regimes. A high ``Pstrong`` means most declared components are marked active at
most recorded objective steps; a lower value means fewer are co-recorded. The
``ip_c_threshold`` parameter is a local classification cutoff chosen by the
experiment. It is not itself evidence of a physical critical point.

Perrier & Bennett describe their framework as a conservative toolkit for
identity evaluation from instrumented scaffold traces. The repository keeps
that scope: the metric can test a declared organization without deciding what
counts as a true self.

Relation to Δ-Kohärenz
----------------------

Δ-Kohärenz (``lab/metrics/delta_coherence.py``) and ``Pstrong`` use different
observables. ``Pstrong`` summarizes component co-activity; the comparison helper
below uses representation-change magnitude as a temporal proxy. Their empirical
relationship is an open question, not a predicted signature of development.

References
----------

- Perrier & Bennett (2026), arXiv:2603.09043.
- ``theory/identity/chord-vs-arpeggio-identity.md`` for the repository's
  deflated commit-time interpretation.
- ``theory/reference/limitations-and-honest-assessment.md`` for scope.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

import numpy as np


def _normalize_components(identity_components: Sequence[str]) -> list[str]:
    """Validate and deduplicate declared components while preserving order."""
    if not identity_components:
        raise ValueError("identity_components must be a non-empty sequence")
    seen: dict[str, None] = {}
    for c in identity_components:
        if not isinstance(c, str):
            raise TypeError(
                f"identity_components must be strings, got {type(c).__name__}"
            )
        seen.setdefault(c, None)
    return list(seen)


def _per_step_persistence(
    identity_set: set[str],
    trajectory: Iterable[set[str] | Iterable[str]],
) -> list[float]:
    """Compute p_t = |I ∩ A_t| / |I| for each recorded step."""
    n = len(identity_set)
    if n == 0:
        return []
    per_step: list[float] = []
    for active in trajectory:
        active_set = active if isinstance(active, set) else set(active)
        intersection = identity_set & active_set
        per_step.append(len(intersection) / n)
    return per_step


def pstrong(
    identity_components: Sequence[str],
    trajectory: Iterable[set[str] | Iterable[str]],
    ip_c_threshold: float = 0.85,
) -> dict[str, Any]:
    """Compute trajectory-level component co-activity.

    Parameters
    ----------
    identity_components:
        The declared component set ``I``. The historical parameter name is
        retained for compatibility; this function does not decide whether the
        supplied components constitute identity.
    trajectory:
        Iterable of active sets ``A_t`` recorded at objective steps.
    ip_c_threshold:
        Experiment-local cutoff for the ``chord`` / ``arpeggio`` label.

    Returns
    -------
    A dictionary containing the mean score, per-step variance, per-step scores,
    local regime label, component/step counts, and threshold used.
    """
    components = _normalize_components(identity_components)
    identity_set = set(components)
    per_step = _per_step_persistence(identity_set, trajectory)

    t = len(per_step)
    if t == 0:
        return {
            "pstrong": 0.0,
            "variance": 0.0,
            "per_step": [],
            "regime": "undefined",
            "n_components": len(components),
            "n_steps": 0,
            "ip_c_threshold": ip_c_threshold,
        }

    arr = np.asarray(per_step, dtype=float)
    mean = float(arr.mean())
    var = float(arr.var())

    regime = "chord" if mean >= ip_c_threshold else "arpeggio"

    return {
        "pstrong": mean,
        "variance": var,
        "per_step": per_step,
        "regime": regime,
        "n_components": len(components),
        "n_steps": t,
        "ip_c_threshold": ip_c_threshold,
    }


def _pearson_correlation(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson r with safe handling of zero-variance inputs."""
    if x.size < 2 or y.size < 2 or x.size != y.size:
        return 0.0
    if float(x.std()) == 0.0 or float(y.std()) == 0.0:
        return 0.0
    matrix = np.corrcoef(x, y)
    r = float(matrix[0, 1])
    if np.isnan(r):
        return 0.0
    return r


def correlate_pstrong_with_delta_coherence(
    identity_components: Sequence[str],
    trajectory: Iterable[set[str] | Iterable[str]],
    representations: Sequence[np.ndarray],
    ip_c_threshold: float = 0.85,
) -> dict[str, Any]:
    """Compare per-step ``Pstrong`` with representation-change magnitude.

    ``delta_coherence.py`` returns a sequence-level statistic, so this helper
    uses ``||r_t - r_{t-1}||`` as a deliberately simple step-wise temporal
    proxy and reports its Pearson correlation with component co-activity.

    The first ``Pstrong`` value has no preceding representation delta, so the
    series are aligned on indices 1..T-1. A correlation here is descriptive of
    the supplied trajectory and instrumentation; it does not establish that
    either statistic measures identity or consciousness.
    """
    p_result = pstrong(
        identity_components,
        trajectory,
        ip_c_threshold=ip_c_threshold,
    )
    per_step_p = p_result["per_step"]

    reps = list(representations)
    if len(reps) < 2:
        return {
            "correlation": 0.0,
            "pstrong_result": p_result,
            "delta_magnitudes": [],
            "aligned_per_step_pstrong": [],
            "n_aligned_steps": 0,
        }

    delta_magnitudes = []
    for i in range(1, len(reps)):
        diff = np.asarray(reps[i]) - np.asarray(reps[i - 1])
        delta_magnitudes.append(float(np.linalg.norm(diff)))

    aligned_p = per_step_p[1 : 1 + len(delta_magnitudes)]

    if len(aligned_p) != len(delta_magnitudes):
        m = min(len(aligned_p), len(delta_magnitudes))
        aligned_p = aligned_p[:m]
        delta_magnitudes = delta_magnitudes[:m]

    r = _pearson_correlation(
        np.asarray(aligned_p, dtype=float),
        np.asarray(delta_magnitudes, dtype=float),
    )

    return {
        "correlation": r,
        "pstrong_result": p_result,
        "delta_magnitudes": delta_magnitudes,
        "aligned_per_step_pstrong": aligned_p,
        "n_aligned_steps": len(aligned_p),
    }


def _demo() -> None:
    """Minimal sanity demo. Run: python -m lab.metrics.persistence_scores"""
    print("=" * 60)
    print("  Pstrong: declared component co-activity over a trajectory")
    print("  One operational instrument; no identity ontology implied")
    print("=" * 60)

    components = [
        "Safety-Lock",
        "Goal-Alpha",
        "Role-Scholar",
        "Ethical-Boundary",
        "Self-Model",
    ]

    full_traj = [set(components)] * 20
    r_full = pstrong(components, full_traj)
    print(
        f" Full-set trajectory    → Pstrong = {r_full['pstrong']:.3f}, "
        f"var = {r_full['variance']:.4f}, regime = {r_full['regime']}"
    )

    rng = np.random.default_rng(7)
    partial_traj = []
    for _ in range(20):
        k = max(1, len(components) // 3)
        idx = rng.choice(len(components), size=k, replace=False)
        partial_traj.append({components[i] for i in idx})
    r_partial = pstrong(components, partial_traj)
    print(
        f" Partial-set trajectory → Pstrong = {r_partial['pstrong']:.3f}, "
        f"var = {r_partial['variance']:.4f}, regime = {r_partial['regime']}"
    )

    reps = [rng.standard_normal(8) for _ in range(20)]
    for i in range(1, len(reps)):
        reps[i] = 0.7 * reps[i - 1] + 0.3 * reps[i]
        n = np.linalg.norm(reps[i]) + 1e-10
        reps[i] /= n

    mixed = full_traj[:10] + partial_traj[:10]
    corr = correlate_pstrong_with_delta_coherence(components, mixed, reps)
    print(
        f" Correlation (Pstrong vs. ||Δr||): r = {corr['correlation']:.3f} "
        f"over n = {corr['n_aligned_steps']} aligned steps"
    )


if __name__ == "__main__":
    _demo()
