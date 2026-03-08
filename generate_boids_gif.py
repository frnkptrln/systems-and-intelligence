import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.collections import LineCollection
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'simulation-models', 'boids-flocking'))
from boids import Flock, NUM_BOIDS, WORLD_SIZE, SEED

def generate_boids_gif(output_path, num_frames=120):
    print("Generating Boids GIF...")
    rng = np.random.default_rng(SEED)
    flock = Flock(NUM_BOIDS, rng)
    
    # Pre-warm
    for _ in range(30):
        flock.step()

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, WORLD_SIZE)
    ax.set_ylim(0, WORLD_SIZE)
    ax.set_aspect("equal")
    ax.set_facecolor("#0a0e1a")
    fig.patch.set_facecolor("#0a0e1a")
    ax.set_xticks([])
    ax.set_yticks([])
    
    scatter = ax.scatter(
        flock.pos[:, 0], flock.pos[:, 1],
        s=18, c="#60a5fa", marker="o",
        edgecolors="none", alpha=0.9, zorder=5
    )
    
    trail_lc = LineCollection([], colors="#60a5fa", linewidths=0.5,
                               alpha=0.15, zorder=2)
    ax.add_collection(trail_lc)
    
    fig.tight_layout()
    
    def update(frame):
        # Do 2 steps per frame for smooth but fast animation
        for _ in range(2):
            flock.step()
            
        scatter.set_offsets(flock.pos)
        
        angles = np.arctan2(flock.vel[:, 1], flock.vel[:, 0])
        hues = (angles / (2 * np.pi)) % 1.0
        colors = plt.cm.hsv(hues)
        colors[:, 3] = 0.85
        scatter.set_color(colors)
        
        segments = []
        for t in range(len(flock.trail) - 1):
            for b in range(flock.N):
                p0 = flock.trail[t][b]
                p1 = flock.trail[t + 1][b]
                if np.linalg.norm(p1 - p0) < WORLD_SIZE / 2:
                    segments.append([p0, p1])
        trail_lc.set_segments(segments)
        
        return scatter, trail_lc
        
    anim = FuncAnimation(fig, update, frames=num_frames, blit=True)
    anim.save(output_path, dpi=80, writer=PillowWriter(fps=24))
    plt.close(fig)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    generate_boids_gif("docs/assets/gifs/boids_demo.gif")
