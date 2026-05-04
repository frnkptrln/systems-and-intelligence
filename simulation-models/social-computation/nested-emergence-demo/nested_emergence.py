#!/usr/bin/env python3
"""
nested_emergence.py

A demonstration of multi-scale emergence.
Level 1: Simple agents follow local rules to form stable clusters (Gliders/Patterns).
Level 2: These clusters are treated as 'meta-agents' that interact to form 
         higher-level structures.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class NestedWorld:
    """
    A 2D world where Level 1 cells form 'organisms' (Level 2).
    """
    def __init__(self, size=60):
        self.size = size
        self.grid = np.random.choice([0, 1], size=(size, size), p=[0.9, 0.1])
        
    def step_l1(self):
        """Standard Game of Life as the Level 1 substrate."""
        new_grid = self.grid.copy()
        for i in range(self.size):
            for j in range(self.size):
                # Count neighbors
                total = int((self.grid[i, (j-1)%self.size] + self.grid[i, (j+1)%self.size] +
                             self.grid[(i-1)%self.size, j] + self.grid[(i+1)%self.size, j] +
                             self.grid[(i-1)%self.size, (j-1)%self.size] + self.grid[(i-1)%self.size, (j+1)%self.size] +
                             self.grid[(i+1)%self.size, (j-1)%self.size] + self.grid[(i+1)%self.size, (j+1)%self.size]))
                
                if self.grid[i, j] == 1:
                    if (total < 2) or (total > 3):
                        new_grid[i, j] = 0
                else:
                    if total == 3:
                        new_grid[i, j] = 1
        self.grid = new_grid

    def get_l2_agents(self, kernel_size=10):
        """
        Scan the grid for 'stable' clusters of activity.
        L2 agents are defined by local density peaks.
        """
        l2_positions = []
        for i in range(0, self.size, kernel_size):
            for j in range(0, self.size, kernel_size):
                sub = self.grid[i:i+kernel_size, j:j+kernel_size]
                if sub.sum() > (kernel_size * kernel_size * 0.1): # Density threshold
                    l2_positions.append((i + kernel_size//2, j + kernel_size//2))
        return np.array(l2_positions)

def run_nested_demo(steps=200):
    print("═" * 60)
    print("  SIMULATION: Nested Emergence (L1 → L2)")
    print("═" * 60)
    
    world = NestedWorld(size=64)
    
    # Pre-run to stabilize L1
    for _ in range(50):
        world.step_l1()
        
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    plt.style.use('dark_background')
    
    img = ax1.imshow(world.grid, cmap='magma', interpolation='nearest')
    ax1.set_title("Level 1: Substrate (Cellular Automata)")
    
    l2_scatter = ax2.scatter([], [], c='#80ffb0', s=100, edgecolors='white')
    ax2.set_xlim(0, 64)
    ax2.set_ylim(0, 64)
    ax2.set_title("Level 2: Emergent 'Meta-Agents' (Clusters)")
    ax2.invert_yaxis()

    def update(frame):
        world.step_l1()
        img.set_data(world.grid)
        
        l2_agents = world.get_l2_agents()
        if len(l2_agents) > 0:
            l2_scatter.set_offsets(l2_agents[:, [1, 0]]) # Swap for plot coordinates
        else:
            l2_scatter.set_offsets(np.empty((0, 2)))
            
        return img, l2_scatter

    # We save a short gif or plot rather than live animation in this headless env
    # For now, just save a final frame comparison
    for _ in range(30):
        world.step_l1()
        
    img.set_data(world.grid)
    l2_agents = world.get_l2_agents()
    if len(l2_agents) > 0:
        l2_scatter.set_offsets(l2_agents[:, [1, 0]])
        
    plt.savefig("nested_emergence_results.png")
    print("\nSimulation complete. Results saved to: nested_emergence_results.png")
    print(f"Identified {len(l2_agents)} Level-2 'Meta-Agents' in the final state.")
    print("═" * 60)

if __name__ == "__main__":
    run_nested_demo()
