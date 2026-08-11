"""A compact Transformer encoder for bounded generator identification."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
from torch import nn


@dataclass(frozen=True)
class ModelConfig:
    input_dim: int = 2
    d_model: int = 96
    nhead: int = 4
    num_layers: int = 3
    dim_feedforward: int = 192
    dropout: float = 0.1
    num_families: int = 4
    max_seq_len: int = 64

    def __post_init__(self) -> None:
        if self.d_model % self.nhead:
            raise ValueError("d_model must be divisible by nhead")
        if self.max_seq_len < 2:
            raise ValueError("max_seq_len must be at least 2")

    def to_dict(self) -> dict[str, int | float | str | list[str]]:
        return {
            **asdict(self),
            "model_type": "trace-to-generator-small",
            "architectures": ["TraceToGeneratorModel"],
        }


class TraceToGeneratorModel(nn.Module):
    """Infer process family/parameter and answer one next-state query."""

    def __init__(self, config: ModelConfig | None = None) -> None:
        super().__init__()
        self.config = config or ModelConfig()
        self.input_projection = nn.Linear(self.config.input_dim, self.config.d_model)
        self.position = nn.Parameter(
            torch.empty(1, self.config.max_seq_len, self.config.d_model)
        )
        layer = nn.TransformerEncoderLayer(
            d_model=self.config.d_model,
            nhead=self.config.nhead,
            dim_feedforward=self.config.dim_feedforward,
            dropout=self.config.dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(
            layer,
            num_layers=self.config.num_layers,
            norm=nn.LayerNorm(self.config.d_model),
        )
        self.family_head = nn.Linear(self.config.d_model, self.config.num_families)
        self.parameter_head = nn.Linear(self.config.d_model, 1)
        self.next_state_head = nn.Linear(self.config.d_model, 1)
        nn.init.normal_(self.position, mean=0.0, std=0.02)

    def forward(
        self, inputs: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if inputs.ndim != 3 or inputs.shape[-1] != self.config.input_dim:
            raise ValueError(
                f"expected [batch, sequence, {self.config.input_dim}] inputs"
            )
        if inputs.shape[1] > self.config.max_seq_len:
            raise ValueError("input sequence exceeds configured max_seq_len")
        hidden = self.input_projection(inputs)
        hidden = hidden + self.position[:, : inputs.shape[1]]
        encoded = self.encoder(hidden)
        summary = encoded[:, -1]
        family_logits = self.family_head(summary)
        parameter = torch.sigmoid(self.parameter_head(summary)).squeeze(-1)
        next_state = torch.sigmoid(self.next_state_head(summary)).squeeze(-1)
        return family_logits, parameter, next_state

    def parameter_count(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters())

    def save_pretrained(self, output_dir: str | Path) -> None:
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        (path / "config.json").write_text(
            json.dumps(self.config.to_dict(), indent=2) + "\n", encoding="utf-8"
        )
        torch.save(self.state_dict(), path / "pytorch_model.bin")

    @classmethod
    def from_pretrained(
        cls, model_dir: str | Path, *, map_location: str | torch.device = "cpu"
    ) -> TraceToGeneratorModel:
        path = Path(model_dir)
        payload = json.loads((path / "config.json").read_text(encoding="utf-8"))
        fields = ModelConfig.__dataclass_fields__
        config = ModelConfig(**{key: payload[key] for key in fields})
        model = cls(config)
        state = torch.load(
            path / "pytorch_model.bin", map_location=map_location, weights_only=True
        )
        model.load_state_dict(state)
        return model
