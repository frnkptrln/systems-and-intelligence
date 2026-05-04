#!/usr/bin/env python3
"""
evolutionary_optimizer.py

An automated tool to search for 'high-intelligence' regimes in 
simulation parameter spaces. Uses a basic Genetic Algorithm 
to maximize the SII score (or other complexity metrics).
"""

import numpy as np
import random

class EvolutionaryOptimizer:
    """
    Optimizes a set of parameters for a given objective function.
    """
    def __init__(self, obj_func, param_bounds, pop_size=10, generations=5):
        self.obj_func = obj_func
        self.param_bounds = param_bounds # List of (min, max) tuples
        self.pop_size = pop_size
        self.generations = generations
        self.population = self._init_population()

    def _init_population(self):
        pop = []
        for _ in range(self.pop_size):
            individual = [random.uniform(b[0], b[1]) for b in self.param_bounds]
            pop.append(individual)
        return pop

    def _evolve(self):
        # 1. Evaluate
        scores = [self.obj_func(ind) for ind in self.population]
        
        # 2. Select (Top 50%)
        ranked_indices = np.argsort(scores)[::-1]
        parents = [self.population[i] for i in ranked_indices[:self.pop_size//2]]
        
        # 3. Crossover & Mutation
        new_pop = list(parents)
        while len(new_pop) < self.pop_size:
            p1, p2 = random.sample(parents, 2)
            child = [(g1 + g2)/2 for g1, g2 in zip(p1, p2)] # Mean crossover
            # Mutation
            for i in range(len(child)):
                if random.random() < 0.2:
                    child[i] += random.normalvariate(0, 0.1)
                    child[i] = np.clip(child[i], self.param_bounds[i][0], self.param_bounds[i][1])
            new_pop.append(child)
        
        self.population = new_pop
        return max(scores), self.population[np.argmax(scores)]

    def run(self):
        best_score = -1
        best_params = None
        
        for g in range(self.generations):
            score, params = self._evolve()
            if score > best_score:
                best_score = score
                best_params = params
            print(f" Generation {g:2d} │ Best Fitness: {score:.4f}")
            
        return best_score, best_params

# --- Mock Objective Function (Simulating SII optimization for Lenia-like params) ---
def mock_sii_objective(params):
    # Simulated "Edge of Chaos" fitness: peaks at specific parameter ratios
    # params[0] = growth_rate, params[1] = kernel_size
    efficiency = np.exp(-(params[0]-0.5)**2 / 0.1)
    stability = np.exp(-(params[1]-5.0)**2 / 2.0)
    return efficiency * stability

def run_optimizer_demo():
    print("═" * 60)
    print("  TOOL: Evolutionary Parameter Optimizer")
    print("═" * 60)
    
    # Range for Growth Rate [0, 1] and Kernel Size [1, 10]
    bounds = [(0, 1), (1, 10)]
    
    opt = EvolutionaryOptimizer(mock_sii_objective, bounds, pop_size=12, generations=8)
    best_fitness, best_params = opt.run()
    
    print("\nOptimization Complete.")
    print(f" Best Fitness (SII Proxy): {best_fitness:.4f}")
    print(f" Optimal Parameters: Growth={best_params[0]:.3f}, Kernel={best_params[1]:.3f}")
    print("═" * 60)

if __name__ == "__main__":
    run_optimizer_demo()
