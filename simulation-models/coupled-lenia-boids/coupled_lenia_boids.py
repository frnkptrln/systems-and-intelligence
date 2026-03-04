#!/usr/bin/env python3
"""
Coupled Lenia-Boids Simulation
--------------------------------------

A multi-model coupling experiment demonstrating upward and downward causation.
We run a continuous cellular automaton (Lenia) representing a living, growing
caloric environment, and an agent-based model (Boids) representing a flock of
foragers.

Upward Causation: Boids are attracted to areas of high Lenia density ("food").
Downward Causation: Boids consume Lenia (reducing its value), but when Boids die 
                    or move, they "fertilize" the Lenia field, spurring new growth.

Press ESC in the matplotlib window to exit.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
from scipy.signal import fftconvolve
import matplotlib.animation as animation

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────

# World Parameters
GRID_SIZE      = 128          # Lenia world resolution
WORLD_SIZE     = 128.0        # Boids world extent (matches GRID_SIZE mapping)
MAX_STEPS      = 5000
DISPLAY_EVERY  = 2
SEED           = 7

# Lenia Parameters (Orbium-like preset)
KERNEL_R       = 13           
DT             = 0.1          
MU             = 0.15         
SIGMA          = 0.017        

# Boids Parameters
NUM_BOIDS      = 60
MAX_SPEED      = 2.0
MAX_FORCE      = 0.2
R_SEPARATION   = 4.0
R_ALIGNMENT    = 10.0
R_COHESION     = 10.0
W_SEPARATION   = 1.5
W_ALIGNMENT    = 1.0
W_COHESION     = 1.0
TRAIL_LENGTH   = 5

# Coupling Parameters
W_FORAGING     = 0.8          # Boids attraction to Lenia
CONSUMPTION    = 0.05         # How much Lenia a boid eats per step
FERTILIZATION  = 0.1          # How much Lenia grows where a boid is (waste/decay)
DEATH_PROB     = 0.005        # Chance a boid dies and becomes pure fertilizer
REBIRTH_ENERGY = 20           # Accumulation needed for a boid to reproduce

# ─────────────────────────────────────────────
# Lenia Core Logic
# ─────────────────────────────────────────────

def make_kernel(R):
    y, x = np.mgrid[-R:R+1, -R:R+1].astype(np.float64)
    r = np.sqrt(x**2 + y**2) / R
    kernel = np.exp(-((r - 0.5) / 0.15) ** 2 / 2.0)
    kernel[r > 1.0] = 0.0
    kernel /= kernel.sum()
    return kernel

def growth(u, mu, sigma):
    return 2.0 * np.exp(-((u - mu) ** 2) / (2.0 * sigma ** 2)) - 1.0

def lenia_step(A, kernel, mu, sigma, dt):
    U = fftconvolve(A, kernel, mode="same")
    G = growth(U, mu, sigma)
    A_new = A + dt * G
    return np.clip(A_new, 0.0, 1.0)

# ─────────────────────────────────────────────
# Boids Vector Helpers
# ─────────────────────────────────────────────

def limit(v, max_mag):
    mag = np.linalg.norm(v, axis=1, keepdims=True)
    mask = (mag > max_mag).flatten()
    if mask.any():
        v[mask] = v[mask] / mag[mask] * max_mag
    return v

def wrap(pos, size):
    return pos % size

def torus_diff(a, b, size):
    d = a - b
    d = (d + size / 2) % size - size / 2
    return d

# ─────────────────────────────────────────────
# Coupled System
# ─────────────────────────────────────────────

class CoupledSystem:
    def __init__(self, rng):
        self.rng = rng
        self.kernel = make_kernel(KERNEL_R)
        
        # Init Lenia world
        self.A = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.float64)
        n_blobs = rng.integers(3, 7)
        for _ in range(n_blobs):
            cx = rng.integers(GRID_SIZE // 4, 3 * GRID_SIZE // 4)
            cy = rng.integers(GRID_SIZE // 4, 3 * GRID_SIZE // 4)
            r = rng.integers(10, 25)
            y, x = np.mgrid[0:GRID_SIZE, 0:GRID_SIZE].astype(np.float64)
            blob = np.exp(-((x - cx)**2 + (y - cy)**2) / (2.0 * r**2))
            self.A += blob * rng.uniform(0.3, 1.0)
        self.A = np.clip(self.A, 0.0, 1.0)
        
        # Init Boids
        self.N = NUM_BOIDS
        self.pos = rng.uniform(0, WORLD_SIZE, (self.N, 2))
        angle = rng.uniform(0, 2 * np.pi, self.N)
        speed = rng.uniform(MAX_SPEED * 0.5, MAX_SPEED, self.N)
        self.vel = np.column_stack([np.cos(angle), np.sin(angle)]) * speed[:, None]
        self.trail = [self.pos.copy() for _ in range(TRAIL_LENGTH)]
        self.energy = np.ones(self.N) * 10.0 # Starting energy

    def get_lenia_gradient(self, pos):
        """Returns the gradient of the Lenia field at the given continuous positions."""
        gradients = np.zeros_like(pos)
        # Compute gradient of A using central differences
        gy, gx = np.gradient(self.A)
        
        for i in range(len(pos)):
            # Bilinear interpolation of gradient (simplified to nearest neighbour for speed)
            x, y = int(pos[i, 0]) % GRID_SIZE, int(pos[i, 1]) % GRID_SIZE
            gradients[i] = [gx[y, x], gy[y, x]] 
            # Note: matplotlib imshow orientation vs numpy indexing means X corresponds to col (idx 1), Y to row (idx 0)
            
        return gradients

    def step(self):
        # 1. Update Lenia (Continuous CA step)
        self.A = lenia_step(self.A, self.kernel, MU, SIGMA, DT)
        
        # 2. Update Boids
        accel = np.zeros_like(self.vel)

        if self.N > 0:
            diff = torus_diff(self.pos[:, None, :], self.pos[None, :, :], WORLD_SIZE)
            dist = np.linalg.norm(diff, axis=2)
            np.fill_diagonal(dist, np.inf)

            # Standard Boids rules
            mask_sep = dist < R_SEPARATION
            sep_force = np.zeros_like(self.vel)
            for i in range(self.N):
                neighbours = mask_sep[i]
                if neighbours.any():
                    d = diff[i, neighbours]
                    w = 1.0 / np.maximum(dist[i, neighbours], 0.01)
                    sep_force[i] = (d * w[:, None]).sum(axis=0)
            sep_mag = np.linalg.norm(sep_force, axis=1, keepdims=True)
            sep_mag = np.maximum(sep_mag, 1e-8)
            sep_force = sep_force / sep_mag * MAX_SPEED - self.vel
            sep_force = limit(sep_force, MAX_FORCE)

            mask_ali = dist < R_ALIGNMENT
            ali_force = np.zeros_like(self.vel)
            for i in range(self.N):
                neighbours = mask_ali[i]
                if neighbours.any():
                    ali_force[i] = self.vel[neighbours].mean(axis=0)
            ali_mag = np.linalg.norm(ali_force, axis=1, keepdims=True)
            ali_mag = np.maximum(ali_mag, 1e-8)
            ali_force = ali_force / ali_mag * MAX_SPEED - self.vel
            ali_force = limit(ali_force, MAX_FORCE)

            mask_coh = dist < R_COHESION
            coh_force = np.zeros_like(self.vel)
            for i in range(self.N):
                neighbours = mask_coh[i]
                if neighbours.any():
                    centre = self.pos[neighbours].mean(axis=0)
                    desired = torus_diff(centre[None, :], self.pos[i:i+1], WORLD_SIZE).flatten()
                    coh_force[i] = desired
            coh_mag = np.linalg.norm(coh_force, axis=1, keepdims=True)
            coh_mag = np.maximum(coh_mag, 1e-8)
            coh_force = coh_force / coh_mag * MAX_SPEED - self.vel
            coh_force = limit(coh_force, MAX_FORCE)

            # FORAGING FORCE: Steer up the Lenia gradient
            food_grad = self.get_lenia_gradient(self.pos)
            foraging_force = food_grad * MAX_SPEED - self.vel
            foraging_force = limit(foraging_force, MAX_FORCE * 1.5)

            # Combine forces
            accel = (
                W_SEPARATION * sep_force +
                W_ALIGNMENT  * ali_force +
                W_COHESION   * coh_force +
                W_FORAGING   * foraging_force
            )
            accel = limit(accel, MAX_FORCE * 3)

            # Apply kinematics
            self.vel += accel
            self.vel = limit(self.vel, MAX_SPEED)
            self.pos = wrap(self.pos + self.vel, WORLD_SIZE)
            
            self.trail.pop(0)
            self.trail.append(self.pos.copy())

            # 3. INTERACTION: Coupling Boids -> Lenia
            deaths = []
            new_pos = []
            new_vel = []
            new_energy = []
            
            for i in range(self.N):
                # Boid location in grid
                px, py = int(self.pos[i, 0]) % GRID_SIZE, int(self.pos[i, 1]) % GRID_SIZE
                
                # Consume Lenia (Upward Causation)
                available_food = self.A[py, px]
                if available_food > CONSUMPTION:
                    self.A[py, px] -= CONSUMPTION
                    self.energy[i] += CONSUMPTION * 2
                else:
                    self.energy[i] -= 0.1 # Starving
                    
                # Fertilize Lenia (Downward Causation - waste)
                self.A[py, px] = min(1.0, self.A[py, px] + FERTILIZATION * 0.1)

                # Life/Death cycle
                if self.energy[i] <= 0 or self.rng.random() < DEATH_PROB:
                    # Death: Fertilize the spot massively
                    self.A[py, px] = min(1.0, self.A[py, px] + FERTILIZATION * 10)
                    deaths.append(i)
                elif self.energy[i] > REBIRTH_ENERGY:
                    # Reproduction (Mitosis)
                    self.energy[i] /= 2
                    new_pos.append(self.pos[i] + self.rng.uniform(-1, 1, 2))
                    new_vel.append(self.vel[i] + self.rng.uniform(-0.1, 0.1, 2))
                    new_energy.append(self.energy[i])
            
            # Remove dead boids
            if deaths:
                mask = np.ones(self.N, dtype=bool)
                mask[deaths] = False
                self.pos = self.pos[mask]
                self.vel = self.vel[mask]
                self.energy = self.energy[mask]
                for t in range(TRAIL_LENGTH):
                    self.trail[t] = self.trail[t][mask]
                self.N = len(self.pos)
                
            # Add new boids
            if new_pos:
                self.pos = np.vstack([self.pos, np.array(new_pos)])
                self.vel = np.vstack([self.vel, np.array(new_vel)])
                self.energy = np.concatenate([self.energy, np.array(new_energy)])
                for t in range(TRAIL_LENGTH):
                    self.trail[t] = np.vstack([self.trail[t], np.array(new_pos)])
                self.N = len(self.pos)

        # Ensure Lenia stays in bounds
        self.A = np.clip(self.A, 0.0, 1.0)


# ─────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────

def run():
    rng = np.random.default_rng(SEED)
    sys = CoupledSystem(rng)

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor("#0a0e1a")
    
    # Custom colormap for Lenia (deep black to sickly green/yellow to represent algae/food)
    lenia_cmap = LinearSegmentedColormap.from_list("lenia_bio", [
        (0.00, (0.00, 0.00, 0.04)),     
        (0.20, (0.05, 0.15, 0.10)),     
        (0.50, (0.15, 0.40, 0.20)),     
        (0.80, (0.60, 0.80, 0.30)),     
        (1.00, (0.90, 1.00, 0.50)),     
    ], N=512)

    # Lenia background
    im = ax.imshow(
        sys.A, cmap=lenia_cmap,
        interpolation="bilinear",
        vmin=0, vmax=1.0,
        origin="lower",
        extent=[0, WORLD_SIZE, 0, WORLD_SIZE]
    )
    
    # Boids overlay
    scatter = ax.scatter(
        [], [],
        s=12, c="#f87171", marker="o",
        edgecolors="white", linewidths=0.5, alpha=0.9, zorder=5
    )
    
    trail_lc = LineCollection([], colors="#f87171", linewidths=0.8,
                               alpha=0.3, zorder=2)
    ax.add_collection(trail_lc)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")

    title = ax.set_title(
        "Coupled Dynamics: Lenia ↔ Boids  |  Step 0",
        fontsize=11, color="#e2e8f0"
    )
    fig.tight_layout()

    exit_flag = {"stop": False}
    def on_key(event):
        if event.key in ("escape", "esc"):
            exit_flag["stop"] = True
    fig.canvas.mpl_connect("key_press_event", on_key)

    for step in range(1, MAX_STEPS + 1):
        if exit_flag["stop"]:
            print("\nSimulation beendet (ESC).")
            break

        sys.step()

        if step % DISPLAY_EVERY == 0:
            # Update Lenia
            im.set_data(sys.A)
            
            # Update Boids
            if sys.N > 0:
                scatter.set_offsets(sys.pos)
                
                # Trail segments
                segments = []
                for t in range(len(sys.trail) - 1):
                    for b in range(sys.N):
                        p0 = sys.trail[t][b]
                        p1 = sys.trail[t + 1][b]
                        if np.linalg.norm(p1 - p0) < WORLD_SIZE / 2:
                            segments.append([p0, p1])
                trail_lc.set_segments(segments)
            else:
                scatter.set_offsets(np.empty((0, 2)))
                trail_lc.set_segments([])

            lenia_mass = sys.A.sum()
            title.set_text(
                f"Coupled Dynamics: Lenia ↔ Boids  |  Step {step}\n"
                f"Lenia Mass: {lenia_mass:.0f}  |  Boids Population: {sys.N}"
            )

            fig.canvas.draw_idle()
            plt.pause(0.001)

            # Re-seed if completely dead
            if lenia_mass < 5.0 and sys.N == 0:
                print(f"  Collapse at step {step}. Re-seeding...")
                sys = CoupledSystem(rng)
                im.set_data(sys.A)

    plt.ioff()
    plt.close(fig)
    print(f"\n─── Finished after {step} steps ───")

if __name__ == "__main__":
    run()
