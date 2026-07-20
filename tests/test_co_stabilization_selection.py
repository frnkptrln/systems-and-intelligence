"""
Regression guards for benchmark v1.12.

The tests protect the accounting, the identity of the baseline arm with
v1.11, and the qualitative headline: partner choice sorts the network
without reversing selection. They deliberately do not hard-code a positive
co-stabilization claim, since the preregistered criterion was not supported.
"""

import importlib.util
import os
import sys
import unittest

import numpy as np

_BENCH = os.path.join(
    os.path.dirname(__file__), "..", "lab", "benchmarks", "inverse-reconstruction",
)
_MOD = os.path.join(_BENCH, "co_stabilization_selection.py")
_V111 = os.path.join(_BENCH, "co_stabilization_population.py")
if not os.path.exists(_MOD):  # local standalone verification
    _MOD = os.path.join(os.path.dirname(__file__), "co_stabilization_selection.py")
    _V111 = os.path.join(os.path.dirname(__file__), "co_stabilization_population.py")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load("co_stabilization_v112", _MOD)


class TestBaselineMatchesV111(unittest.TestCase):
    """The comparison is only meaningful if the arms share one accounting."""

    @unittest.skipUnless(os.path.exists(_V111), "v1.11 module not present")
    def test_blind_arm_reproduces_v111_exactly(self):
        v11 = _load("co_stabilization_v111_ref", _V111)
        for seed in (0, 1):
            a = v11.run_population(seed, "independent", True)
            b = m.run_population(seed, "blind", "independent", True)
            np.testing.assert_allclose(a.abundance, b.abundance)
            np.testing.assert_allclose(a.linked_support, b.linked_support)
            np.testing.assert_allclose(a.link_density, b.link_density)
            self.assertEqual(a.links_formed, b.links_formed)
            self.assertEqual(a.links_broken, b.links_broken)


class TestAccounting(unittest.TestCase):
    def test_no_arm_exceeds_unused_repair_capacity(self):
        for mech in m.MECHANISMS:
            res = m.run_population(0, mech, "independent", True, steps=120)
            self.assertLessEqual(res.max_capacity_ratio, 1.0 + 1e-9, mech)

    def test_energy_never_negative(self):
        for mech in m.MECHANISMS:
            res = m.run_population(1, mech, "independent", True, steps=120)
            self.assertGreaterEqual(res.min_energy, -1e-9, mech)

    def test_blind_arm_pays_no_assessment(self):
        res = m.run_population(0, "blind", "independent", True, steps=120)
        self.assertEqual(res.assessment_paid, 0.0)

    def test_informed_arms_pay_for_partner_information(self):
        for mech in m.INFORMED:
            res = m.run_population(0, mech, "independent", True, steps=120)
            self.assertGreater(res.assessment_paid, 0.0, mech)

    def test_zero_assessment_cost_still_charges_link_cost(self):
        # Cost sweeps must vary only the information price.
        res = m.run_population(0, "partner_choice", "independent", True,
                               steps=120, assess_cost=0.0)
        self.assertEqual(res.assessment_paid, 0.0)
        self.assertGreater(res.links_formed, 0)


class TestPartnerChoiceSortsTheNetwork(unittest.TestCase):
    def test_partner_choice_excludes_low_contributors_from_links(self):
        # The headline qualitative finding: cheaters are excluded from the
        # network rather than eliminated from the population.
        edge_u, edge_v = m.lattice()[1:]
        excluded = []
        for seed in (0, 1, 2, 3):
            pop = m.run_population(
                seed, "partner_choice", "independent", True,
                initial=m.seed_invasion(seed),
            ).population
            linked = pop.occupied & (m._linked_degree(pop, edge_u, edge_v) > 0)
            if linked.any():
                excluded.append(float(np.mean(pop.support[linked] < 0.20)))
        self.assertTrue(excluded, "no seed produced a linked population")
        self.assertLess(float(np.median(excluded)), 0.10)

    def test_blind_arm_does_not_exclude_them(self):
        edge_u, edge_v = m.lattice()[1:]
        included = []
        for seed in (0, 1, 2, 3):
            pop = m.run_population(
                seed, "blind", "independent", True,
                initial=m.seed_invasion(seed),
            ).population
            linked = pop.occupied & (m._linked_degree(pop, edge_u, edge_v) > 0)
            if linked.any():
                included.append(float(np.mean(pop.support[linked] < 0.20)))
        self.assertTrue(included)
        self.assertGreater(float(np.median(included)), 0.10)


class TestSelectionStillFails(unittest.TestCase):
    def test_no_arm_reverses_support_selection(self):
        # Guards the reported falsification. If a future change makes an arm
        # retain support, this test should fail loudly and be rewritten with
        # the new result -- not silently pass.
        for mech in m.MECHANISMS:
            deltas = [m.one_seed(s, mech)["selection_delta"] for s in (0, 1, 2)]
            self.assertLess(float(np.median(deltas)), 0.0, mech)


if __name__ == "__main__":
    unittest.main()
