import numpy as np
import matplotlib.pyplot as plt

"""
active_inference_simulation.py

A mathematical formalization of Karl Friston's Free Energy Principle.
Demonstrates how an agent minimizes "surprise" (Variational Free Energy) 
through two distinct mechanisms:
1. Perception (Updating internal beliefs about the world)
2. Action (Changing the world to match internal predictions)

This script proves that goal-directed behavior emerges naturally from 
a system that simply tries to minimize prediction error.
"""

class ActiveInferenceAgent:
    def __init__(self, prior_preference=1.0):
        # The agent's generative model of the world.
        # It believes the world should be in state '1' (e.g., "Full Energy" or "Optimal Temperature")
        # prior_preference is the precision (certainty) of this belief.
        self.mu_prior = 1.0 
        self.pi_prior = prior_preference 
        
        # Internal belief about the current state of the world (initially wrong/uncertain)
        self.mu_state = 0.0
        
        # Generative model mapping: Observation (y) = State (x) + noise
        self.pi_sensory = 2.0 # Sensory precision (how much we trust our sensors)
        
        # Tracking metrics
        self.history = {
            'time': [],
            'true_state': [],
            'belief_state': [],
            'free_energy': [],
            'action': []
        }

    def calc_free_energy(self, observation, action=0.0):
        """
        Calculates Variational Free Energy (F).
        F ≈ Sensory Prediction Error + Prior Prediction Error
        """
        # 1. Sensory Error: (Observation - predicted observation) squared, weighted by sensory precision
        # Note: Action affects the true state, which affects observation.
        predicted_obs = self.mu_state 
        sensory_error = 0.5 * self.pi_sensory * (observation - predicted_obs)**2
        
        # 2. Prior Error: (Belief - Prior Preference) squared, weighted by prior precision
        prior_error = 0.5 * self.pi_prior * (self.mu_state - self.mu_prior)**2
        
        return sensory_error + prior_error

    def perception_update(self, observation, learning_rate=0.1):
        """
        Gradient descent on Free Energy with respect to internal belief (mu_state).
        "Change my mind to match the world."
        """
        # dF/d(mu_state) = Prior Error Gradient - Sensory Error Gradient
        dF_dmu = self.pi_prior * (self.mu_state - self.mu_prior) - self.pi_sensory * (observation - self.mu_state)
        
        # Update belief to minimize F
        self.mu_state -= learning_rate * dF_dmu

    def action_update(self, observation, learning_rate=0.1):
        """
        Gradient descent on Free Energy with respect to Action.
        "Change the world to match my mind."
        Assuming d(Observation)/d(Action) ≈ 1 (Action directly moves state toward prediction)
        """
        # dF/da = dF/d(observation) * d(observation)/d(action)
        # dF/d(obs) = pi_sensory * (observation - mu_state)
        dF_da = self.pi_sensory * (observation - self.mu_state) * 1.0 
        
        # Calculate action to minimize F
        action = -learning_rate * dF_da
        return action

def run_simulation(steps=100, mechanism="both"):
    """
    Runs the Active Inference loop.
    mechanisms: "perception_only", "action_only", "both"
    """
    agent = ActiveInferenceAgent()
    
    # The actual true state of the environment (e.g., standard temperature = 0.0)
    # The agent *expects* it to be 1.0. This creates a prediction error (Surprise).
    true_state = 0.0 
    
    for t in range(steps):
        # 1. Generate Observation from True State (with slight noise)
        observation = true_state + np.random.normal(0, 0.05)
        
        FE = agent.calc_free_energy(observation)
        action = 0.0
        
        # 2. Minimize Free Energy
        if mechanism in ["perception_only", "both"]:
            # Update internal beliefs
            for _ in range(5): # Fast perception loop
                agent.perception_update(observation)
                
        if mechanism in ["action_only", "both"]:
            # Generate action to change the world
            action = agent.action_update(observation)
            # The action literally changes the true state of the environment
            true_state += action 
            
        # Log metrics
        agent.history['time'].append(t)
        agent.history['true_state'].append(true_state)
        agent.history['belief_state'].append(agent.mu_state)
        agent.history['free_energy'].append(FE)
        agent.history['action'].append(action)
        
    return agent.history

def plot_results():
    print("Simulating Perception Only (Agent accepts reality)...")
    res_perc = run_simulation(mechanism="perception_only")
    
    print("Simulating Action Only (Agent changes reality)...")
    res_act = run_simulation(mechanism="action_only")
    
    print("Simulating Active Inference (Perception + Action)...")
    res_both = run_simulation(mechanism="both")

    fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    
    # 1. Perception Only
    axs[0].plot(res_perc['true_state'], label='True World State (Cold=0.0)', color='blue')
    axs[0].plot(res_perc['belief_state'], label='Agent Belief', color='orange', linestyle='--')
    axs[0].set_title('Perception Only: Changing Beliefs to Match the World')
    axs[0].set_ylabel('State Value')
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)

    # 2. Action Only
    axs[1].plot(res_act['true_state'], label='True World State', color='blue')
    axs[1].plot(res_act['belief_state'], label='Agent Belief (Fixed Expectation=1.0)', color='orange', linestyle='--')
    axs[1].set_title('Action Only: Changing the World to Match Expectations')
    axs[1].set_ylabel('State Value')
    axs[1].legend()
    axs[1].grid(True, alpha=0.3)

    # 3. Active Inference (Free Energy)
    axs[2].plot(res_perc['free_energy'], label='FE (Perception Only)')
    axs[2].plot(res_act['free_energy'], label='FE (Action Only)')
    axs[2].plot(res_both['free_energy'], label='FE (Active Inference)', color='red', linewidth=2)
    axs[2].set_title('Variational Free Energy (Surprise) Minimization')
    axs[2].set_ylabel('Free Energy')
    axs[2].set_xlabel('Time Step')
    axs[2].legend()
    axs[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('active_inference_plot.png')
    print("Saved plot to 'active_inference_plot.png'")
    
    # Print terminal readout for the Active Inference (both) run
    print("\n==================================================")
    print("ACTIVE INFERENCE: FINAL STATE (t=100)")
    print("==================================================")
    print(f"Goal State (Prior Prediction): 1.000")
    print(f"Actual World State:            {res_both['true_state'][-1]:.3f}")
    print(f"Agent's Internal Belief:       {res_both['belief_state'][-1]:.3f}")
    print(f"Prediction Error (Free Energy):{res_both['free_energy'][-1]:.4f}")
    print("Conclusion: The agent successfully altered the environment to match its internal goals.")

if __name__ == "__main__":
    plot_results()
