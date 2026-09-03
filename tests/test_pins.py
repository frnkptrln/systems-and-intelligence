"""Pins added 2026-09-03.

Four frozen facts that no earlier test guarded:

- the conjugation maps of Experiment B partition the 256 elementary rules into the
  88 classes known for reflection and complementation;
- the v1.2 enumeration-cost figures quoted in the inverse-reconstruction README
  (rule 90 within 36 candidates, rule 30 within 771, rule 110 within 116,232,
  size-10 targets within about 4.2 million) follow from ``family_search``;
- the committed full-grid result files of Experiments A and B carry the parameters
  their READMEs declare and the headline numbers their READMEs report;
- the corridor paper's text above its post-v1.0 TODO section is byte-frozen.
"""

import hashlib
import importlib.util
import json
import os
import re
import sys
import unittest
from collections import Counter

_HERE = os.path.dirname(__file__)
_REPO = os.path.abspath(os.path.join(_HERE, ".."))


def _load(rel_path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, os.path.join(_REPO, rel_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _read(rel_path: str) -> str:
    with open(os.path.join(_REPO, rel_path), encoding="utf-8") as handle:
        return handle.read()


class TestConjugationOrbits(unittest.TestCase):
    def test_complement_and_reflection_give_88_classes(self):
        rr = _load("lab/experiments/representation_reconstruction/representation_reconstruction.py", "pins_rr")
        seen = set()
        orbits = 0
        for rule in range(256):
            if rule in seen:
                continue
            orbits += 1
            c = rr.complement_rule(rule)
            r = rr.reflect_rule(rule)
            seen.update({rule, c, r, rr.reflect_rule(c)})
            self.assertEqual(rr.complement_rule(r), rr.reflect_rule(c), rule)
        self.assertEqual(orbits, 88)
        self.assertEqual(len(seen), 256)


class TestFamilySearchCosts(unittest.TestCase):
    def test_enumeration_cost_figures_quoted_in_the_readme(self):
        fs = _load("lab/benchmarks/inverse-reconstruction/family_search.py", "pins_fs")
        best = fs.minimal_sizes()
        stream = fs.stream_sizes()
        cumulative = [sum(stream[1 : n + 1]) for n in range(len(stream))]
        self.assertEqual(best[90], 3)
        self.assertEqual(best[30], 5)
        self.assertEqual(best[110], 8)
        self.assertEqual(cumulative[3], 36)
        self.assertEqual(cumulative[5], 771)
        self.assertEqual(cumulative[8], 116_232)
        self.assertEqual(cumulative[10], 4_193_562)
        self.assertEqual(
            sorted(Counter(best.values()).items()),
            [(1, 3), (2, 3), (3, 10), (4, 22), (5, 21), (6, 81), (7, 43), (8, 43), (9, 18), (10, 12)],
        )
        readme = _read("lab/benchmarks/inverse-reconstruction/README.md")
        for figure in ("≤36", "≤771", "≤116,232", "≤4.2M"):
            self.assertIn(figure, readme)


class TestExperimentResultFiles(unittest.TestCase):
    def test_persistence_narrowing_full_grid(self):
        pn = _load("lab/experiments/persistence_narrowing/persistence_narrowing.py", "pins_pn")
        data = json.loads(_read("lab/experiments/persistence_narrowing/results/persistence_narrowing.json"))
        self.assertEqual(
            data["parameters"],
            {"seeds": 2, "rows": 8, "rules": 256, "budget": pn.BUDGET, "p_recall": str(pn.P_RECALL),
             "memory_worlds": pn.MEMORY_WORLDS, "width": pn.WIDTH},
        )
        readme = _read("lab/experiments/persistence_narrowing/README.md")
        for condition in pn.CONDITIONS:
            full = data["families"]["full"]["conditions"][condition]
            self.assertTrue(full["heldout_equals_ceiling_identity"], condition)
            self.assertEqual(full["runs"], 4096)
            self.assertAlmostEqual(full["mean_heldout"], full["mean_ceiling"], places=12)
            self.assertIn(f"{full['mean_heldout']:.4f}", readme)
            affine = data["families"]["affine"]["conditions"][condition]
            self.assertEqual(affine["runs"], 4096)
            self.assertIn(f"{affine['mean_observed']:.4f}", readme)
            self.assertIn(f"{affine['mean_heldout']:.4f}", readme)

    def test_representation_reconstruction_full_grid(self):
        rr = _load("lab/experiments/representation_reconstruction/representation_reconstruction.py", "pins_rr2")
        data = json.loads(_read("lab/experiments/representation_reconstruction/results/representation_reconstruction.json"))
        self.assertEqual(data["parameters"]["seeds"], 2)
        self.assertEqual(data["parameters"]["rules"], 256)
        self.assertEqual(list(data["parameters"]["conditions"]), list(rr.CONDITIONS))
        for name in rr.INVERTIBLE:
            check = data["invertibility_check"][name]
            self.assertTrue(check["exact"], name)
            self.assertEqual(check["class_size_equal_raw"], check["runs"], name)
            self.assertEqual(check["runs"], 3072, name)
        shift = data["description_size_shift"]
        self.assertEqual(
            {k: shift[k]["rules_with_changed_size"] for k in ("complement", "reflect", "both")},
            {"complement": 98, "reflect": 0, "both": 98},
        )
        self.assertEqual(shift["complement"]["max_abs_size_shift"], 1)
        readme = _read("lab/experiments/representation_reconstruction/README.md")
        self.assertIn("3,072 of 3,072", readme)
        self.assertRegex(readme, r"\|\s*complement\s*\|\s*98\s*\|\s*49\s*\|\s*49\s*\|\s*1\s*\|")
        self.assertRegex(readme, r"\|\s*reflect\s*\|\s*0\s*\|\s*0\s*\|\s*0\s*\|\s*0\s*\|")


class TestCorridorPaperFrozen(unittest.TestCase):
    """v1.0 is the submission version. The text above the TODO section is frozen.

    If the maintainer issues a new version, update ``FROZEN_SHA256`` in the same
    change that revises the paper and records the version in its changelog.
    """

    FROZEN_SHA256 = "ccbeabd8f0c7d431ebc1294b52dd553d7ea5f35538200c1d28d343102ade4904"
    MARKER = "## TODO (post-v1.0)"

    def test_text_above_the_todo_section_is_unchanged(self):
        text = _read("papers/viable-corridor.md")
        self.assertIn(self.MARKER, text)
        frozen = text[: text.index(self.MARKER)]
        self.assertRegex(frozen, r"v1\.0")
        digest = hashlib.sha256(frozen.encode("utf-8")).hexdigest()
        self.assertEqual(
            digest,
            self.FROZEN_SHA256,
            "papers/viable-corridor.md changed above its TODO section; v1.0 is frozen. "
            "A new paper version updates FROZEN_SHA256 in this test in the same change.",
        )


if __name__ == "__main__":
    unittest.main()
