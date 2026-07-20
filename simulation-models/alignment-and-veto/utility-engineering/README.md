# Utility Engineering: Preference-Consistency Scaffold

**Status:** Mock simulation and experimental scaffold. No live API integration or validated model
audit is currently included.

The module asks a bounded question: given a set of pairwise responses, how transitive is the
resulting directed preference graph? A transitivity score describes those elicited responses under
that protocol. It does not reveal a unique internal utility function, stable goals, self-preservation
drive, or future autonomous behavior.

## Components

1. [THEORY.md](THEORY.md) — earlier systems-theoretic interpretation; read as a hypothesis.
2. [utility_engineering_framework.md](utility_engineering_framework.md) — proposed measurement
   framework.
3. [graph_engine.py](graph_engine.py) — directed-graph transitivity and the proposed Coherence Score.
4. [api_triad_generator.py](api_triad_generator.py) — dilemma generation with a hard-coded mock
   responder. Despite the historical filename, live API calls are not implemented.
5. [utility_monitor.py](utility_monitor.py) — conceptual drift simulation, not access to model
   internals.
6. [citizen_assembly.py](citizen_assembly.py) — governance toy model.

## What would make this empirical

A real-model study would need:

- an implemented and version-pinned provider;
- stored prompts, raw responses, parameters, timestamps, and model identifiers;
- randomized presentation order and repeated samples;
- controls for refusal, framing, position bias, and context;
- held-out tests of whether the score predicts later choices;
- a clear separation between response consistency and claims about latent preferences.

The [March 2026 note](empirical-results/chatgpt-vs-claude-audit.md) records an informal manual
prompting episode without the material needed for independent reproduction. It is retained as
research history, not as empirical validation.

## Run the current artifacts

- python3 graph_engine.py
- python3 utility_monitor.py
- python3 citizen_assembly.py
- python3 api_triad_generator.py

The final command uses the mock responder. Selecting its non-mock branch currently prints
“Real API call not implemented yet” and returns no observations.
