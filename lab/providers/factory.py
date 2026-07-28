"""
Factory and config loader for the provider abstraction.

Two entry points:

- `load_config(path=None)` — reads `lab/config.yaml`. Returns a dict.
- `get_provider(cfg)` — returns an `LLMProvider` based on `cfg['llm']['provider']`.

Mock mode is the default. Anthropic mode requires the API key environment
variable to be set; if it is missing, `get_provider` raises rather than
silently falling back to mock.

The legacy `USE_MOCK_LLM` top-level flag is honored for backward
compatibility with the existing experiments: if it is set to `true` and no
explicit `llm.provider` is specified, the mock provider is returned.
"""

from __future__ import annotations

import os
from pathlib import Path

import yaml

from .anthropic_provider import (
    DEFAULT_API_VERSION,
    DEFAULT_ENDPOINT,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_TIMEOUT,
    AnthropicProvider,
)
from .base import LLMProvider
from .mock_provider import MockProvider


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


def load_config(path: str | os.PathLike | None = None) -> dict:
    """Read the suite's config.yaml. Path defaults to lab/config.yaml."""
    p = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_provider(cfg: dict | None = None) -> LLMProvider:
    """
    Return an LLMProvider instance based on the loaded config.

    Resolution order:
      1. cfg['llm']['provider'] if present.
      2. 'mock' if cfg['USE_MOCK_LLM'] is true (legacy flag).
      3. 'mock' as the default.
    """
    if cfg is None:
        cfg = load_config()

    llm_cfg = cfg.get("llm", {}) or {}
    provider_name = llm_cfg.get("provider")

    if provider_name is None:
        provider_name = "mock" if cfg.get("USE_MOCK_LLM", True) else "anthropic"

    provider_name = provider_name.lower()

    if provider_name == "mock":
        return MockProvider()

    if provider_name == "anthropic":
        a = llm_cfg.get("anthropic", {}) or {}
        return AnthropicProvider(
            api_key_env=a.get("api_key_env", "ANTHROPIC_API_KEY"),
            model=a.get("model", DEFAULT_MODEL),
            max_tokens=a.get("max_tokens", DEFAULT_MAX_TOKENS),
            endpoint=a.get("endpoint", DEFAULT_ENDPOINT),
            api_version=a.get("api_version", DEFAULT_API_VERSION),
            timeout_seconds=a.get("timeout_seconds", DEFAULT_TIMEOUT),
        )

    raise ValueError(
        f"Unknown LLM provider: {provider_name!r}. "
        "Valid choices: 'mock', 'anthropic'."
    )
