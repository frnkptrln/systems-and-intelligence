# 🔭 Meta

**Status:** Orientation index for `meta/` — not a claim document.

This folder has two lanes so we don't mix conceptual reflection with repository governance:

1. **Conceptual Meta** (epistemology, philosophical framing)
2. **Repository Meta** (governance, contribution and structure rules)

---

## Meta Inventory (current files)

| File | Lane | Purpose |
|---|---|---|
| `conceptual-meta/agent-operating-note.md` | Repository Meta (filed under conceptual-meta/) | What an agent working in the repository reads first and must not do; supersedes the prompt seed. |
| `conceptual-meta/agent-prompt-seed.md` | Conceptual Meta | Superseded 2026-09-02 by `agent-operating-note.md`; retained as history. |
| `repository-meta/repository-information-architecture.md` | Repository Meta | Canonical placement rules and lane-splitting logic for the whole repo. |
| `repository-meta/repository-as-thought-system.md` | Repository Meta | Meta-orientation: how the repo's own structure can be read without becoming self-referential noise. |
| `repository-meta/freshness-and-review.md` | Repository Meta | Freshness policy for changing external claims and internally derived state, with CI-backed drift checks. |
| `repository-meta/speculative-writing-guidelines.md` | Repository Meta | Speculative writing conventions (placement, labeling, continuity, style baseline). |
| `repository-meta/cultural-optimization-red-team-manual.md` | Repository Meta | Guardrails against Goodhart pressure in cultural optimization systems. |
| `repository-meta/core-claims.md` | Repository Meta | Claim register for the viability arc and identity branch, with artifact links and failure conditions. |
| `repository-meta/identification-claims.md` | Repository Meta | Claim register for the model-identification arc, proposed 2026-09-02. |

If a future file does not clearly fit one lane, add a one-line "Lane:" declaration at the top of that file.

---

## Conceptual Meta

### [Agent Operating Note](conceptual-meta/agent-operating-note.md)

What an agent working inside the repository reads first, the invariants it keeps, the local gate it
runs, and the decisions it leaves to the maintainer. Supersedes the prompt seed below.

### [Agent Prompt Seed](conceptual-meta/agent-prompt-seed.md)

Superseded 2026-09-02 by the operating note; retained as history. It was an experiment in
autonomous identity seeding: a prompt designed to initialize an agent with a set of thermodynamic and
systemic axioms, forcing it to navigate the tension between entropy, growth, and alignment.

---

## Repository Meta

### [Repository Information Architecture](repository-meta/repository-information-architecture.md)

Defines where new artifacts should live and how the repository keeps a coherent lane split.

### [Repository as Thought System](repository-meta/repository-as-thought-system.md)

Defines the useful meta-level: the repo can be read as operator, iteration, form, boundary, and return path, but only to improve navigation and prevent drift.

### [Freshness and Review](repository-meta/freshness-and-review.md)

Defines how time-sensitive external claims, publication states, provider interfaces, copied counts,
and other internally derived state are reviewed without erasing research history. The deterministic
subset is checked by [`lab/tools/audit_repository_freshness.py`](../lab/tools/audit_repository_freshness.py)
in CI.

### [Speculative Writing Guidelines](repository-meta/speculative-writing-guidelines.md)

Lightweight conventions for placing and labeling speculative fiction/theory so new additions stay connected to existing concepts and formats.

### [Cultural Optimization Red Team Manual](repository-meta/cultural-optimization-red-team-manual.md)

A practical anti-pattern and review ritual guide for authenticity/care optimization systems.

### [Core Claims](repository-meta/core-claims.md)

The claim register for the viability arc and identity branch — Substrate Veto, Impedance Matching, Identity Persistence, and Vital Floors — each with artifact links and explicit failure conditions.

### [Identification Claims](repository-meta/identification-claims.md)

The claim register for the model-identification arc, proposed 2026-09-02: four claims and one
candidate, derived only from the benchmark, the Witness Principle, Decision-Relevant
Identifiability, and Active Identifiability, each with artifacts by evidential kind and a failure
condition.

---

These notes are intentionally mixed in maturity level, but separated by function so conceptual essays and repository-meta documents don't blur together.
