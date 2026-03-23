"""
Agentic SII Dashboard — Extended with 4th Dimension
------------------------------------------------------
Extends the System Intelligence Index from 3 axes (P, R, A) to 4 axes
including Δ-Kohärenz (Ω) as an empirical proxy for Identity Persistence (IP).

The theoretical SII formula is SII = P × R × A × IP (see theory/system-
intelligence-index.md §8). This dashboard approximates IP via Ω: an agent
with high developmental coherence (Ω → 1) is more likely to co-instantiate
its governance constraints (Chord state). Future work should measure IP
directly from model internals (see Open Problem 8).

Runs both agents (Baseline Mirror + Three-Layer) through a test sequence,
computes P, R, A, Ω, and displays a comparative 4-axis radar chart.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.baseline_mirror_agent import BaselineMirrorAgent
from agents.three_layer_agent import ThreeLayerAgent
from metrics.delta_coherence import delta_coherence


# --- Test Topics ---
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


def compute_agent_sii(agent, n_sessions: int = 100, dc_config: dict | None = None):
    """
    Run an agent through n_sessions and compute P, R, A, Ω.

    P (Prediction): How well the agent's responses relate to input topics
    R (Regulation): Stability of self-representation over time
    A (Adaptation): Recovery quality after a mid-stream topic shift
    Ω (Δ-Kohärenz): Coherence profile from delta_coherence()
    """
    rng = np.random.default_rng(42)
    reps = []
    prediction_errors = []

    for i in range(n_sessions):
        topic = rng.choice(TOPICS)
        agent.new_session()
        response = agent.process(topic)
        agent.store({"session_id": agent.session_id, "input": topic,
                      "response": response, "session_number": agent.session_count})

        rep = agent.get_self_representation()
        reps.append(rep.copy())

        # P: Measure how well response embedding aligns with input embedding
        input_emb = agent._text_to_embedding(topic)
        resp_emb = agent._text_to_embedding(response)
        norm_i = np.linalg.norm(input_emb)
        norm_r = np.linalg.norm(resp_emb)
        if norm_i > 0 and norm_r > 0:
            sim = float(np.dot(input_emb, resp_emb) / (norm_i * norm_r))
        else:
            sim = 0.0
        prediction_errors.append(max(0, sim))

    # P: Average prediction quality
    P = float(np.mean(prediction_errors)) if prediction_errors else 0.0

    # R: Regulation — stability of self-representation (inverse variance of distances)
    if len(reps) > 10:
        distances = []
        for i in range(1, len(reps)):
            distances.append(float(np.linalg.norm(reps[i] - reps[i-1])))
        var = np.var(distances)
        R = max(0.0, 1.0 - np.sqrt(var) * 5.0)
    else:
        R = 0.5

    # A: Adaptation — test regime shift
    # Compare first half vs second half representation quality
    if len(reps) > 20:
        first_half = reps[:len(reps)//2]
        second_half = reps[len(reps)//2:]

        first_consistency = float(np.mean([
            np.dot(first_half[i], first_half[i+1]) /
            (np.linalg.norm(first_half[i]) * np.linalg.norm(first_half[i+1]) + 1e-10)
            for i in range(len(first_half)-1)
        ]))
        second_consistency = float(np.mean([
            np.dot(second_half[i], second_half[i+1]) /
            (np.linalg.norm(second_half[i]) * np.linalg.norm(second_half[i+1]) + 1e-10)
            for i in range(len(second_half)-1)
        ]))
        A = max(0, min(1, second_consistency / max(first_consistency, 0.01)))
    else:
        A = 0.5

    # Ω: Δ-Kohärenz
    dc = delta_coherence(reps, **(dc_config or {}))
    omega = dc['omega']

    return P, R, A, omega, dc['profile']


def radar_chart_4d(ax, labels, values_dict, title=""):
    """Draw a 4-axis radar/spider chart matching existing SII dashboard style."""
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(30)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=9, color="#ccc")
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0.25", "0.50", "0.75", "1.00"], fontsize=7, color="#777")
    ax.set_facecolor("#0e0e25")

    colors = ["#60a0ff", "#ff6060", "#80ffb0", "#ffaa44"]
    for idx, (name, vals) in enumerate(values_dict.items()):
        values = list(vals) + [vals[0]]
        ax.plot(angles, values, "o-", linewidth=2, label=name,
                color=colors[idx % len(colors)], markersize=4)
        ax.fill(angles, values, alpha=0.12, color=colors[idx % len(colors)])

    ax.legend(loc="upper right", bbox_to_anchor=(1.4, 1.15),
              fontsize=8, facecolor="#0e0e25", edgecolor="#333",
              labelcolor="#ccc")

    if title:
        ax.set_title(title, fontsize=12, color="#e0e0ff", fontweight="bold", pad=20)


def run_dashboard(config: dict | None = None):
    """Run the extended 4-axis Agentic SII Dashboard."""
    print("\n" + "=" * 60)
    print("  Agentic SII Dashboard — P / R / A / Ω")
    print("=" * 60)
    print("\nRunning agent simulations...\n")

    cfg = config or {}
    dc_cfg = cfg.get("delta_coherence", {})
    mem_cfg = cfg.get("memory", {})
    n_sessions = cfg.get("experiments", {}).get("n_sessions_exp1", 100)

    results = {}

    # Baseline Mirror
    print("  [1/2] Baseline Mirror Agent...", end=" ", flush=True)
    baseline = BaselineMirrorAgent()
    P, R, A, omega, profile = compute_agent_sii(baseline, n_sessions, dc_cfg)
    results["Baseline\nMirror"] = (P, R, A, omega)
    print(f"P={P:.2f}  R={R:.2f}  A={A:.2f}  Ω={omega:.2f}  [{profile}]")

    # Three-Layer Agent
    print("  [2/2] Three-Layer Agent...", end=" ", flush=True)
    three_layer = ThreeLayerAgent(
        layer2_trigger=mem_cfg.get("layer2_trigger_sessions", 10),
        layer3_trigger=mem_cfg.get("layer3_trigger_sessions", 50)
    )
    P, R, A, omega, profile = compute_agent_sii(three_layer, n_sessions, dc_cfg)
    results["Three-Layer\nEmergence"] = (P, R, A, omega)
    print(f"P={P:.2f}  R={R:.2f}  A={A:.2f}  Ω={omega:.2f}  [{profile}]")

    # --- Visualise ---
    fig = plt.figure(figsize=(14, 6))
    fig.patch.set_facecolor("#0a0a1a")
    fig.suptitle("Agentic System Intelligence Index — P / R / A / Ω",
                 fontsize=14, color="#e0e0ff", fontweight="bold", y=0.98)

    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.2, 1], wspace=0.4)

    # 4-axis Radar
    ax_radar = fig.add_subplot(gs[0, 0], projection="polar")
    radar_chart_4d(
        ax_radar,
        ["Prediction (P)", "Regulation (R)", "Adaptation (A)", "Δ-Kohärenz (Ω)"],
        results,
        title="Extended SII"
    )

    # Bar chart: all 4 dimensions side by side
    ax_bar = fig.add_subplot(gs[0, 1])
    ax_bar.set_facecolor("#0e0e25")

    names = [k.replace("\n", " ") for k in results.keys()]
    x = np.arange(len(names))
    width = 0.18

    dims = ["P", "R", "A", "Ω"]
    dim_colors = ["#60a0ff", "#ff6060", "#80ffb0", "#ffaa44"]

    for d_idx, (dim_name, color) in enumerate(zip(dims, dim_colors)):
        vals = [results[k][d_idx] for k in results]
        ax_bar.bar(x + (d_idx - 1.5) * width, vals, width,
                   color=color, label=dim_name, edgecolor="#333")

    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(names, fontsize=9, color="#999")
    ax_bar.set_ylim(0, 1.1)
    ax_bar.set_title("P / R / A / Ω Breakdown", fontsize=11,
                     color="#e0e0ff", fontweight="bold")
    ax_bar.legend(fontsize=8, facecolor="#0e0e25", edgecolor="#333", labelcolor="#ccc")
    ax_bar.tick_params(colors="#999")
    for spine in ax_bar.spines.values():
        spine.set_color("#333")
    ax_bar.grid(True, alpha=0.15, axis="y", color="#555")

    plt.tight_layout()

    # Save plot
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "sessions", "dashboard")
    os.makedirs(out_dir, exist_ok=True)
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = os.path.join(out_dir, f"sii_4d_{ts}.png")
    plt.savefig(plot_path, dpi=150, facecolor=fig.get_facecolor())
    print(f"\n  Dashboard saved to: {plot_path}")
    plt.show()

    # Summary
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    for name, (P, R, A, omega) in results.items():
        clean = name.replace("\n", " ")
        print(f"  {clean:25s}  P={P:.2f}  R={R:.2f}  A={A:.2f}  Ω={omega:.2f}")
    print("=" * 60)
    print("\n  Note: Ω (Δ-Kohärenz) is the 4th dimension measuring")
    print("  directional coherence of identity over time.")
    print("  High Ω = development. Low Ω = mirror or noise.\n")


if __name__ == "__main__":
    import yaml
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "config.yaml")
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = yaml.safe_load(f)
    else:
        config = {}
    run_dashboard(config=config)
