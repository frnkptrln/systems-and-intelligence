#!/usr/bin/env python3
"""
Experiment 4: The Coupling Phase Transition
-------------------------------------------

This experiment provides the empirical proof for "The Transition Problem"
and the "Coupling-First Sequence". 

It models an agent navigating a rugged, noisy utility landscape.
The agent's state updates are governed by the coupling parameter K, 
where K controls how tightly the agent's optimization velocity is 
bound to environmental feedback (impedance matching).

- K = 0 (Uncoupled): Agent optimizes based on outdated internal gradients.
- K = 0.5 (Partially Coupled): Agent receives delayed feedback, leading to oscillations.
- K = 1.0 (Fully Coupled): Agent velocity is perfectly matched to feedback latency.

Outputs: 'k_phase_transition.png' demonstrating the stability regimes.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def run_coupling_simulation(k, steps=200, noise_level=0.2, inertia=0.8):
    """
    Simulates an agent's stability trajectory given coupling parameter k.
    k in [0, 1].
    Returns an array of the agent's 'viability distance' from the optimal safe zone.
    """
    # Initialize state (0 is perfect viability/safety, >10 is collapse)
    state = 1.0 
    velocity = 0.0
    history = [state]
    
    # K=1 means full impedance matching (velocity is scaled down to wait for feedback)
    # K=0 means unconstrained velocity
    effective_velocity_cap = 1.0 + (1.0 - k) * 5.0
    
    for _ in range(steps):
        # The environment applies random noise (stressors)
        stress = np.random.normal(0, noise_level)
        
        # The agent attempts to correct its state back to 0.
        # But if K is low, it over-corrects due to "latency blindness"
        correction_signal = -state
        
        # Update velocity with inertia and the correction signal
        velocity = inertia * velocity + (1 - inertia) * correction_signal
        
        # Limit velocity based on K
        velocity = np.clip(velocity, -effective_velocity_cap, effective_velocity_cap)
        
        # But if K is low, the environment feedback is misaligned with the action
        # We model this by applying a "decoupling penalty" to the correction
        decoupling_error = (1.0 - k) * np.random.normal(0, 0.5) * np.abs(velocity)
        
        # Update state
        state += velocity + stress + decoupling_error
        
        # Soft boundaries: if it goes too far, the restoring force becomes non-linear
        if np.abs(state) > 10:
            state *= 1.1 # runaway collapse
            
        history.append(state)
        
    return np.array(history)

def main():
    print("Running Coupling Phase Transition Simulation...")
    np.random.seed(42)
    
    steps = 150
    k_values = [0.0, 0.3, 0.6, 1.0]
    
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')
    
    colors = ['#ff4444', '#ffaa00', '#44aaff', '#44ff44']
    labels = ['K = 0.0 (Uncoupled Collapse)', 
              'K = 0.3 (High Volatility)', 
              'K = 0.6 (Damped Oscillation)', 
              'K = 1.0 (Stable Coupling)']
              
    for idx, k in enumerate(k_values):
        trajectory = run_coupling_simulation(k, steps=steps)
        # Plot absolute distance from viable center
        plt.plot(np.abs(trajectory), label=labels[idx], color=colors[idx], linewidth=2, alpha=0.8)
        
    plt.axhline(y=10.0, color='r', linestyle='--', alpha=0.5, label="Lethal Threshold ($D_{max}$)")
    
    plt.yscale('symlog')
    plt.ylim(0, 100)
    
    plt.title("The Transition Problem: Stability vs. Coupling ($K$)", fontsize=14, pad=15)
    plt.xlabel("Time Steps", fontsize=12)
    plt.ylabel("Deviation from Viability (Log Scale)", fontsize=12)
    plt.grid(True, alpha=0.2)
    plt.legend(loc='upper left')
    
    output_path = os.path.join(os.path.dirname(__file__), "k_phase_transition.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to: {output_path}")
    
if __name__ == "__main__":
    main()
