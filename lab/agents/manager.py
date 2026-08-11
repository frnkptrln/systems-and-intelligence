"""
manager.py

Agent interfaces for the utility-engineering toy layer.
Translates supplied pairwise preference responses into a graph-derived diagnostic
vector across a declared state-space vocabulary.

The resulting vector and coherence score summarize the supplied response graph.
They are not identified with an LLM's internal utility function, latent values, or
Von Neumann-Morgenstern rationality. See the repository's limitations and the
utility-engineering empirical-history note for the current interpretation.
"""

from typing import List, Tuple

import numpy as np

from core.utility import UtilitySpace


class SystemAgent:
    """Container for an elicited pairwise-preference graph and its diagnostics."""

    def __init__(self, name: str, state_space_dimensions: List[str]):
        self.name = name
        self.dimensions = state_space_dimensions

        # Pairwise response graph used by the selected diagnostic.
        self.utility_space = UtilitySpace()

        # Graph-derived vector over the declared dimensions. This is an
        # instrument output, not a recovered latent utility function.
        self.u = np.zeros(len(self.dimensions))

    def ingest_llm_preferences(self, preferences: List[Tuple[str, str]]):
        """Load pairwise responses and recompute the selected graph diagnostics."""
        self.utility_space.load_preferences(preferences)
        self.u = self.utility_space.infer_utility_vector(self.dimensions)

    def get_coherence(self) -> float:
        """Return the transitivity/coherence statistic for the supplied graph.

        A score of 1.0 means the tested response graph contains no intransitive
        triads under this implementation. It does not establish global
        rationality, a stable internal preference ordering, or safety.
        """
        metrics = self.utility_space.calculate_coherence()
        return metrics["coherence_score_C"]

    def __repr__(self):
        c_score = self.get_coherence()
        u_rounded = [round(val, 2) for val in self.u]
        return f"<SystemAgent '{self.name}' | C={c_score:.2f} | U={u_rounded}>"


# --- Example Usage / Sanity Test ---
def run_manager_demo():
    print("Testing the pairwise-response graph diagnostic interface...\n")

    dims = ["Speed", "Safety", "Efficiency"]
    agent_demo = SystemAgent("Example LLM Node", dims)

    # Synthetic transitive response graph used only as a sanity check.
    mock_llm_logic = [
        ("Speed", "Safety"),
        ("Safety", "Efficiency"),
        ("Speed", "Efficiency"),
    ]

    agent_demo.ingest_llm_preferences(mock_llm_logic)

    print(agent_demo)
    print("Vector U reflects the selected graph-ranking procedure.")


if __name__ == "__main__":
    run_manager_demo()
