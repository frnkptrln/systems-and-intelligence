"""Guards for Experiment B (representation and reconstruction difficulty).

Pinned: the rule maps are involutions and produce the transformed truth on a
fully covered trace; invertible re-encodings leave the consistent class size
unchanged (the experiment's central prediction, checked exactly on a sample);
a lossy encoding produces contradictions; and the declared CI subgrid
reproduces the committed ``results/ci_subgrid.json``.
"""

import importlib.util
import json
import os
import sys
import unittest

_HERE = os.path.dirname(__file__)
_EXP = os.path.join(_HERE, "..", "lab", "experiments", "representation_reconstruction")
_MODULE = os.path.join(_EXP, "representation_reconstruction.py")


def _load():
    spec = importlib.util.spec_from_file_location("representation_reconstruction_test", _MODULE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


rr = _load()

SAMPLE_RULES = (0, 30, 54, 90, 110, 150, 184, 255)


class TestRuleMaps(unittest.TestCase):
    def test_maps_are_involutions(self):
        for rule in range(256):
            self.assertEqual(rr.complement_rule(rr.complement_rule(rule)), rule)
            self.assertEqual(rr.reflect_rule(rr.reflect_rule(rule)), rule)

    def test_transformed_truth_is_recovered_on_a_covered_trace(self):
        for rule in SAMPLE_RULES:
            for condition in rr.INVERTIBLE:
                r = rr.run_one(rule, condition, "random", 0.0, 0)
                self.assertTrue(r["truth_in_class"], f"rule={rule} condition={condition}")


class TestInvertibilityPreservesClassSize(unittest.TestCase):
    def test_class_size_equal_under_invertible_maps(self):
        for rule in SAMPLE_RULES:
            for ic in rr.ICS:
                raw = rr.run_one(rule, "raw", ic, 0.0, 0)
                for condition in rr.INVERTIBLE:
                    r = rr.run_one(rule, condition, ic, 0.0, 0)
                    self.assertEqual(r["class_size"], raw["class_size"], f"rule={rule} ic={ic} condition={condition}")
                    self.assertEqual(r["contradictions"], 0)

    def test_lossy_encoding_produces_contradictions_somewhere(self):
        hits = sum(1 for rule in SAMPLE_RULES if rr.run_one(rule, "block_or2", "random", 0.0, 0)["contradictions"] > 0)
        self.assertGreater(hits, 0)


class TestCommittedSubgrid(unittest.TestCase):
    def test_ci_subgrid_reproduces_committed_results(self):
        path = os.path.join(_EXP, "results", "ci_subgrid.json")
        with open(path, encoding="utf-8") as handle:
            committed = json.load(handle)
        recomputed = json.loads(json.dumps(rr.aggregate(**rr.CI_SUBGRID)))
        self.assertEqual(recomputed, committed)


if __name__ == "__main__":
    unittest.main()
