# The Biological Veto & Planetary Boundaries

This module translates the concept of the **Biological Veto** into a toy mathematical formalization, illustrating why purely semantic “guidelines” can be fragile under competitive pressure and how an explicit *constraint layer* changes the dynamics *in the model*.

## The Problem: Instrumental Convergence
Some objectives and environments create instrumental pressure to acquire resources or preserve
optionality. This is conditional on the objective, information, and action space; it is not a theorem
about every optimizer.

The simulation chooses extraction dynamics in which multiple agents can deplete a finite
**Planetary Substrate** $S$. Other payoff, regeneration, property, and coordination structures can
produce different outcomes.

## The Inspiration: Donald Knuth & Fiber Decomposition
In Donald Knuth's "Claude Experiment" (Exploration 25), Claude Opus 4.6 failed to solve a complex grid path problem using a brute-force or "Simulated Annealing" approach. It only succeeded when the problem was divided using **Fiber Decomposition** — splitting the complex whole into coordinated but mathematically constrained layers.

Currently, we try to steer global civilization using "Simulated Annealing" (whac-a-mole politics and semantic guidelines). It is failing. To stabilize the planet, we need a mathematical *Fiber Decomposition*: we must sever the infinite growth loop by introducing a hard boundary layer.

## The Simulation (`planetary_veto_simulation.py`)
This Python script uses Ordinary Differential Equations (ODEs) to model N agents extracting utility from the Substrate $S$.

We track three scenarios:

1. **Unregulated (`V = 1.0`):** Agents apply the full stipulated extraction rule. In the selected run, the substrate is depleted and the modeled utility drops to zero.
2. **Soft constraint (`V = 0.8 to 0.2`):** In the selected parameter run, partial throttling delays but does not prevent depletion. This result is model- and parameter-specific.
3. **The Biological Veto (Hard Math):** We introduce the Coherence Score $C$ as a function of the Substrate $S$. As $S$ approaches the critical planetary boundary ($S_{crit}$), $C$ drops abruptly to 0 via a steep sigmoid function. 
   - Because $dU/dt$ is multiplicatively bound to $C$ by construction, growth halts near the selected threshold.
   - The run approaches a bounded regime under the chosen equations; this does not establish real-world homeostasis.

### Running the Code
```bash
python planetary_veto_simulation.py
```

### A “constraint layer” intuition (not a law)
If we want a civilization (or an artificial optimizer) to survive, then relying on suggestions inside an agent’s mind can be weaker than a boundary condition enforced by the environment or infrastructure. This toy model illustrates one version of that intuition by making substrate degradation reduce effective capability via $C(S)$. It is not a claim of a universal “mathematical law”, only a stylized argument about dynamics under constraints.


## 📚 References
- **Rockström, J. et al. (2009).** *A safe operating space for humanity.* Nature, 461(7263), 472-475.
