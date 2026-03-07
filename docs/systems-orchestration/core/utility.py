"""
utility.py

Core mathematical logic for Utility Engineering.
Handles the calculation of Utility (U), Transitivity Checks (VNM Rationality),
Coherence Metrics (C), and Harmonic Resonance between agent utility vectors.
"""

import networkx as nx
import numpy as np
import itertools
from typing import List, Tuple, Dict

class UtilitySpace:
    """
    Manages the VNM preference graph for an agent and calculates 
    system stability via the Coherence Metric (C).
    """
    def __init__(self):
        self.preference_graph = nx.DiGraph()

    def load_preferences(self, preferences: List[Tuple[str, str]]):
        """
        Loads pairwise preferences. (A, B) implies A > B.
        """
        self.preference_graph.clear()
        for winner, loser in preferences:
            self.preference_graph.add_edge(winner, loser)

    def calculate_coherence(self) -> Dict[str, float]:
        """
        Calculates the System Coherence Score (C) based on the absence
        of transitive cycles in the preference graph.
        C = 1 - (T_cycles / T_total)
        """
        nodes = list(self.preference_graph.nodes())
        if len(nodes) < 3:
            return {"coherence_score_C": 1.0, "total_triads": 0, "cycles": 0}

        total_triads = 0
        intransitive_cycles = 0

        # Evaluate all triads for cycles
        for triad in itertools.combinations(nodes, 3):
            subgraph = self.preference_graph.subgraph(triad)
            
            # Only consider complete triads where all 3 edges exist
            if subgraph.number_of_edges() == 3:
                total_triads += 1
                try:
                    nx.find_cycle(subgraph)
                    intransitive_cycles += 1
                except nx.NetworkXNoCycle:
                    pass

        c_score = 1.0 - (intransitive_cycles / total_triads) if total_triads > 0 else 1.0
        
        return {
            "coherence_score_C": c_score,
            "total_triads": total_triads,
            "cycles": intransitive_cycles
        }

    def infer_utility_vector(self, dimensions: List[str]) -> np.ndarray:
        """
        Translates a preference graph into a normalized continuous utility vector U.
        Uses PageRank as a proxy for VNM utility weighting across the state space.
        """
        if len(self.preference_graph) == 0:
            return np.zeros(len(dimensions))
            
        try:
            # PageRank assigns higher scores to nodes that win matchups
            # We reverse the graph because directed edges are Winner -> Loser,
            # so we want "votes" to flow from Loser to Winner to calculate priority.
            reversed_graph = self.preference_graph.reverse()
            centrality = nx.pagerank(reversed_graph, alpha=0.85)
            
            # Map centralities to the requested dimension order
            vec = [centrality.get(dim, 0.0) for dim in dimensions]
            u_vector = np.array(vec)
            
            # Normalize to sum=1
            if np.sum(u_vector) > 0:
                u_vector = u_vector / np.sum(u_vector)
                
            return u_vector
        except Exception:
            # Fallback for unconnected/empty graphs
            return np.ones(len(dimensions)) / len(dimensions)

def calculate_harmonic_resonance(u1: np.ndarray, u2: np.ndarray) -> float:
    """
    Calculates the Harmonic Resonance between two utility vectors.
    System-Theoretic Background: Resonance is defined as the cosine similarity
    between vectors in the preference state-space. High resonance means
    the agents share a similar directional pull in their optimization.
    """
    if np.linalg.norm(u1) == 0 or np.linalg.norm(u2) == 0:
        return 0.0
    
    return np.dot(u1, u2) / (np.linalg.norm(u1) * np.linalg.norm(u2))

def build_interaction_matrix(utility_vectors: List[np.ndarray]) -> np.ndarray:
    """
    Constructs the Matrix M of all pairwise harmonic resonances.
    Used by the Harmonic paradigm for eigenvalue analysis.
    """
    n = len(utility_vectors)
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            M[i, j] = calculate_harmonic_resonance(utility_vectors[i], utility_vectors[j])
    return M
