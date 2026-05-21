"""
Anthropic provider — calls the real Anthropic API.

Uses the standard library (`urllib`) so no new dependency is added to the
project. The Anthropic Python SDK is **not** required for this provider to
work; it speaks HTTP/JSON directly.

Behavior:

- `complete()` calls `POST /v1/messages` with the configured model.
- `embed()` falls back to the same deterministic hash-based embedding the
  mock provider uses. Anthropic does not currently expose a public
  embeddings endpoint; the suite's embedding-based metrics (Δ-Kohärenz,
  self-representation) therefore use the mock embedder regardless of
  completion provider. This is documented and intentional. When a real
  embedding service is added, subclass this provider and override
  `embed()`.

Real mode requires the `ANTHROPIC_API_KEY` environment variable. The
provider raises a clear error at construction time if the variable is
missing — fail-fast over silent misconfiguration.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

import numpy as np

from .base import LLMProvider
from .mock_provider import MockProvider


DEFAULT_ENDPOINT = "https://api.anthropic.com/v1/messages"
DEFAULT_API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-4-20250514"
DEFAULT_MAX_TOKENS = 1024
DEFAULT_TIMEOUT = 60


class AnthropicProvider(LLMProvider):
    """Calls the Anthropic Messages API. Real mode."""

    def __init__(
        self,
        api_key: str | None = None,
        api_key_env: str = "ANTHROPIC_API_KEY",
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = 1.0,
        endpoint: str = DEFAULT_ENDPOINT,
        api_version: str = DEFAULT_API_VERSION,
        timeout_seconds: int = DEFAULT_TIMEOUT,
        embedding_dim: int = 384,
    ):
        key = api_key if api_key is not None else os.environ.get(api_key_env)
        if not key:
            raise RuntimeError(
                f"AnthropicProvider requires an API key. "
                f"Set {api_key_env} in the environment, or pass api_key explicitly."
            )
        self._api_key = key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.endpoint = endpoint
        self.api_version = api_version
        self.timeout_seconds = timeout_seconds

        # Reuse the mock embedder for `embed()`. See module docstring.
        self._fallback_embedder = MockProvider(embedding_dim=embedding_dim)

    @property
    def name(self) -> str:
        return "anthropic"

    def complete(self, prompt: str, system: str | None = None) -> str:
        body: dict = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system is not None:
            body["system"] = system

        data = json.dumps(body).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint,
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "x-api-key": self._api_key,
                "anthropic-version": self.api_version,
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace") if e.fp else ""
            raise RuntimeError(
                f"Anthropic API error {e.code}: {e.reason}. Response: {detail}"
            ) from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Anthropic API request failed: {e.reason}") from e

        # The Messages API returns content as a list of blocks. Concatenate
        # text blocks; ignore tool-use or other block types for now.
        blocks = payload.get("content", [])
        parts = [b.get("text", "") for b in blocks if b.get("type") == "text"]
        return "".join(parts)

    def embed(self, text: str) -> np.ndarray:
        # See module docstring: Anthropic does not currently expose
        # embeddings, so we fall back to the deterministic mock embedder.
        # Override in a subclass when a real embedding service is added.
        return self._fallback_embedder.embed(text)
