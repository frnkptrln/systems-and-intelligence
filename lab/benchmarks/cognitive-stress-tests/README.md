## Cognitive Stress Tests for AI Systems

This module contains a benchmark for **systemic thinking under stress** – for humans, language models, and multi-agent systems.

Instead of testing local task performance, these scenarios probe:

- **Moral dilemmas**: conflicting norms, incomplete rules, uncertainty.
- **System tradeoffs**: safety vs. capabilities vs. speed, centralization vs. decentralization.
- **Emergent coordination**: multi-agent dynamics, feedback loops, coordination failures.
- **Governance conflicts**: misaligned regulatory layers, internal vs. external governance.

Each scenario asks systems to:

- **Analyse** the situation and key actors.
- **Propose decisions or policies** under constraints.
- **Anticipate side-effects and failure modes**.
- **Reflect on uncertainty and limitations** of the proposed solution.

### Repository structure

- `SCHEMA.md` – Specification of the machine-readable scenario format.
- `DESIGN_NOTES.md` – Methodological choices, limitations, open questions.
- `scenarios/`
  - `human-readable/` – Narrative Markdown formulations for humans.
  - `machine/` – JSON/YAML versions for programmatic evaluation.
- `evaluation/`
  - `api.py` – Thin interface for loading scenarios, running a system, and recording scores.

The goal is to keep the **scenario and rubric definitions separate from any particular model**, so that:

- humans, LLMs, and complex simulation-based systems can all be evaluated on the same cognitive stress tests, and
- the benchmark can evolve over time as we discover new kinds of systemic failure modes.

