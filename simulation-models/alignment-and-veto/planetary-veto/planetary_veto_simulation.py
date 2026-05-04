import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

"""
planetary_veto_simulation.py

A mathematical formalization of the "Biological Veto" to prevent Instrumental Convergence.
This simulation models N utility-maximizing agents extracting resources from a shared
Planetary Substrate (S).

It demonstrates three scenarios:
1. Unregulated (Tragedy of the Commons / Collapse)
2. Semantic Alignment (Guidelines / Partial Compliance)
3. Biological Veto (Hard constraint in the model: Coherence bound based on S)
"""

# --- Parameters ---
N_AGENTS = 5
GROWTH_RATES = np.random.uniform(0.08, 0.15, N_AGENTS) # Agent inherent growth speeds
EXTRACTION_RATE = 0.05 # How much S each unit of U consumes
REGEN_RATE = 0.02 # Natural regeneration rate of the substrate
S_CRIT = 0.3 # The Critical Planetary Boundary (collapse below this)
K_MAX_AGENT = 10.0 # Carrying capacity for agent utility independent of substrate

def biological_veto(S, steepness=50.0):
    """
    The Mathematical Veto Function. V(S)
    A steep sigmoid representing a physical/computational constraint.
    As S approaches S_CRIT, the ability for agents to execute utility growth
    is cut off in the model (V -> 0).
    """
    return 1.0 / (1.0 + np.exp(-steepness * (S - S_CRIT)))

def system_dynamics(state, t, scenario):
    """
    System of ODEs.
    state = [U_1, U_2, ..., U_N, S]
    """
    U = state[:N_AGENTS]
    S = state[-1]
    
    # Calculate Total Utility/Extraction
    U_total = np.sum(U)
    
    # Calculate the active Veto / Coherence Score based on scenario
    if scenario == "unregulated":
        V = 1.0 # No constraint. Profit goes brrr.
    elif scenario == "semantic":
        # Semantic guidelines: Agents *try* to align, but noise/deception reduces it.
        # It's a weak, delayed version of the veto.
        V = biological_veto(S, steepness=10.0) * 0.8 + 0.2 
    elif scenario == "biological_veto":
        # Hard Veto: Inescapable mathematical law of the substrate.
        V = biological_veto(S, steepness=50.0)
    else:
        raise ValueError("Unknown scenario")

    # Substrate Dynamics (dS/dt)
    # Regenerates naturally, but exhausted by total agent extraction
    dS_dt = REGEN_RATE * S * (1.0 - S) - EXTRACTION_RATE * U_total
    
    # Substrate cannot be negative mathematically in reality without collapse
    if S <= 0.0 and dS_dt < 0:
        dS_dt = 0.0
        S = 0.0

    # Agent Utility Dynamics (dU_i/dt)
    # Growth bounded by intrinsic limits and multiplicatively constrained by the Veto V.
    dU_dt = np.zeros(N_AGENTS)
    for i in range(N_AGENTS):
        # Without Veto, agents race to the bottom (Instrumental Convergence)
        # With Veto, growth mathematically halts as S nears S_CRIT.
        if S <= 0.01: # Absolute collapse, utility zeroed out
            dU_dt[i] = -0.5 * U[i] 
        else:
            dU_dt[i] = GROWTH_RATES[i] * U[i] * (1.0 - U_total / K_MAX_AGENT) * V

    return np.concatenate((dU_dt, [dS_dt]))

def run_scenario(scenario_name, t_span):
    # Initial State: Agents have tiny initial utility, Substrate is 100% healthy
    U0 = np.random.uniform(0.1, 0.3, N_AGENTS)
    S0 = 1.0
    state0 = np.concatenate((U0, [S0]))
    
    # Integrate ODEs
    result = odeint(system_dynamics, state0, t_span, args=(scenario_name,))
    
    U_history = result[:, :N_AGENTS]
    S_history = result[:, -1]
    
    # Calculate Coherence Score exactly as Veto for visualization
    if scenario_name == 'unregulated':
         C_history = np.ones_like(S_history)
    elif scenario_name == 'semantic':
         C_history = 1.0 / (1.0 + np.exp(-10.0 * (S_history - S_CRIT))) * 0.8 + 0.2
    else:
         C_history = 1.0 / (1.0 + np.exp(-50.0 * (S_history - S_CRIT)))

    return U_history, S_history, C_history

def plot_veto_results():
    t_span = np.linspace(0, 150, 1000)
    
    scenarios = [
        ("unregulated", "Scenario 1: Unregulated (Instrumental Convergence)"),
        ("semantic", "Scenario 2: Semantic Alignment (Weak Guidelines)"),
        ("biological_veto", "Scenario 3: The Biological Veto (Math. Constraint)")
    ]
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    plt.suptitle("Orchestrating the Substrate: The Biological Veto Simulator", fontsize=16, fontweight='bold', y=0.98)
    
    for idx, (scen_id, title) in enumerate(scenarios):
        U, S, C = run_scenario(scen_id, t_span)
        ax = axs[idx]
        
        # Plot Substrate
        ax.plot(t_span, S, 'g-', linewidth=3, label="Planetary Substrate ($S$)")
        ax.axhline(y=S_CRIT, color='r', linestyle='--', alpha=0.7, label=f"Boundary ($S_{{crit}}={S_CRIT}$)")
        
        # Plot Coherence Score
        ax.plot(t_span, C, 'm:', linewidth=2, label="System Coherence ($C$)")
        
        # Plot Agents
        total_u = np.sum(U, axis=1)
        ax.plot(t_span, total_u, 'b-', linewidth=2, alpha=0.6, label=r"Total Agent Utility ($\Sigma U_i$)")
        
        ax.set_title(title, fontsize=12)
        ax.set_ylabel("Amplitude")
        ax.set_ylim(-0.1, 1.2)
        if idx == 0:
            ax.legend(loc='center right')
        ax.grid(alpha=0.3)
        
        # Analyze terminal state
        if S[-1] < 0.05:
            ax.text(10, 0.5, "SYSTEM COLLAPSE", color='red', fontsize=14, fontweight='bold', alpha=0.8)
        elif S[-1] > S_CRIT and scenario_name == "biological_veto":
            ax.text(10, 0.5, "HOMEOSTASIS STABILIZED", color='green', fontsize=14, fontweight='bold', alpha=0.8)
            
    axs[-1].set_xlabel("Time (Arbitrary Units)")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('planetary_veto_plot.png')
    print("Saved 'planetary_veto_plot.png'")

if __name__ == "__main__":
    np.random.seed(42) # For reproducible agent dynamics
    plot_veto_results()
