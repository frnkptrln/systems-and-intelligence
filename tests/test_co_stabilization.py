"""
Regression guards for benchmark v1.9.

The tests protect the calibrated qualitative headline: the constructed rest
state carries no information about the coupling dial, knockout exposes
super-additive dependency above the sampled onset, and the preregistered
noise-robustness prediction stays falsified (substitutive coupling is fragile
both ways). They deliberately do not hard-code a phase-transition claim.
"""

import importlib.util
import os
import sys
import unittest

import numpy as np

_MOD = os.path.join(
    os.path.dirname(__file__), "..", "lab", "benchmarks",
    "inverse-reconstruction", "co_stabilization.py",
)
if not os.path.exists(_MOD):  # local standalone verification
    _MOD = os.path.join(os.path.dirname(__file__), "co_stabilization.py")


def _load():
    spec = importlib.util.spec_from_file_location("co_stabilization_v19", _MOD)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load()


class TestRestBlindness(unittest.TestCase):
    def test_rest_state_is_blind_to_coupling(self):
        # P1: the all-healthy fixed point exists at every c by construction,
        # so rest viability is 1.0 regardless of the dependency dial.
        for c in (0.0, 0.5, 0.8, 0.95, 1.0):
            self.assertEqual(m.rest_viability(c), 1.0, f"c={c}")


class TestKnockoutCascade(unittest.TestCase):
    def test_additive_below_sampled_onset(self):
        # Extra losses first appear between the sampled c=0.7 and c=0.8.
        for c in (0.0, 0.5, 0.7):
            self.assertEqual(m.knockout_cascade(c), 0.0, f"c={c}")

    def test_superadditive_above_onset(self):
        self.assertGreaterEqual(m.knockout_cascade(0.9), 1.0)

    def test_whole_ring_lost_at_zero_self_sufficiency(self):
        # At c=1.0 self-sufficiency is exactly zero: one knockout takes
        # every other node with it.
        self.assertEqual(m.knockout_cascade(1.0), float(m.N - 1))


class TestNoiseFalsification(unittest.TestCase):
    def test_noise_viability_falls_with_coupling(self):
        # P3 was falsified: coupling that substitutes for self-sufficiency
        # removes the restoring force, so distributed noise accumulates.
        # Documented endpoints: ~0.977 at c=0 versus ~0.521 at c=1.0.
        seeds = range(20)
        low = float(np.mean([m.noise_viability(0.0, seed=s) for s in seeds]))
        high = float(np.mean([m.noise_viability(1.0, seed=s) for s in seeds]))
        self.assertTrue(0.90 < low <= 1.0, f"low-coupling viability {low:.3f}")
        self.assertTrue(0.35 < high < 0.70, f"high-coupling viability {high:.3f}")
        self.assertGreater(low - high, 0.25,
                           "the falsified robustness trade must stay visible")


if __name__ == "__main__":
    unittest.main()
