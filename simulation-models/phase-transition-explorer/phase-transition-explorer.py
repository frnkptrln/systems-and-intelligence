#!/usr/bin/env python3
"""
Phase Transition Explorer – 2D Ising Model
---------------------------------------------

The Ising model is the simplest statistical-mechanics system that
exhibits a genuine **phase transition**: below a critical temperature
T_c ≈ 2.269 (Onsager, 1944), spins spontaneously align (order);
above T_c, thermal fluctuations destroy long-range order (disorder).

This simulation implements the **Metropolis–Hastings** algorithm on a
periodic 2D lattice:

    ΔE = 2 · s_i · Σ_{neighbours} s_j
    P(flip) = min(1, exp(-ΔE / T))

**Connection to the repository:**

- **Edge of Chaos (Axiom 2):** At T_c the system is poised between
  frozen order (H → 0) and total chaos (max H).  Information
  processing — correlations, fluctuations, susceptibility — peaks
  exactly at this critical point.

- **Self-Organized Criticality:** While the Ising model requires
  external tuning of T, it illustrates *why* criticality is special:
  the correlation length diverges, and the system becomes scale-free.

- **System Intelligence Index:** Near T_c, predictive power P is
  maximal (long-range correlations make the future informative),
  regulation R is fragile (the system sits on a knife-edge), and
  adaptive capacity A peaks (small perturbations propagate globally).

Controls:
    ←  / →     Decrease / increase temperature by 0.1
    r          Reset the grid
    ESC        Exit
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────
GRID_SIZE     = 128          # N×N spin lattice
T_INIT        = 2.5          # initial temperature
T_MIN         = 0.5
T_MAX         = 5.0
T_STEP        = 0.1
MC_STEPS      = 5            # full sweeps per frame
DISPLAY_EVERY = 1
MAX_FRAMES    = 20000

# Critical temperature (Onsager exact solution)
T_CRITICAL = 2.0 / np.log(1.0 + np.sqrt(2.0))  # ≈ 2.26918...


# ─────────────────────────────────────────────
# Initialisation
# ─────────────────────────────────────────────
def init_grid(N):
    """Random initial configuration: each spin ±1."""
    return np.random.choice([-1, 1], size=(N, N))


# ─────────────────────────────────────────────
# Metropolis sweep
# ─────────────────────────────────────────────
def metropolis_step(grid, T):
    """
    One full Monte Carlo sweep (N² random single-spin flips).
    Returns updated grid, total energy, and magnetisation.
    """
    N = grid.shape[0]
    beta = 1.0 / max(T, 1e-10)

    for _ in range(N * N):
        i = np.random.randint(N)
        j = np.random.randint(N)

        # Sum of four nearest neighbours (periodic boundaries)
        nb_sum = (
            grid[(i + 1) % N, j] +
            grid[(i - 1) % N, j] +
            grid[i, (j + 1) % N] +
            grid[i, (j - 1) % N]
        )

        dE = 2 * grid[i, j] * nb_sum

        if dE <= 0 or np.random.rand() < np.exp(-beta * dE):
            grid[i, j] *= -1

    # Compute observables
    energy = compute_energy(grid)
    mag = np.mean(grid)

    return grid, energy, mag


def compute_energy(grid):
    """Total energy: E = -Σ s_i · s_j (nearest neighbours)."""
    N = grid.shape[0]
    right  = np.roll(grid, -1, axis=1)
    down   = np.roll(grid, -1, axis=0)
    return -np.sum(grid * right + grid * down) / (N * N)


# ─────────────────────────────────────────────
# Phase diagram (pre-compute for reference line)
# ─────────────────────────────────────────────
def onsager_magnetisation(T):
    """Exact Onsager solution for spontaneous magnetisation (T < T_c)."""
    if T >= T_CRITICAL:
        return 0.0
    return (1.0 - np.sinh(2.0 / T) ** (-4)) ** (1.0 / 8.0)


# ─────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────
def run():
    grid = init_grid(GRID_SIZE)
    T = T_INIT

    # History buffers
    T_history   = []
    M_history   = []
    E_history   = []

    # ── Figure layout ────────────────────────
    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor("#0a0a1a")
    gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)

    # Spin grid (large, left)
    ax_grid = fig.add_subplot(gs[:, 0])
    im = ax_grid.imshow(grid, cmap="RdBu", vmin=-1, vmax=1,
                        interpolation="nearest", origin="lower")
    ax_grid.set_xticks([])
    ax_grid.set_yticks([])
    ax_grid.set_facecolor("#0a0a1a")

    title = ax_grid.set_title(
        f"T = {T:.2f}   (T_c ≈ {T_CRITICAL:.3f})",
        fontsize=13, color="#e0e0ff", fontweight="bold"
    )

    # Magnetisation time series
    ax_mag = fig.add_subplot(gs[0, 1])
    _style_axis(ax_mag, "Magnetisation |M|", "#60a0ff")
    line_mag, = ax_mag.plot([], [], color="#60a0ff", linewidth=1.2)
    ax_mag.set_ylim(-0.05, 1.05)
    ax_mag.axhline(y=0, color="#444", linewidth=0.5)

    # Energy time series
    ax_eng = fig.add_subplot(gs[1, 1])
    _style_axis(ax_eng, "Energy per spin E", "#ff6060")
    line_eng, = ax_eng.plot([], [], color="#ff6060", linewidth=1.2)

    # Phase diagram (right column)
    ax_phase = fig.add_subplot(gs[0, 2])
    _style_axis(ax_phase, "Phase Diagram  |M|(T)", "#80ffb0")
    T_exact = np.linspace(0.5, 4.5, 300)
    M_exact = [onsager_magnetisation(t) for t in T_exact]
    ax_phase.plot(T_exact, M_exact, color="#80ffb0", linewidth=1.5,
                  alpha=0.7, label="Onsager exact")
    ax_phase.axvline(x=T_CRITICAL, color="#ffcc44", linewidth=1,
                     linestyle="--", alpha=0.6, label=f"T_c ≈ {T_CRITICAL:.3f}")
    phase_dot, = ax_phase.plot([], [], "o", color="#ffffff", markersize=8, zorder=5)
    ax_phase.set_xlim(0.3, 4.7)
    ax_phase.set_ylim(-0.05, 1.05)
    ax_phase.set_xlabel("Temperature T", color="#999", fontsize=9)
    ax_phase.legend(fontsize=8, facecolor="#0e0e25", edgecolor="#333",
                    labelcolor="#bbb")

    # Specific heat proxy
    ax_cv = fig.add_subplot(gs[1, 2])
    _style_axis(ax_cv, "Energy Fluctuations (∝ C_v)", "#ffaa44")
    line_cv, = ax_cv.plot([], [], color="#ffaa44", linewidth=1.2)

    fig.tight_layout()

    # ── Controls ─────────────────────────────
    state = {"T": T, "stop": False, "reset": False}

    def on_key(event):
        if event.key in ("escape", "esc"):
            state["stop"] = True
        elif event.key == "right":
            state["T"] = min(T_MAX, state["T"] + T_STEP)
        elif event.key == "left":
            state["T"] = max(T_MIN, state["T"] - T_STEP)
        elif event.key == "r":
            state["reset"] = True

    fig.canvas.mpl_connect("key_press_event", on_key)

    plt.ion()

    # ── Main loop ────────────────────────────
    E_window = []  # sliding window for C_v proxy
    Cv_history = []

    for frame in range(MAX_FRAMES):
        if state["stop"]:
            break

        if state["reset"]:
            grid = init_grid(GRID_SIZE)
            T_history.clear()
            M_history.clear()
            E_history.clear()
            E_window.clear()
            Cv_history.clear()
            state["reset"] = False

        T = state["T"]

        # Monte Carlo sweeps
        for _ in range(MC_STEPS):
            grid, energy, mag = metropolis_step(grid, T)

        T_history.append(T)
        M_history.append(abs(mag))
        E_history.append(energy)

        # Specific heat proxy: variance of E in sliding window
        E_window.append(energy)
        if len(E_window) > 30:
            E_window.pop(0)
        Cv_history.append(np.var(E_window) / max(T * T, 1e-6))

        # ── Update plots ─────────────────────
        if frame % DISPLAY_EVERY == 0:
            im.set_data(grid)
            title.set_text(
                f"T = {T:.2f}   (T_c ≈ {T_CRITICAL:.3f})   |   "
                f"|M| = {abs(mag):.3f}   E = {energy:.3f}"
            )

            x_range = range(len(M_history))

            line_mag.set_data(x_range, M_history)
            ax_mag.set_xlim(0, max(10, len(M_history)))

            line_eng.set_data(x_range, E_history)
            ax_eng.set_xlim(0, max(10, len(E_history)))
            if E_history:
                emin, emax = min(E_history), max(E_history)
                ax_eng.set_ylim(emin - 0.1, emax + 0.1)

            phase_dot.set_data([T], [abs(mag)])

            line_cv.set_data(x_range, Cv_history)
            ax_cv.set_xlim(0, max(10, len(Cv_history)))
            if Cv_history:
                ax_cv.set_ylim(0, max(Cv_history) * 1.2 + 0.01)

            fig.canvas.draw_idle()
            plt.pause(0.001)

    plt.ioff()
    plt.close(fig)
    print(f"\n─── Finished after {frame + 1} frames ───")
    print(f"Final T = {T:.2f},  |M| = {abs(mag):.3f},  E = {energy:.3f}")


def _style_axis(ax, title, color):
    """Apply dark theme styling to an axis."""
    ax.set_facecolor("#0e0e25")
    ax.set_title(title, fontsize=10, color=color, fontweight="bold")
    ax.tick_params(colors="#666", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#333")
    ax.grid(True, alpha=0.15, color="#555")


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════╗")
    print("║   Phase Transition Explorer – 2D Ising Model    ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║  ← / →   Change temperature                    ║")
    print("║  r        Reset grid                            ║")
    print("║  ESC      Exit                                  ║")
    print("║                                                 ║")
    print("║  Watch how the system transitions between       ║")
    print("║  ORDER (T < T_c) and DISORDER (T > T_c).       ║")
    print("║  At T_c ≈ 2.269, criticality emerges:          ║")
    print("║  correlations diverge, the system becomes       ║")
    print("║  scale-free – the Edge of Chaos.                ║")
    print("╚══════════════════════════════════════════════════╝")
    run()
