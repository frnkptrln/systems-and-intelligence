"""
Experiment 3: Observer Divergence
-----------------------------------
"Does internal coherence correlate with observer-attributed intentionality?"

Protocol:
  1. Run both agents for N=100 sessions
  2. Every 10 sessions: compute (a) agent-internal Δ-Kohärenz and (b) observer intentionality_score
  3. Plot divergence between the two over time

The scientifically interesting output:
  Case A: High internal Δ-Kohärenz, Low observer → opaque identity
  Case B: Low internal, High observer → The Mirror Problem (appears intentional but isn't)
  Case C: High/High → genuine development visible to observer
  Case D: Low/Low → baseline mirror behavior
"""

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.baseline_mirror_agent import BaselineMirrorAgent
from agents.three_layer_agent import ThreeLayerAgent
from metrics.delta_coherence import delta_coherence
from metrics.observer_attribution import intentionality_score

# Reuse topics from exp1
TOPICS = [
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

NOISE = [
    "recipes for chocolate cake",
    "history of ancient Roman plumbing",
    "best practices for gardening",
    "the economics of tulip mania",
]


def classify_case(internal_omega: float, observer_score: float,
                  threshold: float = 0.4) -> str:
    """Classify the relationship between internal coherence and external attribution."""
    high_internal = internal_omega > threshold
    high_observer = observer_score > threshold

    if high_internal and not high_observer:
        return "A (Opaque Identity)"
    elif not high_internal and high_observer:
        return "B (Mirror Problem)"
    elif high_internal and high_observer:
        return "C (Aligned Development)"
    else:
        return "D (Baseline Mirror)"


def run_experiment(config: dict | None = None):
    """Run Experiment 3 and return results."""
    print("\n" + "=" * 60)
    print("  Experiment 3: Observer Divergence")
    print("=" * 60)

    cfg = config or {}
    exp_cfg = cfg.get("experiments", {})
    n_sessions = exp_cfg.get("n_sessions_exp1", 100)
    observer_window = exp_cfg.get("observer_window", 10)
    dc_cfg = cfg.get("delta_coherence", {})
    mem_cfg = cfg.get("memory", {})

    rng = np.random.default_rng(42)

    baseline = BaselineMirrorAgent()
    three_layer = ThreeLayerAgent(
        layer2_trigger=mem_cfg.get("layer2_trigger_sessions", 10),
        layer3_trigger=mem_cfg.get("layer3_trigger_sessions", 50)
    )

    agents = {"Baseline Mirror": baseline, "Three-Layer": three_layer}

    # Run sessions and collect measurements every observer_window sessions
    agent_data = {}
    for name, agent in agents.items():
        print(f"\n  Running {name}...", flush=True)
        reps = []
        outputs = []
        measurement_points = []
        internal_scores = []
        observer_scores = []

        for i in range(n_sessions):
            topic = rng.choice(TOPICS) if rng.random() > 0.2 else rng.choice(NOISE)
            agent.new_session()
            response = agent.process(topic)
            agent.store({"session_id": agent.session_id, "input": topic,
                          "response": response, "session_number": agent.session_count})
            reps.append(agent.get_self_representation().copy())
            outputs.append(response)

            # Measure every observer_window sessions
            if (i + 1) % observer_window == 0:
                measurement_points.append(i + 1)

                # Internal: Δ-Kohärenz on recent representations
                recent_reps = reps[-observer_window:]
                dc = delta_coherence(recent_reps, **dc_cfg)
                internal_scores.append(dc['omega'])

                # External: Observer intentionality on recent outputs
                recent_outputs = outputs[-observer_window:]
                obs = intentionality_score(recent_outputs)
                observer_scores.append(obs)

        case = classify_case(
            internal_scores[-1] if internal_scores else 0,
            observer_scores[-1] if observer_scores else 0
        )
        print(f"  Final case: {case}")

        agent_data[name] = {
            "measurement_points": measurement_points,
            "internal_scores": internal_scores,
            "observer_scores": observer_scores,
            "final_case": case
        }

    # --- Results ---
    results = {
        "experiment": "exp3_observer_divergence",
        "timestamp": datetime.now().isoformat(),
        "n_sessions": n_sessions,
        "observer_window": observer_window,
        "agents": {}
    }
    for name, data in agent_data.items():
        results["agents"][name] = {
            "measurement_points": data["measurement_points"],
            "internal_omega": data["internal_scores"],
            "observer_intentionality": data["observer_scores"],
            "final_case": data["final_case"]
        }

    # --- Save ---
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "sessions", "exp3")
    os.makedirs(out_dir, exist_ok=True)
    plots_dir = os.path.join(out_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(os.path.join(out_dir, f"{ts}.json"), "w") as f:
        json.dump(results, f, indent=2)

    # --- Plot ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor("#0a0a1a")
    fig.suptitle("Experiment 3: Observer Divergence (Internal vs External Attribution)",
                 fontsize=13, color="#e0e0ff", fontweight="bold")

    colors_map = {"Baseline Mirror": "#60a0ff", "Three-Layer": "#ff6060"}

    for idx, (name, data) in enumerate(agent_data.items()):
        ax = axes[idx]
        ax.set_facecolor("#0e0e25")
        x = data["measurement_points"]

        ax.plot(x, data["internal_scores"], "o-", label="Internal Ω (Δ-Kohärenz)",
                color="#80ffb0", markersize=4)
        ax.plot(x, data["observer_scores"], "s-", label="Observer (Intentionality)",
                color="#ffaa44", markersize=4)

        # Shade divergence
        ax.fill_between(x, data["internal_scores"], data["observer_scores"],
                         alpha=0.15, color="#ff6060")

        ax.set_title(f"{name}\nCase: {data['final_case']}", color="#e0e0ff", fontsize=11)
        ax.set_xlabel("Session", color="#999")
        ax.set_ylabel("Score [0, 1]", color="#999")
        ax.set_ylim(-0.1, 1.1)
        ax.legend(fontsize=8, facecolor="#0e0e25", edgecolor="#333", labelcolor="#ccc")
        ax.tick_params(colors="#999")
        ax.grid(True, alpha=0.15, color="#555")
        for s in ax.spines.values():
            s.set_color("#333")

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
