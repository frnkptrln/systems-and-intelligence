"""
Δ-Kohärenz (Delta Coherence) Metric
--------------------------------------
The fourth SII dimension. Measures how an agent's self-representation
changes over time and classifies its behavioral profile.

Profiles:
  - 'mirror':      Low change, low variance → static resonance
  - 'noise':       High variance → incoherent change
  - 'development': Moderate change + high trajectory consistency → directional evolution
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
    threshold_consistency: float = 0.70
) -> dict:
    """
    Compute Δ-Kohärenz from a sequence of self-representation embeddings.

    Parameters:
        representations: list of embedding vectors, one per session
        window: smoothing window for delta computation
        threshold_low: below this mean_delta → mirror
        threshold_high: above this variance → noise
        threshold_consistency: above this trajectory_consistency → development

    Returns: {
        'mean_delta':              float,  # Average magnitude of change per step
        'variance':                float,  # Variance of change magnitudes
        'trajectory_consistency':  float,  # Cosine similarity of consecutive delta vectors
        'omega':                   float,  # Normalized Ω score for SII [0, 1]
        'profile':                 str     # 'mirror' | 'noise' | 'development'
    }
    """
    if len(representations) < 2:
        return {
            'mean_delta': 0.0,
            'variance': 0.0,
            'trajectory_consistency': 0.0,
            'omega': 0.0,
            'profile': 'mirror'
        }

    # Compute delta vectors between consecutive representations
    deltas = []
    delta_magnitudes = []
    for i in range(1, len(representations)):
        delta = representations[i] - representations[i - 1]
        deltas.append(delta)
        delta_magnitudes.append(float(np.linalg.norm(delta)))

    delta_magnitudes = np.array(delta_magnitudes)

    # Mean delta (average magnitude of change)
    mean_delta = float(np.mean(delta_magnitudes))

    # Variance of change (stability measure)
    variance = float(np.var(delta_magnitudes))

    # Trajectory consistency: cosine similarity between consecutive delta vectors
    # High value = the agent is changing in a consistent direction (development)
    # Low value = the agent's changes are random (noise)
    if len(deltas) < 2:
        trajectory_consistency = 0.0
    else:
        consistencies = []
        for i in range(1, len(deltas)):
            sim = cosine_similarity(deltas[i], deltas[i - 1])
            consistencies.append(sim)
        trajectory_consistency = float(np.mean(consistencies))

    # Profile classification
    if variance > threshold_high:
        profile = 'noise'
    elif mean_delta < threshold_low and variance < threshold_low:
        profile = 'mirror'
    elif mean_delta > threshold_low and trajectory_consistency > threshold_consistency:
        profile = 'development'
    elif mean_delta < threshold_low:
        profile = 'mirror'
    else:
        # Moderate change but inconsistent direction
        profile = 'noise'

    # Ω score: normalized composite for SII radar chart
    # High Ω = development (good), Low Ω = mirror or noise
    if profile == 'development':
        omega = min(1.0, trajectory_consistency * (1.0 - variance / max(threshold_high, 0.01)))
    elif profile == 'mirror':
        omega = max(0.0, 0.2 - mean_delta)
    else:  # noise
        omega = max(0.0, 0.1 * (1.0 - variance / max(threshold_high, 0.01)))

    omega = float(np.clip(omega, 0.0, 1.0))

    return {
        'mean_delta': mean_delta,
        'variance': variance,
        'trajectory_consistency': trajectory_consistency,
        'omega': omega,
        'profile': profile
    }
