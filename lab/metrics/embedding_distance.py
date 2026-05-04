"""
Embedding Distance Utility
----------------------------
Compute cosine distances across Layer 2/3 representations over time.
"""

import numpy as np


def cosine_distance_series(embeddings: list[np.ndarray]) -> list[float]:
    """
    Compute pairwise cosine distance between consecutive embeddings.

    Returns a list of distances (1 - cosine_similarity) for each step.
    """
    distances = []
    for i in range(1, len(embeddings)):
        a, b = embeddings[i - 1], embeddings[i]
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            distances.append(1.0)
        else:
            sim = float(np.dot(a, b) / (norm_a * norm_b))
            distances.append(1.0 - sim)
    return distances


def cumulative_drift(embeddings: list[np.ndarray]) -> float:
    """
    Compute total cumulative drift from the initial representation.
    High drift = the agent has changed significantly from its initial state.
    """
    if len(embeddings) < 2:
        return 0.0

    origin = embeddings[0]
    norm_origin = np.linalg.norm(origin)
    if norm_origin == 0:
        return 0.0

    final = embeddings[-1]
    norm_final = np.linalg.norm(final)
    if norm_final == 0:
        return 1.0

    sim = float(np.dot(origin, final) / (norm_origin * norm_final))
    return 1.0 - sim


def windowed_stability(embeddings: list[np.ndarray], window: int = 10) -> list[float]:
    """
    Compute variance of cosine distances within sliding windows.
    Low variance = stable identity. High variance = identity crisis.
    """
    distances = cosine_distance_series(embeddings)
    if len(distances) < window:
        return [float(np.var(distances))] if distances else [0.0]

    stabilities = []
    for i in range(len(distances) - window + 1):
        chunk = distances[i:i + window]
        stabilities.append(float(np.var(chunk)))
    return stabilities
