import random
import time
import argparse
import sys

class Cell:
    def __init__(self, id):
        self.id = id
        self.energy = 100.0
        self.pain = 0.0
        self.productivity_base = random.uniform(0.5, 1.5)
        self.alive = True
        
    def work(self):
        if not self.alive:
            return 0
        
        # When pain is high or energy is very low, productivity drops.
        efficiency = (max(0, self.energy) / 100.0) * (1.0 - (min(self.pain, 100) / 100.0))
        value_produced = self.productivity_base * efficiency * 10
        
        # Working costs energy and induces wear and tear (pain)
        self.energy -= random.uniform(5, 15)
        self.pain += random.uniform(2, 8)
        
        # Check death conditions
        if self.energy <= 0 or self.pain >= 100:
            self.alive = False
            self.energy = 0
            
        return max(0, value_produced)
        
    def heal(self, resources):
        if not self.alive:
            return
        # Resources convert to energy and reduce pain
        self.energy = min(100.0, self.energy + resources * 2)
        self.pain = max(0.0, self.pain - resources * 1.5)

class DAOEcosystem:
    def __init__(self, num_cells, strategy):
        self.cells = [Cell(i) for i in range(num_cells)]
        self.wealth = 0.0
        self.strategy = strategy
        self.step = 0
        
    def simulate_step(self):
        self.step += 1
        total_produced = 0
        
        # 1. Cells Work
        for cell in self.cells:
            if cell.alive:
                total_produced += cell.work()
                
        # DAO takes a cut of the production
        dao_cut = total_produced * 0.2
        available_resources = total_produced * 0.8  # what the DAO can distribute back
        
        self.wealth += dao_cut
        
        # 2. DAO distributes resources based on fitness function / strategy
        alive_cells = [c for c in self.cells if c.alive]
        
        if not alive_cells:
            return False # Entire substrate is dead
            
        if self.strategy == "capitalism":
            # Optimizes for max return: gives resources to the most productive cells
            # ignoring their pain.
            alive_cells.sort(key=lambda c: c.productivity_base, reverse=True)
            # Give to top 20%
            top_performers = alive_cells[:max(1, len(alive_cells) // 5)]
            resources_per_cell = available_resources / len(top_performers)
            for cell in top_performers:
                cell.heal(resources_per_cell)
                
        elif self.strategy == "homeostasis":
            # Optimizes for system health: routes resources to where pain is highest
            # (acting like a nervous system / immune response)
            alive_cells.sort(key=lambda c: c.pain, reverse=True)
            # Help the ones struggling the most
            struggling_cells = alive_cells[:max(1, len(alive_cells) // 2)]
            if struggling_cells:
                resources_per_cell = available_resources / len(struggling_cells)
                for cell in struggling_cells:
                    cell.heal(resources_per_cell)
        
        return True

    def stats(self):
        alive_cells = [c for c in self.cells if c.alive]
        num_alive = len(alive_cells)
        if num_alive == 0:
            return f"Step {self.step:03d} | DAO Wealth: {self.wealth:7.1f} | ALL CELLS DEAD (SYSTEM COLLAPSE)"
            
        avg_energy = sum(c.energy for c in alive_cells) / num_alive
        avg_pain = sum(c.pain for c in alive_cells) / num_alive
        
        return (f"Step {self.step:03d} | Alive: {num_alive:3} | "
                f"Avg Energy: {avg_energy:5.1f} | Avg Pain: {avg_pain:5.1f} | "
                f"DAO Wealth: {self.wealth:7.1f}")

def main():
    parser = argparse.ArgumentParser(description="Simulate a DAO Ecosystem with different fitness functions.")
    parser.add_argument('--strategy', type=str, choices=['capitalism', 'homeostasis'], default='capitalism',
                        help='Strategy for resource distribution: capitalism (max profit) or homeostasis (system health)')
    parser.add_argument('--steps', type=int, default=50, help='Number of simulation steps')
    args = parser.parse_args()
    
    print(f"--- Starting Simulation: Strategy '{args.strategy.upper()}' ---")
    dao = DAOEcosystem(num_cells=100, strategy=args.strategy)
    
    for _ in range(args.steps):
        sys.stdout.write('\r' + dao.stats())
        sys.stdout.flush()
        running = dao.simulate_step()
        time.sleep(0.1)
        if not running:
            sys.stdout.write('\r' + dao.stats() + "\n")
            print("\nSimulation aborted due to total biological collapse.")
            break
            
    if dao.step == args.steps:
        print("\n\n--- Simulation Finished ---")
        final_alive = len([c for c in dao.cells if c.alive])
        print(f"Final alive cells: {final_alive}/100")
        print(f"Final DAO wealth: {dao.wealth:.1f}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSimulation manually stopped.")
