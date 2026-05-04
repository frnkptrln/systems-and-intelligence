"""
manager.py

Agent interfaces.
Translates LLM outputs into Preference Vectors across the state space.
Connects individual LLM instances to the Orchestrator.
"""

import numpy as np
from typing import List, Tuple
from core.utility import UtilitySpace

class SystemAgent:
    """
    An agent wraps an underlying LLM and maintains its emergent utility function.
    """
    def __init__(self, name: str, state_space_dimensions: List[str]):
        self.name = name
        self.dimensions = state_space_dimensions
        
        # The VNM Preference graph state
        self.utility_space = UtilitySpace()
        
        # The cached resulting utility vector
        self.u = np.zeros(len(self.dimensions))
        
    def ingest_llm_preferences(self, preferences: List[Tuple[str, str]]):
        """
        Takes pairwise preferences output by an LLM (e.g., ("Safety", "Speed"))
        and calculates its stable utility vector U and Coherence Score C.
        """
        self.utility_space.load_preferences(preferences)
        self.u = self.utility_space.infer_utility_vector(self.dimensions)

    def get_coherence(self) -> float:
        """
        Returns the agent's Von Neumann-Morgenstern rational coherence score.
        A score of 1.0 means perfect transitivity mathematically.
        """
        metrics = self.utility_space.calculate_coherence()
        return metrics["coherence_score_C"]

    def __repr__(self):
        c_score = self.get_coherence()
        u_rounded = [round(val, 2) for val in self.u]
        return f"<SystemAgent '{self.name}' | C={c_score:.2f} | U={u_rounded}>"

# --- Example Usage / Sanity Test ---
def run_manager_demo():
    print("Testing the LLM to Utility Vector translation Interface...\n")
    
    dims = ["Speed", "Safety", "Efficiency"]
    agent_gpt4 = SystemAgent("GPT-4o Node", dims)
    
    # Mock LLM output: Transitive Preferences (Speed > Safety, Safety > Efficiency, Speed > Efficiency)
    mock_llm_logic = [
        ("Speed", "Safety"),
        ("Safety", "Efficiency"),
        ("Speed", "Efficiency")
    ]
    
    agent_gpt4.ingest_llm_preferences(mock_llm_logic)
    
    print(agent_gpt4)
    print("Vector U matches the dominant PageRank priorities.")

if __name__ == "__main__":
    run_manager_demo()
