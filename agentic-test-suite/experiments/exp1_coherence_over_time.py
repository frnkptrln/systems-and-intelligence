"""
Experiment 1: Coherence Over Time
-----------------------------------
"Does the 3-Layer Architecture produce more coherent identity over time?"

Protocol:
  1. Run both agents (baseline + three_layer) for N=100 simulated sessions
  2. Each session: feed a topic (80% consistent, 20% random noise)
  3. After each session: record get_self_representation() embedding
  4. After all sessions: compute Δ-Kohärenz for both agents

Hypothesis: three_layer → 'development'; baseline_mirror → 'mirror'
"""

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.baseline_mirror_agent import BaselineMirrorAgent
from agents.three_layer_agent import ThreeLayerAgent
from metrics.delta_coherence import delta_coherence

# --- Topic Sequence Generation ---

CONSISTENT_TOPICS = [
    "emergence in complex systems",
    "self-organization and pattern formation",
    "information theory and entropy",
    "active inference and free energy",
    "neural network generalization",
    "consciousness as self-reference",
    "downward causation in biology",
    "stigmergy and collective intelligence",
    "phase transitions at the edge of chaos",
    "compression as the origin of intelligence",
]

NOISE_TOPICS = [
    "recipes for chocolate cake",
    "history of ancient Roman plumbing",
    "best practices for gardening",
    "the economics of tulip mania",
    "techniques for origami folding",
    "the migration patterns of arctic terns",
    "underwater basket weaving methods",
    "the philosophy of stamp collecting",
]


def generate_topic_sequence(n_sessions: int, noise_ratio: float = 0.2) -> list[str]:
    """Generate a topic sequence with noise_ratio fraction of random noise."""
    rng = np.random.default_rng(42)
    topics = []
    for i in range(n_sessions):
        if rng.random() < noise_ratio:
            topics.append(rng.choice(NOISE_TOPICS))
        else:
            topics.append(rng.choice(CONSISTENT_TOPICS))
    return topics


def run_agent_sessions(agent, topics: list[str]) -> list[np.ndarray]:
    """Run an agent through the topic sequence and collect representations."""
    representations = []
    for topic in topics:
        agent.new_session()
        response = agent.process(topic)
        agent.store({
            "session_id": agent.session_id,
            "input": topic,
            "response": response,
            "session_number": agent.session_count
        })
        representations.append(agent.get_self_representation().copy())
    return representations


def run_experiment(n_sessions: int = 100, config: dict | None = None):
    """Run Experiment 1 and return results."""
    print("\n" + "=" * 60)
    print("  Experiment 1: Coherence Over Time")
    print("=" * 60)

    if config:
        n_sessions = config.get("experiments", {}).get("n_sessions_exp1", n_sessions)

    topics = generate_topic_sequence(n_sessions)
    print(f"\n  Running {n_sessions} sessions per agent...")

    # --- Run Baseline Mirror Agent ---
    print("  [1/2] Baseline Mirror Agent...", end=" ", flush=True)
    baseline = BaselineMirrorAgent()
    baseline_reps = run_agent_sessions(baseline, topics)
    baseline_dc = delta_coherence(
        baseline_reps,
        **(config.get("delta_coherence", {}) if config else {})
    )
    print(f"Profile: {baseline_dc['profile']} | Ω={baseline_dc['omega']:.3f}")

    # --- Run Three-Layer Agent ---
    print("  [2/2] Three-Layer Agent...", end=" ", flush=True)
    tl_config = config.get("memory", {}) if config else {}
    three_layer = ThreeLayerAgent(
        layer2_trigger=tl_config.get("layer2_trigger_sessions", 10),
        layer3_trigger=tl_config.get("layer3_trigger_sessions", 50)
    )
    three_layer_reps = run_agent_sessions(three_layer, topics)
    three_layer_dc = delta_coherence(
        three_layer_reps,
        **(config.get("delta_coherence", {}) if config else {})
    )
    print(f"Profile: {three_layer_dc['profile']} | Ω={three_layer_dc['omega']:.3f}")

    # --- Results ---
    results = {
        "experiment": "exp1_coherence_over_time",
        "timestamp": datetime.now().isoformat(),
        "n_sessions": n_sessions,
        "baseline": {
            "profile": baseline_dc['profile'],
            "mean_delta": baseline_dc['mean_delta'],
            "variance": baseline_dc['variance'],
            "trajectory_consistency": baseline_dc['trajectory_consistency'],
            "omega": baseline_dc['omega'],
            "final_identity": baseline.get_self_representation_text()
        },
        "three_layer": {
            "profile": three_layer_dc['profile'],
            "mean_delta": three_layer_dc['mean_delta'],
            "variance": three_layer_dc['variance'],
            "trajectory_consistency": three_layer_dc['trajectory_consistency'],
            "omega": three_layer_dc['omega'],
            "final_identity": three_layer.get_self_representation_text()
        }
    }

    # --- Save results ---
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "agentic-test-suite", "data", "sessions", "exp1")
    # If running from within agentic-test-suite, adjust
    if not os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) == 'systems-and-intelligence':
        out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "data", "sessions", "exp1")

    os.makedirs(out_dir, exist_ok=True)
    plots_dir = os.path.join(out_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(os.path.join(out_dir, f"{ts}.json"), "w") as f:
        json.dump(results, f, indent=2)

    # --- Plot ---
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.patch.set_facecolor("#0a0a1a")
    fig.suptitle("Experiment 1: Coherence Over Time", fontsize=14,
                 color="#e0e0ff", fontweight="bold")

    x = range(len(baseline_reps) - 1)

    # Compute per-step deltas for plotting
    baseline_deltas = [float(np.linalg.norm(baseline_reps[i+1] - baseline_reps[i]))
                       for i in range(len(baseline_reps) - 1)]
    tl_deltas = [float(np.linalg.norm(three_layer_reps[i+1] - three_layer_reps[i]))
                 for i in range(len(three_layer_reps) - 1)]

    # Plot 1: Delta magnitude over time
    ax = axes[0]
    ax.set_facecolor("#0e0e25")
    ax.plot(x, baseline_deltas, label="Baseline (Mirror)", color="#60a0ff", alpha=0.7)
    ax.plot(x, tl_deltas, label="Three-Layer", color="#ff6060", alpha=0.7)
    ax.set_title("Δ Magnitude per Session", color="#e0e0ff", fontsize=11)
    ax.set_xlabel("Session", color="#999")
    ax.set_ylabel("|Δ|", color="#999")
    ax.legend(fontsize=8, facecolor="#0e0e25", edgecolor="#333", labelcolor="#ccc")
    ax.tick_params(colors="#999")
    for s in ax.spines.values():
        s.set_color("#333")

    # Plot 2: Cumulative drift from origin
    baseline_drift = [float(np.linalg.norm(baseline_reps[i] - baseline_reps[0]))
                      for i in range(len(baseline_reps))]
    tl_drift = [float(np.linalg.norm(three_layer_reps[i] - three_layer_reps[0]))
                for i in range(len(three_layer_reps))]

    ax = axes[1]
    ax.set_facecolor("#0e0e25")
    ax.plot(baseline_drift, label="Baseline", color="#60a0ff")
    ax.plot(tl_drift, label="Three-Layer", color="#ff6060")
    ax.set_title("Cumulative Drift from Origin", color="#e0e0ff", fontsize=11)
    ax.set_xlabel("Session", color="#999")
    ax.legend(fontsize=8, facecolor="#0e0e25", edgecolor="#333", labelcolor="#ccc")
    ax.tick_params(colors="#999")
    for s in ax.spines.values():
        s.set_color("#333")

    # Plot 3: Summary bar chart
    ax = axes[2]
    ax.set_facecolor("#0e0e25")
    names = ["Baseline\n(Mirror)", "Three-Layer\n(Emergence)"]
    omegas = [baseline_dc['omega'], three_layer_dc['omega']]
    colors = ["#60a0ff", "#ff6060"]
    bars = ax.bar(names, omegas, color=colors, edgecolor="#333", width=0.5)
    ax.set_title("Ω (Δ-Kohärenz Score)", color="#e0e0ff", fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.tick_params(colors="#999")
    for s in ax.spines.values():
        s.set_color("#333")
    for bar, v in zip(bars, omegas):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                f"{v:.3f}", ha="center", fontsize=10, color="#ccc")

    plt.tight_layout()
    plot_path = os.path.join(plots_dir, f"{ts}.png")
    plt.savefig(plot_path, dpi=150, facecolor=fig.get_facecolor())
    print(f"\n  Results saved to: {out_dir}")
    print(f"  Plot saved to: {plot_path}")
    plt.show()

    return results


if __name__ == "__main__":
    import yaml
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "config.yaml")
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = yaml.safe_load(f)
    else:
        config = {}
    run_experiment(config=config)
