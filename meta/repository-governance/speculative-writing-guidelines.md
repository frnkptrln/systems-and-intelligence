# Speculative Writing Guidelines

This document defines how speculative additions should be integrated into the repository without fragmenting its conceptual architecture.

---

## 1) Placement Rules

- Put work in **`fiction/`** when it is a **narrative stress test** of existing theory claims and constraints.
- Put work in **`theory/`** when it is a **conceptual or theory-adjacent essay** that introduces, sharpens, or challenges a claim.
- Put work in **`meta/`** when it defines **rules, epistemic framing, taxonomy, and repository self-governance**.

Do not create a new top-level taxonomy unless an existing lane cannot carry the artifact.

---

## 2) Required Speculation Label

Every speculative text should declare its mode near the top. Use one of:

- `Narrative consequence`
- `Conceptual essay`
- `Thought experiment`
- `Open metaphor`
- `Proto-theory`

If a text mixes modes, declare a primary mode and one secondary mode.

---

## 3) Continuity Over Mythology

Speculative writing should connect to existing concepts rather than invent isolated lore.

Before adding a text, map it to at least two repository anchors (examples):
- Substrate Veto
- Biological Veto
- Human Vital Systems
- Local Causality and Invisible Consequences
- Chord vs Arpeggio
- Mirror Problem
- TEO framework constraints

If a new term is introduced, define it minimally and show how it relates to existing architecture.

---

## 4) Fiction Style Baseline

Default fiction style in this repository is **Dossier / Found Footage / Log / Transcript**.

Prefer these forms unless there is a strong reason to use a conventional linear narrative. If you deviate, explain why in a one-line author note.

Fiction should:
- dramatize consequences of constraints,
- preserve ambiguity where appropriate,
- avoid turning theory into sermon,
- avoid generic corporate or cyberpunk aesthetics detached from repository logic.

---

## 5) Epistemic Hygiene

Speculative texts must not silently present narrative invention as established fact.

Use clear framing signals:
- in fiction: institutional headers, source notes, transcript framing,
- in essays: explicit status tags (`Draft`, `Working Note`, `Formalized`) and scope statements.

When making bold claims in theory-adjacent writing, distinguish:
- what is demonstrated in code/simulation,
- what is hypothesized,
- what is exploratory metaphor.

---

## 6) Cross-Linking Requirement

Each new speculative file should link to relevant neighboring files (or be linked from index files) so it is discoverable inside existing reading paths.

Minimum integration steps:
1. update local README/index in its folder,
2. update root `README.md` only if that section already lists similar artifacts,
3. avoid duplicate summaries across multiple files.

---

## 7) Practical Checklist for Contributors

Before opening a PR, verify:

- [ ] The artifact is placed in the correct lane (`fiction/`, `theory/`, or `meta/`).
- [ ] The text declares its speculative mode.
- [ ] The text references existing concepts rather than standing alone.
- [ ] The tone matches repository constraints and avoids marketing language.
- [ ] Index files were minimally updated for discoverability.
- [ ] No contradictions were introduced against hard constraints unless intentionally framed as a challenge case.

---

## 8) Scope of This Guideline

This guideline governs speculative prose artifacts. It does not replace coding standards, simulation validation practices, or publication formatting in `papers/`.
