# 🧠 systems-and-intelligence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/frnkptrln/systems-and-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/frnkptrln/systems-and-intelligence/actions/workflows/ci.yml)
[![Docs](https://github.com/frnkptrln/systems-and-intelligence/actions/workflows/deploy-docs.yml/badge.svg)](https://frnkptrln.github.io/systems-and-intelligence)

<div align="center">
  <h3><i>A research notebook on emergence, inverse reconstruction, and viability constraints in intelligent systems</i></h3>
</div>

> **What this is — and is not.** This repository does not claim a theory of everything. It studies one recurring asymmetry: simple generators produce rich traces cheaply, but reconstructing the generator from its trace — especially under noise, partial observability, and an unknown model class — is hard; and optimizing systems become dangerous when their constraint architecture cannot scale with their capability. At its speculative edge it asks, without answering, whether phenomena like identity and consciousness are best read not as properties of behavior but as *modes of generative organization* — a question kept open, and explicitly not a claim that any present system is conscious. Every major claim carries an epistemic status tag, every major concept an external anchor in the [Related Work Map](meta/research-alignment/related-work-map.md), and the boundaries are stated explicitly in **[What This Project Does NOT Claim](theory/reference/what-this-project-does-not-claim.md)**.

---

## ⚡ Try it live in your browser
Don't want to install anything? You can experience the core concepts immediately directly in your browser:

- 🧭 **Recommended Reading Path** — the research arc *emergence → optimization → constraint architecture → survivability* (full map: **[Canonical Path v2](meta/repository-meta/canonical-path-v2.md)**; the epistemic spine folded into one page: **[From Trace to World-Binding](theory/core/from-trace-to-world-binding.md)**):
  1. **[The Generator Question](theory/core/the-generator-question.md)** — The organizing question. Forward vs. inverse asymmetry. The three walls (P vs. NP, Kolmogorov, Gödel). The foundational assumption.
  2. **[Emergence Manifesto](theory/core/emergence-manifesto-v1.3.md)** — The core claim set (emergence).
  3. **[Optimization and Its Blindness](theory/optimization/optimization-and-its-blindness.md)** — The hinge: why unconstrained optimization of an emergent system is non-viable, and why capability loads multiple constraints at once.
  4. **[TEO Framework](theory/teo-framework/README.md)** — The constraint-architecture model.
  5. **[The Viable Corridor](papers/viable-corridor.md)** — The formal synthesis: constraint architecture + capability loading (a stabilized *node*, not the whole repo).
  6. **[From Rule to Mind](book/09_from_rule_to_mind.md)** — The compact course spine connecting the whole system.
  7. **[AI Alignment Veto](simulation-models/alignment-and-veto/ai-alignment-veto/README.md)** — A runnable proof artifact.
- 🕹️ **[Run the Web Emergence Explorer](https://frnkptrln.github.io/systems-and-intelligence/interactive/web-explorer/)** — An interactive Cellular Automata sandbox with real-time entropy and mutual information charts.
- 📖 **[Read the Interactive Book](https://frnkptrln.github.io/systems-and-intelligence)** — The curated online book: the reader-first path through the theory. (A PDF snapshot lives at [`systems-and-intelligence-book.pdf`](systems-and-intelligence-book.pdf).)

---

**This project brings together simulation models, theoretical notes, and learning systems** that illustrate how local actions generate global behavior, how systems stabilize themselves, and how observers learn from the dynamics they inhabit.

The project spans several layers:

- **Self-organization**
- **Nested learning**
- **Emergent regulation**
- **Feedback and control**
- **Limits of computation and intelligence**

Each folder represents a different perspective on these themes.

---

## 📜 Papers (working drafts)
Two paper-style syntheses live in `papers/`. Neither is published or externally reviewed; both carry explicit status blocks:
- **[The Viable Corridor](papers/viable-corridor.md)** — the current synthesis (v0.8): constraint architecture + capability loading, with proofs, predictions, and stated limitations.
- **[Quantifying Emergent Utility & Stability in Multi-Agent LLM Ecosystems](papers/quantifying-emergent-utility-in-llms.md)** — the project's early statement (SII, C-Score, orchestration). Predates the current epistemic line and awaits revision as the empirical companion once the Agentic Identity Suite runs on real models; see the status note in the file.

---

## ⚖️ License & Intellectual Property
This repository and its mathematical frameworks (including the $C$-Score, The Planetary Veto, and Systems Orchestration) are licensed under the **MIT License**.

**What this means:**
- **Open Science & Open Source:** Academics, researchers, and open-source developers are free to use, modify, and distribute this work. Startups and individuals are encouraged to build upon these simulations.
- **Permissive Use:** You are free to use this code for both open-source and commercial applications without being required to open-source your own code, as long as the original copyright notice is included.

This ensures that the project remains a true open-source public good, fostering an open ecosystem for everyone.

---

## 💡 About this Project

Why this repository exists, in one honest sentence: curiosity — some of these questions interest me intrinsically, and they don't let go.

**Note:** This entire repository is conceived as a *thought experiment* developed by Frank Peterlein in collaboration with AI. It is primarily a space to capture, explore, and run simulations on complex ideas. Because it's a living, experimental space, it may contain errors or untested hypotheses. Feedback, discussions, and corrections are always welcome!

---

## 🔬 Scientific Status

This repository operates at the intersection of **computational complexity science** (established), **systems theory** (established), and **AI consciousness research** (emerging / contested).

Claims in this repository have different epistemic statuses:

| Claim Type | Examples | Status |
|:-----------|:---------|:-------|
| Computational demonstrations | Kuramoto synchronization, Bak's Sandpile power laws | ✅ Well-established |
| Measurable hypotheses | Δ-Kohärenz, 3-Layer Memory coherence | 🧪 Testable — see `lab/AGENTIC_README.md` |
| Theoretical frameworks | Markov Blanket as agent-human boundary, Free Energy alignment | 📐 Formalized — see `theory/core/mathematical-axioms.md` |
| Open problems | The Mirror Problem, bootstrapping of identity | ❓ Unresolved — see `theory/reference/open-problems.md` |
| Speculative framings | Relational emergence, criticality as intelligence zone | 💭 Speculative — see `theory/reference/glossary.md` for definitions |

We believe intellectual honesty about these distinctions makes the project *more* interesting, not less. The open problems are the most generative part.

---

## 📂 Repository Overview

To keep this repository coherent while it grows, use this practical split:

- **`book/`** = curated reading path ("online book")
- **`papers/` + `docs/papers/`** = publication-style outputs (compact, citable, less narrative)
- **`theory/`** = formal and semi-formal theory essays
- **`logs/`** = architectural journals (applied, speculative system design notes)
- **`fiction/`** = narrative thought experiments constrained by theory
- **`simulation-models/` + `lab/`** = executable artifacts, orchestration framework, and reusable primitives

If you're unsure where new material belongs, see **[`meta/repository-meta/repository-information-architecture.md`](meta/repository-meta/repository-information-architecture.md)**.

| Folder | Purpose |
| :--- | :--- |
| **`docs/`** | The curated reading path, MkDocs build resources, and the complete "Online Book". |
| **`fiction/`** | 🎬 **The Narrative Synthesis**: Hard Sci-Fi "found footage" translating the math into stories. |
| **`lab/`** | The unified Python ecosystem. Contains the Multi-Paradigm Orchestrator (`orchestration/`), the empirical Agentic Identity Suite (`experiments/`), the inverse-reconstruction benchmark and cognitive stress tests (`benchmarks/`), info-theoretic tools (`data-analysis/`), and reusable primitives (`core/`). |
| **`logs/`** | Architecture logs: applied design notebooks bridging abstract theory and deployment constraints. |
| **`meta/`** | Reflections on epistemology, ethics, repository governance, and the limits of formal systems and computation. |
| **`papers/`** | Paper-style synthesis documents with an academic framing and tighter scope. |
| **`simulation-models/`** | Isolated toy models, clustered by theme (emergent-dynamics, cognitive-architectures, etc.). |
| **`theory/`** | Conceptual notes and essays on systems, intelligence, and emergent behavior. |

Each subfolder contains its own README with context and details.

### 🔍 Full Index

The complete index of simulations, theory essays, fiction stress tests, lab frameworks, and architecture logs lives on the **[live site](https://frnkptrln.github.io/systems-and-intelligence)** — it stays current automatically with the repository. This README intentionally does not duplicate it.

Entry points by interest:

- **Plain language:** [The Snow Story](meta/repository-meta/the-snow-story.md) — the whole project told so that a child can follow it, with every paragraph pointing back to its instruments.
- **Theory:** [The Generator Question](theory/core/the-generator-question.md) (start here) → [Emergence Manifesto](theory/core/emergence-manifesto-v1.3.md) → [Trace to Generator](theory/emergence/trace-to-generator.md).
- **Measured core:** [Inverse-Reconstruction Benchmark](lab/benchmarks/inverse-reconstruction/README.md) — the spine's asymmetry as curves: where inversion is cheap and where it walls; equivalence classes counted and collapsed; the search wall; Occam's world-dependent payoff; the optimizer's curse, its cure, and the closed loop. Runs in seconds, `numpy` only.
- **Runnable code:** [Simulation → Theory Map](theory/core/simulation-theory-map.md) lists all 35 simulations with their direction (Forward / Inverse / Both) and the wall they touch.
- **Lab:** [Agentic Identity Suite](lab/AGENTIC_README.md), [LLM provider layer](lab/providers/README.md), [Identity Persistence (Pstrong)](lab/metrics/persistence_scores.py).
- **Fiction:** [Narrative dossiers](fiction/README.md) — each entry annotated with the theory claim it stress-tests.

### 📡 Interactive Tools

- [**Web Emergence Explorer**](lab/tools/web-explorer/README.md) – Browser-based Game of Life with real-time entropy, spatial mutual information, and complexity charts. Zero dependencies.
- [**SII Dashboard**](lab/data-analysis/sii_dashboard.py) — Quantitative System Intelligence Index: runs headless mini-simulations and generates comparative radar/bar charts of P, R, A, IP dimensions.
- [**Identity Morphospace**](lab/tools/morphospace_visualizer.py) — Plots agent trajectories in Persistence/Coherence space, visualizing the Chord vs. Arpeggio regimes.

---

## 🚀 Getting Started

Clone the repository and install dependencies:

```bash
git clone https://github.com/frnkptrln/systems-and-intelligence.git
cd systems-and-intelligence
pip install -r requirements.txt
```

Some simulations use optional ML dependencies (e.g. PyTorch). Install them with:

```bash
pip install -r requirements-ml.txt
```

Then run any simulation:

```bash
cd simulation-models/emergent-dynamics/lenia
python3 lenia.py
```

Press `ESC` in any simulation window to exit.

---

## 🗺 Conceptual Map

For a guide to how all the models connect, see
[Conceptual Map](theory/core/conceptual-map.md) – the conceptual map
that traces the arc from self-organization through learning to
system intelligence and its limits.
