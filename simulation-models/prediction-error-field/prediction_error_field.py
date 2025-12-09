"""
Prediction Error Field – Game of Life Version
---------------------------------------------

In this simulation:

- The WORLD follows Conway's Game of Life (B3/S23).
- Each CELL is a simple local learner that tries to PREDICT its OWN next state
  based only on its 8 neighbours.

We visualise:

LEFT  = World state (0/1, Game of Life)
RIGHT = Prediction error per cell (|prediction - reality|)

Press ESC in the window to exit the simulation.
"""

import time
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# Simulation parameters
# -----------------------------
GRID_SIZE = 50          # etwas kleiner für flüssigere Darstellung
LEARNING_RATE = 0.05    # learning rate for local learners
SEED = 42               # random seed for reproducibility
DISPLAY_INTERVAL = 0.08 # Sekunden zwischen Frames (Rendering-Geschwindigkeit)


# -----------------------------
# Game of Life core functions
# -----------------------------
def init_world(size: int) -> np.ndarray:
    """Initialise the world with random 0/1 cells."""
    rng = np.random.default_rng(SEED)
    return rng.integers(0, 2, size=(size, size), endpoint=False).astype(float)


def get_neighbourhood(grid: np.ndarray) -> np.ndarray:
    """
    Returns an array of shape (H, W, 8) with the 8 neighbours of each cell
    using periodic boundary conditions.

    Order of neighbours (for reference):

        0: up
        1: down
        2: left
        3: right
        4: up-left
        5: up-right
        6: down-left
        7: down-right
    """
    up    = np.roll(grid, -1, axis=0)
    down  = np.roll(grid,  1, axis=0)
    left  = np.roll(grid, -1, axis=1)
    right = np.roll(grid,  1, axis=1)

    up_left     = np.roll(up,   -1, axis=1)
    up_right    = np.roll(up,    1, axis=1)
    down_left   = np.roll(down, -1, axis=1)
    down_right  = np.roll(down,  1, axis=1)

    neighbours = np.stack(
        [up, down, left, right, up_left, up_right, down_left, down_right],
        axis=-1
    )
    return neighbours


def world_update_gol(grid: np.ndarray) -> np.ndarray:
    """
    Apply Conway's Game of Life rule:

        - A live cell with 2 or 3 neighbours survives.
        - A dead cell with exactly 3 neighbours becomes alive.
        - Otherwise the cell is dead.
    """
    neighbours = get_neighbourhood(grid)
    neighbour_sum = neighbours.sum(axis=-1)

    next_grid = np.zeros_like(grid)

    # Survival: live cell with 2 or 3 neighbours
    next_grid[(grid == 1) & ((neighbour_sum == 2) | (neighbour_sum == 3))] = 1

    # Birth: dead cell with exactly 3 neighbours
    next_grid[(grid == 0) & (neighbour_sum == 3)] = 1

    return next_grid


# -----------------------------
# Learning model
# -----------------------------
def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def run():
    # Initial world
    grid = init_world(GRID_SIZE)

    rng = np.random.default_rng(SEED)

    # Each cell has 9 weights: bias + 8 neighbours
    # Shape: (H, W, 9)
    weights = rng.normal(0.0, 0.5, size=(GRID_SIZE, GRID_SIZE, 9)).astype(float)

    # Initial error field
    error_field = np.zeros_like(grid, dtype=float)
    step_count = 0

    # ------------------------------------
    # Matplotlib setup (clean, leichtgewichtig)
    # ------------------------------------
    plt.ion()
    fig, (ax_state, ax_err) = plt.subplots(1, 2, figsize=(12, 6))

    # World state (clear black/white, pixelig)
    im_state = ax_state.imshow(
        grid.astype(int),
        cmap="gray_r",
        interpolation="nearest",
        vmin=0,
        vmax=1
    )
    ax_state.set_title("World State (Game of Life)", fontsize=10)
    ax_state.set_xticks([])
    ax_state.set_yticks([])

    # Prediction error field (Heatmap, feste Skala 0..1)
    im_err = ax_err.imshow(
        error_field,
        cmap="magma",
        interpolation="nearest",
        vmin=0,
        vmax=1
    )
    ax_err.set_title("Prediction Error Field", fontsize=10)
    ax_err.set_xticks([])
    ax_err.set_yticks([])

    suptitle = fig.suptitle(
        f"Prediction Error Field — Step: {step_count} — press ESC to exit",
        fontsize=12
    )

    # Layout einmal fixen, oben Platz für Titel lassen
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    # ESC handling
    exit_flag = {"stop": False}

    def on_key(event):
        if event.key in ("escape", "esc"):
            exit_flag["stop"] = True

    fig.canvas.mpl_connect("key_press_event", on_key)

    # ------------------------------------
    # Main simulation loop
    # ------------------------------------
    while True:
        if exit_flag["stop"]:
            print("\nSimulation beendet (ESC gedrückt).")
            break

        step_count += 1

        # Neighbours (8-neighbourhood)
        neighbours = get_neighbourhood(grid)

        # Input vectors x = [1, N1..N8], shape: (H, W, 9)
        bias = np.ones_like(grid)
        x = np.stack(
            [bias] + [neighbours[..., i] for i in range(8)],
            axis=-1
        )

        # Predictions: sigmoid(w · x)
        logits = np.sum(weights * x, axis=-1)
        preds = sigmoid(logits)

        # True next world state from GoL
        next_grid = world_update_gol(grid)

        # Prediction error
        error = next_grid - preds          # signed error
        abs_error = np.abs(error)
        error_field = abs_error

        # Weight update (local learning)
        # Simple gradient-style update: w <- w + eta * (y_true - y_pred) * x
        weights += LEARNING_RATE * error[..., None] * x

        # Clip weights for numerical stability (prevents huge logits)
        weights = np.clip(weights, -10.0, 10.0)

        # Advance world
        grid = next_grid

        # Update visuals
        im_state.set_data(grid.astype(int))
        im_err.set_data(error_field)

        suptitle.set_text(
            f"Prediction Error Field — Step: {step_count} — press ESC to exit"
        )

        fig.canvas.draw_idle()
        plt.pause(0.001)           # Events abarbeiten
        time.sleep(DISPLAY_INTERVAL)  # tatsächliche Frame-Pause

    plt.ioff()
    plt.close(fig)


if __name__ == "__main__":
    run()

