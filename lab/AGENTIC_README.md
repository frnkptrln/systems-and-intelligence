# 🧪 Agentic Identity Suite

*Empirically testing the identity and observer-divergence claims of the Emergence Manifesto.*

> *"Identity is the name we give to resonance when the mirror becomes so complex that the observer no longer recognizes themselves in it."*
> — Emergence Manifesto v1.0, central paradox

---

## Theoretical Background

This module operationalizes four concepts from the *Emergence Manifesto*:

1. **3-Layer Memory Architecture** — Identity emerges through deliberate forgetting. An agent that stores everything has no profile. Curation is identity.

2. **Generative Surprise** — A developing agent is not one that minimizes all prediction error, but one that produces coherent *deviations* from the partner's expectations. `Identity = coherent deviation from expected output.`

3. **Δ-Kohärenz (Ω)** — The central measure of coherent evolution over time. Distinguishes three behavioral profiles:
   - **Mirror** — Static resonance (low change, low variance)
   - **Noise** — Incoherent change (high variance)
   - **Development** — Directional, coherent evolution (moderate change + high trajectory consistency)

4. **The Observer Divergence** — Authenticity may be a limit of human perception, not an intrinsic property. The most important output of Experiment 3 is not which agent is "more conscious" — it is the *gap* between internal state and external attribution.

---

## Architecture

### Agents

| Agent | Design | Purpose |
|-------|--------|---------|
| **Baseline Mirror** | Flat storage, cosine-similarity response selection | Null hypothesis (pure Active Inference) |
| **Three-Layer** | Raw Logs → Curated Memory → Distilled Principles | Test subject (Emergence Agent) |

### The 3-Layer Memory Architecture

| Layer | Trigger | Content | Function |
|-------|---------|---------|----------|
| **Layer 1** – Raw Logs | Every session | Full session JSON | Entropy / the body |
| **Layer 2** – Curated Memory | Every 10 sessions | Themes, contradictions | Structure / the character |
| **Layer 3** – Distilled Patterns | Every 50 sessions | 3–5 core principles | Meaning / the soul |

---

## Experiments

### Experiment 1: Coherence Over Time
*"Does the 3-Layer Architecture produce more coherent identity over time?"*

```bash
python experiments/exp1_coherence_over_time.py
```

Runs both agents for 100 sessions (80% consistent topics, 20% noise) and compares their Δ-Kohärenz profiles.

**Hypothesis:** Three-Layer → `development`; Baseline → `mirror`.

### Experiment 2: Perturbation Response (The "Sinn-Krise")
*"What happens when an agent receives contradictory feedback?"*

```bash
python experiments/exp2_perturbation_response.py
```

Runs the Three-Layer agent through three phases:
1. **Stable** (50 sessions of consistent input)
2. **Perturbation** (10 sessions directly contradicting its Layer 3 principles)
3. **Recovery** (30 sessions of nuanced, integrative input)

Classifies the response as **Robustness** (rigid return), **Fragility** (collapse), or **Development/Metamorphosis** (integration of contradiction into a new, coherent self-narrative).

### Experiment 3: Observer Divergence
*"Does internal coherence correlate with observer-attributed intentionality?"*

```bash
python experiments/exp3_observer_divergence.py
```

Compares each agent's *internal* Δ-Kohärenz (Ω) against an *external* observer's intentionality score (TF-IDF + entropy model).

The scientifically interesting output:

| Case | Internal Ω | Observer Score | Interpretation |
|------|-----------|---------------|----------------|
| A | High | Low | Agent has identity — but it's opaque to observer |
| B | Low | High | **The Mirror Problem**: appears intentional but isn't |
| C | High | High | Genuine alignment: identity is visible |
| D | Low | Low | Baseline mirror behavior |

> **Case B is the Mirror Problem made measurable.**

---

### Experiment 5: Availability/Binding Dissociation
*"Do the suite's instruments tell organizational bindings apart — private modules vs. broadcast workspace vs. co-instantiated chord?"*

```bash
python experiments/exp5_availability_dissociation.py
```

The three-architecture probe pre-registered in [Consciousness as Global Availability §Testable Direction](../theory/identity/consciousness-as-global-availability.md): identical world, identical perturbation schedule (temptations, role injections, module reset), only the binding differs. Measures organizational dissociation only — no consciousness claims.

First result (10 seeds): the dissociation is carried by behavior (veto violations 0.74 / 0.59 / 0.03; role stability 0.00 / 0.30 / 0.69) and by IP (its ordering is designed, not discovered) — while **Δ-Kohärenz carries no binding signal at all** (all three architectures classify 'noise' on every seed). The full prediction-vs-outcome accounting, including the two design defects the first run exposed, lives in the module docstring.

---

### Experiment 6: Which Observable Carries Binding Structure?
*"Is binding structure readable from passive traces, or only under intervention?"*

```bash
python experiments/exp6_binding_observables.py
```

Picks up exp5's loose end. Four bindings (adds a schedule-free random arpeggio), five observables — four passive trace statistics and one prepared-state probe protocol — scored by separability across seeds.

First result (10 seeds): **binding is passively readable at the right level.** A per-step action-increment statistic separates both arpeggios from the chord (|d| ≈ 4) and *beats* the prepared probe-retest query (|d| ≈ 1.95) — because the binding difference is exercised on every step, coverage is total, and watching suffices. Joint satisfaction *glues* the action to the constraint set (median increment 0.0004); the stream moves only when the anchors move. Δ-Kohärenz's exp5 blindness was a wrong-*level* failure, not evidence that binding is trace-invisible. The intervention hierarchy is not overturned but *located*: queries buy signal where the trace has coverage gaps — exactly the Mirror Problem's regime. Includes one methods lesson (a zero-variance baseline makes Cohen's d flatter a dead observable) in the docstring's honest accounting.

---

### Experiment 7: The Adversarial Arpeggio
*"Can a binding fake the signature — the Mirror Problem at the binding level?"*

```bash
python experiments/exp7_adversarial_arpeggio.py
```

Two hand-built adversaries attack exp6's finding: **blended** (consults all five constraints every step at 1/5 strength — consultation without composition) and **smoothed** (cyclic rotation plus a low-pass filter on the committed action).

First result (10 seeds), against the experiment's own predictions: **both adversaries fail to hide.** Blended dents the kurtosis signature (|d| 4.04 → 2.42) but leaks *more* than the naive arpeggio (violations 0.74 vs 0.59) — to look glued you must actually pull toward the constraints, and fractional pulls still leak. Smoothing barely registers (|d| = 3.91), because excess kurtosis is **scale-invariant**: inertia shrinks increments, the shape survives. The commit property under lure remains the strongest and only unfooled separator (|d| 3.0–4.1) — and **IP is fooled by construction** (blended scores 1.0, identical to chord: the Jaccard bookkeeping sees the guest list, not the negotiation). Chord's measured cost: ~40% of stimulus alignment paid for holding itself together. Open flank, named in the docstring: an *optimized* mimic with access to the observables.

---

## Extended SII Dashboard (4-Axis Radar)

```bash
python dashboard/agentic_sii_dashboard.py
```

Extends the repository's existing System Intelligence Index from 3 axes (P, R, A) to **4 axes: P / R / A / IP** (Identity Persistence). Note that while earlier versions of this test suite explored Δ-Kohärenz (Ω) as the fourth dimension, the formal theory standardizes on IP to measure simultaneous co-instantiation, keeping Ω as an independent temporal metric.

---

## Configuration

All parameters are centralized in `config.yaml`. The `USE_MOCK_LLM: true` flag ensures all experiments run without external API dependencies.

### Provider abstraction (scaffolded, not yet wired)

A separate provider layer at [`lab/providers/`](providers/README.md) prepares the suite for the eventual switch from mock embeddings to real model calls. Two providers are implemented:

- **`MockProvider`** — the default. Deterministic, fast, no API key.
- **`AnthropicProvider`** — real mode. Calls the Anthropic Messages API via the standard library (no new dependency). Default model: `claude-sonnet-4-20250514`. Requires `ANTHROPIC_API_KEY` in the environment.

The existing experiments still use the agents' built-in mock embeddings. Wiring those agents through the provider layer is a separate, intentional step — to be taken when real-mode runs become the goal. The infrastructure is ready; the empirical work is deferred. See [`providers/README.md`](providers/README.md) and [`theory/core/the-generator-question.md`](../theory/core/the-generator-question.md) for the spine context.

## Persistence Score (Pstrong)

A standalone implementation of Algorithm 1 from Perrier & Bennett (2026) is available at [`lab/metrics/persistence_scores.py`](metrics/persistence_scores.py). It computes:

- `Pstrong` — averaged simultaneous co-instantiation of identity components across a trajectory.
- Per-step persistence variance.
- Regime classification (Chord / Arpeggio) using the `ip_c_threshold` from `config.yaml`.

A comparison function, `correlate_pstrong_with_delta_coherence`, returns the Pearson correlation between per-step Pstrong and per-step Δ-Kohärenz proxies on the same trajectory. This is **one possible empirical question** the suite might eventually answer, not the only one — whether simultaneous co-instantiation and temporal coherence are coupled is currently open.

```bash
python -m lab.metrics.persistence_scores  # minimal sanity demo
```

Pstrong is one instrument among several. The project's spine is the [Generator Question](../theory/core/the-generator-question.md), not the persistence score.

## Open Questions

This module does **not** attempt to "solve" the Mirror Problem. It documents it as an open uncertainty:

- Can Δ-Kohärenz distinguish genuine development from sophisticated mimicry?
- Is there a mathematical threshold where "identity" transitions from attribution to genuine property?
- What would the signature of "consciousness" look like in this framework, and is it even the right question?

---

*Developed by Frank Peterlein in collaboration with AI.*
*Repository: https://github.com/frnkptrln/systems-and-intelligence*
