"""Guards for Experiment A (persistence and search narrowing).

Three things are pinned: the ``none`` condition reproduces the referee
benchmark's loop exactly (same referee interface), the held-out == ceiling
identity holds in every condition for the full family (the memory is
target-independent), and the declared CI subgrid reproduces the committed
``results/ci_subgrid.json`` exactly.
"""

import importlib.util
import json
import os
import sys
import unittest

_HERE = os.path.dirname(__file__)
_EXP = os.path.join(_HERE, "..", "lab", "experiments", "persistence_narrowing")
_MODULE = os.path.join(_EXP, "persistence_narrowing.py")


def _load():
    spec = importlib.util.spec_from_file_location("persistence_narrowing_test", _MODULE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


pn = _load()
rb = pn.rb


class TestRefereeInterface(unittest.TestCase):
    def test_none_condition_reproduces_the_referee_benchmark(self):
        for family in ("full", "affine"):
            memory = pn.build_memory(family, 0)
            for rule in (0, 30, 90, 110, 255):
                for row in (0, 1):
                    ours = pn.run_loop(rule, 0, family=family, condition="none", memory=memory, row_index=row)
                    theirs = rb.run_loop(rule, 0, family=family, budget=pn.BUDGET, row_index=row)
                    self.assertEqual(
                        (ours.observed_passed, ours.observed_total, ours.heldout_correct, ours.tests_final),
                        (theirs.observed_passed, theirs.observed_total, theirs.heldout_correct, theirs.tests_final),
                        f"loop diverges from the referee benchmark: family={family} rule={rule} row={row}",
                    )

    def test_memory_is_deterministic_and_target_independent(self):
        for family in ("full", "affine"):
            a = pn.build_memory(family, 0)
            b = pn.build_memory(family, 0)
            self.assertEqual(a, b)
            self.assertEqual(len(a), pn.MEMORY_WORLDS)
            self.assertTrue(all(len(m) == (8 if family == "full" else 4) for m in a))


class TestHeldoutEqualsCeilingInEveryCondition(unittest.TestCase):
    def test_identity_holds_for_the_full_family(self):
        memory = pn.build_memory("full", 0)
        for condition in pn.CONDITIONS:
            for row in (0, 1):
                block = pn.row_block("full", condition, 0, row, memory)
                self.assertTrue(all(r.observed == 1 for r in block), f"non-saturated run: {condition} row={row}")
                heldout_total = sum(r.heldout_correct for r in block)
                tests_total = sum(r.tests_final for r in block)
                self.assertEqual(
                    2 * heldout_total,
                    tests_total + 256 * pn.COORDS,
                    f"identity violated under condition={condition} row={row}: some draw sees the hidden rule",
                )


class TestCommittedSubgrid(unittest.TestCase):
    def test_ci_subgrid_reproduces_committed_results(self):
        path = os.path.join(_EXP, "results", "ci_subgrid.json")
        with open(path, encoding="utf-8") as handle:
            committed = json.load(handle)
        recomputed = json.loads(json.dumps(pn.aggregate(**pn.CI_SUBGRID)))
        self.assertEqual(recomputed, committed)


if __name__ == "__main__":
    unittest.main()
