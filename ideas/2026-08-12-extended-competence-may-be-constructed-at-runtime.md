# Extended Competence May Be Constructed at Runtime

**Status:** exploratory note — not a repository claim.

**Trigger:** Gu et al. (2026), *HarnessWAM: Bridging Prediction and Deliberation in World Action Models*.

A model may possess strong local predictive and action competence while still failing at temporally extended tasks. HarnessWAM addresses this not by changing the underlying World Action Model, but by adding external task state, evidence-grounded scene belief, capability constraints, verification, and recovery.

## Question

When does apparently “latent” competence belong to the model, and when is extended competence newly constructed by the runtime that composes local abilities across time?

This suggests separating **local policy competence** from **runtime-constructed competence**. A system can outperform the same model not because more knowledge was uncovered, but because external state and feedback alter which trajectories are reachable.

## Tension

Expanding the system boundary may explain performance better, but risks making competence attribution vacuous if every supporting mechanism is absorbed into “the agent.” The useful question may therefore be not simply where competence resides, but which competence remains invariant under changes to runtime, memory, observation, verification, and recovery.

## Connections

- *The Agent Is Not Where the Model Ends*
- situated competence
- runtime as generator
- verification as reverse pressure
- external memory
