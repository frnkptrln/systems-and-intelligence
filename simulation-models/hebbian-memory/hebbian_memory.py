#!/usr/bin/env python3
"""
Hebbian Memory – Self-Organizing Associative Memory (Hopfield Network)
-----------------------------------------------------------------------

A network of N binary neurons (±1) stores patterns via Hebb's rule:
    W += pattern ⊗ pattern  (outer product)

Given a noisy or partial input, the network relaxes to the nearest
stored attractor – pattern completion emerges from purely local update
rules with no external teacher.

The simulation shows:
  - Stored patterns (8×8 pixel icons)
  - Noisy input pattern
  - Step-by-step convergence to a recalled pattern
  - Energy landscape descent

Press ESC in the matplotlib window to exit early.
"""

import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────
PATTERN_SIZE = 8            # each pattern is PATTERN_SIZE × PATTERN_SIZE
NUM_PATTERNS = 4            # number of patterns to store
NOISE_LEVEL  = 0.30         # fraction of flipped bits in the probe
MAX_RECALL_STEPS = 30       # max async update sweeps
DISPLAY_PAUSE    = 0.35     # seconds between convergence frames
SEED = 42

# ─────────────────────────────────────────────
# Hand-crafted 8×8 patterns (iconic shapes)
# ─────────────────────────────────────────────
# +1 = "on" (white), -1 = "off" (black)
# These are more recognisable than random patterns.

LETTER_T = [
    [+1,+1,+1,+1,+1,+1,+1,+1],
    [+1,+1,+1,+1,+1,+1,+1,+1],
    [-1,-1,-1,+1,+1,-1,-1,-1],
    [-1,-1,-1,+1,+1,-1,-1,-1],
    [-1,-1,-1,+1,+1,-1,-1,-1],
    [-1,-1,-1,+1,+1,-1,-1,-1],
    [-1,-1,-1,+1,+1,-1,-1,-1],
    [-1,-1,-1,+1,+1,-1,-1,-1],
]

LETTER_X = [
    [+1,-1,-1,-1,-1,-1,-1,+1],
    [-1,+1,-1,-1,-1,-1,+1,-1],
    [-1,-1,+1,-1,-1,+1,-1,-1],
    [-1,-1,-1,+1,+1,-1,-1,-1],
    [-1,-1,-1,+1,+1,-1,-1,-1],
    [-1,-1,+1,-1,-1,+1,-1,-1],
    [-1,+1,-1,-1,-1,-1,+1,-1],
    [+1,-1,-1,-1,-1,-1,-1,+1],
]

CHECKER = [
    [+1,-1,+1,-1,+1,-1,+1,-1],
    [-1,+1,-1,+1,-1,+1,-1,+1],
    [+1,-1,+1,-1,+1,-1,+1,-1],
    [-1,+1,-1,+1,-1,+1,-1,+1],
    [+1,-1,+1,-1,+1,-1,+1,-1],
    [-1,+1,-1,+1,-1,+1,-1,+1],
    [+1,-1,+1,-1,+1,-1,+1,-1],
    [-1,+1,-1,+1,-1,+1,-1,+1],
]

DIAMOND = [
    [-1,-1,-1,+1,+1,-1,-1,-1],
    [-1,-1,+1,+1,+1,+1,-1,-1],
    [-1,+1,+1,-1,-1,+1,+1,-1],
    [+1,+1,-1,-1,-1,-1,+1,+1],
    [+1,+1,-1,-1,-1,-1,+1,+1],
    [-1,+1,+1,-1,-1,+1,+1,-1],
    [-1,-1,+1,+1,+1,+1,-1,-1],
    [-1,-1,-1,+1,+1,-1,-1,-1],
]

BUILT_IN_PATTERNS = [LETTER_T, LETTER_X, CHECKER, DIAMOND]
PATTERN_NAMES     = ["T", "X", "Checker", "Diamond"]


# ─────────────────────────────────────────────
# Hopfield network
# ─────────────────────────────────────────────

class HopfieldNetwork:
    """Binary Hopfield network with Hebbian learning."""

    def __init__(self, n_neurons):
        self.N = n_neurons
        self.W = np.zeros((n_neurons, n_neurons), dtype=np.float64)
        self.patterns = []

    def store(self, pattern):
        """Store a pattern via the Hebb rule: W += p ⊗ p / N."""
        p = pattern.flatten().astype(np.float64)
        assert p.shape[0] == self.N
        self.patterns.append(p.copy())
        self.W += np.outer(p, p) / self.N
        np.fill_diagonal(self.W, 0)  # no self-connections

    def energy(self, state):
        """Hopfield energy: E = -½ sᵀ W s."""
        s = state.flatten().astype(np.float64)
        return -0.5 * s @ self.W @ s

    def update_async(self, state, rng):
        """One full asynchronous sweep: update every neuron once in random order."""
        s = state.flatten().copy()
        order = rng.permutation(self.N)
        for i in order:
            h = self.W[i] @ s
            s[i] = 1.0 if h >= 0 else -1.0
        return s

    def recall(self, probe, rng, max_steps=MAX_RECALL_STEPS):
        """
        Run the network from a probe state until convergence.
        Returns list of (state, energy) at each step.
        """
        s = probe.flatten().copy()
        trajectory = [(s.copy(), self.energy(s))]

        for _ in range(max_steps):
            s_new = self.update_async(s, rng)
            e_new = self.energy(s_new)
            trajectory.append((s_new.copy(), e_new))
            if np.array_equal(s_new, s):
                break  # fixed point
            s = s_new

        return trajectory

    def overlap(self, state):
        """Compute overlap (cosine) with each stored pattern."""
        s = state.flatten()
        overlaps = []
        for p in self.patterns:
            overlaps.append(np.dot(s, p) / self.N)
        return overlaps


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def add_noise(pattern, noise_level, rng):
    """Flip a fraction of bits in a ±1 pattern."""
    p = pattern.flatten().copy()
    n_flip = int(noise_level * len(p))
    flip_idx = rng.choice(len(p), size=n_flip, replace=False)
    p[flip_idx] *= -1
    return p


# ─────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────

def run():
    rng = np.random.default_rng(SEED)
    N = PATTERN_SIZE * PATTERN_SIZE
    net = HopfieldNetwork(N)

    # Store patterns
    patterns = [np.array(p) for p in BUILT_IN_PATTERNS[:NUM_PATTERNS]]
    for p in patterns:
        net.store(p)

    print(f"Stored {len(patterns)} patterns in a {N}-neuron Hopfield network.\n")

    # ── Figure layout ──
    # Row 1: stored patterns
    # Row 2: noisy probe → convergence animation → final state
    # Row 3: energy curve + overlap bar chart
    n_stored = len(patterns)

    plt.ion()
    fig = plt.figure(figsize=(14, 9))
    fig.suptitle("Hebbian Memory – Hopfield Network", fontsize=13)

    # Row 1: stored patterns
    axes_stored = []
    for i in range(n_stored):
        ax = fig.add_subplot(3, max(n_stored, 4), i + 1)
        ax.imshow(patterns[i], cmap="gray_r", vmin=-1, vmax=1,
                  interpolation="nearest")
        ax.set_title(f"Stored: {PATTERN_NAMES[i]}", fontsize=9)
        ax.set_xticks([]); ax.set_yticks([])
        axes_stored.append(ax)

    # Row 2: probe | current state | recalled
    ax_probe = fig.add_subplot(3, 4, 5)
    ax_probe.set_title("Noisy Probe", fontsize=9)
    ax_probe.set_xticks([]); ax_probe.set_yticks([])

    ax_current = fig.add_subplot(3, 4, 6)
    ax_current.set_title("Current State", fontsize=9)
    ax_current.set_xticks([]); ax_current.set_yticks([])

    ax_recalled = fig.add_subplot(3, 4, 7)
    ax_recalled.set_title("Recalled", fontsize=9)
    ax_recalled.set_xticks([]); ax_recalled.set_yticks([])

    ax_info = fig.add_subplot(3, 4, 8)
    ax_info.axis("off")

    # Row 3: energy + overlap
    ax_energy = fig.add_subplot(3, 2, 5)
    ax_energy.set_xlabel("Update sweep")
    ax_energy.set_ylabel("Energy")
    ax_energy.grid(True, alpha=0.3)

    ax_overlap = fig.add_subplot(3, 2, 6)
    ax_overlap.set_ylabel("Overlap")
    ax_overlap.set_ylim(-1.1, 1.1)
    ax_overlap.axhline(0, color="gray", lw=0.5)
    ax_overlap.grid(True, alpha=0.3)

    fig.tight_layout(rect=[0, 0, 1, 0.95])

    # ESC handler
    exit_flag = {"stop": False}
    def on_key(event):
        if event.key in ("escape", "esc"):
            exit_flag["stop"] = True
    fig.canvas.mpl_connect("key_press_event", on_key)

    # ── Run recall for each pattern ──
    for pi, (pat, name) in enumerate(zip(patterns, PATTERN_NAMES)):
        if exit_flag["stop"]:
            break

        probe = add_noise(pat, NOISE_LEVEL, rng)
        trajectory = net.recall(probe, rng)

        # Show probe
        im_probe = ax_probe.imshow(
            probe.reshape(PATTERN_SIZE, PATTERN_SIZE),
            cmap="gray_r", vmin=-1, vmax=1, interpolation="nearest"
        )
        ax_probe.set_title(f"Noisy Probe ({name}, {NOISE_LEVEL:.0%} noise)",
                           fontsize=9)

        # Animate convergence
        energies = []
        for step_i, (state, energy) in enumerate(trajectory):
            if exit_flag["stop"]:
                break

            grid = state.reshape(PATTERN_SIZE, PATTERN_SIZE)
            energies.append(energy)

            # Current state
            ax_current.clear()
            ax_current.imshow(grid, cmap="gray_r", vmin=-1, vmax=1,
                              interpolation="nearest")
            ax_current.set_title(f"Sweep {step_i}", fontsize=9)
            ax_current.set_xticks([]); ax_current.set_yticks([])

            # Energy plot
            ax_energy.clear()
            ax_energy.plot(energies, "o-", color="crimson", markersize=3,
                           linewidth=1.2)
            ax_energy.set_xlabel("Update sweep")
            ax_energy.set_ylabel("Energy")
            ax_energy.set_title("Energy descent", fontsize=9)
            ax_energy.grid(True, alpha=0.3)

            # Overlap bar
            overlaps = net.overlap(state)
            ax_overlap.clear()
            colors = ["#3b82f6", "#f59e0b", "#10b981", "#ef4444"]
            ax_overlap.bar(PATTERN_NAMES[:len(overlaps)], overlaps,
                           color=colors[:len(overlaps)], edgecolor="white",
                           linewidth=0.5)
            ax_overlap.set_ylim(-1.1, 1.1)
            ax_overlap.axhline(0, color="gray", lw=0.5)
            ax_overlap.set_ylabel("Overlap")
            ax_overlap.set_title("Pattern overlap", fontsize=9)
            ax_overlap.grid(True, alpha=0.3, axis="y")

            fig.canvas.draw_idle()
            plt.pause(DISPLAY_PAUSE)

        if exit_flag["stop"]:
            break

        # Final recalled state
        final_state = trajectory[-1][0].reshape(PATTERN_SIZE, PATTERN_SIZE)
        ax_recalled.clear()
        ax_recalled.imshow(final_state, cmap="gray_r", vmin=-1, vmax=1,
                           interpolation="nearest")

        # Identify best match
        final_overlaps = net.overlap(trajectory[-1][0])
        best_idx = int(np.argmax(np.abs(final_overlaps)))
        best_name = PATTERN_NAMES[best_idx]
        best_ov = final_overlaps[best_idx]
        ax_recalled.set_title(f"Recalled: {best_name} ({best_ov:+.2f})",
                              fontsize=9)
        ax_recalled.set_xticks([]); ax_recalled.set_yticks([])

        # Info box
        ax_info.clear(); ax_info.axis("off")
        info_text = (
            f"Pattern: {name}\n"
            f"Noise: {NOISE_LEVEL:.0%}\n"
            f"Steps to converge: {len(trajectory) - 1}\n"
            f"Best match: {best_name}\n"
            f"Overlap: {best_ov:+.3f}\n"
            f"Correct: {'✓' if best_name == name else '✗'}"
        )
        ax_info.text(0.1, 0.5, info_text, transform=ax_info.transAxes,
                     fontsize=10, verticalalignment="center",
                     fontfamily="monospace",
                     bbox=dict(boxstyle="round", facecolor="#1e293b",
                               edgecolor="#334155", alpha=0.9),
                     color="#e5e7eb")

        print(f"  {name}: converged in {len(trajectory)-1} sweeps → "
              f"recalled {best_name} (overlap {best_ov:+.3f})")

        fig.canvas.draw_idle()
        plt.pause(2.0)  # pause between patterns

    plt.ioff()
    if not exit_flag["stop"]:
        print("\nAll patterns recalled. Close the window to exit.")
        plt.show()
    else:
        print("\nSimulation beendet (ESC).")
        plt.close(fig)


if __name__ == "__main__":
    run()
