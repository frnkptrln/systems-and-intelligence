#!/usr/bin/env python3
"""
Reaction-Diffusion Morphogenesis – Gray-Scott Model
-----------------------------------------------------

Two virtual chemicals (U and V) diffuse across a 2D grid and react:

    U + 2V → 3V          (autocatalytic growth of V)
    V → P                (V decays into inert product)

With continuous feed of U and removal of V, emergent spatial patterns
appear: spots, stripes, labyrinthine structures – the same mechanism
Alan Turing proposed in 1952 to explain biological morphogenesis.

The simulation uses explicit Euler integration of the Gray-Scott PDEs
on a discrete grid with periodic boundary conditions.

Press ESC in the matplotlib window to exit.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────
GRID_SIZE = 200          # NxN grid resolution
DU        = 0.16         # diffusion rate of U
DV        = 0.08         # diffusion rate of V
F         = 0.035        # feed rate  (try 0.02–0.06)
K         = 0.065        # kill rate  (try 0.05–0.07)
DT        = 1.0          # time step
MAX_STEPS = 12000
DISPLAY_EVERY = 40       # render every N steps
SEED      = 42

# Some beautiful parameter presets:
#   Mitosis (splitting dots):   F=0.028, k=0.062
#   Coral growth:               F=0.037, k=0.064
#   Labyrinthine:               F=0.035, k=0.065  (default)
#   Spots:                      F=0.030, k=0.062
#   Worms:                      F=0.038, k=0.061

# ─────────────────────────────────────────────
# Custom colourmap (deep ocean → coral → cream)
# ─────────────────────────────────────────────
_CMAP_COLORS = [
    (0.02, 0.02, 0.10),   # deep navy
    (0.05, 0.15, 0.35),   # dark teal
    (0.10, 0.40, 0.55),   # ocean blue
    (0.85, 0.35, 0.25),   # coral
    (1.00, 0.92, 0.80),   # cream
]
MORPHO_CMAP = LinearSegmentedColormap.from_list("morpho", _CMAP_COLORS, N=256)


# ─────────────────────────────────────────────
# Laplacian (periodic boundary, 5-point stencil)
# ─────────────────────────────────────────────
def laplacian(Z):
    """Discrete Laplacian with periodic (wrap-around) boundaries."""
    return (
        np.roll(Z, 1, axis=0) + np.roll(Z, -1, axis=0) +
        np.roll(Z, 1, axis=1) + np.roll(Z, -1, axis=1) -
        4.0 * Z
    )


# ─────────────────────────────────────────────
# Initialisation
# ─────────────────────────────────────────────
def init_fields(rng):
    """
    U starts at 1 everywhere, V at 0 everywhere,
    with a small seeded square of V in the centre
    (plus a few random perturbation patches).
    """
    U = np.ones((GRID_SIZE, GRID_SIZE), dtype=np.float64)
    V = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.float64)

    # Central seed
    cx, cy = GRID_SIZE // 2, GRID_SIZE // 2
    r = GRID_SIZE // 20
    U[cx - r:cx + r, cy - r:cy + r] = 0.50
    V[cx - r:cx + r, cy - r:cy + r] = 0.25

    # A few random perturbation patches for richer patterns
    for _ in range(5):
        px = rng.integers(r, GRID_SIZE - r)
        py = rng.integers(r, GRID_SIZE - r)
        s = rng.integers(3, r)
        U[px - s:px + s, py - s:py + s] = 0.50
        V[px - s:px + s, py - s:py + s] = 0.25

    # Tiny noise to break perfect symmetry
    U += 0.02 * rng.standard_normal(U.shape)
    V += 0.02 * rng.standard_normal(V.shape)

    return U, V


# ─────────────────────────────────────────────
# Simulation step
# ─────────────────────────────────────────────
def gray_scott_step(U, V):
    """One Euler step of the Gray-Scott equations."""
    Lu = laplacian(U)
    Lv = laplacian(V)
    uvv = U * V * V

    U_new = U + DT * (DU * Lu - uvv + F * (1.0 - U))
    V_new = V + DT * (DV * Lv + uvv - (F + K) * V)

    # Clamp to [0, 1] for numerical safety
    np.clip(U_new, 0.0, 1.0, out=U_new)
    np.clip(V_new, 0.0, 1.0, out=V_new)

    return U_new, V_new


# ─────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────
def run():
    rng = np.random.default_rng(SEED)
    U, V = init_fields(rng)

    plt.ion()
    fig, ax = plt.subplots(figsize=(7, 7))

    im = ax.imshow(
        V, cmap=MORPHO_CMAP,
        interpolation="bilinear",
        vmin=0, vmax=0.35,
        origin="lower",
    )
    ax.set_xticks([])
    ax.set_yticks([])
    title = ax.set_title(
        f"Reaction-Diffusion (Gray-Scott)  |  F={F}  k={K}  |  Step 0",
        fontsize=10,
    )
    fig.tight_layout()

    # ESC handler
    exit_flag = {"stop": False}

    def on_key(event):
        if event.key in ("escape", "esc"):
            exit_flag["stop"] = True

    fig.canvas.mpl_connect("key_press_event", on_key)

    for step in range(1, MAX_STEPS + 1):
        if exit_flag["stop"]:
            print("\nSimulation beendet (ESC).")
            break

        U, V = gray_scott_step(U, V)

        if step % DISPLAY_EVERY == 0:
            im.set_data(V)
            title.set_text(
                f"Reaction-Diffusion (Gray-Scott)  |  "
                f"F={F}  k={K}  |  Step {step}"
            )
            fig.canvas.draw_idle()
            plt.pause(0.001)

    plt.ioff()
    plt.close(fig)
    print(f"\n─── Finished after {step} steps ───")
    print(f"V range: [{V.min():.4f}, {V.max():.4f}]")


if __name__ == "__main__":
    run()
