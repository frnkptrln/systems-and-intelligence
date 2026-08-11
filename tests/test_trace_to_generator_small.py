"""Deterministic tests for the learned trace-to-generator experiment."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lab.experiments.trace_to_generator_small.data import (
    SPLIT_PARAMETER_QUANTILES,
    DataConfig,
    generate_sample,
    write_jsonl,
)
from lab.experiments.trace_to_generator_small.dynamics import (
    FAMILIES,
    denormalize_parameter,
    transition,
)


def test_declared_dynamics_remain_bounded_without_control() -> None:
    states = np.linspace(0.0, 1.0, 101)
    for family_id, family in enumerate(FAMILIES):
        for parameter in (family.parameter_min, family.parameter_max):
            outputs = transition(family_id, states, parameter)
            assert np.all(outputs >= 0.0)
            assert np.all(outputs <= 1.0)


def test_sample_generation_is_deterministic_and_query_is_replayable() -> None:
    config = DataConfig(trace_length=8, burn_in=3)
    first = generate_sample(17, "train", seed=99, config=config)
    second = generate_sample(17, "train", seed=99, config=config)
    assert first["family_id"] == second["family_id"]
    assert first["parameter"] == second["parameter"]
    np.testing.assert_array_equal(first["inputs"], second["inputs"])

    inputs = first["inputs"]
    replay = transition(
        first["family_id"], inputs[-1, 0], first["parameter"], inputs[-1, 1]
    )
    assert replay == pytest.approx(first["target_next_state"], abs=1e-7)


@pytest.mark.parametrize("split", ("train", "iid", "ood"))
def test_parameter_split_boundaries_are_respected(split: str) -> None:
    low, high = SPLIT_PARAMETER_QUANTILES[split]
    values = [
        generate_sample(index, split)["parameter_normalized"] for index in range(64)
    ]
    assert all(low <= value <= high for value in values)


def test_jsonl_export_is_hugging_face_loadable(tmp_path) -> None:
    path = tmp_path / "iid.jsonl"
    write_jsonl(path, 3, "iid", config=DataConfig(trace_length=4))
    records = [json.loads(line) for line in path.read_text().splitlines()]
    assert len(records) == 3
    assert len(records[0]["inputs"]) == 5
    assert len(records[0]["inputs"][0]) == 2


def test_parameter_denormalization_hits_declared_endpoints() -> None:
    for family_id, family in enumerate(FAMILIES):
        assert denormalize_parameter(family_id, 0.0) == family.parameter_min
        assert denormalize_parameter(family_id, 1.0) == family.parameter_max


def test_model_forward_backward_and_pretrained_round_trip(tmp_path) -> None:
    torch = pytest.importorskip("torch")
    from lab.experiments.trace_to_generator_small.model import (
        ModelConfig,
        TraceToGeneratorModel,
    )

    config = ModelConfig(
        d_model=32,
        nhead=4,
        num_layers=1,
        dim_feedforward=64,
        dropout=0.0,
        max_seq_len=9,
    )
    model = TraceToGeneratorModel(config)
    inputs = torch.rand(4, 9, 2)
    family_logits, parameter, next_state = model(inputs)
    assert family_logits.shape == (4, len(FAMILIES))
    assert parameter.shape == (4,)
    assert next_state.shape == (4,)
    loss = (
        torch.nn.functional.cross_entropy(family_logits, torch.tensor([0, 1, 2, 3]))
        + parameter.square().mean()
        + next_state.square().mean()
    )
    loss.backward()
    assert any(weight.grad is not None for weight in model.parameters())

    model.eval()
    expected = model(inputs)
    model.save_pretrained(tmp_path)
    loaded = TraceToGeneratorModel.from_pretrained(tmp_path)
    loaded.eval()
    actual = loaded(inputs)
    for expected_tensor, actual_tensor in zip(expected, actual):
        torch.testing.assert_close(expected_tensor, actual_tensor)


def test_default_model_size_is_frozen() -> None:
    pytest.importorskip("torch")
    from lab.experiments.trace_to_generator_small.model import (
        ModelConfig,
        TraceToGeneratorModel,
    )

    model = TraceToGeneratorModel(ModelConfig(max_seq_len=25))
    assert model.parameter_count() == 227_814


def test_training_cli_writes_complete_hugging_face_bundle(tmp_path) -> None:
    pytest.importorskip("torch")
    output_dir = tmp_path / "model"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "lab.experiments.trace_to_generator_small.train",
            "--output-dir",
            str(output_dir),
            "--train-size",
            "16",
            "--eval-size",
            "8",
            "--trace-length",
            "6",
            "--epochs",
            "1",
            "--batch-size",
            "8",
            "--threads",
            "1",
            "--device",
            "cpu",
        ],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert "iid" in result.stdout
    for filename in (
        "config.json",
        "pytorch_model.bin",
        "training_args.json",
        "metrics.json",
        "modeling_trace_to_generator.py",
        "README.md",
    ):
        assert (output_dir / filename).is_file()
    metrics = json.loads((output_dir / "metrics.json").read_text(encoding="utf-8"))
    assert set(metrics["metrics"]) == {"iid", "ood"}
    subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from modeling_trace_to_generator import TraceToGeneratorModel; "
                "print(TraceToGeneratorModel.from_pretrained('.').parameter_count())"
            ),
        ],
        cwd=output_dir,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
