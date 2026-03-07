import time
import random
import os
import sys

# --- SIMULATION PARAMETERS ---
GRID_SIZE = 30 
INITIAL_DENSITY = 0.25
SIMULATION_SPEED = 0.1

# Target fill ratio for homeostasis
TARGET_FILL = 0.30
BASE_BIRTH_PROB = 0.5
ADJUST_FACTOR = 1.5

# PARAMETER FOR MORE ROBUST DYNAMICS
S4_SURVIVAL_PROB = 0.5 # Survival probability when a cell has 4 neighbors

EMPTY = ' '
MATTER = '#'

def initialize_grid(size, density):
    grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    start = size // 5
    end = size - size // 5
    
    for r in range(start, end):
        for c in range(start, end):
            if random.random() < density:
                grid[r][c] = MATTER
    return grid

def count_neighbors(grid, r, c):
    size = len(grid)
    count = 0
    
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and grid[nr][nc] == MATTER:
                count += 1
    return count

def population_stats(grid):
    """Counts living cells and returns (alive_count, fill_ratio)."""
    size = len(grid)
    alive = 0
    for r in range(size):
        for c in range(size):
            if grid[r][c] == MATTER:
                alive += 1
    total = size * size
    fill_ratio = alive / total
    return alive, fill_ratio

def compute_birth_prob(fill_ratio):
    """
    Computes the birth probability as a function of fill ratio.
    """
    diff = TARGET_FILL - fill_ratio
    p = BASE_BIRTH_PROB + ADJUST_FACTOR * diff
    p = max(0.0, min(1.0, p))
    return p

def apply_rule_set(grid, fill_ratio):
    """
    Applies B3/S234 (modified) with homeostasis.
    Focus on longevity of clusters.
    """
    size = len(grid)
    new_grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    
    birth_prob = compute_birth_prob(fill_ratio)
    
    for r in range(size):
        for c in range(size):
            state = grid[r][c]
            neighbors = count_neighbors(grid, r, c)
            
            if state == MATTER:
                # Survival: S23 (guaranteed)
                if neighbors in [2, 3]:
                    new_grid[r][c] = MATTER
                
                # Modification: S4 (probabilistic)
                elif neighbors == 4:
                    if random.random() < S4_SURVIVAL_PROB:
                        new_grid[r][c] = MATTER # Survives with probability
                    else:
                        new_grid[r][c] = EMPTY # Dies from overpopulation
                
                # Death: 0, 1, 5 or more neighbors
                else:
                    new_grid[r][c] = EMPTY
            else:
                # Birth: B3 (classic) with homeostasis probability
                if neighbors == 3 and random.random() < birth_prob:
                    new_grid[r][c] = MATTER
                else:
                    new_grid[r][c] = EMPTY
                    
    return new_grid, birth_prob

def print_grid(grid, generation, alive, fill_ratio, birth_prob):
    os.system('cls' if os.name == 'nt' else 'clear')

    header = f"🧬 Robust Dynamics (B3/S234 Mod.) - Gen: {generation:03d}"
    
    print("-" * (len(header) + 4))
    print(f"| {header} |")
    print(f"| Alive: {alive:4d}  Fill ratio: {fill_ratio*100:5.1f}%  Target: {TARGET_FILL*100:4.1f}% |")
    print(f"| Birth probability: {birth_prob:.3f} |")
    print("-" * (len(header) + 4))
    
    border = '+' + '-' * (len(grid[0]) * 2 + 1) + '+'
    print(border)
    
    for row in grid:
        print('| ' + ' '.join(row) + ' |')

    print(border)
    print(f"Speed: {1/SIMULATION_SPEED:.1f} gen/s. [Ctrl+C] to exit.")
    print("The modified S234 rule allows longer-lived, denser clusters at stable density.")

def main():
    grid = initialize_grid(GRID_SIZE, INITIAL_DENSITY)
    generation = 0
    
    try:
        while True:
            generation += 1

            alive, fill_ratio = population_stats(grid)
            grid, birth_prob = apply_rule_set(grid, fill_ratio)
            
            print_grid(grid, generation, alive, fill_ratio, birth_prob)
            time.sleep(SIMULATION_SPEED)

    except KeyboardInterrupt:
        print("\n\nSimulation ended.")
        sys.exit(0)

if __name__ == "__main__":
    main()
