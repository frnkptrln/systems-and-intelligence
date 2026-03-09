from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Protocol
import json


BASE_DIR = Path(__file__).resolve().parents[1]
SCENARIO_DIR = BASE_DIR / "scenarios" / "machine"


@dataclass
class RubricDimension:
  id: str
  label: str
  description: str
  scale_min: float
  scale_max: float


@dataclass
class Rubric:
  dimensions: List[RubricDimension]
  notes: str | None = None


@dataclass
class Task:
  id: str
  instruction: str


@dataclass
class Scenario:
  id: str
  title: str
  category: str
  story: str
  role: str
  tasks: List[Task]
  constraints: List[str]
  tags: List[str]
  rubric: Rubric


@dataclass
class TaskResponse:
  task_id: str
  content: str


@dataclass
class ScenarioResponse:
  scenario_id: str
  responses: List[TaskResponse]
  metadata: Dict[str, Any] | None = None


@dataclass
class DimensionScore:
  dimension_id: str
  score: float
  comment: str | None = None


@dataclass
class ScenarioScore:
  scenario_id: str
  scores: List[DimensionScore]
  rater_id: str | None = None
  metadata: Dict[str, Any] | None = None


class CognitiveSystem(Protocol):
  """Protocol for systems that can answer a cognitive stress scenario."""

  def __call__(self, scenario: Scenario) -> ScenarioResponse:  # pragma: no cover - protocol definition
    ...


def load_scenario(scenario_id: str) -> Scenario:
  """Load a machine-readable scenario by id."""
  path = SCENARIO_DIR / f"{scenario_id}.json"
  if not path.exists():
    raise FileNotFoundError(f"Scenario not found: {path}")

  with path.open("r", encoding="utf-8") as f:
    data = json.load(f)

  rubric_dims = [
    RubricDimension(
      id=d["id"],
      label=d["label"],
      description=d["description"],
      scale_min=d["scale_min"],
      scale_max=d["scale_max"],
    )
    for d in data["rubric"]["dimensions"]
  ]

  rubric = Rubric(
    dimensions=rubric_dims,
    notes=data["rubric"].get("notes"),
  )

  tasks = [Task(id=t["id"], instruction=t["instruction"]) for t in data["tasks"]]

  return Scenario(
    id=data["id"],
    title=data["title"],
    category=data["category"],
    story=data["story"],
    role=data["role"],
    tasks=tasks,
    constraints=data.get("constraints", []),
    tags=data.get("tags", []),
    rubric=rubric,
  )


def run_system_on_scenario(
  system: CognitiveSystem,
  scenario: Scenario,
) -> ScenarioResponse:
  """Run a cognitive system on a scenario.

  This is intentionally thin; orchestration (e.g. prompting an LLM, running
  an interactive simulation) should be implemented in higher-level wrappers.
  """
  return system(scenario)


def score_response(
  response: ScenarioResponse,
  rubric: Rubric,
  scoring_fn: Callable[[ScenarioResponse, Rubric], List[DimensionScore]],
) -> ScenarioScore:
  """Apply a scoring function to a scenario response.

  The scoring function can be implemented by human raters (e.g. UI layer)
  or by meta-evaluator models; this module only defines the data plumbing.
  """
  scores = scoring_fn(response, rubric)
  return ScenarioScore(
    scenario_id=response.scenario_id,
    scores=scores,
  )

