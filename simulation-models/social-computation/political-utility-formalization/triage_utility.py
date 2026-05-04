import numpy as np
import matplotlib.pyplot as plt

"""
triage_utility.py

The State as an Optimizer: The Mathematics of Sacrifice.
Demonstrates the hidden utility function of a state during a resource crisis.

No state admits its exact weighting of human lives vs. economic growth.
But by observing the Pareto frontier of decisions under constrained resources,
we can mathematically derive the hidden parameters of the state's utility function.
"""

def state_utility(economy, lives_saved, alpha=0.5, beta=0.5):
    """
    The hidden utility function governing state actions.
    U(s) = alpha * log(Economy) + beta * log(Lives_Saved)
    """
    # Using log weighting to represent diminishing marginal returns
    # (The first 1% drop in GDP hurts less than the 10th 1% drop)
    return alpha * np.log(max(economy, 0.01)) + beta * np.log(max(lives_saved, 0.01))

def simulate_crisis():
    # A crisis restricts the total available "capacity" of the system.
    # Every action to save lives (e.g., lockdowns) costs economic output.
    # Resource constraint equation: Economy^2 + Lives_Saved^2 <= Crisis_Capacity^2
    crisis_capacity = 100 
    
    # Generate the Pareto frontier of all *possible* state actions
    # x-axis: Action severity (0 = do nothing, 100 = total shutdown)
    action_space = np.linspace(0, crisis_capacity, 500)
    
    lives_saved = action_space
    economy = np.sqrt(crisis_capacity**2 - lives_saved**2)
    
    # Define three different "Hidden Utility" archetypes for states
    states = [
        {"name": "The Mercantilist State", "alpha": 0.8, "beta": 0.2, "color": "orange", "marker": "s"},
        {"name": "The Balanced Democracy", "alpha": 0.5, "beta": 0.5, "color": "blue", "marker": "o"},
        {"name": "The Biopolitical State", "alpha": 0.2, "beta": 0.8, "color": "green", "marker": "^"}
    ]
    
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.canvas.manager.set_window_title('Political Utility Formalization')
    
    ax.set_title("The Triage Problem: Mathematical Optimization of the State", fontsize=14)
    ax.set_xlabel("Vulnerable Lives Saved (%)", fontsize=12)
    ax.set_ylabel("Economic Output Retained (%)", fontsize=12)
    
    # Plot the constraint boundary (what is physically possible)
    ax.plot(lives_saved, economy, 'k--', linewidth=2, label="Crisis Impact Pareto Frontier (Constraint)")
    ax.fill_between(lives_saved, 0, economy, color='grey', alpha=0.1, label="Possibility Space")
    
    # Find the maximum utility point for each state archetype
    for state in states:
        utilities = state_utility(economy, lives_saved, state["alpha"], state["beta"])
        best_decision_index = np.argmax(utilities)
        
        opt_lives = lives_saved[best_decision_index]
        opt_econ = economy[best_decision_index]
        
        # Draw the indifference curve (contour map) for the winning utility value
        max_u = np.max(utilities)
        # We want to plot: alpha*log(E) + beta*log(L) = max_u
        # E = exp((max_u - beta*log(L)) / alpha)
        # Avoid dividing by zero or log(0)
        l_vals = np.linspace(1, 100, 200)
        e_vals = np.exp((max_u - state['beta'] * np.log(l_vals)) / state['alpha'])
        
        ax.plot(l_vals, e_vals, color=state['color'], linestyle=':', alpha=0.6)
        
        # Plot the actual decision point
        label = f"{state['name']} (Econ: {state['alpha']}, Lives: {state['beta']})"
        ax.plot(opt_lives, opt_econ, marker=state['marker'], color=state['color'], 
                markersize=12, label=label)
        
        # Add a text annotation
        ax.annotate(f"{opt_lives:.1f}%, {opt_econ:.1f}%", 
                    (opt_lives, opt_econ), 
                    textcoords="offset points", 
                    xytext=(10,10), 
                    ha='left',
                    color=state['color'],
                    fontweight='bold')

    # Formatting
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower left", fontsize=10)
    
    # Explanation text box
    textstr = '\n'.join((
        r'The mathematical formalization of the "Taboo Calculus".',
        r'During a crisis, the State optimizes its utility function $U(s)$',
        r'subject to resource constraints. The realized policy exactly',
        r'reveals the State\'s true hidden weighting of lives vs economy.'
    ))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Running Triage Utility Simulation...")
    print("Computing Pareto frontiers for state-level optimization...")
    simulate_crisis()
