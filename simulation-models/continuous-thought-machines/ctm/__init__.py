"""
Continuous Thought Machines (CTM)

This package is intentionally lightweight and self-contained so it can be used
from standalone simulation scripts inside `simulation-models/`.
"""

from .nlm import (
    NLMConfig,
    NLMActivation,
    ActivationHistoryBuffer,
)

__all__ = [
    "NLMConfig",
    "NLMActivation",
    "ActivationHistoryBuffer",
]

