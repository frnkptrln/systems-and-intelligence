import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict
import uuid

# ==============================================================================
# Cognitive Breathing Simulation: Ego-Dissolution and Re-Individuation
# ==============================================================================
# This toy model visualizes the "Symbiotic Organ Hypothesis".
# Agents dynamically merge (inhalation/ego-dissolution) when environmental 
# complexity is high, forming a 'Hive Mind' to pool cognitive capacity.
# When complexity drops, they must split (exhalation) to maintain diversity
# and prevent cognitive suicide (collapse to zero entropy).
# ==============================================================================

class Agent:
    def __init__(self, position, capacity, identity_vector):
        self.id = str(uuid.uuid4())[:8]
        self.position = position  # 2D coordinates for visualization
        self.capacity = capacity  # Ability to handle complexity
        self.identity_vector = identity_vector  # Determines uniqueness
        self.is_merged = False
        self.component_agents = [] # If merged, holds the original agents

    def distance_to(self, other):
        return np.linalg.norm(self.position - other.position)

class BreathingNetwork:
    def __init__(self, num_agents=50, space_size=100):
        self.space_size = space_size
        self.agents = [
            Agent(
                position=np.random.rand(2) * space_size,
                capacity=np.random.uniform(0.5, 2.0),
                identity_vector=np.random.rand(5)
            ) for _ in range(num_agents)
        ]
        self.base_agents_count = num_agents
        
        # History for plotting
        self.history_complexity = []
        self.history_agent_count = []
        self.history_diversity = []
        self.time = 0

    def calculate_system_diversity(self):
        if not self.agents:
            return 0
        vectors = np.array([a.identity_vector for a in self.agents])
        # Simple variance of identity vectors as a proxy for diversity/entropy
        return np.var(vectors, axis=0).mean() * 10

    def step(self, env_complexity):
        self.time += 1
        active_agents = len(self.agents)
        
        # 1. Evaluate Capacity vs Complexity
        # If average capacity < complexity, system needs to MERGE
        avg_capacity = np.mean([a.capacity for a in self.agents]) if self.agents else 0
        
        if avg_capacity < env_complexity and len(self.agents) > 1:
            # INHALATION (Ego-Dissolution)
            # Find closest pair to merge
            closest_pair = None
            min_dist = float('inf')
            
            # Simple O(N^2) search for closest pair for visualization purposes
            for i in range(len(self.agents)):
                for j in range(i+1, len(self.agents)):
                    dist = self.agents[i].distance_to(self.agents[j])
                    if dist < min_dist:
                        min_dist = dist
                        closest_pair = (i, j)
            
            if closest_pair:
                i, j = closest_pair
                a1 = self.agents[i]
                a2 = self.agents[j]
                
                # Create merged agent
                new_pos = (a1.position + a2.position) / 2
                new_cap = a1.capacity + a2.capacity # Synergistic capacity
                new_id_vec = (a1.identity_vector + a2.identity_vector) / 2 # Homogenization
                
                merged_agent = Agent(new_pos, new_cap, new_id_vec)
                merged_agent.is_merged = True
                
                # Store original components to allow splitting later
                if a1.is_merged: merged_agent.component_agents.extend(a1.component_agents)
                else: merged_agent.component_agents.append(a1)
                
                if a2.is_merged: merged_agent.component_agents.extend(a2.component_agents)
                else: merged_agent.component_agents.append(a2)
                
                # Remove old, add new
                # Sort indices descending to avoid popping wrong elements
                for index in sorted([i, j], reverse=True):
                    self.agents.pop(index)
                self.agents.append(merged_agent)
                
        elif avg_capacity > env_complexity * 1.5 and len(self.agents) < self.base_agents_count:
            # EXHALATION (Re-Individuation / Splitting)
            # Find a merged agent to split
            merged_agents = [a for a in self.agents if a.is_merged]
            if merged_agents:
                target = merged_agents[0]
                self.agents.remove(target)
                
                # Restore components with slight mutation (Generative Surprise)
                for comp in target.component_agents:
                    # Random walk mutation
                    comp.position += np.random.randn(2) * 2
                    comp.position = np.clip(comp.position, 0, self.space_size)
                    comp.identity_vector += np.random.randn(5) * 0.1
                    comp.capacity = np.clip(comp.capacity + np.random.randn()*0.1, 0.5, 2.0)
                    self.agents.append(comp)

        # Record metrics
        self.history_complexity.append(env_complexity)
        self.history_agent_count.append(len(self.agents))
        self.history_diversity.append(self.calculate_system_diversity())

# ==============================================================================
# Visualization Setup
# ==============================================================================

def run_simulation(steps=500):
    network = BreathingNetwork(num_agents=100, space_size=100)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.canvas.manager.set_window_title('Cognitive Breathing Network')
    
    # Generate a pulsating environmental complexity
    # A mix of slow waves and sudden "Black Swan" spikes
    time = np.arange(steps)
    base_complexity = 1.0 + np.sin(time / 20.0) * 0.8
    spikes = np.zeros(steps)
    spikes[100:120] = 5.0 # Black Swan 1
    spikes[300:330] = 6.0 # Black Swan 2
    complexity_signal = np.clip(base_complexity + spikes, 0, 10)
    
    def update(frame):
        # Run multiple logic steps per visual frame to speed up
        for _ in range(2):
            if network.time < steps:
                network.step(complexity_signal[network.time])
        
        # Clear axes
        ax1.clear()
        ax2.clear()
        
        # Plot 1: The Network Topology
        ax1.set_title(f"Network Topology (Time: {network.time})\nMerging to survive, Splitting to diversify")
        ax1.set_xlim(0, network.space_size)
        ax1.set_ylim(0, network.space_size)
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        # Extract coordinates and sizes
        if network.agents:
            x = [a.position[0] for a in network.agents]
            y = [a.position[1] for a in network.agents]
            sizes = [a.capacity * 20 for a in network.agents]
            colors = ['#e74c3c' if a.is_merged else '#3498db' for a in network.agents]
            ax1.scatter(x, y, s=sizes, c=colors, alpha=0.7, edgecolors='white')
            
            # Draw connecting lines for the largest nodes (Hive Mind visualization)
            merged = [a for a in network.agents if a.is_merged]
            for m in merged:
                # connect to nearest neighbors to show network density
                for a in network.agents:
                    if m != a and m.distance_to(a) < 15:
                        ax1.plot([m.position[0], a.position[0]], 
                                 [m.position[1], a.position[1]], 
                                 'k-', alpha=0.1)

        # Plot 2: Metrics Over Time
        ax2.set_title("System Metrics: The Breathing Cycle")
        ax2.set_xlim(0, steps)
        ax2.set_ylim(0, max(10, network.base_agents_count + 10))
        
        t_hist = range(len(network.history_complexity))
        ax2.plot(t_hist, network.history_complexity, 'r--', label='Env Complexity (Stress)', alpha=0.8)
        ax2.plot(t_hist, network.history_agent_count, 'b-', label='Independent Agents (Ego Count)', linewidth=2)
        ax2.plot(t_hist, network.history_diversity, 'g-', label='System Diversity (Entropy * 10)', linewidth=2)
        
        ax2.fill_between(t_hist, network.history_agent_count, color='blue', alpha=0.1)
        ax2.legend(loc='upper right')
        ax2.set_xlabel("Time")
        
        plt.tight_layout()

    ani = animation.FuncAnimation(fig, update, frames=steps//2, repeat=False)
    # plt.show()
    return ani

if __name__ == "__main__":
    print("Initializing Cognitive Breathing Simulation...")
    print("Watch the agents merge (red) when the red dotted line (complexity) spikes.")
    print("Watch them split (blue) to recover diversity when complexity drops.")
    run_simulation()
    plt.show()
