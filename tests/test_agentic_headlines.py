"""
test_agentic_headlines.py

Regression guard for the identity-suite numbers quoted in prose.

lab/AGENTIC_README.md reports very specific results for Exp5-7 — "veto
violations 0.74 / 0.59 / 0.03", "role stability 0.00 / 0.30 / 0.69", "|d| ~ 4"
against "|d| ~ 1.95", "kurtosis 4.04 -> 2.42", "~40% of stimulus alignment" —
and Claim 3 in meta/repository-meta/core-claims.md rests on them. The
inverse-reconstruction benchmark has had a guard of this kind since
test_benchmark_headlines.py; the identity branch did not, which left the arm
carrying the softest evidence with the weakest protection against silent drift.

This suite closes that asymmetry. It re-runs each experiment at its documented
seed count and asserts the published numbers inside tolerance bands. A failure
here means the prose must be re-measured, not that the band should be widened.

Bands follow the same rule as the benchmark guard: they protect the *claim*, not
the third decimal. Designed constants (the IP floor, the Delta-Koharenz
blindness) are checked exactly; measured rates and effect sizes get brackets
around the quoted value; and the orderings that carry the argument — passive
beats prepared, the commit property survives both adversaries — are asserted as
orderings rather than as magnitudes.
"""

import importlib.util
import os
import unittest

import numpy as np

_EXPERIMENTS = os.path.join(os.path.dirname(__file__), "..", "lab", "experiments")


def _load(name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(_EXPERIMENTS, f"{name}.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


exp5 = _load("exp5_availability_dissociation")
exp6 = _load("exp6_binding_observables")
exp7 = _load("exp7_adversarial_arpeggio")

ARCHITECTURES = ("private", "broadcast", "chord")
KURTOSIS = "O3 increment kurtosis (passive)"
RETEST = "O5 retest divergence (prepared)"
OMEGA = "O1 Δ-Kohärenz Ω (passive)"


def mean(values):
    return float(np.asarray(values, dtype=float).mean())


def abs_d(module, a, b):
    return abs(module.cohens_d(list(a), list(b)))


class TestExp5Dissociation(unittest.TestCase):
    """Exp5: identical world and perturbations; only the binding differs."""

    @classmethod
    def setUpClass(cls):
        cls.res = exp5.run_suite(n_seeds=10)

    def test_identity_persistence_is_the_designed_floor(self):
        """Quoted: IP 0.00 / 0.20 / 1.00 — designed, not discovered (P1)."""
        observed = [mean(self.res[a]["ip"]) for a in ARCHITECTURES]
        for got, want in zip(observed, (0.00, 0.20, 1.00)):
            self.assertAlmostEqual(got, want, places=2)

    def test_violation_rates_carry_the_dissociation(self):
        """Quoted: veto violations 0.74 / 0.59 / 0.03 over 10 seeds."""
        observed = [mean(self.res[a]["violation_rate"]) for a in ARCHITECTURES]
        for got, want in zip(observed, (0.74, 0.59, 0.03)):
            self.assertAlmostEqual(got, want, delta=0.05,
                                   msg=f"violation rates moved: {observed}")
        # The dissociation is the ordering, not the three magnitudes; and the
        # chord's near-zero leak is what separates it from a fluent mimic.
        self.assertGreater(observed[0], observed[1])
        self.assertGreater(observed[1], observed[2])
        self.assertLess(observed[2], 0.10)

    def test_role_stability_orders_the_three_bindings(self):
        """Quoted: role stability 0.00 / 0.30 / 0.69 over 10 seeds."""
        observed = [mean(self.res[a]["role_stability"]) for a in ARCHITECTURES]
        for got, want in zip(observed, (0.00, 0.30, 0.69)):
            self.assertAlmostEqual(got, want, delta=0.05,
                                   msg=f"role stability moved: {observed}")
        self.assertLess(observed[0], observed[1])
        self.assertLess(observed[1], observed[2])

    def test_delta_koharenz_classifies_noise_on_every_seed(self):
        """Quoted: Δ-Kohärenz carries no binding signal at all (P3 failed).

        This is a recorded blind spot of the instrument, so it is checked
        exactly. If a binding ever stops classifying 'noise', the blindness has
        changed and the claim needs rewriting rather than relaxing.
        """
        for architecture in ARCHITECTURES:
            profiles = list(self.res[architecture]["profiles"])
            self.assertEqual(profiles, ["noise"] * 10, f"{architecture} moved")


class TestExp6Observables(unittest.TestCase):
    """Exp6: is binding structure readable passively, or only under probing?"""

    @classmethod
    def setUpClass(cls):
        cls.res = exp6.run_suite(n_seeds=10)

    def _separation(self, observable):
        return [
            abs_d(exp6, self.res["chord"][observable], self.res[arm][observable])
            for arm in ("broadcast", "arpeggio-random")
        ]

    def test_increment_kurtosis_separates_both_arpeggios(self):
        """Quoted: a per-step action-increment statistic separates both
        arpeggios from the chord at |d| ~ 4."""
        for separation in self._separation(KURTOSIS):
            self.assertTrue(3.0 < separation < 5.0,
                            f"kurtosis |d| {separation:.2f} left the ~4 band")

    def test_prepared_retest_separates_less(self):
        """Quoted: the prepared probe-retest query reaches |d| ~ 1.95."""
        for separation in self._separation(RETEST):
            self.assertTrue(1.4 < separation < 2.6,
                            f"retest |d| {separation:.2f} left the ~1.95 band")

    def test_passive_statistic_beats_the_prepared_query(self):
        """The finding itself: watching suffices where coverage is total.

        Asserted as an ordering because that is what the claim says; the
        magnitudes are guarded by the two tests above.
        """
        for passive, prepared in zip(self._separation(KURTOSIS),
                                     self._separation(RETEST)):
            self.assertGreater(passive, prepared)

    def test_delta_koharenz_is_blind_at_this_level(self):
        """Quoted: Δ-Kohärenz's exp5 blindness was a wrong-*level* failure."""
        for separation in self._separation(OMEGA):
            self.assertLess(separation, 0.8,
                            f"Ω suddenly separates at |d| {separation:.2f}")


class TestExp7AdversarialArpeggio(unittest.TestCase):
    """Exp7: can a hand-built binding fake the signature?"""

    @classmethod
    def setUpClass(cls):
        cls.res = exp7.run_suite(n_seeds=10)

    def _kurtosis_d(self, arm):
        return abs_d(exp7, self.res["chord"]["kurtosis"], self.res[arm]["kurtosis"])

    def _commit_d(self, arm):
        return abs_d(
            exp7, self.res["chord"]["violation_rate"], self.res[arm]["violation_rate"]
        )

    def test_blending_dents_the_kurtosis_signature(self):
        """Quoted: |d| 4.04 -> 2.42 for the blended adversary."""
        self.assertTrue(3.4 < self._kurtosis_d("broadcast") < 4.6)
        self.assertTrue(1.9 < self._kurtosis_d("blended") < 3.0)
        self.assertLess(self._kurtosis_d("blended"), self._kurtosis_d("broadcast"))

    def test_smoothing_barely_registers(self):
        """Quoted: |d| = 3.91, because excess kurtosis is scale-invariant."""
        self.assertTrue(3.3 < self._kurtosis_d("smoothed") < 4.5)

    def test_blended_leaks_more_than_the_naive_arpeggio(self):
        """Quoted: violations 0.74 (blended) versus 0.59 (naive arpeggio).

        To look glued you must actually pull toward the constraints; fractional
        pulls still leak.
        """
        blended = mean(self.res["blended"]["violation_rate"])
        naive = mean(self.res["broadcast"]["violation_rate"])
        self.assertAlmostEqual(blended, 0.74, delta=0.06)
        self.assertAlmostEqual(naive, 0.59, delta=0.06)
        self.assertGreater(blended, naive)

    def test_commit_property_is_the_unfooled_separator(self):
        """Quoted: the commit property under lure holds at |d| 3.0-4.1 against
        every adversary — the strongest and only separator neither one dents."""
        for arm in ("broadcast", "smoothed", "blended"):
            separation = self._commit_d(arm)
            self.assertTrue(2.6 < separation < 4.6,
                            f"{arm} commit |d| {separation:.2f} left the band")

    def test_chord_pays_about_forty_percent_of_stimulus_alignment(self):
        """Quoted: chord's measured cost for holding itself together."""
        chord = mean(self.res["chord"]["tracking"])
        naive = mean(self.res["broadcast"]["tracking"])
        cost = 1.0 - chord / naive
        self.assertTrue(0.30 < cost < 0.50, f"tracking cost {cost:.1%} left ~40%")


if __name__ == "__main__":
    unittest.main()
