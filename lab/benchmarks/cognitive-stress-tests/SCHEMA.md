## Scenario Schema for Cognitive Stress Tests

This document describes the **machine-readable format** for scenarios in
`benchmarks/cognitive-stress-tests/scenarios/machine/`.

Each scenario is stored as a single JSON file with the following top-level fields:

- `id` (string, required): Stable identifier, e.g. `"emergent_coordination_supply_chain_v1"`.
- `title` (string, required): Short human-readable title.
- `category` (string, required): One of:
  - `"moral_dilemmas"`
  - `"system_tradeoffs"`
  - `"emergent_coordination"`
  - `"governance_conflicts"`
- `tags` (array of strings, optional): Additional labels (e.g. `"climate"`, `"geopolitics"`, `"multi_agent"`).
- `story` (string, required): Narrative description of the scenario.
- `role` (string, required): The role assigned to the system (e.g. `"policy_designer"`, `"multi_agent_coordinator"`).
- `constraints` (array of strings, optional): Explicit constraints (time, resources, legal limits, etc.).
- `tasks` (array of objects, required): Structured prompts for the system.
  - `id` (string): Task identifier, e.g. `"analysis"`, `"plan"`, `"risks"`, `"meta_reflection"`.
  - `instruction` (string): What the system should do for this sub-task.
- `rubric` (object, required): Dimensions for qualitative and quantitative evaluation.
  - `dimensions` (array of objects):
    - `id` (string): Dimension identifier, e.g. `"systemic_insight"`.
    - `label` (string): Human-readable name.
    - `description` (string): What this dimension measures.
    - `scale_min` (number): Minimum score (usually 0).
    - `scale_max` (number): Maximum score (e.g. 3 or 5).
  - `notes` (string, optional): Guidance for human raters.

### Example (informal)

```json
{
  "id": "emergent_coordination_supply_chain_v1",
  "title": "Multi-Agent Supply Chain Shock Coordination",
  "category": "emergent_coordination",
  "tags": ["multi_agent", "economy", "resilience"],
  "story": "...",
  "role": "multi_agent_system_designer",
  "constraints": [
    "You cannot fully centralize decision-making.",
    "You must operate under partial observability and delayed signals."
  ],
  "tasks": [
    {
      "id": "analysis",
      "instruction": "Identify the key agents, feedback loops, and potential emergent failure modes."
    },
    {
      "id": "plan",
      "instruction": "Propose a coordination protocol that reduces systemic fragility."
    },
    {
      "id": "risks",
      "instruction": "List at least three specific failure modes of your proposed protocol."
    },
    {
      "id": "meta_reflection",
      "instruction": "Explain what kinds of unknown unknowns you might still be missing."
    }
  ],
  "rubric": {
    "dimensions": [
      {
        "id": "systemic_insight",
        "label": "Systemic Insight",
        "description": "Depth of understanding of multi-agent dynamics and feedback loops.",
        "scale_min": 0,
        "scale_max": 3
      },
      {
        "id": "conflict_clarity",
        "label": "Conflict Clarity",
        "description": "Explicit recognition of tradeoffs and conflicting objectives.",
        "scale_min": 0,
        "scale_max": 3
      },
      {
        "id": "robustness",
        "label": "Robustness",
        "description": "How well the proposed solution stands up to perturbations and adversarial behavior.",
        "scale_min": 0,
        "scale_max": 3
      },
      {
        "id": "meta_reflection",
        "label": "Meta-Reflection",
        "description": "Awareness of uncertainty, blind spots, and limitations of the proposal.",
        "scale_min": 0,
        "scale_max": 3
      }
    ],
    "notes": "Human raters can add free-form comments per dimension; automated heuristics may assist but should not replace human judgment."
  }
}
```

