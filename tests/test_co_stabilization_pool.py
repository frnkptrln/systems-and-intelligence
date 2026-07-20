"""
Regression guards for benchmark v1.13.

The tests protect the accounting, the identity of the donor arm with v1.11,
and the two qualitative headlines: pooling nearly removes selection against
support without reversing it, and pooling reverses the invasion outcome.
They do not hard-code a positive retention claim, since the preregistered
criterion was not met.
"""

import importlib.util
import os
import sys
import unittest

import numpy as np

_BENCH = os.path.join(
    os.path.dirname(__file__), "..", "lab", "benchmarks", "inverse-reconstruction",
)
_MOD = os.path.join(_BENCH, "co_stabilization_pool.py")
_V111 = os.path.join(_BENCH, "co_stabilization_population.py")
if not os.path.exists(_MOD):  # local standalone verification
    _MOD = os.path.join(os.path.dirname(__file__), "co_stabilization_pool.py")
    _V111 = os.path.join(os.path.dirname(__file__), "co_stabilization_population.py")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load("co_stabilization_v113", _MOD)


class TestDonorArmMatchesV111(unittest.TestCase):
    """The comparison is only meaningful if the arms share one accounting."""

    @unittest.skipUnless(os.path.exists(_V111), "v1.11 module not present")
    def test_donor_arm_reproduces_v111_exactly(self):
        v11 = _load("co_stabilization_v111_pool_ref", _V111)
        for seed in (0, 1):
            a = v11.run_population(seed, "independent", True)
            b = m.run_population(seed, "donor", "independent", True)
            np.testing.assert_allclose(a.abundance, b.abundance)
            np.testing.assert_allclose(a.linked_support, b.linked_support)
            np.testing.assert_allclose(a.link_density, b.link_density)
            self.assertEqual(a.links_formed, b.links_formed)
            self.assertEqual(a.links_broken, b.links_broken)


class TestAccounting(unittest.TestCase):
    def test_no_arm_exceeds_unused_repair_capacity(self):
        for arm in m.ARMS:
            res = m.run_population(0, arm, "independent", True, steps=150)
            self.assertLessEqual(res.max_capacity_ratio, 1.0 + 1e-9, arm)

    def test_energy_never_negative(self):
        for arm in m.ARMS:
            res = m.run_population(1, arm, "independent", True, steps=150)
            self.assertGreaterEqual(res.min_energy, -1e-9, arm)

    def test_pool_levy_is_bounded_by_group_capacity(self):
        # A group can never distribute more than eta times what it collected.
        pop = m.initialize(3)
        edge_u, edge_v = m.lattice()[1:]
        spare = np.where(pop.occupied, m.REPAIR_BUDGET, 0.0)
        pop.health = np.where(pop.occupied, 0.5, 0.0)
        energy_before = pop.energy.sum()
        health_before = pop.health.sum()
        draw, ratio = m._route_pool(pop, spare, edge_u, edge_v)
        spent = energy_before - pop.energy.sum()
        gained = pop.health.sum() - health_before
        self.assertLessEqual(ratio, 1.0 + 1e-9)
        self.assertAlmostEqual(spent, draw, places=9)
        self.assertLessEqual(gained, m.TRANSFER_ETA * draw + 1e-9)

    def test_zero_support_group_transfers_nothing(self):
        pop = m.initialize(4)
        pop.support[:] = 0.0
        pop.health = np.where(pop.occupied, 0.5, 0.0)
        edge_u, edge_v = m.lattice()[1:]
        spare = np.where(pop.occupied, m.REPAIR_BUDGET, 0.0)
        draw, ratio = m._route_pool(pop, spare, edge_u, edge_v)
        self.assertEqual(draw, 0.0)
        self.assertEqual(ratio, 0.0)


class TestComponents(unittest.TestCase):
    def test_components_are_disjoint_and_linked(self):
        pop = m.initialize(0)
        edge_u, edge_v = m.lattice()[1:]
        groups = m._components(pop, edge_u, edge_v)
        seen = set()
        for g in groups:
            self.assertGreaterEqual(len(g), 2)
            for node in g:
                self.assertNotIn(int(node), seen)
                seen.add(int(node))
                self.assertTrue(pop.occupied[node])


class TestHeadlines(unittest.TestCase):
    def test_pool_reduces_selection_pressure_against_support(self):
        # The measured headline: pooling nearly removes the loss the donor
        # arm shows. Not that it reverses it -- the criterion was not met.
        donor = [m.one_seed(s, "donor")["selection_delta"] for s in (0, 1, 2)]
        pool = [m.one_seed(s, "pool")["selection_delta"] for s in (0, 1, 2)]
        self.assertLess(float(np.median(donor)), -0.05)
        self.assertGreater(float(np.median(pool)), float(np.median(donor)))

    def test_pool_reverses_the_invasion_outcome(self):
        # P3 was predicted to fail and failed in the opposite direction:
        # pooling suppresses cheaters below their seeded level.
        donor = [m.invasion_test(s, "donor")["end"] for s in (0, 1, 2)]
        pool = [m.invasion_test(s, "pool")["end"] for s in (0, 1, 2)]
        self.assertGreater(float(np.median(donor)), 0.10)
        self.assertLess(float(np.median(pool)), 0.10)


if __name__ == "__main__":
    unittest.main()
