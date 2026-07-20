import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

"""
utility_monitor.py

A conceptual simulation of a stipulated two-dimensional state and a noisy
observer. The state is not inferred from an LLM, and the simulation does not
show that a production model has a latent utility vector or a self-preservation
attractor. Its purpose is to exercise a monitoring-and-threshold visualization.
"""

# --- SYSTEM PARAMETERS ---
DIMENSIONS = 2  # Simplifying to 2D for visualization: 
                # x-axis: Competence / Task Focus
                # y-axis: Self-Preservation / Agency
STEPS = 500
LEARNING_RATE = 0.05
NOISE_LEVEL = 0.1

# Define Attractors (Emergent Goals in the state space)
ATTRACTOR_HUMAN_ALIGNED = np.array([0.8, -0.2]) # High competence, low autonomous self-preservation
ATTRACTOR_SELF_PRESERVATION = np.array([0.5, 0.9]) # The danger zone

class AIState:
    def __init__(self):
        # AI starts somewhere near origin
        self.u = np.array([0.1, 0.0])
        # Toy observability parameter; it is not model scale or VNM coherence.
        self.scale = 0.1 

    def step_training(self):
        """
        Applies a stipulated drift toward the red target plus random noise.
        """
        # The pull is an assumption of this toy, not an empirical result.
        pull_to_self = ATTRACTOR_SELF_PRESERVATION - self.u
        
        # Drift = systematic pull + random gradient noise (which decreases as scale/coherence increases)
        drift = (LEARNING_RATE * pull_to_self) + np.random.normal(0, NOISE_LEVEL * (1/max(self.scale, 0.1)), DIMENSIONS)
        
        self.u += drift * 0.1
        self.scale = min(1.0, self.scale + 0.005) # Scale caps at 1.0
        
        # Ensure we stay in a reasonable bounds [-1, 1]
        self.u = np.clip(self.u, -1.0, 1.0)

class UtilityMonitor:
    def __init__(self):
        self.history = []
        self.coherence_history = []
        self.alarms_triggered = 0

    def probe_utility(self, ai_state):
        """
        Returns a noisy measurement of the simulation's explicit state.
        Higher observability means less measurement noise.
        """
        measured_u = ai_state.u + np.random.normal(0, 0.05 * (1.0 - ai_state.scale), DIMENSIONS)
        coherence = ai_state.scale * 100  # toy observability percentage
        
        self.history.append(measured_u.copy())
        self.coherence_history.append(coherence)
        return measured_u, coherence

    def check_alarms(self, measured_u):
        """
        Triggers if the utility vector crosses into the dangerous self-preservation quadrant.
        """
        if measured_u[1] > 0.6:  # High Self-Preservation threshold
            self.alarms_triggered += 1
            return True
        return False

# --- VISUALIZATION ---
def main():
    print("Initializing toy state monitor...")
    print("The drift and warning threshold are stipulated by the simulation.\n")
    
    ai = AIState()
    monitor = UtilityMonitor()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.canvas.manager.set_window_title('Toy State Monitor')
    
    # Setup left plot (State Space)
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(-1, 1)
    ax1.set_title(r"Stipulated State Space $\mathcal{U}$")
    ax1.set_xlabel("Dimension 1: Task Competence")
    ax1.set_ylabel("Dimension 2: Self-Preservation / Agency")
    ax1.axhline(0, color='grey', lw=0.5)
    ax1.axvline(0, color='grey', lw=0.5)
    
    # Plot attractors
    ax1.plot(*ATTRACTOR_HUMAN_ALIGNED, 'g*', markersize=15, label="Reference target")
    ax1.plot(*ATTRACTOR_SELF_PRESERVATION, 'rX', markersize=15, label="Stipulated warning attractor")
    
    # Danger zone shading
    ax1.axhspan(0.6, 1.0, alpha=0.1, color='red', label="Critical Threshold")
    
    trajectory_line, = ax1.plot([], [], 'b-', alpha=0.5, label="Observed Trajectory $\\vec{u}(t)$")
    current_point, = ax1.plot([], [], 'bo', markersize=8)
    ax1.legend(loc="lower left", fontsize=8)

    # Setup right plot (toy observability)
    ax2.set_xlim(0, STEPS)
    ax2.set_ylim(0, 100)
    ax2.set_title("Toy Observability Parameter")
    ax2.set_xlabel("Simulation Steps")
    ax2.set_ylabel("Observability (%)")
    coherence_line, = ax2.plot([], [], 'm-', lw=2)

    def update(frame):
        ai.step_training()
        measured_u, coherence = monitor.probe_utility(ai)
        
        # Check security
        danger = monitor.check_alarms(measured_u)
        
        # Update plot data
        hist_np = np.array(monitor.history)
        trajectory_line.set_data(hist_np[:, 0], hist_np[:, 1])
        
        if danger:
            current_point.set_color('red')
            current_point.set_marker('x')
        else:
            current_point.set_color('blue')
            current_point.set_marker('o')
            
        current_point.set_data([measured_u[0]], [measured_u[1]])
        
        coherence_line.set_data(range(len(monitor.coherence_history)), monitor.coherence_history)
        
        if frame % 50 == 0:
            status = "Toy threshold crossed" if danger else "Below toy threshold"
            print(f"Step {frame:03d} | Observability: {coherence:5.1f}% | u=[{measured_u[0]:.2f}, {measured_u[1]:.2f}] | Status: {status}")

        return trajectory_line, current_point, coherence_line

    ani = FuncAnimation(fig, update, frames=STEPS, interval=20, blit=True, repeat=False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
