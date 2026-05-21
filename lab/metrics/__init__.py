"""
lab.metrics
===========

Behavioral metrics for the Agentic Identity Suite.

- ``delta_coherence`` (Ω) — temporal trajectory coherence.
- ``persistence_scores`` (Pstrong) — simultaneous co-instantiation, Algorithm 1
  from Perrier & Bennett (2026). One instrument among several.
- ``identity_persistence`` — original Jaccard-style IP utility class.
- ``embedding_distance``, ``observer_attribution`` — supporting metrics.

The metrics module is intentionally agnostic to the LLM provider. See
``lab.providers`` for the mock/real provider switch.
"""

from .delta_coherence import delta_coherence
from .persistence_scores import pstrong, correlate_pstrong_with_delta_coherence

__all__ = [
    "delta_coherence",
    "pstrong",
    "correlate_pstrong_with_delta_coherence",
]
