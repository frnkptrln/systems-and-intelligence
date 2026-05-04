#!/usr/bin/env python3
"""
Economic Trust Network
--------------------------------------

An agent-based model exploring the emergence of specialized trade,
reputation, and wealth inequality from local interactions.

Each agent has:
- A set of skills (efficiency in producing specific resources)
- A portfolio of resources they need to consume to "survive"
- A local network of trade partners

Rules:
1. Produce: Agents produce resources they are best at.
2. Consume: Agents consume a mix of all resources. If they lack a resource, they lose "health".
3. Trade: Agents trade surplus for deficits with neighbors.
4. Trust: Agents can fulfill trades honestly or defect (steal). Defection gives short-term gain but lowers reputation.
5. Rewiring: Agents drop edges with low-reputation partners and seek new connections.

Press ESC in the matplotlib window to exit.
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.animation as animation
import random

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────
NUM_AGENTS = 80
NUM_RESOURCES = 3
INITIAL_ENERGY = 100.0
ENERGY_DECAY = 2.0  # cost of living per step
PRODUCTION_RATE = 5.0
TRADE_VOLUME = 3.0

# Trust/Reputation dynamics
INITIAL_TRUST = 0.5
CHEAT_PROB_BASE = 0.05
TRUST_DECAY = 0.98  # Trust decays towards 0 slowly without interaction
TRUST_BOOST = 0.1   # Gain from successful trade
TRUST_PENALTY = 0.4 # Penalty for cheating

# Network dynamics
REWIRING_THRESHOLD = 0.2
REWIRING_PROB = 0.1
MAX_DEGREE = 8

MAX_STEPS = 1000
DISPLAY_EVERY = 1
SEED = 42

# ─────────────────────────────────────────────
# Agent and Economy Logic
# ─────────────────────────────────────────────

class Agent:
    def __init__(self, id, rng):
        self.id = id
        self.energy = INITIAL_ENERGY
        self.alive = True
        
        # Determine specialization: random vector summing to 1.0
        # Highly specialized agents will have e.g. [0.9, 0.05, 0.05]
        # Generalists will have e.g. [0.33, 0.33, 0.33]
        base_skills = rng.random(NUM_RESOURCES)
        # Apply exponent to push towards specialization
        base_skills = base_skills ** 3
        self.skills = base_skills / base_skills.sum()
        
        # Strategy: how likely they are to cheat
        # 0 = always honest, 1 = always cheats
        self.cheat_tendency = rng.beta(1.5, 5.0) 
        
        # Current inventory of the 3 resources
        self.inventory = np.zeros(NUM_RESOURCES)
        
        # Reputation as perceived by the network (global average for visualization)
        self.global_reputation = INITIAL_TRUST

class EconomyGraph:
    def __init__(self, n, rng):
        self.rng = rng
        self.n = n
        self.agents = {i: Agent(i, rng) for i in range(n)}
        
        # Create initial random geometric graph (local clusters)
        pos = {i: (rng.random(), rng.random()) for i in range(n)}
        self.G = nx.random_geometric_graph(n, radius=0.15, pos=pos)
        
        # Ensure graph is connected initially
        while not nx.is_connected(self.G):
            self.G = nx.random_geometric_graph(n, radius=0.2, pos=pos)
            
        # Initialize edge attributes for trust
        for u, v in self.G.edges():
            self.G[u][v]['trust'] = INITIAL_TRUST

    def step(self):
        # 1. Production
        for i, agent in self.agents.items():
            if not agent.alive:
                continue
            # Produce according to skills
            production = agent.skills * PRODUCTION_RATE
            agent.inventory += production

        # 2. Consumption (Cost of living)
        # Agents need all resources to survive smoothly
        # Energy loss is higher if a resource is missing
        for i, agent in self.agents.items():
            if not agent.alive:
                continue
                
            consumption_need = ENERGY_DECAY / NUM_RESOURCES
            penalty = 0
            
            for r in range(NUM_RESOURCES):
                if agent.inventory[r] >= consumption_need:
                    agent.inventory[r] -= consumption_need
                else:
                    # Missing resource causes disproportionate energy loss
                    shortfall = consumption_need - agent.inventory[r]
                    agent.inventory[r] = 0
                    penalty += shortfall * 3.0
                    
            agent.energy -= (ENERGY_DECAY * 0.2 + penalty)
            
            # Starvation
            if agent.energy <= 0:
                agent.alive = False
                agent.energy = 0

        # 3. Trade
        alive_nodes = [i for i, a in self.agents.items() if a.alive]
        random.shuffle(alive_nodes)
        
        for u in alive_nodes:
            agent_u = self.agents[u]
            neighbors = list(self.G.neighbors(u))
            alive_neighbors = [v for v in neighbors if self.agents[v].alive]
            
            if not alive_neighbors:
                continue
                
            # Pick a partner weighted by trust
            trusts = [self.G[u][v]['trust'] for v in alive_neighbors]
            if sum(trusts) == 0:
                v = alive_neighbors[0]
            else:
                probs = np.array(trusts) / sum(trusts)
                v = np.random.choice(alive_neighbors, p=probs)
                
            agent_v = self.agents[v]
            
            # Determine what u needs most and what v can offer
            u_needs = np.argmin(agent_u.inventory)
            v_surplus = np.argmax(agent_v.inventory)
            
            # Reciprocal trade if they have complementary needs/surpluses
            if agent_v.inventory[v_surplus] > TRADE_VOLUME and agent_u.inventory[v_surplus] < TRADE_VOLUME:
                # v gives surplus to u
                
                # Does v cheat?
                v_cheats = self.rng.random() < agent_v.cheat_tendency
                # Does u cheat in return (not paying)?
                u_cheats = self.rng.random() < agent_u.cheat_tendency
                
                if not v_cheats and not u_cheats:
                    # Honest trade
                    agent_v.inventory[v_surplus] -= TRADE_VOLUME
                    agent_u.inventory[v_surplus] += TRADE_VOLUME
                    
                    # Assume u pays with their own surplus
                    u_surplus = np.argmax(agent_u.inventory)
                    if agent_u.inventory[u_surplus] > TRADE_VOLUME:
                        agent_u.inventory[u_surplus] -= TRADE_VOLUME
                        agent_v.inventory[u_surplus] += TRADE_VOLUME
                        
                    # Mutual trust boost
                    self.G[u][v]['trust'] = min(1.0, self.G[u][v]['trust'] + TRUST_BOOST)
                    # Both gain a bit of abstract energy representing "trade efficiency"
                    agent_u.energy = min(INITIAL_ENERGY * 2, agent_u.energy + 1.0)
                    agent_v.energy = min(INITIAL_ENERGY * 2, agent_v.energy + 1.0)
                    
                elif v_cheats and not u_cheats:
                    # v takes payment but gives nothing
                    u_surplus = np.argmax(agent_u.inventory)
                    if agent_u.inventory[u_surplus] > TRADE_VOLUME:
                        agent_u.inventory[u_surplus] -= TRADE_VOLUME
                        agent_v.inventory[u_surplus] += TRADE_VOLUME
                    self.G[u][v]['trust'] = max(0.01, self.G[u][v]['trust'] - TRUST_PENALTY)
                    
                elif u_cheats and not v_cheats:
                    # u takes goods but gives no payment
                    agent_v.inventory[v_surplus] -= TRADE_VOLUME
                    agent_u.inventory[v_surplus] += TRADE_VOLUME
                    self.G[u][v]['trust'] = max(0.01, self.G[u][v]['trust'] - TRUST_PENALTY)
                    
                else: # Both cheat - no goods exchanged, but trust broken
                    self.G[u][v]['trust'] = max(0.01, self.G[u][v]['trust'] - TRUST_PENALTY)

        # 4. Decay trust & update global reputation
        for u, v in self.G.edges():
            self.G[u][v]['trust'] = max(0.01, self.G[u][v]['trust'] * TRUST_DECAY)
            
        for i, agent in self.agents.items():
            if agent.alive:
                neighbors = list(self.G.neighbors(i))
                if neighbors:
                    agent.global_reputation = np.mean([self.G[i][v]['trust'] for v in neighbors])
                else:
                    agent.global_reputation = 0.0

        # 5. Network Rewiring
        edges_to_remove = []
        for u, v in self.G.edges():
            if self.G[u][v]['trust'] < REWIRING_THRESHOLD and self.rng.random() < REWIRING_PROB:
                edges_to_remove.append((u, v))
                
        self.G.remove_edges_from(edges_to_remove)
        
        # Nodes seek new connections
        for u in alive_nodes:
            if self.G.degree(u) < MAX_DEGREE and self.rng.random() < REWIRING_PROB * 2:
                # Prefer nodes with high global reputation
                candidates = [v for v in alive_nodes if v != u and not self.G.has_edge(u, v) and self.G.degree(v) < MAX_DEGREE]
                if candidates:
                    weights = [self.agents[v].global_reputation + 0.01 for v in candidates]
                    probs = np.array(weights) / sum(weights)
                    chosen = np.random.choice(candidates, p=probs)
                    self.G.add_edge(u, chosen, trust=INITIAL_TRUST)
                    
        return True


# ─────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────

def run():
    rng = np.random.default_rng(SEED)
    economy = EconomyGraph(NUM_AGENTS, rng)
    pos = nx.get_node_attributes(economy.G, 'pos')
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")
    
    # Custom colormap for wealth (blue to gold)
    wealth_cmap = LinearSegmentedColormap.from_list("wealth", [
        (0.0, "#1e3a8a"),  # dark blue (poor)
        (0.5, "#3b82f6"),  # light blue (average)
        (0.8, "#fbbf24"),  # amber (wealthy)
        (1.0, "#fef3c7"),  # white-gold (very wealthy)
    ])

    title = ax.set_title(
        f"Economic Trust Network  |  Step 0",
        fontsize=12, color="#e5e7eb"
    )
    fig.tight_layout()

    # Pre-calculate positions using spring layout seeded by geographic layout
    pos = nx.spring_layout(economy.G, pos=pos, iterations=50)

    exit_flag = {"stop": False}
    def on_key(event):
        if event.key in ("escape", "esc"):
            exit_flag["stop"] = True
    fig.canvas.mpl_connect("key_press_event", on_key)

    for step in range(1, MAX_STEPS + 1):
        if exit_flag["stop"]:
            print("\nSimulation ended (ESC).")
            break

        economy.step()

        if step % DISPLAY_EVERY == 0:
            ax.clear()
            
            # Recalculate layout gently
            pos = nx.spring_layout(economy.G, pos=pos, iterations=2, k=0.15)
            
            alive_nodes = [n for n in economy.G.nodes() if economy.agents[n].alive]
            dead_nodes = [n for n in economy.G.nodes() if not economy.agents[n].alive]
            
            # Draw edges
            if alive_nodes:
                edges = economy.G.edges()
                # Edge color based on trust
                edge_colors = []
                for u, v in edges:
                    trust = economy.G[u][v]['trust']
                    if trust > 0.6:
                        edge_colors.append((0.2, 0.8, 0.2, 0.6)) # Green - high trust
                    elif trust < 0.3:
                        edge_colors.append((0.8, 0.2, 0.2, 0.4)) # Red - low trust
                    else:
                        edge_colors.append((0.5, 0.5, 0.5, 0.2)) # Gray - neutral
                        
                nx.draw_networkx_edges(economy.G, pos, ax=ax, alpha=0.5, edge_color=edge_colors)

            # Draw dead nodes
            if dead_nodes:
                nx.draw_networkx_nodes(economy.G, pos, nodelist=dead_nodes, ax=ax, 
                                      node_color="#374151", node_size=20, alpha=0.3)

            # Draw alive nodes
            if alive_nodes:
                energies = np.array([economy.agents[n].energy for n in alive_nodes])
                reputations = np.array([economy.agents[n].global_reputation for n in alive_nodes])
                
                # Size = Reputation/Trust (trusted hubs get bigger)
                sizes = 30 + reputations * 150
                
                # Color = Wealth/Energy
                normalized_energies = np.clip(energies / (INITIAL_ENERGY * 1.5), 0, 1)
                
                # Plot specialized resource marker
                for n, s, c in zip(alive_nodes, sizes, normalized_energies):
                    a = economy.agents[n]
                    # Marker indicates the primary resource they produce
                    primary = np.argmax(a.skills)
                    marker = ['^', 'o', 's'][primary] 
                    ax.scatter(pos[n][0], pos[n][1], s=s, color=wealth_cmap(c), 
                               marker=marker, edgecolors='#cbd5e1', linewidths=0.5, zorder=5)

            total_energy = sum([a.energy for a in economy.agents.values()])
            total_trust = sum([economy.G[u][v]['trust'] for u,v in economy.G.edges()]) / max(1, len(economy.G.edges()))
            alive_count = len(alive_nodes)
            
            ax.set_title(
                f"Economic Trust Network  |  Step {step}\n"
                f"Alive: {alive_count}/{NUM_AGENTS}  |  Avg Trust: {total_trust:.2f}  |  Total Wealth: {total_energy:.0f}",
                fontsize=11, color="#94a3b8"
            )
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_aspect('equal')
            ax.axis('off')

            fig.canvas.draw_idle()
            plt.pause(0.001)

            if alive_count == 0:
                print("All agents died.")
                break

    plt.ioff()
    plt.close(fig)

    print(f"\n─── Finished after {step} steps ───")
    # Quick post-analysis
    alive_agents = [a for a in economy.agents.values() if a.alive]
    if alive_agents:
        wealths = [a.energy for a in alive_agents]
        gini = 0.0
        if sum(wealths) > 0: # Simple Gini index approximation
            diff_sum = sum(abs(x - y) for x in wealths for y in wealths)
            gini = diff_sum / (2 * len(wealths) * sum(wealths))
        print(f"Survivors: {len(alive_agents)}")
        print(f"Wealth Inequality (Gini): {gini:.3f}")

if __name__ == "__main__":
    run()
