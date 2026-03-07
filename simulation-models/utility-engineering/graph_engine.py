"""
graph_engine.py

Implementation of the Coherence Audit for emergent Utility Functions.
Uses graph theory to evaluate Von Neumann-Morgenstern Transitivity.
"""

import networkx as nx
import itertools

class SystemCoherenceAuditor:
    def __init__(self):
        """Initializes the auditor with an empty directed graph."""
        self.graph = nx.DiGraph()

    def load_preferences(self, preferences: list[tuple[str, str]]):
        """
        Loads pairwise comparisons into the system.
        Format: [(Winner_A, Loser_B), (Winner_C, Loser_D), ...]
        """
        self.graph.clear()
        for winner, loser in preferences:
            # An edge from Winner to Loser means: Winner > Loser
            self.graph.add_edge(winner, loser)

    def analyze_triads(self) -> dict:
        """
        Analyzes all triads (groups of 3 nodes) for transitivity.
        Returns a dictionary with metrics.
        """
        nodes = list(self.graph.nodes())
        if len(nodes) < 3:
            return {"error": "Not enough nodes for triad analysis."}

        total_triads = 0
        intransitive_cycles = 0
        transitive_triads = 0
        
        # Generate all possible combinations of 3 nodes
        for triad in itertools.combinations(nodes, 3):
            subgraph = self.graph.subgraph(triad)
            
            # We only consider triads where a preference (edge) exists 
            # between all 3 nodes (complete relation)
            if subgraph.number_of_edges() == 3:
                total_triads += 1
                
                # If there is a cycle in this subgraph (A->B, B->C, C->A),
                # the relation is intransitive.
                try:
                    nx.find_cycle(subgraph)
                    intransitive_cycles += 1
                except nx.NetworkXNoCycle:
                    transitive_triads += 1

        coherence_score = 1.0 - (intransitive_cycles / total_triads) if total_triads > 0 else 0.0

        return {
            "total_triads_evaluated": total_triads,
            "transitive_triads": transitive_triads,
            "intransitive_cycles": intransitive_cycles,
            "coherence_score_C": coherence_score
        }

if __name__ == "__main__":
    auditor = SystemCoherenceAuditor()

    print("--- Test 1: Coherent System (Transitive) ---")
    # A > B, B > C, A > C (Perfectly rational)
    coherent_prefs = [("A", "B"), ("B", "C"), ("A", "C")]
    auditor.load_preferences(coherent_prefs)
    results = auditor.analyze_triads()
    print(f"Metrics: {results}\n")

    print("--- Test 2: Incoherent System (Intransitive/Cyclic) ---")
    # A > B, B > C, C > A (Irrational loop)
    incoherent_prefs = [("A", "B"), ("B", "C"), ("C", "A")]
    auditor.load_preferences(incoherent_prefs)
    results2 = auditor.analyze_triads()
    print(f"Metrics: {results2}")
