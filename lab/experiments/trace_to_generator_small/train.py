#!/usr/bin/env python3
"""Train and evaluate trace-to-generator-small from synthetic traces."""

from __future__ import annotations

import argparse
import copy
import json
import random
import shutil
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

from .data import DataConfig, generate_sample
from .dynamics import FAMILIES
from .model import ModelConfig, TraceToGeneratorModel


class SyntheticTraceDataset(Dataset):
    def __init__(self, size: int, split: str, *, seed: int, config: DataConfig) -> None:
        if size < 1:
            raise ValueError("dataset size must be positive")
        self.size = size
        self.split = split
        self.seed = seed
        self.config = config

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, index: int) -> dict[str, torch.Tensor]:
        sample = generate_sample(index, self.split, seed=self.seed, config=self.config)
        return {
            "inputs": torch.from_numpy(sample["inputs"]),
            "family": torch.tensor(sample["family_id"], dtype=torch.long),
            "parameter": torch.tensor(
                sample["parameter_normalized"], dtype=torch.float32
            ),
            "next_state": torch.tensor(
                sample["target_next_state"], dtype=torch.float32
            ),
        }


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def loss_terms(
    outputs: tuple[torch.Tensor, torch.Tensor, torch.Tensor],
    batch: dict[str, torch.Tensor],
) -> tuple[torch.Tensor, dict[str, float]]:
    family_logits, parameter, next_state = outputs
    family_loss = nn.functional.cross_entropy(family_logits, batch["family"])
    parameter_loss = nn.functional.mse_loss(parameter, batch["parameter"])
    forecast_loss = nn.functional.mse_loss(next_state, batch["next_state"])
    loss = family_loss + parameter_loss + forecast_loss
    return loss, {
        "family_loss": float(family_loss.detach()),
        "parameter_loss": float(parameter_loss.detach()),
        "forecast_loss": float(forecast_loss.detach()),
    }


def train_epoch(
    model: TraceToGeneratorModel,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> float:
    model.train()
    total = 0.0
    count = 0
    for batch in loader:
        batch = {key: value.to(device) for key, value in batch.items()}
        optimizer.zero_grad(set_to_none=True)
        loss, _ = loss_terms(model(batch["inputs"]), batch)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total += float(loss.detach()) * batch["inputs"].shape[0]
        count += batch["inputs"].shape[0]
    return total / count


@torch.no_grad()
def evaluate(
    model: TraceToGeneratorModel, loader: DataLoader, device: torch.device
) -> dict[str, float]:
    model.eval()
    total = 0
    family_correct = 0
    parameter_absolute_error = 0.0
    forecast_absolute_error = 0.0
    persistence_absolute_error = 0.0
    loss_total = 0.0
    for batch in loader:
        batch = {key: value.to(device) for key, value in batch.items()}
        outputs = model(batch["inputs"])
        loss, _ = loss_terms(outputs, batch)
        family_logits, parameter, next_state = outputs
        batch_size = batch["inputs"].shape[0]
        total += batch_size
        loss_total += float(loss) * batch_size
        family_correct += int((family_logits.argmax(dim=-1) == batch["family"]).sum())
        parameter_absolute_error += float((parameter - batch["parameter"]).abs().sum())
        forecast_absolute_error += float((next_state - batch["next_state"]).abs().sum())
        persistence = batch["inputs"][:, -1, 0]
        persistence_absolute_error += float(
            (persistence - batch["next_state"]).abs().sum()
        )
    return {
        "loss": loss_total / total,
        "family_accuracy": family_correct / total,
        "parameter_normalized_mae": parameter_absolute_error / total,
        "forecast_mae": forecast_absolute_error / total,
        "persistence_baseline_mae": persistence_absolute_error / total,
    }


def model_card(
    model: TraceToGeneratorModel,
    metrics: dict[str, dict[str, float]],
    training: dict[str, object],
) -> str:
    return f"""---
license: mit
library_name: pytorch
tags:
- time-series
- system-identification
- synthetic-data
- transformer
---

# trace-to-generator-small

This checkpoint is a compact Transformer encoder trained from scratch on synthetic,
controlled one-dimensional dynamical traces. It predicts the declared generator family,
its within-family normalized parameter, and the next state under a supplied query
intervention.

It is a bounded system-identification experiment, not a general world model and not
evidence that a finite trace identifies a unique real generator.

## Checkpoint

- Parameters: {model.parameter_count():,}
- Families: {", ".join(family.name for family in FAMILIES)}
- Trace tokens: {training["trace_length"] + 1}
- Training seed: {training["seed"]}

## Metrics

```json
{json.dumps(metrics, indent=2)}
```

The `iid` split reuses the training parameter interval with different deterministic
samples. The `ood` split uses only the held-out upper parameter interval. The gap
between them is part of the result, not a nuisance to be tuned away after inspection.

## Load without the source repository

Download this model folder, then run:

```python
from modeling_trace_to_generator import TraceToGeneratorModel

model = TraceToGeneratorModel.from_pretrained(".")
```

The model expects a float tensor shaped `[batch, trace_tokens, 2]`, where each token
contains `(state, control)`. The final token is the next-state query.

## Limitations

- The family set and intervention channel are supplied.
- Traces are synthetic and scalar, with no measurement noise in v0.
- Parameter intervals may expose family-specific dynamical signatures.
- Forecasting one step does not establish causal recovery or long-horizon equivalence.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--train-size", type=int, default=20_000)
    parser.add_argument("--eval-size", type=int, default=4_000)
    parser.add_argument("--trace-length", type=int, default=24)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--seed", type=int, default=260811)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        parser.error("output directory must be absent or empty")
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA requested but not available")
    selected_device = (
        "cuda"
        if args.device == "auto" and torch.cuda.is_available()
        else "cpu"
        if args.device == "auto"
        else args.device
    )
    device = torch.device(selected_device)
    torch.set_num_threads(args.threads)
    set_seed(args.seed)

    data_config = DataConfig(trace_length=args.trace_length)
    datasets = {
        "train": SyntheticTraceDataset(
            args.train_size, "train", seed=args.seed, config=data_config
        ),
        "iid": SyntheticTraceDataset(
            args.eval_size, "iid", seed=args.seed, config=data_config
        ),
        "ood": SyntheticTraceDataset(
            args.eval_size, "ood", seed=args.seed, config=data_config
        ),
    }
    shuffle_generator = torch.Generator().manual_seed(args.seed)
    loaders = {
        "train": DataLoader(
            datasets["train"],
            batch_size=args.batch_size,
            shuffle=True,
            generator=shuffle_generator,
        ),
        "iid": DataLoader(datasets["iid"], batch_size=args.batch_size),
        "ood": DataLoader(datasets["ood"], batch_size=args.batch_size),
    }
    model = TraceToGeneratorModel(ModelConfig(max_seq_len=args.trace_length + 1)).to(
        device
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)

    history: list[dict[str, float | int]] = []
    best_loss = float("inf")
    best_state = None
    for epoch in range(1, args.epochs + 1):
        train_loss = train_epoch(model, loaders["train"], optimizer, device)
        iid = evaluate(model, loaders["iid"], device)
        history.append({"epoch": epoch, "train_loss": train_loss, **iid})
        print(
            f"epoch={epoch:03d} train={train_loss:.5f} "
            f"iid_acc={iid['family_accuracy']:.3f} "
            f"iid_param_mae={iid['parameter_normalized_mae']:.3f} "
            f"iid_forecast_mae={iid['forecast_mae']:.3f}"
        )
        if iid["loss"] < best_loss:
            best_loss = iid["loss"]
            best_state = copy.deepcopy(model.state_dict())
    if best_state is None:
        raise RuntimeError("training produced no checkpoint")
    model.load_state_dict(best_state)
    metrics = {
        "iid": evaluate(model, loaders["iid"], device),
        "ood": evaluate(model, loaders["ood"], device),
    }

    model = model.to("cpu")
    model.save_pretrained(output_dir)
    shutil.copyfile(
        Path(__file__).with_name("model.py"),
        output_dir / "modeling_trace_to_generator.py",
    )
    training = {
        **vars(args),
        "output_dir": str(output_dir),
        "device_used": str(device),
        "model_parameters": model.parameter_count(),
        "data_config": data_config.to_dict(),
        "model_config": model.config.to_dict(),
    }
    (output_dir / "training_args.json").write_text(
        json.dumps(training, indent=2, default=str) + "\n", encoding="utf-8"
    )
    (output_dir / "metrics.json").write_text(
        json.dumps({"metrics": metrics, "history": history}, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "README.md").write_text(
        model_card(model, metrics, training), encoding="utf-8"
    )
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
