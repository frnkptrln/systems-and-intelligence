# Active Measurement Stack

**Status:** experimental lab scaffold, not a theory claim.

This directory turns several recent research threads into one testable program. The common question is whether an observed failure reflects a missing mechanism, or merely a measurement / representation interface that fails to expose it.

The stack deliberately separates three levels:

1. **Generator identification** — can passive traces distinguish candidate mechanisms, or is an intervention required?
2. **Readout identification** — does a self-report change because the underlying state changed, or because the measurement channel changed?
3. **World-model identification** — does a learned model preserve decision-relevant dynamics across policies, runtimes, action representations, and embodiments?

## Track A — causal identification (runnable now)

`causal_identification.py` implements a minimal two-generator example.

Generator A:

```text
X ~ N(0, 1)
Y = X + eps, eps ~ N(0, 1)
```

Generator B:

```text
Y ~ N(0, 2)
X = 0.5 Y + eta, eta ~ N(0, 0.5)
```

Both induce exactly the same observational Gaussian distribution with covariance

```text
[[1, 1],
 [1, 2]]
```

so passive observations cannot identify the causal direction. Under `do(X=x)`, however:

```text
A: Y ~ N(x, 1)
B: Y ~ N(0, 2)
```

The script computes expected information gain about generator identity and an optional intervention-cost-adjusted optimum.

Run:

```bash
python -m lab.experiments.active_measurement.causal_identification
```

Expected reference values (equal model priors):

| intervention | information gain |
|---|---:|
| `do(X=0)` | ~0.0397 bit |
| `do(X=1)` | ~0.1400 bit |
| `do(X=2)` | ~0.3800 bit |
| `do(X=3)` | ~0.6338 bit |

With quadratic cost `0.05 * x^2` on `x in [0,3]`, the utility-maximizing intervention is approximately `x = 2.55`.

This is a toy witness for **active identifiability**. It is not a reproduction of Model Discovery Agent and does not establish a general causal-discovery result.

## Track B — self-report readouts

`self_report_protocol.yaml` defines a measurement matrix that separates:

```text
latent/internal state
        -> readout representation
        -> elicitation / decoding
        -> observed self-report
```

The protocol varies persona or behavioural state, measurement channel, and perturbation independently. The core comparison is not simply "which prompt gets the best answer?" but **which claims remain invariant across semantically different readouts of the same target**.

The activation-probe channel is explicitly optional because it requires open-weight models and a separate probing pipeline. The initial executable version can use sampled text, forced choice, and log-probability / logit readout where available.

## Track C — world models and embodiment

`world_model_protocol.yaml` defines a later XPolicyLab-compatible evaluation grid. It separates:

```text
action command
    -> realized robot motion
    -> predicted environmental consequence
    -> observed environmental consequence
```

The design includes runtime regime, action representation, embodiment shift, task success, action fidelity, world-action consistency, and cross-embodiment transfer. This lets us test whether apparent policy/model differences survive when integration boundaries are standardized.

## Shared epistemic rule

A negative result is not immediately interpreted as absence of competence or mechanism. First ask which layer failed:

```text
generator / state
representation
measurement interface
selector / runtime
validation
```

Conversely, agreement at the observable layer is not enough to infer shared mechanism.

## Next executable milestones

- [x] Minimal active-identification witness.
- [ ] Run and store causal-identification output in CI or a small result artifact.
- [ ] Implement the text + forced-choice self-report channels on one open model.
- [ ] Add logit-level readout on the same trials.
- [ ] Bring up XPolicyLab `demo_policy` in debug mode.
- [ ] Add one real policy under the same observation/action boundary.
- [ ] Add world-action consistency and embodiment-shift metrics before scaling the policy zoo.

The aim is not to collapse these topics into one theory. The shared stack exists so that the same epistemic distinctions can be tested across otherwise different domains.
