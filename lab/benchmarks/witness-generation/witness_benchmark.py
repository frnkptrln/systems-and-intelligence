"""
Exact finite baseline for the Witness Principle.

The candidate family is the 256 elementary cellular-automaton (ECA) rules.
A query prepares one binary ring row and observes its successor. Query cost is
Hamming distance from the all-zero row. An exact witness generator enumerates
every row at a declared cost and chooses the row minimizing:

    (worst-case residual class, expected residual class, row)

The equal-cost baseline is the exact mean over all rows at that cost, not a
Monte-Carlo estimate.

This demonstrates constructive query selection inside one finite declared
family. It is not a learned witness generator and not a general intelligence
benchmark.

Usage:
    python witness_benchmark.py
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations
from statistics import mean
from typing import Iterable, Iterator, Sequence

Row = tuple[int, ...]


@dataclass(frozen=True)
class QueryScore:
    """Exact refinement score for one deterministic query."""

    row: Row
    cost: int
    neighborhoods_seen: int
    worst_case_remaining: int
    expected_remaining: float


@dataclass(frozen=True)
class FrontierPoint:
    """Best structured query and equal-cost unstructured baseline."""

    cost: int
    best: QueryScore
    mean_worst_case_remaining: float
    query_count: int


def neighborhoods(row: Sequence[int]) -> tuple[int, ...]:
    """Return the distinct ECA neighborhood codes present on a binary ring."""
    width = len(row)
    if width < 3:
        raise ValueError("row width must be at least 3")
    if any(bit not in (0, 1) for bit in row):
        raise ValueError("rows must be binary")
    return tuple(
        sorted(
            {
                (row[(i - 1) % width] << 2)
                | (row[i] << 1)
                | row[(i + 1) % width]
                for i in range(width)
            }
        )
    )


def step(rule: int, row: Sequence[int]) -> Row:
    """Apply one ECA update with Wolfram rule-bit indexing 000 -> bit 0."""
    if not 0 <= rule < 256:
        raise ValueError("ECA rule must be in [0, 255]")
    width = len(row)
    present = [
        (row[(i - 1) % width] << 2)
        | (row[i] << 1)
        | row[(i + 1) % width]
        for i in range(width)
    ]
    return tuple((rule >> code) & 1 for code in present)


def rows_at_cost(width: int, cost: int) -> Iterator[Row]:
    """Enumerate every row at exact Hamming cost from the all-zero row."""
    if width < 3:
        raise ValueError("width must be at least 3")
    if not 0 <= cost <= width:
        raise ValueError("cost must lie in [0, width]")
    for positions in combinations(range(width), cost):
        row = [0] * width
        for position in positions:
            row[position] = 1
        yield tuple(row)


def query_partition(rules: Iterable[int], row: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    """Partition candidate rules by their observable successor row."""
    blocks: dict[Row, list[int]] = defaultdict(list)
    for rule in rules:
        blocks[step(rule, row)].append(rule)
    return tuple(tuple(block) for block in blocks.values())


def score_query(rules: Iterable[int], row: Row) -> QueryScore:
    """Score one query by worst-case and uniform-prior residual class size."""
    candidate_rules = tuple(rules)
    if not candidate_rules:
        raise ValueError("candidate class must not be empty")
    blocks = query_partition(candidate_rules, row)
    sizes = [len(block) for block in blocks]
    expected = sum(size * size for size in sizes) / len(candidate_rules)
    return QueryScore(
        row=row,
        cost=sum(row),
        neighborhoods_seen=len(neighborhoods(row)),
        worst_case_remaining=max(sizes),
        expected_remaining=expected,
    )


def best_query_at_cost(
    rules: Iterable[int] = range(256),
    *,
    width: int = 8,
    cost: int,
) -> QueryScore:
    """Construct the best query at one exact preparation cost."""
    candidate_rules = tuple(rules)
    scores = (score_query(candidate_rules, row) for row in rows_at_cost(width, cost))
    return min(
        scores,
        key=lambda score: (
            score.worst_case_remaining,
            score.expected_remaining,
            score.row,
        ),
    )


def generate_witness(
    rules: Iterable[int] = range(256),
    *,
    width: int = 8,
    max_cost: int,
) -> QueryScore:
    """Construct the best query available at or below a preparation budget."""
    candidate_rules = tuple(rules)
    candidates = (
        best_query_at_cost(candidate_rules, width=width, cost=cost)
        for cost in range(max_cost + 1)
    )
    return min(
        candidates,
        key=lambda score: (
            score.worst_case_remaining,
            score.expected_remaining,
            score.cost,
            score.row,
        ),
    )


def exact_frontier(
    rules: Iterable[int] = range(256),
    *,
    width: int = 8,
    max_cost: int = 4,
) -> tuple[FrontierPoint, ...]:
    """Compute the structured optimum and full equal-cost baseline."""
    candidate_rules = tuple(rules)
    points = []
    for cost in range(max_cost + 1):
        scores = [
            score_query(candidate_rules, row)
            for row in rows_at_cost(width, cost)
        ]
        best = min(
            scores,
            key=lambda score: (
                score.worst_case_remaining,
                score.expected_remaining,
                score.row,
            ),
        )
        points.append(
            FrontierPoint(
                cost=cost,
                best=best,
                mean_worst_case_remaining=mean(
                    score.worst_case_remaining for score in scores
                ),
                query_count=len(scores),
            )
        )
    return tuple(points)


def separating_witness(
    rule_a: int,
    rule_b: int,
    *,
    width: int = 8,
    max_cost: int | None = None,
) -> Row | None:
    """Return the cheapest row that produces different outcomes for two rules."""
    if rule_a == rule_b:
        return None
    limit = width if max_cost is None else max_cost
    for cost in range(limit + 1):
        for row in rows_at_cost(width, cost):
            if step(rule_a, row) != step(rule_b, row):
                return row
    return None


def pairwise_witness_costs(*, width: int = 8) -> Counter[int]:
    """Exact minimal-cost distribution over all unordered ECA rule pairs."""
    counts: Counter[int] = Counter()
    for rule_a in range(256):
        for rule_b in range(rule_a + 1, 256):
            row = separating_witness(rule_a, rule_b, width=width)
            if row is None:  # unreachable for distinct deterministic rule tables
                raise AssertionError(f"no witness for rules {rule_a} and {rule_b}")
            counts[sum(row)] += 1
    return counts


def _row_text(row: Row) -> str:
    return "".join(str(bit) for bit in row)


def print_report(width: int = 8, max_cost: int = 4) -> None:
    frontier = exact_frontier(width=width, max_cost=max_cost)
    print("WITNESS-GENERATION BENCHMARK")
    print(f"family: all 256 ECA rules | query width: {width}")
    print()
    print("cost  seen  best_remaining  equal_cost_mean  best_query")
    for point in frontier:
        print(
            f"{point.cost:>4}  "
            f"{point.best.neighborhoods_seen:>4}  "
            f"{point.best.worst_case_remaining:>14}  "
            f"{point.mean_worst_case_remaining:>15.2f}  "
            f"{_row_text(point.best.row)}"
        )

    print()
    print("PAIRWISE MINIMAL WITNESS COSTS")
    counts = pairwise_witness_costs(width=width)
    for cost in sorted(counts):
        print(f"cost {cost}: {counts[cost]:>5} rule pairs")
    print(f"total : {sum(counts.values()):>5} rule pairs")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=8)
    parser.add_argument("--max-cost", type=int, default=4)
    args = parser.parse_args()
    print_report(width=args.width, max_cost=args.max_cost)


if __name__ == "__main__":
    main()
