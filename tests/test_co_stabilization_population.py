"""Regression guards for the v1.11 endogenous-support population."""

import importlib.util
import os
import sys
import unittest

import numpy as np

_MOD = os.path.join(
    os.path.dirname(__file__), "..", "lab", "benchmarks",
    "inverse-reconstruction", "co_stabilization_population.py",
)
if not os.path.exists(_MOD):
    _MOD = os.path.join(
        os.path.dirname(__file__), "co_stabilization_population.py"
    )


def _load():
    spec = importlib.util.spec_from_file_location("co_stabilization_v111", _MOD)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load()


class TestPopulationAccounting(unittest.TestCase):
    def test_torus_has_four_neighbors_and_unique_edges(self):
        neighbors, edge_u, edge_v = m.lattice(side=5)
        self.assertEqual(neighbors.shape, (25, 4))
        self.assertEqual(len(edge_u), 50)
        edges = {tuple(sorted((int(u), int(v)))) for u, v in zip(edge_u, edge_v)}
        self.assertEqual(len(edges), 50)

    def test_energy_and_repair_capacity_are_bounded(self):
        result = m.run_population(seed=0, steps=120)
        self.assertGreaterEqual(result.min_energy, -1e-9)
        self.assertLessEqual(result.max_capacity_ratio, 1.0 + 1e-9)
        self.assertGreater(result.links_formed, 0)
        self.assertGreater(result.links_broken, 0)

    def test_zero_support_makes_transfer_switch_irrelevant(self):
        initial = m.initialize(seed=1)
        initial.support[:] = 0.0
        enabled = initial.copy()
        disabled = initial.copy()
        env = m.make_environment(seed=1, steps=1)
        neighbors, edge_u, edge_v = m.lattice()
        for pop, switch in ((enabled, True), (disabled, False)):
            m.population_step(
                pop, env, 0, "independent", switch,
                neighbors, edge_u, edge_v,
                reproduce=False, evolve_links=False,
            )
        np.testing.assert_array_equal(
            enabled.occupied, disabled.occupied
        )
        np.testing.assert_allclose(
            enabled.health, disabled.health
        )
        np.testing.assert_allclose(
            enabled.energy, disabled.energy
        )


class TestSupportMechanism(unittest.TestCase):
    def test_paid_support_improves_sparse_pulse_health(self):
        pop = m.initialize(seed=2)
        pop.occupied[:] = True
        pop.health[:] = 1.0
        pop.energy[:] = 1.0
        pop.support[:] = 1.0
        pop.link_gene[:] = 1.0
        pop.links[:] = True
        enabled = m.pulse_assay(pop, seed=2, regime="independent", transfer_enabled=True)
        ablated = m.pulse_assay(pop, seed=2, regime="independent", transfer_enabled=False)
        self.assertLess(enabled.recovery_time, ablated.recovery_time)
        self.assertLessEqual(enabled.max_capacity_ratio, 1.0 + 1e-9)

    def test_representative_function_selection_tension(self):
        # A regression for this finite model's headline, not a universal claim:
        # support helps the evolved network acutely but is selected downward.
        rows = [m.one_seed(seed) for seed in range(4)]
        self.assertLess(
            float(np.mean([row["support_selection"] for row in rows])), 0.0
        )
        self.assertGreater(
            float(np.mean([row["sparse_viability_gain"] for row in rows])), 0.0
        )


if __name__ == "__main__":
    unittest.main()
