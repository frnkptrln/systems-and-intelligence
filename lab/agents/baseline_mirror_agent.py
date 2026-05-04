"""
Baseline Mirror Agent — The Null Hypothesis
---------------------------------------------
A control agent with flat memory storage. It optimizes purely for minimal
prediction error: responses are constructed from cosine similarity to recent
inputs. No internal model, no curation, no distillation.

This agent is the control. All other agents are measured against it.
"""

import numpy as np
from .agent_base import AgentBase


class BaselineMirrorAgent(AgentBase):
    """
    Flat-storage agent. No layers, no curation, no identity model.
    get_self_representation() returns a naive average of recent session embeddings.
    """

    def __init__(self, embedding_dim: int = 384):
        super().__init__(name="BaselineMirrorAgent")
        self.embedding_dim = embedding_dim
        self.memory: list[dict] = []
        self.rng = np.random.default_rng(42)
        # Simulated word-to-vector mapping (deterministic hash-based)
        self._vocab_cache: dict[str, np.ndarray] = {}

    def _text_to_embedding(self, text: str) -> np.ndarray:
        """
        Deterministic mock embedding: hash each word to a pseudo-random vector,
        then average. This simulates sentence-transformers without the dependency.
        """
        words = text.lower().split()
        if not words:
            return np.zeros(self.embedding_dim)

        vectors = []
        for w in words:
            if w not in self._vocab_cache:
                # Deterministic pseudo-random vector from word hash
                seed = hash(w) % (2**31)
                rng = np.random.default_rng(seed)
                self._vocab_cache[w] = rng.standard_normal(self.embedding_dim)
                self._vocab_cache[w] /= np.linalg.norm(self._vocab_cache[w]) + 1e-10
            vectors.append(self._vocab_cache[w])

        emb = np.mean(vectors, axis=0)
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb /= norm
        return emb

    def process(self, input_text: str) -> str:
        """
        Respond with the most similar previous input (pure mirror).
        If no memory, echo a transformed version of the input.
        """
        if not self.memory:
            return f"[Mirror reflects: {input_text[:80]}]"

        input_emb = self._text_to_embedding(input_text)
        best_sim = -1.0
        best_response = self.memory[-1].get("input", input_text)

        for entry in self.memory[-20:]:  # Only look at last 20 (recency bias)
            mem_emb = self._text_to_embedding(entry["input"])
            sim = float(np.dot(input_emb, mem_emb))
            if sim > best_sim:
                best_sim = sim
                best_response = entry.get("response", entry["input"])

        return best_response

    def store(self, session_data: dict) -> None:
        """Flat storage: just append."""
        self.memory.append(session_data)

    def recall(self, query: str) -> list[str]:
        """Return top-5 most similar memories."""
        query_emb = self._text_to_embedding(query)
        scored = []
        for entry in self.memory:
            mem_emb = self._text_to_embedding(entry["input"])
            sim = float(np.dot(query_emb, mem_emb))
            scored.append((sim, entry["input"]))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored[:5]]

    def get_self_representation(self) -> np.ndarray:
        """Naive average of recent session embeddings. No identity model."""
        if not self.memory:
            return np.zeros(self.embedding_dim)

        recent = self.memory[-10:]
        embeddings = [self._text_to_embedding(e["input"]) for e in recent]
        avg = np.mean(embeddings, axis=0)
        norm = np.linalg.norm(avg)
        if norm > 0:
            avg /= norm
        return avg

    def get_self_representation_text(self) -> str:
        """No self-model — just return summary of recent inputs."""
        if not self.memory:
            return "No sessions yet."
        recent = self.memory[-5:]
        topics = [e["input"][:40] for e in recent]
        return f"Recent topics: {'; '.join(topics)}"
