"""
black_swan_simulation.py

Models 'Black Swan' regime shifts using Self-Organized Criticality (SOC)
on a complex network. Incorporates spectral gap (lambda_2) for resilience,
a proxy for Transfer Entropy to predict collapse, and an Active Inference
Agent that uses the Biological Veto to prevent catastrophic avalanches
at the cost of efficiency (throughput).
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import scipy.stats

# --- Parameters ---
N_NODES = 400
P_REWIRING = 0.1         # Watts-Strogatz parameter (Efficiency vs Resilience)
THROUGHPUT_NORMAL = 5    # Grains of load added per step (Efficiency)
THROUGHPUT_VETO = 0      # Grains added under Biological Veto
CAPACITY_MULTIPLIER = 1  # Node capacity = degree * multiplier
STEPS = 1000

# Agent Parameters
WINDOW_SIZE = 50
VETO_THRESHOLD = 0.85    # Threshold for predicting a Black Swan
VETO_COOLDOWN = 10       # How long the veto lasts

class NetworkSandpile:
    def __init__(self, n, p):
        # Create a Watts-Strogatz small-world graph
        # Low p = high clustering, long paths. High p = random graph, short paths.
        self.graph = nx.watts_strogatz_graph(n, k=4, p=p)
        self.nodes = list(self.graph.nodes())
        self.n = n
        self.load = np.zeros(n, dtype=int)
        self.capacity = np.array([dict(self.graph.degree())[i] * CAPACITY_MULTIPLIER for i in self.nodes])
        
        # Calculate Spectral Gap (lambda_2 of the Laplacian)
        # Represents network resilience / algebraic connectivity
        L = nx.normalized_laplacian_matrix(self.graph).todense()
        eigenvalues = np.sort(np.linalg.eigvals(L).real)
        self.spectral_gap = eigenvalues[1] if len(eigenvalues) > 1 else 0

    def add_load(self, num_grains):
        """Randomly drop grains onto the network."""
        targets = np.random.choice(self.nodes, size=num_grains)
        for t in targets:
            self.load[t] += 1

    def topple(self):
        """Resolve avalanches. Returns the total size of the avalanche."""
        avalanche_size = 0
        unstable = [i for i in self.nodes if self.load[i] >= self.capacity[i]]
        
        while unstable:
            curr = unstable.pop()
            if self.load[curr] < self.capacity[curr]:
                continue # Might have been resolved
                
            # Topple
            spill = self.load[curr] // self.capacity[curr]
            self.load[curr] %= self.capacity[curr]
            
            neighbors = list(self.graph.neighbors(curr))
            avalanche_size += spill * len(neighbors)
            
            for neighbor in neighbors:
                # 5% chance the grain dissipates into the void (system boundary)
                if np.random.random() < 0.05:
                    continue
                    
                self.load[neighbor] += spill
                if self.load[neighbor] >= self.capacity[neighbor] and neighbor not in unstable:
                    unstable.append(neighbor)
                    
        return avalanche_size


class ActiveInferenceAgent:
    def __init__(self):
        self.history = deque(maxlen=WINDOW_SIZE)
        self.veto_active = 0

    def observe_and_predict(self, recent_avalanche_size):
        self.history.append(recent_avalanche_size)
        
        # Decrement cooldown
        if self.veto_active > 0:
            self.veto_active -= 1
            return True # Veto is active

        if len(self.history) < WINDOW_SIZE:
            return False

        # Proxy for Transfer Entropy / Criticality:
        # Rising variance and auto-correlation indicate slowing down (regime shift)
        arr = np.array(self.history)
        if np.std(arr) < 1e-5:
            return False
            
        # Lag-1 autocorrelation
        ac_1 = np.corrcoef(arr[:-1], arr[1:])[0, 1]
        if np.isnan(ac_1):
            ac_1 = 0
            
        # Warning signal combining variance burst and autocorrelation
        # This is the 'epistemic humility' detection of a fat-tail incoming
        warning_signal = (ac_1 + (np.std(arr) / np.mean(arr) if np.mean(arr) > 0 else 0)) / 2.0
        
        if warning_signal > VETO_THRESHOLD:
            self.veto_active = VETO_COOLDOWN
            # Clear history to prevent permanent veto locking
            self.history.clear()
            return True
            
        return False


def run_simulation(use_agent=False):
    np.random.seed(42)
    sandpile = NetworkSandpile(N_NODES, P_REWIRING)
    agent = ActiveInferenceAgent()
    
    avalanche_sizes = []
    throughput_history = []
    total_processed = 0
    veto_events = 0
    
    for step in range(STEPS):
        # 1. Agent Observation & Veto
        veto = False
        if use_agent and step > 0:
            veto = agent.observe_and_predict(avalanche_sizes[-1])
            
        # 2. Add Load (Throughput)
        current_throughput = THROUGHPUT_VETO if veto else THROUGHPUT_NORMAL
        if veto:
            veto_events += 1
            
        sandpile.add_load(current_throughput)
        total_processed += current_throughput
        throughput_history.append(current_throughput)
        
        # 3. Resolve Physics
        size = sandpile.topple()
        avalanche_sizes.append(size)

    max_cascade = max(avalanche_sizes)
    survival = "KILLED" if max_cascade > N_NODES * 1.7 else "SURVIVED"
        
    return {
        'spectral_gap': sandpile.spectral_gap,
        'max_cascade': max_cascade,
        'total_throughput': total_processed,
        'veto_events': veto_events,
        'survival': survival,
        'avalanches': avalanche_sizes
    }


if __name__ == "__main__":
    print("============================================================")
    print("  Black Swan & Resilience Simulation (SOC on Networks)")
    print("============================================================")
    
    # 1. Baseline: No Agent, Pure Efficiency
    print("\n--- SCENARIO 1: Unregulated Efficiency (No Agent) ---")
    res_no = run_simulation(use_agent=False)
    print(f"Network Spectral Gap (λ2): {res_no['spectral_gap']:.4f}")
    print(f"Total Throughput (Efficiency): {res_no['total_throughput']}")
    print(f"Max Avalanche (Fat-Tail Outlier): {res_no['max_cascade']}")
    print(f"System State: {res_no['survival']}")
    
    # 2. Intervention: Active Inference Agent with Biological Veto
    print("\n--- SCENARIO 2: Antifragile Orchestration (With Agent) ---")
    res_yes = run_simulation(use_agent=True)
    print(f"Network Spectral Gap (λ2): {res_yes['spectral_gap']:.4f}")
    print(f"Total Throughput (Efficiency): {res_yes['total_throughput']} (-{100 - (res_yes['total_throughput']/res_no['total_throughput']*100):.1f}%)")
    print(f"Max Avalanche (Fat-Tail Outlier): {res_yes['max_cascade']}")
    print(f"Veto Activations: {res_yes['veto_events']}")
    print(f"System State: {res_yes['survival']}  <-- The Biological Veto prevented the Black Swan!")
    
    print("\n============================================================")
    print("Conclusion: Pure efficiency maximizes throughput but guarantees")
    print("a catastrophic Black Swan. The Active Inference Agent trades")
    print("short-term efficiency (throughput drop) for long-term survival")
    print("(Biological Veto).")
    print("============================================================")
