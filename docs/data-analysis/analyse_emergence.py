#!/usr/bin/env python3
"""
Analyse Emergence – Apply information-theoretic measures to simulations
------------------------------------------------------------------------

This script runs a quick snapshot of several simulations and measures
their information-theoretic properties, producing a comparative table
and visualisation.

It demonstrates how the measures in info_measures.py can make the
System Intelligence Index (SII) quantitative.

Usage:
    cd data-analysis
    python3 analyse_emergence.py
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")   # non-interactive backend for file output
import matplotlib.pyplot as plt

# Add parent paths for imports
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "simulation-models", "reaction-diffusion"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "simulation-models", "prediction-error-field"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "simulation-models", "self-organized-criticality"))

from info_measures import (
    shannon_entropy,
    spatial_mutual_information,
    block_entropy,
    integration,
    complexity_measure,
    analyse_field,
)


def generate_test_fields(rng):
    """Generate a set of canonical test fields for comparison."""

    fields = {}
    SIZE = 100

    # 1. Pure noise (maximum entropy, no structure)
    fields["Random noise"] = rng.random((SIZE, SIZE))

    # 2. Uniform field (zero entropy)
    fields["Uniform (0.5)"] = np.full((SIZE, SIZE), 0.5)

    # 3. Checkerboard (perfect structure, low entropy)
    checker = np.zeros((SIZE, SIZE))
    checker[::2, ::2] = 1.0
    checker[1::2, 1::2] = 1.0
    fields["Checkerboard"] = checker

    # 4. Game of Life snapshot (complex, structured)
    gol = rng.integers(0, 2, (SIZE, SIZE)).astype(float)
    # Run 50 GoL steps
    for _ in range(50):
        # Count neighbours (periodic)
        n = sum(
            np.roll(np.roll(gol, dy, 0), dx, 1)
            for dy in (-1, 0, 1) for dx in (-1, 0, 1)
            if (dy, dx) != (0, 0)
        )
        gol = ((gol == 1) & ((n == 2) | (n == 3)) | (gol == 0) & (n == 3)).astype(float)
    fields["Game of Life (50 steps)"] = gol

    # 5. Reaction-Diffusion snapshot
    try:
        import reaction_diffusion as rd
        U, V = rd.init_fields(rng)
        for _ in range(2000):
            U, V = rd.gray_scott_step(U, V)
        fields["Reaction-Diffusion (2000 steps)"] = V[:SIZE, :SIZE]
    except ImportError:
        print("  (reaction_diffusion not available, skipping)")

    # 6. Sandpile critical state
    try:
        from sandpile import Sandpile
        pile = Sandpile(SIZE)
        for _ in range(SIZE * SIZE * 4):
            r, c = rng.integers(0, SIZE, 2)
            pile.drop_grain(r, c)
        fields["Sandpile (critical)"] = pile.grid.astype(float) / max(pile.grid.max(), 1)
    except ImportError:
        print("  (sandpile not available, skipping)")

    return fields


def main():
    rng = np.random.default_rng(42)

    print("=" * 60)
    print("  INFORMATION-THEORETIC ANALYSIS OF EMERGENT SYSTEMS")
    print("=" * 60)

    fields = generate_test_fields(rng)

    # Compute measures for each field
    results = {}
    for name, field in fields.items():
        r = analyse_field(field, name=name)
        results[name] = r

    # ── Comparative summary table ──
    print("\n" + "=" * 80)
    print(f"  {'System':<35} {'H':>6} {'MI':>6} {'Φ':>7} {'C':>7}")
    print("─" * 80)
    for name, r in results.items():
        print(
            f"  {name:<35} "
            f"{r['shannon_entropy']:6.2f} "
            f"{r['spatial_MI']:6.3f} "
            f"{r['integration']:+7.3f} "
            f"{r['complexity']:7.2f}"
        )
    print("=" * 80)

    # ── Generate comparison chart ──
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    names = list(results.keys())
    short_names = [n[:18] for n in names]

    measures = [
        ("Shannon entropy H", "shannon_entropy", "#3b82f6"),
        ("Spatial MI", "spatial_MI", "#10b981"),
        ("Integration Φ", "integration", "#f59e0b"),
        ("Complexity C", "complexity", "#ef4444"),
    ]

    for ax, (label, key, color) in zip(axes, measures):
        values = [results[n].get(key, 0) for n in names]
        bars = ax.barh(short_names, values, color=color, edgecolor="white",
                       linewidth=0.5, alpha=0.85)
        ax.set_title(label, fontsize=10, fontweight="bold")
        ax.grid(True, alpha=0.2, axis="x")
        ax.invert_yaxis()

    fig.suptitle(
        "Information-Theoretic Comparison of Emergent Systems",
        fontsize=13, fontweight="bold"
    )
    fig.tight_layout(rect=[0, 0, 1, 0.94])

    output_path = os.path.join(os.path.dirname(__file__), "emergence_analysis.png")
    fig.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    print(f"\n  Chart saved to: {output_path}")
    plt.close(fig)

    print("\nDone.")


if __name__ == "__main__":
    main()
