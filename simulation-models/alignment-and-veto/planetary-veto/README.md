# The Biological Veto & Planetary Boundaries

This module translates the concept of the **Biological Veto** into a toy mathematical formalization,
illustrating why purely semantic “guidelines” can be fragile under competitive pressure and how an
explicit *constraint layer* changes the dynamics *in the model*.

## The Problem: Instrumental Convergence

Some objectives and environments create instrumental pressure to acquire resources or preserve
optionality. This is conditional on the objective, information, and action space; it is not a theorem
about every optimizer.

The simulation chooses extraction dynamics in which multiple agents can deplete a finite
**Planetary Substrate** $S$. Other payoff, regeneration, property, and coordination structures can
produce different outcomes.

## Historical inspiration: Knuth's *Claude's Cycles*

Donald Knuth's note *Claude's Cycles* (28 February 2026; later revised) describes an extended
problem-solving interaction with Claude Opus 4.6 on a directed-Hamiltonian-cycle construction.
The sequence is more interesting than the earlier README summary implied:

- **Exploration 15** introduced a fiber decomposition using
  $i+j+k\pmod m$, turning the three-dimensional graph into a layered problem with two-dimensional
  fiber coordinates.
- Later explorations used exhaustive search and simulated annealing to find finite examples and
  regularities. Knuth records the conclusion after **Exploration 25** as essentially: simulated
  annealing can find solutions, but it does not supply a general construction.
- The eventual odd-$m$ construction emerged from the fiber/serpentine representation and subsequent
  analysis. The source is a case study in how a change of representation can expose constructive
  structure; it is not evidence for the Biological Veto or for a general law of decomposition.

The earlier version of this README incorrectly compressed that history into “Exploration 25 failed
with simulated annealing and then succeeded by fiber decomposition.” The primary source does not
support that chronology.

### Why the analogy remains here

The useful analogy is deliberately narrow: a difficult search can sometimes become tractable after
choosing a representation that exposes constraints and decomposition structure. That is an
**inspiration for model design**, not a derivation from Knuth's result.

Likewise, describing political or civilizational governance as “simulated annealing” is only a
metaphor. This simulation does not establish that real societies require one particular mathematical
fiber decomposition, or that a hard boundary layer is sufficient for planetary stability.

## The Simulation (`planetary_veto_simulation.py`)

This Python script uses Ordinary Differential Equations (ODEs) to model N agents extracting utility
from the Substrate $S$.

We track three scenarios:

1. **Unregulated (`V = 1.0`):** Agents apply the full stipulated extraction rule. In the selected
   run, the substrate is depleted and the modeled utility drops to zero.
2. **Soft constraint (`V = 0.8 to 0.2`):** In the selected parameter run, partial throttling delays
   but does not prevent depletion. This result is model- and parameter-specific.
3. **The Biological Veto (hard model constraint):** We introduce the Coherence Score $C$ as a
   function of the Substrate $S$. As $S$ approaches the selected critical boundary ($S_{crit}$),
   $C$ drops abruptly toward 0 via a steep sigmoid function.
   - Because $dU/dt$ is multiplicatively bound to $C$ by construction, growth halts near the selected
     threshold.
   - The run approaches a bounded regime under the chosen equations; this does not establish
     real-world homeostasis.

### Running the Code

```bash
python planetary_veto_simulation.py
```

### A constraint-layer intuition, not a law

If a system's continued operation depends on measured substrate variables, an independently enforced
boundary condition can constrain actions in ways that an internal suggestion may not. This toy model
illustrates one version of that intuition by making substrate degradation reduce effective capability
through $C(S)$.

The result is conditional on the stipulated equations. It is not a universal mathematical law of
alignment, ecology, governance, or survival.

## References

- **Knuth, D. E. (2026).** *Claude's Cycles*. Stanford Computer Science Department, 28 February
  2026, revised 14 April 2026. Primary historical source for the fiber-decomposition anecdote.
- **Rockström, J. et al. (2009).** *A safe operating space for humanity.* Nature, 461(7263),
  472–475.
