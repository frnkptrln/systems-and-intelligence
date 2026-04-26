# 🧭 Repository Information Architecture

This document defines **where new content should live** so the project can scale without turning into one undifferentiated stream of notes.

---

## 1) Content Lanes (What goes where)

### A. `docs/book/` → Curated narrative
Use this for the **reader-first canonical path**.  
Characteristics:
- pedagogical ordering
- lower branching, higher coherence
- links outward to theory/code, but does not duplicate all details

### B. `theory/` → Formal + conceptual essays
Use this for claims, derivations, definitions, and argument structure.  
Characteristics:
- can be exploratory, but should still target falsifiability
- may be longer and denser than book chapters
- should clearly mark epistemic status (demonstrated / hypothesized / open / speculative)

### C. `papers/` (and mirrored `docs/papers/`) → Publication packaging
Use this for concise, citation-ready syntheses of a bounded scope.  
Characteristics:
- tighter than theory essays
- explicit method / limitations framing
- less world-building, more formal communication

### D. `logs/` → Applied architecture journals
Use this for "**if we built this for real**" design logs.  
Characteristics:
- architectural options, protocol sketches, operational constraints
- more applied than theory, less polished than papers
- can include unknowns and design forks

### E. `fiction/` → Narrative stress-testing
Use this for scenario-driven exploration constrained by the theory.  
Characteristics:
- story format (dossier, transcript, short story, etc.)
- translates formal constraints into lived consequences
- should not silently contradict core physical/theoretical constraints

### F. `simulation-models/`, `core/`, `systems-orchestration/` → Executables
Use this for runnable artifacts and reusable implementation primitives.  
Characteristics:
- code first; docs explain assumptions, parameters, and expected behavior
- when possible, map simulation outcomes back to specific theory claims

---

## 2) Decision Rules (Quick triage)

When adding a new artifact, ask:

1. **Is this primarily runnable?**  
   → put in `simulation-models/`, `core/`, or `systems-orchestration/`.
2. **Is this primarily a formal argument?**  
   → put in `theory/`.
3. **Is this optimized for linear reading?**  
   → put in `docs/book/`.
4. **Is this publication-facing and compact?**  
   → put in `papers/`.
5. **Is this an applied design notebook with open decisions?**  
   → put in `logs/`.
6. **Is this a narrative scenario to test implications?**  
   → put in `fiction/`.

If two answers are true, choose one **home location** and cross-link instead of duplicating.

---

## 3) Minimal Maturity Tags (recommended)

For non-code documents, add a short status line near the top:

- `Status: Draft`
- `Status: Working Note`
- `Status: Formalized`
- `Status: Publication Draft`

This keeps expectations clear for readers and contributors.

---

## 4) Anti-Entropy Rules

To keep the repository "rounder":

1. **One source of truth per concept.**  
   Everything else links to it.
2. **No silent duplicates.**  
   If mirrored for docs rendering, note the canonical file.
3. **Map code ↔ claim.**  
   Each simulation README should name the theory claims it informs.
4. **Separate modes of writing.**  
   Theory argues, logs design, fiction dramatizes, papers compress.

---

## 5) Suggested Next Cleanup Steps

1. Add a short `Status + Scope + Links` header template to every `logs/*.md`.
2. Build a small index table mapping each `logs` entry to related `theory` and `simulation-models` files.
3. Add "home file" references where `papers/` and `docs/papers/` intentionally mirror each other.
