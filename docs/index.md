<div class="hero-banner" markdown>

<p class="eyebrow">Systems &amp; Intelligence · a research notebook · Berlin · 2024–2026</p>

# Some traces have causes. Not all causes can be recovered.

*What follows from a process model, what evidence can identify, and how optimization stays survivable.* Frank Peterlein, independent research.

[Start here :material-arrow-right:](synthesis.md){ .md-button .md-button--primary }
[Source repository](https://github.com/frnkptrln/systems-and-intelligence){ .md-button }

</div>

!!! note "Epistemic status — read this first"
    This is a **research notebook**, not a theory of everything. The process foundation is established mathematics rather than a novel empirical theory. Identity remains test-relative; learning and intelligence require declared tasks; phenomenal consciousness is not derived. The inverse-reconstruction results are measured in small, controlled systems. The Viable Corridor necessity result is conditional on its model assumptions; **sufficiency is conjectured, not proved**; the civilizational mapping is **heuristic**, not measured; and the AI-specific predictions have not been tested on real agent ecologies. The explicit negative space is maintained at [What This Project Does NOT Claim](../theory/reference/what-this-project-does-not-claim.md).

## Two bounded questions

The notebook begins with a foundational audit and then studies two questions:

1. **Model identification** — how an observer moves from traces to useful candidate process models, through construction, world-coupling, intervention, and revision.
2. **The viability arc** — how an optimizing system stays viable when growing capability loads several constraints at once.

The [Foundations Reconstruction](../theory/core/mathematical-axioms.md) establishes the common process language and shows where extra assumptions enter. The first question is folded into [From Trace to World-Binding](../theory/core/from-trace-to-world-binding.md); the second is mapped in [Canonical Path v2](../meta/repository-meta/canonical-path-v2.md).

The measured core is the [inverse-reconstruction benchmark](../lab/benchmarks/inverse-reconstruction/README.md): known-family inversion, equivalence classes, intervention, family search, model exploitation, marked uncertainty, closed-loop revision, ensembles, and process composition. The viability arc rests on formal results and two synthetic models; external calibration and real-agent tests remain open.

## Six ways in

Not a prescribed path. The same material, entered from different angles.

<div class="doors" markdown>

<div class="door" markdown>

<p class="door-meta">01 / Theory</p>

### The argument

The reconstructed foundation first, then the formal and exploratory essays it constrains — emergence, identity, veto, computation.

[Enter the theory →](../theory/README.md)

</div>

<div class="door door--blue" markdown>

<p class="door-meta">02 / The route</p>

### One thing after another

A compact linear path for readers who want a sequence rather than a map. The earlier book chapters predate the foundations audit and stay in the repository.

[Start with *From Rule to Mind* →](../book/09_from_rule_to_mind.md)

</div>

<div class="door door--warm" markdown>

<p class="door-meta">03 / Papers</p>

### The formal core

*The Viable Corridor* — constraint architecture and capability loading, a working draft, available as PDF. Its empirical companion measures utility and stability in multi-agent LLM ecologies.

[Read the Viable Corridor →](../papers/viable-corridor.md)

</div>

<div class="door" markdown>

<p class="door-meta">04 / Lab</p>

### What runs

The benchmark results behind the measured claims — every one reproducible in seconds. The simulations themselves (Boids, Kuramoto, SOC, Lenia, IFS, L-systems, TEO Civilization) live with their code in the repository.

[Run the benchmark →](../lab/benchmarks/inverse-reconstruction/README.md)

</div>

<div class="door door--warm" markdown>

<p class="door-meta">05 / Stories</p>

### Narrative stress tests

Nineteen scenarios that put abstract constraints into lived situations, where they can be felt rather than only checked.

[Read the fiction →](../fiction/README.md)

</div>

<div class="door door--blue" markdown>

<p class="door-meta">06 / Thinking space</p>

### Unfinished questions

Encounters, contradictions, and probes that stay open without promising to become canonical claims.

[Enter the thinking space →](thinking-space.md)

</div>

</div>

## The recommended reading path

New to the project? This is the most direct route through the core theory and results.

1. **[Foundations Reconstruction](../theory/core/mathematical-axioms.md)** — minimal primitives, axioms, derivations, counterexamples, and comparison with neighboring theories.
2. **[From Trace to World-Binding](../theory/core/from-trace-to-world-binding.md)** — the bounded model-identification loop.
3. **[Inverse-Reconstruction Benchmark](../lab/benchmarks/inverse-reconstruction/README.md)** — the measured equivalence classes and intervention results.
4. **[Emergence Manifesto](../theory/core/emergence-manifesto-v1.3.md)** — the earlier emergence claim set, read under the reconstructed foundation.
5. **[Optimization and Its Blindness](../theory/optimization/optimization-and-its-blindness.md)** — the hinge into the viability arc.
6. **[The Viable Corridor](../papers/viable-corridor.md)** — one conditional formal model, also available as a PDF.

If you would rather start from a story than from an axiom, [The Snow Story](../meta/repository-meta/the-snow-story.md) carries the whole argument at any age.

This site publishes about seventy pages. The repository behind it holds more than three times that — simulation code, architecture logs, working notes, and essays that are not finished enough to ask anyone to read in order. [What stays in the repository](repository-map.md) says what is where, and why.

## What's next

!!! info "The framework is drafted, not closed. The next step is external contact, not deployment."
    The strongest current artifacts are controlled toy experiments and synthetic models. The next phase should test their boundaries against learned systems, external baselines, and critical review.

**Near-term — the real frontier:**

1. **Learned searchers vs. the family-search floor** — give LLMs or program synthesizers the same partial traces and query budgets as the exact CA baseline; pre-register consistency, truth recovery, description size, support violations, and cost. *The [task protocol is frozen](../lab/benchmarks/learned-searcher/README.md); whether to run it, and against which exact model, remains deliberately unregistered.*
2. **External review of the Viable Corridor** — freeze the paper's conceptual scope while its dynamical assumptions, sufficiency gap, and empirical mapping receive a critical read.
3. **Rigorous sufficiency** — replace single-trajectory evidence with open-set tests and, if possible, construct or bound $\gamma_c$.
4. **Separate the real-model questions correctly** — live Agentic Identity Suite runs test Mirror/Chord/binding claims; P7/P8 require a distinct real-agent ecology with hard/soft budgets and independently varied constraint architecture.
5. **Separate selection from drift after cost relocation** — v1.13's local group funding nearly
   removes selection against support and suppresses seeded cheaters, but it does not meet the
   retention criterion and makes within-group variation nearly cost-neutral. The next discriminating
   arm should introduce a measurable within-group cost gradient without changing the matched group
   budget.

**Speculative / long-horizon** `[SPECULATIVE]`:

- Hardware prototyping (analog / memristor circuits for physical $\gamma$-pin vetoes).
- Protocol-level "Substrate Veto" specifications for decentralized governance systems.

If you want to contribute, the project is open for critical **review**, preregistered **experiments**, external **baselines**, and corrections to any claim that exceeds its evidence.

## Run it yourself

```bash
# Clone the repository
git clone https://github.com/frnkptrln/systems-and-intelligence.git
cd systems-and-intelligence

# Run the TEO Civilization Simulation
python simulation-models/alignment-and-veto/teo-civilization/teo_simulation.py

# Run the Black Swan Resilience Simulation
python simulation-models/alignment-and-veto/black-swan-resilience/black_swan_simulation.py

# Serve this notebook locally
pip install -r requirements-docs.txt
mkdocs serve
```

!!! tip "Living document"
    A thought experiment developed by Frank Peterlein in collaboration with AI — a space to capture, explore, and formalize ideas about emergent intelligence, kept going by nothing grander than curiosity. Feedback, corrections, and discussions are always welcome.
