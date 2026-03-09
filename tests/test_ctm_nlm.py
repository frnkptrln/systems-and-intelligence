"""
test_ctm_nlm.py

Smoke tests for the CTM Neuron-Level Models (NLM) building block.

These tests are intentionally lightweight: they should not fail the repo on
machines without optional ML dependencies installed.
"""

import os
import sys
import unittest


def _try_import_torch():
    try:
        import torch  # noqa: F401
        return True
    except Exception:
        return False


@unittest.skipUnless(_try_import_torch(), "Optional dependency 'torch' not installed")
class TestCTMNLM(unittest.TestCase):
    def setUp(self):
        # Allow importing the CTM mini-package from the repo root.
        repo_root = os.path.join(os.path.dirname(__file__), "..")
        ctm_root = os.path.join(repo_root, "simulation-models", "continuous-thought-machines")
        sys.path.append(ctm_root)

    def test_nlm_shapes(self):
        import torch

        from ctm.nlm import NLMActivation, NLMConfig

        m = NLMActivation(NLMConfig(num_neurons=7, history_len=4, hidden_dim=8))
        x = torch.randn(3, 7)
        y, h = m(x)
        self.assertEqual(tuple(y.shape), (3, 7))
        self.assertEqual(tuple(h.shape), (3, 7, 4))

    def test_nlm_external_history(self):
        import torch

        from ctm.nlm import NLMActivation, NLMConfig

        cfg = NLMConfig(num_neurons=5, history_len=2, hidden_dim=8)
        m = NLMActivation(cfg)

        x = torch.randn(2, 5)
        hist = torch.zeros(2, 5, 2)
        y1, h1 = m(x, history=hist, update_internal_history=False)
        self.assertEqual(tuple(y1.shape), (2, 5))
        self.assertEqual(tuple(h1.shape), (2, 5, 2))


if __name__ == "__main__":
    unittest.main()

