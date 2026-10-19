"""Controls for target-independent archive replacements and their accounting."""

from collections import Counter
from dataclasses import replace
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys

import pytest


REPO = Path(__file__).resolve().parents[1]
HERE = REPO / "lab" / "experiments" / "persistence_narrowing"
SPEC = importlib.util.spec_from_file_location("archive_control_test", HERE / "archive_control.py")
ac = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ac
SPEC.loader.exec_module(ac)


def distance_matrix(entries):
    return [[sum(x != y for x, y in zip(a, b)) for b in entries] for a in entries]


def test_banks_preserve_ordered_size_and_are_repeatable():
    for family, width in (("full", 8), ("affine", 4)):
        banks, mask = ac.build_archives(family, 0)
        assert (banks, mask) == ac.build_archives(family, 0)
        assert banks["fitted"] == ac.pn.build_memory(family, 0)
        assert any(mask)
        assert len(mask) == width
        for bank in banks.values():
            assert len(bank) == 16
            assert all(len(state) == width and set(state) <= {0, 1} for state in bank)
        # The declared affine draw is with replacement, not an enumeration of all states.
        if family == "affine":
            assert len(set(banks["uniform"])) < 16


def test_one_translation_preserves_all_pair_distances_and_duplicate_indices():
    for family in ac.pn.FAMILIES:
        for seed in (0, 1):
            banks, mask = ac.build_archives(family, seed)
            fitted, translated = banks["fitted"], banks["translated"]
            assert translated == tuple(tuple(x ^ y for x, y in zip(state, mask)) for state in fitted)
            assert distance_matrix(fitted) == distance_matrix(translated)
            table = ac.pn._to_table(family)
            assert distance_matrix(tuple(map(table, fitted))) == distance_matrix(tuple(map(table, translated)))
            assert [[a == b for b in fitted] for a in fitted] == [
                [a == b for b in translated] for a in translated
            ]


def test_archive_audit_keeps_duplicates_in_its_geometry():
    bank = ((0,) * 4,) * 15 + ((1,) * 4,)
    audit = ac.archive_audit("affine", bank)
    assert audit["unique_states"] == 2
    assert audit["multiplicities"] == {"0000": 15, "1111": 1}
    assert audit["parameter_pair_distances"] == {0: 105, 4: 15}
    assert sum(audit["table_pair_distances"].values()) == 120


def test_all_archive_arms_use_identical_flip_and_recall_draws(monkeypatch):
    banks, _ = ac.build_archives("affine", 0)
    original_random = random.Random
    streams = {}

    class Spy:
        def __init__(self, seed):
            self.rng = original_random(seed)
            self.calls = []
            streams.setdefault(seed, []).append(self.calls)

        def random(self):
            result = self.rng.random()
            self.calls.append(("random", result))
            return result

        def randrange(self, *args):
            result = self.rng.randrange(*args)
            self.calls.append(("randrange", args, result))
            return result

        def getrandbits(self, k):
            return self.rng.getrandbits(k)

    monkeypatch.setattr(random, "Random", Spy)
    outcomes = []
    for rule in (0, 255):
        for arm in ("fitted", "uniform", "translated"):
            outcomes.append(ac.pn.run_loop(
                rule, 0, family="affine", condition="memory", memory=banks[arm], row_index=1,
            ))
    for name in ("loop:affine:0:1", "recall:affine:0:1"):
        calls = streams[name]
        assert len(calls) == 6
        assert all(value == calls[0] for value in calls)
    assert len(streams["loop:affine:0:1"][0]) == 128
    assert len({run.recalls for run in outcomes}) == 1


def test_wrapper_reuses_each_bank_across_every_target_and_row(monkeypatch):
    original_builder = ac.build_archives
    original_loop = ac.pn.run_loop
    created = {}
    received = Counter()

    def builder(family, seed):
        assert (family, seed) not in created
        created[family, seed] = original_builder(family, seed)
        return created[family, seed]

    def loop(rule, seed, *, family, condition, memory, row_index, budget):
        banks = created[family, seed][0]
        assert any(memory is bank for bank in banks.values())
        received[family, row_index, rule] += 1
        return original_loop(rule, seed, family=family, condition=condition,
                             memory=memory, row_index=row_index, budget=budget)

    monkeypatch.setattr(ac, "build_archives", builder)
    monkeypatch.setattr(ac.pn, "run_loop", loop)
    report = ac.aggregate(1, 2, budget=0)
    assert len(created) == 2
    assert len(received) == 2 * 2 * 256
    assert set(received.values()) == {4}
    assert report["parameters"]["evaluation_runs"] == 4096


def test_unsaturated_identity_is_distinct_from_fitting_and_detects_corruption():
    banks, _ = ac.build_archives("full", 0)
    blocks = {
        arm: [ac.pn.run_loop(rule, 0, family="full", condition="none" if arm == "none" else "memory",
                            memory=banks["fitted" if arm == "none" else arm], budget=0)
              for rule in range(256)]
        for arm in ac.ARMS
    }
    checks = ac.check_block(blocks)
    assert all(row["information_identity"] for row in checks["arms"].values())
    assert not any(row["visible_saturation"] for row in checks["arms"].values())
    blocks["none"][0] = replace(blocks["none"][0], heldout_correct=7)
    with pytest.raises(AssertionError, match="target-independence"):
        ac.check_block(blocks)


def test_original_cells_reproduce_the_existing_instrument():
    report = ac.aggregate(1, 1)
    for family in ac.pn.FAMILIES:
        memory = ac.pn.build_memory(family, 0)
        for arm, condition in (("none", "none"), ("fitted", "memory")):
            originals = ac.pn.row_block(family, condition, 0, 0, memory)
            means = report["families"][family]["arms"][arm]["means"]
            for key in ac.METRICS:
                expected = sum((Fraction(getattr(run, key)) for run in originals), Fraction(0)) / 256
                assert Fraction(means[key]) == expected


def test_archive_record_identifies_its_sources_and_preserves_prior_results():
    record = json.loads((HERE / "results" / "archive-control-2026-10-19.json").read_text())
    for path, expected_hash in record["sources_sha256"].items():
        assert hashlib.sha256((REPO / path).read_bytes()).hexdigest() == expected_hash
    prior = json.loads((HERE / "results" / "persistence_narrowing.json").read_text())
    names = {"observed": "mean_observed", "heldout": "mean_heldout",
             "distinct_proposals": "mean_distinct_proposals", "distinct_accepted": "mean_distinct_accepted"}
    for family in ac.pn.FAMILIES:
        for arm, old in (("none", "none"), ("fitted", "memory")):
            means = record["families"][family]["arms"][arm]["means"]
            for name, previous_name in names.items():
                assert float(Fraction(means[name])) == prior["families"][family]["conditions"][old][previous_name]


def test_rejects_invalid_grid_arguments():
    for seeds, rows, budget in ((0, 1, 128), (1, 0, 128), (1, 1, -1)):
        with pytest.raises(ValueError):
            ac.aggregate(seeds, rows, budget=budget)


def test_full_archive_record_replays_exactly():
    recorded = json.loads((HERE / "results" / "archive-control-2026-10-19.json").read_text())
    assert json.loads(json.dumps(ac.aggregate(2, 8))) == recorded
