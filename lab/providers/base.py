"""
Abstract LLM provider interface for the Agentic Identity Suite.

Two methods every provider must implement:

- `complete(prompt, system=None)` — text in, text out. The runtime of the
  generator. Used by agents to produce responses, by curation routines to
  summarize sessions, and by Layer 3 distillation when active.
- `embed(text)` — text in, vector out. Used by Δ-Kohärenz computation and
  by Layer 2 / Layer 3 self-representations.

The Anthropic API does not currently provide a public embeddings endpoint.
Real-mode providers therefore fall back to a deterministic hash-based
embedding by default. A future provider can override `embed()` with a real
embedding service without changing any caller.
"""

from abc import ABC, abstractmethod

import numpy as np


class LLMProvider(ABC):
    """Abstract base for all LLM providers used by the suite."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Short identifier for logs and traces. Example: 'mock', 'anthropic'."""

    @abstractmethod
    def complete(self, prompt: str, system: str | None = None) -> str:
        """Return a completion for `prompt`, optionally with a system message."""

    @abstractmethod
    def embed(self, text: str) -> np.ndarray:
        """Return an embedding vector for `text`."""
