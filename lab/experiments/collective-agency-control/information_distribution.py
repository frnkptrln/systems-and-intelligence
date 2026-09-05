#!/usr/bin/env python3
"""Exact finite-state calibration of information scores versus known erasures.

Python 3.10+, standard library only. Run: python information_distribution.py --output information-distribution-result.json
Not the repository's preregistered collective-agency benchmark. No agent,
learning, time-series prediction, NTIC, consciousness, or viability claims.
All probability calculations enumerate the full declared distribution;
entropies and mutual information are evaluated in floating-point bits.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations, product
import json
from math import log2
from pathlib import Path
import unittest

PRIME = 5
Row = tuple[int, int, int, int]  # target, component 1, component 2, component 3
Rows = tuple[Row, ...]
CASES = ("broadcast", "hub_essential", "two_of_three", "three_of_three")


def enumerate_case(name: str) -> Rows:
    """Rows are equiprobable; component indices are fixed and known."""
    p = PRIME
    if name == "broadcast":
        return tuple((s, s, s, s) for s in range(p))
    if name == "hub_essential":
        return tuple((s, r, (s-r) % p, (s-r) % p)
                     for s, r in product(range(p), repeat=2))
    if name == "two_of_three":
        return tuple((s, (s+r) % p, (s+2*r) % p, (s+3*r) % p)
                     for s, r in product(range(p), repeat=2))
    if name == "three_of_three":
        return tuple((s, (s+r+q) % p, (s+2*r+4*q) % p,
                      (s+3*r+9*q) % p)
                     for s, r, q in product(range(p), repeat=3))
    raise ValueError(f"Unknown case: {name}")


def counts(rows: Rows, columns: tuple[int, ...]) -> Counter:
    return Counter(tuple(row[i] for i in columns) for row in rows)


def clean(x: float) -> float:
    return 0.0 if abs(x) < 1e-12 else x


def entropy(rows: Rows, columns: tuple[int, ...]) -> float:
    if not rows:
        raise ValueError("An empty distribution has no defined probability law.")
    total = len(rows)
    return clean(-sum((c/total)*log2(c/total) for c in counts(rows, columns).values()))


def mutual_information(rows: Rows, a: tuple[int, ...], b: tuple[int, ...]) -> float:
    joint = tuple(dict.fromkeys(a+b))
    return clean(entropy(rows, a)+entropy(rows, b)-entropy(rows, joint))


def bayes_accuracy(rows: Rows, observed: tuple[int, ...]) -> float:
    """Best possible decoding from surviving shares; no finite-data training."""
    conditional = defaultdict(Counter)
    for row in rows:
        conditional[tuple(row[i] for i in observed)][row[0]] += 1
    return sum(max(c.values()) for c in conditional.values()) / len(rows)


def specific_information(rows: Rows, source: int, target_value: int) -> float:
    marginal = Counter(row[source] for row in rows)
    selected = [row for row in rows if row[0] == target_value]
    conditional = Counter(row[source] for row in selected)
    return clean(sum((c/len(selected))*log2((c/len(selected))/(marginal[x]/len(rows)))
                     for x, c in conditional.items()))


def pair_pid_imin(rows: Rows, a: int, b: int) -> dict[str, float]:
    """Two-source Williams-Beer minimum-specific-information PID.

    This is NOT a general three-source decomposition. The three pair scores
    are reported separately, then averaged over all three unordered pairs.
    """
    targets = Counter(row[0] for row in rows)
    redundancy = sum((c/len(rows))*min(specific_information(rows, a, y),
                                       specific_information(rows, b, y))
                     for y, c in targets.items())
    ia = mutual_information(rows, (a,), (0,))
    ib = mutual_information(rows, (b,), (0,))
    joint = mutual_information(rows, (a, b), (0,))
    return {"redundancy_bits": clean(redundancy),
            "unique_a_bits": clean(ia-redundancy),
            "unique_b_bits": clean(ib-redundancy),
            "synergy_bits": clean(joint-ia-ib+redundancy),
            "joint_information_bits": joint}


def lagrange_at_zero(points: tuple[tuple[int, int], ...]) -> int:
    """Interpolate a polynomial at zero over GF(5)."""
    if not points or len({x for x, _ in points}) != len(points):
        raise ValueError("Need a nonempty set of distinct field coordinates.")
    value = 0
    for x, y in points:
        weight = 1
        for z, _ in points:
            if z != x:
                weight = (weight * (-z) * pow((x-z) % PRIME, -1, PRIME)) % PRIME
        value = (value + y*weight) % PRIME
    return value


def coalition_profile(rows: Rows) -> tuple[dict[str, float], list[list[int]]]:
    """Every source subset, including empty; exact decoding, not a multivariate PID."""
    subsets = tuple(group for size in range(4) for group in combinations((1, 2, 3), size))
    accuracies = {group: bayes_accuracy(rows, group) for group in subsets}
    reconstructing = [group for group in subsets if accuracies[group] == 1.0]
    minimal = [list(group) for group in reconstructing
               if not any(set(other) < set(group) for other in reconstructing)]
    return {",".join(map(str, group)) or "empty": accuracy
            for group, accuracy in accuracies.items()}, minimal


def summarize(name: str) -> dict:
    rows = enumerate_case(name)
    h = entropy(rows, (0,))
    singles = [mutual_information(rows, (i,), (0,)) for i in (1, 2, 3)]
    joint = mutual_information(rows, (1, 2, 3), (0,))
    pairs = {f"{a},{b}": pair_pid_imin(rows, a, b) for a, b in combinations((1,2,3), 2)}
    erasures = []
    for lost in (1, 2, 3):
        remaining = tuple(i for i in (1, 2, 3) if i != lost)
        mi = mutual_information(rows, remaining, (0,))
        erasures.append({"erased_component": lost,
                         "remaining_target_information_bits": mi,
                         "remaining_target_entropy_bits": clean(h-mi),
                         "optimal_decoding_accuracy": bayes_accuracy(rows, remaining)})
    coalition_accuracy, minimal = coalition_profile(rows)
    return {"name": name, "equiprobable_states": len(rows),
            "coalition_optimal_decoding_accuracy": coalition_accuracy,
            "minimal_reconstructing_coalitions": minimal,
            "target_entropy_bits": h,
            "component_entropies_bits": [entropy(rows, (i,)) for i in (1,2,3)],
            "joint_component_entropy_bits": entropy(rows, (1,2,3)),
            "individual_target_information_bits": singles,
            "joint_target_information_bits": joint,
            "normalized_joint_over_best_single_gain": clean((joint-max(singles))/h),
            "pair_pid_imin": pairs,
            "normalized_mean_pair_synergy": clean(sum(x["synergy_bits"] for x in pairs.values())/(3*h)),
            "intact_optimal_decoding_accuracy": bayes_accuracy(rows, (1,2,3)),
            "known_erasures": erasures,
            "worst_single_erasure_accuracy": min(e["optimal_decoding_accuracy"] for e in erasures),
            "uniform_single_erasure_accuracy": sum(e["optimal_decoding_accuracy"] for e in erasures)/3}


class CalibrationTests(unittest.TestCase):
    def test_local_budgets_and_target(self) -> None:
        for name in CASES:
            rows = enumerate_case(name)
            for i in range(4):
                self.assertAlmostEqual(entropy(rows, (i,)), log2(PRIME))
            self.assertEqual(bayes_accuracy(rows, (1,2,3)), 1.0)

    def test_matched_entropy_and_randomness_for_main_comparison(self) -> None:
        a, b = enumerate_case("hub_essential"), enumerate_case("two_of_three")
        self.assertEqual(len(a), len(b))
        self.assertAlmostEqual(entropy(a, (1,2,3)), entropy(b, (1,2,3)))

    def test_no_single_share_informs_target(self) -> None:
        for name in CASES[1:]:
            rows = enumerate_case(name)
            for i in (1,2,3):
                self.assertAlmostEqual(mutual_information(rows, (i,), (0,)), 0.0)
                self.assertEqual(bayes_accuracy(rows, (i,)), 1/PRIME)

    def test_declared_scores(self) -> None:
        expected = {"broadcast": (0.0, 0.0, 1.0),
                    "hub_essential": (1.0, 2/3, 1/PRIME),
                    "two_of_three": (1.0, 1.0, 1.0),
                    "three_of_three": (1.0, 0.0, 1/PRIME)}
        for name, (gain, synergy, worst) in expected.items():
            result = summarize(name)
            self.assertAlmostEqual(result["normalized_joint_over_best_single_gain"], gain)
            self.assertAlmostEqual(result["normalized_mean_pair_synergy"], synergy)
            self.assertAlmostEqual(result["worst_single_erasure_accuracy"], worst)

    def test_pid_additivity(self) -> None:
        for name in CASES:
            rows = enumerate_case(name)
            for a, b in combinations((1,2,3), 2):
                d = pair_pid_imin(rows, a, b)
                atoms = [d[k] for k in ("redundancy_bits", "unique_a_bits", "unique_b_bits", "synergy_bits")]
                self.assertAlmostEqual(sum(atoms), d["joint_information_bits"])
                self.assertTrue(all(x >= -1e-12 for x in atoms))

    def test_explicit_decoders(self) -> None:
        for s, r, second, third in enumerate_case("hub_essential"):
            self.assertEqual((r+second) % PRIME, s)
            self.assertEqual((r+third) % PRIME, s)
        for row in enumerate_case("two_of_three"):
            for indices in combinations((1,2,3), 2):
                self.assertEqual(lagrange_at_zero(tuple((i,row[i]) for i in indices)), row[0])
        for row in enumerate_case("three_of_three"):
            self.assertEqual(lagrange_at_zero(tuple((i,row[i]) for i in (1,2,3))), row[0])

    def test_all_dropout_locations(self) -> None:
        expected = {"broadcast": [1.0,1.0,1.0], "hub_essential": [0.2,1.0,1.0],
                    "two_of_three": [1.0,1.0,1.0], "three_of_three": [0.2,0.2,0.2]}
        for name, values in expected.items():
            self.assertEqual([e["optimal_decoding_accuracy"] for e in summarize(name)["known_erasures"]], values)


def run() -> dict:
    """Reproduce the static calibration; importing this module starts no work."""
    return {"date": "2026-09-05", "kind": "exact_enumeration_calibration_not_preregistered_benchmark",
            "prime": PRIME, "components": 3,
            "probability_method": "complete equiprobable enumeration; floating-point log2",
            "erasure_model": "known identity of one unavailable share; ideal observer decodes remaining shares",
            "cases": [summarize(name) for name in CASES],
            "limitations": ["static encoding, not next-state prediction",
                            "gain versus best individual is not a PID synergy definition",
                            "all-pair PID average is not a three-source PID",
                            "not a run of the repository's proposed oscillator benchmark",
                            "known erasures only, no incorrect shares, learning, repair or decoder failure",
                            "encoding and decoding infrastructure is assumed available",
                            "no NTIC, macro-intervention, viability, consciousness or agency measurement"],
            "sources": ["https://dl.acm.org/doi/10.1145/359168.359176",
                        "https://arxiv.org/abs/1004.2515"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON result path.")
    args = parser.parse_args()
    tests = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(CalibrationTests))
    if not tests.wasSuccessful():
        raise SystemExit(1)
    data = run()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("\nCase                 gain/H(S)   pair synergy/H(S)    worst dropout accuracy")
    for case in data["cases"]:
        print(f"{case['name']:20s} {case['normalized_joint_over_best_single_gain']:8.4f}"
              f" {case['normalized_mean_pair_synergy']:20.4f} {case['worst_single_erasure_accuracy']:24.1%}")


if __name__ == "__main__":
    main()
