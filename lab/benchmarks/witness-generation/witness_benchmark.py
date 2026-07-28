"""
Exact finite baseline for the Witness Principle.

The candidate family is the 256 elementary cellular-automaton (ECA) rules.
A query prepares one binary ring row and observes its successor. Query cost is
Hamming distance from the all-zero row. An exact witness generator enumerates
every row at a declared cost and chooses the row minimizing:

    (worst-case residual class, expected residual class, row)

The equal-cost baseline is the exact mean over all rows at that cost, not a
Monte-Carlo estimate.

For the full 256-rule family, an independent analytical route derives the
residual class from neighborhood coverage and derives the pairwise witness
profile from the Hamming weights of differing rule-table coordinates.

This demonstrates constructive query selection inside one finite declared
family. It is not a learned witness generator and not a general intelligence
benchmark.

Usage:
    python witness_benchmark.py
    python witness_benchmark.py --candidates 0,128
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations
from math import comb
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


@dataclass(frozen=True)
class ObjectiveComparison:
    """Candidate-aware optimum versus the strongest coverage optimum."""

    cost: int
    candidate_aware: QueryScore
    maximal_coverage: QueryScore
    maximal_neighborhoods: int
    maximal_coverage_query_count: int


@dataclass(frozen=True)
class PairwiseObjectiveGap:
    """Pairwise separability gap at one exact query cost."""

    cost: int
    pair_count: int
    candidate_aware_separable: int
    maximal_coverage_separable: int

    @property
    def divergence_count(self) -> int:
        return self.candidate_aware_separable - self.maximal_coverage_separable


def declared_candidates(rules: Iterable[int]) -> tuple[int, ...]:
    """Validate and freeze a declared subset of the 256 ECA rules."""
    candidates = tuple(rules)
    if not candidates:
        raise ValueError("candidate class must not be empty")
    if any(not isinstance(rule, int) or not 0 <= rule < 256 for rule in candidates):
        raise ValueError("ECA rules must be integers in [0, 255]")
    if len(set(candidates)) != len(candidates):
        raise ValueError("candidate class must not contain duplicates")
    return candidates


def parse_candidates(value: str) -> tuple[int, ...]:
    """Parse a comma-separated candidate declaration for the CLI."""
    try:
        return declared_candidates(int(item.strip()) for item in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


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


def full_family_residual(row: Sequence[int]) -> int:
    """Return the exact residual size for the full 256-rule ECA family.

    Observing a query reveals one rule-table bit for every distinct
    neighborhood in the row. Every unobserved table bit remains free.
    """
    return 1 << (8 - len(neighborhoods(row)))


def rule_difference_coordinates(rule_a: int, rule_b: int) -> tuple[int, ...]:
    """Return rule-table coordinates on which two ECA rules disagree."""
    if not 0 <= rule_a < 256 or not 0 <= rule_b < 256:
        raise ValueError("ECA rules must be in [0, 255]")
    difference = rule_a ^ rule_b
    return tuple(code for code in range(8) if difference & (1 << code))


def neighborhood_access_cost(code: int) -> int:
    """Return the minimum prepared-bit cost for exposing one neighborhood."""
    if not 0 <= code < 8:
        raise ValueError("ECA neighborhood code must be in [0, 7]")
    return code.bit_count()


def analytic_pair_witness_cost(rule_a: int, rule_b: int) -> int | None:
    """Return pairwise witness cost from the lowest differing table layer."""
    differences = rule_difference_coordinates(rule_a, rule_b)
    if not differences:
        return None
    return min(neighborhood_access_cost(code) for code in differences)


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
    candidate_rules = declared_candidates(rules)
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
    candidate_rules = declared_candidates(rules)
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
    candidate_rules = declared_candidates(rules)
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
    candidate_rules = declared_candidates(rules)
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


def restricted_frontier(
    candidates: Iterable[int],
    *,
    width: int = 8,
    max_cost: int = 4,
) -> tuple[FrontierPoint, ...]:
    """Run the exact frontier over an explicitly declared proper subset."""
    candidate_rules = declared_candidates(candidates)
    if len(candidate_rules) == 256 and set(candidate_rules) == set(range(256)):
        raise ValueError("restricted frontier requires a proper subset")
    return exact_frontier(candidate_rules, width=width, max_cost=max_cost)


def compare_candidate_and_coverage(
    rules: Iterable[int],
    *,
    width: int = 8,
    max_cost: int = 4,
) -> tuple[ObjectiveComparison, ...]:
    """Compare candidate-aware search with maximal coordinate coverage.

    At each exact cost, the coverage arm first maximizes the number of
    neighborhoods exposed. Among all tied coverage maximizers, it receives
    the strongest possible candidate-class score. A remaining gap therefore
    cannot be attributed to an unlucky tie-break.
    """
    candidate_rules = declared_candidates(rules)
    comparisons = []
    for cost in range(max_cost + 1):
        scores = [
            score_query(candidate_rules, row)
            for row in rows_at_cost(width, cost)
        ]
        score_key = lambda score: (
            score.worst_case_remaining,
            score.expected_remaining,
            score.row,
        )
        candidate_aware = min(scores, key=score_key)
        maximal_neighborhoods = max(
            score.neighborhoods_seen for score in scores
        )
        coverage_scores = [
            score
            for score in scores
            if score.neighborhoods_seen == maximal_neighborhoods
        ]
        comparisons.append(
            ObjectiveComparison(
                cost=cost,
                candidate_aware=candidate_aware,
                maximal_coverage=min(coverage_scores, key=score_key),
                maximal_neighborhoods=maximal_neighborhoods,
                maximal_coverage_query_count=len(coverage_scores),
            )
        )
    return tuple(comparisons)


def pairwise_objective_gap(
    rules: Iterable[int] = range(256),
    *,
    width: int = 8,
    cost: int,
) -> PairwiseObjectiveGap:
    """Count pairs separable by any query but not by a coverage maximizer.

    Both arms receive the same exact preparation cost. The maximal-coverage
    arm may use any query tied for greatest neighborhood coverage, so the
    reported divergence is objective-level rather than tie-break-specific.
    """
    candidate_rules = declared_candidates(rules)
    signatures = tuple(
        frozenset(neighborhoods(row))
        for row in rows_at_cost(width, cost)
    )
    maximal_size = max(len(signature) for signature in signatures)
    maximal_signatures = tuple(
        signature
        for signature in signatures
        if len(signature) == maximal_size
    )

    pair_count = 0
    candidate_aware_separable = 0
    maximal_coverage_separable = 0
    for rule_a, rule_b in combinations(candidate_rules, 2):
        pair_count += 1
        differences = frozenset(rule_difference_coordinates(rule_a, rule_b))
        if any(signature & differences for signature in signatures):
            candidate_aware_separable += 1
        if any(signature & differences for signature in maximal_signatures):
            maximal_coverage_separable += 1

    return PairwiseObjectiveGap(
        cost=cost,
        pair_count=pair_count,
        candidate_aware_separable=candidate_aware_separable,
        maximal_coverage_separable=maximal_coverage_separable,
    )


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


def pairwise_witness_costs(
    rules: Iterable[int] = range(256),
    *,
    width: int = 8,
) -> Counter[int]:
    """Exact minimal-cost distribution over a declared ECA candidate class."""
    candidate_rules = declared_candidates(rules)
    counts: Counter[int] = Counter()
    for rule_a, rule_b in combinations(candidate_rules, 2):
        row = separating_witness(rule_a, rule_b, width=width)
        if row is None:  # unreachable for distinct deterministic rule tables
            raise AssertionError(f"no witness for rules {rule_a} and {rule_b}")
        counts[sum(row)] += 1
    return counts


def analytic_pairwise_witness_costs() -> Counter[int]:
    """Derive the full-family pairwise profile without searching query rows.

    The eight ECA table coordinates occur in Hamming-weight layers of size
    1, 3, 3, and 1. A pair's cheapest witness cost is the first layer on
    which its rule tables differ.
    """
    counts: Counter[int] = Counter()
    unresolved_before = comb(256, 2)
    coordinates_exposed = 0

    for cost, layer_size in enumerate((1, 3, 3, 1)):
        coordinates_exposed += layer_size
        block_size = 1 << (8 - coordinates_exposed)
        block_count = 1 << coordinates_exposed
        unresolved_after = block_count * comb(block_size, 2)
        counts[cost] = unresolved_before - unresolved_after
        unresolved_before = unresolved_after

    if unresolved_before:
        raise AssertionError("all distinct ECA rule pairs should be resolved")
    return counts


def universal_witnesses(*, width: int = 8) -> tuple[Row, ...]:
    """Enumerate rows exposing all eight ECA rule-table coordinates."""
    return tuple(
        row
        for cost in range(width + 1)
        for row in rows_at_cost(width, cost)
        if len(neighborhoods(row)) == 8
    )


def coverage_classes(*, width: int = 8) -> dict[tuple[int, ...], tuple[Row, ...]]:
    """Quotient query rows by the rule-table coordinates they expose."""
    classes: dict[tuple[int, ...], list[Row]] = defaultdict(list)
    for cost in range(width + 1):
        for row in rows_at_cost(width, cost):
            classes[neighborhoods(row)].append(row)
    return {
        signature: tuple(rows)
        for signature, rows in sorted(classes.items())
    }


def _row_text(row: Row) -> str:
    return "".join(str(bit) for bit in row)


def print_report(
    width: int = 8,
    max_cost: int = 4,
    rules: Iterable[int] = range(256),
) -> None:
    candidate_rules = declared_candidates(rules)
    full_family = (
        len(candidate_rules) == 256
        and set(candidate_rules) == set(range(256))
    )
    frontier = exact_frontier(
        candidate_rules,
        width=width,
        max_cost=max_cost,
    )
    print("WITNESS-GENERATION BENCHMARK")
    family = (
        "all 256 ECA rules"
        if full_family
        else "declared rules " + ",".join(str(rule) for rule in candidate_rules)
    )
    print(f"family: {family} | query width: {width}")
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

    if full_family:
        universal = universal_witnesses(width=width)
        universal_costs = Counter(sum(row) for row in universal)
        query_classes = coverage_classes(width=width)
        print()
        print("COVERAGE-DUALITY RECEIPT")
        print("full-family residual: 2^(8 - neighborhoods seen)")
        print(
            f"raw queries / coverage classes: "
            f"{2**width} / {len(query_classes)}"
        )
        print(f"universal width-{width} queries: {len(universal)}")
        print(
            "universal cost profile: "
            + ", ".join(
                f"cost {cost}: {count}"
                for cost, count in sorted(universal_costs.items())
            )
        )
    else:
        print()
        print("CANDIDATE-AWARE VS MAXIMAL COVERAGE")
        print("cost  aware_remaining  coverage_remaining  aware_query  coverage_query")
        for comparison in compare_candidate_and_coverage(
            candidate_rules,
            width=width,
            max_cost=max_cost,
        ):
            print(
                f"{comparison.cost:>4}  "
                f"{comparison.candidate_aware.worst_case_remaining:>15}  "
                f"{comparison.maximal_coverage.worst_case_remaining:>18}  "
                f"{_row_text(comparison.candidate_aware.row)}  "
                f"{_row_text(comparison.maximal_coverage.row)}"
            )

    print()
    print("PAIRWISE MINIMAL WITNESS COSTS")
    counts = pairwise_witness_costs(candidate_rules, width=width)
    for cost in sorted(counts):
        print(f"cost {cost}: {counts[cost]:>5} rule pairs")
    print(f"total : {sum(counts.values()):>5} rule pairs")
    if full_family:
        print(
            "analytic profile matches exhaustive search: "
            f"{counts == analytic_pairwise_witness_costs()}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=8)
    parser.add_argument("--max-cost", type=int, default=4)
    parser.add_argument(
        "--candidates",
        type=parse_candidates,
        default=tuple(range(256)),
        help="comma-separated ECA rule subset, for example 0,128",
    )
    args = parser.parse_args()
    print_report(
        width=args.width,
        max_cost=args.max_cost,
        rules=args.candidates,
    )


if __name__ == "__main__":
    main()
