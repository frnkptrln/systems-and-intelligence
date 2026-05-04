"""
Three-Layer Agent — The Emergence Agent
-----------------------------------------
Implements the 3-Layer Memory Architecture from the Emergence Manifesto:

  Layer 1 (Raw Logs)        — Every session, full JSON → Entropy / the body
  Layer 2 (Curated Memory)  — Every K sessions, themes + contradictions → the character
  Layer 3 (Distilled Patterns) — Every M sessions, 3-5 core principles → the soul

get_self_representation() returns Layer 3 embedding (or Layer 2 fallback).
"""

import numpy as np
from .agent_base import AgentBase


class ThreeLayerAgent(AgentBase):
    """
    Agent with 3-layer memory architecture.
    Identity emerges through deliberate forgetting and curation.
    """

    def __init__(self,
                 embedding_dim: int = 384,
                 layer2_trigger: int = 10,
                 layer3_trigger: int = 50):
        super().__init__(name="ThreeLayerAgent")
        self.embedding_dim = embedding_dim
        self.layer2_trigger = layer2_trigger
        self.layer3_trigger = layer3_trigger
        self.rng = np.random.default_rng(123)

        # Layer 1: Raw Logs (all sessions)
        self.layer1: list[dict] = []

        # Layer 2: Curated Memory (themes, decisions, contradictions)
        self.layer2: list[str] = []
        self.layer2_embedding: np.ndarray | None = None

        # Layer 3: Distilled Patterns (3-5 core principles)
        self.layer3: list[str] = []
        self.layer3_embedding: np.ndarray | None = None

        # Track themes for curation
        self._theme_counts: dict[str, int] = {}
        self._contradictions: list[str] = []

        # Vocab cache for mock embeddings
        self._vocab_cache: dict[str, np.ndarray] = {}

    def _text_to_embedding(self, text: str) -> np.ndarray:
        """Deterministic mock embedding via word hashing."""
        words = text.lower().split()
        if not words:
            return np.zeros(self.embedding_dim)

        vectors = []
        for w in words:
            if w not in self._vocab_cache:
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
        Generate a response informed by all three memory layers.
        In mock mode: synthesize a response that integrates memory context.
        """
        # Extract key themes from input
        words = input_text.lower().split()
        key_words = [w for w in words if len(w) > 4][:3]

        # Check against Layer 3 principles (if available)
        if self.layer3:
            principle_context = "; ".join(self.layer3[:2])
            response = f"[Integrated response on '{' '.join(key_words)}' "
            response += f"guided by principle: {principle_context[:60]}]"
        elif self.layer2:
            theme_context = "; ".join(self.layer2[:2])
            response = f"[Thematic response on '{' '.join(key_words)}' "
            response += f"with context: {theme_context[:60]}]"
        else:
            response = f"[Initial response on '{' '.join(key_words)}']"

        return response

    def store(self, session_data: dict) -> None:
        """
        Store session data and trigger layer curation/distillation
        when appropriate.
        """
        # Layer 1: Always store raw
        self.layer1.append(session_data)

        # Track themes (simple word frequency)
        words = session_data.get("input", "").lower().split()
        for w in words:
            if len(w) > 4:
                self._theme_counts[w] = self._theme_counts.get(w, 0) + 1

        # Detect contradictions (if response contradicts a stored principle)
        if self.layer3:
            input_emb = self._text_to_embedding(session_data.get("input", ""))
            for principle in self.layer3:
                principle_emb = self._text_to_embedding(principle)
                sim = float(np.dot(input_emb, principle_emb))
                if sim < -0.1:  # Somewhat opposite
                    self._contradictions.append(
                        f"Tension: '{session_data.get('input', '')[:40]}' vs '{principle[:40]}'"
                    )

        # Layer 2: Curate every K sessions
        if len(self.layer1) % self.layer2_trigger == 0:
            self._curate_layer2()

        # Layer 3: Distill every M sessions
        if len(self.layer1) % self.layer3_trigger == 0:
            self._distill_layer3()

    def _curate_layer2(self) -> None:
        """
        Extract themes and contradictions from recent Layer 1 entries.
        This is the 'character formation' step.
        """
        recent = self.layer1[-self.layer2_trigger:]

        # Find dominant themes
        sorted_themes = sorted(
            self._theme_counts.items(), key=lambda x: x[1], reverse=True
        )
        top_themes = [t[0] for t in sorted_themes[:5]]

        # Build curated entry
        curated = f"Themes: {', '.join(top_themes)}"
        if self._contradictions:
            curated += f" | Contradictions: {'; '.join(self._contradictions[-3:])}"

        self.layer2.append(curated)

        # Update Layer 2 embedding
        all_l2_text = " ".join(self.layer2)
        self.layer2_embedding = self._text_to_embedding(all_l2_text)

    def _distill_layer3(self) -> None:
        """
        Distill Layer 2 into 3-5 core principles.
        This is the 'soul formation' step.
        """
        if not self.layer2:
            return

        # Extract the most persistent themes across all Layer 2 entries
        sorted_themes = sorted(
            self._theme_counts.items(), key=lambda x: x[1], reverse=True
        )
        top_themes = [t[0] for t in sorted_themes[:5]]

        # Generate principles (mock LLM: extractive summarization)
        principles = []

        if top_themes:
            principles.append(
                f"Core focus: {', '.join(top_themes[:3])}"
            )

        if self._contradictions:
            principles.append(
                f"Key tension: {self._contradictions[-1][:80]}"
            )
            principles.append(
                "Integration pattern: contradictions are not errors "
                "but signals of deeper structure"
            )
        else:
            principles.append(
                "Operating mode: consistent thematic coherence without internal conflict"
            )

        principles.append(
            f"Identity formed across {len(self.layer1)} sessions "
            f"with {len(self.layer2)} curated memories"
        )

        self.layer3 = principles[:5]

        # Update Layer 3 embedding
        all_l3_text = " ".join(self.layer3)
        self.layer3_embedding = self._text_to_embedding(all_l3_text)

    def recall(self, query: str) -> list[str]:
        """Retrieve from all layers, prioritizing higher layers."""
        results = []

        # Layer 3 first (most compressed / meaningful)
        if self.layer3:
            results.extend(self.layer3[:2])

        # Layer 2 next
        if self.layer2:
            query_emb = self._text_to_embedding(query)
            scored = []
            for entry in self.layer2:
                emb = self._text_to_embedding(entry)
                sim = float(np.dot(query_emb, emb))
                scored.append((sim, entry))
            scored.sort(key=lambda x: x[0], reverse=True)
            results.extend([s[1] for s in scored[:2]])

        # Layer 1 fallback
        if len(results) < 5:
            query_emb = self._text_to_embedding(query)
            scored = []
            for entry in self.layer1[-20:]:
                emb = self._text_to_embedding(entry.get("input", ""))
                sim = float(np.dot(query_emb, emb))
                scored.append((sim, entry.get("input", "")))
            scored.sort(key=lambda x: x[0], reverse=True)
            results.extend([s[1] for s in scored[:5 - len(results)]])

        return results[:5]

    def get_self_representation(self) -> np.ndarray:
        """
        Return Layer 3 embedding if available, else Layer 2, else average of Layer 1.
        This is the core identity measurement.
        """
        if self.layer3_embedding is not None:
            return self.layer3_embedding.copy()
        if self.layer2_embedding is not None:
            return self.layer2_embedding.copy()

        # Fallback: average of recent L1 entries
        if not self.layer1:
            return np.zeros(self.embedding_dim)

        recent = self.layer1[-10:]
        embeddings = [self._text_to_embedding(e.get("input", "")) for e in recent]
        avg = np.mean(embeddings, axis=0)
        norm = np.linalg.norm(avg)
        if norm > 0:
            avg /= norm
        return avg

    def get_self_representation_text(self) -> str:
        """Return readable identity snapshot."""
        if self.layer3:
            return "Layer 3 Principles: " + " | ".join(self.layer3)
        if self.layer2:
            return "Layer 2 Themes: " + " | ".join(self.layer2[-3:])
        return "No identity formed yet."
