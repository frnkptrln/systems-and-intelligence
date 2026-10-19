"""Independent finite-orbit controls for the constraint-release graph ensemble."""

from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path
import subprocess
import sys


REPO = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    REPO / "lab" / "benchmarks" / "constraint-release" / "graph_ensemble.py"
)
SPEC = importlib.util.spec_from_file_location("constraint_graph_ensemble", MODULE_PATH)
assert SPEC and SPEC.loader
ge = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ge
SPEC.loader.exec_module(ge)

HAMMING_HISTOGRAMS = {
    "1": [522, 195, 42, 9],
    "2": [201, 84, 75, 24],
    "3": [27, 12, 9, 16],
}
PREFIX_HISTOGRAMS = {
    "1": [174, 65, 14, 3],
    "2": [348, 130, 28, 6],
    "3": [134, 56, 50, 16],
    "4": [67, 28, 25, 8],
    "5": [27, 12, 9, 16],
}


def orbit_successes(targets, blocked_mask):
    """Follow each orbit until goal, a blocked source, or a repeated state.

    This oracle has no simulator horizon and does not call the implementation's
    trace, gain, or success functions.
    """

    successful = set()
    for start in range(3):
        state, visited = start, set()
        while state != 3 and state not in visited:
            if blocked_mask & (1 << state):
                break
            visited.add(state)
            state = targets[state]
        if state == 3:
            successful.add(start)
    return frozenset(successful)


def test_enumeration_is_complete_without_duplicate_pairs():
    cases = tuple(ge.enumerate_cases())
    actual = {
        (case.targets, case.blocked_mask, case.release_mask) for case in cases
    }
    expected = {
        (targets, blocked, release)
        for targets in product(range(4), repeat=3)
        for blocked in range(8)
        for release in range(1, 8)
        if set(i for i in range(3) if release & (1 << i))
        <= set(i for i in range(3) if blocked & (1 << i))
    }
    assert actual == expected
    assert len(cases) == len(actual) == 1216
    assert Counter(bin(case.release_mask).count("1") for case in cases) == {
        1: 768,
        2: 384,
        3: 64,
    }


def test_success_and_gain_agree_with_unbounded_cycle_oracle():
    for targets in product(range(4), repeat=3):
        for blocked in range(8):
            expected = orbit_successes(targets, blocked)
            assert ge.successful_starts(targets, blocked) == expected
            assert {
                start for start in range(3) if ge.trace(targets, blocked, start)[-1] == 3
            } == expected

    observed = {k: Counter() for k in (1, 2, 3)}
    for case in ge.enumerate_cases():
        before = orbit_successes(case.targets, case.blocked_mask)
        after = orbit_successes(
            case.targets, case.blocked_mask ^ case.release_mask
        )
        assert before <= after
        expected_gain = len(after - before)
        assert ge.gain_count(case) == expected_gain
        observed[bin(case.release_mask).count("1")][expected_gain] += 1
    assert {
        str(k): [histogram[gain] for gain in range(4)]
        for k, histogram in observed.items()
    } == HAMMING_HISTOGRAMS


def test_conditional_payload_lengths_for_every_nonempty_release():
    # These are declared address payloads, not optimal encodings of subsets.
    expected = {
        1: (1, 2, 1),
        2: (1, 2, 2),
        3: (2, 4, 3),
        4: (1, 2, 2),
        5: (2, 4, 3),
        6: (2, 4, 4),
        7: (3, 6, 5),
    }
    for release_mask, (edits, fixed_bits, prefix_bits) in expected.items():
        assert ge.intervention_costs(release_mask) == {
            "hamming_edits": edits,
            "fixed_address_payload_bits": fixed_bits,
            "prefix_address_payload_bits": prefix_bits,
        }


def test_equal_cost_does_not_identify_gain_even_with_graph_and_reference_fixed():
    ineffective = ge.Case((1, 2, 3), 0b110, 0b010)
    effective = ge.Case((1, 2, 3), 0b110, 0b100)
    assert ge.intervention_costs(ineffective.release_mask) == ge.intervention_costs(
        effective.release_mask
    )
    assert orbit_successes(ineffective.targets, ineffective.blocked_mask) == frozenset()
    assert orbit_successes(ineffective.targets, ineffective.after_mask) == frozenset()
    assert orbit_successes(effective.targets, effective.after_mask) == frozenset({2})
    assert ge.gain_count(ineffective) == 0
    assert ge.gain_count(effective) == 1


def test_all_relabelings_transport_physical_traces_and_preserve_gain():
    cases = tuple(ge.enumerate_cases())
    changed_costs = 0
    for mapping in permutations(range(3)):
        pooled = {cost: Counter() for cost in PREFIX_HISTOGRAMS}
        for case in cases:
            transported = ge.relabel(case, mapping)
            assert ge.gain_count(transported) == ge.gain_count(case)
            for before_mask, after_mask in (
                (case.blocked_mask, transported.blocked_mask),
                (case.after_mask, transported.after_mask),
            ):
                for start in range(3):
                    expected_trace = tuple(
                        3 if state == 3 else mapping[state]
                        for state in ge.trace(case.targets, before_mask, start)
                    )
                    assert ge.trace(
                        transported.targets, after_mask, mapping[start]
                    ) == expected_trace
            old_cost = ge.intervention_costs(case.release_mask)[
                "prefix_address_payload_bits"
            ]
            new_cost = ge.intervention_costs(transported.release_mask)[
                "prefix_address_payload_bits"
            ]
            changed_costs += old_cost != new_cost
            pooled[str(new_cost)][ge.gain_count(transported)] += 1
        assert {
            cost: [histogram[gain] for gain in range(4)]
            for cost, histogram in pooled.items()
        } == PREFIX_HISTOGRAMS
    assert changed_costs == 3072


def test_same_intervention_can_change_prefix_length_under_relabeling():
    original = ge.Case((1, 2, 3), 0b100, 0b100)
    transported = ge.relabel(original, (2, 1, 0))
    assert ge.gain_count(original) == ge.gain_count(transported) == 3
    assert ge.intervention_costs(original.release_mask)["prefix_address_payload_bits"] == 2
    assert ge.intervention_costs(transported.release_mask)["prefix_address_payload_bits"] == 1


def test_report_preserves_exact_counting_and_conditional_histograms():
    report = ge.run_experiment()
    json.dumps(report)
    assert report["counts"] == {
        "graphs": 64,
        "reference_masks": 8,
        "paired_cases": 1216,
    }
    expected_codes = {
        "hamming_edits": HAMMING_HISTOGRAMS,
        "fixed_address_payload_bits": {
            str(2 * int(cost)): counts
            for cost, counts in HAMMING_HISTOGRAMS.items()
        },
        "prefix_address_payload_bits": PREFIX_HISTOGRAMS,
    }
    assert set(report["cost_histograms"]) == set(expected_codes)
    for code, expected_histogram in expected_codes.items():
        actual = report["cost_histograms"][code]
        assert set(actual) == set(expected_histogram)
        for cost, counts in expected_histogram.items():
            row = actual[cost]
            total = sum(counts)
            assert row["case_count"] == total
            assert row["gain_counts"] == counts
            assert Fraction(row["zero_gain_fraction"]) == Fraction(counts[0], total)
            assert Fraction(row["mean_competence_gain"]) == Fraction(
                sum(gain * count for gain, count in enumerate(counts)), 3 * total
            )
    assert report["relabeling"] == {
        "permutations": 6,
        "transported_cases": 7296,
        "prefix_cost_changed_cases": 3072,
        "individual_gain_invariant": True,
        "pooled_histograms_invariant": True,
    }


def test_archived_result_replays_from_the_identified_source():
    archived_path = MODULE_PATH.parent / "results" / "graph-ensemble-2026-10-19.json"
    archived = json.loads(archived_path.read_text(encoding="utf-8"))
    assert archived["source_sha256"] == hashlib.sha256(MODULE_PATH.read_bytes()).hexdigest()
    completed = subprocess.run(
        [sys.executable, str(MODULE_PATH), "--format", "json"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(completed.stdout) == archived
