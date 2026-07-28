"""Regression guards for the exact Witness Principle baseline."""

import importlib.util
import os
import sys
import unittest

_MODULE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "lab",
    "benchmarks",
    "witness-generation",
    "witness_benchmark.py",
)


def _load():
    spec = importlib.util.spec_from_file_location("witness_benchmark", _MODULE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


wb = _load()


class TestClassWitnessFrontier(unittest.TestCase):
    def test_exact_frontier_headline(self):
        points = wb.exact_frontier(width=8, max_cost=4)
        self.assertEqual(
            [point.best.worst_case_remaining for point in points],
            [128, 16, 8, 2, 1],
        )
        self.assertEqual(
            [point.best.neighborhoods_seen for point in points],
            [1, 4, 5, 7, 8],
        )

    def test_cost_four_query_identifies_every_rule(self):
        score = wb.best_query_at_cost(width=8, cost=4)
        self.assertEqual(score.row, (0, 0, 0, 1, 0, 1, 1, 1))
        self.assertEqual(score.worst_case_remaining, 1)
        self.assertEqual(len(wb.query_partition(range(256), score.row)), 256)

    def test_equal_cost_baseline_is_not_smuggled_compute(self):
        points = wb.exact_frontier(width=8, max_cost=4)
        self.assertEqual([point.query_count for point in points], [1, 8, 28, 56, 70])
        self.assertAlmostEqual(points[2].mean_worst_case_remaining, 80 / 7)
        self.assertAlmostEqual(points[3].mean_worst_case_remaining, 40 / 7)
        self.assertAlmostEqual(points[4].mean_worst_case_remaining, 40 / 7)


class TestPairwiseWitnesses(unittest.TestCase):
    def test_deepest_pair_requires_three_prepared_bits(self):
        # Rules 0 and 128 differ only on neighborhood 111.
        self.assertIsNone(wb.separating_witness(0, 128, width=8, max_cost=2))
        row = wb.separating_witness(0, 128, width=8, max_cost=3)
        self.assertIsNotNone(row)
        self.assertEqual(sum(row), 3)
        self.assertNotEqual(wb.step(0, row), wb.step(128, row))

    def test_pairwise_cost_distribution(self):
        counts = wb.pairwise_witness_costs(width=8)
        self.assertEqual(
            dict(counts),
            {0: 16384, 1: 14336, 2: 1792, 3: 128},
        )
        self.assertEqual(sum(counts.values()), 256 * 255 // 2)


if __name__ == "__main__":
    unittest.main()
