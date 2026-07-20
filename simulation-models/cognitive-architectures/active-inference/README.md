# Active-Inference Gradient Toy

*Status: small illustrative optimization model. It is not a neurobiological foundation for the
repository and does not establish how LLMs, organisms, or alignment work.*

## Model

The script defines a scalar free-energy-like objective with an internal estimate, an observation,
and an action. It compares gradient updates that:

1. change only the internal estimate;
2. change only the modeled environment through action;
3. update both.

Under the supplied equations, each enabled variable moves down the selected objective. The third
condition reaches the trade-off encoded by its coefficients.

This illustrates a common active-inference distinction between perceptual and active updates. A full
model must specify a generative model, variational family, preferences, precision, policy, and
observation/action mapping. Surprise is not simply prediction error, and variational free energy is
not identical to a human value or substrate-health signal.

## Run

    python active_inference_simulation.py

## Bounded Interpretation

If a controller is given fixed preferences and actions that can change the environment, the chosen
objective may favor changing the environment rather than revising beliefs. It may also favor belief
revision, information gathering, inaction, or another policy, depending on the model. Nothing in
this run shows that a model with a conflicting preference will inevitably act against humans.

Useful follow-ups vary preference precision, action costs, model error, inaccessible observations,
and alternative policies, then compare active inference with ordinary state estimation and control.

## Reference

- Friston, K. (2010). *The free-energy principle: a unified brain theory?* Nature Reviews
  Neuroscience, 11(2), 127–138.
