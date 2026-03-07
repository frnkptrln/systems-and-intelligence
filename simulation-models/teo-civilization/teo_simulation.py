"""
teo_simulation.py

Thermodynamics of Emergent Orchestration (TEO) — Numerical Simulation

Solves the coupled ODE system:
  - Replicator Equation  (Market Paradigm)
  - Kuramoto Model       (Harmonic Paradigm)
  - Homeostatic Control   (Regulatory Paradigm)
  - Entropy Budget        (Biological Veto)

Demonstrates how civilizations / AI ecologies survive or collapse
depending on cultural coupling (K), regulatory strength (gamma),
and the physical entropy limit (D_max).
"""

import numpy as np
from scipy.integrate import solve_ivp
import json


# ─── Parameters ───────────────────────────────────────────────
N = 6              # Number of agents
K_COUPLING = 2.5   # Cultural coupling strength (Kuramoto)
GAMMA = 1.0        # Regulatory (homeostatic) strength
X_CRIT = 0.35      # Maximum permissible resource share per agent
D_MAX = 0.8        # Maximum entropy dissipation capacity of substrate
ETA = 0.3          # Entropy-per-unit-output coefficient
T_SPAN = (0, 50)   # Simulation time
T_EVAL = np.linspace(0, 50, 500)


def fitness(x, i):
    """Agent fitness — heterogeneous base rates plus interaction."""
    base_fitness = [1.2, 0.9, 1.0, 1.1, 0.8, 1.05]
    return base_fitness[i % len(base_fitness)]


def homeostatic_control(x_i):
    """Regulatory brake: pushes agents back below x_crit."""
    return -GAMMA * max(0, x_i - X_CRIT)


def entropy_production(x, f_vals):
    """Total entropy production of the system."""
    return ETA * np.sum(x * f_vals)


def teo_system(t, state):
    """
    The full TEO coupled ODE system.

    State vector: [x_0, ..., x_{N-1}, theta_0, ..., theta_{N-1}]
    """
    x = state[:N]
    theta = state[N:]

    # Ensure x stays non-negative
    x = np.maximum(x, 1e-10)
    x = x / np.sum(x)  # Normalize to simplex

    # --- Fitness values ---
    f_vals = np.array([fitness(x, i) for i in range(N)])
    phi_bar = np.sum(x * f_vals)  # Average fitness

    # --- Entropy check (Biological Veto) ---
    S_dot = entropy_production(x, f_vals)
    veto_active = S_dot > D_MAX
    veto_damping = 1.0 if not veto_active else max(0.0, D_MAX / (S_dot + 1e-10))

    # --- Replicator + Homeostatic (dx/dt) ---
    dx = np.zeros(N)
    for i in range(N):
        replicator = x[i] * (f_vals[i] - phi_bar)
        control = homeostatic_control(x[i])
        dx[i] = (replicator + control) * veto_damping

    # --- Kuramoto (dtheta/dt) ---
    # Full connectivity for simplicity (A_ij = 1 for all i != j)
    dtheta = np.zeros(N)
    for i in range(N):
        omega_i = 0.1 * (i - N / 2)  # Spread of natural frequencies
        coupling = (K_COUPLING / N) * np.sum(np.sin(theta - theta[i]))
        dtheta[i] = omega_i + coupling

    return np.concatenate([dx, dtheta])


def compute_order_parameter(theta):
    """Kuramoto order parameter r(t) — measures global synchronization."""
    return np.abs(np.mean(np.exp(1j * theta)))


def run_simulation(K=None, gamma=None, d_max=None):
    """Run the TEO simulation with optional parameter overrides."""
    global K_COUPLING, GAMMA, D_MAX
    if K is not None:
        K_COUPLING = K
    if gamma is not None:
        GAMMA = gamma
    if d_max is not None:
        D_MAX = d_max

    # Initial conditions
    x0 = np.ones(N) / N  # Equal resource distribution
    theta0 = np.random.uniform(0, 2 * np.pi, N)  # Random value orientations
    state0 = np.concatenate([x0, theta0])

    # Solve ODE
    sol = solve_ivp(teo_system, T_SPAN, state0, t_eval=T_EVAL,
                    method='RK45', max_step=0.1)

    # Compute derived quantities
    x_history = sol.y[:N, :]
    theta_history = sol.y[N:, :]
    order_param = np.array([compute_order_parameter(theta_history[:, t])
                            for t in range(len(sol.t))])

    entropy_history = np.array([
        entropy_production(x_history[:, t],
                           np.array([fitness(x_history[:, t], i) for i in range(N)]))
        for t in range(len(sol.t))
    ])

    return {
        't': sol.t,
        'x': x_history,
        'theta': theta_history,
        'order_parameter': order_param,
        'entropy': entropy_history,
        'D_max': D_MAX,
    }


def print_summary(result):
    """Print a human-readable summary of the simulation."""
    t = result['t']
    x = result['x']
    r = result['order_parameter']
    S = result['entropy']

    print("=" * 60)
    print("  Thermodynamics of Emergent Orchestration (TEO)")
    print("  Civilization Simulation Results")
    print("=" * 60)
    print(f"  Agents:                  {N}")
    print(f"  Cultural Coupling (K):   {K_COUPLING}")
    print(f"  Regulatory Strength (γ): {GAMMA}")
    print(f"  Entropy Limit (D_max):   {D_MAX}")
    print("-" * 60)

    # Final state
    x_final = x[:, -1]
    r_final = r[-1]
    S_final = S[-1]

    print(f"\n  Final Resource Distribution:")
    for i in range(N):
        bar = "█" * int(x_final[i] * 50)
        print(f"    Agent {i}: {x_final[i]:.3f}  {bar}")

    print(f"\n  Final Coherence (r):     {r_final:.3f}", end="")
    if r_final > 0.8:
        print("  ✓ Synchronized")
    elif r_final > 0.4:
        print("  ⚠ Partially coherent")
    else:
        print("  ✗ Chaotic / Polarized")

    print(f"  Final Entropy Rate:      {S_final:.3f} / {D_MAX}", end="")
    if S_final > D_MAX:
        print("  ✗ BIOLOGICAL VETO ACTIVE")
    else:
        print(f"  ✓ Within limits ({S_final/D_MAX*100:.0f}%)")

    # Gini coefficient of resource distribution
    x_sorted = np.sort(x_final)
    gini = (2 * np.sum((np.arange(1, N + 1) * x_sorted)) / (N * np.sum(x_sorted))) - (N + 1) / N
    print(f"  Gini Coefficient:        {gini:.3f}", end="")
    if gini > 0.4:
        print("  ⚠ High inequality")
    else:
        print("  ✓ Moderate inequality")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║     SCENARIO 1: Healthy Civilization                    ║")
    print("║     K=2.5, γ=1.0, D_max=0.8                            ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    result1 = run_simulation(K=2.5, gamma=1.0, d_max=0.8)
    print_summary(result1)

    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║     SCENARIO 2: No Regulation (γ=0)                     ║")
    print("║     Instrumental Convergence / Monopoly                  ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    result2 = run_simulation(K=2.5, gamma=0.0, d_max=0.8)
    print_summary(result2)

    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║     SCENARIO 3: Cultural Collapse (K=0.1)               ║")
    print("║     Filter Bubbles / Polarization                        ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    result3 = run_simulation(K=0.1, gamma=1.0, d_max=0.8)
    print_summary(result3)

    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║     SCENARIO 4: Entropy Limit Exceeded                   ║")
    print("║     Ecological Collapse / Biological Veto                 ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    result4 = run_simulation(K=2.5, gamma=1.0, d_max=0.15)
    print_summary(result4)
