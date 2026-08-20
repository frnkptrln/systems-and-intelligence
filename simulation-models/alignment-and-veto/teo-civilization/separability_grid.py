"""
separability_grid.py

Appendix C.4 separability experiment for papers/viable-corridor.md —
the canonical, full 64-cell run.

CLAIM UNDER TEST.  In the substrate-safe regime the three state axes of the
TEO system do not interact dynamically: across an 8x8 grid of (gamma, K)
cells — gamma in [0, 1.5], K in [0, 4], evenly spaced — the *decoupled*
prediction of viability matches *coupled* robust viability in every cell
(0 mismatches). Two forms of the decoupled prediction are checked:

  * analytic:  gamma > gamma_c  AND  K > K_c, with
               gamma_c = x_crit (1 - x_crit) delta / (x_crit - x_reg) = 0.495
               (Eq. (9) of the paper) and K_c = 2 sigma sqrt(2/pi) ~ 1.596
               (S3.3, Gaussian frequency density);
  * per-axis empirical:  V1 read off a run varying gamma alone at reference
               K = 3.0; V2 off a run varying K alone at reference
               gamma = 1.5.

CRITERION.  A cell counts as coupled-robustly-viable when V1
(max_i x_i < x_crit) and V2 (r > r_min) hold along the entire trajectory
(t in [0, 80]), integrated from the standard coherent initial condition
(Params.seed = 7; run() draws ICs with seed+1). The substrate axis stays
safe on this grid (mean throughput ~1.1 < D_max = 1.5), so H = 1
throughout and the only coupling channel is never activated — which is
exactly what the experiment probes: whether the coupled system can leave V
at parameters where each constraint, taken individually, holds.

HISTORY.  The experiment was run ad hoc for paper v0.6 but its code was
never released; it was reconstructed and re-verified on 2026-08-20
(0 mismatches in both variants). A reduced 4x4 subset is pinned in CI
(tests/test_corridor_headlines.py); this script is the full run.

Usage::

    python separability_grid.py        # full 8x8 grid, ~40 s

Exits nonzero on any mismatch, so the full run doubles as a manual
pre-submission check.

Related:
- papers/viable-corridor.md  (Appendix C.4; S7.1 "the contribution is the
  conjunction")
- teo_simulation.py  (the TEO ODE this grid sweeps)
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import teo_simulation as teo  # noqa: E402


def separability_grid(n_gamma: int = 8, n_K: int = 8):
    """Coupled viability vs. both decoupled predictions on the C.4 grid.

    Returns (gammas, Ks, coupled, analytic, axiswise); the three verdict
    arrays are boolean with shape (n_K, n_gamma), rows indexed by K.
    """
    p = teo.Params()
    gammas = np.linspace(0.0, 1.5, n_gamma)
    Ks = np.linspace(0.0, 4.0, n_K)
    gamma_c = p.x_crit * (1 - p.x_crit) * p.delta / (p.x_crit - p.x_reg)
    k_c = teo.kc_gaussian(p.sigma)

    # Single-axis verdicts for the per-axis empirical prediction: vary one
    # parameter, hold the other at its reference value.
    v1_of_gamma = np.array([
        teo.viability_report(teo.run(replace(p, gamma=float(g))))["V1_pluralism"]
        for g in gammas])
    v2_of_K = np.array([
        teo.viability_report(teo.run(replace(p, K=float(K))))["V2_coherence"]
        for K in Ks])

    coupled = np.zeros((n_K, n_gamma), dtype=bool)
    for i, K in enumerate(Ks):
        for j, g in enumerate(gammas):
            rep = teo.viability_report(
                teo.run(replace(p, gamma=float(g), K=float(K))))
            coupled[i, j] = rep["V1_pluralism"] and rep["V2_coherence"]

    analytic = (gammas[None, :] > gamma_c) & (Ks[:, None] > k_c)
    axiswise = v1_of_gamma[None, :] & v2_of_K[:, None]
    return gammas, Ks, coupled, analytic, axiswise


def main() -> int:
    p = teo.Params()
    gamma_c = p.x_crit * (1 - p.x_crit) * p.delta / (p.x_crit - p.x_reg)
    k_c = teo.kc_gaussian(p.sigma)
    print("Appendix C.4 separability — full 8x8 (gamma, K) grid")
    print(f"  gamma in [0, 1.5], K in [0, 4]; gamma_c = {gamma_c:.4f}, "
          f"K_c = {k_c:.4f}")
    print("  cell viable iff V1 and V2 hold for all t in [0, 80] "
          f"(N={p.N}, seed={p.seed})\n")

    gammas, Ks, coupled, analytic, axiswise = separability_grid()

    # Grid picture: rows K descending, '#' = coupled-viable, '.' = not,
    # '!' = mismatch against the analytic prediction.
    header = "         " + "  ".join(f"g={g:4.2f}" for g in gammas)
    print(header)
    for i in reversed(range(Ks.size)):
        row = []
        for j in range(gammas.size):
            mark = "#" if coupled[i, j] else "."
            if coupled[i, j] != analytic[i, j]:
                mark = "!"
            row.append(f"   {mark}  ")
        print(f"  K={Ks[i]:4.2f} " + " ".join(row))

    mm_analytic = int(np.sum(coupled != analytic))
    mm_axiswise = int(np.sum(coupled != axiswise))
    print(f"\n  mismatches, analytic prediction (g > gamma_c AND K > K_c): "
          f"{mm_analytic} / {coupled.size}")
    print(f"  mismatches, per-axis empirical prediction:                 "
          f"{mm_axiswise} / {coupled.size}")
    if mm_analytic or mm_axiswise:
        for i in range(Ks.size):
            for j in range(gammas.size):
                if coupled[i, j] != analytic[i, j]:
                    print(f"    analytic mismatch at gamma={gammas[j]:.3f}, "
                          f"K={Ks[i]:.3f}: predicted {bool(analytic[i, j])}, "
                          f"coupled {bool(coupled[i, j])}")
                if coupled[i, j] != axiswise[i, j]:
                    print(f"    axiswise mismatch at gamma={gammas[j]:.3f}, "
                          f"K={Ks[i]:.3f}: predicted {bool(axiswise[i, j])}, "
                          f"coupled {bool(coupled[i, j])}")
        print("\n  SEPARABILITY VIOLATED — Appendix C.4 must be re-examined.")
        return 1
    print("\n  0 mismatches in both variants — the C.4 separability claim "
          "reproduces.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
