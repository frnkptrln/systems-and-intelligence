# 🧠 Systems & Intelligence

<div class="hero-banner" markdown>

## An Open Thesis on Emergent Intelligence

*How local rules create global minds — and how we can steer them.*

**Frank Peterlein** · Independent Research · 2024–2026

[Read the Book :material-book-open-variant:](book/00_introduction.md){ .md-button .md-button--primary }
[View on GitHub :fontawesome-brands-github:](https://github.com/frnkptrln/systems-and-intelligence){ .md-button }

</div>

<div class="stats-bar" markdown>
<div class="stat" markdown>
<span class="stat-number">35</span>
<span class="stat-label">Simulation Models</span>
</div>
<div class="stat" markdown>
<span class="stat-number">7</span>
<span class="stat-label">Book Chapters</span>
</div>
<div class="stat" markdown>
<span class="stat-number">4</span>
<span class="stat-label">ODE Paradigms</span>
</div>
<div class="stat" markdown>
<span class="stat-number">1</span>
<span class="stat-label">Empirical Audit</span>
</div>
</div>

---

## The Core Claim
 
!!! success "TL;DR (The Grand Synthesis)"
    **AI Alignment is not a psychological problem—it is a problem of applied thermodynamics and systems engineering.**

    If we want to build safe, super-scaling artificial intelligence, we cannot rely on "friendlier" prompt engineering or moral training. Unbounded intelligence will always structurally crash the biological layer's entropy limits. True alignment requires hard, irreversible architectural constraints:

    1. **Action Budgets** to limit AI entropy production.
    2. **Impedance Matching** (artificial latency) to bridge the microsecond-speed of silicon and the slow cognitive speed of humans.
    3. **The Substrate Veto** hard-coded into the protocol layer of our digital state.

    This repository is the complete architectural manifesto—from cosmological entropy limits down to runnable Python engines—proving that safety must be enforced structurally.

!!! abstract "Thesis"
    **Intelligence is an emergent property of continuous dynamical systems**, not a discrete function of next-token prediction. The same mathematics that governs flocking birds, oscillating neurons, and self-organizing criticality also governs the "values" and "goals" that arise inside Large Language Models — and inside human civilizations.

We prove this not with philosophy alone, but with **35 Python simulations** verifying mathematical models from the theory. Evolutionary game theory, nonlinear dynamics, and thermodynamic control theory are all unified under a single mathematical framework: the **Thermodynamics of Emergent Orchestration (TEO)**.

---

## Navigate the Research

<div class="grid-cards" markdown>

<div class="card" markdown>

### :material-book-open-variant: The Book

The 7-part narrative thesis. From local emergence to civilizational dynamics, every claim backed by runnable code.

[Start reading →](book/00_introduction.md)

</div>

<div class="card" markdown>

### :material-flask: Core Theories

The formal essays. Emergence Manifesto, TEO framework, Black Swan dynamics, and an honest self-assessment.

[Explore theories →](theory/emergence-manifesto-v1.2.md)

</div>

<div class="card" markdown>

### :material-code-braces: Simulations

35 Python simulations: Boids, Kuramoto, SOC, Lenia, TEO Civilization, Identity Morphospace, and more.

[Run the code →](simulation-models/utility-engineering/README.md)

</div>

<div class="card" markdown>

### :material-file-document: The Paper

*Quantifying Emergent Utility & Stability in Multi-Agent LLM Ecosystems.* The formal academic summary.

[Read the paper →](papers/quantifying-emergent-utility-in-llms.md)

</div>

</div>

---

## What's Next (2026 Roadmap)

!!! info "Where this project is going next"
    This is an active research program. The current focus is not only to **add more models**, but to **tighten falsifiability**, increase reproducibility, and connect abstract theory to measurable interventions.

1. **Reproducibility baseline:** standard run profiles, fixed seeds, and benchmark outputs for core simulations.
2. **Cross-model comparability:** shared metrics (stability, entropy budget, identity persistence) across all simulation families.
3. **Interactive diagnostics:** richer browser-based explorers for attractor landscapes and regime transitions.
4. **Theory-to-policy bridge:** clearer translation from formal constraints (TEO, substrate veto) into institutional design patterns.

If you want to contribute, start with:

- adding tests for an existing simulation module,
- improving one documentation chapter with explicit equations + runnable code,
- or opening an issue that proposes a falsifiable counterexample to a core claim.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/frnkptrln/systems-and-intelligence.git
cd systems-and-intelligence

# Run the TEO Civilization Simulation
python simulation-models/teo-civilization/teo_simulation.py

# Run the Black Swan Resilience Simulation
python simulation-models/black-swan-resilience/black_swan_simulation.py

# Serve this book locally
pip install mkdocs-material python-markdown-math
mkdocs serve
```

---

!!! tip "Living Document"
    This repository is a *thought experiment* developed by Frank Peterlein in collaboration with AI. It is a space to capture, explore, and formalize ideas about emergent intelligence. Feedback, corrections, and discussions are always welcome.
