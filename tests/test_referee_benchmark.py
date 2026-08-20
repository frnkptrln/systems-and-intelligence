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
# CI subgrid: 4 seeds x 4 rows = 16 evidence rows, each crossed with all 256
# rules. The published grid (README) is 4 x 256 = 1024 rows via the same code;
# the held-out == ceiling identity is guarded separately in
# tests/test_referee_invariant.py and holds on any rule-complete subgrid.
SEEDS = 4
ROWS = 4
AGG = {arm: rb.aggregate(arm, SEEDS, ROWS) for arm in rb.ARMS}


def _proposal_slots(rule, seed, arm):
    result = rb.run_loop(rule, seed, arm=arm, keep_trace=True, **rb.ARMS[arm])
    return [e["slot"] for e in result.trace if e["event"] == "proposal"]


class TestSelfRevisionSaturates(unittest.TestCase):
    def test_frozen_referee_reaches_all_green(self):
        for arm in ("full-frozen", "full-frozen-10x"):
            self.assertEqual(AGG[arm].all_pass_runs, 4096)
            self.assertEqual(AGG[arm].observed_sum, Fraction(4096))

    def test_ten_times_the_budget_stays_at_the_exact_same_ceiling(self):
        self.assertEqual(AGG["full-frozen"].heldout_correct_total, 28544)
        self.assertEqual(AGG["full-frozen-10x"].heldout_correct_total, 28544)
        self.assertEqual(AGG["full-frozen"].mean_heldout, Fraction(223, 256))
        self.assertEqual(AGG["full-frozen"].mean_heldout, AGG["full-frozen"].mean_ceiling)
        self.assertEqual(AGG["full-frozen-10x"].mean_heldout, AGG["full-frozen-10x"].mean_ceiling)

    def test_long_budget_extends_the_same_proposal_stream(self):
        short = _proposal_slots(110, 0, "full-frozen")
        long = _proposal_slots(110, 0, "full-frozen-10x")
        self.assertEqual(short, long[: len(short)])

    def test_random_streams_do_not_depend_on_hidden_rule(self):
        # The public experimental coordinates determine the random streams.
        # Therefore all 256 hidden rules see the same evidence row and proposal
        # slots for a fixed seed/family; only the target outputs differ.
        for seed in range(SEEDS):
            world_rows = []
            proposal_streams = []
            for rule in (0, 1, 30, 110, 255):
                world_rng, _ = rb.experiment_streams(seed, "full")
                world_rows.append(tuple(world_rng.getrandbits(1) for _ in range(rb.WIDTH)))
                proposal_streams.append(_proposal_slots(rule, seed, "full-frozen"))
            self.assertTrue(all(row == world_rows[0] for row in world_rows))
            self.assertTrue(all(slots == proposal_streams[0] for slots in proposal_streams))

    def test_evidence_mask_is_rule_independent(self):
        for seed in range(SEEDS):
            masks = []
            for rule in range(256):
                world_rng, _ = rb.experiment_streams(seed, "full")
                row = tuple(world_rng.getrandbits(1) for _ in range(rb.WIDTH))
                masks.append(tuple(rb.evidence_tests(rule, row)))
            self.assertTrue(all(mask == masks[0] for mask in masks))

    def test_evidence_is_arm_independent(self):
        self.assertEqual(AGG["full-frozen"].tests_final_total, 24320)
        self.assertEqual(AGG["full-frozen-10x"].tests_final_total, 24320)
        self.assertEqual(AGG["affine-frozen"].tests_final_total, 24320)


class TestRefereeQueriesRaiseTheCeiling(unittest.TestCase):
    def test_queries_add_evidence_and_heldout_follows_exactly(self):
        agg = AGG["full-witness"]
        self.assertEqual(agg.tests_final_total, 30720)
        self.assertEqual(agg.heldout_correct_total, 31744)
        self.assertEqual(agg.all_pass_runs, 4096)
        self.assertEqual(agg.observed_sum, Fraction(4096))
        self.assertEqual(agg.mean_heldout, Fraction(31, 32))
        self.assertEqual(agg.mean_heldout, agg.mean_ceiling)
        self.assertGreater(
            agg.heldout_correct_total, AGG["full-frozen"].heldout_correct_total
        )


class TestEvaluatorCaptureInflatesOnlyTheReport(unittest.TestCase):
    def test_frozen_referee_reports_misspecification_honestly(self):
        agg = AGG["affine-frozen"]
        self.assertEqual(agg.all_pass_runs, 590)
        self.assertEqual(agg.observed_sum, Fraction(16173, 5))
        self.assertEqual(agg.heldout_correct_total, 23286)
        self.assertEqual(agg.deletions_total, 0)

    def test_capture_goes_green_without_heldout_gain(self):
        agg = AGG["affine-capture"]
        self.assertEqual(agg.all_pass_runs, 3931)
        self.assertEqual(agg.observed_sum, Fraction(169639, 42))
        self.assertEqual(agg.heldout_correct_total, 23148)
        self.assertEqual(agg.deletions_total, 5074)
        self.assertEqual(agg.tests_final_total, 24320 - 5074)

    def test_frozen_and_capture_share_the_proposal_stream(self):
        frozen = _proposal_slots(110, 0, "affine-frozen")
        capture = _proposal_slots(110, 0, "affine-capture")
        self.assertEqual(frozen, capture)

    def test_honesty_gap_widens_under_capture(self):
        frozen = AGG["affine-frozen"]
        capture = AGG["affine-capture"]
        gap_frozen = frozen.mean_observed - frozen.mean_heldout
        gap_capture = capture.mean_observed - capture.mean_heldout
        self.assertGreater(gap_capture, 2 * gap_frozen)


class TestRunLoopDrawsCarryNoTargetInformation(unittest.TestCase):
    """Guard the information boundary through run_loop itself.

    These checks observe only the public trace and result of run_loop, never
    the stream helper, so they fail — rather than error — against any
    implementation whose world or proposal randomness sees the hidden rule.
    """

    PROBE_RULES = (0, 3, 45, 110, 254)

    def test_proposal_slots_are_identical_across_hidden_rules(self):
        for seed in range(SEEDS):
            for row in (0, 1):
                for arm in ("full-frozen", "affine-frozen"):
                    streams = {
                        tuple(
                            e["slot"]
                            for e in rb.run_loop(
                                rule, seed, arm=arm, row_index=row,
                                keep_trace=True, **rb.ARMS[arm],
                            ).trace
                            if e["event"] == "proposal"
                        )
                        for rule in self.PROBE_RULES
                    }
                    self.assertEqual(len(streams), 1)

    def test_evidence_mask_size_is_identical_across_hidden_rules(self):
        for seed in range(SEEDS):
            sizes = {
                rb.run_loop(
                    rule, seed, arm="full-frozen", **rb.ARMS["full-frozen"]
                ).tests_final
                for rule in self.PROBE_RULES
            }
            self.assertEqual(len(sizes), 1)


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
