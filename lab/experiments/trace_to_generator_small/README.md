# trace-to-generator-small — a learned inverse model

**Status:** implementation complete; only smoke-tested; no research run or Hugging Face checkpoint yet.

**Epistemic status:** bounded system-identification experiment. The model is trained from scratch on synthetic data. It does not consume repository prose, and success within the declared family set would not prove recovery of a unique real generator.

## Question

Can a compact learned sequence encoder infer which declared process family produced a controlled scalar trace, estimate its parameter, and forecast one held-out interventional response? How much of that competence survives a parameter-range shift?

This fills a different slot from two existing tracks:

- the [inverse-reconstruction benchmark](../../benchmarks/inverse-reconstruction/README.md) uses exact or classical estimators inside supplied process families;
- the [learned-searcher protocol](../../benchmarks/learned-searcher/README.md) tests an externally trained language model zero-shot on exact cellular-automaton tasks.

Here the searcher itself is trained, its weights are ours, and the data are generated from declared equations rather than repository text.

## Declared generators

All observed states are clipped to $[0,1]$. A known control $u_t$ is applied after each transition.

| Family | Parameter range | Transition before clipping |
|---|---:|---|
| logistic | $r\in[2.8,4.0]$ | $r x_t(1-x_t)+u_t$ |
| tent | $\mu\in[1.1,2.0]$ | $\mu\min(x_t,1-x_t)+u_t$ |
| sine | $a\in[0.7,1.0]$ | $a\sin(\pi x_t)+u_t$ |
| cubic | $c\in[1.4,2.5]$ | $c x_t(1-x_t^2)+u_t$ |

Each example contains 24 observed transitions and a final query token $(x_T,u_T)$. The targets are:

1. generator family;
2. the within-family parameter normalized to $[0,1]$;
3. $x_{T+1}$ under the query intervention.

## Frozen split boundary for v0

The normalized parameter $q$ is sampled from disjoint intervals:

| Split | $q$ interval | Purpose |
|---|---:|---|
| train | $[0.0,0.7]$ | fitting |
| iid | $[0.0,0.7]$ | new deterministic traces in the fitted range |
| ood | $[0.8,1.0]$ | parameter extrapolation |

The interval $(0.7,0.8)$ is unused. The OOD gap is part of the protocol and must not be moved after seeing a result. v0 has no observation noise; noise, missing states, new families, and changed intervention channels are later stress tests, not hidden degrees of freedom in the first run.

## Model

`TraceToGeneratorModel` is a small PyTorch Transformer encoder with learned positional embeddings and three heads. It is not based on Qwen or another pretrained model. A training run writes a Hugging Face-ready folder containing:

- `config.json`;
- `pytorch_model.bin`;
- `training_args.json`;
- `metrics.json`;
- `modeling_trace_to_generator.py`, so the checkpoint can be loaded without this repository;
- a generated `README.md` model card.

## Run locally

Install the optional ML dependency first:

```bash
pip install -r requirements-ml.txt

python -m lab.experiments.trace_to_generator_small.export_dataset \
  --output-dir /tmp/trace-to-generator-data

python -m lab.experiments.trace_to_generator_small.train \
  --output-dir /tmp/trace-to-generator-model
```

A cheap pipeline check is intentionally not a research result:

```bash
python -m lab.experiments.trace_to_generator_small.train \
  --output-dir /tmp/trace-to-generator-smoke \
  --train-size 256 --eval-size 64 --epochs 1 --batch-size 32
```

## What the first real run must report

- IID and OOD family accuracy;
- normalized parameter MAE;
- one-step forecast MAE;
- the persistence baseline $\lvert x_{T+1}-x_T\rvert$ on the exact same samples;
- architecture, parameter count, seeds, split sizes, and full training history.

The checkpoint is interesting only if its forecast beats persistence and the OOD result remains materially above the 25% uniform-family floor. IID success alone is compatible with interpolation or family-specific surface cues.

## Failure boundaries

- The family set and observation/control interface are supplied.
- A family label can be right while the fitted mechanism is wrong.
- Clipping can itself reveal information about a family and parameter regime.
- One-step prediction does not establish long-horizon or interventional equivalence.
- Synthetic success does not imply identification in physical, biological, or social systems.
