"""
lab.metrics
===========

Behavioral metrics for the Agentic Identity Suite.

- ``delta_coherence`` (Ω) — temporal trajectory coherence.
- ``persistence_scores`` (Pweak/Pstrong) — weak occurrence and strong
  co-instantiation over explicit windows, following Perrier & Bennett (2026).
- ``component_coverage`` — the repository's distinct fractional per-step
  coverage diagnostic.
- ``identity_persistence`` — original Jaccard-style IP utility class.
- ``generative_surprise`` — normalized coherent-deviation score (the
  historical E × C product is kept as ``generative_surprise_legacy``).
- ``embedding_distance``, ``observer_attribution`` — supporting metrics.

The metrics module is intentionally agnostic to the LLM provider. See
``lab.providers`` for the mock/real provider switch.
"""

from .delta_coherence import delta_coherence
from .generative_surprise import generative_surprise, generative_surprise_legacy
from .persistence_scores import (
    component_coverage,
    correlate_component_coverage_with_delta_coherence,
    correlate_pstrong_with_delta_coherence,
    persistence_scores,
    pstrong,
)

__all__ = [
    "delta_coherence",
    "generative_surprise",
    "generative_surprise_legacy",
    "persistence_scores",
    "pstrong",
    "component_coverage",
    "correlate_component_coverage_with_delta_coherence",
    "correlate_pstrong_with_delta_coherence",
]
