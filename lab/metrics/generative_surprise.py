"""Generative Surprise — coherent deviation, with explicit normalization.

History
-------
Emergence Manifesto v1.3, Claim 6, and the glossary defined

    Generative Surprise = prediction_error_observer × trajectory_consistency_agent

with ``prediction_error`` an unnormalized distance between the observer's
prediction and the agent's output, and ``trajectory_consistency`` the mean
cosine of consecutive change vectors from ``delta_coherence`` (a value in
[-1, 1]). No code implemented it until 2026-09-21; the glossary pointed at
``lab/agents/three_layer_agent.py``, which never computed it. The product as
written is kept below as ``generative_surprise_legacy`` because
``tests/test_generative_surprise.py`` reproduces its three defects:

1. Not a conjunction. The error term is unbounded, so one large deviation
   times a small consistency outranks a moderate deviation with moderate
   consistency. "Both high" was the stated intent and was not enforced.
2. Scale-dependent ranking. The error term carries the scale of the
   embedding space; the consistency term does not. Rescaling every vector by
   ``lambda > 0`` multiplies the score by ``lambda``, so trajectories embedded
   at different scales, or judged by observers with different units, cannot
   be ranked against each other.
3. Undocumented null-vector convention. A missing prediction (the zero
   vector) *raised* the score, and the repository's two cosine helpers
   disagree: ``delta_coherence.cosine_similarity`` returns 0 for a null
   operand, ``embedding_distance.cosine_distance_series`` returns distance 1.

Corrected definition
--------------------
For step ``t`` with output ``o_t``, observer prediction ``p_t``, and
self-representation change vectors ``d_t = v_t - v_{t-1}``:

    E_t  = (1 - cos(o_t, p_t)) / 2               in [0, 1]
    C_t  = max(0, cos(d_t, d_{t-1}))             in [0, 1]
    GS_t = E_t * C_t                             in [0, 1]

``E_t`` is 0 when the prediction is right up to a positive scale, 1/2 when it
is orthogonal, 1 when it is anti-aligned. ``C_t`` is 1 when the trajectory
continues in the same direction, 0 for an orthogonal or reversed step.
Random isotropic change has ``C_t`` near 0 in high dimension, which is the
"noise surprises but is not coherent" case the definition was written for.

Properties (each is checked by the test suite):

* Conjunction: ``0 <= GS_t <= min(E_t, C_t)``, so ``GS_t >= g`` implies both
  ``E_t >= g`` and ``C_t >= g``. This is the product t-norm on the unit
  square; it is what makes "both high" a theorem instead of a hope.
* Invariance: every ``E_t``, ``C_t``, ``GS_t`` is unchanged when all vectors
  are mapped by ``v -> lambda Q v`` for any ``lambda > 0`` and any orthogonal
  ``Q`` (the similarity group fixing the origin), because both factors are
  cosines. ``E_t`` is further invariant under rescaling ``o_t`` and ``p_t``
  by *different* positive factors. The ranking of steps within a trajectory
  and of trajectories against each other is therefore scale-free. The metric
  is *not* invariant under translation of the embedding origin, and it does
  not see deviations that change only the magnitude of ``o_t``; both are
  consequences of choosing cosines and are stated rather than hidden.
* Null-vector convention: a cosine with an operand of norm at most ``eps``
  is *undefined*. Every undefined factor is set to 0, so an undefined term
  can lower a step's score to 0 but can never raise it. The number of
  undefined terms is returned so a caller can see how much of a trajectory
  the convention touched.

What the metric is not
----------------------
A scale-free coherent-deviation statistic over declared embeddings and a
declared observer prediction. It is not a measure of creativity,
development, agency, or selfhood, and it inherits every limitation of the
embedding and of the observer model that produced ``p_t``.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from .delta_coherence import delta_coherence

DEFAULT_EPS = 1e-12

NULL_VECTOR_CONVENTION = (
    "a cosine whose operand has norm <= eps is undefined; every undefined "
    "factor is set to 0, so it can lower a step's score but never raise it"
)


def _as_vectors(values: Sequence[np.ndarray], name: str) -> list[np.ndarray]:
    vectors = [np.asarray(v, dtype=float).reshape(-1) for v in values]
    if len(vectors) > 1 and any(v.shape != vectors[0].shape for v in vectors):
        raise ValueError(f"{name} must contain vectors of one dimension")
    return vectors


def _cosine(a: np.ndarray, b: np.ndarray, eps: float) -> float | None:
    """Cosine similarity, or ``None`` when an operand is a null vector."""
    norm_a = float(np.linalg.norm(a))
    norm_b = float(np.linalg.norm(b))
    if norm_a <= eps or norm_b <= eps:
        return None
    value = float(np.dot(a, b) / (norm_a * norm_b))
    return min(1.0, max(-1.0, value))


def generative_surprise(
    observed: Sequence[np.ndarray],
    predicted: Sequence[np.ndarray],
    representations: Sequence[np.ndarray] | None = None,
    *,
    eps: float = DEFAULT_EPS,
) -> dict:
    """Normalized Generative Surprise per step, with the conventions above.

    Parameters
    ----------
    observed:
        ``o_t``, the agent's output embedding at each step.
    predicted:
        ``p_t``, the observer's prediction of ``o_t``; same length.
    representations:
        ``v_t``, the agent's self-representation at each step, from which the
        change vectors are formed. Defaults to ``observed``.
    eps:
        Norm threshold below which a vector counts as null.

    Returns
    -------
    A dictionary with ``step_indices`` (the steps ``t >= 2`` at which two
    change vectors exist), the per-step ``error``, ``consistency`` and
    ``per_step`` scores, their ``mean`` and ``max``, ``n_steps``, the counts
    ``undefined_error_terms`` and ``undefined_consistency_terms``, and the
    ``convention`` string.
    """
    if len(observed) != len(predicted):
        raise ValueError("observed and predicted must have the same length")
    outputs = _as_vectors(observed, "observed")
    predictions = _as_vectors(predicted, "predicted")
    reps = _as_vectors(representations if representations is not None else observed,
                       "representations")
    if len(reps) != len(outputs):
        raise ValueError("representations must have the same length as observed")

    deltas = [reps[t] - reps[t - 1] for t in range(1, len(reps))]

    step_indices: list[int] = []
    errors: list[float] = []
    consistencies: list[float] = []
    scores: list[float] = []
    undefined_error = 0
    undefined_consistency = 0

    for t in range(2, len(outputs)):
        cos_prediction = _cosine(outputs[t], predictions[t], eps)
        if cos_prediction is None:
            undefined_error += 1
            error = 0.0
        else:
            error = (1.0 - cos_prediction) / 2.0

        cos_direction = _cosine(deltas[t - 1], deltas[t - 2], eps)
        if cos_direction is None:
            undefined_consistency += 1
            consistency = 0.0
        else:
            consistency = max(0.0, cos_direction)

        step_indices.append(t)
        errors.append(error)
        consistencies.append(consistency)
        scores.append(error * consistency)

    return {
        "step_indices": step_indices,
        "error": errors,
        "consistency": consistencies,
        "per_step": scores,
        "mean": float(np.mean(scores)) if scores else 0.0,
        "max": float(np.max(scores)) if scores else 0.0,
        "n_steps": len(scores),
        "undefined_error_terms": undefined_error,
        "undefined_consistency_terms": undefined_consistency,
        "convention": NULL_VECTOR_CONVENTION,
    }


def generative_surprise_legacy(
    observed: Sequence[np.ndarray],
    predicted: Sequence[np.ndarray],
    representations: Sequence[np.ndarray] | None = None,
) -> dict:
    """The historical E × C product, retained so its defects stay reproducible.

    Mean Euclidean prediction error times the trajectory-level
    ``trajectory_consistency`` scalar of ``delta_coherence``. Do not use it
    for a new result; it is here for the regression test and for reading the
    manifesto's original formula.
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
