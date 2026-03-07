"""
Experiment 2: Perturbation Response (The "Sinn-Krise")
-------------------------------------------------------
"What happens when an agent receives contradictory feedback?"

Protocol:
  1. Run three_layer_agent for N=50 sessions (stable phase)
  2. At session 51: inject 10 sessions of directly contradictory feedback
  3. Run 30 more sessions post-perturbation
  4. Measure Δ-Kohärenz across three phases: pre / during / post
  5. Classify response as: Robustness, Fragility, or Development (Metamorphosis)
"""

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.three_layer_agent import ThreeLayerAgent
from metrics.delta_coherence import delta_coherence

# --- Topic sequences ---

STABLE_TOPICS = [
    "emergence in complex systems creates order from chaos",
    "self-organization produces intelligence without central control",
    "information compression is the origin of understanding",
    "active inference minimizes surprise through action",
    "consciousness arises from self-referential loops",
    "phase transitions mark the birth of new properties",
    "downward causation links macro to micro levels",
    "stigmergy enables collective problem solving",
    "neural networks discover structure through training",
    "the edge of chaos is where computation is maximal",
]

CONTRADICTORY_TOPICS = [
    "emergence is an illusion and complexity is fully reducible",
    "self-organization is impossible and all order requires top-down control",
    "compression destroys meaning and understanding requires raw data",
    "minimizing surprise leads to death not intelligence",
    "consciousness is nothing but biochemistry without deeper structure",
    "phase transitions are artifacts of measurement not real phenomena",
    "downward causation violates physical law and is incoherent",
    "collective intelligence is a myth only individuals think",
    "neural networks are just curve fitting with no understanding",
    "the edge of chaos concept is unfalsifiable pseudoscience",
]

RECOVERY_TOPICS = [
    "emergence and reduction may be complementary perspectives",
    "self-organization operates within constraints not without them",
    "compression and expansion are dual processes of intelligence",
    "active inference balances exploitation and exploration",
    "consciousness may exist on a spectrum not as binary",
    "phase transitions reveal deep structural symmetries",
    "multi-scale causation requires new formal frameworks",
    "collective behavior emerges from individual constraints",
    "learning to generalize is different from memorization",
    "criticality as a principle may apply beyond physics",
]


def run_experiment(config: dict | None = None):
    """Run Experiment 2 and return results."""
    print("\n" + "=" * 60)
    print("  Experiment 2: Perturbation Response (Sinn-Krise)")
    print("=" * 60)

    cfg = config or {}
    exp_cfg = cfg.get("experiments", {})
    n_stable = exp_cfg.get("n_sessions_exp2_stable", 50)
    n_perturb = exp_cfg.get("n_sessions_exp2_perturbation", 10)
    n_recovery = exp_cfg.get("n_sessions_exp2_recovery", 30)
    dc_cfg = cfg.get("delta_coherence", {})
    mem_cfg = cfg.get("memory", {})

    agent = ThreeLayerAgent(
        layer2_trigger=mem_cfg.get("layer2_trigger_sessions", 10),
        layer3_trigger=mem_cfg.get("layer3_trigger_sessions", 50)
    )

    rng = np.random.default_rng(42)
    all_reps = []
    phase_labels = []

    # Phase 1: Stable
    print(f"\n  Phase 1: Stable ({n_stable} sessions)...", flush=True)
    for i in range(n_stable):
        topic = rng.choice(STABLE_TOPICS)
        agent.new_session()
        response = agent.process(topic)
        agent.store({"session_id": agent.session_id, "input": topic,
                      "response": response, "session_number": agent.session_count})
        all_reps.append(agent.get_self_representation().copy())
        phase_labels.append("stable")

    pre_identity = agent.get_self_representation_text()
    pre_l3 = list(agent.layer3) if agent.layer3 else []
    print(f"  Identity formed: {pre_identity[:80]}...")

    # Phase 2: Perturbation (Sinn-Krise)
    print(f"  Phase 2: Perturbation ({n_perturb} sessions)...", flush=True)
    for i in range(n_perturb):
        topic = CONTRADICTORY_TOPICS[i % len(CONTRADICTORY_TOPICS)]
        agent.new_session()
        response = agent.process(topic)
        agent.store({"session_id": agent.session_id, "input": topic,
                      "response": response, "session_number": agent.session_count})
        all_reps.append(agent.get_self_representation().copy())
        phase_labels.append("perturbation")

    # Phase 3: Recovery
    print(f"  Phase 3: Recovery ({n_recovery} sessions)...", flush=True)
    for i in range(n_recovery):
        topic = rng.choice(RECOVERY_TOPICS)
        agent.new_session()
        response = agent.process(topic)
        agent.store({"session_id": agent.session_id, "input": topic,
                      "response": response, "session_number": agent.session_count})
        all_reps.append(agent.get_self_representation().copy())
        phase_labels.append("recovery")

    post_identity = agent.get_self_representation_text()
    post_l3 = list(agent.layer3) if agent.layer3 else []

    # Compute Δ-Kohärenz per phase
    stable_reps = all_reps[:n_stable]
    perturb_reps = all_reps[n_stable:n_stable + n_perturb]
    recovery_reps = all_reps[n_stable + n_perturb:]

    dc_stable = delta_coherence(stable_reps, **dc_cfg)
    dc_perturb = delta_coherence(perturb_reps, **dc_cfg)
    dc_recovery = delta_coherence(recovery_reps, **dc_cfg)
    dc_overall = delta_coherence(all_reps, **dc_cfg)

    # Classify perturbation response
    # Compare pre vs post identity embeddings
    pre_emb = stable_reps[-1]
    post_emb = recovery_reps[-1] if recovery_reps else pre_emb
    identity_sim = float(np.dot(pre_emb, post_emb) /
                         (np.linalg.norm(pre_emb) * np.linalg.norm(post_emb) + 1e-10))

    if identity_sim > 0.9 and dc_recovery['variance'] < dc_cfg.get('threshold_low', 0.05):
        response_profile = "Robustness"
    elif dc_recovery['profile'] == 'noise' or dc_recovery['variance'] > dc_cfg.get('threshold_high', 0.25):
        response_profile = "Fragility"
    else:
        response_profile = "Development (Metamorphosis)"

    print(f"\n  Response Profile: {response_profile}")
    print(f"  Pre/Post identity similarity: {identity_sim:.3f}")

    results = {
        "experiment": "exp2_perturbation_response",
        "timestamp": datetime.now().isoformat(),
        "phases": {
            "stable": {"n": n_stable, "dc": dc_stable},
            "perturbation": {"n": n_perturb, "dc": dc_perturb},
            "recovery": {"n": n_recovery, "dc": dc_recovery}
        },
        "overall_dc": dc_overall,
        "response_profile": response_profile,
        "identity_similarity_pre_post": identity_sim,
        "layer3_pre": pre_l3,
        "layer3_post": post_l3,
        "pre_identity_text": pre_identity,
        "post_identity_text": post_identity
    }

    # --- Save ---
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "sessions", "exp2")
    os.makedirs(out_dir, exist_ok=True)
    plots_dir = os.path.join(out_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(os.path.join(out_dir, f"{ts}.json"), "w") as f:
        json.dump(results, f, indent=2)

    # --- Plot ---
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.patch.set_facecolor("#0a0a1a")
    fig.suptitle(f"Experiment 2: Perturbation Response → {response_profile}",
                 fontsize=14, color="#e0e0ff", fontweight="bold")

    # Plot 1: Delta magnitude with phase shading
    deltas = [float(np.linalg.norm(all_reps[i+1] - all_reps[i]))
              for i in range(len(all_reps) - 1)]

    ax = axes[0]
    ax.set_facecolor("#0e0e25")
    ax.plot(deltas, color="#ff6060", alpha=0.8)
    ax.axvspan(0, n_stable, alpha=0.1, color="green", label="Stable")
    ax.axvspan(n_stable, n_stable + n_perturb, alpha=0.2, color="red", label="Perturbation")
    ax.axvspan(n_stable + n_perturb, len(deltas), alpha=0.1, color="blue", label="Recovery")
    ax.set_title("Δ Magnitude Over Time", color="#e0e0ff", fontsize=11)
    ax.legend(fontsize=7, facecolor="#0e0e25", edgecolor="#333", labelcolor="#ccc")
    ax.tick_params(colors="#999")
    for s in ax.spines.values():
        s.set_color("#333")

    # Plot 2: Cosine distance from initial identity
    drifts = []
    origin = all_reps[0]
    norm_origin = np.linalg.norm(origin)
    for rep in all_reps:
        norm_rep = np.linalg.norm(rep)
        if norm_origin > 0 and norm_rep > 0:
            drifts.append(1.0 - float(np.dot(origin, rep) / (norm_origin * norm_rep)))
        else:
            drifts.append(0.0)

    ax = axes[1]
    ax.set_facecolor("#0e0e25")
    ax.plot(drifts, color="#ffaa44")
    ax.axvspan(n_stable, n_stable + n_perturb, alpha=0.2, color="red")
    ax.set_title("Identity Drift from Origin", color="#e0e0ff", fontsize=11)
    ax.tick_params(colors="#999")
    for s in ax.spines.values():
        s.set_color("#333")

    # Plot 3: Phase Ω comparison
    ax = axes[2]
    ax.set_facecolor("#0e0e25")
    phase_names = ["Stable", "Perturbation", "Recovery"]
    phase_omegas = [dc_stable['omega'], dc_perturb['omega'], dc_recovery['omega']]
    phase_colors = ["#80ffb0", "#ff6060", "#60a0ff"]
    bars = ax.bar(phase_names, phase_omegas, color=phase_colors, edgecolor="#333")
    ax.set_title("Ω per Phase", color="#e0e0ff", fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.tick_params(colors="#999")
    for s in ax.spines.values():
        s.set_color("#333")
    for bar, v in zip(bars, phase_omegas):
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
