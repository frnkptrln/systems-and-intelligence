#!/usr/bin/env python3
"""
Nested Emergence Demo — Cross-Scale Coherence Propagation
--------------------------------------------------------

A two-scale coupled thought experiment:

  Bottom scale: Continuous cellular field (Lenia-like) evolving on a grid.
  Top scale:    Boids swarm moving in continuous 2D space.

Couplings:
  Bottom -> Top: boids sample local field coherence; coherence modulates
                 alignment strength and stochastic exploration.
  Top -> Bottom: boids deposit a density field; density perturbs bottom dynamics.

Outputs:
  - Field snapshot + boids overlay
  - Time series of bottom coherence and swarm order parameter
  - Simple lag correlation between the two (propagation proxy)

Press ESC to exit.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d


# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────

SEED = 42

# World / field
GRID_SIZE = 96
WORLD_SIZE = 100.0  # boids live in [0, WORLD_SIZE)^2 (toroidal)
DT_FIELD = 1.0

R_KERNEL = 5
MU_BASE = 0.14
SIGMA = 0.018

# Swarm
NUM_BOIDS = 160
DT_BOIDS = 1.0
MAX_SPEED = 2.0
MAX_FORCE = 0.15

R_SEPARATION = 3.5
R_ALIGNMENT = 11.5
R_COHESION = 13.0

W_SEPARATION = 1.7
W_ALIGNMENT_BASE = 0.9
W_COHESION = 0.9

# Bottom->Top modulation
ALIGN_GAIN = 1.8          # multiplier when coherence is high
NOISE_STD_BASE = 0.12     # random steering baseline
NOISE_STD_GAIN = 0.22     # additional noise when coherence is low

# Top->Bottom coupling
DEPOSIT_STRENGTH = 0.30    # how much boid density perturbs the field
DENSITY_BLUR_PX = 4        # blur radius (in pixels) for density

# Metrics / viz
MAX_STEPS = 6000
DISPLAY_EVERY = 2
HISTORY_LEN = 500
MAX_LAG = 120


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def wrap(pos: np.ndarray, size: float) -> np.ndarray:
    return pos % size


def torus_diff(a: np.ndarray, b: np.ndarray, size: float) -> np.ndarray:
    """Shortest vector from b to a on a torus."""
    d = a - b
    d = (d + size / 2) % size - size / 2
    return d


def limit(v: np.ndarray, max_mag: float) -> np.ndarray:
    mag = np.linalg.norm(v, axis=1, keepdims=True)
    mask = (mag > max_mag).flatten()
    if mask.any():
        v[mask] = v[mask] / np.maximum(mag[mask], 1e-8) * max_mag
    return v


def make_disk_kernel(r: int) -> np.ndarray:
    y, x = np.ogrid[-r : r + 1, -r : r + 1]
    mask = x * x + y * y <= r * r
    k = np.zeros((2 * r + 1, 2 * r + 1), dtype=np.float64)
    k[mask] = 1.0
    k /= np.sum(k)
    return k


def gaussian_kernel_2d(r: int, sigma: float) -> np.ndarray:
    ax = np.arange(-r, r + 1, dtype=np.float64)
    xx, yy = np.meshgrid(ax, ax)
    k = np.exp(-(xx * xx + yy * yy) / (2 * sigma * sigma))
    k /= np.sum(k)
    return k


def bilinear_sample(field: np.ndarray, x: np.ndarray, y: np.ndarray, world_size: float) -> np.ndarray:
    """
    Sample a 2D field (GRID_SIZE x GRID_SIZE) at continuous world coords.
    Toroidal wrap, bilinear interpolation.
    """
    h, w = field.shape
    fx = (x / world_size) * w
    fy = (y / world_size) * h

    x0 = np.floor(fx).astype(int) % w
    y0 = np.floor(fy).astype(int) % h
    x1 = (x0 + 1) % w
    y1 = (y0 + 1) % h

    dx = fx - np.floor(fx)
    dy = fy - np.floor(fy)

    v00 = field[y0, x0]
    v10 = field[y0, x1]
    v01 = field[y1, x0]
    v11 = field[y1, x1]

    v0 = v00 * (1 - dx) + v10 * dx
    v1 = v01 * (1 - dx) + v11 * dx
    return v0 * (1 - dy) + v1 * dy


def lag_correlation(a: np.ndarray, b: np.ndarray, max_lag: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute correlation corr(a_t, b_{t-lag}) for lag in [-max_lag, +max_lag].
    Returns (lags, corrs). Uses z-scored arrays.
    """
    if len(a) != len(b) or len(a) < 5:
        lags = np.arange(-max_lag, max_lag + 1)
        return lags, np.zeros_like(lags, dtype=np.float64)

    aa = (a - np.mean(a)) / (np.std(a) + 1e-8)
    bb = (b - np.mean(b)) / (np.std(b) + 1e-8)

    lags = np.arange(-max_lag, max_lag + 1)
    corrs = np.zeros_like(lags, dtype=np.float64)
    n = len(aa)
    for i, lag in enumerate(lags):
        if lag < 0:
            x = aa[-lag:]
            y = bb[: n + lag]
        elif lag > 0:
            x = aa[: n - lag]
            y = bb[lag:]
        else:
            x = aa
            y = bb
        if len(x) < 5:
            corrs[i] = 0.0
        else:
            corrs[i] = float(np.mean(x * y))
    return lags, corrs


# ─────────────────────────────────────────────
# Bottom scale: continuous field
# ─────────────────────────────────────────────

class ContinuousField:
    def __init__(self, size: int, rng: np.random.Generator):
        self.size = int(size)
        self.grid = rng.random((self.size, self.size))
        self.kernel = make_disk_kernel(R_KERNEL)

        # density blur kernel (for top->bottom coupling)
        blur_r = int(DENSITY_BLUR_PX)
        blur_sigma = max(1.0, 0.45 * blur_r)
        self.blur_kernel = gaussian_kernel_2d(blur_r, blur_sigma)

    def growth(self, u: np.ndarray, mu: np.ndarray) -> np.ndarray:
        # bell-shaped growth curve centered at mu
        return 2.0 * np.exp(-((u - mu) ** 2) / (2 * SIGMA**2)) - 1.0

    def step(self, density_field: np.ndarray) -> np.ndarray:
        # neighborhood sum
        u = convolve2d(self.grid, self.kernel, mode="same", boundary="wrap")

        # top->bottom coupling: blur density and push mu locally
        dens = convolve2d(density_field, self.blur_kernel, mode="same", boundary="wrap")
        dens = dens / (np.max(dens) + 1e-8)
        mu = MU_BASE + DEPOSIT_STRENGTH * (dens - 0.5)

        g = self.growth(u, mu)
        self.grid = np.clip(self.grid + DT_FIELD * g, 0.0, 1.0)
        return self.grid

    def coherence_field(self) -> np.ndarray:
        """
        Local coherence proxy: 1 - normalized local variance.
        High when field is locally smooth/consistent.
        """
        # local mean and mean square
        mean = convolve2d(self.grid, self.kernel, mode="same", boundary="wrap")
        mean2 = convolve2d(self.grid * self.grid, self.kernel, mode="same", boundary="wrap")
        var = np.maximum(mean2 - mean * mean, 0.0)

        # normalize variance into [0,1] approximately
        v = var / (np.percentile(var, 95) + 1e-8)
        v = np.clip(v, 0.0, 1.0)
        coh = 1.0 - v
        return coh

    def coherence_scalar(self) -> float:
        coh = self.coherence_field()
        return float(np.mean(coh))


# ─────────────────────────────────────────────
# Top scale: boids
# ─────────────────────────────────────────────

class Flock:
    def __init__(self, n: int, rng: np.random.Generator):
        self.N = int(n)
        self.pos = rng.uniform(0, WORLD_SIZE, (self.N, 2))
        angle = rng.uniform(0, 2 * np.pi, self.N)
        speed = rng.uniform(MAX_SPEED * 0.4, MAX_SPEED, self.N)
        self.vel = np.column_stack([np.cos(angle), np.sin(angle)]) * speed[:, None]

    def step(self, local_coherence: np.ndarray, rng: np.random.Generator) -> None:
        # pairwise diffs
        diff = torus_diff(self.pos[:, None, :], self.pos[None, :, :], WORLD_SIZE)
        dist = np.linalg.norm(diff, axis=2)
        np.fill_diagonal(dist, np.inf)

        # separation
        mask_sep = dist < R_SEPARATION
        sep_force = np.zeros_like(self.vel)
        for i in range(self.N):
            neigh = mask_sep[i]
            if neigh.any():
                d = diff[i, neigh]
                w = 1.0 / np.maximum(dist[i, neigh], 0.01)
                sep_force[i] = (d * w[:, None]).sum(axis=0)
        sep_mag = np.linalg.norm(sep_force, axis=1, keepdims=True)
        sep_force = sep_force / np.maximum(sep_mag, 1e-8) * MAX_SPEED - self.vel
        sep_force = limit(sep_force, MAX_FORCE)

        # alignment
        mask_ali = dist < R_ALIGNMENT
        ali_force = np.zeros_like(self.vel)
        for i in range(self.N):
            neigh = mask_ali[i]
            if neigh.any():
                ali_force[i] = self.vel[neigh].mean(axis=0)
        ali_mag = np.linalg.norm(ali_force, axis=1, keepdims=True)
        ali_force = ali_force / np.maximum(ali_mag, 1e-8) * MAX_SPEED - self.vel
        ali_force = limit(ali_force, MAX_FORCE)

        # cohesion
        mask_coh = dist < R_COHESION
        coh_force = np.zeros_like(self.vel)
        for i in range(self.N):
            neigh = mask_coh[i]
            if neigh.any():
                centre = self.pos[neigh].mean(axis=0)
                desired = torus_diff(centre[None, :], self.pos[i : i + 1], WORLD_SIZE).flatten()
                coh_force[i] = desired
        coh_mag = np.linalg.norm(coh_force, axis=1, keepdims=True)
        coh_force = coh_force / np.maximum(coh_mag, 1e-8) * MAX_SPEED - self.vel
        coh_force = limit(coh_force, MAX_FORCE)

        # bottom->top modulation:
        # coherence in [0,1]. High coherence => stronger alignment, less noise.
        coh = np.clip(local_coherence, 0.0, 1.0)
        w_align = W_ALIGNMENT_BASE * (1.0 + ALIGN_GAIN * coh)
        noise_std = NOISE_STD_BASE + NOISE_STD_GAIN * (1.0 - coh)
        noise = rng.normal(0.0, noise_std[:, None], size=self.vel.shape)

        accel = (
            W_SEPARATION * sep_force
            + w_align[:, None] * ali_force
            + W_COHESION * coh_force
            + noise
        )
        accel = limit(accel, MAX_FORCE * 3)

        self.vel = limit(self.vel + accel, MAX_SPEED)
        self.pos = wrap(self.pos + DT_BOIDS * self.vel, WORLD_SIZE)

    def order_parameter(self) -> float:
        """
        Swarm coherence: magnitude of mean unit velocity (0..1).
        """
        v = self.vel
        n = np.linalg.norm(v, axis=1, keepdims=True)
        u = v / np.maximum(n, 1e-8)
        m = np.mean(u, axis=0)
        return float(np.linalg.norm(m))

    def deposit_density(self, grid_size: int) -> np.ndarray:
        """
        Rasterize boids onto a grid (toroidal), returning a density field in [0, +).
        """
        dens = np.zeros((grid_size, grid_size), dtype=np.float64)
        gx = (self.pos[:, 0] / WORLD_SIZE) * grid_size
        gy = (self.pos[:, 1] / WORLD_SIZE) * grid_size
        ix = np.floor(gx).astype(int) % grid_size
        iy = np.floor(gy).astype(int) % grid_size
        np.add.at(dens, (iy, ix), 1.0)
        return dens


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def run() -> None:
    rng = np.random.default_rng(SEED)
    field = ContinuousField(GRID_SIZE, rng)
    flock = Flock(NUM_BOIDS, rng)

    bottom_hist: list[float] = []
    top_hist: list[float] = []

    # Matplotlib setup
    plt.ion()
    fig = plt.figure(figsize=(14, 7.5))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.2, 1.2, 1.0], height_ratios=[1.0, 1.0])

    ax_field = fig.add_subplot(gs[:, 0])
    ax_ts = fig.add_subplot(gs[0, 1:])
    ax_lag = fig.add_subplot(gs[1, 1:])

    ax_field.set_title("Bottom field + Boids overlay")
    ax_field.set_xticks([])
    ax_field.set_yticks([])

    img = ax_field.imshow(field.grid, cmap="viridis", vmin=0, vmax=1, interpolation="nearest")
    scatter = ax_field.scatter([], [], s=10, c="#e5e7eb", alpha=0.85, edgecolors="none")

    ax_ts.set_title("Cross-scale coherence time series")
    ax_ts.set_xlabel("step")
    ax_ts.set_ylabel("coherence / order")
    line_bottom, = ax_ts.plot([], [], color="#22c55e", linewidth=1.3, label="bottom coherence")
    line_top, = ax_ts.plot([], [], color="#ef4444", linewidth=1.3, label="swarm order")
    ax_ts.set_ylim(-0.05, 1.05)
    ax_ts.grid(True, alpha=0.25)
    ax_ts.legend(loc="upper right")

    ax_lag.set_title("Lag correlation (bottom ↔ top)")
    ax_lag.set_xlabel("lag (steps)")
    ax_lag.set_ylabel("corr")
    line_lag, = ax_lag.plot([], [], color="#60a5fa", linewidth=1.3)
    ax_lag.axhline(0.0, color="gray", linewidth=0.8, alpha=0.3)
    ax_lag.grid(True, alpha=0.25)

    fig.suptitle("Nested Emergence Demo — Coherence Propagation Across Scales", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    exit_flag = {"stop": False}

    def on_key(event):
        if event.key in ("escape", "esc"):
            exit_flag["stop"] = True

    fig.canvas.mpl_connect("key_press_event", on_key)

    for step in range(1, MAX_STEPS + 1):
        if exit_flag["stop"]:
            print("\nSimulation ended (ESC).")
            break

        # Top -> Bottom deposit
        density = flock.deposit_density(GRID_SIZE)
        field.step(density)

        # Bottom -> Top sample coherence at boid positions
        coh_field = field.coherence_field()
        local_coh = bilinear_sample(coh_field, flock.pos[:, 0], flock.pos[:, 1], WORLD_SIZE)
        flock.step(local_coh, rng)

        # Metrics
        bottom_c = float(np.mean(coh_field))
        top_c = flock.order_parameter()
        bottom_hist.append(bottom_c)
        top_hist.append(top_c)

        if len(bottom_hist) > HISTORY_LEN:
            bottom_hist = bottom_hist[-HISTORY_LEN:]
            top_hist = top_hist[-HISTORY_LEN:]

        if step % DISPLAY_EVERY == 0:
            # field
            img.set_data(field.grid)

            # overlay boids in field pixel coords
            bx = (flock.pos[:, 0] / WORLD_SIZE) * (GRID_SIZE - 1)
            by = (flock.pos[:, 1] / WORLD_SIZE) * (GRID_SIZE - 1)
            scatter.set_offsets(np.column_stack([bx, by]))

            # time series
            xs = np.arange(len(bottom_hist))
            line_bottom.set_data(xs, bottom_hist)
            line_top.set_data(xs, top_hist)
            ax_ts.set_xlim(0, max(10, len(xs)))

            # lag corr
            lags, corrs = lag_correlation(np.array(bottom_hist), np.array(top_hist), MAX_LAG)
            line_lag.set_data(lags, corrs)
            ax_lag.set_xlim(-MAX_LAG, MAX_LAG)
            ax_lag.set_ylim(-1.0, 1.0)

            fig.canvas.draw_idle()
            plt.pause(0.001)

    plt.ioff()
    plt.close(fig)


if __name__ == "__main__":
    run()

