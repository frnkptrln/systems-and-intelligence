#!/usr/bin/env python3
"""Minimal finite sanity check for identity abduction.

Separates three things that are easy to blur together: surface similarity, a
shared weak invariant, and an explicit equivalence witness.

``README.md`` records an independent Wolfram Language evaluation of exactly
these quantities. That transcript is provenance — a second implementation, in
another system, of the same claim. This module is the executable side, so the
recorded result is checked on every CI run instead of only when someone opens a
notebook and retypes it.

Usage:
    python -m lab.experiments.identity_abduction.identity_checks
"""

from __future__ import annotations

import numpy as np


# A 6-cycle. Every vertex has degree 2.
CYCLE_6 = np.array(
    [
        [0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0],
    ],
    dtype=int,
)

# Two disconnected triangles. Also 2-regular, so the degree sequence alone
# cannot tell it apart from the 6-cycle. This is the adversarial decoy.
TWO_TRIANGLES = np.array(
    [
        [0, 1, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 1, 0, 1],
        [0, 0, 0, 1, 1, 0],
    ],
    dtype=int,
)

# One-indexed, matching the Wolfram ``IdentityMatrix[6][[perm]]`` in README.md.
PERMUTATION = (3, 6, 2, 5, 1, 4)


def permutation_matrix(perm: tuple[int, ...] = PERMUTATION) -> np.ndarray:
    """Rows of the identity matrix selected by a one-indexed permutation."""
    size = len(perm)
    return np.eye(size, dtype=int)[[index - 1 for index in perm]]


def relabel(adjacency: np.ndarray, perm: tuple[int, ...] = PERMUTATION) -> np.ndarray:
    """Apply the vertex relabeling: ``P . A . transpose(P)``."""
    p = permutation_matrix(perm)
    return p @ adjacency @ p.T


def degree_sequence(adjacency: np.ndarray) -> np.ndarray:
    return np.sort(adjacency.sum(axis=0))


def spectrum(adjacency: np.ndarray, decimals: int = 6) -> np.ndarray:
    """Sorted adjacency eigenvalues. Symmetric input, so ``eigvalsh`` applies."""
    return np.round(np.sort(np.linalg.eigvalsh(adjacency.astype(float))), decimals)


def reaches(adjacency: np.ndarray, source: int, target: int, steps: int = 5) -> bool:
    """True when a walk of exactly ``steps`` edges connects the two vertices."""
    return bool(np.linalg.matrix_power(adjacency, steps)[source, target] > 0)


def run_checks() -> dict[str, object]:
    """Reproduce every quantity in the README's recorded result block."""
    a = CYCLE_6
    b = relabel(a)
    d = TWO_TRIANGLES
    p = permutation_matrix()

    return {
        "positivePermutationWitness": bool(np.array_equal(b, p @ a @ p.T)),
        "positiveDegreeSequenceEqual": bool(
            np.array_equal(degree_sequence(a), degree_sequence(b))
        ),
        "positiveSpectrumEqual": bool(np.allclose(spectrum(a), spectrum(b))),
        "negativeDegreeSequenceEqual": bool(
            np.array_equal(degree_sequence(a), degree_sequence(d))
        ),
        "negativeSpectrumEqual": bool(np.allclose(spectrum(a), spectrum(d))),
        "spectrumCycle6": spectrum(a),
        "spectrumTwoTriangles": spectrum(d),
        "negativeConnectednessDiffers": (reaches(a, 0, 3), reaches(d, 0, 3)),
    }


def main() -> None:
    results = run_checks()
    width = max(len(name) for name in results)
    print("Identity abduction — minimal finite sanity check")
    print("=" * (width + 34))
    for name, value in results.items():
        if isinstance(value, np.ndarray):
            rendered = "{" + ", ".join(f"{v:g}" for v in value) + "}"
        elif isinstance(value, tuple):
            rendered = "{" + ", ".join(str(v) for v in value) + "}"
        else:
            rendered = str(value)
        print(f"  {name:<{width}}  ->  {rendered}")
    print(
        "\nReading: the permutation is an explicit witness; the shared degree\n"
        "sequence cannot reject the decoy; spectrum and connectivity can.\n"
        "Verification is downstream of the hypothesis, not a substitute for it."
    )


if __name__ == "__main__":
    main()
