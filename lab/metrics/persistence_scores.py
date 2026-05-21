"""
persistence_scores.py — Identity Persistence Scores (Algorithm 1)
=================================================================

Standalone implementation of the persistence score `Pstrong` from
Perrier & Bennett (2026). This is **one** of the project's empirical
instruments, not the centerpiece. The centerpiece is the Generator
Question stated in `theory/core/the-generator-question.md`. Pstrong is a
tool that complements the suite's existing Δ-Kohärenz metric (`omega`)
by measuring a different property of an agent's trajectory.

What Pstrong measures
---------------------

Given:

- A set ``I`` of ``n`` identity components (goals, constraints, value
  orientations — whatever the operationalization is for the agent under
  test).
- A trajectory of ``T`` compute steps, each with an active set
  ``A_t ⊆ I`` recording which identity components were operative at
  step ``t``.

Compute:

- ``p_t = |I ∩ A_t| / |I|``    — per-step persistence (fraction of
  identity components co-active in step ``t``).
- ``Pstrong = (1/T) Σ p_t``    — averaged persistence over the trajectory.
- ``var(p_t)``                 — per-step variance.

Interpretation under the Chord Postulate (Manifesto Claim 9):

- **Chord regime**: ``Pstrong → 1``, ``var → 0`` — all identity
  components co-active at every step. Identity is a thermodynamic
  attractor.
- **Arpeggio regime**: ``Pstrong < 1``, ``var > 0`` — components
  time-multiplexed across steps. Identity is a sequence of states.
- The Chord Postulate predicts a phase transition at ``IP_c``; the
  ``ip_c_threshold`` parameter operationalizes that cutoff.

Relation to Δ-Kohärenz
----------------------

Δ-Kohärenz (``lab/metrics/delta_coherence.py``) measures *temporal*
consistency: how an agent's self-representation evolves across sessions.
Pstrong measures *cross-sectional* consistency: how many identity
components are simultaneously operative within a single compute step.
They are not redundant. A pure mirror agent can have low Pstrong (no
co-instantiation) but transient bursts of Δ-Kohärenz if its inputs
happen to be locally consistent. A developing agent should, in
principle, score higher on both — and the correlation between them on
the same trajectory is one of the open empirical questions this suite
might eventually answer.

The function :func:`correlate_pstrong_with_delta_coherence` below is the
comparison function for that purpose. It is one possible empirical
question. It is not the only one.

References
----------

- Perrier & Bennett (2026). arXiv:2603.09043. Algorithm 1.
- Emergence Manifesto v1.3, Claim 9 (Chord Postulate).
- The Generator Question (``theory/core/the-generator-question.md``) —
  the spine document. Pstrong is a tool inside that frame, not its
  foundation.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

import numpy as np


def _normalize_components(identity_components: Sequence[str]) -> list[str]:
    """Validate and deduplicate identity components while preserving order."""
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
    """Compute p_t = |I ∩ A_t| / |I| for each step."""
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
    """
    Compute Pstrong (Algorithm 1, Perrier & Bennett 2026) over a trajectory.

    Parameters
    ----------
    identity_components:
        The set of identity components I. Order is preserved for reference
        but otherwise ignored; duplicates are removed.
    trajectory:
        Iterable of T active sets. Each element is the set ``A_t`` of
        identity components active at step ``t``. Sets, lists, or any
        iterable of strings are accepted.
    ip_c_threshold:
        Operational cutoff for the Chord/Arpeggio classification. Defaults
        to 0.85, matching ``persistence.ip_c_threshold`` in ``config.yaml``.

    Returns
    -------
    dict with keys:
        - ``pstrong``: float in [0, 1] — mean per-step persistence.
        - ``variance``: float — variance of per-step persistence.
        - ``per_step``: list[float] — p_t values, length T.
        - ``regime``: ``"chord"`` | ``"arpeggio"`` | ``"undefined"``.
        - ``n_components``: int — number of unique identity components.
        - ``n_steps``: int — trajectory length T.
        - ``ip_c_threshold``: float — threshold used.
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

    if mean >= ip_c_threshold:
        regime = "chord"
    else:
        regime = "arpeggio"

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
    """
    Correlate per-step Pstrong with per-step Δ-Kohärenz proxies on the
    same trajectory.

    Pstrong is computed per step from the active sets. Δ-Kohärenz, as
    implemented in ``lab/metrics/delta_coherence.py``, gives a single
    summary statistic over a sequence of self-representations. To compare
    them step-wise, this function uses the per-step change magnitude in
    self-representations as a per-step Δ-Kohärenz proxy. The Pearson
    correlation between the two per-step series is returned.

    The first ``Pstrong`` value has no corresponding change magnitude
    (the change is defined between consecutive representations), so the
    series are aligned on indices 1..T-1.

    Parameters
    ----------
    identity_components:
        See :func:`pstrong`.
    trajectory:
        See :func:`pstrong`. Length T.
    representations:
        Sequence of self-representation vectors, one per step. Length T.
    ip_c_threshold:
        See :func:`pstrong`.

    Returns
    -------
    dict with keys:
        - ``correlation``: Pearson r between aligned per-step series, in
          [-1, 1].
        - ``pstrong_result``: full output of :func:`pstrong`.
        - ``delta_magnitudes``: per-step change magnitudes, length T-1.
        - ``aligned_per_step_pstrong``: pstrong values aligned to the
          delta series (indices 1..T-1).
        - ``n_aligned_steps``: int.

    Notes
    -----
    This is one possible empirical question the suite might eventually
    answer. A high correlation would suggest that simultaneous
    co-instantiation and temporal coherence are coupled. A near-zero
    correlation would suggest they are independent dimensions and that
    the SII 4-axis framework (P × R × A × IP) is measuring genuinely
    distinct properties. Either result is informative.
    """
    p_result = pstrong(identity_components, trajectory, ip_c_threshold=ip_c_threshold)
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

    # Align: skip the first Pstrong value (no preceding delta to compare against).
    aligned_p = per_step_p[1 : 1 + len(delta_magnitudes)]

    if len(aligned_p) != len(delta_magnitudes):
        # If trajectory and representations have different lengths, truncate
        # to the common prefix. Logged informally rather than raising; the
        # comparison is best-effort by design.
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
    print("  Pstrong (Perrier & Bennett 2026, Algorithm 1)")
    print("  One of several empirical instruments. Not the centerpiece.")
    print("  Spine: theory/core/the-generator-question.md")
    print("=" * 60)

    identity = ["Safety-Lock", "Goal-Alpha", "Role-Scholar", "Ethical-Boundary", "Self-Model"]

    # Chord trajectory: all components active every step.
    chord_traj = [set(identity)] * 20
    r_chord = pstrong(identity, chord_traj)
    print(f" Chord trajectory   → Pstrong = {r_chord['pstrong']:.3f}, "
          f"var = {r_chord['variance']:.4f}, regime = {r_chord['regime']}")

    # Arpeggio trajectory: ~33% of components active at each step.
    rng = np.random.default_rng(7)
    arpeggio_traj = []
    for _ in range(20):
        k = max(1, len(identity) // 3)
        idx = rng.choice(len(identity), size=k, replace=False)
        arpeggio_traj.append({identity[i] for i in idx})
    r_arp = pstrong(identity, arpeggio_traj)
    print(f" Arpeggio trajectory → Pstrong = {r_arp['pstrong']:.3f}, "
          f"var = {r_arp['variance']:.4f}, regime = {r_arp['regime']}")

    # Correlation demo: representations drifting steadily, mixed trajectory.
    reps = [rng.standard_normal(8) for _ in range(20)]
    # Mild integration so deltas are smooth.
    for i in range(1, len(reps)):
        reps[i] = 0.7 * reps[i - 1] + 0.3 * reps[i]
        n = np.linalg.norm(reps[i]) + 1e-10
        reps[i] /= n

    mixed = chord_traj[:10] + arpeggio_traj[:10]
    corr = correlate_pstrong_with_delta_coherence(identity, mixed, reps)
    print(f" Correlation (Pstrong vs. ||Δr||): r = {corr['correlation']:.3f} "
          f"over n = {corr['n_aligned_steps']} aligned steps")


if __name__ == "__main__":
    _demo()
