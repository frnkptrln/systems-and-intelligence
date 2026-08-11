#!/usr/bin/env python3
"""
morphospace_visualizer.py

Visualizes a repository-local toy plane (component coverage vs. coherence).

This predates and is not Perrier & Bennett's three-axis identity morphospace.
The trajectories are hand-constructed illustrations, not measured agents.
"""

import numpy as np
import matplotlib.pyplot as plt

def generate_trajectory(steps=100, entropy_vortex=False):
    """
    Simulates an agent's path through the morphospace.
    """
    # X axis: fractional component coverage (P)
    # Y axis: Coherence (C)
    P = np.linspace(0.9, 0.4, steps) # Identity fades as task gets harder
    C = np.linspace(0.95, 0.5, steps) # Coherence drops
    
    if entropy_vortex:
        # Add 'flickering' noise
        P += np.random.normal(0, 0.05, steps)
        C += np.random.normal(0, 0.05, steps)
    
    return np.clip(P, 0, 1), np.clip(C, 0, 1)

def plot_morphospace():
    print("═" * 60)
    print("  TOOL: Identity Morphospace Plotter")
    print("═" * 60)
    
    plt.figure(figsize=(10, 8))
    plt.style.use('dark_background')
    
    # ── Background Regions ──
    plt.axvspan(0.7, 1.0, 0.7, 1.0, color="#224422", alpha=0.3, label="High-coverage region")
    plt.axvspan(0.0, 0.4, 0.0, 0.4, color="#442222", alpha=0.3, label="Low-coverage region")
    
    # ── Plot Trajectories ──
    # 1. Stable Agent (TEO Chord)
    p1, c1 = generate_trajectory(steps=50, entropy_vortex=False)
    plt.plot(p1, c1, 'o-', color="#80ffb0", label="Synthetic smooth trace", alpha=0.6, markersize=3)
    plt.annotate("Start", (p1[0], c1[0]), color="#80ffb0", fontsize=8)
    plt.annotate("Stable End", (p1[-1], c1[-1]), color="#80ffb0", fontsize=8)
    
    # 2. Unstable Agent (Standard Scaffold)
    p2, c2 = generate_trajectory(steps=50, entropy_vortex=True)
    # Make it fade more aggressively
    p2 = np.clip(p2 - 0.2, 0.1, 0.9)
    plt.plot(p2, c2, 'x--', color="#ff6060", label="Synthetic noisy trace", alpha=0.6)
    plt.annotate("Low-coverage end", (p2[-1], c2[-1]), color="#ff6060", fontsize=8)
    
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel("Local fractional component coverage (P)")
    plt.ylabel("Selected coherence statistic (C)")
    plt.title("Illustrative Coverage/Coherence Plane", color="#e0e0ff", pad=20)
    plt.legend(loc="upper left")
    plt.grid(alpha=0.1)
    
    output_path = "identity_morphospace_plot.png"
    plt.savefig(output_path)
    print(f"\nVisual results saved to: {output_path}")
    print("═" * 60)

if __name__ == "__main__":
    plot_morphospace()
