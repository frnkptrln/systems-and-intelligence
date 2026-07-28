"""
lab.providers
=============

LLM provider abstraction for the Agentic Identity Suite.

Mock mode (the default) is deterministic, fast, and requires no network or
API key. Real mode calls the Anthropic API. The default model for empirical
runs is `claude-sonnet-5`, configurable via `lab/config.yaml`.

This module is infrastructure. The existing experiments still use the
agents' built-in mock embeddings by design — see the Emergence Manifesto
(v1.3) and the Mirror Problem documentation for the empirical roadmap.
Switching the experiments to real mode is a separate piece of work; the
scaffolding is here so that step is straightforward when Frank decides to
take it.

Usage::

    from lab.providers import load_config, get_provider
    cfg = load_config()
    provider = get_provider(cfg)
    text = provider.complete("Hello")
    vec  = provider.embed("Hello")
"""

from .base import LLMProvider
from .mock_provider import MockProvider
from .anthropic_provider import AnthropicProvider


def load_config(path=None):
    """Load provider configuration without importing PyYAML on package import."""
    from .factory import load_config as _load_config

    return _load_config(path)


def get_provider(cfg=None):
    """Construct the configured provider."""
    from .factory import get_provider as _get_provider

    return _get_provider(cfg)

__all__ = [
    "LLMProvider",
    "MockProvider",
    "AnthropicProvider",
    "load_config",
    "get_provider",
]
