"""Persistence and search narrowing in a self-revision loop (Experiment A).

Origin notes (``ideas/``): persistence-can-narrow-search-space,
research-loop-becomes-environment, mechanistic-discovery-needs-methodological-
separation, experience-needs-an-invalidation-boundary.

The loop is the referee benchmark's generate-evaluate-revise loop
(``lab/benchmarks/recursive-workbench/referee_benchmark.py``): a hidden
elementary cellular-automaton rule, evidence induced by one update of a random
width-8 ring, a frozen evaluator, a stochastic hill-climbing proposer, a hard
budget, and exact integer accounting. This module reuses the benchmark's
primitives (rule tables, evidence tests, affine family, target-independent
streams) and re-implements the loop body so that the *proposal generator* can
be given state across runs. The referee, the target, the acceptance rule, and
the budget are untouched; the ``none`` condition reproduces
``referee_benchmark.run_loop`` exactly, which ``tests/test_persistence_narrowing.py``
asserts.

Memory. Before the evaluation rows are run, the loop is run on ``M`` *prior
worlds* whose hidden rules come from the stream ``memory:{family}:{seed}`` and
whose evidence rows and proposals come from ``world-memory:{seed}:{m}`` and
``loop-memory:{family}:{seed}:{m}``. The final accepted artifact of each prior
world is remembered. Nothing in the memory depends on the hidden rule of an
evaluation run, so within a (seed, row) block the memory is identical across
all 256 hidden rules; the held-out == ceiling identity of the referee benchmark
therefore has to hold in every condition, and ``aggregate`` checks it.

Conditions (same seeds, same budget, same referee):

- ``none``          the benchmark loop; every proposal flips one random slot.
- ``memory``        with probability ``P_RECALL`` a proposal is a remembered
                    artifact instead of a flip (drawn from the run's own
                    ``recall`` stream); accepted under the same rule.
- ``invalidation``  as ``memory``, but a recalled artifact that fails at least
                    one visible test is discarded from the run's copy of the
                    memory (the declared check). An emptied memory falls back
                    to flips.

Measures per run: observed score, held-out table accuracy, the number of
distinct candidate tables proposed, the number of distinct artifacts accepted
(the declared diversity measure: how much of the artifact space the accepted
path covers), and the Hamming distance from the final artifact to the nearest
remembered artifact (attractor pull; computed against the same memory in every
condition so the conditions are comparable).

Standard library only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
_RB_PATH = REPO / "lab" / "benchmarks" / "recursive-workbench" / "referee_benchmark.py"


def _load_referee_benchmark():
    spec = importlib.util.spec_from_file_location("persistence_rb", _RB_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


rb = _load_referee_benchmark()

COORDS = rb.COORDS
WIDTH = rb.WIDTH
BUDGET = 128
P_RECALL = Fraction(1, 2)
MEMORY_WORLDS = 16
FAMILIES = ("full", "affine")
CONDITIONS = ("none", "memory", "invalidation")
# The declared CI subgrid, pinned by tests/test_persistence_narrowing.py against
# results/ci_subgrid.json.
CI_SUBGRID = {"seeds": 1, "rows": 2}


def _to_table(family: str):
    return tuple if family == "full" else rb.affine_table


def _state_size(family: str) -> int:
    return COORDS if family == "full" else 4


def build_memory(family: str, seed: int, worlds: int = MEMORY_WORLDS) -> tuple[tuple[int, ...], ...]:
    """Final accepted artifacts of ``worlds`` prior runs, target-independent.

    The prior worlds' hidden rules come from ``memory:{family}:{seed}``; their
    evidence rows and proposal streams from ``world-memory`` and
    ``loop-memory`` streams. None of these touch any evaluation rule.
    """
    rule_rng = random.Random(f"memory:{family}:{seed}")
    remembered = []
    for m in range(worlds):
        rule = rule_rng.randrange(256)
        world_rng = random.Random(f"world-memory:{seed}:{m}")
        loop_rng = random.Random(f"loop-memory:{family}:{seed}:{m}")
        row = tuple(world_rng.getrandbits(1) for _ in range(WIDTH))
        tests = rb.evidence_tests(rule, row)
        state = _climb(family, tests, loop_rng, BUDGET)
        remembered.append(tuple(state))
    return tuple(remembered)


def _climb(family: str, tests: dict[int, int], loop_rng: random.Random, budget: int) -> list[int]:
    """The benchmark's hill climb, memory-free, returning the final state."""
    to_table = _to_table(family)
    state = [0] * _state_size(family)
    table = to_table(state)
    score = sum(1 for c, o in tests.items() if table[c] == o)
    for _ in range(budget):
        slot = loop_rng.randrange(len(state))
        candidate = list(state)
        candidate[slot] ^= 1
        candidate_table = to_table(candidate)
        candidate_score = sum(1 for c, o in tests.items() if candidate_table[c] == o)
        if candidate_score >= score:
            state, table, score = candidate, candidate_table, candidate_score
    return state


@dataclass(frozen=True)
class RunResult:
    observed_passed: int
    observed_total: int
    heldout_correct: int
    tests_final: int
    distinct_proposals: int
    distinct_accepted: int
    accepted: int
    recalls: int
    invalidated: int
    pull: int

    @property
    def observed(self) -> Fraction:
        if self.observed_total == 0:
            return Fraction(1)
        return Fraction(self.observed_passed, self.observed_total)

    @property
    def heldout(self) -> Fraction:
        return Fraction(self.heldout_correct, COORDS)


def hamming(a: Iterable[int], b: Iterable[int]) -> int:
    return sum(1 for x, y in zip(a, b) if x != y)


def run_loop(
    rule: int,
    seed: int,
    *,
    family: str,
    condition: str,
    memory: tuple[tuple[int, ...], ...],
    row_index: int = 0,
    budget: int = BUDGET,
) -> RunResult:
    """One bounded run under a frozen referee, with or without memory."""
    world_rng, loop_rng = rb.experiment_streams(seed, family, row_index)
    recall_rng = random.Random(f"recall:{family}:{seed}:{row_index}")
    row = tuple(world_rng.getrandbits(1) for _ in range(WIDTH))
    tests = rb.evidence_tests(rule, row)
    to_table = _to_table(family)

    def passed(table: tuple) -> int:
        return sum(1 for c, o in tests.items() if table[c] == o)

    state = [0] * _state_size(family)
    table = to_table(state)
    score = passed(table)
    live_memory = list(memory)
    proposed: set[tuple] = set()
    accepted_tables: set[tuple] = {table}
    accepted = recalls = invalidated = 0
    use_memory = condition in ("memory", "invalidation")

    for _ in range(budget):
        slot = loop_rng.randrange(len(state))
        recalled = False
        if use_memory and live_memory and recall_rng.random() < P_RECALL:
            candidate = list(live_memory[recall_rng.randrange(len(live_memory))])
            recalled = True
            recalls += 1
        else:
            candidate = list(state)
            candidate[slot] ^= 1
        candidate_table = to_table(candidate)
        candidate_score = passed(candidate_table)
        proposed.add(candidate_table)
        if candidate_score >= score:
            state, table, score = candidate, candidate_table, candidate_score
            accepted += 1
            accepted_tables.add(candidate_table)
        if (
            recalled
            and condition == "invalidation"
            and candidate_score < len(tests)
        ):
            live_memory.remove(tuple(candidate))
            invalidated += 1

    heldout_correct = sum(
        1 for c in range(COORDS) if table[c] == rb.rule_bit(rule, c)
    )
    pull = min(hamming(state, m) for m in memory) if memory else -1
    return RunResult(
        observed_passed=score,
        observed_total=len(tests),
        heldout_correct=heldout_correct,
        tests_final=len(tests),
        distinct_proposals=len(proposed),
        distinct_accepted=len(accepted_tables),
        accepted=accepted,
        recalls=recalls,
        invalidated=invalidated,
        pull=pull,
    )


def row_block(family: str, condition: str, seed: int, row_index: int, memory) -> list[RunResult]:
    return [
        run_loop(rule, seed, family=family, condition=condition, memory=memory, row_index=row_index)
        for rule in range(256)
    ]


def aggregate(seeds: int, rows: int) -> dict:
    """Exact aggregates per family and condition, with the identity check."""
    out: dict = {
        "parameters": {
            "seeds": seeds,
            "rows": rows,
            "rules": 256,
            "budget": BUDGET,
            "p_recall": str(P_RECALL),
            "memory_worlds": MEMORY_WORLDS,
            "width": WIDTH,
        },
        "families": {},
    }
    for family in FAMILIES:
        memories = {seed: build_memory(family, seed) for seed in range(seeds)}
        fam: dict = {"memory_size": MEMORY_WORLDS, "conditions": {}}
        for condition in CONDITIONS:
            runs = 0
            observed_sum = Fraction(0)
            heldout_total = tests_total = distinct_total = pull_total = 0
            distinct_accepted_total = 0
            accepted_total = recalls_total = invalidated_total = 0
            identity_ok = True
            for seed in range(seeds):
                for row in range(rows):
                    block = row_block(family, condition, seed, row, memories[seed])
                    h = sum(r.heldout_correct for r in block)
                    t = sum(r.tests_final for r in block)
                    if family == "full" and 2 * h != t + 256 * COORDS:
                        identity_ok = False
                    runs += len(block)
                    observed_sum += sum((r.observed for r in block), Fraction(0))
                    heldout_total += h
                    tests_total += t
                    distinct_total += sum(r.distinct_proposals for r in block)
                    distinct_accepted_total += sum(r.distinct_accepted for r in block)
                    pull_total += sum(r.pull for r in block)
                    accepted_total += sum(r.accepted for r in block)
                    recalls_total += sum(r.recalls for r in block)
                    invalidated_total += sum(r.invalidated for r in block)
            fam["conditions"][condition] = {
                "runs": runs,
                "mean_observed": float(observed_sum / runs),
                "mean_heldout": float(Fraction(heldout_total, runs * COORDS)),
                "mean_ceiling": (
                    float((Fraction(tests_total, runs) + Fraction(COORDS * runs - tests_total, 2 * runs)) / COORDS)
                    if family == "full" else None
                ),
                "heldout_equals_ceiling_identity": identity_ok if family == "full" else None,
                "mean_distinct_proposals": distinct_total / runs,
                "mean_distinct_accepted": distinct_accepted_total / runs,
                "mean_pull_to_memory": pull_total / runs,
                "mean_accepted": accepted_total / runs,
                "mean_recalls": recalls_total / runs,
                "mean_invalidated": invalidated_total / runs,
            }
        out["families"][family] = fam
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=2)
    parser.add_argument("--rows", type=int, default=8)
    parser.add_argument("--save", action="store_true", help="write results/persistence_narrowing.json")
    args = parser.parse_args()
    result = aggregate(args.seeds, args.rows)
    print(json.dumps(result, indent=1))
    if args.save:
        out = HERE / "results" / "persistence_narrowing.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {out.relative_to(REPO)}")
        sub = HERE / "results" / "ci_subgrid.json"
        sub.write_text(json.dumps(aggregate(**CI_SUBGRID), indent=1) + "\n", encoding="utf-8")
        print(f"wrote {sub.relative_to(REPO)}")


if __name__ == "__main__":
    main()
