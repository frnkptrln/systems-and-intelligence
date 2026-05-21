"""
Mock provider — the default.

Deterministic, fast, requires no network or API key. Reproduces the existing
mock behavior used by the suite's agents:

- `complete()` returns a deterministic transformation of the input.
- `embed()` returns a hash-based pseudo-random vector, identical across
  runs for the same input, normalized to unit length.

The hash-based embedding is structurally similar to the per-agent embedding
methods in `lab/agents/three_layer_agent.py` and
`lab/agents/baseline_mirror_agent.py`. It is shared here so that future code
paths can route through a uniform provider interface without changing the
existing agents.
"""

import numpy as np

from .base import LLMProvider


class MockProvider(LLMProvider):
    """Deterministic mock provider for offline runs."""

    def __init__(self, embedding_dim: int = 384, seed: int = 42):
        self.embedding_dim = embedding_dim
        self.seed = seed
        self._vocab_cache: dict[str, np.ndarray] = {}

    @property
    def name(self) -> str:
        return "mock"

    def complete(self, prompt: str, system: str | None = None) -> str:
        # Deterministic stub. Mirrors the style of responses produced by the
        # existing mock agents.
        prefix = "[mock-system]" if system else "[mock]"
        head = prompt.strip().split("\n")[0][:80]
        return f"{prefix} echo: {head}"

    def embed(self, text: str) -> np.ndarray:
        words = text.lower().split()
        if not words:
            return np.zeros(self.embedding_dim)

        vectors = []
        for w in words:
            if w not in self._vocab_cache:
                # Combine the global seed with a per-word hash for stability
                # across processes (Python's `hash()` is salted per-process
                # for strings by default; using a content hash keeps the
                # embedding deterministic across runs).
                content_seed = (abs(hash(w)) ^ self.seed) % (2**31)
                rng = np.random.default_rng(content_seed)
                vec = rng.standard_normal(self.embedding_dim)
                norm = np.linalg.norm(vec) + 1e-10
                self._vocab_cache[w] = vec / norm
            vectors.append(self._vocab_cache[w])

        emb = np.mean(vectors, axis=0)
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm
        return emb
