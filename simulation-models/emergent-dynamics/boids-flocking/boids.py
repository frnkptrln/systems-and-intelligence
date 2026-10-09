#!/usr/bin/env python3
"""
Boids – Emergent Collective Motion
------------------------------------

Implements Craig Reynolds' (1987) boids algorithm: each agent follows
three simple local rules and complex flock-like motion emerges.

Rules:
  1. Separation  – steer away from nearby neighbours
  2. Alignment   – match heading with nearby neighbours
  3. Cohesion    – steer toward the centre of nearby neighbours

No agent knows the global flock shape.  Yet stable, organic-looking
formations arise from these purely local interactions.

Press ESC in the matplotlib window to exit.
"""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────
NUM_BOIDS       = 150
WORLD_SIZE      = 100.0       # toroidal world extent
MAX_SPEED       = 2.0
MAX_FORCE       = 0.15

# Perception radii
R_SEPARATION    = 4.0
R_ALIGNMENT     = 12.0
R_COHESION      = 14.0

# Rule weights
W_SEPARATION    = 1.8
W_ALIGNMENT     = 1.0
W_COHESION      = 1.0

MAX_STEPS       = 8000
DISPLAY_EVERY   = 1
TRAIL_LENGTH    = 6           # tail segments per boid
SEED            = 42

# ─────────────────────────────────────────────
# Vector helpers
# ─────────────────────────────────────────────

def limit(v, max_mag):
    """Clamp magnitude of each row vector."""
    mag = np.linalg.norm(v, axis=1, keepdims=True)
    mask = (mag > max_mag).flatten()
    if mask.any():
        v[mask] = v[mask] / mag[mask] * max_mag
    return v


def wrap(pos, size):
    """Toroidal wrap-around."""
    return pos % size


def torus_diff(a, b, size):
    """Shortest vector from b to a on a torus."""
    d = a - b
    d = (d + size / 2) % size - size / 2
    return d


# ─────────────────────────────────────────────
# Boids logic
# ─────────────────────────────────────────────

class Flock:
    __slots__ = ("pos", "vel", "N", "trail")

    def __init__(self, n, rng):
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            raise ValueError("the flock must contain a positive integer number of boids")
        self.N = n
        self.pos = rng.uniform(0, WORLD_SIZE, (n, 2))
        angle = rng.uniform(0, 2 * np.pi, n)
        speed = rng.uniform(MAX_SPEED * 0.5, MAX_SPEED, n)
        self.vel = np.column_stack([np.cos(angle), np.sin(angle)]) * speed[:, None]
        # trail: list of recent positions for drawing tails
        self.trail = [self.pos.copy() for _ in range(TRAIL_LENGTH)]

    def step(self):
        accel = np.zeros_like(self.vel)

        # Pairwise differences (toroidal)
        # diff[i, j] = shortest vector from j to i
        diff = torus_diff(
            self.pos[:, None, :],  # (N,1,2)
            self.pos[None, :, :],  # (1,N,2)
            WORLD_SIZE
        )  # (N, N, 2)
        dist = np.linalg.norm(diff, axis=2)  # (N, N)

        # Ignore self
        np.fill_diagonal(dist, np.inf)

        # 1. SEPARATION
        mask_sep = dist < R_SEPARATION
        # For each boid, average of (normalised away-vectors) from too-close neighbours
        sep_force = np.zeros_like(self.vel)
        for i in range(self.N):
            neighbours = mask_sep[i]
            if neighbours.any():
                d = diff[i, neighbours]       # vectors from j to i
                w = 1.0 / np.maximum(dist[i, neighbours], 0.01)
                sep_force[i] = (d * w[:, None]).sum(axis=0)
        sep_mag = np.linalg.norm(sep_force, axis=1, keepdims=True)
        sep_mag = np.maximum(sep_mag, 1e-8)
        sep_force = sep_force / sep_mag * MAX_SPEED - self.vel
        sep_force = limit(sep_force, MAX_FORCE)
        sep_force[~mask_sep.any(axis=1)] = 0

        # 2. ALIGNMENT
        mask_ali = dist < R_ALIGNMENT
        ali_force = np.zeros_like(self.vel)
        for i in range(self.N):
            neighbours = mask_ali[i]
            if neighbours.any():
                avg_vel = self.vel[neighbours].mean(axis=0)
                ali_force[i] = avg_vel
        ali_mag = np.linalg.norm(ali_force, axis=1, keepdims=True)
        ali_mag = np.maximum(ali_mag, 1e-8)
        ali_force = ali_force / ali_mag * MAX_SPEED - self.vel
        ali_force = limit(ali_force, MAX_FORCE)
        ali_force[~mask_ali.any(axis=1)] = 0

        # 3. COHESION
        mask_coh = dist < R_COHESION
        coh_force = np.zeros_like(self.vel)
        for i in range(self.N):
            neighbours = mask_coh[i]
            if neighbours.any():
                # Average in this boid's local coordinate frame. Averaging
                # absolute wrapped positions puts seam-crossing neighbours
                # near the middle of the world, where none of them are.
                coh_force[i] = -diff[i, neighbours].mean(axis=0)
        coh_mag = np.linalg.norm(coh_force, axis=1, keepdims=True)
        coh_mag = np.maximum(coh_mag, 1e-8)
        coh_force = coh_force / coh_mag * MAX_SPEED - self.vel
        coh_force = limit(coh_force, MAX_FORCE)
        coh_force[~mask_coh.any(axis=1)] = 0

        # Combine
        accel = (
            W_SEPARATION * sep_force +
            W_ALIGNMENT  * ali_force +
            W_COHESION   * coh_force
        )
        accel = limit(accel, MAX_FORCE * 3)

        # Update velocity & position
        self.vel += accel
        self.vel = limit(self.vel, MAX_SPEED)
        self.pos = wrap(self.pos + self.vel, WORLD_SIZE)

        # Update trail
        self.trail.pop(0)
        self.trail.append(self.pos.copy())


# ─────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────

def run(n=NUM_BOIDS, seed=SEED, max_steps=MAX_STEPS):
    # Headless runs need only NumPy; import the display stack on demand.
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    rng = np.random.default_rng(seed)
    flock = Flock(n, rng)

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, WORLD_SIZE)
    ax.set_ylim(0, WORLD_SIZE)
    ax.set_aspect("equal")
    ax.set_facecolor("#0a0e1a")
    fig.patch.set_facecolor("#0a0e1a")
    ax.set_xticks([])
    ax.set_yticks([])

    # Boid heads (triangular markers showing heading)
    scatter = ax.scatter(
        flock.pos[:, 0], flock.pos[:, 1],
        s=18, c="#60a5fa", marker="o",
        edgecolors="none", alpha=0.9, zorder=5
    )

    # Trail lines (line collection for efficiency)
    trail_lc = LineCollection([], colors="#60a5fa", linewidths=0.5,
                               alpha=0.15, zorder=2)
    ax.add_collection(trail_lc)

    title = ax.set_title(
        "Boids – Emergent Flocking  |  Step 0",
        color="#e5e7eb", fontsize=11
    )

    fig.tight_layout()

    exit_flag = {"stop": False}
    def on_key(event):
        if event.key in ("escape", "esc"):
            exit_flag["stop"] = True
    fig.canvas.mpl_connect("key_press_event", on_key)

    for step in range(1, max_steps + 1):
        if exit_flag["stop"] or not plt.fignum_exists(fig.number):
            print("\nSimulation ended (ESC).")
            break

        flock.step()

        if step % DISPLAY_EVERY == 0:
            scatter.set_offsets(flock.pos)

            # Heading-based colour (hue = angle)
            angles = np.arctan2(flock.vel[:, 1], flock.vel[:, 0])
            hues = (angles / (2 * np.pi)) % 1.0
            # HSV → RGB conversion
            colors = plt.cm.hsv(hues)
            colors[:, 3] = 0.85  # alpha
            scatter.set_color(colors)

            # Trail segments
            segments = []
            for t in range(len(flock.trail) - 1):
                for b in range(flock.N):
                    p0 = flock.trail[t][b]
                    p1 = flock.trail[t + 1][b]
                    # Only draw if not wrapping
                    if np.linalg.norm(p1 - p0) < WORLD_SIZE / 2:
                        segments.append([p0, p1])
            trail_lc.set_segments(segments)

            title.set_text(
                f"Boids – Emergent Flocking  |  "
                f"N={n}  |  Step {step}"
            )

            fig.canvas.draw_idle()
            plt.pause(0.001)

    plt.ioff()
    plt.close(fig)


def observables(flock, step):
    """Speed and mean unit-heading magnitude; stationary headings count as zero."""
    speed = np.linalg.norm(flock.vel, axis=1)
    headings = np.divide(flock.vel, speed[:, None], out=np.zeros_like(flock.vel),
                         where=speed[:, None] > 0)
    return {
        "step": step,
        "mean_speed": float(speed.mean()),
        "maximum_speed": float(speed.max()),
        "polarization": float(np.clip(np.linalg.norm(headings.mean(axis=0)), 0, 1)),
    }


def run_report(n=NUM_BOIDS, seed=SEED, steps=200, sample_every=10):
    """Run the same dynamics without a window and return a reproducible record."""
    for name, value, minimum in (("seed", seed, 0), ("steps", steps, 0),
                                  ("sample_every", sample_every, 1)):
        if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
            raise ValueError(f"{name} must be an integer >= {minimum}")
    flock = Flock(n, np.random.default_rng(seed))
    samples = [observables(flock, 0)]
    for step in range(1, steps + 1):
        flock.step()
        if step % sample_every == 0 or step == steps:
            samples.append(observables(flock, step))
    return {
        "schema": "boids-run/1",
        "dynamics": "boids-torus-v2",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "seed": seed,
        "boids": n,
        "steps": steps,
        "sample_every": sample_every,
        "parameters": {
            "world_size": WORLD_SIZE, "max_speed": MAX_SPEED, "max_force": MAX_FORCE,
            "separation_radius": R_SEPARATION, "alignment_radius": R_ALIGNMENT,
            "cohesion_radius": R_COHESION, "separation_weight": W_SEPARATION,
            "alignment_weight": W_ALIGNMENT, "cohesion_weight": W_COHESION,
        },
        "samples": samples,
        "final_state": {"positions": flock.pos.tolist(), "velocities": flock.vel.tolist()},
        "interpretation": "Descriptive simulation observables, not measurements of agency or intelligence.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--boids", type=int, default=NUM_BOIDS)
    parser.add_argument("--steps", type=int, default=MAX_STEPS)
    parser.add_argument("--headless", action="store_true", help="write a JSON run record without opening a window")
    parser.add_argument("--sample-every", type=int, default=10, help="headless observation interval in simulation steps")
    parser.add_argument("--output", type=Path, help="new JSON file (headless only); otherwise print to stdout")
    args = parser.parse_args(argv)
    if args.boids < 1 or args.steps < 0 or args.seed < 0 or args.sample_every < 1:
        parser.error("boids and sample-every must be positive; seed and steps must be nonnegative")
    if args.output and not args.headless:
        parser.error("--output requires --headless")
    if args.output and args.output.exists():
        parser.error("output already exists; choose a new filename")
    if not args.headless:
        run(n=args.boids, seed=args.seed, max_steps=args.steps)
        return 0
    report = run_report(n=args.boids, seed=args.seed, steps=args.steps, sample_every=args.sample_every)
    payload = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(payload)
        except OSError as error:
            parser.error(f"cannot create output: {error.strerror}")
        print(f"Wrote {args.output}")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
