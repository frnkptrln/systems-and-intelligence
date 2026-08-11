# Providers — Mock and Real

**Status:** Infrastructure documentation, not a live experiment.  
**External interface last reviewed:** 2026-08-08  
**Review trigger:** Anthropic changes the default target model, Messages API contract, sampling behavior, or first-party embedding support.

Scaffolding for the Agentic Identity Suite's eventual switch from mock to real LLM runs. The
existing experiments still use the agents' built-in mock embeddings by design.

## What's here

- `base.py` — Abstract `LLMProvider` interface. Every provider implements `complete(prompt, system=None)` and `embed(text)`.
- `mock_provider.py` — Default. Deterministic, fast, no API key required.
- `anthropic_provider.py` — Real mode. Calls `POST /v1/messages` via `urllib` (no new dependency). Repository default model: `claude-sonnet-5`.
- `factory.py` — `load_config()` and `get_provider(cfg)`. Mock is the default; setting `llm.provider: anthropic` switches to real mode.

## Why this layer exists

The Mirror Problem (see [Open Problem
1](../../theory/reference/open-problems.md#open-problem-1-the-mirror-problem)) needs
empirical validation with real language models. The mock embeddings used by
`lab/agents/three_layer_agent.py` and `lab/agents/baseline_mirror_agent.py` are
sufficient for unit-testing the suite's architecture, but not for claims about real-model
identity. See the [Foundations
Reconstruction](../../theory/core/mathematical-axioms.md) for the current scope.

This provider layer is the seam between the suite's mock-based architecture and its future empirical
work. Nothing in the existing experiments has been changed; the suite still runs in mock mode by
default.

## Running real mode

1. Set the API key:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   ```
2. Edit `lab/config.yaml`:
   ```yaml
   llm:
     provider: anthropic
     anthropic:
       model: claude-sonnet-5
   ```
3. Wire the provider into whichever experiment will be updated. The agents are not yet routed
   through the provider; that remains an explicit empirical step rather than an implied capability.

### Sampling behavior of the repository default

As checked against Anthropic's Claude Platform documentation on 2026-08-08, **Claude Sonnet 5**
rejects non-default `temperature`, `top_p`, and `top_k` values. The provider therefore omits all
three. This statement is scoped to the configured model/API behavior rather than generalized to
"current Claude models," because older supported model families can have different compatibility
rules.

Experiments that need behavioral variance should either use an explicitly supported mechanism or
elicit variation through a recorded protocol. In either case, the exact model ID and request
configuration belong in the experiment artifact.

## Embeddings note

As checked on 2026-08-08, Anthropic's own platform documentation states that Anthropic does not
offer a first-party embedding model and points users to external embedding providers such as Voyage
AI. `AnthropicProvider.embed()` therefore falls back to the same deterministic hash-based embedding
the mock provider uses.

That fallback keeps the interface uniform, but it is **not a real-model embedding measurement**.
Any experiment claiming semantic geometry of a production model must replace the fallback with a
declared embedding provider and record that provider/model as part of the measurement apparatus.

## Status

- `[DEMONSTRATED]` — Mock provider runs deterministically; covered by the existing suite.
- `[INFRASTRUCTURE READY]` — Real-mode Messages API path is implemented and import-clean. Not yet wired into the existing experiments.
- `[MEASUREMENT LIMIT]` — `embed()` remains a deterministic fallback and must not be described as an Anthropic embedding.
- `[OPEN PROBLEM]` — Whether real-mode identity/coherence instruments separate trace-memorizers from generator-approximators under a preregistered protocol.
