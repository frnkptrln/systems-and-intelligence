# World Models and VLA Systems: A Process-Model Mapping

**Status:** Hypothesis-generating mapping, not a survey, capability forecast, or claim that robotics
implements the repository's former generator spine.

## Scope

A learned world model estimates selected aspects of an environment's dynamics from data. A
vision-language-action (VLA) system maps observations and instructions to actions, often with a
learned policy and representations inherited from large-scale training. Both can be expressed using
the reconstructed foundation's typed processes, observation kernels, policies, and interventions.

Calling a world model a reconstructed generator is too strong unless the state, observation channel,
equivalence target, and identification result are specified. It is ordinarily one predictive model
optimized for a task, not a uniquely recovered mechanism.

## World Models and Underdetermination

A model can fit training trajectories yet fail when a planner selects states where its errors are
large. Model-based control studies this as model bias or model exploitation. The repository's v1.3
toy isolates a related optimizer's-curse pattern: selecting the best-looking plan from uncertain
model values creates disappointment even when individual errors are unbiased.

The connection is structural, not quantitative. The cellular-automaton benchmark does not predict a
robotics failure rate, and its finite equivalence classes are not learned latent dynamics.

Passive records can also leave causal alternatives unresolved. Action-conditioned data or targeted
experiments may distinguish some alternatives, as the benchmark's interventions do in its declared
family. They need not identify a unique true model, and embodiment is neither necessary nor
sufficient for causal identification.

## VLA Systems and World Coupling

Physical action supplies consequences and new observations that text-only evaluation may omit. It
also introduces latency, actuator limits, damage, and safety constraints. This makes action a useful
source of evidence and a costly intervention.

Matter is not a perfect referee. Sensors are partial and noisy, reward can be misspecified, delayed
effects can escape the horizon, and a successful action does not verify the model that proposed it.
The provenance-depth language can record that an output reached a physical process; depth zero does
not mean epistemic certainty or harmlessness.

Torque, power, battery, and workspace limits are real constraints on a specified platform. They do
not automatically encode human or ecological values, and failure at a physical limit is not a safe
veto.

## What the Mapping Contributes

The mapping suggests four test questions:

1. Which candidate dynamics models remain consistent with the available trajectories?
2. Where does planning amplify model error relative to non-optimizing baselines?
3. Which actions are informative enough to justify their cost and risk?
4. Which independently enforced limits remain effective when the learned policy encounters
   out-of-distribution states?

The repository benchmarks provide small controls for these questions. Transfer to learned world
models or VLA systems requires matched experiments on those systems.

## Boundary

No robotics timeline, mechanism-identification claim, or quantitative transfer follows. The mapping
fails if its vocabulary does not improve preregistration, baseline selection, or failure prediction
beyond the fields' existing concepts.

Related anchors include Dyna, learned world models, model-based reinforcement learning, causal
confusion in imitation learning, and VLA research. The [Related Work
Map](../../meta/research-alignment/related-work-map.md) maintains the project-specific comparison.
