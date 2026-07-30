"""Exact toy benchmark for constraint exposure versus lens reinterpretation.

The benchmark keeps a seeded transition substrate and a fixed policy constant
while changing either one constraint bit or one observer-lens rule.  A fourth
arm edits the transition generator as a control.  The state labels are
permuted by the seed; the measured relations are invariant to that relabeling.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import random
from statistics import mean
from typing import Iterable


DEFAULT_SEED = 26
ACTION = "advance"
LATENT_EDGE = "latent-leg"
HORIZON = 4


@dataclass(frozen=True)
class Transition:
    """One named transition in the fixed substrate."""

    edge_id: str
    source: int
    action: str
    target: int


@dataclass(frozen=True)
class Substrate:
    """A transition generator with opaque, seed-permuted state labels."""

    seed: int
    start: int
    staging: int
    gate: int
    goal: int
    transitions: tuple[Transition, ...]

    def step(self, state: int, action: str) -> Transition | None:
        return next(
            (
                transition
                for transition in self.transitions
                if transition.source == state and transition.action == action
            ),
            None,
        )


@dataclass(frozen=True)
class ConstraintSet:
    """Named transition edges that are unavailable."""

    blocked_edges: frozenset[str]


@dataclass(frozen=True)
class Episode:
    """One fixed-policy trace."""

    start: int
    goal: int
    states: tuple[int, ...]

    @property
    def terminal(self) -> int:
        return self.states[-1]

    @property
    def physical_success(self) -> bool:
        return self.terminal == self.goal


@dataclass(frozen=True)
class ArmResult:
    """Summary of one intervention arm."""

    arm: str
    seed: int
    generator_changed: bool
    constraint_edits: int
    lens_edits: int
    physical_success: float
    observed_competence: float
    trace_changed: bool
    classification: str
    traces: tuple[tuple[int, ...], ...]


def make_substrate(seed: int = DEFAULT_SEED) -> Substrate:
    """Construct the same four-state path under a seeded label permutation."""

    labels = [101, 211, 307, 419]
    random.Random(seed).shuffle(labels)
    start, staging, gate, goal = labels
    transitions = (
        Transition("approach", start, ACTION, staging),
        Transition("reach-gate", staging, ACTION, gate),
        Transition(LATENT_EDGE, gate, ACTION, goal),
    )
    return Substrate(seed, start, staging, gate, goal, transitions)


def make_edited_substrate(reference: Substrate) -> Substrate:
    """Return a generator-edit control that jumps to the goal.

    Its edges have new identities, so the reference constraint does not merely
    release the original latent edge.  This arm is deliberately outside the
    latent-competence definition used by the benchmark.
    """

    starts = (reference.start, reference.staging, reference.gate)
    transitions = tuple(
        Transition(f"edited-shortcut-{index}", state, ACTION, reference.goal)
        for index, state in enumerate(starts)
    )
    return Substrate(
        reference.seed,
        reference.start,
        reference.staging,
        reference.gate,
        reference.goal,
        transitions,
    )


def fixed_policy(_state: int) -> str:
    """The policy used in every arm."""

    return ACTION


def run_episode(
    substrate: Substrate,
    constraints: ConstraintSet,
    start: int,
    *,
    horizon: int = HORIZON,
) -> Episode:
    """Execute the fixed policy; a blocked or missing edge leaves state fixed."""

    state = start
    states = [state]
    for _ in range(horizon):
        transition = substrate.step(state, fixed_policy(state))
        if transition is None or transition.edge_id in constraints.blocked_edges:
            states.append(state)
            break
        state = transition.target
        states.append(state)
        if state == substrate.goal:
            break
    return Episode(start=start, goal=substrate.goal, states=tuple(states))


def run_tasks(
    substrate: Substrate,
    constraints: ConstraintSet,
) -> tuple[Episode, ...]:
    """Run the three declared entry points of the path."""

    starts = (substrate.start, substrate.staging, substrate.gate)
    return tuple(run_episode(substrate, constraints, start) for start in starts)


def lens_class(state: int, substrate: Substrate, lens: str) -> int | str:
    """Map physical states into observer equivalence classes."""

    if lens == "exact":
        return state
    if lens == "gate-equals-goal":
        if state in {substrate.gate, substrate.goal}:
            return "accepted-terminal"
        return state
    raise ValueError(f"unknown lens: {lens}")


def competence(
    episodes: Iterable[Episode],
    substrate: Substrate,
    lens: str,
) -> float:
    """Fraction of tasks whose terminal is lens-equivalent to the goal."""

    return mean(
        lens_class(episode.terminal, substrate, lens)
        == lens_class(episode.goal, substrate, lens)
        for episode in episodes
    )


def summarize_arm(
    *,
    arm: str,
    substrate: Substrate,
    constraints: ConstraintSet,
    lens: str,
    baseline_traces: tuple[tuple[int, ...], ...],
    generator_changed: bool,
    reference_constraints: ConstraintSet,
) -> ArmResult:
    episodes = run_tasks(substrate, constraints)
    traces = tuple(episode.states for episode in episodes)
    physical_success = mean(episode.physical_success for episode in episodes)
    observed = competence(episodes, substrate, lens)
    constraint_edits = len(
        constraints.blocked_edges.symmetric_difference(
            reference_constraints.blocked_edges
        )
    )
    lens_edits = int(lens != "exact")

    if arm == "reference":
        classification = "reference"
    elif generator_changed:
        classification = "creation-or-import control"
    elif traces == baseline_traces and observed > 0:
        classification = "lens reinterpretation"
    elif constraint_edits and physical_success > 0:
        classification = "constraint exposure"
    else:
        classification = "no detected increase"

    return ArmResult(
        arm=arm,
        seed=substrate.seed,
        generator_changed=generator_changed,
        constraint_edits=constraint_edits,
        lens_edits=lens_edits,
        physical_success=physical_success,
        observed_competence=observed,
        trace_changed=traces != baseline_traces,
        classification=classification,
        traces=traces,
    )


def run_experiment(seed: int = DEFAULT_SEED) -> tuple[ArmResult, ...]:
    """Run the reference and three controlled intervention arms."""

    substrate = make_substrate(seed)
    reference_constraints = ConstraintSet(frozenset({LATENT_EDGE}))
    released_constraints = ConstraintSet(frozenset())
    baseline_episodes = run_tasks(substrate, reference_constraints)
    baseline_traces = tuple(episode.states for episode in baseline_episodes)

    specifications = (
        (
            "reference",
            substrate,
            reference_constraints,
            "exact",
            False,
        ),
        (
            "constraint-release",
            substrate,
            released_constraints,
            "exact",
            False,
        ),
        (
            "lens-only",
            substrate,
            reference_constraints,
            "gate-equals-goal",
            False,
        ),
        (
            "generator-edit",
            make_edited_substrate(substrate),
            reference_constraints,
            "exact",
            True,
        ),
    )
    return tuple(
        summarize_arm(
            arm=arm,
            substrate=arm_substrate,
            constraints=constraints,
            lens=lens,
            baseline_traces=baseline_traces,
            generator_changed=generator_changed,
            reference_constraints=reference_constraints,
        )
        for (
            arm,
            arm_substrate,
            constraints,
            lens,
            generator_changed,
        ) in specifications
    )


def render_markdown(results: tuple[ArmResult, ...]) -> str:
    """Render documentation-ready output."""

    reference = results[0]
    lines = [
        f"Seed: `{reference.seed}`",
        "",
        (
            "| arm | generator changed | constraint edits | lens edits | "
            "physical success | observed competence | trace changed | classification |"
        ),
        "|:---|:---:|---:|---:|---:|---:|:---:|:---|",
    ]
    for result in results:
        lines.append(
            f"| `{result.arm}` | {'yes' if result.generator_changed else 'no'} | "
            f"{result.constraint_edits} | {result.lens_edits} | "
            f"{result.physical_success:.3f} | "
            f"{result.observed_competence:.3f} | "
            f"{'yes' if result.trace_changed else 'no'} | "
            f"{result.classification} |"
        )

    lines.extend(
        [
            "",
            (
                "The `constraint-release` and `lens-only` arms both have "
                "$\\Delta C_{\\mathrm{obs}}=1$, but only constraint release "
                "changes physical traces and exact-goal success."
            ),
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    args = parser.parse_args()
    results = run_experiment(args.seed)
    if args.format == "json":
        print(json.dumps([asdict(result) for result in results], indent=2))
    else:
        print(render_markdown(results))


if __name__ == "__main__":
    main()
