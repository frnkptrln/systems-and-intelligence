#!/usr/bin/env python3
"""
Self-Organized Criticality – Bak-Tang-Wiesenfeld Sandpile
-----------------------------------------------------------

The BTW sandpile (Bak, Tang & Wiesenfeld, 1987) is the canonical model
of self-organized criticality (SOC): the system drives itself to a
critical state where avalanches of all sizes occur, following a
**power-law distribution**.

Rules:
  1. Drop a grain of sand on a random cell.
  2. If any cell has ≥ 4 grains, it topples:
     - loses 4 grains
     - each of its 4 neighbours gains 1 grain
  3. Toppling can cascade (avalanches).
  4. Grains falling off the edge are lost.
  5. Record avalanche size = total number of topplings.

After a transient, the system reaches a critical state where:
  - Small avalanches are frequent, large ones rare
  - The size distribution follows P(s) ~ s^(-τ) with τ ≈ 1.1-1.3
  - This power law emerges WITHOUT tuning any parameter

This is the same statistics seen in earthquakes (Gutenberg-Richter law),
forest fires, neural avalanches, and financial crashes.

Press ESC in the matplotlib window to exit.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from collections import deque

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────
GRID_SIZE       = 64            # NxN sandpile
NUM_GRAINS      = 80000         # total grains to drop
DISPLAY_EVERY   = 200           # refresh display every N grain drops
WARMUP_GRAINS   = 5000          # ignore avalanches during transient
SEED            = 42

# ─────────────────────────────────────────────
# Sandpile colourmap (sand tones)
# ─────────────────────────────────────────────
_CMAP = LinearSegmentedColormap.from_list("sandpile", [
    (0.00, (0.12, 0.10, 0.08)),     # dark earth
    (0.25, (0.55, 0.42, 0.25)),     # brown sand
    (0.50, (0.85, 0.72, 0.45)),     # warm sand
    (0.75, (0.95, 0.88, 0.65)),     # light sand
    (1.00, (1.00, 0.98, 0.90)),     # near-white
], N=256)

# ─────────────────────────────────────────────
# Sandpile model
# ─────────────────────────────────────────────

class Sandpile:
    """Bak-Tang-Wiesenfeld sandpile on a finite grid with open boundaries."""

    THRESHOLD = 4  # topple when height >= 4

    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size), dtype=np.int64)
        self.total_grains_dropped = 0

    def drop_grain(self, row, col):
        """Drop one grain and return avalanche size (total topplings)."""
        self.grid[row, col] += 1
        self.total_grains_dropped += 1
        return self._relax()

    def _relax(self):
        """
        Topple all unstable cells until the pile is stable.
        Returns total number of topplings (= avalanche size).
        """
        total_topplings = 0

        while True:
            unstable = self.grid >= self.THRESHOLD
            if not unstable.any():
                break

            # Count topplings this round
            n = unstable.sum()
            total_topplings += n

            # Topple: each unstable cell loses 4, neighbours each gain 1
            topple_count = self.grid // self.THRESHOLD  # how many times each cell topples
            topple_mask = topple_count > 0

            self.grid -= topple_count * 4

            # Distribute to neighbours (with boundary loss)
            # Up
            self.grid[1:, :]  += topple_count[:-1, :]
            # Down
            self.grid[:-1, :] += topple_count[1:, :]
            # Left
            self.grid[:, 1:]  += topple_count[:, :-1]
            # Right
            self.grid[:, :-1] += topple_count[:, 1:]

        return total_topplings


# ─────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────

def run():
    rng = np.random.default_rng(SEED)
    pile = Sandpile(GRID_SIZE)
    avalanche_sizes = []

    plt.ion()
    fig, (ax_pile, ax_dist) = plt.subplots(
        1, 2, figsize=(14, 6),
        gridspec_kw={"width_ratios": [1, 1.2]}
    )

    # Left: sandpile state
    im = ax_pile.imshow(
        pile.grid, cmap=_CMAP,
        interpolation="nearest",
        vmin=0, vmax=3,
        origin="lower"
    )
    ax_pile.set_title("Sandpile State", fontsize=10)
    ax_pile.set_xticks([]); ax_pile.set_yticks([])
    cbar = fig.colorbar(im, ax=ax_pile, fraction=0.046, pad=0.04)
    cbar.set_label("Grains", fontsize=9)

    # Right: avalanche size distribution (log-log)
    ax_dist.set_xlabel("Avalanche size s", fontsize=10)
    ax_dist.set_ylabel("Frequency P(s)", fontsize=10)
    ax_dist.set_title("Avalanche Size Distribution", fontsize=10)
    ax_dist.set_xscale("log")
    ax_dist.set_yscale("log")
    ax_dist.grid(True, alpha=0.2, which="both")

    suptitle = fig.suptitle(
        "Self-Organized Criticality – Bak-Tang-Wiesenfeld Sandpile",
        fontsize=12
    )
    fig.tight_layout(rect=[0, 0, 1, 0.94])

    exit_flag = {"stop": False}
    def on_key(event):
        if event.key in ("escape", "esc"):
            exit_flag["stop"] = True
    fig.canvas.mpl_connect("key_press_event", on_key)

    max_avalanche = 0

    for grain_i in range(1, NUM_GRAINS + 1):
        if exit_flag["stop"]:
            print("\nSimulation beendet (ESC).")
            break

        # Drop grain at random position
        r = rng.integers(0, GRID_SIZE)
        c = rng.integers(0, GRID_SIZE)
        aval_size = pile.drop_grain(r, c)

        # Record avalanche (skip warmup transient)
        if grain_i > WARMUP_GRAINS and aval_size > 0:
            avalanche_sizes.append(aval_size)
            max_avalanche = max(max_avalanche, aval_size)

        # Update display
        if grain_i % DISPLAY_EVERY == 0:
            im.set_data(pile.grid)
            im.set_clim(vmin=0, vmax=max(3, pile.grid.max()))

            # Update distribution plot
            ax_dist.clear()
            if len(avalanche_sizes) > 50:
                sizes = np.array(avalanche_sizes)

                # Logarithmic binning for cleaner power law
                max_s = sizes.max()
                if max_s > 1:
                    bins = np.logspace(0, np.log10(max_s), 40)
                    counts, edges = np.histogram(sizes, bins=bins)
                    bin_centres = np.sqrt(edges[:-1] * edges[1:])
                    mask = counts > 0
                    if mask.sum() > 2:
                        # Normalise to PDF
                        widths = edges[1:] - edges[:-1]
                        pdf = counts / (widths * len(sizes))

                        ax_dist.scatter(
                            bin_centres[mask], pdf[mask],
                            c="#e07040", s=30, edgecolors="#8a3020",
                            linewidths=0.5, zorder=5, alpha=0.8
                        )

                        # Fit power law: log(P) = -τ log(s) + C
                        log_s = np.log10(bin_centres[mask])
                        log_p = np.log10(pdf[mask])
                        if len(log_s) >= 3:
                            coeffs = np.polyfit(log_s, log_p, 1)
                            tau = -coeffs[0]
                            fit_y = 10 ** np.polyval(coeffs, log_s)
                            ax_dist.plot(
                                bin_centres[mask], fit_y,
                                "--", color="#60a5fa", linewidth=1.5,
                                label=f"Power law: τ ≈ {tau:.2f}"
                            )
                            ax_dist.legend(fontsize=9, loc="upper right")

            ax_dist.set_xlabel("Avalanche size s")
            ax_dist.set_ylabel("Frequency P(s)")
            ax_dist.set_title(
                f"Avalanche Distribution  (n={len(avalanche_sizes)})",
                fontsize=10
            )
            ax_dist.set_xscale("log")
            ax_dist.set_yscale("log")
            ax_dist.grid(True, alpha=0.2, which="both")

            suptitle.set_text(
                f"Self-Organized Criticality  |  "
                f"Grains: {grain_i}/{NUM_GRAINS}  |  "
                f"Max avalanche: {max_avalanche}"
            )

            fig.canvas.draw_idle()
            plt.pause(0.001)

    plt.ioff()
    plt.close(fig)

    # ── Summary ──
    if avalanche_sizes:
        sizes = np.array(avalanche_sizes)
        print(f"\n─── Results ───")
        print(f"Total avalanches recorded: {len(sizes)}")
        print(f"Mean size:    {sizes.mean():.1f}")
        print(f"Median size:  {np.median(sizes):.0f}")
        print(f"Max size:     {sizes.max()}")
        print(f"Avalanches > 100: {(sizes > 100).sum()}")

        # Power-law fit
        max_s = sizes.max()
        if max_s > 1:
            bins = np.logspace(0, np.log10(max_s), 40)
            counts, edges = np.histogram(sizes, bins=bins)
            bin_centres = np.sqrt(edges[:-1] * edges[1:])
            mask = counts > 0
            if mask.sum() >= 3:
                widths = edges[1:] - edges[:-1]
                pdf = counts / (widths * len(sizes))
                log_s = np.log10(bin_centres[mask])
                log_p = np.log10(pdf[mask])
                coeffs = np.polyfit(log_s, log_p, 1)
                tau = -coeffs[0]
                print(f"\nPower-law exponent τ ≈ {tau:.2f}")
                if 0.8 < tau < 2.0:
                    print("→ Consistent with self-organized criticality!")
                else:
                    print("→ Exponent outside typical SOC range. "
                          "Try more grains or a larger grid.")


if __name__ == "__main__":
    run()
