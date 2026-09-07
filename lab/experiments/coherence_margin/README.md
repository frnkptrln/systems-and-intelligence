# A Counterexample to the Continuum Sufficiency Claim

**Status:** Analytical counterexample in the Lorentzian Ott–Antonsen regime;
finite Gaussian size control completed, 2026-09-07.

[Conjecture 1](../../../papers/viable-corridor.md#34-conjecture-1-sufficiency)
requires `K > K_c` but defines viability using a fixed floor `r >= r_min > 0`.
Those conditions are different. The Lorentzian distribution explicitly
allowed in §2 gives a counterexample to the conjecture's continuum reading,
even at `H = 1`, where the coherence axis is decoupled. The paper now carries
an erratum at §3.4.

## Analytical counterexample and scope

For an infinite all-to-all population with Lorentzian frequency half-width
`Delta > 0`, the established Ott–Antonsen reduction
([2008, §III](https://arxiv.org/html/0806.0004v1#S3)) gives, at full substrate health,

$$
\dot r=r\left[\frac K2(1-r^2)-\Delta\right],\qquad
r_* = \sqrt{1-\frac{2\Delta}{K}},\qquad K>K_c=2\Delta.
$$

For `0 < r_min < 1`, the vector field at the required floor points inward exactly when

$$
\dot r\big|_{r=r_{\min}}\geq0
\quad\Longleftrightarrow\quad
K\geq K_{\mathrm{floor}}:=\frac{2\Delta}{1-r_{\min}^2}.
$$

If `K < K_floor`, the field is strictly negative on the entire compact
interval `[r_min, 1]` and bounded away from zero there. Every initially
admissible reduced trajectory crosses the floor in finite time. Thus **no
invariant open set exists on this coherence axis**. At equality the interval
is invariant but the limiting margin is zero; strict inequality gives a
positive limiting margin. Equality can satisfy the paper's deterministic
open-set definition, which does not require robustness to parameter changes.

For `Delta = 1`, `r_min = 0.5`, onset is `K_c = 2` and the required threshold
is `K_floor = 8/3`. Choosing `K = 2.2` satisfies onset but gives
`r_* = sqrt(1/11) = 0.301511 < 0.5`. Independent resource regulation and a
safe substrate budget cannot remove this obstruction: `gamma` does not enter
the phase equation at `H = 1`. This defeats the stated sufficient conjunction
under its Lorentzian continuum/Ott–Antonsen interpretation.

**The larger defect is an unspecified regime.** The paper combines finite-`N`
resource and substrate lemmas with a thermodynamic-limit coherence lemma,
then states sufficiency without fixing a common state space, admissible
initial distributions, or topology for the open set `U`. A repaired statement
must first choose its regime and then supply a floor-dependent condition.
The scalar result is exact on the reduced manifold. Extending the obstruction
to a wider continuum class requires the regularity and attraction assumptions
of Ott and Antonsen ([2009, §§III–IV](https://arxiv.org/abs/0902.2773)); the
manifold alone is not an open subset of every phase-distribution space.
No universal finite-`N` threshold follows from this argument.

This is an obstruction on the coherence axis itself. The paper's existing
warning about coupling-induced transient excursions does not address it.

![Lorentzian equilibrium and reduced trajectories, alongside the Gaussian population-size control at K=2](results/coherence_margin.png)

## Finite Gaussian size control

The original `N = 50` grid contained two failures at `K = 2.0`, above the
Gaussian stationary floor `1.747903`. To test their persistence with size,
the unchanged canonical TEO right-hand side was run at `N = 200` and
`N = 1000`, using the same seeds `0..15`, `K = 2.0`, and `t = 0..80`.
All other scalar parameters and the initial-condition procedure are unchanged.
Larger populations extend the same random draw sequences for frequencies and
initial phases; the original `N = 50` results provide the comparison.

| Population | Floor failures | Range of minimum sampled coherence |
|---|---:|---:|
| 50 | 2 / 16 | 0.159197–0.804039 |
| 200 | 0 / 16 | 0.532021–0.784975 |
| 1000 | 0 / 16 | 0.672819–0.750204 |

The two failures disappear on both larger grids, and dispersion narrows.
**These runs do not establish an additional continuum dynamical obstruction
above the Gaussian stationary floor.** They are consistent with finite-size
effects. Changing population size changes both the empirical frequencies and
the phase sample, so this control does not isolate frequency sampling as the
sole cause. Sixteen seeds and a finite observation interval do not establish
universal safety, a convergence rate, or a failure probability.

All 32 additional runs completed and retained safe resource shares and
substrate health; the largest simplex error over all 112 recorded runs is
`4.25e-14` or less. The new trajectories closest to the floor (seed `15` at
`N = 200`, seed `11` at `N = 1000`) were rerun with tighter tolerances and
halved maximum step. Both classifications survive; their minimum coherence
changes by at most `1.20e-8` and final coherence by at most `5.17e-8`.

The original `N = 50` grid remains a descriptive record:

| `K` | 0.8 | 1.6 | 1.7 | 2.0 | 3.0 |
|---|---:|---:|---:|---:|---:|
| Failures / 16 runs | 16 | 10 | 9 | 2 | 0 |

Its above-onset failures are not the evidence for the Lorentzian
counterexample. The distributions differ, and finite Gaussian transients were
already anticipated by the paper.

## Independent numerical checks

Forty-five scalar integrations agree with the closed solution for `y = r^2`,
derived from `y' = (K-2*Delta)y-K*y^2`, to maximum absolute error `1.06e-11`.
They cover three floors `{0.25, 0.5, 0.75}`, three initial amplitudes per
floor, and five couplings spanning onset and the relevant floor.
Independent stationary-branch quadrature agrees with the Lorentzian formula
to `6.04e-14`. The same quadrature gives:

| Required coherence | Lorentzian floor, `Delta = 1` | Gaussian stationary floor, `sigma = 1` |
|---|---:|---:|
| 0.25 | 2.133333 | 1.628843 |
| 0.50 | 2.666667 | 1.747903 |
| 0.75 | 4.571429 | 2.070711 |

The onset thresholds are respectively `2` and `1.595769`. The Gaussian
column is a stationary-branch calculation, not a transient or finite-`N`
invariance bound.

## Data, tests and reproduction

[results.json](results/results.json) contains all 80 original cells, the
32 added cells, scalar checks, validation reruns and source hashes. Records
occupy one line each. Frequency arrays are regenerated from seeds and the
recorded NumPy version; only their useful diagnostics are stored. There is
one committed figure, in PNG format. The original numerical values are
retained; redundant solver settings and frequency arrays were removed.

CI **recomputes all 48 size-comparison trajectories** through the canonical
`run()`, including its initial-condition construction, and checks the
`2/16, 0/16, 0/16` result. It also independently integrates the scalar
equation and checks quadrature. The stored original 80-cell grid receives an
integrity check, with two further canonical reruns at `K = 1.6` and `3.0`.
Its other 62 cells are frozen records, not independently regenerated by CI.

From the repository root, with [requirements.txt](../../../requirements.txt)
and the test dependencies installed:

```bash
python lab/experiments/coherence_margin/coherence_margin.py --output /tmp/coherence-margin
pytest tests/test_coherence_margin.py -q
```

The first command recomputes all 112 cells and numerical controls. The
canonical TEO implementation is unchanged from base `ef9c5117`. The
[original runner](https://github.com/frnkptrln/systems-and-intelligence/commit/f59d5e0eb4fee6224aed3f9bb19e682897f27e80)
is retained in history; baseline and size-sweep source hashes are recorded
separately. The paper's original capability-loading and budget results are
unaffected by this correction.
