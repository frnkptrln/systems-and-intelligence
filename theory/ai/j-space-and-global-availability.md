# The J-Space Result: Global Availability Measured in Production Models

**Status:** Reading note and external-anchor mapping — no new result of this repository.

**Scope:** Maps Anthropic's July 2026 workspace paper onto this repository's global-availability
layer. The paper is evidence about the functional organization of specific production language
models. It is not evidence about consciousness, and this note does not use it as such.

**Epistemic note:** The primary source is Gurnee, Sofroniew, Pearce et al.,
[*Verbalizable Representations Form a Global Workspace in Language Models*](https://transformer-circuits.pub/2026/workspace)
(Anthropic, July 2026), measured on Claude Sonnet 4.5, Haiku 4.5, Opus 4.5, and in parts Opus 4.6.
Everything below that is not attributed to that paper is this repository's interpretation, tagged
accordingly. The result is weeks old and unreplicated outside its lab; every use of it here
inherits that provisionality.

**Repository anchors:** [Consciousness as Global Availability](../identity/consciousness-as-global-availability.md),
[Foundations Reconstruction §4.6 and §7](../core/mathematical-axioms.md),
[Open Problem 10](../reference/open-problems.md#open-problem-10-the-global-availability-question),
[exp5](../../lab/experiments/exp5_availability_dissociation.py) / [exp6](../../lab/experiments/exp6_binding_observables.py).

---

## What the paper reports

The authors introduce the **Jacobian lens** (J-lens): a readout measuring the average linearized
effect of internal activations on the probability of future token production. The **J-space** is
their term for the set of points expressible as a sparse nonnegative combination of J-lens
vectors. Their findings, in their vocabulary:

- A privileged subset of internal representations supports five workspace-like functions:
  **verbal report** (the model can name what is in the space; swapping vectors changes the
  report), **directed modulation** (concepts can be activated independently of outputs),
  **internal reasoning** (workspace vectors carry intermediate computations; intervening redirects
  conclusions), **flexible generalization** (the same representation serves as an argument to
  different downstream operations), and **selectivity** (routine processing stays outside).
- The space lives in the **middle layers**, between an early uninterpretable-read region and a
  late motor/output region.
- It is **small**: typically at most ~25 J-lens vectors active at once, never explaining more
  than ~10% of activation variance.
- Broadcast is **feedforward, not recurrent**, and no clearly encapsulated specialist processors
  were identified — two of the paper's own stated gaps between what was found and what global
  workspace theory describes.
- On consciousness the authors take an explicit non-position: the finding concerns the
  *functional role* played by consciously accessible information in humans, and they claim
  neither that the models reproduce the full workspace architecture nor anything about
  subjective experience.

One provenance observation in passing, since this repository keeps a
[verification-economy log](../../logs/017_provenance-depth-and-the-verification-economy.md):
the term "J-Space" traveled from a technical definition to press coverage to an encyclopedia
article within days of publication. The concept's public shape is already partly
press-generated; this note deliberately anchors on the primary source only.

## Why this repository cares

The [global-availability node](../identity/consciousness-as-global-availability.md) has carried
one core claim since before this paper existed:

> Some architectures make selected local states broadly available, combine them with a
> self-model and constraints, and let the result alter later action. This describes a functional
> profile, not an amount of subjective experience.

The paper reports that production language models exhibit the first half of that profile, found
by internal inspection rather than behavioral testing. The mapping, term by term
`[HYPOTHESIZED]`:

| Paper | This repository |
|:---|:---|
| Verbalizable representations, selectivity | selected local states (not all processing is available) |
| Flexible generalization, broadcast to downstream operations | global availability to the whole system |
| Directed modulation, intervention redirecting reasoning | availability altering later action |
| J-lens | a declared observation process ([Foundations §4.6](../core/mathematical-axioms.md#46-observation)) |
| k ≤ 25 capacity, ≤ 10% variance | bounded integration — availability is scarce, not total |

Two disciplines happen to match exactly. The paper's "we take no position" on experience is
[non-claim #8](../reference/what-this-project-does-not-claim.md) in other words. And the paper's
method is the move this repository's
[consciousness nodes](../identity/machine-consciousness-as-generator-coherence.md) argued was
required: behavior underdetermines internal organization, so the question must be answered by
inspecting structure, not by interrogating fluency. That an interpretability team with weight
access did exactly this is methodological progress independent of how the specific result ages.

## What the result is relative to

The repository's foundation supplies the caveat the press coverage drops. The J-lens is an
observation kernel with a declared interface, and what counts as "in the workspace" is relative
to it. The paper says this itself in its limitations: the lens only identifies concepts
corresponding to single tokens in the vocabulary. In the foundation's terms, the sigma-algebra
has been chosen, and it determines which distinctions can exist in the result
([Foundations §9.4](../core/mathematical-axioms.md#94-internal-limitations)). The
[hidden-extension proposition](../core/mathematical-axioms.md#7-a-result-the-foundation-forces-non-identifiability)
adds the general form: systems equivalent under one lens need not share mechanism.

None of this diminishes the finding. It states its type: **"the J-space" is
instrument-relative** — a different lens may carve a different privileged set, and whether the
five functional properties are properties of one underlying structure or of the lens family is
exactly the kind of question the paper's own limitations section leaves open.

## The question it makes quantitative

[Open Problem 10](../reference/open-problems.md#open-problem-10-the-global-availability-question)
ends with: real language models remain untested, and a solution requires internal-state access.
This paper is that step for the availability half. What it does not answer is the repository's
sharper half — the **Chord vs. Arpeggio** question: at the moment of commitment, are goals,
world-state, self-model, and veto constraints *jointly* operative, or do they rotate through?

The paper makes this question quantitative for the first time `[HYPOTHESIZED]`:

> If the workspace holds at most ~25 simultaneously active vectors, then co-instantiation has a
> budget. The chord question becomes: do constraint representations occupy workspace slots
> *at the same step* as the plan they constrain — or is the observed feedforward broadcast
> exactly the fast sequential pass that [exp5](../../lab/experiments/exp5_availability_dissociation.py)
> measured leaking 12% of temptations in the toy?

The paper's own gap report points the same way: broadcast is feedforward, not recurrent. A
workspace that cannot re-enter is structurally closer to an arpeggio than a chord. Whether that
matters behaviorally is measurable, and the toy version already exists.

## Testable follow-ups

1. **A J-lens analogue at toy scale.** Exp6 found that binding structure in the toy
   architectures is passively readable from per-step increment statistics. The J-lens logic —
   average linearized effect of internal state on future output — is a second passive readout of
   the same type. Applying it to exp5's private/broadcast/chord architectures asks: does it
   separate them, and does it agree with exp6's observable? Agreement would say the toy
   instruments measure something lens-independent; disagreement would locate lens-relativity at
   toy scale, where it can be dissected.
2. **Constraint occupancy at commitment** (outside this repository's reach, inside a lab with
   weight access): sample workspace contents at action-commitment steps and test whether
   constraint vectors co-occur with plan vectors or alternate with them.

## What would weaken this note

- Failure of the paper's findings to replicate, or a lens-family study showing the five
  properties do not survive a change of instrument.
- The mapping table degenerating into synonym-trading — if no prediction ever differs because of
  it, it is decoration and should be deleted.
- Any use of this note, inside or outside the repository, as support for "language models are
  conscious." Both the paper and this repository state the opposite of that inference.

---

## Related

- [Consciousness as Global Availability](../identity/consciousness-as-global-availability.md) — the architecture layer this anchors
- [Machine Consciousness as Generator Coherence](../identity/machine-consciousness-as-generator-coherence.md) — why internal inspection was the required move
- [Foundations Reconstruction](../core/mathematical-axioms.md) — observation kernels, lens-relativity, hidden extensions
- [Open Problem 10](../reference/open-problems.md#open-problem-10-the-global-availability-question) — the question this partially advances
- [World Models and VLA Systems](world-models-and-vla.md) — the sibling reading note for embodied systems

> **External anchors.** Gurnee, Sofroniew, Pearce et al. (2026),
> [*Verbalizable Representations Form a Global Workspace in Language Models*](https://transformer-circuits.pub/2026/workspace),
> the primary source; Baars (1988), *A Cognitive Theory of Consciousness*, and Dehaene &
> Changeux (2011) for the global-workspace lineage the paper measures against; Mashour et al.
> (2020) for the neuronal-workspace synthesis. The anchors ground the workspace vocabulary; none
> of them, and not the 2026 paper either, establishes a bridge from function to experience.
