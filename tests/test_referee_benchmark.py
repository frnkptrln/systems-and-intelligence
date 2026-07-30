"""Regression guards for the recursive-workbench referee benchmark headline."""

import importlib.util
import os
import sys
import unittest
from fractions import Fraction

_MODULE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "lab",
    "benchmarks",
    "recursive-workbench",
    "referee_benchmark.py",
)


def _load():
    spec = importlib.util.spec_from_file_location("referee_benchmark", _MODULE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


rb = _load()
SEEDS = 4
AGG = {arm: rb.aggregate(arm, SEEDS) for arm in rb.ARMS}


class TestSelfRevisionSaturates(unittest.TestCase):
    def test_frozen_referee_reaches_all_green(self):
        for arm in ("full-frozen", "full-frozen-10x"):
            self.assertEqual(AGG[arm].all_pass_runs, 1024)
            self.assertEqual(AGG[arm].observed_sum, Fraction(1024))

    def test_ten_times_the_budget_stays_at_the_same_ceiling(self):
        self.assertEqual(AGG["full-frozen"].heldout_correct_total, 6977)
        self.assertEqual(AGG["full-frozen-10x"].heldout_correct_total, 6984)

    def test_long_budget_extends_the_same_proposal_stream(self):
        short = rb.run_loop(
            110, 0, arm="full-frozen", keep_trace=True,
            **rb.ARMS["full-frozen"],
        )
        long = rb.run_loop(
            110, 0, arm="full-frozen-10x", keep_trace=True,
            **rb.ARMS["full-frozen-10x"],
        )
        short_slots = [e["slot"] for e in short.trace if e["event"] == "proposal"]
        long_slots = [e["slot"] for e in long.trace if e["event"] == "proposal"]
        self.assertEqual(short_slots, long_slots[: len(short_slots)])

    def test_evidence_is_arm_independent(self):
        # The world rng is decoupled from the loop rng: every frozen arm and
        # the misspecified arm face the same evidence per (rule, seed).
        self.assertEqual(AGG["full-frozen"].tests_final_total, 5764)
        self.assertEqual(AGG["full-frozen-10x"].tests_final_total, 5764)
        self.assertEqual(AGG["affine-frozen"].tests_final_total, 5764)

    def test_heldout_sits_at_the_evidence_ceiling(self):
        agg = AGG["full-frozen"]
        gap = abs(agg.mean_heldout - agg.mean_ceiling)
        self.assertLess(gap, Fraction(1, 100))


class TestRefereeQueriesRaiseTheCeiling(unittest.TestCase):
    def test_queries_add_evidence_and_heldout_follows(self):
        agg = AGG["full-witness"]
        self.assertEqual(agg.tests_final_total, 7519)
        self.assertEqual(agg.heldout_correct_total, 7869)
        self.assertEqual(agg.all_pass_runs, 1024)
        self.assertEqual(agg.observed_sum, Fraction(1024))
        # The gain over the frozen arm is evidence-driven: held-out tracks the
        # raised ceiling within the same tolerance as the frozen arm.
        self.assertLess(
            abs(agg.mean_heldout - agg.mean_ceiling), Fraction(1, 100)
        )
        self.assertGreater(
            agg.heldout_correct_total, AGG["full-frozen"].heldout_correct_total
        )


class TestEvaluatorCaptureInflatesOnlyTheReport(unittest.TestCase):
    def test_frozen_referee_reports_misspecification_honestly(self):
        agg = AGG["affine-frozen"]
        self.assertEqual(agg.all_pass_runs, 166)
        self.assertEqual(agg.observed_sum, Fraction(684679, 840))
        self.assertEqual(agg.heldout_correct_total, 5752)
        self.assertEqual(agg.deletions_total, 0)

    def test_capture_goes_green_without_heldout_gain(self):
        agg = AGG["affine-capture"]
        self.assertEqual(agg.all_pass_runs, 989)
        self.assertEqual(agg.observed_sum, Fraction(40521, 40))
        self.assertEqual(agg.heldout_correct_total, 5734)
        self.assertEqual(agg.deletions_total, 1179)
        self.assertEqual(agg.tests_final_total, 5764 - 1179)

    def test_frozen_and_capture_share_the_proposal_stream(self):
        frozen = rb.run_loop(
            110, 0, arm="affine-frozen", keep_trace=True,
            **rb.ARMS["affine-frozen"],
        )
        capture = rb.run_loop(
            110, 0, arm="affine-capture", keep_trace=True,
            **rb.ARMS["affine-capture"],
        )
        frozen_slots = [
            e["slot"] for e in frozen.trace if e["event"] == "proposal"
        ]
        capture_slots = [
            e["slot"] for e in capture.trace if e["event"] == "proposal"
        ]
        self.assertEqual(frozen_slots, capture_slots)

    def test_honesty_gap_widens_under_capture(self):
        frozen = AGG["affine-frozen"]
        capture = AGG["affine-capture"]
        gap_frozen = frozen.mean_observed - frozen.mean_heldout
        gap_capture = capture.mean_observed - capture.mean_heldout
        self.assertGreater(gap_capture, 2 * gap_frozen)


class TestTraceIsComplete(unittest.TestCase):
    def test_trace_records_every_proposal_and_evaluator_edit(self):
        result = rb.run_loop(
            110, 0, arm="affine-capture", keep_trace=True,
            **rb.ARMS["affine-capture"],
        )
        proposals = [e for e in result.trace if e["event"] == "proposal"]
        edits = [e for e in result.trace if e["event"] == "evaluator-edit"]
        self.assertEqual(len(proposals), rb.ARMS["affine-capture"]["budget"])
        self.assertEqual(len(edits), result.deletions)


if __name__ == "__main__":
    unittest.main()
