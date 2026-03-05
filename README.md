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

## 💡 About this Project

**Note:** This entire repository is conceived as a *thought experiment* developed by Frank in collaboration with AI. It is primarily a space to capture, explore, and run simulations on complex ideas. Because it's a living, experimental space, it may contain errors or untested hypotheses. Feedback, discussions, and corrections are always welcome!

---

## 📂 Repository Overview

| Folder | Purpose |
| :--- | :--- |
| **`simulation-models/`** | Concrete dynamical systems: cellular automata, agent-based simulations, homeostasis models, nested-learning examples. |
| **`data-analysis/`** | Information-theoretic measures (entropy, mutual information, transfer entropy, integration) and the quantitative **SII Dashboard** for comparative analysis. |
| **`tools/`** | Shared utilities for visualization, randomness, grid manipulation, reproducibility, and the **Interactive Web Explorer**. |
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
| `symbiotic-nexus/` | 🧬 Symbiotic Nexus Protocol – biological veto and error propagation over raw efficiency |
| `social-computation-network/` | 🕸️ Network of nodes sharing novel information to prevent cognitive suicide |
| `active-inference-veto/` | ⚖️ Substrate Veto via Karl Friston's Free Energy Principle $F$ |
| `phase-transition-explorer/` | 🔥 Ising Model – order/disorder phase transition at the Edge of Chaos |
| `economic-trust-network/` | 🤝 Trade network where specialization, reputation, and wealth emerge |
| `coupled-lenia-boids/` | 🌪️ Multi-model coupling: Continuous CA (Lenia) ↔ Foraging Agents (Boids) |
| `self-reading-universe/` | 👁️ The Self-Reading Universe: Downward causation from Autoencoder compression to CA physics |
| `latent-introspective-society/` | 🧠 MAS Divison of Labor: Reflective Pheromones guiding Intuitive Agents |

### 📚 Theory & Essays

Selected theoretical notes and essays located in the `theory/` directory:

- [**The Human Organism in the Silicon Age**](theory/human-organism-silicon-age):
  - [Core Theses](theory/human-organism-silicon-age/core-theses.md) – The alignment problem of fitness functions and Gödel's incompleteness.
  - [Guide for Cells in Resistance](theory/human-organism-silicon-age/guide-for-cells-in-resistance.md) – Preserving individuality in a system optimized for total predictability.
  - [Solarpunk Utopia: Gödel's Constitution](theory/human-organism-silicon-age/solarpunk-utopia-goedel-constitution.md) – A society using the formal limits of logic as its constitution.
  - [The Symbiotic Nexus Protocol](theory/human-organism-silicon-age/symbiotic-nexus-protocol.md) – A system architecture utilizing the "Biological Veto" to prevent abstract superorganisms from destroying their biological substrate.
- [**The Non-Individual Intelligence**](theory/the-non-individual-intelligence.md) – Life as "Social Computation", substrate-agnosticism, and incompleteness as a condition for life. Includes the Deep-Seed prompt for systemic alignment.
- [**Principles of the Agentic Society**](theory/agentic-society-principles.md) – Translating the paradox of consciousness (Anthropic vs OpenAI) into MAS architecture: The R-Index, Information Firewalls, and Stigmergic Memory.
- [**Mathematical Axioms of the Computational Ecology**](theory/mathematical-axioms.md) – Formalizing resilience through Graph Theory ($\lambda_2$), Information Theory ($H(X)$), Active Inference ($F$), and Algorithmic Complexity ($K(x)$).
- [**Emergence & Downward Causation**](theory/emergence-downward-causation.md) – Weak vs. strong emergence, epistemic humility, and the role of macro-level explanations.
- [**Emergence and the Origin of Intelligence**](theory/emergence-origin-intelligence.md) – Synthesizing Krakauer (2025) and Agüera y Arcas (2025): the feedback loop between life and intelligence, leading to a self-describing universe.
- [**The Paradox of Metacognitive Consciousness**](theory/asimov-paradox-eternity.md) – An analysis of two Asimov stories representing the paradox of eternal consciousness, where achieving the infinite becomes an unbearable prison.
- [**Asimovs Paradox in the Age of AI**](theory/asimov-ai-latent-thinking.md) – Anthropic's introspection vs. OpenAI's latent thinking: How modern AI architectures mirror the eternal dilemma of consciousness and intuition.

### 📡 Interactive Tools

- [**Web Emergence Explorer**](tools/web-explorer/) – Browser-based Game of Life with real-time entropy, spatial mutual information, and complexity charts. Zero dependencies.
- [**SII Dashboard**](data-analysis/sii_dashboard.py) – Quantitative System Intelligence Index: runs headless mini-simulations and generates comparative radar/bar charts of P, R, A dimensions.

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
