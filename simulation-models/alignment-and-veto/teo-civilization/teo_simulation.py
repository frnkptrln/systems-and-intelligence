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


# ─── Default Parameters ──────────────────────────────────────
DEFAULT_PARAMS = {
    'N': 6,
    'K': 2.5,           # Cultural coupling strength (Kuramoto)
    'gamma': 1.0,        # Regulatory (homeostatic) strength
    'x_crit': 0.35,      # Max permissible resource share per agent
    'D_max': 0.8,        # Max entropy dissipation capacity
    'eta': 0.3,          # Entropy-per-unit-output coefficient
    'T_end': 50,         # Simulation duration
    'steps': 500,        # Number of output time steps
    'base_fitness': [1.2, 0.9, 1.0, 1.1, 0.8, 1.05],
}


def make_teo_system(params):
    """Create the TEO ODE right-hand side with given parameters."""
    N = params['N']
    K = params['K']
    gamma = params['gamma']
    x_crit = params['x_crit']
    D_max = params['D_max']
    eta = params['eta']
    base_fitness = params['base_fitness']

    def system(t, state):
        x_raw = state[:N]
        theta = state[N:]

        # ── Project x onto valid simplex (non-negative, sums to 1) ──
        x = np.maximum(x_raw, 0.0)
        x_sum = np.sum(x)
        if x_sum < 1e-12:
            x = np.ones(N) / N
        else:
            x = x / x_sum

        # ── Fitness ──
        f = np.array([base_fitness[i % len(base_fitness)] for i in range(N)])
        phi_bar = np.dot(x, f)

        # ── Entropy check (Biological Veto) ──
        S_dot = eta * np.dot(x, f)
        if S_dot > D_max:
            veto = D_max / (S_dot + 1e-10)
        else:
            veto = 1.0

        # ── Replicator + Homeostatic (dx/dt) ──
        dx = np.zeros(N)
        for i in range(N):
            replicator = x[i] * (f[i] - phi_bar)
            # Homeostatic brake: only fires when above x_crit
            control = -gamma * max(0.0, x[i] - x_crit)
            # Soft floor: prevent driving resources further negative
            if x_raw[i] < 0.01 and (replicator + control) < 0:
                dx[i] = 0.0
            else:
                dx[i] = (replicator + control) * veto

        # ── Kuramoto (dtheta/dt) ──
        dtheta = np.zeros(N)
        omega = 0.1 * (np.arange(N) - N / 2.0)
        for i in range(N):
            coupling = (K / N) * np.sum(np.sin(theta - theta[i]))
            dtheta[i] = omega[i] + coupling

        return np.concatenate([dx, dtheta])

    return system


def compute_order_parameter(theta):
    """Kuramoto order parameter r — measures global synchronization."""
    return float(np.abs(np.mean(np.exp(1j * theta))))


def run_scenario(label, params):
    """Run one TEO scenario and return results."""
    N = params['N']
    T_end = params['T_end']
    steps = params['steps']

    np.random.seed(42)  # Reproducible results
    x0 = np.ones(N) / N
    theta0 = np.random.uniform(0, 2 * np.pi, N)
    state0 = np.concatenate([x0, theta0])

    t_eval = np.linspace(0, T_end, steps)
    system = make_teo_system(params)

    sol = solve_ivp(system, (0, T_end), state0, t_eval=t_eval,
                    method='RK45', max_step=0.05)

    # Post-process: clamp x to non-negative
    x_hist = np.maximum(sol.y[:N, :], 0.0)
    theta_hist = sol.y[N:, :]

    # Normalize x at each time step
    for t_idx in range(x_hist.shape[1]):
        s = np.sum(x_hist[:, t_idx])
        if s > 1e-12:
            x_hist[:, t_idx] /= s

    order = np.array([compute_order_parameter(theta_hist[:, t])
                      for t in range(len(sol.t))])

    eta = params['eta']
    bf = params['base_fitness']
    entropy = np.array([
        eta * np.dot(x_hist[:, t],
                     [bf[i % len(bf)] for i in range(N)])
        for t in range(len(sol.t))
    ])

    return {
        'label': label,
        'params': params,
        't': sol.t,
        'x': x_hist,
        'theta': theta_hist,
        'order_parameter': order,
        'entropy': entropy,
    }


def gini_coefficient(x):
    """Compute Gini coefficient of a distribution."""
    x = np.sort(np.maximum(x, 0.0))
    n = len(x)
    total = np.sum(x)
    if total < 1e-12:
        return 0.0
    index = np.arange(1, n + 1)
    return float((2.0 * np.sum(index * x) / (n * total)) - (n + 1.0) / n)


def print_summary(result):
    """Print a human-readable summary of the simulation."""
    params = result['params']
    N = params['N']
    D_max = params['D_max']
    x_final = result['x'][:, -1]
    r_final = result['order_parameter'][-1]
    S_final = result['entropy'][-1]
    gini = gini_coefficient(x_final)

    print("=" * 60)
    print("  Thermodynamics of Emergent Orchestration (TEO)")
    print("  Civilization Simulation Results")
    print("=" * 60)
    print(f"  Agents:                  {N}")
    print(f"  Cultural Coupling (K):   {params['K']}")
    print(f"  Regulatory Strength (γ): {params['gamma']}")
    print(f"  Entropy Limit (D_max):   {D_max}")
    print("-" * 60)

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

    print(f"  Final Entropy Rate:      {S_final:.3f} / {D_max}", end="")
    if S_final > D_max:
        print("  ✗ BIOLOGICAL VETO ACTIVE")
    else:
        print(f"  ✓ Within limits ({S_final/D_max*100:.0f}%)")

    print(f"  Gini Coefficient:        {gini:.3f}", end="")
    if gini > 0.4:
        print("  ⚠ High inequality")
    else:
        print("  ✓ Moderate inequality")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    scenarios = [
        ("SCENARIO 1: Healthy Civilization",
         "K=2.5, γ=1.0, D_max=0.8",
         {**DEFAULT_PARAMS}),

        ("SCENARIO 2: No Regulation (γ=0)",
         "Instrumental Convergence / Monopoly",
         {**DEFAULT_PARAMS, 'gamma': 0.0}),

        ("SCENARIO 3: Cultural Collapse (K=0.1)",
         "Filter Bubbles / Polarization",
         {**DEFAULT_PARAMS, 'K': 0.1}),

        ("SCENARIO 4: Entropy Limit Exceeded",
         "Ecological Collapse / Biological Veto",
         {**DEFAULT_PARAMS, 'D_max': 0.15}),
    ]

    for title, subtitle, params in scenarios:
        print(f"\n╔{'═'*58}╗")
        print(f"║  {title:<55} ║")
        print(f"║  {subtitle:<55} ║")
        print(f"╚{'═'*58}╝\n")
        result = run_scenario(title, params)
        print_summary(result)
