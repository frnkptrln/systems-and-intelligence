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
- ``embedding_distance``, ``observer_attribution`` — supporting metrics.

The metrics module is intentionally agnostic to the LLM provider. See
``lab.providers`` for the mock/real provider switch.
"""

from .delta_coherence import delta_coherence
from .persistence_scores import (
    component_coverage,
    correlate_component_coverage_with_delta_coherence,
    correlate_pstrong_with_delta_coherence,
    persistence_scores,
    pstrong,
)

__all__ = [
    "delta_coherence",
    "persistence_scores",
    "pstrong",
    "component_coverage",
    "correlate_component_coverage_with_delta_coherence",
    "correlate_pstrong_with_delta_coherence",
]
