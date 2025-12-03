import time
import random
import os
import sys

# --- SIMULATIONS-PARAMETER ---
GRID_SIZE = 30 
INITIAL_DENSITY = 0.25
SIMULATION_SPEED = 0.1

# Ziel-Füllgrad für Homeostase
TARGET_FILL = 0.30
BASE_BIRTH_PROB = 0.5
ADJUST_FACTOR = 1.5

# NEUER PARAMETER FÜR ROBUSTERE DYNAMIK
S4_SURVIVAL_PROB = 0.5 # Überlebenswahrscheinlichkeit, wenn eine Zelle 4 Nachbarn hat

EMPTY = ' '
MATTER = '#'

# (Unveränderte Hilfsfunktionen: initialize_grid, count_neighbors, population_stats, compute_birth_prob)
# ... [Code für initialize_grid, count_neighbors, population_stats, compute_birth_prob] ...

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
    """Zählt lebende Zellen und gibt (alive_count, fill_ratio) zurück."""
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
    Berechnet die Geburtswahrscheinlichkeit in Abhängigkeit vom Füllgrad.
    """
    diff = TARGET_FILL - fill_ratio
    p = BASE_BIRTH_PROB + ADJUST_FACTOR * diff
    p = max(0.0, min(1.0, p))
    return p

def apply_rule_set(grid, fill_ratio):
    """
    Wendet B3/S234 (Mod.) mit Homeostase an.
    Fokus auf Langlebigkeit von Clustern.
    """
    size = len(grid)
    new_grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    
    birth_prob = compute_birth_prob(fill_ratio)
    
    for r in range(size):
        for c in range(size):
            state = grid[r][c]
            neighbors = count_neighbors(grid, r, c)
            
            if state == MATTER:
                # Überleben: S23 (garantiert)
                if neighbors in [2, 3]:
                    new_grid[r][c] = MATTER
                
                # Modifikation: S4 (wahrscheinlich)
                elif neighbors == 4:
                    if random.random() < S4_SURVIVAL_PROB:
                        new_grid[r][c] = MATTER # Überlebt mit Wahrscheinlichkeit
                    else:
                        new_grid[r][c] = EMPTY # Stirbt an Überbevölkerung
                
                # Tod: Nachbarn 0, 1, 5 oder mehr
                else:
                    new_grid[r][c] = EMPTY
            else:
                # Geburt: B3 (Klassisch) mit Homeostase-Wahrscheinlichkeit
                if neighbors == 3 and random.random() < birth_prob:
                    new_grid[r][c] = MATTER
                else:
                    new_grid[r][c] = EMPTY
                    
    return new_grid, birth_prob

def print_grid(grid, generation, alive, fill_ratio, birth_prob):
    os.system('cls' if os.name == 'nt' else 'clear')

    header = f"🧬 Robuste Dynamik (B3/S234 Mod.) - Gen: {generation:03d}"
    
    print("-" * (len(header) + 4))
    print(f"| {header} |")
    print(f"| Alive: {alive:4d}  Füllgrad: {fill_ratio*100:5.1f}%  Ziel: {TARGET_FILL*100:4.1f}% |")
    print(f"| Geburts-Wahrscheinlichkeit: {birth_prob:.3f} |")
    print("-" * (len(header) + 4))
    
    border = '+' + '-' * (len(grid[0]) * 2 + 1) + '+'
    print(border)
    
    for row in grid:
        print('| ' + ' '.join(row) + ' |')

    print(border)
    print(f"Geschw: {1/SIMULATION_SPEED:.1f} Gen/s. [Strg+C] zum Beenden.")
    print("Die modifizierte S234-Regel erlaubt langlebigere, dichtere Cluster bei stabiler Dichte.")

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
        print("\n\nSimulation beendet.")
        sys.exit(0)

if __name__ == "__main__":
    main()
