import unittest

from lab.experiments.active_measurement.causal_identification import (
    best_cost_adjusted_intervention,
    information_gain_bits,
    observationally_equivalent,
    posterior_probability_a,
)


class ActiveIdentificationTests(unittest.TestCase):
    def test_observational_equivalence(self) -> None:
        self.assertTrue(observationally_equivalent())

    def test_information_gain_is_symmetric_in_intervention_sign(self) -> None:
        self.assertAlmostEqual(information_gain_bits(3.0), information_gain_bits(-3.0), places=9)

    def test_reference_information_values(self) -> None:
        expected = {
            0.0: 0.0396841323,
            1.0: 0.1400454032,
            2.0: 0.3799611638,
            3.0: 0.6338353789,
        }
        for x, target in expected.items():
            self.assertAlmostEqual(information_gain_bits(x), target, places=8)

    def test_cost_adjusted_optimum(self) -> None:
        x, utility = best_cost_adjusted_intervention(cost_lambda=0.05, x_min=0.0, x_max=3.0)
        self.assertAlmostEqual(x, 2.5504, places=3)
        self.assertAlmostEqual(utility, 0.199799, places=5)

    def test_posterior_examples(self) -> None:
        self.assertAlmostEqual(posterior_probability_a(3.0, 3.0), 0.9306407359, places=8)
        self.assertAlmostEqual(posterior_probability_a(3.0, 0.0), 0.0154674916, places=8)
        self.assertAlmostEqual(posterior_probability_a(3.0, -1.0), 0.0006087911, places=8)


if __name__ == "__main__":
    unittest.main()
