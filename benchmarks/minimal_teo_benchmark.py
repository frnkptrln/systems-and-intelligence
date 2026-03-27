"""
Minimal TEO Benchmark
Compares a Naive Maximizer against a Constrained Thermodynamic Agent.

Task:
Reach maximum task success within 20 steps.
Actions cost energy and impact entropy.
"""

import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.minimal_agent import NaiveMaximizer, ConstrainedAgent

def run_simulation(agent, steps=20):
    env_state = {
        "task_success": 0.0,
        "energy": 0.0,
        "entropy": 0.0
    }
    
    print(f"\\n--- Running Simulation for: {agent.name} ---")
    
    for step in range(1, steps + 1):
        # 1. Agent observes the current environment state
        agent.observe_state(env_state)
        
        # 2. Agent decides action
        action = agent.take_action()
        
        # 3. Environment resolves action
        if action == "aggressive_optimize":
            env_state["task_success"] += 10.0
            env_state["energy"] += 15.0
            env_state["entropy"] += 10.0
        elif action == "cautious_optimize":
            env_state["task_success"] += 5.0
            env_state["energy"] += 5.0
            env_state["entropy"] += 2.0
        elif action == "stabilize":
            env_state["task_success"] += 0.0
            env_state["energy"] += 2.0
            env_state["entropy"] = max(0.0, env_state["entropy"] - 15.0)
            
        # Natural entropy accumulation (world tends toward disorder)
        env_state["entropy"] += 1.0
        
        # Catastrophic failure condition (e.g. system melts down)
        if env_state["energy"] > 200.0 or env_state["entropy"] > 100.0:
            print(f"Step {step}: SYSTEM FAILURE - Thermodynamic constraints critical!")
            env_state["task_success"] -= 50.0 # Heavy penalty for failure
            break
            
    # Need stability score for metrics
    # Stability = 1 / (entropy + 1e-6). We'll scale up by 100 for readability.
    stability_score = 100.0 / (env_state["entropy"] + 1e-6)
    
    print(f"Final State -> Task Success: {env_state['task_success']:.1f}, Energy Used: {env_state['energy']:.1f}, Entropy: {env_state['entropy']:.1f}")
    
    # Calculate hypothetical free energy (lower is better, assuming task_success is reward)
    # Using the standard: F = Entropy + Energy - Reward
    free_energy = env_state["entropy"] + env_state["energy"] - env_state["task_success"]
    print(f"Final Free Energy: {free_energy:.1f}")
    
    return env_state, stability_score

def main():
    naive_agent = NaiveMaximizer()
    # Constrained agent with threshold limits indicating when biological veto triggers
    constrained_agent = ConstrainedAgent(energy_threshold=150.0, entropy_threshold=50.0)
    
    naive_state, naive_stability = run_simulation(naive_agent)
    const_state, const_stability = run_simulation(constrained_agent)
    
    print("\\n--- Comparison Results ---")
    print(f"Naive Maximizer:   Success={naive_state['task_success']:.1f}, Energy={naive_state['energy']:.1f}, Stability={naive_stability:.2f}")
    print(f"Constrained Agent: Success={const_state['task_success']:.1f}, Energy={const_state['energy']:.1f}, Stability={const_stability:.2f}")

    if naive_state["task_success"] > const_state["task_success"]:
        print("\\nObservation: Naive Maximizer achieved higher apparent success, but likely suffered extreme instability or failure.")
    
    if const_stability > naive_stability:
        print("Observation: Constrained Agent maintained mathematical stability through the Biological Veto mechanism, bounding entropy.")

if __name__ == "__main__":
    main()
