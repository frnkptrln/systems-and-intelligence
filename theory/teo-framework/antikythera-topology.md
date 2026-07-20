# Attractor Analysis for the TEO Phase Space

*An analysis programme; fixed points, cycles, chaos, and fractal basins must be established,
not inferred from their names.*

---

## Status

TEO defines a coupled dynamical system, so questions about equilibria, stability, periodic
orbits, and basins are well posed. The current repository simulations exhibit selected
trajectories and parameter sweeps. They do **not** yet classify every attractor, prove a
limit cycle, establish chaos, or measure a fractal basin boundary.

## State and parameters

Let the model state be

$$
z=(x_1,\ldots,x_N,\theta_1,\ldots,\theta_N,\Omega,H).
$$

For fixed parameters $p$, write its dynamics as

$$
\dot z=F(z;p).
$$

The first analysis task is to find admissible equilibria $z^*$ satisfying

$$
F(z^*;p)=0
$$

under the simplex, phase, and substrate constraints.

## Fixed points

Local stability of a differentiable equilibrium is assessed from the Jacobian

$$
J(z^*;p)=\frac{\partial F}{\partial z}(z^*;p).
$$

If all relevant eigenvalues have negative real parts after accounting for neutral phase
symmetries and constraints, the equilibrium is locally asymptotically stable.

Positive regulation, coupling above a Kuramoto threshold, and bounded overshoot do not by
themselves prove convergence to a unique equitable fixed point. That conclusion depends on
the fitness functions, graph, frequency distribution, brake, boundary conditions, and
initial state.

## Periodic and chaotic behaviour

A periodic trace is not enough to establish a stable limit cycle. Evidence should include a
closed orbit or Poincaré section, attraction from nearby initial states, and numerical
convergence checks.

Likewise, irregular output is not enough to establish chaos. A chaos claim should report,
at minimum:

- a positive maximal Lyapunov exponent with convergence diagnostics;
- sensitivity across nearby initial states;
- bounded aperiodic trajectories over adequate horizons;
- robustness to integration step and solver choice;
- exclusion of transient or numerical artefacts.

No general “edge of chaos” intelligence conclusion follows from a positive exponent.

## Basins and the viable set

A basin of attraction is defined only after an attractor is identified. Mapping a basin
requires sampling initial states from a declared measure and classifying their long-run
destinations with explicit tolerances.

The viable corridor is instead an admissible region defined by selected constraint
conditions. A viable set need not be an attractor basin, and a basin boundary need not be
fractal. Those are separate properties to test.

## Network topology

For an undirected communication graph, $\lambda_2>0$ establishes connectivity. It does not
establish structural resilience under node loss. A Chord-style state would need its own
commit-time composition test; it is not implied by the attractor type or Fiedler value.

## Concrete next experiment

1. choose a small $N$ and freeze all model functions and parameters;
2. solve or numerically locate equilibria;
3. compute constrained Jacobian spectra;
4. continue equilibria across $\gamma$, $K$, and throughput parameters;
5. test for bifurcations;
6. sample initial conditions and estimate basin volumes;
7. only then test periodicity, chaos, or boundary geometry.

The output should distinguish theorem, numerical observation, and solver-dependent
diagnostic.

## Current conclusion

Attractor language is appropriate for TEO, but the original three-way classification was a
hypothesis presented as a result. What survives is a clear mathematical work programme.

## Related

- [Thermodynamics of Emergent Orchestration](../core/thermodynamics-of-orchestration.md)
- [The Viable Corridor](../../papers/viable-corridor.md)
- [Lerchner Boundary](lerchner-boundary.md)
- [Foundations Reconstruction](../core/mathematical-axioms.md)
