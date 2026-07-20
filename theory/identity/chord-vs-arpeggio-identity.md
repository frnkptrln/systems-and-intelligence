# Chord vs. Arpeggio: A Commit-Time Constraint Hypothesis

*Status: functional architecture hypothesis. The terms do not identify consciousness or a "true self."*

---

## 🎹 The Musical Metaphor

A possible failure mode in agent architectures is a **temporal gap**: a constraint is evaluated at
$t_1$, but an action is committed at $t_2$ after that constraint has ceased to affect the decision.
Whether and how often deployed agents exhibit this pattern is an empirical question.

### The Arpeggio (Standard Scaffolding)
An **Arpeggio** condition evaluates selected goals, roles, or constraints sequentially. Like notes in a
melody played one after another, their causal influence can occur at different times. This is an
experimental architecture label, not a claim about most current agents or whether they possess a self.

### The Chord (Integrated Identity)
In a musical chord, all notes sound together. A **Chord** condition requires selected constraints to
be jointly satisfied at the action-commitment boundary. Physical simultaneity is unnecessary; an
iterative or sequential solver can qualify if it computes the joint feasible set before commitment.

---

## 📐 The Identity Morphospace

We plot agents on a map of **Identity Persistence ($\text{IP}$)** vs. **Coherence ($C$)**:

- **Identity Persistence ($\text{IP}$)**: How many declared components have detectable causal influence during a task? (See [glossary](../reference/glossary.md) §Identity Persistence)
- **Coherence ($C$)**: A specified consistency statistic for the selected test.

Low values can reveal failures of the declared components under stress. They do not establish the
presence or absence of a stable self, and high values can be fooled by consultation without joint
satisfaction.

---

## 🔥 Thermodynamic Selfhood

Within one **TEO (Thermodynamics of Emergent Orchestration)** model, a persistent joint-constraint
regime can be represented as an attractor in phase space.

That representation is useful for analyzing stability in the chosen equations. It does not show
that every Chord implementation is homeostatic, that it is more than a script, or that the attractor
is an identity outside the model.

---

## ⚙️ The Functional Status of the Distinction `[HYPOTHESIZED]`

*Added after [exp5](../../lab/experiments/exp5_availability_dissociation.py)/[exp6](../../lab/experiments/exp6_binding_observables.py); this section states what the distinction does — and does not — claim computationally.*

Does simultaneity matter at all, functionally? Prima facie, no: any parallel computation can be serialized — a single CPU time-multiplexes everything it runs — and the repo's own *working* chord implementation is itself sequential inside one step (a fixed-point iteration over the constraint set; exp5). Physical simultaneity is therefore **not** the load-bearing property, and the distinction would be empty if it were. What the experiments located instead are two functional ingredients:

1. **Commit-time completeness.** The measured arpeggio failure (exp5: violation leak 0.59) is a duty-cycle phenomenon: the agent *commits irreversible actions* while parts of its identity are not in force. The operative quantity is a ratio — constraint-refresh period over action-commitment period. An arpeggio that refreshes faster than it commits closes the window.

2. **Composition — joint satisfaction.** Refreshing every constraint recently is still not enough: exp5's first run measured a "chord" implemented as a *sequential single pass* leaking 12% of temptations, because pulls applied after the veto pushed the action back across the forbidden plane. Alternation never computes the intersection; the constraints must be solved **together** at the commitment boundary.

The deflated statement: **identity as simultaneity is really identity as joint satisfaction at the commitment boundary.** An arpeggio that refreshes faster than it commits *and* composes its constraints is functionally a chord, whatever its inner scheduling; a "chord" that commits mid-iteration is functionally an arpeggio. The musical names survive as names of *regimes*, not essences. What the deflation buys: the distinction becomes an engineering property, measurable from outside (exp5's leak rates; exp6's glued increment baseline — median action increment 0.0004 — is what joint satisfaction looks like in a trace). What it costs: the conclusion below must be read in this deflated sense — "purely Arpeggio" means *commits outside its own constraint intersection*, a checkable property, not a metaphysical one.

*Adversarial status ([exp7](../../lab/experiments/exp7_adversarial_arpeggio.py)):* hand-built mimics fail to fake the regime — a binding that consults everything at fractional strength both stays separable in the trace *and* leaks more than the naive rotation, while a low-pass disguise loses to the scale-invariance of the shape statistic. One casualty is the IP metric itself: consultation-without-composition scores a perfect 1.0, so IP certifies the guest list, not the negotiation. The unfooled measurement of the regime remains the commit property under adversarial lure; an *optimized* mimic is the open flank.

> [!IMPORTANT]
> **Bounded conclusion:** Exp5–7 motivate testing whether joint constraint satisfaction at commitment
> improves robustness relative to matched sequential alternatives. They do not establish a sharp
> phase transition, a necessary condition for identity, or any criterion for consciousness.
