"""Tests for the real Anthropic provider that never make network calls."""

import json
import os
import sys
from unittest.mock import patch


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


def test_completion_exposes_usage_and_response_metadata():
    class FakeResponse:
        headers = {"request-id": "req_test"}

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def read(self):
            return json.dumps(
                {
                    "content": [{"type": "text", "text": "answer"}],
                    "usage": {"input_tokens": 3, "output_tokens": 1},
                    "stop_reason": "end_turn",
                }
            ).encode("utf-8")

    provider = AnthropicProvider(api_key="test-key")
    with patch(
        "lab.providers.anthropic_provider.urllib.request.urlopen",
        return_value=FakeResponse(),
    ):
        reply = provider.complete("prompt")

    assert reply == "answer"
    assert provider.last_usage == {"input_tokens": 3, "output_tokens": 1}
    assert provider.last_stop_reason == "end_turn"
    assert provider.last_request_id == "req_test"
