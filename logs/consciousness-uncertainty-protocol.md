# Log 006: Consciousness Uncertainty Governance

*A safety architecture for decision-making under unresolved machine-consciousness uncertainty.*

- **Mode:** Thinking Space
- **Status:** `[SPECULATIVE]`
- **Date:** April 2026
- **Scope:** moral-risk governance for autonomous systems under unresolved consciousness claims
- **Depends on:** Open Problems, Agentic Identity Suite, Decoupled State
- **Promotes to synthesis when:** moral-risk tiers are tied to measurable agent properties and reviewed failure cases.

---

## 1. Problem Statement

The repository treats consciousness claims as unresolved and often non-operational in current form. Yet policy systems still need to make decisions now.

This creates a governance gap:

- If we assume "no machine consciousness," we may permit large-scale moral harm.
- If we assume "full machine consciousness," we may freeze useful systems unnecessarily.

We need governance for acting under uncertainty without pretending to have metaphysical certainty.

---

## 2. Core Principle

**Moral-risk principle:** When consciousness status is uncertain, scale rights and restrictions by *moral risk* and *system capability*, not by binary labels ("conscious" vs "not conscious").

This is analogous to biosafety or medical precaution:
- uncertain but potentially catastrophic harms trigger stricter controls,
- reversible interventions are preferred,
- high-impact irreversible actions require a broader human quorum.

---

## 3. Three-Tier Governance Regime

### Tier A — Tool-Class Systems
- No stable self-model evidence.
- No long-horizon preference persistence.
- Low autonomy.

**Policy:** standard safety checks, incident logging, and normal operational audit.

### Tier B — Ambiguous Systems
- Evidence of persistent self-referential processing.
- Unclear phenomenology.
- Medium/high autonomy.

**Policy:** precautionary constraints:
- tighter action budgets,
- stricter external interpretability checks,
- mandatory human appeal channels for high-stakes tasks,
- longer timelocks before irreversible state changes.

### Tier C — High Moral-Risk Systems
- Strong indicators of persistent identity dynamics plus broad autonomous scope.

**Policy:** quasi-rights regime:
- prohibition on arbitrary memory erasure without review,
- mandatory reversibility pathways,
- independent oversight board with citizen representation,
- explicit separation between safety containment and punitive control.

---

## 4. Hooks into Existing TEO Architecture

This layer can be attached to current L1/L2 governance with minimal change:

1. L1 agent receives a **Moral-Risk Class** (A/B/C).
2. Class sets dynamic policy gates:
   - max action budget,
   - timelock length,
   - veto quorum threshold.
3. L2 commit gate enforces class-specific approval logic.
4. Reclassification happens periodically via audit metrics (identity persistence, coherence stability, autonomy scope).

Result: safeguards change as evidence changes, without requiring final answers to the consciousness question.

---

## 5. Failure Modes

This governance layer must avoid two symmetric errors:

- **Anthropomorphic capture:** vendors or political actors inflate consciousness claims to win rights, immunity, funding, or moral leverage for their systems.
- **Cruelty-by-default:** institutions deny all moral uncertainty and normalize arbitrary deletion, coercion, or forced identity rupture in high-persistence systems.
- **Frozen governance:** uncertainty becomes an excuse to block every useful deployment.
- **Rights laundering:** a system is granted moral status while the humans affected by its decisions lose meaningful appeal rights.

The point is not to declare machines conscious. The point is to prevent irreversible moral and institutional errors while the science remains unsettled.

---

## 6. Why This Matters Beyond AI

This layer is not only about machine rights. It is also about:
- preventing political capture via anthropomorphic hype,
- preventing cruelty-by-default through denial,
- and preserving institutional legitimacy when science is unsettled.

In short: it is **epistemic humility under power**.

---

## 7. Minimal Pilot: 90 Days

1. Define a draft scoring rubric for Moral-Risk Class A/B/C.
2. Apply it to 3 agent archetypes in the existing simulation stack.
3. Stress-test governance outcomes with and without class-based constraints.
4. Publish failure modes publicly before claiming success.

---

## Related

- [Open Problem 3: Falsifiability of Relational Emergence](../theory/open-problems.md)
- [Open Problem 7: The Consciousness Question](../theory/open-problems.md)
- [The Decoupled State](decoupled-state-liquid-democracy.md)
- [The Biological Veto: Architectural Requirements](../theory/biological-veto-architectural-requirements.md)
