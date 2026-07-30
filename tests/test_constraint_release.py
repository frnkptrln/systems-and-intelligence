"""Regression tests for the exact constraint-release benchmark."""

import importlib.util
from pathlib import Path
import sys


REPO = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    REPO
    / "lab"
    / "benchmarks"
    / "constraint-release"
    / "constraint_release.py"
)
SPEC = importlib.util.spec_from_file_location("constraint_release", MODULE_PATH)
assert SPEC and SPEC.loader
cr = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cr
SPEC.loader.exec_module(cr)


def by_name(seed=cr.DEFAULT_SEED):
    return {result.arm: result for result in cr.run_experiment(seed)}


def test_constraint_release_changes_behavior_without_changing_generator():
    results = by_name()
    reference = results["reference"]
    released = results["constraint-release"]

    assert reference.physical_success == 0.0
    assert released.physical_success == 1.0
    assert released.observed_competence == 1.0
    assert released.trace_changed
    assert not released.generator_changed
    assert released.constraint_edits == 1
    assert released.classification == "constraint exposure"


def test_lens_only_changes_score_not_behavior():
    results = by_name()
    reference = results["reference"]
    lens_only = results["lens-only"]

    assert lens_only.physical_success == reference.physical_success == 0.0
    assert lens_only.observed_competence == 1.0
    assert lens_only.traces == reference.traces
    assert not lens_only.trace_changed
    assert lens_only.lens_edits == 1
    assert lens_only.classification == "lens reinterpretation"


def test_generator_edit_is_not_misclassified_as_latent_exposure():
    edited = by_name()["generator-edit"]

    assert edited.generator_changed
    assert edited.physical_success == 1.0
    assert edited.classification == "creation-or-import control"


def test_relations_are_invariant_to_seeded_state_relabeling():
    signatures = []
    for seed in (0, 1, 26, 41, 73, 101):
        signatures.append(
            tuple(
                (
                    result.arm,
                    result.physical_success,
                    result.observed_competence,
                    result.trace_changed,
                    result.classification,
                )
                for result in cr.run_experiment(seed)
            )
        )

    assert all(signature == signatures[0] for signature in signatures[1:])


def test_markdown_report_is_stable_and_declares_seed():
    report = cr.render_markdown(cr.run_experiment())

    assert "Seed: `26`" in report
    assert "| `constraint-release` | no | 1 | 0 | 1.000 | 1.000 | yes |" in report
    assert "| `lens-only` | no | 0 | 1 | 0.000 | 1.000 | no |" in report
