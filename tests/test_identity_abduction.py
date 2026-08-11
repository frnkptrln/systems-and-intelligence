"""Lock the identity-abduction sanity check to the result its README records.

The README carries a Wolfram Language transcript evaluated independently on
2026-08-11. These assertions are that transcript, so the two implementations
have to keep agreeing.
"""

import numpy as np

from lab.experiments.identity_abduction.identity_checks import (
    CYCLE_6,
    PERMUTATION,
    TWO_TRIANGLES,
    degree_sequence,
    is_connected,
    permutation_matrix,
    relabel,
    run_checks,
    spectrum,
)


def test_recorded_result_block_reproduces():
    results = run_checks()

    assert results["positivePermutationWitness"] is True
    assert results["positiveDegreeSequenceEqual"] is True
    assert results["positiveSpectrumEqual"] is True
    assert results["negativeDegreeSequenceEqual"] is True
    assert results["negativeSpectrumEqual"] is False
    assert results["negativeConnectednessDiffers"] == (True, False)


def test_recorded_spectra():
    assert np.allclose(run_checks()["spectrumCycle6"], [-2, -1, -1, 1, 1, 2])
    assert np.allclose(run_checks()["spectrumTwoTriangles"], [-1, -1, -1, -1, 2, 2])


def test_both_graphs_are_two_regular():
    """The decoy is adversarial only because this weak invariant is shared."""
    assert np.array_equal(degree_sequence(CYCLE_6), np.full(6, 2))
    assert np.array_equal(degree_sequence(TWO_TRIANGLES), np.full(6, 2))


def test_permutation_matrix_is_a_permutation():
    p = permutation_matrix()

    assert np.array_equal(p.sum(axis=0), np.ones(6, dtype=int))
    assert np.array_equal(p.sum(axis=1), np.ones(6, dtype=int))
    assert np.array_equal(p @ p.T, np.eye(6, dtype=int))


def test_relabeling_preserves_edge_count_and_is_not_the_identity():
    b = relabel(CYCLE_6)

    assert b.sum() == CYCLE_6.sum()
    assert not np.array_equal(b, CYCLE_6), "a witness that changes nothing proves nothing"


def test_witness_survives_any_permutation():
    """Relabeling is the claim; the specific permutation is not load-bearing."""
    rng = np.random.default_rng(0)
    for _ in range(16):
        perm = tuple(int(i) + 1 for i in rng.permutation(6))
        relabeled = relabel(CYCLE_6, perm)
        assert np.allclose(spectrum(relabeled), spectrum(CYCLE_6))
        assert np.array_equal(degree_sequence(relabeled), degree_sequence(CYCLE_6))


def test_connectivity_separates_where_the_degree_sequence_cannot():
    assert is_connected(CYCLE_6) is True
    assert is_connected(TWO_TRIANGLES) is False


def test_connectedness_rejects_non_square_or_directed_inputs():
    with np.testing.assert_raises_regex(ValueError, "square matrix"):
        is_connected(np.ones((2, 3), dtype=int))
    with np.testing.assert_raises_regex(ValueError, "undirected"):
        is_connected(np.array([[0, 1], [0, 0]], dtype=int))


def test_readme_permutation_is_the_one_the_module_uses():
    assert PERMUTATION == (3, 6, 2, 5, 1, 4)
