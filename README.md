# 🧠 systems-and-intelligence

This repository explores how **intelligence**, **adaptation**, and **structure**
emerge from the interaction of simple components.
It brings together simulation models, theoretical notes, and learning systems
that illustrate how **local rules can generate global behavior**, how systems
stabilize themselves, and how observers learn from the dynamics they inhabit.

The project spans several layers:

- **Self-organization**
- **Nested learning**
- **Emergent regulation**
- **Feedback and control**
- **Limits of computation and intelligence**

Each folder represents a different perspective on these themes.

---

## 📂 Repository Overview

| Folder | Purpose |
| :--- | :--- |
| **`simulation-models/`** | Concrete dynamical systems: cellular automata, agent-based simulations, homeostasis models, nested-learning examples. |
| **`data-analysis/`** | Information-theoretic measures (entropy, mutual information, transfer entropy, integration) and comparative analysis tools. |
| **`tools/`** | Shared utilities for visualization, randomness, grid manipulation, and reproducibility. |
| **`theory/`** | Conceptual notes and essays on systems, intelligence, and emergent behavior. |
| **`meta/`** | Reflections on epistemology, ethics, and the limits of formal systems and computation. |

Each subfolder contains its own README with context and details.

### 🧪 Simulation Models

| Model | Theme |
| :--- | :--- |
| `ecosystem-regulation/` | 🌿 Homeostatic cellular automaton with density feedback |
| `nested-learning-two-state/` | 🧠 Observer learning a Markov system's transition matrix |
| `prediction-error-field/` | 🔮 Local learners embedded in a Game of Life world |
| `tensor-logic-reasoning/` | 📐 Embedding-based relational reasoning (Tensor Logic) |
| `stigmergy-swarm/` | 🐜 Ant-like agents with pheromone trails – emergent path optimization |
| `meta-learning-regime-shift/` | 🔄 Meta-learner that adapts η under regime shifts |
| `coupled-oscillators/` | 🔗 Kuramoto model – emergent synchronization of phase oscillators |
| `reaction-diffusion/` | 🌊 Gray-Scott model – Turing patterns from two diffusing chemicals |
| `hebbian-memory/` | 🧬 Hopfield network – self-organizing associative memory via Hebb's rule |
| `boids-flocking/` | 🐦 Reynolds' Boids – emergent collective motion from three local rules |
| `lenia/` | 🌌 Lenia – continuous cellular automata producing lifelike organisms |
| `self-organized-criticality/` | ⚡ Bak's Sandpile – power-law avalanches without parameter tuning |
| `dao-ecosystem/` | ⚖️ DAO Ecosystem – resource alignment and homeostasis vs exponential growth |

### 📚 Theory & Essays

Selected theoretical notes and essays located in the `theory/` directory:

- [**Der Menschheits-Organismus im Silizium-Zeitalter**](theory/human-organism-silicon-age):
  - [Kernthesen](theory/human-organism-silicon-age/core-theses.md) – The alignment problem of fitness functions and Gödel's incompleteness.
  - [Anleitung für Zellen im Widerstand](theory/human-organism-silicon-age/guide-for-cells-in-resistance.md) – Preserving individuality in a system optimized for total predictability.
  - [Solarpunk-Utopie: Gödels Verfassung](theory/human-organism-silicon-age/solarpunk-utopia-goedel-constitution.md) – A society using the formal limits of logic as its constitution.

---

## 🚀 Getting Started

Clone the repository and install dependencies:

```bash
git clone https://github.com/frnkptrln/systems-and-intelligence.git
cd systems-and-intelligence
pip install -r requirements.txt
```

Then run any simulation:

```bash
cd simulation-models/lenia
python3 lenia.py
```

Press `ESC` in any simulation window to exit.

---

## 🗺 Conceptual Map

For a guide to how all the models connect, see
[Conceptual Map](theory/conceptual-map.md) – the conceptual map
that traces the arc from self-organization through learning to
system intelligence and its limits.
