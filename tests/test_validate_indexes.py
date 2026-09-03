"""Tests for lab/tools/validate_indexes.py.

Each rule is exercised on a small temporary repository, and the real
repository must pass with no finding.
"""

import importlib.util
import os
import sys
import unittest
from pathlib import Path
import tempfile

_HERE = os.path.dirname(__file__)
_REPO = os.path.abspath(os.path.join(_HERE, ".."))
_MODULE = os.path.join(_REPO, "lab", "tools", "validate_indexes.py")


def _load():
    spec = importlib.util.spec_from_file_location("validate_indexes_test", _MODULE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


vi = _load()


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _messages(findings):
    return [str(f) for f in findings]


class TestFlatIndexes(unittest.TestCase):
    def test_unindexed_idea_log_and_story_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "ideas/README.md", "- [A](2026-01-01-a.md)\n")
            _write(root, "ideas/2026-01-01-a.md", "# A\n")
            _write(root, "ideas/2026-01-02-b.md", "# B\n")
            _write(root, "logs/README.md", "1. [One](001_one.md)\n")
            _write(root, "logs/001_one.md", "# One\n")
            _write(root, "logs/002_two.md", "# Two\n")
            _write(root, "fiction/README.md", "- [S](01_s.md)\n")
            _write(root, "fiction/01_s.md", "# S\n")
            _write(root, "fiction/02_t.md", "# T\n")
            messages = _messages(vi.collect_findings(root))
        self.assertTrue(any(m.startswith("ideas/2026-01-02-b.md") for m in messages), messages)
        self.assertTrue(any(m.startswith("logs/002_two.md") for m in messages), messages)
        self.assertTrue(any(m.startswith("fiction/02_t.md") for m in messages), messages)
        self.assertFalse(any("2026-01-01-a.md" in m or "001_one" in m or "01_s" in m for m in messages), messages)

    def test_anchored_link_counts_as_indexed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "ideas/README.md", "- [A](2026-01-01-a.md#section)\n")
            _write(root, "ideas/2026-01-01-a.md", "# A\n## Section\n")
            self.assertEqual(vi.collect_findings(root), [])


class TestTheoryIndex(unittest.TestCase):
    def test_subdirectory_readme_can_index_its_siblings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "theory/README.md", "- [Core](core/a.md)\n- [Framework](framework/README.md)\n")
            _write(root, "theory/core/a.md", "# A\n")
            _write(root, "theory/framework/README.md", "- [Sub](sub.md)\n")
            _write(root, "theory/framework/sub.md", "# Sub\n")
            _write(root, "theory/core/orphan.md", "# Orphan\n")
            messages = _messages(vi.collect_findings(root))
        self.assertEqual(len(messages), 1, messages)
        self.assertTrue(messages[0].startswith("theory/core/orphan.md"), messages)


class TestDirectoryIndexes(unittest.TestCase):
    def test_simulation_directory_must_be_named_in_the_map(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "theory/README.md", "- [Map](core/simulation-theory-map.md)\n")
            _write(root, "theory/core/simulation-theory-map.md", "`group/mapped/` is here.\n")
            _write(root, "simulation-models/group/mapped/README.md", "# M\n")
            _write(root, "simulation-models/group/unmapped/README.md", "# U\n")
            messages = _messages(vi.collect_findings(root))
        self.assertEqual(len(messages), 1, messages)
        self.assertTrue(messages[0].startswith("simulation-models/group/unmapped/"), messages)

    def test_lab_benchmarks_and_experiments_must_be_named_in_the_lab_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "lab/README.md", "[b](benchmarks/known/README.md) and experiments/known/ too.\n")
            _write(root, "lab/benchmarks/known/README.md", "# K\n")
            _write(root, "lab/benchmarks/missing/README.md", "# M\n")
            _write(root, "lab/experiments/known/README.md", "# K\n")
            _write(root, "lab/experiments/missing/README.md", "# M\n")
            _write(root, "lab/experiments/__pycache__/README.md", "# cache\n")
            messages = _messages(vi.collect_findings(root))
        self.assertEqual(len(messages), 2, messages)
        self.assertTrue(any(m.startswith("lab/benchmarks/missing/") for m in messages), messages)
        self.assertTrue(any(m.startswith("lab/experiments/missing/") for m in messages), messages)


class TestLinkLabels(unittest.TestCase):
    def test_path_label_must_match_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "theory/README.md", "- [Core](core/a.md)\n- [Note](core/b.md)\n")
            _write(root, "theory/core/a.md", "# A\n")
            _write(
                root,
                "theory/core/b.md",
                "See [`theory/a.md`](a.md) and [`theory/core/a.md`](a.md) and [`a.md`](a.md#top) "
                "and [`theory/`](../README.md) and [`missing.py`](https://example.org/x).\n",
            )
            messages = _messages(vi.collect_findings(root))
        self.assertEqual(len(messages), 1, messages)
        self.assertIn("link text `theory/a.md` does not match its target theory/core/a.md", messages[0])


class TestRealRepository(unittest.TestCase):
    def test_repository_indexes_are_complete_and_labels_match(self):
        findings = vi.collect_findings(Path(_REPO))
        self.assertEqual(_messages(findings), [])


if __name__ == "__main__":
    unittest.main()
