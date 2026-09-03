"""Decision layer on the witness-generation benchmark (Candidate C1).

Origin: Candidate C1 of ``meta/repository-meta/identification-claims.md``
("Class Size Is Not Decision Risk; Information Gain Is Not Value of
Information") and §7 of ``theory/core/decision-relevant-identifiability.md``,
which asks for a task/value layer on the witness benchmark that compares
class-reduction and information-gain query selectors with a decision-value
selector under matched query cost.

Instrument: ``lab/benchmarks/witness-generation/witness_benchmark.py``, loaded
by path and used unchanged for candidate classes, admissible queries (width-8
rows at exact Hamming cost), outcomes, partitions, and coverage signatures.

Construction (all quantities exact; no float enters a ranking):

- a *candidate class* ``B`` is a declared subset of the 256 ECA rules, uniform prior;
- a *query* is a row at exact cost ``c``; its outcome partitions ``B`` into blocks;
- a *value card* is an integer table ``V[rule][action]``;
- ``EV(B) = max_a mean_rule V``, ``EV(q) = mean over blocks (weighted by size) of
  max_a sum V / |B|``, ``VoI(q) = EV(q) - EV(B)``;
- the *regret radius* of a block is ``min_a max_{rule in block} (max_a' V - V[a])``
  (the essay's decision risk of a posterior class);
- class-size scores are the benchmark's own: worst-case block and expected remaining
  size ``sum |b|^2 / |B|``; information gain is ranked by the integer entropy product
  ``prod |b|^|b|`` (smaller product, more bits).

Selectors at one cost: SIZE (the benchmark's key, worst case then expected size),
IG (smallest entropy product), VOI (largest value of information). A cell
(class, card, cost) is *size-strict* when the best VoI among all size-optimal rows
is strictly below the cost's maximal VoI, *IG-strict* likewise for the IG-optimal
rows. The criticized arm always receives the best VoI among its tied optima, the
benchmark's own device against tie-breaking artifacts. A *full reversal* is an
IG-strict cell whose representatives also satisfy "more bits and smaller expected
class, less value". A *risk-inversion pair* is two blocks of one (class, card) with
the smaller block carrying the larger regret radius.

Standard library only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from fractions import Fraction
from itertools import combinations
from math import log2
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
_WB_PATH = REPO / "lab" / "benchmarks" / "witness-generation" / "witness_benchmark.py"


def _load_witness_benchmark():
    spec = importlib.util.spec_from_file_location("decision_layer_wb", _WB_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


wb = _load_witness_benchmark()

WIDTH = 8
COSTS = (0, 1, 2, 3, 4)
HI = 10
SAFE = 6
CARD_NAMES = ("U", "D1", "D2", "D3")


# ---------------------------------------------------------------- classes and cards
def cube_class(coords) -> tuple[int, ...]:
    """The eight rules that differ exactly on the neighborhood codes ``coords``."""
    coords = tuple(sorted(set(coords)))
    rules = []
    for mask in range(1 << len(coords)):
        rule = 0
        for i, code in enumerate(coords):
            if (mask >> i) & 1:
                rule |= 1 << code
        rules.append(rule)
    return wb.declared_candidates(sorted(rules))


def rule_bit(rule: int, code: int) -> int:
    return (rule >> code) & 1


class Card:
    """A finite action set and an integer value table over (rule, action)."""

    def __init__(self, name: str, actions: tuple, value: dict):
        self.name = name
        self.actions = tuple(actions)
        self.value = value

    def v(self, rule: int, action) -> int:
        return self.value[(rule, action)]


def card_identification(rules) -> Card:
    """Every distinction worth the same: guess the rule, paid 1 when right."""
    actions = tuple(rules)
    return Card("U", actions, {(r, a): int(r == a) for r in rules for a in actions})


def card_decision_bit(rules, d: int, hi: int = HI) -> Card:
    """Only the rule's table bit at coordinate ``d`` matters (the essay's Case B)."""
    actions = (0, 1)
    return Card("D1", actions, {(r, a): hi * int(rule_bit(r, d) == a) for r in rules for a in actions})


def card_safe(rules, d: int, hi: int = HI, safe: int = SAFE) -> Card:
    """As D1 with a third, safe action that pays ``safe`` whatever the rule."""
    actions = (0, 1, "s")
    value = {}
    for r in rules:
        for a in (0, 1):
            value[(r, a)] = hi * int(rule_bit(r, d) == a)
        value[(r, "s")] = safe
    return Card("D2", actions, value)


def card_harmless(rules) -> Card:
    """One action is better whatever the rule (the essay's Case A)."""
    actions = (0, 1)
    return Card("D3", actions, {(r, a): 1 - a for r in rules for a in actions})


def build_card(name: str, rules, d: int) -> Card:
    if name == "U":
        return card_identification(rules)
    if name == "D1":
        return card_decision_bit(rules, d)
    if name == "D2":
        return card_safe(rules, d)
    if name == "D3":
        return card_harmless(rules)
    raise ValueError(f"unknown card {name!r}")


# ---------------------------------------------------------------- exact quantities
def block_value(block, card: Card) -> int:
    return max(sum(card.v(r, a) for r in block) for a in card.actions)


def prior_value(rules, card: Card) -> Fraction:
    return Fraction(block_value(rules, card), len(rules))


def value_after(rules, blocks, card: Card) -> Fraction:
    return Fraction(sum(block_value(b, card) for b in blocks), len(rules))


def value_of_information(rules, blocks, card: Card) -> Fraction:
    return value_after(rules, blocks, card) - prior_value(rules, card)


def regret_radius(block, card: Card) -> int:
    """min over actions of the worst regret inside the block."""
    best = {r: max(card.v(r, a) for a in card.actions) for r in block}
    return min(max(best[r] - card.v(r, a) for r in block) for a in card.actions)


def expected_regret(rules, blocks, card: Card) -> Fraction:
    return sum((Fraction(len(b), len(rules)) * regret_radius(b, card) for b in blocks), Fraction(0))


def expected_remaining(rules, blocks) -> Fraction:
    return Fraction(sum(len(b) * len(b) for b in blocks), len(rules))


def entropy_product(blocks) -> int:
    product = 1
    for b in blocks:
        product *= len(b) ** len(b)
    return product


def information_gain_bits(rules, blocks) -> float:
    n = len(rules)
    return log2(n) - sum(len(b) * log2(len(b)) for b in blocks) / n


def row_text(row) -> str:
    return "".join(str(bit) for bit in row)


# ---------------------------------------------------------------- one cell
def measure_row(rules, row, card: Card) -> dict:
    blocks = wb.query_partition(rules, row)
    sizes = [len(b) for b in blocks]
    return {
        "row": row_text(row),
        "wc": max(sizes),
        "expected_remaining": expected_remaining(rules, blocks),
        "entropy_product": entropy_product(blocks),
        "ig_bits": information_gain_bits(rules, blocks),
        "voi": value_of_information(rules, blocks, card),
        "expected_regret": expected_regret(rules, blocks, card),
        "blocks": sorted((len(b), regret_radius(b, card)) for b in blocks),
    }


def cell(rules, card: Card, cost: int, width: int = WIDTH) -> dict:
    rows = list(wb.rows_at_cost(width, cost))
    measures = {row: measure_row(rules, row, card) for row in rows}

    def size_key(row):
        return (measures[row]["wc"], measures[row]["expected_remaining"])

    best_size = min(size_key(r) for r in rows)
    size_arm = [r for r in rows if size_key(r) == best_size]
    best_w = min(measures[r]["entropy_product"] for r in rows)
    ig_arm = [r for r in rows if measures[r]["entropy_product"] == best_w]
    voi_max = max(measures[r]["voi"] for r in rows)
    voi_arm = [r for r in rows if measures[r]["voi"] == voi_max]

    def strongest(arm):
        # the best VoI among the arm's tied optima, then the lexicographically first row
        return max(arm, key=lambda r: (measures[r]["voi"], [-b for b in r]))

    def weakest_voi_row(arm):
        # the VoI-optimal row that is hardest to beat on the other scores
        return min(arm, key=lambda r: (measures[r]["entropy_product"], measures[r]["expected_remaining"], r))

    q_size = strongest(size_arm)
    q_ig = strongest(ig_arm)
    q_voi = weakest_voi_row(voi_arm)
    voi_size_arm = measures[q_size]["voi"]
    voi_ig_arm = measures[q_ig]["voi"]
    strict_size = voi_size_arm < voi_max
    strict_ig = voi_ig_arm < voi_max
    full_reversal = (
        strict_ig
        and measures[q_ig]["entropy_product"] < measures[q_voi]["entropy_product"]
        and measures[q_ig]["expected_remaining"] < measures[q_voi]["expected_remaining"]
    )
    return {
        "cost": cost,
        "rows": len(rows),
        "q_size": row_text(q_size),
        "q_ig": row_text(q_ig),
        "q_voi": row_text(q_voi),
        "voi_max": voi_max,
        "voi_size_arm": voi_size_arm,
        "voi_ig_arm": voi_ig_arm,
        "strict_size": strict_size,
        "strict_ig": strict_ig,
        "full_reversal": full_reversal,
        "measures": {row_text(r): measures[r] for r in (q_size, q_ig, q_voi)},
        "blocks_all_rows": sorted({pair for r in rows for pair in measures[r]["blocks"]}),
    }


def coverage_criterion(coords, d: int, cost: int, width: int = WIDTH) -> bool:
    """P4: strictness of a cube cell predicted from coverage signatures alone.

    A cell is predicted strict iff some cost-``cost`` row exposes ``d`` and every row
    that exposes the most coordinates of the cube omits ``d``.
    """
    coords = set(coords)
    signatures = {wb.neighborhoods(row) for row in wb.rows_at_cost(width, cost)}
    exposes_d = any(d in s for s in signatures)
    if not exposes_d:
        return False
    best = max(len(coords & set(s)) for s in signatures)
    return all(d not in s for s in signatures if len(coords & set(s)) == best)


def risk_inversion_pairs(blocks_all_rows) -> list:
    """Pairs (smaller block, larger block) whose regret radii are inverted."""
    pairs = []
    for (size_a, rho_a), (size_b, rho_b) in combinations(blocks_all_rows, 2):
        if size_a < size_b and rho_a > rho_b:
            pairs.append([[size_a, rho_a], [size_b, rho_b]])
    return pairs


# ---------------------------------------------------------------- grids
def cube_classes() -> dict:
    """Every cube: 56 coordinate triples × 3 choices of decision coordinate."""
    classes = {}
    for triple in combinations(range(8), 3):
        rules = cube_class(triple)
        for d in triple:
            name = "C" + "".join(str(c) for c in triple) + f"d{d}"
            classes[name] = {"rules": rules, "d": d, "coords": triple}
    return classes


NAMED_CLASSES = {
    "K1": {"rules": cube_class((2, 5, 7)), "d": 7, "coords": (2, 5, 7)},
    "K2": {"rules": cube_class((0, 2, 5)), "d": 0, "coords": (0, 2, 5)},
    "K3": {"rules": wb.declared_candidates((0, 128)), "d": 7, "coords": None},
    "K4": {"rules": wb.declared_candidates(range(256)), "d": 7, "coords": None},
}

CI_SUBGRID = {
    "class_names": ("K1", "K2", "K3", "K4"),
    "cards": CARD_NAMES,
    "costs": COSTS,
    "exclude": (("K4", "U", 4),),
}


def all_classes() -> dict:
    classes = dict(NAMED_CLASSES)
    classes.update(cube_classes())
    return classes


def aggregate(class_names, cards=CARD_NAMES, costs=COSTS, exclude=()) -> dict:
    classes = all_classes()
    excluded = {tuple(e) for e in exclude}
    out = {
        "parameters": {
            "width": WIDTH,
            "costs": list(costs),
            "cards": list(cards),
            "hi": HI,
            "safe": SAFE,
            "classes": {
                name: {"rules": list(classes[name]["rules"]), "d": classes[name]["d"], "coords": classes[name]["coords"]}
                for name in class_names
            },
            "excluded_cells": [list(e) for e in exclude],
        },
        "cells": {},
        "risk_inversion": {},
        "case_ab": {},
        "summary": {},
    }
    strict_counts = {}
    criterion_checks = []
    for name in class_names:
        spec = classes[name]
        rules, d, coords = spec["rules"], spec["d"], spec["coords"]
        for card_name in cards:
            card = build_card(card_name, rules, d)
            blocks_seen = set()
            for cost in costs:
                if (name, card_name, cost) in excluded:
                    continue
                result = cell(rules, card, cost)
                blocks_seen.update(tuple(p) for p in result["blocks_all_rows"])
                out["cells"][f"{name}|{card_name}|{cost}"] = result
                key = f"{card_name}|{cost}"
                strict_counts.setdefault(key, {"size": 0, "ig": 0, "full_reversal": 0, "cells": 0})
                strict_counts[key]["cells"] += 1
                strict_counts[key]["size"] += int(result["strict_size"])
                strict_counts[key]["ig"] += int(result["strict_ig"])
                strict_counts[key]["full_reversal"] += int(result["full_reversal"])
                if coords is not None and card_name == "D1":
                    predicted = coverage_criterion(coords, d, cost)
                    criterion_checks.append(predicted == result["strict_size"])
                    result["criterion"] = predicted
            pairs = risk_inversion_pairs(sorted(blocks_seen))
            out["risk_inversion"][f"{name}|{card_name}"] = {
                "pairs": pairs,
                "example": pairs[0] if pairs else None,
                "blocks": [list(p) for p in sorted(blocks_seen)],
            }
    for name, card_name in (("K4", "D3"), ("K3", "D1")):
        if name in class_names and card_name in cards:
            rules, d = classes[name]["rules"], classes[name]["d"]
            card = build_card(card_name, rules, d)
            out["case_ab"][f"{name}|{card_name}"] = {"class_size": len(rules), "rho": regret_radius(rules, card)}
    out["summary"] = {
        "strict_cells_by_card_and_cost": strict_counts,
        "criterion_checked_cells": len(criterion_checks),
        "criterion_matches_enumeration": all(criterion_checks) if criterion_checks else None,
    }
    return out


# ---------------------------------------------------------------- serialization
def to_jsonable(obj):
    if isinstance(obj, Fraction):
        return f"{obj.numerator}/{obj.denominator}" if obj.denominator != 1 else str(obj.numerator)
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [to_jsonable(v) for v in obj]
    return obj


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true", help="write results/decision_layer.json and results/ci_subgrid.json")
    parser.add_argument("--subgrid-only", action="store_true", help="print only the CI subgrid")
    args = parser.parse_args()
    if args.subgrid_only:
        print(json.dumps(to_jsonable(aggregate(**CI_SUBGRID)), indent=1))
        return
    full_names = tuple(NAMED_CLASSES) + tuple(cube_classes())
    result = to_jsonable(aggregate(full_names))
    print(json.dumps(result["summary"], indent=1))
    if args.save:
        out = HERE / "results" / "decision_layer.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {out.relative_to(REPO)}")
        sub = HERE / "results" / "ci_subgrid.json"
        sub.write_text(json.dumps(to_jsonable(aggregate(**CI_SUBGRID)), indent=1) + "\n", encoding="utf-8")
        print(f"wrote {sub.relative_to(REPO)}")


if __name__ == "__main__":
    main()
