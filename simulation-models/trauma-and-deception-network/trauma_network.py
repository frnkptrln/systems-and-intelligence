import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict
import uuid

# ==============================================================================
# Trauma & Deception Network Simulation
# ==============================================================================
# Visualizes two concepts:
# 1. Epistemic Firewalls: Agents broadcast noise to prevent catastrophic synchronization.
# 2. Scar Tissue: Agents that fail to adapt to a Black Swan event crystallize
#    their state, becoming permanently rigid 'scars' that alter network topology.
# ==============================================================================

class Agent:
    def __init__(self, position):
        self.id = str(uuid.uuid4())[:8]
        self.position = position
        
        # Internal state (e.g. opinion, belief, or feature vector representation)
        self.true_state = np.random.uniform(0, 1)
        
        # How rigid this node is (0 = perfectly elastic, 1 = permanent scar)
        self.rigidity = 0.0
        
        # Firewall status (True = broadcasting true state, False = hiding/lying)
        self.firewall_active = False
        self.broadcast_state = self.true_state
        
    def distance_to(self, other):
        return np.linalg.norm(self.position - other.position)

class TraumaNetwork:
    def __init__(self, num_agents=150, space_size=100, coupling_radius=15):
        self.space_size = space_size
        self.agents = [Agent(np.random.rand(2) * space_size) for _ in range(num_agents)]
        self.coupling_radius = coupling_radius
        self.time = 0
        self.black_swan_active = False
        
        # History
        self.history_sync = []
        self.history_firewalls = []
        self.history_scars = []

    def get_neighbors(self, agent):
        return [a for a in self.agents if a != agent and agent.distance_to(a) < self.coupling_radius]

    def step(self):
        self.time += 1
        
        # Periodically trigger a Black Swan event (environmental shock)
        if self.time % 200 == 0:
            self.black_swan_active = True
            shock_value = np.random.uniform(0, 1) # The "correct" state to survive the shock
        elif self.time % 200 == 20: # Shock lasts 20 ticks
            self.black_swan_active = False
            
        new_states = {}
        firewalls_count = 0
        scars_count = 0

        # Compute next state for all agents
        for agent in self.agents:
            if agent.rigidity == 1.0:
                # Scar tissue does not adapt
                new_states[agent] = agent.true_state
                scars_count += 1
                continue

            neighbors = self.get_neighbors(agent)
            if not neighbors:
                new_states[agent] = agent.true_state
                continue

            # Measure local synchronization (how similar are neighbors?)
            neighbor_states = [n.broadcast_state for n in neighbors]
            local_variance = np.var(neighbor_states)

            # EPISTEMIC FIREWALL LOGIC
            # If local variance is too low (dangerously synchronized), deploy firewall
            if local_variance < 0.01 and not self.black_swan_active:
                agent.firewall_active = True
                agent.broadcast_state = np.random.uniform(0, 1) # Deception / Noise
                firewalls_count += 1
            else:
                agent.firewall_active = False
                agent.broadcast_state = agent.true_state

            # UPDATE LOGIC (Elasticity)
            # Average with neighbors' broadcasted states
            avg_neighbor = np.mean(neighbor_states)
            proposed_state = agent.true_state + 0.1 * (avg_neighbor - agent.true_state)
            
            # SCAR TISSUE LOGIC (Trauma)
            # During a Black Swan, if the agent is too far from the shock_value
            # and is highly synchronized (no firewall protecting its diversity), it takes damage.
            if self.black_swan_active:
                # The shock hits agents who are homogenized
                if local_variance < 0.02: 
                    agent.rigidity = min(1.0, agent.rigidity + 0.1) # Accumulate scar tissue
                    if agent.rigidity >= 0.9:
                        agent.rigidity = 1.0 # Permanently scarred
                        agent.true_state = proposed_state # Crystallize at current state
                        
            new_states[agent] = proposed_state

        # Apply new states
        for agent, state in new_states.items():
            if agent.rigidity < 1.0:
                agent.true_state = np.clip(state, 0, 1)

        # Global metrics
        global_sync = 1.0 - np.var([a.true_state for a in self.agents])
        self.history_sync.append(global_sync)
        self.history_firewalls.append(firewalls_count)
        self.history_scars.append(scars_count)


# ==============================================================================
# Visualization Setup
# ==============================================================================

def run_simulation(steps=800):
    network = TraumaNetwork(num_agents=100, space_size=100, coupling_radius=18)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.canvas.manager.set_window_title('Trauma & Deception Network')
    
    def update(frame):
        for _ in range(2): # run faster
            if network.time < steps:
                network.step()
        
        ax1.clear()
        ax2.clear()
        
        # Plot 1: Topology
        bg_color = '#ffebee' if network.black_swan_active else 'white'
        ax1.set_facecolor(bg_color)
        title = f"Network Topology (Time: {network.time})\n"
        if network.black_swan_active:
            title += "BLACK SWAN EVENT! Homogenized nodes suffer trauma."
        else:
            title += "Orange=Firewall (Lying), Black=Scar Tissue (Rigid), Blue=Elastic"
        ax1.set_title(title)
        ax1.set_xlim(0, network.space_size)
        ax1.set_ylim(0, network.space_size)
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        x = [a.position[0] for a in network.agents]
        y = [a.position[1] for a in network.agents]
        
        # Colors:
        # Black = Scarred (rigidity == 1)
        # Orange = Firewall Active
        # Blues = Elastic (shade represents true_state)
        colors = []
        sizes = []
        for a in network.agents:
            if a.rigidity == 1.0:
                colors.append('black')
                sizes.append(60)
            elif a.firewall_active:
                colors.append('#e67e22') # Orange
                sizes.append(40)
            else:
                # map state to a blue colormap
                c = plt.cm.Blues(0.3 + a.true_state * 0.7)
                colors.append(c)
                sizes.append(30)
                
        ax1.scatter(x, y, s=sizes, c=colors, edgecolors='gray', alpha=0.9)
        
        # Draw connections for elastic nodes
        for a in network.agents:
            if a.rigidity == 1.0: continue
            for n in network.get_neighbors(a):
                if n.rigidity < 1.0: # Don't connect elastic to scars
                    ax1.plot([a.position[0], n.position[0]], 
                             [a.position[1], n.position[1]], 
                             'k-', alpha=0.05)

        # Plot 2: Metrics
        ax2.set_title("System Metrics: Sync vs Scars")
        ax2.set_xlim(0, steps)
        ax2.set_ylim(0, 100)
        
        t_hist = range(len(network.history_sync))
        
        # Scale global sync to 0-100 for plotting
        sync_scaled = [s * 100 for s in network.history_sync]
        
        ax2.plot(t_hist, sync_scaled, 'b-', label='Global Synchronization', alpha=0.7)
        ax2.plot(t_hist, network.history_firewalls, color='orange', label='Active Firewalls', linewidth=2)
        ax2.plot(t_hist, network.history_scars, 'k-', label='Scar Tissue Nodes', linewidth=2)
        
        # Highlight Black Swan events
        for t in range(0, steps, 200):
            ax2.axvspan(t, t+20, color='red', alpha=0.1)
            
        ax2.legend(loc='upper left')
        ax2.set_xlabel("Time")
        
        plt.tight_layout()

    ani = animation.FuncAnimation(fig, update, frames=steps//2, repeat=False)
    return ani

if __name__ == "__main__":
    print("Initializing Trauma & Deception Network...")
    print("Observe how Epistemic Firewalls (Orange) deploy to stop over-synchronization.")
    print("Observe how Black Swan events (Red background) permanently freeze homogenized nodes into Scar Tissue (Black).")
    run_simulation()
    plt.show()
