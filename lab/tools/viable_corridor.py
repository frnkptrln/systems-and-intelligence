"""
viable_corridor.py — Visualization of the Viable Corridor in TEO parameter space.

Generates Figure 1 for the paper "The Viable Corridor: A
Constraint-Architecture Framework for Survivable Multi-Agent Optimization"
(papers/viable-corridor.md).

The figure shows the three TEO necessity conditions — gamma > 0 (homeostatic
regulation), K > K_c (value coupling above the Kuramoto critical threshold),
and bounded accumulated substrate overshoot Omega(t) < S_max — as
half-spaces in parameter space. Their intersection is the *necessity region*
that contains the viable corridor C. (Sufficiency is conjectured to require
the stronger gamma > gamma_c; see §3.4 of the paper, so C is a proper subset
of the region drawn here.)

The third axis is drawn as instantaneous dS/dt for visual clarity, but the
operative substrate constraint in the paper (v0.3) is the cumulative
Omega(t) < S_max. See the figure caption in the paper.

An illustrative trajectory shows the "paperclip" path: a system whose
parameters drift toward gamma = 0, K < K_c, and rising substrate stress,
exiting the region through its boundaries.

The figure is schematic. The numerical values for K_c, D_max, etc. are
illustrative only; calibrating them to specific systems is an open empirical
task discussed in §5 of the paper.

Usage::

    python -m lab.tools.viable_corridor              # display interactively
    python -m lab.tools.viable_corridor --save       # save to viable_corridor.png
    python -m lab.tools.viable_corridor --save -o my.png  # custom output

Related:

- theory/core/mathematical-axioms.md (current foundation)
- theory/core/the-generator-question.md (legacy motivation)
- theory/teo-framework/love-as-constraint.md (modeling note)
- theory/core/thermodynamics-of-orchestration.md (the TEO ODE system)
- papers/quantifying-emergent-utility-in-llms.md (companion empirical paper)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# Parameter ranges for the visualisation (illustrative, not calibrated).
GAMMA_RANGE = (0.0, 1.0)
K_RANGE = (0.0, 2.0)
DSDT_RANGE = (0.0, 2.0)

# Critical thresholds (illustrative).
GAMMA_MIN = 0.0       # gamma > 0 is the lower bound; any positive value qualifies
K_CRIT = 0.6          # Kuramoto critical coupling K_c
D_MAX = 1.5           # substrate dissipation ceiling

# Colours.
COLOR_CORRIDOR = "#2ca02c"   # green
COLOR_GAMMA = "#d62728"      # red:    gamma = 0 plane
COLOR_K = "#ff7f0e"          # orange: K = K_c plane
COLOR_D = "#9467bd"          # purple: dS/dt = D_max plane
COLOR_TRAJ = "#000000"       # black:  trajectory


def _draw_box(ax, x_range, y_range, z_range, color, alpha=0.15, edge_color=None):
    """Draw a translucent 3D box with high-contrast edges."""
    x0, x1 = x_range
    y0, y1 = y_range
    z0, z1 = z_range
    edge_color = edge_color if edge_color is not None else color

    # Eight vertices of the box.
    v = np.array(
        [
            [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],  # bottom
            [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1],  # top
        ]
    )
    # Six faces as quads. We render the face fill without edges, and then
    # draw box edges separately as opaque lines so they remain visible
    # regardless of the face alpha.
    faces = [
        [v[0], v[1], v[2], v[3]],
        [v[4], v[5], v[6], v[7]],
        [v[0], v[1], v[5], v[4]],
        [v[2], v[3], v[7], v[6]],
        [v[1], v[2], v[6], v[5]],
        [v[0], v[3], v[7], v[4]],
    ]
    poly = Poly3DCollection(
        faces, facecolor=color, alpha=alpha, linewidth=0
    )
    ax.add_collection3d(poly)

    # Twelve edges of the box, rendered fully opaque for contrast.
    edges = [
        (v[0], v[1]), (v[1], v[2]), (v[2], v[3]), (v[3], v[0]),
        (v[4], v[5]), (v[5], v[6]), (v[6], v[7]), (v[7], v[4]),
        (v[0], v[4]), (v[1], v[5]), (v[2], v[6]), (v[3], v[7]),
    ]
    for p1, p2 in edges:
        ax.plot(
            [p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
            color=edge_color, linewidth=1.6, alpha=0.9,
        )


def _draw_plane(ax, axis, value, ranges, color, alpha=0.10):
    """Draw a translucent plane parallel to two axes at fixed value on the third."""
    g_range, k_range, s_range = ranges
    if axis == "gamma":
        Y, Z = np.meshgrid(np.linspace(*k_range, 2), np.linspace(*s_range, 2))
        X = value * np.ones_like(Y)
    elif axis == "K":
        X, Z = np.meshgrid(np.linspace(*g_range, 2), np.linspace(*s_range, 2))
        Y = value * np.ones_like(X)
    elif axis == "dSdt":
        X, Y = np.meshgrid(np.linspace(*g_range, 2), np.linspace(*k_range, 2))
        Z = value * np.ones_like(X)
    else:
        raise ValueError(f"unknown axis: {axis}")
    ax.plot_surface(X, Y, Z, color=color, alpha=alpha, linewidth=0)


def _paperclip_trajectory(n=60):
    """Generate the illustrative 'paperclip' trajectory.

    Starts inside the corridor at moderate (gamma, K, dS/dt) and curves
    toward (gamma -> 0, K -> below K_c, dS/dt -> D_max). The path is
    monotone in each coordinate and crosses each boundary in turn.
    """
    t = np.linspace(0, 1, n)
    # Start: well inside the corridor.
    g0, k0, s0 = 0.55, 1.30, 0.45
    # End: outside on all three axes.
    g1, k1, s1 = 0.03, 0.30, 0.97 * D_MAX
    # Each coordinate follows a slightly different curve to suggest sequenced
    # phase transitions.
    gx = g0 + (g1 - g0) * t ** 2.2
    ky = k0 + (k1 - k0) * t ** 1.5
    sz = s0 + (s1 - s0) * t ** 1.2
    return gx, ky, sz


def plot_viable_corridor(save_path: Path | None = None) -> None:
    """Generate Figure 1: the Viable Corridor."""
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111, projection="3d")

    # --- The viable corridor itself (γ > 0, K > K_c, dS/dt < D_max) ---
    _draw_box(
        ax,
        (GAMMA_MIN + 0.01, GAMMA_RANGE[1]),
        (K_CRIT, K_RANGE[1]),
        (DSDT_RANGE[0], D_MAX),
        color=COLOR_CORRIDOR,
        alpha=0.18,
    )

    # --- Constraint-boundary planes (failure modes) ---
    ranges = (GAMMA_RANGE, K_RANGE, DSDT_RANGE)
    _draw_plane(ax, "gamma", GAMMA_MIN, ranges, COLOR_GAMMA, alpha=0.16)
    _draw_plane(ax, "K", K_CRIT, ranges, COLOR_K, alpha=0.13)
    _draw_plane(ax, "dSdt", D_MAX, ranges, COLOR_D, alpha=0.13)

    # --- The paperclip trajectory ---
    gx, ky, sz = _paperclip_trajectory()
    ax.plot(gx, ky, sz, color=COLOR_TRAJ, linewidth=2.5, zorder=10)
    # Endpoints.
    ax.scatter(
        [gx[0]], [ky[0]], [sz[0]],
        s=70, facecolor="white", edgecolor=COLOR_TRAJ, linewidths=2, zorder=11,
    )
    ax.scatter(
        [gx[-1]], [ky[-1]], [sz[-1]],
        s=100, color=COLOR_TRAJ, marker="X", zorder=11,
    )
    ax.text(gx[0] + 0.04, ky[0], sz[0] + 0.08, "Start", fontsize=10, color=COLOR_TRAJ)
    ax.text(
        gx[-1] + 0.04, ky[-1] - 0.10, sz[-1] + 0.08, "Collapse",
        fontsize=10, color=COLOR_TRAJ,
    )

    # --- Threshold annotations ---
    ax.text(
        GAMMA_RANGE[1] + 0.02, K_CRIT, 0.0, r"$K_c$",
        fontsize=11, color=COLOR_K, ha="left", va="center",
    )
    ax.text(
        GAMMA_RANGE[1] + 0.02, K_RANGE[1], D_MAX, r"$D_{\max}$",
        fontsize=11, color=COLOR_D, ha="left", va="center",
    )
    ax.text(
        0.0, K_RANGE[1] + 0.05, 0.0, r"$\gamma = 0$",
        fontsize=11, color=COLOR_GAMMA, ha="center",
    )

    # --- Axes ---
    ax.set_xlabel(r"$\gamma$  (homeostatic regulation)", fontsize=11, labelpad=10)
    ax.set_ylabel(r"$K$  (value coupling)", fontsize=11, labelpad=10)
    ax.set_zlabel(r"$dS/dt$  (entropy production)", fontsize=11, labelpad=10)
    ax.set_xlim(GAMMA_RANGE)
    ax.set_ylim(K_RANGE)
    ax.set_zlim(DSDT_RANGE)

    # --- Title ---
    ax.set_title(
        "The Viable Corridor in TEO Parameter Space\n"
        r"Necessity region: $\{\gamma > 0\} \cap \{K > K_c\} \cap \{\Omega(t) < S_{\max}\}$"
        "\n(sufficiency conjectured to require $\\gamma > \\gamma_c$)",
        fontsize=11,
        pad=18,
    )

    # --- Custom legend (3D legends are awkward; use proxy artists). ---
    legend_elements = [
        Patch(facecolor=COLOR_CORRIDOR, edgecolor=COLOR_CORRIDOR, alpha=0.30,
              label="Necessity region (contains corridor $\\mathcal{C}$)"),
        Patch(facecolor=COLOR_GAMMA, edgecolor=COLOR_GAMMA, alpha=0.30,
              label=r"$\gamma = 0$: monopoly boundary (Lemma 1)"),
        Patch(facecolor=COLOR_K, edgecolor=COLOR_K, alpha=0.30,
              label=r"$K = K_c$: coherence-collapse boundary (Lemma 2)"),
        Patch(facecolor=COLOR_D, edgecolor=COLOR_D, alpha=0.30,
              label=r"substrate veto: $\Omega(t) = S_{\max}$ (Lemma 3)"),
        Line2D([0], [0], color=COLOR_TRAJ, linewidth=2.5,
               label="Unconstrained (paperclip) trajectory"),
    ]
    ax.legend(
        handles=legend_elements,
        loc="upper left",
        bbox_to_anchor=(0.0, 0.96),
        fontsize=9,
        framealpha=0.92,
    )

    # --- Viewing angle: emphasise the corridor and the trajectory's escape. ---
    ax.view_init(elev=18, azim=-58)

    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
        print(f"Saved: {save_path}")
    else:
        plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the Viable Corridor figure for the paper."
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Save to a PNG file instead of displaying interactively.",
    )
    parser.add_argument(
        "-o", "--output", type=str, default="viable_corridor.png",
        help="Output filename when --save is given (default: viable_corridor.png).",
    )
    args = parser.parse_args()

    save_path = Path(args.output) if args.save else None
    plot_viable_corridor(save_path=save_path)


if __name__ == "__main__":
    main()
