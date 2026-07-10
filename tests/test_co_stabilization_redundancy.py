"""
Regression guards for benchmark v1.10.

The tests protect the experiment's accounting and qualitative headline:
redundancy may reallocate only existing capacity, and in the representative
sparse-shock world it must outperform matched coexistence without gaining
free repair budget. They deliberately do not hard-code a universal
co-stabilization claim.
"""

import importlib.util
import os
import sys
import unittest

import numpy as np

_MOD = os.path.join(
    os.path.dirname(__file__), "..", "lab", "benchmarks",
    "inverse-reconstruction", "co_stabilization_redundancy.py",
)
if not os.path.exists(_MOD):  # local standalone verification
    _MOD = os.path.join(
        os.path.dirname(__file__), "co_stabilization_redundancy.py"
    )


def _load():
    spec = importlib.util.spec_from_file_location("co_stabilization_v110", _MOD)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load()


class TestBudgetAccounting(unittest.TestCase):
    def test_no_architecture_exceeds_matched_capacity(self):
        n = 16
        adj = m.make_adjacency(n, "small_world", seed=0)
        damage = m.make_damage(0, n, "independent", steps=80)
        for architecture in m.ARCHITECTURES:
            result = m.simulate(
                architecture, adj, damage, threshold=0.70
            )
            self.assertLessEqual(result.max_budget_ratio, 1.0 + 1e-9)

    def test_redundancy_with_zero_transfer_equals_coexistence(self):
        n = 16
        adj = m.make_adjacency(n, "ring", seed=0)
        damage = m.make_damage(1, n, "independent", steps=80)
        co = m.simulate(
            "coexistence", adj, damage, threshold=0.70, eta=0.0
        )
        red = m.simulate(
            "redundancy", adj, damage, threshold=0.70, eta=0.0
        )
        np.testing.assert_allclose(co.health_trace, red.health_trace)


class TestQualitativeResult(unittest.TestCase):
    def test_redundancy_helps_representative_sparse_shocks(self):
        gains_vs_coexistence = []
        gains_vs_substitution = []
        for seed in range(6):
            n = 32
            adj = m.make_adjacency(n, "small_world", seed)
            damage = m.make_damage(seed, n, "independent", steps=120)
            co = m.simulate("coexistence", adj, damage, threshold=0.70)
            sub = m.simulate("substitution", adj, damage, threshold=0.70)
            red = m.simulate("redundancy", adj, damage, threshold=0.70)
            gains_vs_coexistence.append(red.viability - co.viability)
            gains_vs_substitution.append(red.viability - sub.viability)
        self.assertGreater(float(np.mean(gains_vs_coexistence)), 0.0)
        # Post-run diagnostic after P4 was falsified; this is not part of the
        # preregistered candidate criterion.
        self.assertGreater(float(np.mean(gains_vs_substitution)), 0.0)

    def test_coexistence_has_zero_counterfactual_dependency(self):
        n = 16
        adj = m.make_adjacency(n, "ring", seed=0)
        damage = m.make_damage(2, n, "independent")
        loss = m.knockout_dependency(
            "coexistence", adj, damage, threshold=0.70, targets=(0,)
        )
        self.assertAlmostEqual(loss, 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
