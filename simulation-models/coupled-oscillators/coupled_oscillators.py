#!/usr/bin/env python3
"""
Coupled Oscillators – Emergent Synchronisation (Kuramoto Model)
---------------------------------------------------------------

N oscillators, each with its own natural frequency, are coupled via
sin-based phase interactions.  Below a critical coupling strength K_c
they remain incoherent; above it they spontaneously synchronise –
a phase transition to collective order.

The simulation tracks the **order parameter** r(t) ∈ [0, 1]:
  r = 0  → fully incoherent
  r = 1  → perfectly synchronised

Visualisation (matplotlib):
  Left  – unit circle with oscillator phases as dots
  Right – order parameter r(t) over time

Press ESC to exit.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────
N_OSCILLATORS = 80              # number of oscillators
K_COUPLING    = 2.5             # coupling strength (try 0.5 … 4.0)
DT            = 0.05            # integration time step
MAX_STEPS     = 6000
DISPLAY_EVERY = 3

# Natural frequency distribution (Lorentzian / Cauchy centred at 0)
FREQ_SPREAD   = 1.0
SEED          = 42

# ─────────────────────────────────────────────
# Kuramoto dynamics
# ─────────────────────────────────────────────

def kuramoto_step(theta, omega, K, dt):
    """
    One Euler step of the Kuramoto model:
        dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j − θ_i)
    """
    N = len(theta)
    # Use the mean-field formulation for efficiency:
    #   r * exp(i ψ) = (1/N) Σ exp(i θ_j)
    # then the coupling term becomes  K r sin(ψ − θ_i)
    z = np.exp(1j * theta)
    mean_field = z.mean()
    r = np.abs(mean_field)
    psi = np.angle(mean_field)

    dtheta = omega + K * r * np.sin(psi - theta)
    theta_new = theta + dt * dtheta
    return theta_new, r, psi


def order_parameter(theta):
    """Compute r and ψ from the phase array."""
    z = np.exp(1j * theta).mean()
    return np.abs(z), np.angle(z)


# ─────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────

def run():
    rng = np.random.default_rng(SEED)

    # Natural frequencies (Cauchy / Lorentzian distribution)
    omega = FREQ_SPREAD * np.tan(np.pi * (rng.random(N_OSCILLATORS) - 0.5))

    # Initial phases uniformly in [0, 2π)
    theta = rng.uniform(0, 2 * np.pi, N_OSCILLATORS)

    r_history = []

    # ── Matplotlib setup ──
    plt.ion()
    fig, (ax_circle, ax_r) = plt.subplots(
        1, 2, figsize=(13, 5.5),
        gridspec_kw={"width_ratios": [1, 1.6]}
    )

    # Left: unit circle
    ax_circle.set_xlim(-1.45, 1.45)
    ax_circle.set_ylim(-1.45, 1.45)
    ax_circle.set_aspect("equal")
    ax_circle.add_patch(Circle((0, 0), 1.0, fill=False, color="gray",
                               linewidth=0.8, linestyle="--"))
    phase_dots, = ax_circle.plot([], [], "o", markersize=4,
                                  color="steelblue", alpha=0.7)
    mean_arrow = ax_circle.annotate(
        "", xy=(0, 0), xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", color="crimson", lw=2.2)
    )
    ax_circle.set_title("Phase Distribution", fontsize=10)
    ax_circle.set_xticks([])
    ax_circle.set_yticks([])

    # Right: order parameter time series
    r_line, = ax_r.plot([], [], color="crimson", linewidth=1.0)
    ax_r.set_xlim(0, MAX_STEPS * DT)
    ax_r.set_ylim(0, 1.05)
    ax_r.set_xlabel("Time")
    ax_r.set_ylabel("Order Parameter r")
    ax_r.set_title(f"Synchronisation  (K = {K_COUPLING},  N = {N_OSCILLATORS})",
                   fontsize=10)
    ax_r.axhline(1.0, color="gray", linestyle=":", alpha=0.3)
    ax_r.grid(True, alpha=0.3)

    suptitle = fig.suptitle("Coupled Oscillators — Kuramoto Model", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])

    exit_flag = {"stop": False}
    def on_key(event):
        if event.key in ("escape", "esc"):
            exit_flag["stop"] = True
    fig.canvas.mpl_connect("key_press_event", on_key)

    # ── Simulation loop ──
    for step in range(1, MAX_STEPS + 1):
        if exit_flag["stop"]:
            print("\nSimulation beendet (ESC).")
            break

        theta, r, psi = kuramoto_step(theta, omega, K_COUPLING, DT)
        r_history.append(r)

        if step % DISPLAY_EVERY == 0:
            # Phase dots on unit circle
            x = np.cos(theta)
            y = np.sin(theta)
            phase_dots.set_data(x, y)

            # Mean-field arrow
            mean_arrow.remove()
            rx, ry = r * np.cos(psi), r * np.sin(psi)
            mean_arrow = ax_circle.annotate(
                f"r={r:.2f}",
                xy=(rx, ry), xytext=(0, 0),
                fontsize=8, color="crimson", fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="crimson", lw=2.2),
            )

            # r(t) curve
            times = np.arange(len(r_history)) * DT
            r_line.set_data(times, r_history)

            suptitle.set_text(
                f"Coupled Oscillators — Kuramoto Model  |  "
                f"Step {step}  |  r = {r:.3f}"
            )

            fig.canvas.draw_idle()
            plt.pause(0.001)

    plt.ioff()
    plt.close(fig)

    # ── Summary ──
    print(f"\n─── Results ───")
    print(f"Final order parameter r = {r_history[-1]:.4f}")
    half = len(r_history) // 2
    print(f"Mean r (2nd half):        {np.mean(r_history[half:]):.4f}")
    if np.mean(r_history[half:]) > 0.5:
        print("→ The oscillators have synchronised (emergent order).")
    else:
        print("→ The oscillators remain incoherent. Try increasing K_COUPLING.")


if __name__ == "__main__":
    run()
