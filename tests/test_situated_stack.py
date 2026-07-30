"""Regression tests for the exact situated-stack benchmark."""

import importlib.util
from pathlib import Path
import sys


REPO = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    REPO / "lab" / "benchmarks" / "situated-stack" / "situated_stack.py"
)
SPEC = importlib.util.spec_from_file_location("situated_stack", MODULE_PATH)
assert SPEC and SPEC.loader
ss = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ss
SPEC.loader.exec_module(ss)


def test_exact_success_counts():
    expected = {
        "canonical": 12,
        "coordinated-mirror": 12,
        "sensor-mismatch": 0,
        "actuator-mismatch": 0,
        "coarse-sensor": 6,
        "right-only-body": 6,
        "barrier-world": 5,
        "goal-mirror": 4,
        "immobile-body": 0,
    }
    measured = {
        stack.name: sum(episode.success for episode in ss.run_stack(stack))
        for stack in ss.STACKS
    }
    assert measured == expected


def test_coordinated_mirror_preserves_world_behavior_but_not_tokens():
    result = ss.compare(
        ss.stack_by_name("canonical"),
        ss.stack_by_name("coordinated-mirror"),
    )
    assert result == {
        "aggregate score": True,
        "task-success profile": True,
        "physical traces": True,
        "controller-token traces": False,
    }


def test_equal_task_profiles_can_hide_different_failure_dynamics():
    result = ss.compare(
        ss.stack_by_name("coarse-sensor"),
        ss.stack_by_name("right-only-body"),
    )
    assert result == {
        "aggregate score": True,
        "task-success profile": True,
        "physical traces": False,
        "controller-token traces": False,
    }
