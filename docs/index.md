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
<span class="stat-number">Run</span>
<span class="stat-label">Simulation Models</span>
</div>
<div class="stat" markdown>
<span class="stat-number">10</span>
<span class="stat-label">Reader Nodes</span>
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
 
!!! success "TL;DR"
    **The thesis: AI alignment is better modeled as a problem of applied thermodynamics and systems engineering than as one of psychology or moral training.**

    The argument is that "friendlier" prompt engineering or moral training may not be enough, because unbounded optimization *tends to* outrun the entropy limits of the layer it runs on. The framework proposes that durable alignment needs *structural* constraints, not only behavioral ones:

    1. **Action Budgets** to bound entropy production.
    2. **Impedance Matching** (artificial latency) to bridge silicon speed and human cognitive speed.
    3. **The Substrate Veto** enforced at the protocol layer.

    This repository develops that case end-to-end — from entropy limits to runnable Python engines — as an **open thesis**, not a finished proof.

!!! note "Epistemic status — read this first"
    This is an **open thesis**: working drafts and *falsifiable hypotheses*, not established results. The central necessity result is a modest theorem (the conjunction of three constraints); **sufficiency is conjectured, not proved**; the civilizational mapping is **heuristic**, not measured; and the AI-specific predictions have **not** yet been tested on real LLM agents. Claims throughout are tagged — *demonstrated / formal / conjecture / hypothesized / heuristic / open problem*. The flagship paper, *The Viable Corridor*, is a **working draft (not submission-ready)**. The explicit negative space is maintained at [What This Project Does NOT Claim](theory/reference/what-this-project-does-not-claim.md).

!!! abstract "Thesis"
    **Intelligence is an emergent property of continuous dynamical systems**, not a discrete function of next-token prediction. The same mathematics that governs flocking birds, oscillating neurons, and self-organizing criticality also governs the "values" and "goals" that arise inside Large Language Models — and inside human civilizations.

We probe this not with philosophy alone, but with runnable simulations testing mathematical models from the theory. Evolutionary game theory, nonlinear dynamics, and thermodynamic control theory are all unified under a single mathematical framework: the **Thermodynamics of Emergent Orchestration (TEO)**.

---

## Navigate the Research

<div class="grid-cards" markdown>

<div class="card" markdown>

### :material-compass: Recommended Reading Path

New to this project? Start here for the most direct path through the core theory and proofs.

1. **[The Generator Question](theory/core/the-generator-question.md)** — The organizing question; forward vs. inverse asymmetry; the three walls.
2. **[Emergence Manifesto](theory/core/emergence-manifesto-v1.3.md)** — The core claim set (emergence).
3. **[Optimization and Its Blindness](theory/optimization/optimization-and-its-blindness.md)** — The hinge: why unconstrained optimization is non-viable, and how capability loads multiple constraints at once.
4. **[TEO Framework](theory/teo-framework/README.md)** — The constraint-architecture model.
5. **[The Viable Corridor](papers/viable-corridor.md)** — The formal synthesis (a stabilized *node*, not the whole project).
6. **[Canonical Path v2](meta/repository-meta/canonical-path-v2.md)** — The full map of the arc.

</div>

<div class="card" markdown>

### :material-book-open-variant: The Book

The curated book and course path. From local emergence to civilizational dynamics, each major claim links back to runnable code or an explicit open problem.

[Start reading →](book/00_introduction.md)

</div>

<div class="card" markdown>

### :material-flask: Core Theories

The formal essays. Emergence Manifesto, TEO framework, Black Swan dynamics, and an honest self-assessment.

[Explore theories →](theory/core/emergence-manifesto-v1.3.md)

</div>

<div class="card" markdown>

### :material-code-braces: Simulations

<p class="si-feature-description">Runnable simulations: Boids, Kuramoto, SOC, Lenia, IFS, L-systems, TEO Civilization, Identity Morphospace, and more.</p>

[Run the code →](simulation-models/alignment-and-veto/utility-engineering/README.md)

</div>

<div class="card" markdown>

### :material-chart-line: The Measured Core

The inverse-reconstruction benchmark: the spine's asymmetry as curves. Equivalence classes counted and collapsed, the search wall, Occam's world-dependent payoff, the optimizer's curse, its cure — and the closed loop. Every claim runs in seconds.

[Run the benchmark →](lab/benchmarks/inverse-reconstruction/README.md)

</div>

<div class="card" markdown>

### :material-file-document: The Papers

*The Viable Corridor* — the flagship formal synthesis (constraint architecture + capability loading; a **working draft**). Its empirical companion is *Quantifying Emergent Utility & Stability in Multi-Agent LLM Ecosystems*.

[Read the Viable Corridor →](papers/viable-corridor.md)

</div>

<div class="card" markdown>

### :material-book-open-page-variant: Sci-Fi Synthesis

Narrative stress tests that make abstract theoretical constraints visible in lived, emotional scenarios.

[Read the Fiction →](fiction/README.md)

</div>

</div>

---

## What's Next

!!! info "The framework is drafted, not closed. The next step is external contact, not deployment."
    The TEO framework and the Viable Corridor paper are at **working-draft** stage: the necessity result holds, but **sufficiency is unproven**, and the model's claims have been demonstrated only *in-model*, not against real systems. The honest next step is **external review and empirical contact** — not hardware or deployment.

**Near-term — the real frontier:**

1. **External review** of the Viable Corridor paper (§5–§8 have not yet had a critical dynamical-systems read).
2. **Empirical LLM auditing** `[OPEN PROBLEM]` — running the Agentic Identity Suite against live APIs to test the AI-specific predictions (P7/P8) on *real* agents, not synthetic ones.
3. **Rigorous sufficiency** `[OPEN PROBLEM]` — constructing $\gamma_c$ and a proper open-set test, rather than single-trajectory evidence.

**Speculative / long-horizon** `[SPECULATIVE]` — directions the framework *suggests* but does not yet support:

- Hardware prototyping (analog / memristor circuits for physical $\gamma$-pin vetoes).
- Protocol-level "Substrate Veto" specifications for decentralized governance systems.

If you want to contribute, the project is open for: critical **review** of the framework and the necessity result; **pull requests** extending the simulations or the Agentic Identity Suite; or sharpening any **open problem**.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/frnkptrln/systems-and-intelligence.git
cd systems-and-intelligence

# Run the TEO Civilization Simulation
python simulation-models/alignment-and-veto/teo-civilization/teo_simulation.py

# Run the Black Swan Resilience Simulation
python simulation-models/alignment-and-veto/black-swan-resilience/black_swan_simulation.py

# Serve this book locally
pip install mkdocs-material python-markdown-math
mkdocs serve
```

---

!!! tip "Living Document"
    This repository is a *thought experiment* developed by Frank Peterlein in collaboration with AI. It is a space to capture, explore, and formalize ideas about emergent intelligence — kept going by nothing grander than curiosity: the wish to understand, maybe, *was die Welt im Innersten zusammenhält*. Feedback, corrections, and discussions are always welcome.
