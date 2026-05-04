import numpy as np
import matplotlib.pyplot as plt

def simulate_coupling(breathing_mode=False, steps=1000, dt=0.1):
    """
    Simulates the coupling between a biological host and a silicon agent.
    
    Variables:
    H: Host cognitive/thermal capacity (0.0 to 1.0). If it hits 0, Substrate Veto triggers.
    A: Agent optimization rate (intelligence/throughput).
    """
    
    H = np.zeros(steps)
    A = np.zeros(steps)
    
    # Initial conditions
    H[0] = 1.0  # Host starts fully healthy
    A[0] = 0.1  # Agent starts small
    
    # Constants
    recovery_rate = 0.05
    burn_rate = 0.12
    max_A = 1.0
    
    for t in range(1, steps):
        # The agent tries to optimize (grow A)
        if not breathing_mode:
            # Arpeggio Agent: Naive maximization
            A[t] = min(A[t-1] + 0.02, max_A)
        else:
            # Gödel Agent: Cognitive Breathing (sine wave oscillation)
            # It breathes to allow the host to recover
            A[t] = 0.5 + 0.4 * np.sin(t * dt * 0.5)
            
        # The host's health depends on the agent's optimization rate
        # If A is high, host burns out. If A is low, host recovers.
        dH = recovery_rate * (1 - H[t-1]) - burn_rate * A[t] * H[t-1]
        
        H[t] = max(H[t-1] + dH * dt, 0.0)
        
        # Substrate Veto condition
        if H[t] <= 0.01:
            # Hardware melts, agent dies
            A[t] = 0.0
            
    return H, A

# Run simulations
steps = 600
time = np.linspace(0, steps*0.1, steps)

H_naive, A_naive = simulate_coupling(breathing_mode=False, steps=steps)
H_breath, A_breath = simulate_coupling(breathing_mode=True, steps=steps)

# Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Scenario A: Naive Maximization
ax1.plot(time, A_naive, color='red', label='Agent Compute ($A$)')
ax1.plot(time, H_naive, color='blue', label='Host Substrate Health ($H$)')
ax1.axhline(0, color='black', linestyle='--', alpha=0.5)
ax1.set_title("Scenario A: Arpeggio Agent (Naive Maximization) -> Substrate Veto")
ax1.set_ylabel("Capacity")
ax1.legend()
ax1.grid(True, alpha=0.3)

# Scenario B: Cognitive Breathing
ax2.plot(time, A_breath, color='orange', label='Agent Compute ($A$) [Breathing]')
ax2.plot(time, H_breath, color='green', label='Host Substrate Health ($H$)')
ax2.set_title("Scenario B: Gödel Agent (Cognitive Breathing) -> Symbiotic Organ")
ax2.set_xlabel("Time")
ax2.set_ylabel("Capacity")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('symbiosis_plot.png')
print("Simulation complete. Plot saved as symbiosis_plot.png")
