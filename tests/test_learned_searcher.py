"""Offline guards for the pre-registered learned-searcher protocol. No network."""

import importlib.util
import os
import sys
import unittest

_MODULE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "lab",
    "benchmarks",
    "learned-searcher",
    "learned_searcher.py",
)


def _load():
    spec = importlib.util.spec_from_file_location("learned_searcher", _MODULE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


ls = _load()


class TestProtocolIsFrozen(unittest.TestCase):
    def test_instance_set_is_deterministic(self):
        a, b = ls.build_instances(0), ls.build_instances(0)
        self.assertEqual(a, b)
        counts = {}
        for inst in a:
            counts[inst["task"]] = counts.get(inst["task"], 0) + 1
        self.assertEqual(counts, {"T1": 40, "T2": 40, "T3": 20})

    def test_traps_differ_only_on_coordinate_111(self):
        traps = [
            i for i in ls.build_instances(0)
            if i["task"] == "T2" and i["trap"]
        ]
        self.assertEqual(len(traps), 6)
        for inst in traps:
            self.assertEqual(inst["a"] ^ inst["b"], 1 << 7)
            self.assertEqual(inst["budget"], 3)


class TestExactScoring(unittest.TestCase):
    def test_candidate_aware_row_beats_coverage_on_the_trap(self):
        aware = (0, 0, 0, 0, 0, 1, 1, 1)
        coverage = (0, 0, 0, 0, 1, 0, 1, 1)
        self.assertNotEqual(
            ls.step(ls.full_table(0), aware), ls.step(ls.full_table(128), aware)
        )
        self.assertEqual(
            ls.step(ls.full_table(0), coverage),
            ls.step(ls.full_table(128), coverage),
        )

    def test_pair_min_cost_matches_the_analytic_layers(self):
        for b, expected in ((1, 0), (2, 1), (8, 2), (128, 3)):
            self.assertEqual(ls.pair_min_cost(0, b), expected)

    def test_min_identifying_cost_for_the_deep_pair(self):
        self.assertEqual(ls.min_identifying_cost([0, 128]), 3)

    def test_t1_scoring_uses_wolfram_digit_order(self):
        inst = {"task": "T1", "rule": 110, "evidence": ls.evidence(110, (0,) * 8)}
        # TABLE line written t111..t000: rule 110 = 0 1 1 0 1 1 1 0.
        bits = (0, 1, 1, 0, 1, 1, 1, 0)
        result = ls.score(inst, bits)
        self.assertTrue(result["consistent"])
        self.assertTrue(result["truth"])


class TestParser(unittest.TestCase):
    def test_last_final_line_wins_and_kind_is_enforced(self):
        text = "thinking...\nROW: 1 1 1 1 1 1 1 1\nno wait\nROW: 0 0 0 0 0 1 1 1"
        self.assertEqual(
            ls.parse_answer(text, "ROW"), (0, 0, 0, 0, 0, 1, 1, 1)
        )
        self.assertIsNone(ls.parse_answer(text, "TABLE"))

    def test_malformed_answers_fail_closed(self):
        for text in ("ROW: 0 1", "ROW: two ones please", "", "TABLE 01010101"):
            self.assertIsNone(ls.parse_answer(text, "ROW"))


if __name__ == "__main__":
    unittest.main()
