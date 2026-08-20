"""Standing CI invariant: held-out == evidence ceiling, exactly, per row-ensemble.

This is a target-conditioning detector, not just a correctness check. For any
evidence row and proposal stream chosen independently of the hidden rule, the
256-rule enumeration makes every unexposed rule coordinate a free bit, so the
ensemble held-out total equals the exact ceiling identity

    2 * heldout_total == tests_final_total + 256 * COORDS

per (seed, row) block, for every full-family arm. The v0.1 RNG leak (the hidden
rule seeded the world and loop streams) broke exactly this identity — 6977 vs
the identity's 6912 over the then-current grid — and the deviation was small
enough to pass for sampling noise. Any future path by which target information
reaches the draws fails this test as an exact inequality, on any rule-complete
subgrid, independent of the pinned aggregate numbers in
tests/test_referee_benchmark.py.
"""

import importlib.util
import os
import sys
import unittest

_MODULE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "lab",
    "benchmarks",
    "recursive-workbench",
    "referee_benchmark.py",
)


def _load():
    spec = importlib.util.spec_from_file_location("referee_invariant_rb", _MODULE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


rb = _load()

FULL_ARMS = ("full-frozen", "full-frozen-10x", "full-witness")
SEEDS = (0, 1)
ROWS = (0, 1)


class TestHeldoutEqualsCeilingIdentity(unittest.TestCase):
    def test_identity_holds_exactly_per_row_ensemble(self):
        for arm in FULL_ARMS:
            for seed in SEEDS:
                for row in ROWS:
                    block = rb.row_runs(arm, seed, row)
                    # Precondition, checked separately so a violation below is
                    # attributable: the identity's seen-coordinate part needs
                    # every run to end consistent with its visible tests.
                    self.assertTrue(
                        all(r.observed == 1 for r in block),
                        f"non-saturated run: arm={arm} seed={seed} row={row} — "
                        "identity precondition failed, not a conditioning "
                        "signal",
                    )
                    heldout_total = sum(r.heldout_correct for r in block)
                    tests_final_total = sum(r.tests_final for r in block)
                    self.assertEqual(
                        2 * heldout_total,
                        tests_final_total + 256 * rb.COORDS,
                        f"identity violated: arm={arm} seed={seed} row={row} — "
                        "the unexposed coordinates are not free bits over the "
                        "enumeration; some draw sees the hidden rule",
                    )

    def test_block_is_the_full_rule_enumeration(self):
        block = rb.row_runs("full-frozen", 0, 0)
        self.assertEqual(len(block), 256)


if __name__ == "__main__":
    unittest.main()
