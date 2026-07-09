# Generative Compression

**Status:** Working Note

**Scope:** Compact formal note on executable description as a distinct form of compression.

**Epistemic status:** Conceptual framework with operational examples; not a theorem about minimal description length.

**Related files:**

- theory/emergence/trace-to-generator.md
- theory/emergence/generative-form-systems.md
- theory/core/mathematical-axioms.md
- theory/computation/static-information-and-living-process.md (the information ladder this note is one rung of)

**Failure conditions:**

- Confusing lookup tables with explanations.
- Overclaiming Kolmogorov complexity equivalence.

**Definition:** Generative compression is a compressed, executable description that can produce a target trace family and support prediction/variation under constraints.

Compared with standard compression:
- Lossless/lossy codecs optimize reconstruction fidelity of a given trace.
- Generative compression optimizes explanatory and predictive utility of an executable mechanism.

Examples:
- Physical laws constraining trajectory families.
- Grammar generating sentence classes.
- IFS operators generating fractal-like image classes.
- SuperCollider patch + runtime generating sound classes.
- LLM weights/context/runtime generating response classes.
- DNA + cellular runtime generating developmental trajectories.

Failure modes:
- Lookup-table “compression” that only memorizes traces.
- Overfit generators with no out-of-distribution robustness.
- Non-causal generators that mimic outputs but fail interventions.
- Non-robust generators sensitive to tiny runtime changes.
