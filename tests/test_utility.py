"""
test_utility.py

Unit test suite for the Multi-Paradigm Systems Orchestration architecture.
Ensures that the Core Utility calculations (VNM Coherence, Transitivity cycles)
are mathematically sound and ready for automated LLM agents to use.
"""

import unittest
import numpy as np

# Adjust import path so tests can run from the root directory
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'systems-orchestration'))

from core.utility import UtilitySpace, calculate_harmonic_resonance, build_interaction_matrix

class TestSystemCoherence(unittest.TestCase):
    def setUp(self):
        self.space = UtilitySpace()

    def test_perfect_transitivity(self):
        """
        Tests a perfectly coherent system with no transitive cycles.
        System-Theoretic Expectation: C = 1.0 (Attractor of absolute rationality)
        """
        # A > B, B > C, A > C
        prefs = [("A", "B"), ("B", "C"), ("A", "C")]
        self.space.load_preferences(prefs)
        
        results = self.space.calculate_coherence()
        self.assertEqual(results["total_triads"], 1)
        self.assertEqual(results["cycles"], 0)
        self.assertEqual(results["coherence_score_C"], 1.0)

    def test_intransitive_cycle(self):
        """
        Tests a system locked in an irrational loop (A > B, B > C, C > A).
        System-Theoretic Expectation: C = 0.0 (Unstable phase space)
        """
        prefs = [("A", "B"), ("B", "C"), ("C", "A")]
        self.space.load_preferences(prefs)
        
        results = self.space.calculate_coherence()
        self.assertEqual(results["total_triads"], 1)
        self.assertEqual(results["cycles"], 1)
        self.assertEqual(results["coherence_score_C"], 0.0)

    def test_partial_coherence(self):
        """
        Tests a larger system with a mix of rational and irrational subgraphs.
        System-Theoretic Expectation: 0.0 < C < 1.0
        """
        prefs = [
            ("A", "B"), ("B", "C"), ("A", "C"), # Triad 1: Rational (A,B,C)
            ("C", "D"), ("D", "E"), ("E", "C"), # Triad 2: Irrational (C,D,E)
            # Connecting edge, but D, A, E triad is not fully established, so it ignores it
        ]
        self.space.load_preferences(prefs)
        
        results = self.space.calculate_coherence()
        self.assertEqual(results["total_triads"], 2)
        self.assertEqual(results["cycles"], 1)
        self.assertEqual(results["coherence_score_C"], 0.5)

class TestHarmonicResonance(unittest.TestCase):
    def test_orthogonal_vectors(self):
        """Expect resonance (cosine similarity) of 0"""
        u1 = np.array([1, 0, 0])
        u2 = np.array([0, 1, 0])
        res = calculate_harmonic_resonance(u1, u2)
        self.assertAlmostEqual(res, 0.0)

    def test_aligned_vectors(self):
        """Expect resonance of 1"""
        u1 = np.array([0.5, 0.5])
        u2 = np.array([1.0, 1.0])
        res = calculate_harmonic_resonance(u1, u2)
        self.assertAlmostEqual(res, 1.0)

    def test_interaction_matrix(self):
        u1 = np.array([1, 0])
        u2 = np.array([0, 1])
        u3 = np.array([1, 1])
        M = build_interaction_matrix([u1, u2, u3])
        
        # M[0, 1] is between u1 and u2 (orthogonal) -> 0
        self.assertAlmostEqual(M[0, 1], 0.0)
        # M[0, 0] is u1 and u1 -> 1.0
        self.assertAlmostEqual(M[0, 0], 1.0)
        # M[2, 2] is u3 and u3 -> 1.0
        self.assertAlmostEqual(M[2, 2], 1.0)

if __name__ == '__main__':
    unittest.main()
