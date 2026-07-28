"""Tests for the real Anthropic provider that never make network calls."""

import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lab.providers.anthropic_provider import AnthropicProvider, DEFAULT_MODEL


def test_request_body_has_no_sampling_parameters():
    provider = AnthropicProvider(api_key="test-key")

    body = provider._build_request_body("Give one exact answer.", system="Be terse.")

    assert body == {
        "model": DEFAULT_MODEL,
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": "Give one exact answer."}],
        "system": "Be terse.",
    }
    assert {"temperature", "top_p", "top_k"}.isdisjoint(body)
