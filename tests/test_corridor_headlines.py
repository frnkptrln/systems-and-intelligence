"""
test_corridor_headlines.py

Regression guard for the Appendix C–D headline numbers of
papers/viable-corridor.md (the Viable Corridor paper).

The paper quotes specific measured results of its two companion simulations —
`simulation-models/alignment-and-veto/teo-civilization/teo_simulation.py`
(Appendix C, the TEO ODE) and `…/agent-ecology/agent_budget_sim.py`
(Appendix D, the stochastic ABM): the C.1 necessity table (in-corridor
margins 0.346 / 0.946; monopoly at gamma=0; dephasing to r=0.31 below K_c;
substrate veto Omega/S_max = 27.49 with H -> 0 vs. the health-coupled
self-limit 0.863 with H = 0.137), the threshold values gamma_c ~ 0.49/0.51
and K_c ~ 1.60, the C.4 separability grid (0 mismatches between the
decoupled prediction and coupled viability), the C.4 rescue quartet at
delta = 2.0, and the D.1/D.2 failure frequencies (hard budgets hold
collapse at ~0 across capability, soft ones rise to 1; hard-only leaves a
residual monopoly frequency ~0.26, only the joint architecture clears
both). Nothing so far checked that the code still produces those numbers.
This suite does, in the pattern of test_benchmark_headlines.py: same seeds,
same dials, tolerance bands that guard the *claim*, not the third decimal.

Reduced, representative configuration (CI budget)
-------------------------------------------------
The full Appendix protocol (both scripts with --save, ~820 ODE
integrations + ~8,400 ABM trajectories) is ~10 minutes of compute — too
long for CI. This suite pins a reduced configuration (~25 s); the manifest
below records the full protocol. Reductions, and why they are
representative:

* Separability: 16 of the 64 grid cells verified on 2026-08-20 (the full
  8x8 grid had 0 mismatches in both the analytic and the axiswise variant
  of the decoupled prediction). The 16 cells are two values per axis on
  each side of the analytic thresholds, *including* the boundary-adjacent
  grid points (gamma 0.429/0.643 around gamma_c = 0.495; K 1.143/1.714
  around K_c = 1.596), so all four quadrants and the hardest cells are
  covered.
* gamma_c: bracketing (final max_x above x_crit at gamma = 0.40, below at
  gamma = 0.60) instead of the 31-point sweep; the quoted crossing ~0.51
  lies inside the bracket, and the closed form 0.495 is checked exactly.
* Capability crossings (C.4): a 9-point delta sweep over [0.6, 1.4] — the
  crossing region — instead of the figure's 30-point sweep over
  [0.05, 3.0].
* ABM frequencies: 50 seeds (seed0 = 0) instead of 200. On 2026-08-20
  every guarded frequency reproduced its 200-seed value to within 0.02
  (the residual-monopoly headline was 0.260 at both 50 and 200 seeds).

Full-run manifest (measured 2026-08-20)
---------------------------------------
    cd simulation-models/alignment-and-veto/teo-civilization
    python teo_simulation.py --save        # all Appendix-C figures; 355 s wall
    cd ../agent-ecology
    python agent_budget_sim.py --save      # Appendix-D figure; 114 s wall

Seeds: the TEO script is deterministic given Params.seed = 7 (the omega
draw; `run()` draws initial conditions with seed+1); the ABM given
`frequencies(seed0=0)`, i.e. per-run seeds 0..199. Both scripts use
np.random.default_rng throughout; no global RNG state.

Known prose drift (marked 2026-08-20, deliberately NOT adopted here):
Appendix C.4 quotes the second boundary crossing (substrate demand
eta*phibar_0 = D_max) "near delta ~ 1.4"; the current code and the
*committed* Figure C4 (lab/tools/teo_p8_capability.png, unchanged since
the figure was generated) both put it at ~1.05. The band below pins what
the code produces and guards the claim that survives (two crossings,
concentration first); the prose number awaits an explicit decision. Do not
widen or move that band to make it match the prose.
"""

import importlib.util
import os
import sys
import unittest
from dataclasses import replace

import numpy as np

_ROOT = os.path.join(os.path.dirname(__file__), "..")
_TEO = os.path.join(_ROOT, "simulation-models", "alignment-and-veto",
                    "teo-civilization", "teo_simulation.py")
_ABM = os.path.join(_ROOT, "simulation-models", "alignment-and-veto",
                    "agent-ecology", "agent_budget_sim.py")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # dataclasses require registration (Py >= 3.12)
    spec.loader.exec_module(mod)
    return mod


teo = _load("teo_simulation", _TEO)
abm = _load("agent_budget_sim", _ABM)

GAMMA_C = 0.495   # x_crit(1-x_crit)*delta/(x_crit-x_reg), Eq. (9)
K_C = teo.kc_gaussian(1.0)


class TestAppendixC1Necessity(unittest.TestCase):
    """The four-row necessity table of C.1 plus the substrate contrast."""

    def test_in_corridor_margins_and_simplex(self):
        """Row (a): max_x 0.346, r 0.946, Omega 0, simplex drift ~2e-15."""
        res = teo.run(teo.Params(), "(a) in-corridor")
        rep = teo.viability_report(res)
        self.assertTrue(rep["viable"])
        self.assertTrue(0.30 < rep["max_x_final"] < 0.40)
        self.assertTrue(0.90 < rep["r_final"] < 0.99)
        self.assertEqual(rep["Omega_final"], 0.0)
        self.assertLess(res.simplex_err, 1e-12)

    def test_gamma_zero_monopoly(self):
        """Row (b), Lemma 1: brake off -> dominant share converges to 1."""
        rep = teo.viability_report(teo.run(replace(teo.Params(), gamma=0.0)))
        self.assertGreater(rep["max_x_final"], 0.99)
        self.assertFalse(rep["V1_pluralism"])

    def test_subcritical_coupling_dephases(self):
        """Row (c), Lemma 2: K=0.8 < K_c from a coherent IC -> r = 0.310.

        The finite-N floor is r ~ 1/sqrt(N) ~ 0.14 (C.5), so the guarded
        claim is 'well below r_min=0.5', not 'r -> 0'.
        """
        rep = teo.viability_report(teo.run(replace(teo.Params(), K=0.8)))
        self.assertTrue(0.10 < rep["r_final"] < 0.45)
        # the resource axis stays healthy — the V2 failure is isolated
        self.assertTrue(0.30 < rep["max_x_final"] < 0.40)

    def test_substrate_veto_canonical(self):
        """Row (d), Lemma 3: Omega/S_max = 27.49, H -> 0, dynamics frozen."""
        rep = teo.viability_report(
            teo.run(replace(teo.Params(), D_max=0.3, eta=2.0)))
        self.assertTrue(20.0 < rep["Omega_over_Smax"] < 35.0)
        self.assertEqual(rep["H_final"], 0.0)
        # frozen early: the resource race never develops, coherence is caught
        self.assertLess(rep["max_x_final"], 0.10)
        self.assertGreater(rep["r_final"], 0.90)

    def test_substrate_self_regulating_variant(self):
        """Contrast run: health-coupled dissipation self-limits at 0.863,
        H plateaus at 0.137 — the veto never binds (S2.5, S6.1)."""
        rep = teo.viability_report(
            teo.run(replace(teo.Params(), D_max=0.3, eta=2.0,
                            entropy_couples_to_H=True)))
        self.assertTrue(0.80 < rep["Omega_over_Smax"] < 0.92)
        self.assertTrue(0.08 < rep["H_final"] < 0.20)


class TestThresholds(unittest.TestCase):
    def test_kc_value(self):
        """K_c = 2*sigma*sqrt(2/pi) ~ 1.60 for the unit Gaussian density."""
        self.assertAlmostEqual(K_C, 2.0 * np.sqrt(2.0 / np.pi), places=12)
        self.assertTrue(1.55 < K_C < 1.65)

    def test_gamma_c_closed_form_and_bracket(self):
        """Eq. (9) gives 0.495; the empirical crossing (~0.51) lies in
        [0.40, 0.60]: max_x is above x_crit at gamma=0.40, below at 0.60."""
        p = teo.Params()
        gc = p.x_crit * (1 - p.x_crit) * p.delta / (p.x_crit - p.x_reg)
        self.assertAlmostEqual(gc, GAMMA_C, places=12)
        above = teo.run(replace(p, gamma=0.40)).max_x[-1]
        below = teo.run(replace(p, gamma=0.60)).max_x[-1]
        self.assertGreater(above, p.x_crit)
        self.assertLess(below, p.x_crit)


class TestSeparability(unittest.TestCase):
    def test_decoupled_prediction_matches_coupled_viability(self):
        """C.4: 0 mismatches between (gamma > gamma_c AND K > K_c) and
        coupled V1-and-V2 viability. Reduced 4x4 subgrid of the verified
        8x8 grid — all four quadrants incl. the boundary-adjacent cells."""
        p = teo.Params()
        gammas = np.linspace(0.0, 1.5, 8)[[0, 2, 3, 7]]   # 0, .429, .643, 1.5
        Ks = np.linspace(0.0, 4.0, 8)[[0, 2, 3, 7]]       # 0, 1.143, 1.714, 4
        for g in gammas:
            for K in Ks:
                rep = teo.viability_report(
                    teo.run(replace(p, gamma=float(g), K=float(K))))
                coupled = rep["V1_pluralism"] and rep["V2_coherence"]
                predicted = (g > GAMMA_C) and (K > K_C)
                self.assertEqual(
                    coupled, predicted,
                    f"separability mismatch at gamma={g:.3f}, K={K:.3f}: "
                    f"decoupled predicts {predicted}, coupled gives {coupled}")


class TestAppendixC4Capability(unittest.TestCase):
    def test_rescue_quartet_at_high_capability(self):
        """delta=2.0: baseline fails V1+V3; +gamma only fixes V1 but not V3;
        +D only fixes V3 but leaves max_x ~ 0.62; only both restore V."""
        p = replace(teo.Params(), delta=2.0)
        baseline = teo.viability_report(teo.run(p))
        self.assertFalse(baseline["V1_pluralism"])
        self.assertFalse(baseline["V3b_substrate"])

        gamma_only = teo.viability_report(teo.run(replace(p, gamma=6.0)))
        self.assertTrue(gamma_only["V1_pluralism"])
        self.assertFalse(gamma_only["V3b_substrate"])

        d_only = teo.viability_report(teo.run(replace(p, D_max=3.0)))
        self.assertTrue(d_only["V3b_substrate"])
        self.assertFalse(d_only["V1_pluralism"])
        self.assertTrue(0.55 < d_only["max_x_final"] < 0.70)

        both = teo.viability_report(
            teo.run(replace(p, gamma=6.0, D_max=3.0)))
        self.assertTrue(both["viable"])

    def test_capability_two_boundary_crossings_in_order(self):
        """One capability axis, two crossings: max_x crosses x_crit first
        (~0.89), then demand crosses the operating D_max=1.5 (~1.05).

        NOTE (2026-08-20): the C.4 prose quotes the second crossing "near
        delta ~ 1.4"; code and the committed Figure C4 both give ~1.05.
        See the module docstring — do not move this band to fit the prose.
        """
        p = teo.Params()
        D_op = 1.5
        deltas = np.linspace(0.6, 1.4, 9)
        mx, dem = [], []
        for d in deltas:
            res = teo.run(replace(p, delta=float(d), D_max=8.0))
            mx.append(res.max_x[-1])
            dem.append(p.eta * float(np.dot(res.x[:, -1],
                                            res.p.base_fitness)))
        mx, dem = np.array(mx), np.array(dem)

        i1 = int(np.argmax(mx > p.x_crit))
        self.assertGreater(i1, 0, "max_x already above x_crit at delta=0.6")
        d1 = float(np.interp(p.x_crit, mx[i1 - 1:i1 + 1],
                             deltas[i1 - 1:i1 + 1]))
        i2 = int(np.argmax(dem > D_op))
        self.assertGreater(i2, 0, "demand already above D_op at delta=0.6")
        d2 = float(np.interp(D_op, dem[i2 - 1:i2 + 1],
                             deltas[i2 - 1:i2 + 1]))

        self.assertTrue(0.80 < d1 < 0.98, f"concentration crossing {d1:.3f}")
        self.assertTrue(0.95 < d2 < 1.15, f"substrate crossing {d2:.3f}")
        self.assertLess(d1, d2, "concentration boundary must come first")


class TestAppendixDAgentEcology(unittest.TestCase):
    N_SEEDS = 50

    def test_p7_hard_holds_soft_collapses(self):
        """D.1: hard budgets hold P(collapse) at ~0 at every capability;
        soft (routable) budgets rise from near zero to 1 past C = D/eta."""
        base = abm.Params()
        for cap in (0.6, 1.8):
            hard = abm.frequencies(
                replace(base, capability=cap, budget="hard", gamma=1.5),
                self.N_SEEDS)
            self.assertLessEqual(hard["P_collapse"], 0.02,
                                 f"hard budget collapsed at C={cap}")
        soft_lo = abm.frequencies(
            replace(base, capability=0.6, budget="soft", gamma=1.5),
            self.N_SEEDS)
        self.assertLessEqual(soft_lo["P_collapse"], 0.30)   # "near zero"
        soft_hi = abm.frequencies(
            replace(base, capability=1.8, budget="soft", gamma=1.5),
            self.N_SEEDS)
        self.assertGreaterEqual(soft_hi["P_collapse"], 0.95)  # "rises to 1"

    def test_p8_only_joint_architecture_clears_both(self):
        """D.2 at C=1.8: soft leaves collapse at 1 regardless of gamma;
        hard-only leaves residual monopoly ~0.26; joint clears both."""
        base = replace(abm.Params(), capability=1.8)
        for g in (0.3, 1.5):
            f = abm.frequencies(replace(base, budget="soft", gamma=g),
                                self.N_SEEDS)
            self.assertGreaterEqual(f["P_collapse"], 0.95)

        hard_weak = abm.frequencies(replace(base, budget="hard", gamma=0.3),
                                    self.N_SEEDS)
        self.assertLessEqual(hard_weak["P_collapse"], 0.02)
        self.assertTrue(0.10 < hard_weak["P_monopoly"] < 0.45,
                        f"residual monopoly {hard_weak['P_monopoly']:.3f} "
                        "left the ~0.26 band")

        joint = abm.frequencies(replace(base, budget="hard", gamma=1.5),
                                self.N_SEEDS)
        self.assertLessEqual(joint["P_monopoly"], 0.05)
        self.assertLessEqual(joint["P_collapse"], 0.02)


if __name__ == "__main__":
    unittest.main()
