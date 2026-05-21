# Providers — Mock and Real

Scaffolding for the Agentic Identity Suite's eventual switch from mock to real LLM runs. This is **infrastructure**, not a live experiment. The existing experiments still use the agents' built-in mock embeddings by design.

## What's here

- `base.py` — Abstract `LLMProvider` interface. Every provider implements `complete(prompt, system=None)` and `embed(text)`.
- `mock_provider.py` — Default. Deterministic, fast, no API key required.
- `anthropic_provider.py` — Real mode. Calls `POST /v1/messages` via `urllib` (no new dependency). Default model: `claude-sonnet-4-20250514`.
- `factory.py` — `load_config()` and `get_provider(cfg)`. Mock is the default; setting `llm.provider: anthropic` switches to real mode.

## Why this layer exists

The Mirror Problem (see [Open Problem 1](../../theory/reference/open-problems.md#open-problem-1-the-mirror-problem)) and Claim 9 of [Emergence Manifesto v1.3](../../theory/core/emergence-manifesto-v1.3.md) need empirical validation with real language models. The mock embeddings used by `lab/agents/three_layer_agent.py` and `lab/agents/baseline_mirror_agent.py` are sufficient for unit-testing the suite's architecture, but not sufficient for the inverse-direction questions the project is structured around — see [The Generator Question](../../theory/core/the-generator-question.md) for the spine.

This provider layer is the seam between the suite's mock-based architecture and its future empirical work. Nothing in the existing experiments has been changed; the suite still runs in mock mode by default.

## Running real mode

1. Set the API key:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   ```
2. Edit `lab/config.yaml`:
   ```yaml
   llm:
     provider: anthropic
   ```
3. Wire the provider into whichever experiment will be updated. The agents are not currently wired through the provider — that is a deliberate next step to be done when Frank decides to take it.

## Embeddings note

The Anthropic API does not currently expose a public embeddings endpoint. `AnthropicProvider.embed()` therefore falls back to the same deterministic hash-based embedding the mock provider uses. The Δ-Kohärenz metric and self-representations work uniformly across providers. When a real embedding service is added (sentence-transformers, OpenAI embeddings, Cohere, etc.), subclass `AnthropicProvider` and override `embed()`. No caller will need to change.

## Status

- `[DEMONSTRATED]` — Mock provider runs deterministically; covered by the existing suite.
- `[INFRASTRUCTURE READY]` — Real-mode HTTP path is implemented and import-clean. Not yet wired into the existing experiments.
- `[OPEN PROBLEM]` — Whether real-mode Δ-Kohärenz separates trace-memorizers from generator-approximators at statistically significant levels.
