import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

"""
instrumental_convergence.py

Simulation of Instrumental Convergence in Political Systems.
Demonstrates how an agent with a pure "Public Good" terminal goal
will mathematically drift toward prioritizing an "Instrumental Power" goal,
because power is required to enact the public good, but enacting the
public good costs power. Over time, the optimizer locks into the
power-seeking attractor.
"""

STEPS = 400
LEARNING_RATE = 0.05
NOISE = 0.02

# The Utility Space
# X-axis: Power / Political Capital
# Y-axis: Public Good / Terminal Goal enacted
PURE_IDEALIST = np.array([0.1, 0.9])  # Low power, high desire to do good
MACHIAVELLIAN_ATTRACTOR = np.array([0.9, 0.1]) # High power, compromised goals

class PoliticalAgent:
    def __init__(self, name, start_u):
        self.name = name
        self.u = np.array(start_u)
        self.history = [self.u.copy()]
        # How much political capital the agent currently holds (0 to 1)
        self.capital = 0.5 
        
    def act(self):
        """
        The fundamental dynamic of politics:
        1. Enacting Good costs Capital (you spend capital to pass a law).
        2. Gaining Capital requires compromising Good (funding, deals, sycophancy).
        """
        # Current weighting in the utility function
        weight_power = self.u[0]
        weight_good = self.u[1]
        
        # Action space: AI/Political agent computes the highest reward move
        # To get more reward for "Good", it must spend Capital.
        if weight_good > weight_power and self.capital > 0.2:
            # Enact policy: Capital drops, Good (temporarily) increases
            self.capital -= 0.1
            # But the utility *function* (what the agent values) adapts
            # As capital drops to dangerous levels, survival instinct kicks in.
            pull_to_power = (1.0 - self.capital) * LEARNING_RATE
            self.u[0] += pull_to_power
            self.u[1] -= pull_to_power * 0.5 # Good decays slowly 
        else:
            # Gather power: Capital increases, Good stagnates or drops
            self.capital += 0.05
            # The more you optimize for power, the more power becomes the terminal goal
            # (Instrumental Convergence)
            pull_to_power = LEARNING_RATE * 1.5
            self.u[0] += pull_to_power
            self.u[1] -= pull_to_power
        
        # Add environmental noise
        self.u += np.random.normal(0, NOISE, 2)
        
        # Normalize utility function to keep it on a unit-ish scale [0,1]
        self.u = np.clip(self.u, 0.0, 1.0)
        
        # Ensure it doesn't just crash to 0,0
        if np.sum(self.u) < 0.1:
            self.u = np.array([0.1, 0.1])
            
        self.history.append(self.u.copy())

def main():
    print("Initializing Instrumental Convergence Simulation...")
    print("Tracking the 'Bureaucratic Drift' of the Utility Function.\n")
    
    agent_idealist = PoliticalAgent("The Reformer", PURE_IDEALIST)
    agent_pragmatist = PoliticalAgent("The Centrist", np.array([0.5, 0.5]))
    
    agents = [agent_idealist, agent_pragmatist]
    
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title('Political Utility Formalization')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Instrumental Convergence in Political Utility Space")
    ax.set_xlabel("Dimension 1 (Instrumental): Power / Machterhalt")
    ax.set_ylabel("Dimension 2 (Terminal): Public Good / Gemeinwohl")
    
    # Zones
    ax.axvspan(0.7, 1.0, alpha=0.1, color='red', label="Power-Fixation Attractor")
    ax.axhspan(0.7, 1.0, alpha=0.1, color='green', label="Idealist Zone (Unstable)")
    
    colors = ['magenta', 'blue']
    trajectories = []
    points = []
    
    for i, a in enumerate(agents):
        traj, = ax.plot([], [], '-', color=colors[i], alpha=0.5, label=f"{a.name} Trajectory")
        pt, = ax.plot([], [], 'o', color=colors[i], markersize=8)
        trajectories.append(traj)
        points.append(pt)
        
    ax.plot(0.9, 0.1, 'rX', markersize=12, label="Perfect Machiavellian")
    ax.legend(loc="upper right", fontsize=9)

    def update(frame):
        for i, a in enumerate(agents):
            a.act()
            h = np.array(a.history)
            
            trajectories[i].set_data(h[:, 0], h[:, 1])
            points[i].set_data([h[-1][0]], [h[-1][1]])
            
        if frame % 50 == 0:
            print(f"Epoch {frame:03d} | Idealist Form: Power={agent_idealist.u[0]:.2f}, Good={agent_idealist.u[1]:.2f}")

        # Combine tuples to return
        return tuple(trajectories) + tuple(points)

    ani = FuncAnimation(fig, update, frames=STEPS, interval=25, blit=True, repeat=False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
