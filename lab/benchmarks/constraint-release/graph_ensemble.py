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
