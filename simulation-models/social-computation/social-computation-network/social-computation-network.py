import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.animation as animation
from collections import deque

class SocialComputationNetwork:
    """
    Simulates a network where nodes must share novel (entropy-reducing) 
    information to survive. Nodes that fail to exchange new information 
    "starve" and are removed from the network (cognitive suicide).
    """
    def __init__(self, num_nodes=50, initial_energy=10.0, energy_decay=0.5):
        self.num_nodes = num_nodes
        self.G = nx.erdos_renyi_graph(n=num_nodes, p=0.1)
        self.initial_energy = initial_energy
        self.energy_decay = energy_decay
        self.knowledge_pool_size = 100
        
        # Initialize node attributes
        for i in self.G.nodes():
            self.G.nodes[i]['energy'] = self.initial_energy
            # Each node starts with a random subset of "knowledge" (represented as integers)
            self.G.nodes[i]['knowledge'] = set(random.sample(range(self.knowledge_pool_size), 5))
            self.G.nodes[i]['alive'] = True

    def step(self):
        """Advances the simulation by one time step."""
        alive_nodes = [n for n in self.G.nodes() if self.G.nodes[n]['alive']]
        
        if not alive_nodes:
            return False # Network is dead
        
        # Energy decary for all alive nodes
        for n in alive_nodes:
            self.G.nodes[n]['energy'] -= self.energy_decay
            
            # Die if energy is depleted
            if self.G.nodes[n]['energy'] <= 0:
                self.G.nodes[n]['alive'] = False
                self.G.nodes[n]['energy'] = 0

        # Alive nodes exchange information with neighbors
        alive_nodes_after_decay = [n for n in self.G.nodes() if self.G.nodes[n]['alive']]
        
        for n in alive_nodes_after_decay:
            neighbors = list(self.G.neighbors(n))
            alive_neighbors = [neighbor for neighbor in neighbors if self.G.nodes[neighbor]['alive']]
            
            if not alive_neighbors:
                continue
                
            # Pick a random neighbor to interact with
            target = random.choice(alive_neighbors)
            
            # Node n shares its knowledge with target
            shared_info_n_to_target = set(random.sample(list(self.G.nodes[n]['knowledge']), min(3, len(self.G.nodes[n]['knowledge']))))
            
            # Target receives info. Calculate novelty (info target didn't already have)
            novel_info_for_target = shared_info_n_to_target - self.G.nodes[target]['knowledge']
            
            if novel_info_for_target:
                # Target gains energy from novel information
                energy_gain = len(novel_info_for_target) * 1.5
                self.G.nodes[target]['energy'] = min(self.initial_energy * 2, self.G.nodes[target]['energy'] + energy_gain)
                # Target learns the new info
                self.G.nodes[target]['knowledge'].update(novel_info_for_target)
                
                # Sender also gains a small "social cohesion" energy boost for successfully teaching
                self.G.nodes[n]['energy'] = min(self.initial_energy * 2, self.G.nodes[n]['energy'] + 0.5)

            
            # Nodes might discover completely new things (Open-ended evolution / Incompleteness)
            # This injects new entropy-reducing info into the network
            if random.random() < 0.05:
                new_discovery = random.randint(0, self.knowledge_pool_size * 2)
                self.G.nodes[n]['knowledge'].add(new_discovery)
                self.G.nodes[n]['energy'] = min(self.initial_energy * 2, self.G.nodes[n]['energy'] + 2.0)
                self.knowledge_pool_size = max(self.knowledge_pool_size, new_discovery + 1)

        return True

    def visualize(self, step_num):
        """Visualizes the current state of the network."""
        plt.clf()
        
        colors = []
        sizes = []
        
        for n in self.G.nodes():
            if self.G.nodes[n]['alive']:
                # Color based on energy
                energy = self.G.nodes[n]['energy']
                intensity = min(1.0, energy / (self.initial_energy * 2))
                colors.append((0.1, 0.8 * intensity, 0.2)) # Greenish, darker if low energy
                sizes.append(50 + energy * 10)
            else:
                colors.append('red')
                sizes.append(20)

        pos = nx.spring_layout(self.G, seed=42) # Consistent layout
        nx.draw(self.G, pos, node_color=colors, node_size=sizes, with_labels=False, edge_color='gray', alpha=0.6)
        
        alive_count = sum(1 for n in self.G.nodes() if self.G.nodes[n]['alive'])
        plt.title(f"Social Computation Network - Step {step_num}\nAlive Nodes: {alive_count}/{self.num_nodes}")


def run_simulation(steps=50):
    network = SocialComputationNetwork(num_nodes=60, initial_energy=8.0, energy_decay=1.0)
    
    fig = plt.figure(figsize=(10, 8))
    
    def update(frame):
        if frame > 0:
            network.step()
        network.visualize(frame)
        return []

    ani = animation.FuncAnimation(fig, update, frames=steps, interval=200, repeat=False)
    
    # Save as gif or simply show
    # ani.save("social_computation.gif", writer='imagemagick')
    plt.show()


if __name__ == "__main__":
    print("Starting Social Computation Network Simulation...")
    print("Nodes exchange information. Novel information grants energy.")
    print("Isolated nodes, or nodes in 'echo chambers' without new info, will 'starve' and die.")
    run_simulation(steps=100)
