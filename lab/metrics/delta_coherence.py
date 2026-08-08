"""Δ-Kohärenz (Delta Coherence) — temporal trajectory diagnostic.

The metric summarizes how a supplied sequence of representation vectors changes
across steps. Early versions called Ω the "fourth SII dimension" and used the
profile labels ``mirror``, ``noise``, and ``development`` as if they named agent
states. Experiments 5–7 showed that Ω can miss organizational binding entirely.

The profile strings are retained for compatibility, but they are classifier
labels produced by selected thresholds over vector-change statistics. They do
not diagnose development, identity, agency, or consciousness.
"""

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def delta_coherence(
    representations: list[np.ndarray],
    window: int = 5,
    threshold_low: float = 0.05,
    threshold_high: float = 0.25,
    threshold_consistency: float = 0.70,
) -> dict:
    """Compute selected change statistics over representation vectors.

    Parameters
    ----------
    representations:
        Embedding vectors, one per recorded step/session.
    window:
        Historical configuration parameter retained for API compatibility.
        The current implementation does not apply windowed smoothing.
    threshold_low:
        Cutoff used by the historical ``mirror`` classifier label.
    threshold_high:
        Variance cutoff used by the historical ``noise`` classifier label.
    threshold_consistency:
        Direction-similarity cutoff used by the historical ``development``
        classifier label.

    Returns
    -------
    ``mean_delta``
        Average norm of consecutive representation changes.
    ``variance``
        Variance of those change magnitudes.
    ``trajectory_consistency``
        Mean cosine similarity of consecutive change vectors.
    ``omega``
        A designed [0, 1] composite derived from the thresholds above.
    ``profile``
        One of the legacy classifier strings ``mirror``, ``noise``, or
        ``development``. The string is not an ontological conclusion.
    """
    # Keep the parameter part of the stable function signature even though the
    # present implementation does not use it for smoothing.
    _ = window

    if len(representations) < 2:
        return {
            "mean_delta": 0.0,
            "variance": 0.0,
            "trajectory_consistency": 0.0,
            "omega": 0.0,
            "profile": "mirror",
        }

    deltas = []
    delta_magnitudes = []
    for i in range(1, len(representations)):
        delta = representations[i] - representations[i - 1]
        deltas.append(delta)
        delta_magnitudes.append(float(np.linalg.norm(delta)))

    delta_magnitudes = np.array(delta_magnitudes)

    mean_delta = float(np.mean(delta_magnitudes))
    variance = float(np.var(delta_magnitudes))

    # Mean cosine alignment of consecutive change directions. A high value
    # means the vector path changes in a similar direction over adjacent steps;
    # no psychological interpretation follows from that statistic alone.
    if len(deltas) < 2:
        trajectory_consistency = 0.0
    else:
        consistencies = []
        for i in range(1, len(deltas)):
            sim = cosine_similarity(deltas[i], deltas[i - 1])
            consistencies.append(sim)
        trajectory_consistency = float(np.mean(consistencies))

    # Legacy threshold classifier. Labels are preserved for compatibility with
    # experiments and stored outputs; they should be read as names of regions
    # in this selected statistic space only.
    if variance > threshold_high:
        profile = "noise"
    elif mean_delta < threshold_low and variance < threshold_low:
        profile = "mirror"
    elif mean_delta > threshold_low and trajectory_consistency > threshold_consistency:
        profile = "development"
    elif mean_delta < threshold_low:
        profile = "mirror"
    else:
        profile = "noise"

    # Designed composite retained for historical comparisons. High Ω means a
    # trajectory falls toward the region originally labelled "development"
    # under these thresholds; it is not an IP or consciousness score.
    if profile == "development":
        omega = min(
            1.0,
            trajectory_consistency
            * (1.0 - variance / max(threshold_high, 0.01)),
        )
    elif profile == "mirror":
        omega = max(0.0, 0.2 - mean_delta)
    else:  # legacy "noise" region
        omega = max(0.0, 0.1 * (1.0 - variance / max(threshold_high, 0.01)))

    omega = float(np.clip(omega, 0.0, 1.0))

    return {
        "mean_delta": mean_delta,
        "variance": variance,
        "trajectory_consistency": trajectory_consistency,
        "omega": omega,
        "profile": profile,
    }
