---
title: Representation Changes Reconstruction Difficulty
date: 2026-08-09
status: exploratory note
---

# Representation Changes Reconstruction Difficulty

**Status:** Exploratory note — not a repository claim.

**Trigger.** Michael Farmer's 2026 paper on representational grounding suggests that changing representation can expose invariants that were already present but hard to use.

**Question.** Can a change of representation make trace → generator reconstruction substantially easier without adding evidence?

If the transformation is invertible, the information content need not change, while the search geometry, accessible invariants, and effective description length can change dramatically. That suggests separating **identifiability** from **representational accessibility** and from raw computational cost. A non-invertible representation is more dangerous: it may discard distinctions and manufacture apparent identity.

**Probe.** Hold the candidate family and evidence fixed while encoding the same finite systems as adjacency matrices, edge lists, random relabelings, and derived invariant tables. Measure reconstruction or identity-witness recovery under matched budgets. Include decoys that share weak invariants, and verify proposed correspondences independently.

**Open tension.** A gain only counts if the representation does not smuggle in the target identity.

**Source:** Michael Farmer (2026), *Abduction Without a Body? Representational Grounding and the Abduction Loop for Scientific Hypothesis Generation*, arXiv:2608.02505.

**Connections.**

- [From Trace to Generator](../theory/emergence/trace-to-generator.md)
- [The Witness Principle](../theory/core/the-witness-principle.md)
- [Invariance and Identity](../theory/core/invariance-and-identity.md)
