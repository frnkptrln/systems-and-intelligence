import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import sys
import os

# Add the simulation directory to path so we can import lenia
sys.path.append(os.path.join(os.path.dirname(__file__), 'simulation-models', 'lenia'))
from lenia import make_kernel, init_world, lenia_step, _CMAP, GRID_SIZE, KERNEL_R, DT, MU, SIGMA

def generate_lenia_gif(output_path, num_frames=150):
    print("Generating Lenia GIF...")
    rng = np.random.default_rng(42)
    kernel = make_kernel(KERNEL_R)
    A = init_world(rng)
    
    # Pre-warm the simulation so we don't just see the initial random noise
    for _ in range(50):
        A = lenia_step(A, kernel, MU, SIGMA, DT)
        
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#000008")
    
    im = ax.imshow(
        A, cmap=_CMAP,
        interpolation="bilinear",
        vmin=0, vmax=1.0,
        origin="lower",
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("#000008")
    fig.tight_layout()
    
    def update(frame):
        nonlocal A
        # Do multiple steps per frame to make the animation faster/more dynamic
        for _ in range(3):
            A = lenia_step(A, kernel, MU, SIGMA, DT)
        im.set_data(A)
        return [im]
        
    anim = FuncAnimation(fig, update, frames=num_frames, blit=True)
    anim.save(output_path, dpi=80, writer=PillowWriter(fps=20))
    plt.close(fig)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    os.makedirs("docs/assets/gifs", exist_ok=True)
    generate_lenia_gif("docs/assets/gifs/lenia_demo.gif")
