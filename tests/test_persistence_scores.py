import numpy as np
import pytest

from lab.metrics.persistence_scores import (
    component_coverage,
    correlate_component_coverage_with_delta_coherence,
    persistence_scores,
    pstrong,
)


COMPONENTS = ["a", "b"]


def test_arpeggio_is_weakly_but_not_strongly_persistent():
    scores = persistence_scores(COMPONENTS, [{"a"}, {"b"}], horizon=1)

    assert scores["pweak"] == 1.0
    assert scores["pstrong"] == 0.0
    assert scores["per_window_pweak"] == [True]
    assert scores["per_window_pstrong"] == [False]


def test_one_chord_makes_the_window_strongly_persistent():
    scores = persistence_scores(COMPONENTS, [{"a", "b"}, set()], horizon=1)

    assert scores["pweak"] == 1.0
    assert scores["pstrong"] == 1.0


def test_fractional_coverage_is_not_pstrong():
    arpeggio = [{"a"}, {"b"}]

    assert component_coverage(COMPONENTS, arpeggio)["component_coverage"] == 0.5
    assert persistence_scores(COMPONENTS, arpeggio, horizon=1)["pstrong"] == 0.0


def test_windows_stride_and_boolean_averaging_are_explicit():
    trace = [{"a"}, {"b"}, {"a", "b"}, {"a"}, {"b"}]
    scores = persistence_scores(COMPONENTS, trace, horizon=1, stride=2)

    assert scores["evaluation_indices"] == [0, 1]
    assert scores["window_start_indices"] == [0, 2]
    assert scores["per_window_pweak"] == [True, True]
    assert scores["per_window_pstrong"] == [False, True]
    assert scores["pweak"] == 1.0
    assert scores["pstrong"] == 0.5


def test_explicit_layer_times_map_to_algorithm_one_windows():
    trace = [{"a"}, {"b"}, {"a", "b"}, set()]
    scores = persistence_scores(
        COMPONENTS,
        trace,
        horizon=1,
        stride=2,
        evaluation_indices=[0, 1],
    )

    assert scores["evaluation_indices"] == [0, 1]
    assert scores["window_start_indices"] == [0, 2]
    assert scores["per_window_pstrong"] == [False, True]


def test_unrelated_active_labels_do_not_fake_an_ingredient_count():
    scores = persistence_scores(
        COMPONENTS,
        [{"a", "unrelated"}, {"unrelated"}],
        horizon=1,
    )

    assert scores["pweak"] == 0.0
    assert scores["pstrong"] == 0.0


def test_no_complete_window_returns_zero_scores_and_auditable_empty_lists():
    scores = persistence_scores(COMPONENTS, [{"a"}], horizon=1)

    assert scores["pweak"] == 0.0
    assert scores["pstrong"] == 0.0
    assert scores["n_windows"] == 0
    assert scores["per_window_pweak"] == []


def test_pstrong_entry_point_uses_the_corrected_window_logic():
    scores = pstrong(COMPONENTS, [{"a"}, {"b"}], horizon=1)
    assert (scores["pweak"], scores["pstrong"]) == (1.0, 0.0)


def test_horizon_is_nonnegative_and_stride_is_positive():
    assert persistence_scores(COMPONENTS, [{"a", "b"}], horizon=0)[
        "pstrong"
    ] == 1.0
    with pytest.raises(ValueError):
        persistence_scores(COMPONENTS, [{"a", "b"}], horizon=-1)
    with pytest.raises(ValueError):
        persistence_scores(COMPONENTS, [{"a", "b"}], horizon=0, stride=0)


def test_invalid_explicit_windows_fail_instead_of_being_clipped():
    with pytest.raises(ValueError, match="no complete window"):
        persistence_scores(
            COMPONENTS,
            [{"a"}, {"b"}],
            horizon=1,
            evaluation_indices=[1],
        )


def test_component_coverage_correlation_uses_accurate_result_names():
    result = correlate_component_coverage_with_delta_coherence(
        COMPONENTS,
        [{"a"}, {"a", "b"}, set()],
        [np.array([0.0]), np.array([1.0]), np.array([3.0])],
    )

    assert result["coverage_result"]["per_step"] == [0.5, 1.0, 0.0]
    assert result["aligned_per_step_coverage"] == [1.0, 0.0]
    assert result["delta_magnitudes"] == [1.0, 2.0]
    assert result["correlation"] == pytest.approx(-1.0)
