"""Regression guards for the inverse-reconstruction v1.1–v1.8 chain.

Follows the test_benchmark_headlines pattern: re-run small declared settings
and assert each headline claim inside a band — or exactly, where the crossed
design makes it an identity. The v1.2–v1.7 suites index experimental settings
(masks, guesses, rows, candidates) by their own counters and cross every
setting with every rule, so no draw is keyed to a rule's loop position; two
uniform-world claims thereby become exact identities and are pinned as such.
Bands guard the claims, not the third decimal.
"""

import importlib.util
import os
import sys
import unittest

import numpy as np

_DIR = os.path.join(
    os.path.dirname(__file__), "..",
    "lab", "benchmarks", "inverse-reconstruction",
)
sys.path.insert(0, _DIR)  # the v1.x modules import one another by name


def _load(name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(_DIR, f"{name}.py")
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class TestV11InterventionsVsObservation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.iv = _load("intervention_experiment")

    def test_kuramoto_kicks_resolve_the_locked_ambiguity(self):
        """Quoted: passive ~83% error on K; one kick ~3%; eight kicks ~0.3%."""
        res = self.iv.run_kuramoto_suite(kick_counts=(0, 1, 8), n_seeds=6)
        passive, one, eight = res["K_err"]
        self.assertGreater(passive, 0.30)
        self.assertLess(one, 0.10)
        self.assertLess(eight, 0.02)

    def test_ca_hierarchy_watching_perturbing_preparing(self):
        """Rule 90: passive plateaus at class 8; the prepared row identifies.

        Rule 0 (frozen exception): single-bit flips never collapse the class;
        only the designed preparation does.
        """
        passive = self.iv.ca_class_curve(90, "passive", budget=10, seed=0)
        self.assertEqual(passive[0], 3)          # baseline: 2^3 = class 8
        self.assertEqual(passive[-1], 3)         # more watching buys nothing
        design = self.iv.ca_class_curve(90, "design", budget=2, seed=0)
        self.assertEqual(design[1], 0)           # de Bruijn row: one step
        flip0 = self.iv.ca_class_curve(0, "flip", budget=10, seed=0)
        self.assertEqual(flip0[-1], flip0[0])    # flips reveal nothing new
        self.assertEqual(self.iv.ca_class_curve(0, "design", budget=2, seed=0)[1], 0)


class TestV12OccamIsChanceOnUniformWorlds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fs = _load("family_search")
        cls.best = cls.fs.minimal_sizes()

    def test_uniform_hit_rate_equals_chance_exactly(self):
        """Crossed identity: per mask, the Occam pick hits exactly one rule
        per consistency class, so the uniform-world hit rate is exactly
        2^-(8-k) — the 'elegance is chance' claim as an identity."""
        res = self.fs.run_occam_suite(self.best, n_masks=1)
        for k, hit, cls in zip(res["k"], res["hit"], res["class"]):
            self.assertAlmostEqual(hit, 2.0 ** (k - 8), places=12)
            self.assertAlmostEqual(cls, 2.0 ** (8 - k), places=12)

    def test_elegance_pays_only_on_simple_worlds(self):
        res = self.fs.run_occam_suite(self.best, n_masks=1)
        i = res["k"].index(5)
        self.assertGreater(res["hit_simple"][i], 0.35)
        self.assertLess(res["hit_complex"][i], 0.05)


class TestV13OptimizersCurseWedge(unittest.TestCase):
    def test_wedge_is_zero_at_u0_and_positive_at_u5(self):
        me = _load("model_exploitation")
        res = me.run_suite(us=(0, 5), n_rules=5, n_settings=24, seed=0)
        self.assertEqual(res["gap_chosen"][0], 0.0)      # model IS the world
        wedge = res["gap_chosen"][1] - res["gap_cand"][1]
        self.assertGreater(wedge, 0.04)
        self.assertLess(abs(res["gap_cand"][1]), 0.05)   # unbiased guesses


class TestV15MarkingTheGuesses(unittest.TestCase):
    def test_wmean_kills_the_wedge_and_beats_committed_regret(self):
        wm = _load("wmax_planner")
        res = wm.run_suite(us=(0, 5), n_rules=6, n_settings=40, seed=0)
        committed_wedge = res["committed"]["wedge"][1]
        wmean_wedge = res["wmean"]["wedge"][1]
        self.assertGreater(committed_wedge, 0.04)
        self.assertLess(wmean_wedge, committed_wedge / 3)
        self.assertLess(res["wmean"]["regret"][1], res["committed"]["regret"][1])


class TestV16ActingIsMeasuring(unittest.TestCase):
    def test_dense_regime_updates_collapse_and_regret_orders(self):
        cl = _load("closed_loop")
        res = cl.run_suite(cl.DENSE, n_rules=4, n_settings=6, seed=0)
        self.assertLess(res["upd_committed"]["u"][1], 0.5)
        self.assertTrue(all(u == 5.0 for u in res["frozen_committed"]["u"]))
        final = {a: res[a]["cum_regret"][-1] for a in cl.AGENTS}
        self.assertLess(final["upd_wmean"], final["upd_committed"])
        self.assertLess(final["upd_committed"], final["frozen_committed"])
        self.assertLess(final["frozen_committed"], final["random_upd"])


class TestV17EnsemblesCureDelusionNotIgnorance(unittest.TestCase):
    def test_wedge_falls_with_k_while_regret_barely_moves(self):
        en = _load("ensemble_size")
        res = en.run_suite(n_rules=4, n_settings=10, seed=0)
        self.assertGreater(res["wedge"][0], 0.03)
        self.assertLess(res["wedge"][-1], res["wedge"][0] / 2)
        self.assertLess(res["regret"][-1], res["regret"][0] + 0.005)


class TestV18MisspecificationDetection(unittest.TestCase):
    def test_center_reading_rule_is_detected_and_blind_rule_is_not(self):
        cp = _load("composition")
        A, _, _ = cp.coupled_forward(110, 90, g=0.10, seed=0)
        t_detect, class_size = cp.level1_scan(A)
        self.assertIsNotNone(t_detect)
        self.assertEqual(class_size, 0)
        A_blind, _, _ = cp.coupled_forward(90, 30, g=0.50, seed=0)
        t_blind, _ = cp.level1_scan(A_blind)
        self.assertIsNone(t_blind)


if __name__ == "__main__":
    unittest.main()
