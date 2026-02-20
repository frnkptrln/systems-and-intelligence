#!/usr/bin/env python3
"""
Lenia – Continuous Cellular Automata
--------------------------------------

Lenia (Bert Chan, 2019) generalises the Game of Life from discrete
to continuous space, time, and state.  The result: cell-like
"creatures" that move, pulse, grow, and interact – emerging from
a single convolution kernel and a smooth growth function.

The system is defined by:

    A(t+dt) = clip[ A(t) + dt · G(K * A(t)) ]

where:
    K   = ring-shaped convolution kernel (Mexican-hat style)
    K*A = spatial convolution ("how alive is my neighbourhood?")
    G   = growth function centred at μ with width σ
          (too little or too much neighbourhood → decay)
    dt  = time step (< 1 for smooth dynamics)

Press ESC in the matplotlib window to exit.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.signal import fftconvolve

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────
GRID_SIZE    = 256          # world resolution
KERNEL_R     = 13           # kernel radius in cells
DT           = 0.1          # time step (continuous!)
MU           = 0.15         # growth centre
SIGMA        = 0.017        # growth width
MAX_STEPS    = 8000
DISPLAY_EVERY = 2
SEED         = 7

# ─── Presets ─────────────────────────────────
# Each preset produces different "lifeforms":
#
#   Orbium (default):  μ=0.15  σ=0.017  R=13  → gliders
#   Geminium:          μ=0.14  σ=0.014  R=10  → splitting cells
#   Smooth Life:       μ=0.30  σ=0.050  R=15  → blobs / amoebae

# ─────────────────────────────────────────────
# Custom colourmap (deep black → electric blue → white)
# ─────────────────────────────────────────────
_CMAP = LinearSegmentedColormap.from_list("lenia", [
    (0.00, (0.00, 0.00, 0.04)),     # near-black
    (0.15, (0.02, 0.06, 0.22)),     # dark navy
    (0.35, (0.04, 0.20, 0.50)),     # deep blue
    (0.55, (0.10, 0.55, 0.80)),     # electric cyan
    (0.75, (0.40, 0.85, 0.90)),     # bright aqua
    (0.90, (0.80, 0.95, 0.98)),     # pale ice
    (1.00, (1.00, 1.00, 1.00)),     # white
], N=512)


# ─────────────────────────────────────────────
# Kernel: smooth ring (annular bump)
# ─────────────────────────────────────────────
def make_kernel(R):
    """
    Create a smooth ring-shaped kernel of radius R.
    The kernel is a bump function on the annulus [0.5R, R].
    """
    size = 2 * R + 1
    y, x = np.mgrid[-R:R+1, -R:R+1].astype(np.float64)
    r = np.sqrt(x**2 + y**2) / R    # normalised distance [0, ~1.4]

    # Smooth ring: bell curve centred at r=0.5 with width ~0.15
    kernel = np.exp(-((r - 0.5) / 0.15) ** 2 / 2.0)

    # Zero outside unit disk
    kernel[r > 1.0] = 0.0

    # Normalise so kernel sums to 1
    kernel /= kernel.sum()
    return kernel


# ─────────────────────────────────────────────
# Growth function
# ─────────────────────────────────────────────
def growth(u, mu, sigma):
    """
    Growth mapping G(u):
        G(u) = 2 · exp(-(u-μ)²/(2σ²)) - 1

    Returns values in [-1, +1]:
        u ≈ μ  → growth (+1)
        u far from μ → decay (-1)
    """
    return 2.0 * np.exp(-((u - mu) ** 2) / (2.0 * sigma ** 2)) - 1.0


# ─────────────────────────────────────────────
# Initialisation
# ─────────────────────────────────────────────
def init_world(rng):
    """
    Start with a mostly empty world and a few Gaussian blobs
    of random activity to seed the dynamics.
    """
    A = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.float64)

    # Place 3-6 random Gaussian blobs
    n_blobs = rng.integers(3, 7)
    for _ in range(n_blobs):
        cx = rng.integers(GRID_SIZE // 4, 3 * GRID_SIZE // 4)
        cy = rng.integers(GRID_SIZE // 4, 3 * GRID_SIZE // 4)
        r = rng.integers(8, 20)
        y, x = np.mgrid[0:GRID_SIZE, 0:GRID_SIZE].astype(np.float64)
        blob = np.exp(-((x - cx)**2 + (y - cy)**2) / (2.0 * r**2))
        A += blob * rng.uniform(0.3, 1.0)

    # Add tiny noise for symmetry breaking
    A += 0.02 * rng.random((GRID_SIZE, GRID_SIZE))

    return np.clip(A, 0.0, 1.0)


# ─────────────────────────────────────────────
# One Lenia step
# ─────────────────────────────────────────────
def lenia_step(A, kernel, mu, sigma, dt):
    """
    A(t+dt) = clip[ A(t) + dt · G(K * A) ]
    """
    # Spatial convolution via FFT (periodic boundaries)
    U = fftconvolve(A, kernel, mode="same")

    # Growth mapping
    G = growth(U, mu, sigma)

    # Update
    A_new = A + dt * G
    return np.clip(A_new, 0.0, 1.0)


# ─────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────
def run():
    rng = np.random.default_rng(SEED)
    kernel = make_kernel(KERNEL_R)
    A = init_world(rng)

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor("#000008")

    im = ax.imshow(
        A, cmap=_CMAP,
        interpolation="bilinear",
        vmin=0, vmax=1.0,
        origin="lower",
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("#000008")

    title = ax.set_title(
        f"Lenia – Continuous Cellular Automata  |  Step 0",
        fontsize=11, color="#90cdf4"
    )
    fig.tight_layout()

    exit_flag = {"stop": False}
    def on_key(event):
        if event.key in ("escape", "esc"):
            exit_flag["stop"] = True
    fig.canvas.mpl_connect("key_press_event", on_key)

    mass_history = []

    for step in range(1, MAX_STEPS + 1):
        if exit_flag["stop"]:
            print("\nSimulation beendet (ESC).")
            break

        A = lenia_step(A, kernel, MU, SIGMA, DT)
        mass = A.sum()
        mass_history.append(mass)

        if step % DISPLAY_EVERY == 0:
            im.set_data(A)

            title.set_text(
                f"Lenia  |  μ={MU}  σ={SIGMA}  R={KERNEL_R}  |  "
                f"Step {step}  |  Mass: {mass:.0f}"
            )

            fig.canvas.draw_idle()
            plt.pause(0.001)

        # If everything died, re-seed
        if mass < 1.0:
            print(f"  Re-seeding at step {step} (mass={mass:.2f})")
            A = init_world(rng)

    plt.ioff()
    plt.close(fig)

    print(f"\n─── Finished after {step} steps ───")
    print(f"Final mass: {mass_history[-1]:.1f}")
    print(f"Mean mass (2nd half): {np.mean(mass_history[len(mass_history)//2:]):.1f}")


if __name__ == "__main__":
    run()
