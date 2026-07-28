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


class TestCoverageDuality(unittest.TestCase):
    def test_full_family_partition_is_determined_by_coverage(self):
        for cost in range(9):
            for row in wb.rows_at_cost(8, cost):
                score = wb.score_query(range(256), row)
                residual = wb.full_family_residual(row)
                self.assertEqual(score.worst_case_remaining, residual)
                self.assertEqual(score.expected_remaining, residual)

    def test_universal_width_eight_queries_are_cost_four_de_bruijn_rows(self):
        rows = wb.universal_witnesses(width=8)
        self.assertEqual(len(rows), 16)
        self.assertEqual({sum(row) for row in rows}, {4})
        self.assertTrue(
            all(wb.neighborhoods(row) == tuple(range(8)) for row in rows)
        )

    def test_query_space_quotients_to_coverage_classes(self):
        classes = wb.coverage_classes(width=8)
        self.assertEqual(sum(len(rows) for rows in classes.values()), 256)
        self.assertEqual(len(classes), 21)

        partitions = set()
        for rows in classes.values():
            class_partitions = {
                frozenset(
                    frozenset(block)
                    for block in wb.query_partition(range(256), row)
                )
                for row in rows
            }
            self.assertEqual(len(class_partitions), 1)
            partitions.update(class_partitions)

        self.assertEqual(len(partitions), 21)


class TestPairwiseWitnesses(unittest.TestCase):
    def test_difference_coordinate_oracle_by_cost_layer(self):
        for rule_b, expected_cost in ((1, 0), (2, 1), (8, 2), (128, 3)):
            self.assertEqual(
                wb.analytic_pair_witness_cost(0, rule_b),
                expected_cost,
            )

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
        self.assertEqual(counts, wb.analytic_pairwise_witness_costs())
        self.assertEqual(sum(counts.values()), 256 * 255 // 2)


class TestRestrictedCandidateClasses(unittest.TestCase):
    def test_cli_candidate_declaration(self):
        self.assertEqual(wb.parse_candidates("0, 64,128, 192"), (0, 64, 128, 192))
        for invalid in ("", "0,0", "-1,0", "0,256", "not-a-rule"):
            with self.assertRaises(Exception):
                wb.parse_candidates(invalid)

    def test_restricted_frontier_is_candidate_aware(self):
        points = wb.restricted_frontier((0, 128), width=8, max_cost=3)
        self.assertEqual(
            [point.best.worst_case_remaining for point in points],
            [2, 2, 2, 1],
        )
        self.assertEqual(points[3].best.row, (0, 0, 0, 0, 0, 1, 1, 1))
        self.assertEqual(points[3].best.neighborhoods_seen, 6)

    def test_distinguishing_query_beats_every_coverage_maximizer(self):
        comparison = wb.compare_candidate_and_coverage(
            (0, 128),
            width=8,
            max_cost=3,
        )[3]
        self.assertEqual(comparison.candidate_aware.worst_case_remaining, 1)
        self.assertEqual(comparison.maximal_neighborhoods, 7)
        self.assertEqual(comparison.maximal_coverage.worst_case_remaining, 2)
        self.assertEqual(comparison.maximal_coverage_query_count, 16)

    def test_exact_full_family_pair_gap_at_cost_three(self):
        gap = wb.pairwise_objective_gap(width=8, cost=3)
        self.assertEqual(gap.pair_count, 32640)
        self.assertEqual(gap.candidate_aware_separable, 32640)
        self.assertEqual(gap.maximal_coverage_separable, 32512)
        self.assertEqual(gap.divergence_count, 128)


if __name__ == "__main__":
    unittest.main()
