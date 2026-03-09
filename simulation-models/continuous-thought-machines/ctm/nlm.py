from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import torch
import torch.nn as nn


@dataclass(frozen=True)
class NLMConfig:
    """
    Configuration for Neuron-Level Models (NLMs).

    Each neuron has its own tiny MLP that maps:
      [pre_activation_t, post_activation_{t-1}, ..., post_activation_{t-H}]
    -> post_activation_t
    """

    num_neurons: int
    history_len: int = 8
    hidden_dim: int = 16
    nonlinearity: str = "gelu"  # "gelu" | "tanh" | "relu" | "silu"
    use_layernorm: bool = True


class ActivationHistoryBuffer(nn.Module):
    """
    A simple FIFO buffer that stores the last H post-activations per neuron.

    Shapes
    - state: (batch, neurons, history_len)
    - push(x): x is (batch, neurons)
    """

    def __init__(self, num_neurons: int, history_len: int):
        super().__init__()
        self.num_neurons = int(num_neurons)
        self.history_len = int(history_len)
        self.register_buffer("_state", torch.empty(0), persistent=False)

    @property
    def state(self) -> torch.Tensor:
        return self._state

    def reset(self, batch_size: int, *, device=None, dtype=None) -> torch.Tensor:
        device = device if device is not None else self._infer_device()
        dtype = dtype if dtype is not None else torch.float32
        self._state = torch.zeros(
            (int(batch_size), self.num_neurons, self.history_len),
            device=device,
            dtype=dtype,
        )
        return self._state

    def push(self, x: torch.Tensor) -> torch.Tensor:
        if x.ndim != 2:
            raise ValueError(f"Expected x with shape (batch, neurons), got {tuple(x.shape)}")
        if x.shape[1] != self.num_neurons:
            raise ValueError(
                f"Expected x neurons dim={self.num_neurons}, got {int(x.shape[1])}"
            )

        if self._state.numel() == 0 or self._state.shape[0] != x.shape[0]:
            self.reset(x.shape[0], device=x.device, dtype=x.dtype)

        if self.history_len == 0:
            return self._state

        # shift right, insert newest at index 0
        self._state = torch.roll(self._state, shifts=1, dims=2)
        self._state[:, :, 0] = x
        return self._state

    def _infer_device(self):
        # best-effort; buffer might be empty before first reset
        for p in self.parameters():
            return p.device
        return torch.device("cpu")


class _PerNeuronLinear(nn.Module):
    """
    A per-neuron linear layer:
      y[b, n, o] = sum_i x[b, n, i] * W[n, o, i] + b[n, o]
    """

    def __init__(self, num_neurons: int, in_features: int, out_features: int):
        super().__init__()
        self.num_neurons = int(num_neurons)
        self.in_features = int(in_features)
        self.out_features = int(out_features)

        w = torch.empty(self.num_neurons, self.out_features, self.in_features)
        b = torch.empty(self.num_neurons, self.out_features)
        nn.init.kaiming_uniform_(w, a=5**0.5)
        nn.init.zeros_(b)
        self.weight = nn.Parameter(w)
        self.bias = nn.Parameter(b)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.ndim != 3:
            raise ValueError(f"Expected x with shape (batch, neurons, in), got {tuple(x.shape)}")
        if x.shape[1] != self.num_neurons or x.shape[2] != self.in_features:
            raise ValueError(
                f"Expected x with shape (batch,{self.num_neurons},{self.in_features}), got {tuple(x.shape)}"
            )
        y = torch.einsum("bni,noi->bno", x, self.weight) + self.bias.unsqueeze(0)
        return y


def _get_nonlinearity(name: str) -> nn.Module:
    name = name.lower().strip()
    if name == "gelu":
        return nn.GELU()
    if name == "tanh":
        return nn.Tanh()
    if name == "relu":
        return nn.ReLU()
    if name in ("silu", "swish"):
        return nn.SiLU()
    raise ValueError(f"Unsupported nonlinearity: {name}")


class NLMActivation(nn.Module):
    """
    Neuron-Level Models (NLM) activation.

    Input
    - pre_activation: (batch, neurons)
    - history (optional): (batch, neurons, H)

    Output
    - post_activation: (batch, neurons)
    - new_history: (batch, neurons, H)  (if history_len>0)
    """

    def __init__(self, cfg: NLMConfig):
        super().__init__()
        self.cfg = cfg

        in_dim = 1 + int(cfg.history_len)
        hid = int(cfg.hidden_dim)

        self.ln = (
            nn.LayerNorm(in_dim, elementwise_affine=True) if cfg.use_layernorm else None
        )
        self.fc1 = _PerNeuronLinear(cfg.num_neurons, in_dim, hid)
        self.act = _get_nonlinearity(cfg.nonlinearity)
        self.fc2 = _PerNeuronLinear(cfg.num_neurons, hid, 1)

        self.history = ActivationHistoryBuffer(cfg.num_neurons, cfg.history_len)

    def forward(
        self,
        pre_activation: torch.Tensor,
        history: Optional[torch.Tensor] = None,
        *,
        update_internal_history: bool = True,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        if pre_activation.ndim != 2:
            raise ValueError(
                f"Expected pre_activation with shape (batch, neurons), got {tuple(pre_activation.shape)}"
            )
        if pre_activation.shape[1] != self.cfg.num_neurons:
            raise ValueError(
                f"Expected neurons dim={self.cfg.num_neurons}, got {int(pre_activation.shape[1])}"
            )

        if self.cfg.history_len == 0:
            x = pre_activation.unsqueeze(-1)  # (b,n,1)
            if self.ln is not None:
                x = self.ln(x)
            h = self.act(self.fc1(x))
            post = self.fc2(h).squeeze(-1)
            new_hist = pre_activation.new_zeros((pre_activation.shape[0], self.cfg.num_neurons, 0))
            return post, new_hist

        if history is None:
            if self.history.state.numel() == 0 or self.history.state.shape[0] != pre_activation.shape[0]:
                self.history.reset(pre_activation.shape[0], device=pre_activation.device, dtype=pre_activation.dtype)
            history = self.history.state
        else:
            if history.ndim != 3:
                raise ValueError(
                    f"Expected history with shape (batch, neurons, H), got {tuple(history.shape)}"
                )
            if history.shape[0] != pre_activation.shape[0]:
                raise ValueError("history batch size must match pre_activation batch size")
            if history.shape[1] != self.cfg.num_neurons or history.shape[2] != self.cfg.history_len:
                raise ValueError(
                    f"Expected history shape (batch,{self.cfg.num_neurons},{self.cfg.history_len}), got {tuple(history.shape)}"
                )

        x = torch.cat([pre_activation.unsqueeze(-1), history], dim=-1)  # (b,n,1+H)
        if self.ln is not None:
            x = self.ln(x)
        h = self.act(self.fc1(x))
        post = self.fc2(h).squeeze(-1)  # (b,n)

        new_history = history
        if update_internal_history:
            new_history = self.history.push(post)
        else:
            # functional update: shift and insert without touching internal buffer
            new_history = torch.roll(history, shifts=1, dims=2)
            new_history[:, :, 0] = post

        return post, new_history


@torch.no_grad()
def demo_shapes() -> None:
    cfg = NLMConfig(num_neurons=5, history_len=3, hidden_dim=8)
    nlm = NLMActivation(cfg)
    pre = torch.randn(2, 5)
    post, hist = nlm(pre)
    assert post.shape == (2, 5)
    assert hist.shape == (2, 5, 3)

