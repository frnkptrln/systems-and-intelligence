"""Deterministic synthetic traces with IID and parameter-OOD splits."""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from .dynamics import FAMILIES, denormalize_parameter, transition

SPLIT_PARAMETER_QUANTILES = {
    "train": (0.0, 0.7),
    "iid": (0.0, 0.7),
    "ood": (0.8, 1.0),
}
SPLIT_SEED_OFFSETS = {"train": 0, "iid": 1_000_000, "ood": 2_000_000}


@dataclass(frozen=True)
class DataConfig:
    """Frozen controls for one synthetic dataset family."""

    trace_length: int = 24
    burn_in: int = 8
    intervention_probability: float = 0.25
    query_intervention_probability: float = 0.5
    intervention_amplitude: float = 0.08
    observation_noise_std: float = 0.0

    def __post_init__(self) -> None:
        if self.trace_length < 2:
            raise ValueError("trace_length must be at least 2")
        if self.burn_in < 0:
            raise ValueError("burn_in cannot be negative")
        for value in (
            self.intervention_probability,
            self.query_intervention_probability,
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError("intervention probabilities must lie in [0, 1]")
        if self.intervention_amplitude < 0.0:
            raise ValueError("intervention_amplitude cannot be negative")
        if self.observation_noise_std < 0.0:
            raise ValueError("observation_noise_std cannot be negative")

    def to_dict(self) -> dict[str, int | float]:
        return asdict(self)


def _rng(seed: int, split: str, index: int) -> np.random.Generator:
    if split not in SPLIT_SEED_OFFSETS:
        raise ValueError(f"unknown split: {split}")
    if index < 0:
        raise ValueError("sample index cannot be negative")
    sequence = np.random.SeedSequence([seed, SPLIT_SEED_OFFSETS[split], index])
    return np.random.default_rng(sequence)


def generate_sample(
    index: int,
    split: str,
    *,
    seed: int = 260811,
    config: DataConfig | None = None,
) -> dict[str, object]:
    """Generate one trace and its family, parameter, and queried next state."""
    config = config or DataConfig()
    rng = _rng(seed, split, index)
    family_id = int(rng.integers(len(FAMILIES)))
    low, high = SPLIT_PARAMETER_QUANTILES[split]
    parameter_normalized = float(rng.uniform(low, high))
    parameter = denormalize_parameter(family_id, parameter_normalized)

    state = float(rng.uniform(0.05, 0.95))
    for _ in range(config.burn_in):
        state = transition(family_id, state, parameter)

    controls = np.zeros(config.trace_length + 1, dtype=np.float64)
    observed_mask = rng.random(config.trace_length) < config.intervention_probability
    observed_indices = np.flatnonzero(observed_mask)
    controls[observed_indices] = rng.uniform(
        -config.intervention_amplitude,
        config.intervention_amplitude,
        size=len(observed_indices),
    )
    if rng.random() < config.query_intervention_probability:
        controls[-1] = rng.uniform(
            -config.intervention_amplitude, config.intervention_amplitude
        )

    states = np.empty(config.trace_length + 1, dtype=np.float64)
    states[0] = state
    for step_index in range(config.trace_length):
        states[step_index + 1] = transition(
            family_id,
            states[step_index],
            parameter,
            controls[step_index],
        )
    target_next_state = transition(family_id, states[-1], parameter, controls[-1])

    observed_states = states.copy()
    if config.observation_noise_std:
        observed_states = np.clip(
            observed_states
            + rng.normal(0.0, config.observation_noise_std, size=states.shape),
            0.0,
            1.0,
        )
    inputs = np.stack((observed_states, controls), axis=-1).astype(np.float32)
    return {
        "id": f"{split}-{index:07d}",
        "split": split,
        "family_id": family_id,
        "family": FAMILIES[family_id].name,
        "parameter": float(parameter),
        "parameter_normalized": parameter_normalized,
        "inputs": inputs,
        "target_next_state": float(target_next_state),
    }


def iter_samples(
    size: int,
    split: str,
    *,
    seed: int = 260811,
    config: DataConfig | None = None,
) -> Iterator[dict[str, object]]:
    if size < 1:
        raise ValueError("split size must be positive")
    for index in range(size):
        yield generate_sample(index, split, seed=seed, config=config)


def json_record(sample: dict[str, object]) -> dict[str, object]:
    return {
        **sample,
        "inputs": np.asarray(sample["inputs"]).tolist(),
    }


def write_jsonl(
    path: Path,
    size: int,
    split: str,
    *,
    seed: int = 260811,
    config: DataConfig | None = None,
) -> None:
    with path.open("x", encoding="utf-8") as handle:
        for sample in iter_samples(size, split, seed=seed, config=config):
            handle.write(json.dumps(json_record(sample), separators=(",", ":")) + "\n")
