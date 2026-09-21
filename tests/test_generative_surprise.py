"""Regression guard for the Generative Surprise metric.

The historical definition (Emergence Manifesto v1.3, Claim 6; glossary
§Generative Surprise) is the product

    prediction_error_observer × trajectory_consistency_agent

with an unnormalized distance as the first factor and a cosine in [-1, 1] as
the second. Three defects were recorded on 2026-09-21:

1. The product is not a conjunction. Because the error term is unbounded, one
   large deviation times a small consistency outranks a moderate deviation
   with a moderate consistency; "both high" is not enforced.
2. The ranking is scale-dependent. The error term carries the scale of the
   embedding space while the consistency term does not, so two trajectories
   embedded at different scales cannot be ranked.
3. The null-vector convention was undocumented. A missing prediction (the zero
   vector) *raised* the score, and the repository's two existing cosine
   helpers disagree on what a null vector means.

Each test below states a property the corrected metric must have and that the
historical product lacks. The suite was committed red against the historical
product and turned green by the corrected definition; the historical product
is retained as ``generative_surprise_legacy`` so the defects stay
reproducible.
"""

import unittest

import numpy as np

from lab.metrics.generative_surprise import generative_surprise


def straight_line(n: int = 6, dim: int = 4, step: float = 1.0) -> list[np.ndarray]:
    """A trajectory whose consecutive change vectors all point the same way."""
    direction = np.zeros(dim)
    direction[0] = 1.0
    return [np.ones(dim) + t * step * direction for t in range(n)]


def orthogonal_matrix(dim: int, seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    q, _ = np.linalg.qr(rng.standard_normal((dim, dim)))
    return q


class TestConjunction(unittest.TestCase):
    """GS must be bounded by both factors: a low factor caps the score."""

    def test_score_never_exceeds_either_factor(self):
        observed = straight_line()
        predicted = [-10.0 * o for o in observed]  # anti-aligned, ten times larger
        result = generative_surprise(observed, predicted, representations=observed)
        self.assertGreater(result["n_steps"], 0)
        for score, error, consistency in zip(
            result["per_step"], result["error"], result["consistency"]
        ):
            self.assertLessEqual(score, min(error, consistency) + 1e-12)
            self.assertGreaterEqual(score, 0.0)

    def test_factors_and_score_live_in_the_unit_interval(self):
        observed = straight_line()
        predicted = [-10.0 * o for o in observed]
        result = generative_surprise(observed, predicted, representations=observed)
        for value in result["error"] + result["consistency"] + result["per_step"]:
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)


class TestInvariance(unittest.TestCase):
    """The ranking may not depend on the scale or orientation of the embedding."""

    def test_uniform_rescaling_leaves_every_per_step_value_unchanged(self):
        observed = straight_line()
        predicted = [o + np.array([0.0, 0.5, 0.0, 0.0]) for o in observed]
        base = generative_surprise(observed, predicted, representations=observed)
        scaled = generative_surprise(
            [100.0 * o for o in observed],
            [100.0 * p for p in predicted],
            representations=[100.0 * o for o in observed],
        )
        np.testing.assert_allclose(scaled["per_step"], base["per_step"])
        self.assertAlmostEqual(scaled["mean"], base["mean"])

    def test_orthogonal_change_of_basis_leaves_every_per_step_value_unchanged(self):
        observed = straight_line()
        predicted = [o + np.array([0.0, 0.5, 0.0, 0.0]) for o in observed]
        q = orthogonal_matrix(4)
        base = generative_surprise(observed, predicted, representations=observed)
        rotated = generative_surprise(
            [q @ o for o in observed],
            [q @ p for p in predicted],
            representations=[q @ o for o in observed],
        )
        np.testing.assert_allclose(rotated["per_step"], base["per_step"])

    def test_cross_trajectory_ranking_survives_a_change_of_scale(self):
        # Trajectory A: coherent, moderately surprising. Trajectory B: a mirror
        # (prediction equals output), so B must rank below A at every scale.
        a_obs = straight_line()
        a_pred = [o + np.array([0.0, 0.5, 0.0, 0.0]) for o in a_obs]
        b_obs = straight_line()
        b_pred = [o.copy() for o in b_obs]
        a = generative_surprise(a_obs, a_pred, representations=a_obs)["mean"]
        for scale in (1e-3, 1.0, 1e3):
            b = generative_surprise(
                [scale * o for o in b_obs],
                [scale * p for p in b_pred],
                representations=[scale * o for o in b_obs],
            )["mean"]
            self.assertGreater(a, b, msg=f"ranking flipped at scale {scale}")


class TestNullVectorConvention(unittest.TestCase):
    """A null vector is undefined data; it must be reported and may never raise GS."""

    def test_missing_prediction_yields_zero_surprise_and_is_counted(self):
        observed = straight_line()
        predicted = [o + np.array([0.0, 0.5, 0.0, 0.0]) for o in observed]
        predicted[3] = np.zeros(4)
        result = generative_surprise(observed, predicted, representations=observed)
        index = result["step_indices"].index(3)
        self.assertEqual(result["error"][index], 0.0)
        self.assertEqual(result["per_step"][index], 0.0)
        self.assertEqual(result["undefined_error_terms"], 1)

    def test_stalled_trajectory_yields_zero_consistency_and_is_counted(self):
        observed = straight_line()
        observed[3] = observed[2].copy()  # no movement: a null change vector
        predicted = [o + np.array([0.0, 0.5, 0.0, 0.0]) for o in observed]
        result = generative_surprise(observed, predicted, representations=observed)
        touched = [i for i, t in enumerate(result["step_indices"]) if t in (3, 4)]
        for index in touched:
            self.assertEqual(result["consistency"][index], 0.0)
            self.assertEqual(result["per_step"][index], 0.0)
        self.assertEqual(result["undefined_consistency_terms"], 2)


class TestDocumentedScale(unittest.TestCase):
    """The endpoints of both factors are stated in the module and hold exactly."""

    def test_mirror_has_zero_surprise(self):
        observed = straight_line()
        result = generative_surprise(observed, [o.copy() for o in observed])
        self.assertTrue(all(e == 0.0 for e in result["error"]))
        self.assertEqual(result["mean"], 0.0)

    def test_anti_prediction_has_unit_error(self):
        observed = straight_line()
        result = generative_surprise(observed, [-o for o in observed])
        self.assertTrue(all(abs(e - 1.0) < 1e-12 for e in result["error"]))

    def test_straight_line_has_unit_consistency_and_reversal_has_zero(self):
        observed = straight_line()
        predicted = [-o for o in observed]
        result = generative_surprise(observed, predicted, representations=observed)
        self.assertTrue(all(abs(c - 1.0) < 1e-12 for c in result["consistency"]))
        zigzag = [np.array([1.0, 0.0]), np.array([2.0, 0.0]), np.array([1.0, 0.0])]
        result = generative_surprise(zigzag, [-v for v in zigzag], representations=zigzag)
        self.assertEqual(result["consistency"], [0.0])


if __name__ == "__main__":
    unittest.main()
