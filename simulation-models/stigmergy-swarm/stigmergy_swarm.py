#!/usr/bin/env python3
"""
Stigmergy Swarm – Collective Intelligence Through Pheromone Trails
-------------------------------------------------------------------

Ant-like agents search for food on a 2D grid.
They communicate indirectly by depositing pheromone that diffuses and
evaporates over time.  No agent knows the global state – yet efficient
paths from nest to food emerge from purely local rules.

Key concepts:
  - Stigmergy (indirect communication via the environment)
  - Self-organization without central control
  - Emergent path optimization

Press ESC in the matplotlib window to exit.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────
GRID_SIZE       = 80
NUM_AGENTS      = 60
NUM_FOOD        = 5
FOOD_AMOUNT     = 150          # units per food source
PHEROMONE_DROP  = 1.0          # amount deposited per step when carrying food
EVAPORATION     = 0.02         # fraction lost per step
DIFFUSION       = 0.12         # fraction diffused to neighbours per step
PHEROMONE_BIAS  = 8.0          # how strongly pheromone attracts
MAX_STEPS       = 4000
DISPLAY_EVERY   = 2            # render every N steps
SEED            = 42

# ─────────────────────────────────────────────
# World setup
# ─────────────────────────────────────────────

def make_world(rng):
    """Create pheromone grid, nest position, and food sources."""
    pheromone = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.float64)
    nest = np.array([GRID_SIZE // 2, GRID_SIZE // 2])

    # Random food positions (not too close to nest)
    foods = []
    while len(foods) < NUM_FOOD:
        pos = rng.integers(5, GRID_SIZE - 5, size=2)
        if np.linalg.norm(pos - nest) > GRID_SIZE // 4:
            foods.append({"pos": pos, "amount": FOOD_AMOUNT})

    return pheromone, nest, foods


# ─────────────────────────────────────────────
# Agent logic
# ─────────────────────────────────────────────

DIRECTIONS = np.array([
    [-1, -1], [-1, 0], [-1, 1],
    [ 0, -1],          [ 0, 1],
    [ 1, -1], [ 1, 0], [ 1, 1],
], dtype=int)


class Agent:
    __slots__ = ("pos", "carrying", "heading")

    def __init__(self, nest, rng):
        self.pos = nest.copy()
        self.carrying = False
        self.heading = rng.integers(0, 8)  # index into DIRECTIONS

    # ── movement helpers ──────────────────────

    @staticmethod
    def _clamp(v, lo, hi):
        return max(lo, min(hi, v))

    def _neighbours(self):
        """Return valid neighbour positions and their direction indices."""
        nbrs, idxs = [], []
        for i, d in enumerate(DIRECTIONS):
            nr, nc = self.pos[0] + d[0], self.pos[1] + d[1]
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                nbrs.append((nr, nc))
                idxs.append(i)
        return nbrs, idxs

    # ── main step ─────────────────────────────

    def step(self, pheromone, nest, foods, rng):
        if self.carrying:
            self._return_to_nest(pheromone, nest)
        else:
            self._search(pheromone, foods, rng)

    def _search(self, pheromone, foods, rng):
        """Move biased by pheromone; pick up food if found."""
        # Check for food at current position
        for f in foods:
            if f["amount"] > 0 and np.array_equal(self.pos, f["pos"]):
                f["amount"] -= 1
                self.carrying = True
                return

        nbrs, idxs = self._neighbours()
        if not nbrs:
            return

        # Probability proportional to pheromone + small baseline
        weights = np.array([
            pheromone[r, c] * PHEROMONE_BIAS + 0.1 for r, c in nbrs
        ])

        # Slight forward bias (persistence)
        for k, idx in enumerate(idxs):
            if idx == self.heading:
                weights[k] *= 1.5

        weights /= weights.sum()
        choice = rng.choice(len(nbrs), p=weights)
        self.pos = np.array(nbrs[choice])
        self.heading = idxs[choice]

    def _return_to_nest(self, pheromone, nest):
        """Move straight toward nest, dropping pheromone."""
        pheromone[self.pos[0], self.pos[1]] += PHEROMONE_DROP

        diff = nest - self.pos
        # Step one cell toward nest
        step = np.sign(diff)
        self.pos = np.clip(self.pos + step, 0, GRID_SIZE - 1)

        if np.array_equal(self.pos, nest):
            self.carrying = False


# ─────────────────────────────────────────────
# Pheromone dynamics
# ─────────────────────────────────────────────

def pheromone_update(pheromone):
    """Evaporate and diffuse the pheromone field."""
    # Evaporation
    pheromone *= (1.0 - EVAPORATION)

    # Simple diffusion via averaging with neighbours
    padded = np.pad(pheromone, 1, mode="constant", constant_values=0)
    diffused = (
        padded[:-2, 1:-1] + padded[2:, 1:-1] +
        padded[1:-1, :-2] + padded[1:-1, 2:]
    ) / 4.0
    pheromone[:] = (1.0 - DIFFUSION) * pheromone + DIFFUSION * diffused


# ─────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────

def run():
    rng = np.random.default_rng(SEED)
    pheromone, nest, foods = make_world(rng)
    agents = [Agent(nest, rng) for _ in range(NUM_AGENTS)]

    plt.ion()
    fig, ax = plt.subplots(figsize=(7, 7))

    # Pheromone background – log-scale for visibility
    im = ax.imshow(
        pheromone,
        cmap="YlOrBr",
        interpolation="bilinear",
        vmin=0, vmax=1,
        origin="lower",
    )

    # Overlay scatter layers
    food_sc = ax.scatter([], [], c="limegreen", s=90, marker="D",
                         edgecolors="darkgreen", linewidths=0.8, zorder=3,
                         label="Food")
    nest_sc = ax.scatter([nest[1]], [nest[0]], c="royalblue", s=200,
                         marker="s", edgecolors="navy", linewidths=1.2,
                         zorder=4, label="Nest")
    search_sc = ax.scatter([], [], c="white", s=12, zorder=5, alpha=0.85)
    carry_sc  = ax.scatter([], [], c="red", s=18, zorder=5, alpha=0.9)

    ax.set_xlim(-0.5, GRID_SIZE - 0.5)
    ax.set_ylim(-0.5, GRID_SIZE - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper right", fontsize=8, framealpha=0.7)
    title = ax.set_title("Stigmergy Swarm – Step 0", fontsize=11)
    fig.tight_layout()

    # ESC handler
    exit_flag = {"stop": False}
    def on_key(event):
        if event.key in ("escape", "esc"):
            exit_flag["stop"] = True
    fig.canvas.mpl_connect("key_press_event", on_key)

    collected_total = 0
    total_food = sum(f["amount"] for f in foods)

    for step in range(1, MAX_STEPS + 1):
        if exit_flag["stop"]:
            print("\nSimulation beendet (ESC).")
            break

        prev_food = sum(f["amount"] for f in foods)

        # Agents act
        for a in agents:
            a.step(pheromone, nest, foods, rng)

        collected_total += prev_food - sum(f["amount"] for f in foods)

        # Pheromone dynamics
        pheromone_update(pheromone)

        # ── Render ──
        if step % DISPLAY_EVERY == 0:
            display_data = np.log1p(pheromone * 5)
            vmax = max(display_data.max(), 0.01)
            im.set_data(display_data)
            im.set_clim(vmin=0, vmax=vmax)

            # Food positions (only those with remaining amount)
            active_foods = [f for f in foods if f["amount"] > 0]
            if active_foods:
                fpos = np.array([f["pos"] for f in active_foods])
                food_sc.set_offsets(np.c_[fpos[:, 1], fpos[:, 0]])
            else:
                food_sc.set_offsets(np.empty((0, 2)))

            # Agent positions
            searching = [(a.pos[1], a.pos[0]) for a in agents if not a.carrying]
            carrying  = [(a.pos[1], a.pos[0]) for a in agents if a.carrying]

            search_sc.set_offsets(searching if searching else np.empty((0, 2)))
            carry_sc.set_offsets(carrying if carrying else np.empty((0, 2)))

            pct = collected_total / total_food * 100
            title.set_text(
                f"Stigmergy Swarm — Step {step}  |  "
                f"Collected: {collected_total}/{total_food} ({pct:.0f}%)"
            )

            fig.canvas.draw_idle()
            plt.pause(0.001)

        # Stop when all food collected
        if collected_total >= total_food:
            print(f"\nAlles Futter gesammelt nach {step} Schritten!")
            plt.pause(2.0)
            break

    plt.ioff()
    plt.close(fig)


if __name__ == "__main__":
    run()
