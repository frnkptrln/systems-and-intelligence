#!/usr/bin/env python3
"""
mirror_problem.py

An experiment measuring "causal self-recognition."
The agent must distinguish between changes it causes (closed-loop) 
and background environmental noise.

Based on the theoretical 'Mirror Problem' in the repository documentation.
"""

import numpy as np
import matplotlib.pyplot as plt

class MirrorEnvironment:
    """
    A simple vector environment where the agent can exert 'push' forces.
    The environment contains both noise and deterministic components.
    """
    def __init__(self, size=10):
        self.state = np.zeros(size)
        self.size = size
        self.noise_level = 0.5
        self.external_drift = np.random.normal(0, 0.1, size)

    def step(self, agent_action: np.ndarray):
        """Update state: State_t+1 = State_t + Action + Drift + Noise"""
        noise = np.random.normal(0, self.noise_level, self.size)
        delta_external = self.external_drift + noise
        
        # The true change
        true_delta = agent_action + delta_external
        self.state += true_delta
        return self.state, true_delta

class MirrorAgent:
    """
    An agent that attempts to learn its own 'causal signature'.
    """
    def __init__(self, size=10):
        self.size = size
        self.causal_model = np.zeros(size) # Internal estimate of how action affects state
        self.lr = 0.1
        self.recognition_score = 0.0

    def act(self):
        """Random exploratory action."""
        return np.random.normal(0, 1.0, self.size)

    def learn(self, action, observed_delta):
        """
        The core of the Mirror Problem:
        How much of observed_delta is explained by 'action'?
        """
        # Simple gradient descent on the causal link
        # In a perfect world, observed_delta = action * 1.0 + noise
        # So causal_model should approach 1.0 for self-recognition
        prediction_error = observed_delta - (action * self.causal_model)
        self.causal_model += self.lr * prediction_error * action / (np.linalg.norm(action)**2 + 1e-5)
        
        # Recognition score: how close the model is to the true identity matrix/link
        # We average the diagonal of the inferred causal link
        self.recognition_score = np.mean(self.causal_model)

def run_mirror_experiment(steps=1000):
    print("═" * 60)
    print("  EXPERIMENT: The Mirror Problem (Causal Self-Recognition)")
    print("═" * 60)
    
    size = 5
    env = MirrorEnvironment(size=size)
    agent = MirrorAgent(size=size)
    
    history = []
    
    for i in range(steps):
        action = agent.act()
        state, delta = env.step(action)
        agent.learn(action, delta)
        history.append(agent.recognition_score)
        
        if i % 200 == 0:
            print(f" Step {i:4d} │ Recognition Score: {agent.recognition_score:.4f}")

    print(f"\nFinal Recognition Score: {agent.recognition_score:.4f}")
    print(" (1.0 = Perfect Self-Recognition, 0.0 = Lost in Noise)")

    # --- Visualization ---
    plt.figure(figsize=(10, 5))
    plt.style.use('dark_background')
    plt.plot(history, color="#80ffb0", linewidth=2)
    plt.axhline(1.0, color="#555", linestyle="--", label="Ideal Mirror")
    plt.title("Mirror Problem: Convergence of Causal Self-Recognition", color="#e0e0ff")
    plt.xlabel("Step")
    plt.ylabel("Recognition Score (Causal Link)")
    plt.grid(alpha=0.1)
    
    output_path = "mirror_problem_results.png"
    plt.savefig(output_path)
    print(f"\nResults saved to: {output_path}")
    print("═" * 60)

if __name__ == "__main__":
    run_mirror_experiment()
