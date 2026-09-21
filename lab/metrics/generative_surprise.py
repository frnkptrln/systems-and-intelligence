"""Generative Surprise — the historical E × C product, transcribed.

Emergence Manifesto v1.3, Claim 6, and the glossary define

    Generative Surprise = prediction_error_observer × trajectory_consistency_agent

with ``prediction_error`` an unnormalized distance between the observer's
prediction and the agent's output, and ``trajectory_consistency`` the mean
cosine of consecutive change vectors from ``delta_coherence`` (a value in
[-1, 1]). The glossary pointed at ``lab/agents/three_layer_agent.py`` as the
place where the metric appears; that file never computed it. This module is
the first executable transcription of the definition as written.

The function below is that historical product, nothing more. Its defects are
recorded by ``tests/test_generative_surprise.py`` before they are fixed.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from .delta_coherence import delta_coherence


def generative_surprise(
    observed: Sequence[np.ndarray],
    predicted: Sequence[np.ndarray],
    representations: Sequence[np.ndarray] | None = None,
) -> dict:
    """The historical E × C product.

    ``observed[t]`` is the agent's output embedding at step ``t``;
    ``predicted[t]`` is the observer's prediction for that step;
    ``representations`` is the agent's self-representation sequence
    (defaults to ``observed``).

    Returns a dictionary with the per-step raw prediction errors, the
    trajectory-level consistency scalar, and their product ``mean``.
    """
    if len(observed) != len(predicted):
        raise ValueError("observed and predicted must have the same length")
    reps = list(representations) if representations is not None else list(observed)
    errors = [
        float(np.linalg.norm(np.asarray(o, dtype=float) - np.asarray(p, dtype=float)))
        for o, p in zip(observed, predicted)
    ]
    consistency = float(delta_coherence(reps)["trajectory_consistency"])
    mean_error = float(np.mean(errors)) if errors else 0.0
    return {
        "error": errors,
        "consistency": consistency,
        "per_step": [e * consistency for e in errors],
        "mean": mean_error * consistency,
        "n_steps": len(errors),
    }
