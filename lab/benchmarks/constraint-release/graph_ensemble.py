"""Exact finite calibration of constraint release across transition graphs.

Enumerate every labelled deterministic graph with three non-goal states and
one absorbing goal, every blocked-source mask, and every nonempty subset of
blocked edges to release. The policy, starts and exact-goal lens stay fixed
within each paired comparison. No learning, model calls or sampling occurs.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import permutations, product
import json
from pathlib import Path


STARTS = (0, 1, 2)
GOAL = 3
HORIZON = 3
PREFIX_CODES = ("0", "10", "11")
RELABELINGS = tuple(permutations(STARTS))


@dataclass(frozen=True)
class Case:
    """One fixed graph, reference constraint and admissible release."""

    targets: tuple[int, int, int]
    blocked_mask: int
    release_mask: int

    @property
    def after_mask(self) -> int:
        return self.blocked_mask & ~self.release_mask


def enumerate_cases():
    """Yield all 64 * (3**3 - 2**3) paired cases exactly once."""

    for targets in product(range(GOAL + 1), repeat=len(STARTS)):
        for blocked in range(1 << len(STARTS)):
            for release in range(1, 1 << len(STARTS)):
                if release & blocked == release:
                    yield Case(targets, blocked, release)


def trace(targets: tuple[int, int, int], blocked_mask: int, start: int):
    """Run the fixed advance action; a blocked source stalls permanently."""

    states = [start]
    for _ in range(HORIZON):
        state = states[-1]
        if state == GOAL:
            break
        if blocked_mask & (1 << state):
            states.append(state)
            break
        states.append(targets[state])
    return tuple(states)


def successful_starts(targets: tuple[int, int, int], blocked_mask: int):
    return frozenset(
        start for start in STARTS if trace(targets, blocked_mask, start)[-1] == GOAL
    )


def gain_count(case: Case) -> int:
    """Additional successful starts; divide by three for competence gain."""

    before = successful_starts(case.targets, case.blocked_mask)
    after = successful_starts(case.targets, case.after_mask)
    if not before <= after:
        raise AssertionError("release lost a previously successful start")
    return len(after) - len(before)


def intervention_costs(release_mask: int) -> dict[str, int]:
    """Declared conditional costs, with graph, reference and k already known.

    Hamming is an edit count. Fixed-width addresses use two bits per source;
    the alternative prefix addresses are 0, 10, 11. Neither payload includes
    a frame, k, the reference, the graph or the cost of choosing the release.
    """

    sources = [source for source in STARTS if release_mask & (1 << source)]
    return {
        "hamming_edits": len(sources),
        "fixed_address_payload_bits": 2 * len(sources),
        "prefix_address_payload_bits": sum(len(PREFIX_CODES[s]) for s in sources),
    }


def relabel(case: Case, mapping: tuple[int, int, int]) -> Case:
    """Transport the same graph and release; the goal retains label three."""

    targets = [0] * len(STARTS)
    blocked = release = 0
    for source in STARTS:
        new_source = mapping[source]
        target = case.targets[source]
        targets[new_source] = GOAL if target == GOAL else mapping[target]
        if case.blocked_mask & (1 << source):
            blocked |= 1 << new_source
        if case.release_mask & (1 << source):
            release |= 1 << new_source
    return Case(tuple(targets), blocked, release)


def describe_case(case: Case) -> dict:
    """Retain the physical traces and both masks for an inspectable witness."""

    return {
        "targets": case.targets,
        "blocked_mask": case.blocked_mask,
        "release_mask": case.release_mask,
        "before_traces": [trace(case.targets, case.blocked_mask, s) for s in STARTS],
        "after_traces": [trace(case.targets, case.after_mask, s) for s in STARTS],
        "additional_successful_starts": gain_count(case),
        "costs": intervention_costs(case.release_mask),
    }


def cost_histograms(cases: tuple[Case, ...]) -> dict:
    """Count equally weighted (graph, reference mask, release subset) cases."""

    counts: dict[str, dict[int, Counter]] = {}
    for case in cases:
        gain = gain_count(case)
        for code, cost in intervention_costs(case.release_mask).items():
            counts.setdefault(code, {}).setdefault(cost, Counter())[gain] += 1
    report = {}
    for code, costs in counts.items():
        report[code] = {}
        for cost, gains in sorted(costs.items()):
            n = sum(gains.values())
            total = sum(gain * count for gain, count in gains.items())
            report[code][str(cost)] = {
                "case_count": n,
                "gain_counts": [gains[gain] for gain in range(len(STARTS) + 1)],
                "mean_competence_gain": str(Fraction(total, len(STARTS) * n)),
                "zero_gain_fraction": str(Fraction(gains[0], n)),
            }
    return report


def run_experiment() -> dict:
    """Return exact distributions and the same-case relabeling controls."""

    cases = tuple(enumerate_cases())
    histograms = cost_histograms(cases)
    cost_changes = 0
    for mapping in RELABELINGS:
        transported = tuple(relabel(case, mapping) for case in cases)
        for before, after in zip(cases, transported):
            if gain_count(before) != gain_count(after):
                raise AssertionError("state relabeling changed physical gain")
            before_cost = intervention_costs(before.release_mask)
            after_cost = intervention_costs(after.release_mask)
            cost_changes += (
                before_cost["prefix_address_payload_bits"]
                != after_cost["prefix_address_payload_bits"]
            )
        if cost_histograms(transported) != histograms:
            raise AssertionError("full-ensemble symmetry check failed")

    # Hold graph AND reference fixed: equal costs, unequal gains.
    no_gain = Case((1, 2, 3), 0b110, 0b010)
    positive_gain = Case((1, 2, 3), 0b110, 0b100)
    # Hold the physical case fixed while changing its opaque state labels.
    chain = Case((1, 2, 3), 0b100, 0b100)
    renamed_chain = relabel(chain, (2, 1, 0))
    return {
        "schema": "constraint-release-graph-ensemble/1",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "specification": {
            "non_goal_states": STARTS,
            "absorbing_goal": GOAL,
            "action": "advance",
            "horizon": HORIZON,
            "weighting": "uniform over labelled (graph, reference mask, release subset)",
            "gain": "additional successful starts divided by three",
            "cost_side_information": "graph, reference mask, k, codebook and framing",
            "prefix_source_codes": PREFIX_CODES,
            "selection_cost_included": False,
        },
        "counts": {
            "graphs": len({case.targets for case in cases}),
            "reference_masks": 1 << len(STARTS),
            "paired_cases": len(cases),
        },
        "cost_histograms": histograms,
        "relabeling": {
            "permutations": len(RELABELINGS),
            "transported_cases": len(cases) * len(RELABELINGS),
            "prefix_cost_changed_cases": cost_changes,
            "individual_gain_invariant": True,
            "pooled_histograms_invariant": True,
        },
        "witnesses": {
            "equal_cost_different_gain": {
                "no_gain": describe_case(no_gain),
                "positive_gain": describe_case(positive_gain),
            },
            "same_release_different_prefix_cost": {
                "before": describe_case(chain),
                "after": describe_case(renamed_chain),
                "mapping": (2, 1, 0),
            },
        },
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Exact graph-ensemble calibration",
        "",
        "64 labelled graphs; 8 reference masks; 1,216 admissible paired cases.",
        "All three non-goal starts; exact-goal lens; fixed advance policy.",
        "",
    ]
    for code, histogram in report["cost_histograms"].items():
        lines.extend([
            f"## {code}",
            "",
            "| cost | cases | gain counts (0, 1/3, 2/3, 1) | mean gain | zero fraction |",
            "|---:|---:|:---|:---|:---|",
        ])
        for cost, row in histogram.items():
            lines.append(
                f"| {cost} | {row['case_count']} | {row['gain_counts']} | "
                f"{row['mean_competence_gain']} | {row['zero_gain_fraction']} |"
            )
        lines.append("")
    lines.extend([
        "Relabeling preserves every physical gain and every pooled histogram.",
        f"Prefix payload changes in {report['relabeling']['prefix_cost_changed_cases']:,} "
        f"of {report['relabeling']['transported_cases']:,} transported cases.",
        "",
        "Counts condition on different reference masks across release sizes;",
        "their means are not a causal dose-response curve. Hamming counts edits;",
        "address payloads assume known k, graph, reference and framing. These are",
        "declared codes, not minimum message lengths or universal complexity.",
        "Monotonicity and pooled relabeling invariance follow from this construction.",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()
    report = run_experiment()
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_markdown(report))


if __name__ == "__main__":
    main()
