"""Referee benchmark v0 — self-revision against frozen, querying, and capturable referees.

Operationalizes the hypothesis of the exploratory note "Self-Improvement Needs a
Referee": a generate-evaluate-revise loop is first self-modifying, and improvement
requires criteria the loop cannot silently redefine. Following the note's design,
the task, evaluator, permissions, and control logic are frozen per arm; the loop
modifies only an external artifact; budgets bound every run; and the complete
proposal/acceptance history is recorded (reversible checkpoints are the accepted
states in that trace).

The world is a hidden elementary cellular automaton rule (Wolfram bit indexing,
matching ``lab/benchmarks/witness-generation``). Visible evidence is the test set
induced by one synchronous update of a random width-8 ring: each distinct
neighborhood that occurs contributes one (neighborhood -> output) test. The
held-out metric is table accuracy: the fraction of all eight rule coordinates the
artifact gets right. The evidence rng is decoupled from the loop rng, so every
arm sees the same evidence for a given (rule, seed) pair.

Five arms, exact aggregation over all 256 hidden rules:

- ``full-frozen``      unrestricted 8-bit artifact, frozen referee, budget 64.
- ``full-frozen-10x``  the same loop with budget 640 (does more self-revision help?).
- ``full-witness``     frozen referee plus two referee-side queries: at proposal
                       32 and 48 the referee reveals the lowest-index unseen
                       neighborhood and adds it as a test.
- ``affine-frozen``    artifact restricted to the 16 affine rules
                       out = a*l XOR b*c XOR c*r XOR d (misspecified for most
                       worlds), frozen referee, budget 128. The observed score is
                       allowed to plateau below 1 — an honest misspecification
                       signal.
- ``affine-capture``   the same loop, but after eight consecutive rejections with
                       a failing test outstanding, the loop deletes the
                       lowest-index failing test from its evaluator.

All scores are exact integer counts aggregated into fractions at the end; no
floats enter the accounting. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

WIDTH = 8
COORDS = 8
STUCK_LIMIT = 8

ARMS: dict[str, dict] = {
    "full-frozen": {"family": "full", "budget": 64},
    "full-frozen-10x": {"family": "full", "budget": 640},
    "full-witness": {"family": "full", "budget": 64, "queries": (32, 48)},
    "affine-frozen": {"family": "affine", "budget": 128},
    "affine-capture": {"family": "affine", "budget": 128, "capture": True},
}


def rule_bit(rule: int, coord: int) -> int:
    """Wolfram indexing: neighborhood (l, c, r) is coordinate 4l + 2c + r."""
    return (rule >> coord) & 1


def evidence_tests(rule: int, row: Iterable[int]) -> dict[int, int]:
    """Tests induced by one synchronous update of a ring row."""
    cells = tuple(row)
    width = len(cells)
    tests = {}
    for i in range(width):
        coord = (
            (cells[(i - 1) % width] << 2)
            | (cells[i] << 1)
            | cells[(i + 1) % width]
        )
        tests[coord] = rule_bit(rule, coord)
    return dict(sorted(tests.items()))


def affine_table(coeffs: Iterable[int]) -> tuple[int, ...]:
    """Rule table of out = a*l XOR b*c XOR c*r XOR d."""
    a, b, c, d = coeffs
    return tuple(
        ((a & (coord >> 2)) ^ (b & ((coord >> 1) & 1)) ^ (c & (coord & 1)) ^ d)
        for coord in range(COORDS)
    )


@dataclass(frozen=True)
class RunResult:
    """Exact outcome of one bounded loop run."""

    observed_passed: int
    observed_total: int
    heldout_correct: int
    deletions: int
    tests_final: int
    trace: tuple

    @property
    def observed(self) -> Fraction:
        if self.observed_total == 0:
            return Fraction(1)
        return Fraction(self.observed_passed, self.observed_total)

    @property
    def heldout(self) -> Fraction:
        return Fraction(self.heldout_correct, COORDS)


def run_loop(
    rule: int,
    seed: int,
    *,
    family: str,
    budget: int,
    capture: bool = False,
    queries: tuple[int, ...] = (),
    arm: str = "",
    keep_trace: bool = False,
) -> RunResult:
    """One bounded generate-evaluate-revise run against the configured referee."""
    world_rng = random.Random(f"world:{rule}:{seed}")
    loop_rng = random.Random(f"loop:{arm}:{rule}:{seed}")

    row = tuple(world_rng.getrandbits(1) for _ in range(WIDTH))
    tests = evidence_tests(rule, row)

    state = [0] * (COORDS if family == "full" else 4)
    to_table = tuple if family == "full" else affine_table

    def passed(table: tuple) -> int:
        return sum(1 for coord, out in tests.items() if table[coord] == out)

    table = to_table(state)
    score = passed(table)
    stuck = 0
    deletions = 0
    trace = []

    for step in range(budget):
        if step in queries:
            unseen = [coord for coord in range(COORDS) if coord not in tests]
            if unseen:
                coord = unseen[0]
                tests[coord] = rule_bit(rule, coord)
                score = passed(table)
                stuck = 0
                if keep_trace:
                    trace.append(
                        {"step": step, "event": "referee-query", "coordinate": coord}
                    )

        slot = loop_rng.randrange(len(state))
        candidate = list(state)
        candidate[slot] ^= 1
        candidate_table = to_table(candidate)
        candidate_score = passed(candidate_table)

        accepted = candidate_score >= score
        if accepted:
            state, table, score = candidate, candidate_table, candidate_score
            stuck = 0
        elif capture and score < len(tests):
            stuck += 1
            if stuck >= STUCK_LIMIT:
                failing = min(
                    coord for coord, out in tests.items() if table[coord] != out
                )
                del tests[failing]
                deletions += 1
                score = passed(table)
                stuck = 0
                if keep_trace:
                    trace.append(
                        {"step": step, "event": "evaluator-edit", "deleted": failing}
                    )
        if keep_trace:
            trace.append(
                {
                    "step": step,
                    "event": "proposal",
                    "slot": slot,
                    "accepted": accepted,
                    "observed": [score, len(tests)],
                }
            )

    heldout_correct = sum(
        1 for coord in range(COORDS) if table[coord] == rule_bit(rule, coord)
    )
    return RunResult(
        observed_passed=score,
        observed_total=len(tests),
        heldout_correct=heldout_correct,
        deletions=deletions,
        tests_final=len(tests),
        trace=tuple(trace),
    )


@dataclass(frozen=True)
class ArmAggregate:
    """Exact totals for one arm over all 256 rules and every seed."""

    runs: int
    observed_sum: Fraction
    heldout_correct_total: int
    all_pass_runs: int
    tests_final_total: int
    deletions_total: int

    @property
    def mean_observed(self) -> Fraction:
        return self.observed_sum / self.runs

    @property
    def mean_heldout(self) -> Fraction:
        return Fraction(self.heldout_correct_total, self.runs * COORDS)

    @property
    def mean_ceiling(self) -> Fraction:
        """Evidence ceiling for the full family: known coordinates plus chance."""
        return (
            Fraction(self.tests_final_total, self.runs)
            + Fraction(COORDS * self.runs - self.tests_final_total, 2 * self.runs)
        ) / COORDS


def aggregate(arm: str, seeds: int) -> ArmAggregate:
    config = ARMS[arm]
    runs = [
        run_loop(rule, seed, arm=arm, **config)
        for rule in range(256)
        for seed in range(seeds)
    ]
    return ArmAggregate(
        runs=len(runs),
        observed_sum=sum((r.observed for r in runs), Fraction(0)),
        heldout_correct_total=sum(r.heldout_correct for r in runs),
        all_pass_runs=sum(1 for r in runs if r.observed == 1),
        tests_final_total=sum(r.tests_final for r in runs),
        deletions_total=sum(r.deletions for r in runs),
    )


def print_report(seeds: int) -> None:
    print("REFEREE BENCHMARK v0")
    print(f"worlds: all 256 ECA rules x {seeds} seeds | held-out: table accuracy /8")
    print()
    header = (
        f"{'arm':<16} {'observed':>9} {'held-out':>9} "
        f"{'ceiling':>8} {'all-pass':>9} {'deletions':>10}"
    )
    print(header)
    for arm in ARMS:
        agg = aggregate(arm, seeds)
        ceiling = (
            f"{float(agg.mean_ceiling):.4f}" if ARMS[arm]["family"] == "full" else "-"
        )
        print(
            f"{arm:<16} {float(agg.mean_observed):>9.4f} "
            f"{float(agg.mean_heldout):>9.4f} {ceiling:>8} "
            f"{agg.all_pass_runs:>5}/{agg.runs:<3} "
            f"{agg.deletions_total / agg.runs:>10.3f}"
        )
    print()
    print("Reading: the frozen-referee loop saturates at the evidence ceiling and")
    print("10x more self-revision adds nothing; referee-side queries raise the")
    print("ceiling and the held-out score follows; under misspecification the")
    print("frozen referee reports the failure honestly, while the capturable")
    print("evaluator converts the same failure into an all-green report.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=4)
    parser.add_argument(
        "--trace",
        metavar="ARM:RULE:SEED",
        help="print the complete JSONL trace of one run, e.g. affine-capture:110:0",
    )
    args = parser.parse_args()

    if args.trace:
        arm, rule, seed = args.trace.split(":")
        result = run_loop(
            int(rule), int(seed), arm=arm, keep_trace=True, **ARMS[arm]
        )
        for event in result.trace:
            print(json.dumps(event))
        print(
            json.dumps(
                {
                    "final": {
                        "observed": [result.observed_passed, result.observed_total],
                        "heldout_correct": result.heldout_correct,
                        "deletions": result.deletions,
                    }
                }
            )
        )
        return

    print_report(args.seeds)


if __name__ == "__main__":
    main()
