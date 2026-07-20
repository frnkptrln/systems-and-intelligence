# Minimal Resource-Constrained Agent

*Status: executable toy controller. Its variables are engineering proxies, not measured
thermodynamic state variables and not a definition of intelligence.*

## Purpose

The code in core/constraints.py and core/minimal_agent.py compares a controller that trades task
reward against a resource budget with one that pursues the task reward more aggressively. It asks a
small question: can an explicit cost and stability term alter the controller's trajectory in the
stipulated environment?

## Variables

- **energy** is a numeric action budget. The values assigned to actions are chosen by the model; they
  are not joules unless an external calibration supplies units.
- **entropy** is an accumulated damage or disorder proxy. Adding one per step and ten for an
  aggressive action is a simulation rule, not thermodynamic entropy.
- **stability_score** is the reciprocal of that proxy. It reports the chosen state variable and does
  not establish homeostasis.
- **task_success** is the reward supplied by the environment.

The combined objective is a multi-objective control rule. Referring to it as free energy is only an
analogy; the script does not derive a variational free-energy objective or implement active
inference.

## What a Run Shows

Under the selected parameters, the constrained controller can preserve more of its budget or
stability proxy while accepting less immediate task reward. That is an ordinary trade-off produced
by the reward and transition equations.

It does not show:

- that intelligence requires these variables;
- that the coefficients are physically correct;
- that one scalar captures ecological or biological viability;
- that a constrained controller is aligned;
- that the policy generalizes outside the toy environment.

## Useful Follow-Ups

Sweep the cost coefficients and initial states, match total action opportunity, add delayed and noisy
measurements, compare hard budgets with soft penalties, and introduce an adversary that can alter the
proxy. Report a Pareto frontier rather than declaring one weighting optimal.

The module is valuable as a minimal test harness for constraint design. Its strongest defensible
claim is that explicitly represented costs can change behavior in the model.
