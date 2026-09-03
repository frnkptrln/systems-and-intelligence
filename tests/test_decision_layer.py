"""Guards for the decision-layer experiment (Candidate C1's receipt).

Pinned: the P1 table for K1|D1|3, the identification control on the full
family (P2), the Case A/B regret radii and the risk-inversion pair (P3), the
coverage criterion against the enumeration on the CI cube classes (P4), the
negative control K2 (P5), agreement of the exact expected-remaining score with
the benchmark's own float score, and the committed ``results/ci_subgrid.json``.
"""

import importlib.util
import json
import os
import sys
import unittest
from fractions import Fraction

_HERE = os.path.dirname(__file__)
_EXP = os.path.join(_HERE, "..", "lab", "experiments", "decision_layer")
_MODULE = os.path.join(_EXP, "decision_layer.py")


def _load():
    spec = importlib.util.spec_from_file_location("decision_layer_test", _MODULE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


dl = _load()
wb = dl.wb


def _cell(name, card_name, cost):
    spec = dl.NAMED_CLASSES[name]
    return dl.cell(spec["rules"], dl.build_card(card_name, spec["rules"], spec["d"]), cost)


class TestP1Table(unittest.TestCase):
    def test_k1_d1_cost3_is_a_full_reversal_with_the_declared_numbers(self):
        c = _cell("K1", "D1", 3)
        self.assertTrue(c["strict_size"] and c["strict_ig"] and c["full_reversal"])
        self.assertEqual((c["q_size"], c["q_ig"], c["q_voi"]), ("00001011", "00001011", "00000111"))
        self.assertEqual(c["voi_max"], Fraction(5))
        self.assertEqual((c["voi_size_arm"], c["voi_ig_arm"]), (Fraction(0), Fraction(0)))
        size_row = c["measures"]["00001011"]
        voi_row = c["measures"]["00000111"]
        self.assertEqual((size_row["wc"], size_row["expected_remaining"], size_row["ig_bits"]), (2, Fraction(2), 2.0))
        self.assertEqual(size_row["blocks"], [(2, 10)] * 4)
        self.assertEqual(size_row["expected_regret"], Fraction(10))
        self.assertEqual((voi_row["wc"], voi_row["expected_remaining"], voi_row["ig_bits"]), (4, Fraction(4), 1.0))
        self.assertEqual(voi_row["blocks"], [(4, 0)] * 2)
        self.assertEqual(voi_row["expected_regret"], Fraction(0))

    def test_k4_d1_cost3_and_k1_d2_cost3(self):
        c = _cell("K4", "D1", 3)
        self.assertTrue(c["strict_size"] and c["strict_ig"] and c["full_reversal"])
        self.assertEqual(c["voi_max"], Fraction(5))
        d2 = _cell("K1", "D2", 3)
        self.assertTrue(d2["strict_size"] and d2["strict_ig"])
        self.assertEqual(d2["voi_max"], Fraction(4))


class TestControls(unittest.TestCase):
    def test_identification_card_on_the_full_family_is_never_strict(self):
        for cost, exposed in zip(range(4), (1, 4, 5, 7)):
            c = _cell("K4", "U", cost)
            self.assertFalse(c["strict_size"] or c["strict_ig"], cost)
            self.assertEqual(c["voi_max"], Fraction(2**exposed - 1, 256), cost)

    def test_case_a_and_case_b_regret_radii(self):
        k4 = dl.NAMED_CLASSES["K4"]["rules"]
        k3 = dl.NAMED_CLASSES["K3"]["rules"]
        self.assertEqual(dl.regret_radius(k4, dl.build_card("D3", k4, 7)), 0)
        self.assertEqual(dl.regret_radius(k3, dl.build_card("D1", k3, 7)), 10)

    def test_risk_inversion_pair_in_k1_d1(self):
        spec = dl.NAMED_CLASSES["K1"]
        card = dl.build_card("D1", spec["rules"], spec["d"])
        blocks = set()
        for cost in dl.COSTS:
            blocks.update(tuple(p) for p in dl.cell(spec["rules"], card, cost)["blocks_all_rows"])
        pairs = dl.risk_inversion_pairs(sorted(blocks))
        self.assertIn([[2, 10], [4, 0]], pairs)

    def test_negative_control_k2_is_never_strict(self):
        for card_name in dl.CARD_NAMES:
            for cost in dl.COSTS:
                c = _cell("K2", card_name, cost)
                self.assertFalse(c["strict_size"] or c["strict_ig"], (card_name, cost))


class TestAgreementWithTheBenchmark(unittest.TestCase):
    def test_exact_expected_remaining_equals_the_benchmark_score(self):
        for name in ("K1", "K4"):
            rules = dl.NAMED_CLASSES[name]["rules"]
            for row in wb.rows_at_cost(dl.WIDTH, 3):
                blocks = wb.query_partition(rules, row)
                exact = dl.expected_remaining(rules, blocks)
                self.assertEqual(float(exact), wb.score_query(rules, row).expected_remaining, (name, row))

    def test_coverage_criterion_equals_enumeration_on_ci_cubes(self):
        for name in ("K1", "K2"):
            spec = dl.NAMED_CLASSES[name]
            card = dl.build_card("D1", spec["rules"], spec["d"])
            for cost in dl.COSTS:
                enumerated = dl.cell(spec["rules"], card, cost)["strict_size"]
                self.assertEqual(dl.coverage_criterion(spec["coords"], spec["d"], cost), enumerated, (name, cost))


class TestCommittedSubgrid(unittest.TestCase):
    def test_ci_subgrid_reproduces_committed_results(self):
        path = os.path.join(_EXP, "results", "ci_subgrid.json")
        with open(path, encoding="utf-8") as handle:
            committed = json.load(handle)
        recomputed = json.loads(json.dumps(dl.to_jsonable(dl.aggregate(**dl.CI_SUBGRID))))
        self.assertEqual(recomputed, committed)


if __name__ == "__main__":
    unittest.main()
