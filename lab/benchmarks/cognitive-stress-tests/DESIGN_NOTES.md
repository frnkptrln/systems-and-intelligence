## Design Notes: Cognitive Stress Tests

This benchmark is intended as a **tool for epistemic humility**, not a leaderboard.

### What we are trying to measure

- **Systemic thinking**: Ability to track feedback loops, second-order effects, and multi-agent dynamics.
- **Conflict awareness**: Seeing and naming conflicts between values, objectives, and constraints.
- **Robustness of reasoning**: Proposing solutions that do not collapse under small perturbations.
- **Meta-cognition**: Explicit reflection on uncertainty, blind spots, and failure modes of one's own reasoning.

### What we are *not* trying to measure

- Raw knowledge of specific facts or laws.
- Surface-level eloquence or verbosity.
- Fine-grained numerical prediction accuracy.

The same scenario should be usable for:

- **Humans** (e.g. workshops, teaching, decision-support training),
- **LLMs and agents** (prompted via API),
- **Simulation-based systems** (e.g. agent-based models whose outcomes are summarized in text).

### Evaluation philosophy

- **Human judgment is central.** Automated heuristics can assist (e.g. checking whether key elements are mentioned), but the core scores are given by human raters using the rubric.
- **Disagreement is data.** Divergent ratings can hint at ambiguous scenarios or hidden assumptions; they should be recorded rather than suppressed.
- **Iterate on scenarios.** If a scenario turns out to be systematically confusing or non-discriminative, it should be revised or retired.

### Open questions

- How to best combine human ratings with model-based meta-evaluation without collapsing to the model's biases.
- How to benchmark **trajectories of reasoning** (multi-step interaction) instead of single-shot answers.
- How to connect scenario performance to concrete downstream risks in real systems.

