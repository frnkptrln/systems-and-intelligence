# Active-Inference Veto Toy Model

*Status: stylized simulation. It does not prove that active inference creates an unbreakable
biological veto.*

## Mechanism Encoded by the Model

The script stipulates two coupled quantities:

1. a resource-extracting controller;
2. a substrate-health variable damaged by extraction.

Below a selected health threshold, the objective assigns a large penalty to extraction and favors a
restorative action. The plotted controller therefore changes behaviour when the threshold is crossed.
That outcome follows from the objective and action set supplied by the code.

The simulation borrows vocabulary from active inference, including surprise and free energy. In a
full active-inference model, results depend on the generative model, preferences, variational family,
precision, observations, and available actions. Free-energy minimization alone does not force a
controller to preserve a biological substrate: it may instead change beliefs, sensing, precision,
or policy. The model also does not address a controller that can modify the veto.

## What It Can Test

The toy is useful for comparing explicit designs:

- no health feedback;
- a finite health penalty;
- a hard action constraint;
- noisy or delayed health observations;
- misspecified thresholds;
- controller access to the measurement or constraint layer.

Those comparisons can show which stipulated mechanisms keep health within bounds in the simulated
environment. Claims about real robustness require adversarial analysis and an implementation whose
constraint layer cannot be silently bypassed.

## Run

```bash
python3 active-inference-veto.py
```

The figures show substrate health, accumulated model utility, and the script's free-energy-like
objective. They should be read as trajectories of this chosen model, not as a theorem derived from
the Free Energy Principle.
