# 🧠 Systems & Intelligence

<div class="hero-banner" markdown>

## A Research Notebook on Generators, Intelligence, and Viability

*How systems produce traces, how observers reconstruct them, and how optimization remains survivable.*

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

## The Core Questions
 
!!! success "TL;DR"
    This repository studies two connected questions:

    1. **Epistemic spine:** How can an observer move from a trace to a useful generator — through construction, world-coupling, intervention, and revision?
    2. **Viability arc:** How can an optimizing system remain viable when growing capability loads several constraints at once?

    The first is folded into [From Trace to World-Binding](theory/core/from-trace-to-world-binding.md). The second is mapped in [Canonical Path v2](meta/repository-meta/canonical-path-v2.md). They share a root in emergence, but neither replaces the other.

!!! note "Epistemic status — read this first"
    This is a **research notebook**, not a theory of everything. The inverse-reconstruction results are measured in small, controlled systems. The Viable Corridor necessity result is conditional on its model assumptions; **sufficiency is conjectured, not proved**; the civilizational mapping is **heuristic**, not measured; and the AI-specific predictions have not been tested on real agent ecologies. Claims throughout are tagged — *demonstrated / formal / conjecture / hypothesized / heuristic / open problem*. The flagship paper, *The Viable Corridor*, remains a **working draft (not submission-ready)**. The explicit negative space is maintained at [What This Project Does NOT Claim](theory/reference/what-this-project-does-not-claim.md).

The measured core is the [inverse-reconstruction benchmark](lab/benchmarks/inverse-reconstruction/README.md): known-family inversion, equivalence classes, intervention, family search, model exploitation, marked uncertainty, closed-loop revision, ensembles, and generator composition. The Viability Arc is currently supported by formal results and two synthetic models; external calibration and real-agent tests remain open.

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
    The strongest current artifacts are controlled toy experiments and synthetic models. The next phase should test their boundaries against learned systems, external baselines, and critical review.

**Near-term — the real frontier:**

1. **Learned searchers vs. the family-search floor** — give LLMs or program synthesizers the same partial traces and query budgets as the exact CA baseline; pre-register consistency, truth recovery, description size, support violations, and cost.
2. **External review of the Viable Corridor** — freeze the paper's conceptual scope while its dynamical assumptions, sufficiency gap, and empirical mapping receive a critical read.
3. **Rigorous sufficiency** — replace single-trajectory evidence with open-set tests and, if possible, construct or bound \(\gamma_c\).
4. **Separate the real-model questions correctly** — live Agentic Identity Suite runs test Mirror/Chord/binding claims; P7/P8 require a distinct real-agent ecology with hard/soft budgets and independently varied constraint architecture.
5. **Co-stabilization after v1.9** — the substitution-coupled ring produced dependency cascades but failed the resilience prediction. Test a redundancy model across topology, size, viability threshold, and coupling resolution before treating mutual maintenance as measured.

**Speculative / long-horizon** `[SPECULATIVE]`:

- Hardware prototyping (analog / memristor circuits for physical \(\gamma\)-pin vetoes).
- Protocol-level "Substrate Veto" specifications for decentralized governance systems.

If you want to contribute, the project is open for critical **review**, preregistered **experiments**, external **baselines**, and corrections to any claim that exceeds its evidence.

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
    This repository is a *thought experiment* developed by Frank Peterlein in collaboration with AI. It is a space to capture, explore, and formalize ideas about emergent intelligence — kept going by nothing grander than curiosity. Feedback, corrections, and discussions are always welcome.
