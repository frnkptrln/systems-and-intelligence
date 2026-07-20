# External Review Request

**Status:** Open request — maintained alongside the claims it exposes.

**What this is:** A reviewer's entry point. The repository is large and most of it is essays; this page lists the small set of claims that are actually load-bearing, says which field each belongs to, and states what would refute it. A reviewer should be able to check one section without reading anything else.

**Why now:** Until mid-2026 this project presented four domain claims as "Mathematical Axioms of the Computational Ecology" and treated P ≠ NP as a load-bearing assumption. The [Foundations Reconstruction](../../theory/core/mathematical-axioms.md) withdrew all of that. What remains is smaller and, we believe, defensible — which is the precondition for asking anyone to spend time on it. [What This Project Does NOT Claim](../../theory/reference/what-this-project-does-not-claim.md) is the boundary; if any claim below exceeds it, that is a defect.

**What we are asking for:** disconfirmation. Not endorsement, not collaboration, not a reading of the whole repository. Each section below names a specific thing that could be wrong.

---

## 1. Categorical probability — is the foundation correct and is it minimal?

**Document:** [Foundations Reconstruction](../../theory/core/mathematical-axioms.md), §§1–4 and §9.5
**Reading time:** ~25 minutes for §§1–4.

The claim is deliberately unoriginal: the smallest familiar classical basis adequate for the repository's vocabulary is standard Borel spaces plus Markov kernels, i.e. `BorelStoch` as a Markov category, and the document says outright that its mathematics is established rather than new (self-assessed 1/5 on novelty).

**What we would like checked:**

1. Are the primitives, axioms, and derivations in §§3–4 stated correctly? Particularly: state as a kernel from the unit interface, the deterministic sub-case, the copy/discard structure, and the disintegration argument in §4.8.
2. Is the **relative minimality claim** in §3 defensible, or is there a strictly weaker compositional language with equal coverage over classical finite and continuous models? This is [Open Problem 13](../../theory/reference/open-problems.md#open-problem-13-foundation-minimality-and-scope) and the place we most expect to be wrong.
3. Does any derivation smuggle in an undeclared assumption?

**What would refute it:** a weaker basis with equal coverage; an undeclared assumption in a derivation; or a classical target phenomenon that provably needs a third primitive.

**Relevant background:** Fritz (2020) on Markov categories is the primary anchor.

---

## 2. Computational mechanics — is the identity claim the right one?

**Document:** [Foundations Reconstruction §5.1](../../theory/core/mathematical-axioms.md#51-identity); [Invariance and Identity](../../theory/core/invariance-and-identity.md)
**Reading time:** ~15 minutes.

We claim the strongest defensible notion of persistent identity recovered by the foundation is **predictive identity** — histories with identical conditional futures — and that this is already causal states in computational mechanics rather than anything new. Everything stronger (identity of persons, agents, organizations) is declared to require a test family and is not derived.

**What we would like checked:**

1. Is the reduction to causal states stated with the right conditions (stationarity, regularity, almost-everywhere qualifications)?
2. Is the negative claim too strong or too weak — i.e. does computational mechanics license more than we grant it, or less?
3. The repository's identity instruments (Identity Persistence, Δ-coherence) are presented as *one proposed test family*, not as measurements of identity. Is that framing adequate, or does it still overclaim?

**What would refute it:** a demonstration that predictive equivalence gives more (or less) than we state under the conditions we name.

**Relevant background:** Shalizi & Crutchfield (2001).

---

## 3. Evolutionary dynamics — is the selection result sound, and is it new to us only?

**Documents:** [benchmark README, v1.11–v1.12](../../lab/benchmarks/inverse-reconstruction/README.md); code in [`co_stabilization_population.py`](../../lab/benchmarks/inverse-reconstruction/co_stabilization_population.py) and [`co_stabilization_selection.py`](../../lab/benchmarks/inverse-reconstruction/co_stabilization_selection.py)
**Reproduction:** `pip install numpy matplotlib`, then `python co_stabilization_population.py` (~7 s) and `python co_stabilization_selection.py` (~80 s). Both print every number quoted in the README.

Two preregistered results, both reported as failures of their own criterion:

- **v1.11:** a support network that is measurably useful in paired ablation (+0.0176 integrated viability) is nevertheless selected *downward* in 16/16 seeds.
- **v1.12:** making contribution visible to partner formation does not reverse this. Partner choice instead excludes non-contributors from the network almost completely (1.2% of linked agents vs 22.0% blind) while they persist in the population (27.1%).

**What we would like checked:**

1. **Is this simply a known public-goods result reproduced in a new costume?** We expect substantial prior art (Olson; Ostrom; Axelrod; spatial reciprocity; partner-choice literature) and would rather be told plainly than discover it later. If the finding is standard, we want to cite the standard source and reduce our claim accordingly.
2. Is the accounting sound? Energy is audited, transfers are bounded by unused repair capacity, and informed arms pay for partner information. The blind arm reproduces v1.11 trajectory-for-trajectory, which a test asserts.
3. Is the **measurement choice** defensible? The preregistered metric compares transfer-on against transfer-off. For a rule that rewards the trait even when transfer is off, the control rises too — so on/off deltas and drift-from-start disagree. We report the preregistered comparison as the verdict and the other as a post-hoc diagnostic. Which is the right question?

**What would refute it:** a bug in the accounting; an established result that already covers this; or a demonstration that the metric answers a different question than the one we ask.

---

## 4. Interpretability methodology — is the identification argument useful outside toys?

**Documents:** [Foundations Reconstruction §7](../../theory/core/mathematical-axioms.md#7-a-result-the-foundation-forces-non-identifiability); [benchmark v1.1](../../lab/benchmarks/inverse-reconstruction/README.md)
**Reproduction:** `python intervention_experiment.py` (~5 s).

The hidden-extension proposition is elementary: a latent process independent of the observation map preserves every observed trace law, so prediction does not identify mechanism. The benchmark supplies the operational counterpart in a toy: passive observation plateaus at equivalence-class size 8 indefinitely, single-bit interventions collapse it within ~10 queries, and one prepared state collapses it in a single step — *watching < perturbing < preparing*.

**What we would like checked:**

1. Is the proposition stated and proved correctly, and is it as elementary as we claim?
2. Does the toy hierarchy transfer to interpretability practice, or does it mislead? We think it argues that behavioural probing alone cannot identify mechanism and that causal intervention is not optional — but we are not an interpretability group and may be overreaching.
3. Is there existing work that makes this argument better, which we should be citing instead of restating?

**What would refute it:** the transfer failing for a stated structural reason; or existing work that supersedes the framing.

---

## 5. The viability arc — is it worth instrumenting or should it be retired?

**Document:** [The Viable Corridor](../../papers/viable-corridor.md)
**Reading time:** the status section and §7.1 are enough for a first judgement.

This is the repository's weakest arm and we know it. It has a conditional necessity result that the paper itself calls close to definitional, an unproved sufficiency conjecture, a `[HEURISTIC]` civilizational mapping, and one runnable tool. Unlike the epistemic arm, it has no benchmark series and no falsifications.

**The honest question is not "is the model right" but "is this worth the effort?"** A reviewer who tells us the corridor is a repackaging of established viability/control theory with no new content would be doing us a service; that outcome would let us retire an arm instead of instrumenting it.

**What would refute it:** established results that already cover the constraint-conjunction claim; or a demonstration that the necessity result is definitional in the way we suspect.

---

## Practical notes for a reviewer

- **Nothing needs to be installed to read.** The mathematical claims are self-contained markdown; only the benchmark checks need Python (`numpy`, `matplotlib`).
- **All quoted numbers regenerate from the checked-in code.** CI guards the headline values of v0, v1.9, v1.10, v1.11, and v1.12 on every push, and validates internal links and anchors.
- **Legacy documents are deliberately preserved.** [The Generator Question](../../theory/core/the-generator-question.md) and several essays are marked as superseded research history rather than deleted, so the change of foundation stays auditable. They are not current claims.
- **A negative review is a useful review.** Roughly half of this repository's recent work has been withdrawing its own earlier claims. Being told that a further section should go is the outcome we are set up to act on.

**Contact:** via the repository's GitHub issues.
