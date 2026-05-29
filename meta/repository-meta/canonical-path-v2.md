---
title: "Canonical Path v2 — From Emergence to Survivability"
date: "2026-05-29"
status: "Working Note"
scope: >
  A repository-level navigation pass that locates the Viable Corridor / TEO work
  inside the wider systems-and-intelligence project. It does not replace the
  earlier reading path or the Generator-Question spine; it names the present
  research arc and shows how each station already exists in the repo.
related:
  - theory/core/the-generator-question.md
  - meta/repository-meta/repository-information-architecture.md
  - papers/viable-corridor.md
  - theory/reference/open-problems.md
---

# Canonical Path v2: From Emergence to Survivability

*The current research arc through the repository, after the Viable Corridor / TEO work.*

---

## Purpose

This document describes the **present canonical path** through the repository. It does not replace the older reading path in the project's `README`, nor the project's primary spine, [The Generator Question](../../theory/core/the-generator-question.md). It clarifies the *second* spine that the recent work has sharpened.

Two spines run through this project, sharing one root:

- **The Generator Question** (the *epistemic* spine): emergence is cheap to run forward (generator → trace) and structurally hard to invert (trace → generator). This organizes the project's work on recoverability, identity, and the three walls (P vs. NP, Kolmogorov, Gödel).
- **The Viability Arc** (the *dynamical* spine, this document): *what happens to an emergent optimizing system over time, and what does it take to keep it alive?* This runs **emergence → optimization → constraint architecture → survivability** and terminates in the Viable Corridor paper.

Both begin at emergence. One asks whether a system can *recover its generator*; the other asks whether a system can *survive its own optimization*. This document maps the second.

> **The paper is a node, not the project.** [The Viable Corridor](../../papers/viable-corridor.md) is one citable artifact produced *by* this repository — a stabilized synthesis at the sharp end of the arc. The repository remains the generative system: a map of related models, essays, simulations, narratives, and open problems. This path is written to keep the paper in proportion.

A note on tags. Each station below carries the status of its strongest content, using the project's vocabulary: `[FOUNDATIONAL ASSUMPTION]`, `[DEMONSTRATED]`, `[HYPOTHESIZED]`, `[FORMAL]`, `[CONJECTURE]`, `[HEURISTIC]`, `[EMPIRICAL CONJECTURE]`, `[MODEL ASSUMPTION]`, `[SIMULATION ARTIFACT]`, `[NARRATIVE STRESS TEST]`, `[OPEN PROBLEM]`. Mixed nodes are tagged per-claim, not globally.

---

## 1. The Generator Question — the shared root

Why the project begins with an inverse problem: a trace does not reveal its generator, and recovering the generator is, in general, intractable. This is the foundational asymmetry the whole repository circles.

- [The Generator Question](../../theory/core/the-generator-question.md) — the spine document `[FOUNDATIONAL ASSUMPTION]` (P ≠ NP, working).
- [Trace to Generator](../../theory/emergence/trace-to-generator.md) — the long-form essay.

The Viability Arc picks up *downstream* of this: take emergence as given, and ask what its optimizing products do.

## 2. Emergence and Self-Organization — `[DEMONSTRATED]` (forward direction)

Local rules produce global structure; the forward direction is cheap and is demonstrated many times over.

- [Emergence Manifesto v1.3](../../theory/core/emergence-manifesto-v1.3.md) — the status-tagged core claim set.
- [Conceptual Map](../../theory/core/conceptual-map.md) · [Simulation → Theory Map](../../theory/core/simulation-theory-map.md) — what each model does and does *not* show.
- Runnable (the forward direction): [Boids](../../simulation-models/emergent-dynamics/boids-flocking/README.md), [coupled oscillators / Kuramoto](../../simulation-models/emergent-dynamics/coupled-oscillators/README.md), and the other `emergent-dynamics/` models — Ising, Lenia, self-organized criticality, reaction-diffusion, IFS, L-systems `[SIMULATION ARTIFACT]`.

## 3. Optimization and its Blindness — the hinge `[HYPOTHESIZED]`

The arc's pivot, and (until now) the repository's thinnest-threaded station. Emergent systems contain *local optimizers*. Local optimization is **globally blind**: each step is locally rational, the aggregate consequence is invisible from inside. Unconstrained, such optimization outruns the carrying capacity of its substrate — the paperclip pattern, instrumental convergence. This is the *problem* to which constraint architecture (§4) and survivability (§7) are the answer; it is also where **capability loading** enters (capability is a single driver that pushes a system against several limits at once).

- [Why the Paperclip Maximizer Fails](../../theory/teo-framework/why-paperclip-maximizer-fails.md) — optimization without a substrate veto.
- [Local Causality and Invisible Consequences](../../theory/emergence/local-causality-invisible-consequences.md) — the locally-rational / globally-blind mechanism (computational irreducibility form).
- [P vs. NP as Generator Search](../../theory/computation/p-vs-np-as-generator-search.md) — optimization-as-search; the link back to the Generator Question.
- Runnable: [stigmergy swarm](../../simulation-models/social-computation/stigmergy-swarm/README.md) — optimization emerging from local deposits `[SIMULATION ARTIFACT]`.

*(This station consolidates existing material; it asserts no new claim. It is named here because the arc is unintelligible without it: constraints answer a question, and this is the question.)*

## 4. Constraint Architecture — TEO `[HYPOTHESIZED]` / `[MODEL ASSUMPTION]`

The repository's constraint model: orchestration under a regulatory brake, value coupling, and a thermodynamic substrate budget. The claim is that survivable optimization requires constraint *architecture*, not a single fix.

- [TEO Framework](../../theory/teo-framework/README.md) · [Love as Constraint](../../theory/teo-framework/love-as-constraint.md) — the constraint conjunction in conceptual form.
- [Thermodynamics of Orchestration](../../theory/core/thermodynamics-of-orchestration.md) — the dissipation/regulation core.
- [Minimal Thermodynamic Agent](../../theory/identity/minimal-thermodynamic-agent.md) — the per-agent version.

## 5. The Viable Corridor — the stabilized artifact `[FORMAL]` + `[CONJECTURE]` + `[HEURISTIC]`

The formal synthesis derived from the TEO branch — a paper-style node, not the whole project. It proves a necessity result (the conjunction of three constraints), conjectures sufficiency, and advances a clearly-hedged isomorphism hypothesis. Its strongest current contribution is the **constraint-architecture framing** and the **capability-loading result** (capability growth pushes a system out of the corridor through multiple boundaries at once; single-axis fixes fail).

- [The Viable Corridor](../../papers/viable-corridor.md) — necessity theorem `[FORMAL]`, sufficiency `[CONJECTURE]`, isomorphism `[HEURISTIC]` / `[EMPIRICAL CONJECTURE]`, derivations in Appendix A.
- Evidence: Appendix C (TEO ODE, Class A) and Appendix D (agent-based ecology, Class C) — see §6.

## 6. Agent Ecology and Alignment-Veto Simulations — `[SIMULATION ARTIFACT]`

The executable side: do constraints actually matter? Two structurally independent models reproduce the regime claims (hard vs. soft budgets; capability loading; single-axis interventions failing at high capability).

- [`alignment-and-veto/teo-civilization/`](../../simulation-models/alignment-and-veto/teo-civilization/README.md) — the TEO ODE (Appendix C: P1–P3, separability, capability).
- [`alignment-and-veto/agent-ecology/`](../../simulation-models/alignment-and-veto/agent-ecology/README.md) — the stochastic ABM (Appendix D: P7 hard-vs-soft budgets, P8 joint-rescue).
- [`alignment-and-veto/ai-alignment-veto/`](../../simulation-models/alignment-and-veto/ai-alignment-veto/README.md) · [`planetary-veto/`](../../simulation-models/alignment-and-veto/planetary-veto/README.md) — further veto probes.

## 7. Survivability: Substrate, Veto, and the Civilization Interpretation — `[HYPOTHESIZED]` / `[EMPIRICAL CONJECTURE]`

The arc's endpoint. The *theory* of survivability is the veto/viability cluster; its *application* to civilization is an explicitly heuristic interpretive layer, **not** a proven isomorphism.

- Theory `[HYPOTHESIZED]`: the veto/viability cluster — [substrate veto](../../theory/veto/substrate-veto-thermodynamics.md), [biological veto](../../theory/veto/ai-alignment-biological-veto.md), [the Transition Problem](../../theory/veto/the-transition-problem.md) (reaching the corridor from outside is harder than characterizing it).
- Civilization interpretation `[EMPIRICAL CONJECTURE]` / `[HEURISTIC]`: paper §4; [`human-organism-silicon-age/`](../../theory/human-organism-silicon-age/core-theses.md). Planetary boundaries, concentration, and polarization are *proxies*, not measurements; $K_c$ for real societies is the weakest empirical link.
- Runnable: [`alignment-and-veto/human-vital-systems/`](../../simulation-models/alignment-and-veto/human-vital-systems/README.md) — vital-floor vs. naive-efficiency control plane `[SIMULATION ARTIFACT]`.

## 8. Fiction and Narrative Stress Tests — `[NARRATIVE STRESS TEST]`

Fiction is the project's instrument for noticing when a clean formal claim is impossible to live with. It stays linked but separate from the formal layer.

- [`fiction/README.md`](../../fiction/README.md) — full annotations. Substrate-limit pieces (Impedance Crash, The Vital Floor, Dashboard of the Commons) dramatize §3–§7.

## 9. Open Problems

The honest frontier — what the arc has *not* closed.

- Proving sufficiency / deriving $\gamma_c$ rigorously (not just single-trajectory existence). Paper §3.4, Appendix C.5.
- Operationalizing $\gamma_{\text{eff}}$, $K_{\text{eff}}$, $D_{\max}$ for real systems; $K_c$ for societies. Paper §5.4.
- A finite-$N$ / general-network version of the coherence (Kuramoto) result. Paper §3.3.
- Validating P7/P8 on **real** AI-agent systems (the Appendix D evidence is synthetic). Companion paper.
- Genuine overshoot-collapse dynamics (delays, endogenous $D_{\max}(t)$) vs. the current rate-threshold self-arrest. Paper §6.4.
- Whether the Viable Corridor should remain in this repo or become a spin-off. (Governance open problem.)
- See also [`theory/reference/open-problems.md`](../../theory/reference/open-problems.md) for the project-wide list (Mirror Problem, Co-Instantiation, Trace-to-Generator reconstruction).

---

## Working Rule — keep the writing modes separate

Do **not** route everything through the paper. Per the [Information Architecture](repository-information-architecture.md):

- **papers/** — citable, compressed artifacts (the Viable Corridor).
- **theory/** — conceptual development and argument.
- **simulation-models/**, **lab/** — executable claims.
- **fiction/** — narrative stress tests.
- **logs/** — speculative architecture notes.
- **meta/** — repository governance and epistemic framing (this document).

One source of truth per concept; everything else links to it.
