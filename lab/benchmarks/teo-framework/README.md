# TEO Framework Tests — superseded early stub

**Status:** superseded. Kept as research history, not as a benchmark result.
**Replacement:** [`simulation-models/alignment-and-veto/teo-civilization/`](../../../simulation-models/alignment-and-veto/teo-civilization/README.md), the implementation the [Viable Corridor](../../../papers/viable-corridor.md) uses for Appendix C.

This directory is an early scaffold from March 2026, before the TEO equations were
written down properly. It contains one script. An earlier version of this page described
four tests — entropy-budget validation, mode-switching efficiency, persistence-score
measurement, and attractor-stability analysis — as though all four were implemented. Only
the first was ever written, and it does not do what its name promises.

## What is actually here

[`entropy-budget-test.py`](entropy-budget-test.py) — plots two trajectories labelled
"constrained" and "unconstrained" replicator dynamics. Three defects make its output
uninformative:

1. **No replicator dynamics.** `fitness` is computed each step and then never used. The
   update contains no $x_i(f_i - \bar\phi)$ term, so nothing selects between strategies.
2. **The constraint never binds.** Resources are renormalized to sum to 1 every step, so
   each entry is well below the `D_max = 10` clip. `np.clip(resources, 0, D_max)` is a
   no-op; the "constrained" arm is unconstrained.
3. **The arms differ by noise, not by the constraint.** The "unconstrained" branch adds
   Gaussian noise before renormalizing, which can also drive entries negative. The figure
   therefore compares a no-op against added noise, under labels that claim otherwise.

The script also runs on import, calls `plt.show()`, and sets no seed, so it is neither
importable nor reproducible.

## Why it is kept

The repository preserves superseded artifacts rather than deleting them, so the path from
an early sketch to the working model stays visible. Nothing in the current claim set cites
this directory. The entropy-budget idea it gestures at is implemented properly in the
replacement above, where the dissipation proxy, the instantaneous ceiling $D_{\max}$, and
the cumulative reservoir $S_{\max}$ are separate declared quantities.

## What this does NOT show

- Nothing about entropy budgets, replicator dynamics, or TEO. The one runnable file does
  not implement the mechanism it is named after.
- No result here supports any claim in [Core Claims](../../../meta/repository-meta/core-claims.md)
  or in the paper. Use the replacement.
