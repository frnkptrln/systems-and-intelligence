# 🧪 Agentic Test Suite

*Empirically testing the theoretical claims of the Emergence Manifesto v1.0.*

> *"Identity is the name we give to resonance when the mirror becomes so complex that the observer no longer recognizes themselves in it."*
> — Emergence Manifesto v1.0, central paradox

---

## Theoretical Background

This module operationalizes four concepts from the *Emergence Manifesto v1.0*:

1. **3-Layer Memory Architecture** — Identity emerges through deliberate forgetting. An agent that stores everything has no profile. Curation is identity.

2. **Generative Surprise** — A developing agent is not one that minimizes all prediction error, but one that produces coherent *deviations* from the partner's expectations. `Identity = coherent deviation from expected output.`

3. **Δ-Kohärenz (Ω)** — The fourth SII dimension. Distinguishes three behavioral profiles:
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

## Extended SII Dashboard (4-Axis Radar)

```bash
python dashboard/agentic_sii_dashboard.py
```

Extends the repository's existing System Intelligence Index from 3 axes (P, R, A) to **4 axes: P / R / A / Ω**.

---

## Configuration

All parameters are centralized in `config.yaml`. The `USE_MOCK_LLM: true` flag ensures all experiments run without external API dependencies.

## Open Questions

This module does **not** attempt to "solve" the Mirror Problem. It documents it as an open uncertainty:

- Can Δ-Kohärenz distinguish genuine development from sophisticated mimicry?
- Is there a mathematical threshold where "identity" transitions from attribution to genuine property?
- What would the signature of "consciousness" look like in this framework, and is it even the right question?

---

*Developed by Frank Peterlein in collaboration with AI.*
*Repository: https://github.com/frnkptrln/systems-and-intelligence*
