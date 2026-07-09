"""
test_benchmark_headlines.py

Regression guard for the benchmark numbers quoted in prose.

The theory layer cites specific measured results of the inverse-reconstruction
benchmark — e.g. theory/core/the-generator-question.md: "near-exact with a
known family and clean data … ~27% error under angle noise, ~41% under partial
observability, ~800% when weights must be inferred from doubly-differenced
noisy positions … rule 90 single-seed: consistent-generator class size 8".
Nothing so far checked that the code still produces those numbers. This suite
does: it re-runs the exact headline settings (same seeds, same dials) and
asserts the results inside tolerance bands. If a benchmark change moves a
headline number outside its band, this test fails — the signal that the prose
must be re-measured, not silently left stale.

Bands are deliberately loose (they guard the *claim*, not the third decimal):
qualitative claims (near-exact, order-of-magnitude blowup, exact class count)
get tight or exact checks; noisy-regime means get wide brackets around the
quoted value.
"""

import importlib.util
import os
import unittest

import numpy as np

_BENCH = os.path.join(
    os.path.dirname(__file__), "..",
    "lab", "benchmarks", "inverse-reconstruction", "inverse_benchmark.py",
)


def _load_benchmark():
    spec = importlib.util.spec_from_file_location("inverse_benchmark", _BENCH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ib = _load_benchmark()
W_TRUE = np.array((0.8, 1.2, 2.0))


class TestKuramotoHeadlines(unittest.TestCase):
    def test_clean_recovery_is_near_exact(self):
        """Known family, no noise, full observability → 'cheap' direction."""
        th, om, K, dt = ib.kuramoto_forward(seed=0)
        K_hat, _, _ = ib.kuramoto_inverse(th, dt, noise=0.0, seed=0)
        self.assertLess(abs(K_hat - K) / K, 0.01)

    def test_angle_noise_headline(self):
        """Quoted: ~27% relative error on K at sigma=0.3 (mean of 6 seeds)."""
        errs = []
        for s in range(6):
            th, om, K, dt = ib.kuramoto_forward(seed=s)
            K_hat, _, _ = ib.kuramoto_inverse(th, dt, noise=0.3, seed=s)
            errs.append(abs(K_hat - K) / K)
        self.assertTrue(0.10 < float(np.mean(errs)) < 0.50,
                        f"mean err {np.mean(errs):.3f} left the ~27% band")

    def test_partial_observability_headline(self):
        """Quoted: ~41% error at observed_frac=0.15, sigma=0.03 (6 seeds)."""
        errs = []
        for s in range(6):
            th, om, K, dt = ib.kuramoto_forward(seed=s)
            K_hat, _, _ = ib.kuramoto_inverse(th, dt, noise=0.03,
                                              observed_frac=0.15, seed=s)
            errs.append(abs(K_hat - K) / K)
        self.assertTrue(0.20 < float(np.mean(errs)) < 0.70,
                        f"mean err {np.mean(errs):.3f} left the ~41% band")


class TestCAHeadlines(unittest.TestCase):
    def test_rule90_single_seed_equivalence_class(self):
        """Quoted: single-seed rule 90 trace → 5/8 neighborhoods, class size 8.

        This is the repository's flagship identifiability number (exact, not
        statistical): 3 unseen neighborhoods → 2^3 consistent generators.
        """
        grid = ib.ca_forward(rule=90, ic="single", seed=0)
        bits, seen, class_size = ib.ca_inverse(grid)
        self.assertEqual(int(seen.sum()), 5)
        self.assertEqual(class_size, 8)

    def test_clean_random_ic_recovery_is_exact(self):
        """Full coverage + no noise → rule bits recovered exactly."""
        for rule in (110, 30, 90):
            grid = ib.ca_forward(rule=rule, seed=0)
            bits, seen, _ = ib.ca_inverse(grid)
            self.assertEqual(ib.ca_bit_accuracy(rule, bits, seen), 1.0)


class TestBoidsHeadlines(unittest.TestCase):
    def test_clean_positions_recover_weights(self):
        """No noise: weights from double-differenced positions, error < 10%."""
        X, dt = ib.boids_forward(w=tuple(W_TRUE), seed=0)
        w_hat = ib.boids_inverse(X, dt, noise=0.0, seed=0)
        err = np.linalg.norm(w_hat - W_TRUE) / np.linalg.norm(W_TRUE)
        self.assertLess(err, 0.10)

    def test_position_noise_blowup_headline(self):
        """Quoted: ~800% error at sigma=0.03 — the double-differencing cost.

        The guarded claim is the order-of-magnitude blowup (>200%), not the
        exact figure.
        """
        errs = []
        for s in range(3):
            X, dt = ib.boids_forward(w=tuple(W_TRUE), seed=s)
            w_hat = ib.boids_inverse(X, dt, noise=0.03, seed=s)
            errs.append(float(np.linalg.norm(w_hat - W_TRUE)
                              / np.linalg.norm(W_TRUE)))
        self.assertGreater(float(np.mean(errs)), 2.0)


if __name__ == "__main__":
    unittest.main()
