# Part 1: The Mechanics of Emergence

**Status:** Current reader chapter.

Emergence is not a substance added to a system. It is a relation between levels of description.
A specified process evolves at one level; an observer selects variables, a scale, and a
coarse-graining at another; stable or useful regularities may then become visible.

Boids provide a simple example. Each simulated bird updates its velocity through separation,
alignment, and cohesion. The flock is a macro-description of the resulting trajectories. The code
demonstrates that those local updates can produce that measured pattern under the selected
parameters. It does not prove that every collective structure has the same cause.

## Local processes and global descriptions

The repository repeatedly studies three questions:

1. Which local processes are specified?
2. Which macro-variable is being measured?
3. Under which perturbations does the macro-pattern persist or fail?

Local components need not represent the selected macro-variable. That is true of many simulations
here, but it is not a universal theorem that components can never obtain global information. Access
depends on the communication architecture, sensors, memory, and model class.

## Formal tools, not axioms

Several established measures recur throughout the project. None defines emergence, life, or
intelligence by itself.

| Domain | Instrument | What it can establish |
|:---|:---|:---|
| Graph theory | Fiedler value $\lambda_2$ | Whether a finite undirected graph is connected when $\lambda_2>0$, plus a topology-sensitive connectivity scale |
| Information theory | Entropy and mutual information | Uncertainty and statistical dependence for declared variables and distributions |
| Active inference | Variational or expected free energy | An objective inside a specified generative model, preference structure, and action scheme |
| Algorithmic information | Description length and $K(x)$ | Compression relative to a language or machine; exact Kolmogorov complexity is generally uncomputable |

A high Fiedler value does not guarantee decentralization or resilience under every attack model.
High entropy can be noise, while deterministic processes can exhibit complex coarse-grained
behavior. Free-energy notation does not create a biological veto. Incompressibility does not imply
novelty, value, or survival.

## Thresholds are model-specific

Kuramoto synchronization, the Ising transition, percolation, and learning dynamics can each display
sharp changes. Their control parameters and order parameters are not interchangeable. Evidence for
a critical point in one model does not establish an “edge of chaos” law for organisms, minds, or
societies.

The right comparative question is therefore not whether every scale uses the same equation, but
whether carefully defined systems share a universality class or another invariant structure. That
is an [open problem](../theory/reference/open-problems.md#open-problem-5-the-renormalization-question),
not a premise.

## Construction as evidence

The simulations make abstract claims executable:

- [Boids](../simulation-models/emergent-dynamics/boids-flocking/README.md) test local motion rules.
- [Coupled oscillators](../simulation-models/emergent-dynamics/coupled-oscillators/README.md) test
  phase synchronization.
- [Reaction–diffusion](../simulation-models/emergent-dynamics/reaction-diffusion/README.md) tests
  pattern formation from local transport and reaction.
- [Iterated function systems](../simulation-models/emergent-dynamics/iterated-function-systems/README.md)
  test repeated contractive maps.
- [Lenia](../simulation-models/emergent-dynamics/lenia/README.md) tests persistent structures in a
  continuous cellular automaton.

Each artifact establishes behavior of its own declared process. Cross-scale interpretation begins
only after the state variables, observations, interventions, and failure conditions have been
matched.
