"""A small learned trace-to-generator system-identification model."""

from .data import DataConfig, generate_sample
from .dynamics import FAMILIES, transition

__all__ = ["FAMILIES", "DataConfig", "generate_sample", "transition"]
