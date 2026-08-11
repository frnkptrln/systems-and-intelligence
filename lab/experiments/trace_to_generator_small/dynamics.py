"""Bounded one-dimensional generator families used by the synthetic dataset."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np


@dataclass(frozen=True)
class GeneratorFamily:
    """One declared process family with a single normalized parameter."""

    name: str
    parameter_name: str
    parameter_min: float
    parameter_max: float
    equation: str

    def to_dict(self) -> dict[str, str | float]:
        return asdict(self)


FAMILIES = (
    GeneratorFamily(
        "logistic",
        "r",
        2.8,
        4.0,
        "x[t+1] = r*x[t]*(1-x[t]) + u[t]",
    ),
    GeneratorFamily(
        "tent",
        "mu",
        1.1,
        2.0,
        "x[t+1] = mu*min(x[t],1-x[t]) + u[t]",
    ),
    GeneratorFamily(
        "sine",
        "a",
        0.7,
        1.0,
        "x[t+1] = a*sin(pi*x[t]) + u[t]",
    ),
    GeneratorFamily(
        "cubic",
        "c",
        1.4,
        2.5,
        "x[t+1] = c*x[t]*(1-x[t]^2) + u[t]",
    ),
)


def family_index(name: str) -> int:
    for index, family in enumerate(FAMILIES):
        if family.name == name:
            return index
    raise ValueError(f"unknown generator family: {name}")


def normalize_parameter(family_id: int, parameter: float) -> float:
    family = FAMILIES[family_id]
    return (parameter - family.parameter_min) / (
        family.parameter_max - family.parameter_min
    )


def denormalize_parameter(family_id: int, normalized: float) -> float:
    family = FAMILIES[family_id]
    return family.parameter_min + normalized * (
        family.parameter_max - family.parameter_min
    )


def transition(
    family_id: int,
    state: float | np.ndarray,
    parameter: float,
    control: float | np.ndarray = 0.0,
) -> float | np.ndarray:
    """Apply one controlled transition and clip the observable state to [0, 1]."""
    family = FAMILIES[family_id]
    if not family.parameter_min <= parameter <= family.parameter_max:
        raise ValueError(
            f"parameter {parameter} outside {family.name} range "
            f"[{family.parameter_min}, {family.parameter_max}]"
        )
    x = np.asarray(state, dtype=np.float64)
    if np.any((x < 0.0) | (x > 1.0)):
        raise ValueError("state must lie in [0, 1]")

    if family.name == "logistic":
        next_state = parameter * x * (1.0 - x)
    elif family.name == "tent":
        next_state = parameter * np.minimum(x, 1.0 - x)
    elif family.name == "sine":
        next_state = parameter * np.sin(np.pi * x)
    else:
        next_state = parameter * x * (1.0 - x**2)

    result = np.clip(next_state + np.asarray(control), 0.0, 1.0)
    if result.ndim == 0:
        return float(result)
    return result
