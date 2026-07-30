"""Exact toy benchmark for capability under situated stack changes.

The controller is identical in every arm.  Only the sensor, actuator, body
constraint, environment, or goal interface changes.  The benchmark is small
enough to enumerate every declared task and compare several observer lenses
without sampling error.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Iterable


MIN_POSITION = -2
MAX_POSITION = 2
MAX_STEPS = 4
TASKS = tuple(
    (start, target)
    for target in (-1, 0, 1)
    for start in range(MIN_POSITION, MAX_POSITION + 1)
    if start != target
)


@dataclass(frozen=True)
class Stack:
    """A declared controller coupling.

    ``controller`` is intentionally absent: every stack calls the same global
    controller function below.
    """

    name: str
    sensor: str = "canonical"
    actuator: str = "canonical"
    body: str = "bidirectional"
    environment: str = "open-line"
    goal_interface: str = "identity"


@dataclass(frozen=True)
class Episode:
    start: int
    target: int
    final_position: int
    positions: tuple[int, ...]
    actions: tuple[str, ...]
    success: bool


STACKS = (
    Stack("canonical"),
    Stack("coordinated-mirror", sensor="mirrored", actuator="mirrored"),
    Stack("sensor-mismatch", sensor="mirrored"),
    Stack("actuator-mismatch", actuator="mirrored"),
    Stack("coarse-sensor", sensor="coarse"),
    Stack("right-only-body", body="right-only"),
    Stack("barrier-world", environment="barrier-at-zero"),
    Stack("goal-mirror", goal_interface="mirrored"),
    Stack("immobile-body", body="immobile"),
)


def controller(observation: str) -> str:
    """The single controller used by every benchmark arm."""

    return {
        "left": "step-left",
        "at": "stay",
        "right": "step-right",
    }[observation]


def map_goal(target: int, interface: str) -> int:
    if interface == "identity":
        return target
    if interface == "mirrored":
        return -target
    raise ValueError(f"unknown goal interface: {interface}")


def observe(position: int, target: int, sensor: str) -> str:
    if position == target:
        canonical = "at"
    elif position < target:
        canonical = "right"
    else:
        canonical = "left"

    if sensor == "canonical":
        return canonical
    if sensor == "mirrored":
        return {"left": "right", "at": "at", "right": "left"}[canonical]
    if sensor == "coarse":
        return "at" if canonical == "at" else "right"
    raise ValueError(f"unknown sensor: {sensor}")


def actuate(action: str, actuator: str) -> int:
    canonical = {"step-left": -1, "stay": 0, "step-right": 1}[action]
    if actuator == "canonical":
        return canonical
    if actuator == "mirrored":
        return -canonical
    raise ValueError(f"unknown actuator: {actuator}")


def apply_body_constraint(delta: int, body: str) -> int:
    if body == "bidirectional":
        return delta
    if body == "right-only":
        return max(delta, 0)
    if body == "immobile":
        return 0
    raise ValueError(f"unknown body: {body}")


def transition(position: int, delta: int, environment: str) -> int:
    proposed = min(MAX_POSITION, max(MIN_POSITION, position + delta))
    if environment == "open-line":
        return proposed
    if environment == "barrier-at-zero":
        crosses_barrier = (position < 0 <= proposed) or (proposed < 0 <= position)
        return position if crosses_barrier else proposed
    raise ValueError(f"unknown environment: {environment}")


def run_episode(
    stack: Stack,
    start: int,
    target: int,
    *,
    max_steps: int = MAX_STEPS,
) -> Episode:
    """Run one task and evaluate it against the external task target."""

    position = start
    positions = [position]
    actions: list[str] = []
    internal_target = map_goal(target, stack.goal_interface)

    for _ in range(max_steps):
        observation = observe(position, internal_target, stack.sensor)
        action = controller(observation)
        actions.append(action)
        if action == "stay":
            break
        delta = apply_body_constraint(actuate(action, stack.actuator), stack.body)
        position = transition(position, delta, stack.environment)
        positions.append(position)

    return Episode(
        start=start,
        target=target,
        final_position=position,
        positions=tuple(positions),
        actions=tuple(actions),
        success=position == target,
    )


def run_stack(stack: Stack, tasks: Iterable[tuple[int, int]] = TASKS) -> tuple[Episode, ...]:
    return tuple(run_episode(stack, start, target) for start, target in tasks)


def success_profile(episodes: tuple[Episode, ...]) -> tuple[bool, ...]:
    return tuple(episode.success for episode in episodes)


def world_trace_profile(episodes: tuple[Episode, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(episode.positions for episode in episodes)


def token_trace_profile(episodes: tuple[Episode, ...]) -> tuple[tuple[str, ...], ...]:
    return tuple(episode.actions for episode in episodes)


def success_rate(episodes: tuple[Episode, ...]) -> float:
    return mean(episode.success for episode in episodes)


def compare(left: Stack, right: Stack) -> dict[str, bool]:
    """Compare two stacks under four declared observer lenses."""

    left_episodes = run_stack(left)
    right_episodes = run_stack(right)
    return {
        "aggregate score": success_rate(left_episodes) == success_rate(right_episodes),
        "task-success profile": success_profile(left_episodes)
        == success_profile(right_episodes),
        "physical traces": world_trace_profile(left_episodes)
        == world_trace_profile(right_episodes),
        "controller-token traces": token_trace_profile(left_episodes)
        == token_trace_profile(right_episodes),
    }


def stack_by_name(name: str) -> Stack:
    return next(stack for stack in STACKS if stack.name == name)


def render_report() -> str:
    lines = [
        "| stack | successes | tasks | success rate |",
        "|:---|---:|---:|---:|",
    ]
    for stack in STACKS:
        episodes = run_stack(stack)
        successes = sum(episode.success for episode in episodes)
        lines.append(
            f"| `{stack.name}` | {successes} | {len(episodes)} | "
            f"{success_rate(episodes):.3f} |"
        )

    lines.extend(
        [
            "",
            "| comparison | aggregate | task profile | physical traces | token traces |",
            "|:---|:---:|:---:|:---:|:---:|",
        ]
    )
    for left_name, right_name in (
        ("canonical", "coordinated-mirror"),
        ("coarse-sensor", "right-only-body"),
    ):
        result = compare(stack_by_name(left_name), stack_by_name(right_name))
        marks = ["yes" if value else "no" for value in result.values()]
        lines.append(
            f"| `{left_name}` vs. `{right_name}` | "
            + " | ".join(marks)
            + " |"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    print(render_report())
