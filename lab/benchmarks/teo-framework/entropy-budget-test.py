import numpy as np
import matplotlib.pyplot as plt

# Parameters
time_steps = 100
N = 50  # number of strategies
D_max = 10  # maximum entropy budget

# Function to simulate replicator dynamics

def replicator_dynamics(constrained=True):
    # Initialize resource distribution and fitness
    resources = np.random.rand(N)
    fitness = np.random.rand(N)

    # Store resources over time
    resource_history = np.zeros((time_steps, N))

    for t in range(time_steps):
        # Update fitness based on current resources
        fitness = resources / np.sum(resources)

        # Apply entropy budget constraint if required
        if constrained:
            resources = np.clip(resources, 0, D_max)
        else:
            resources += np.random.normal(0, 1, N)  # Random fluctuations

        # Normalize resources to maintain proportion
        resources = resources / np.sum(resources)
        resource_history[t] = resources

    return resource_history

# Function to plot results

def plot_results(history_constrained, history_unconstrained):
    plt.figure(figsize=(12, 6))
    for i in range(N):
        plt.plot(history_constrained[:, i], label=f'Constrained Strategy {i}', alpha=0.3)
        plt.plot(history_unconstrained[:, i], label=f'Unconstrained Strategy {i}', alpha=0.3, linestyle='--')

    plt.title('Resource Distribution: Constrained vs Unconstrained Replicator Dynamics')
    plt.xlabel('Time Steps')
    plt.ylabel('Resource Proportion')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()

# Run simulations
history_constrained = replicator_dynamics(constrained=True)
history_unconstrained = replicator_dynamics(constrained=False)

# Plot the results
plot_results(history_constrained, history_unconstrained)
