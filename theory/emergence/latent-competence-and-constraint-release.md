---
title: Latent Competence and Constraint Release
date: 2026-07-30
status: working definition and experimental programme
---

# Latent Competence and Constraint Release

**Status:** Working definition and experimental programme over verified
biological observations. The definition does not imply a Platonic ontology,
substrate-independent intelligence, or absence of historical selection.

**Why this page exists:** The repository has language for emergence,
embodiment, affordances, and test-relative equivalence, but lacked a precise
way to distinguish a capacity exposed by changed constraints from a capacity
created by adaptation or merely attributed by a changed observer.

## 1. Three epistemic levels

Claims about surprising biological competence often move too quickly through
three levels:

1. **Observation.** A system performs robustly in a configuration for which
   that current configuration was not the direct target of design, training,
   or selection.
2. **Interpretation.** The substrate and its developmental history support a
   repertoire of reachable dynamics wider than the reference embodiment
   expresses.
3. **Metaphysics.** The physical system accesses patterns that exist
   independently in a Platonic space.

Selected versions of levels 1 and 2 can be tested. Level 3 is a philosophical
proposal. Levin's own Platonic-space essay presents it as speculative; the
repository does not adopt it as a scientific commitment.

## 2. Definition relative to a reference

Let $P_X$ be a typed process associated with substrate $X$. A **coupling
configuration** is

$$
\kappa=(B,E,C,O,A,\Gamma),
$$

where $B$ is embodiment, $E$ environment, $C$ coupling, $O$ observation
operators, $A$ available actions, and $\Gamma$ admissibility constraints. Fix
an observer lens $\ell$, task family $\tau$, and competence relation
$\mathcal C(P_X,\kappa;\ell,\tau)$.

**Definition — latent competence.** A capacity $c$ is latent relative to
reference $\kappa_0$ and admissible transformation family $\mathcal T$ if

$$
c\notin\mathcal C(P_X,\kappa_0;\ell,\tau)
$$

and

$$
\exists T\in\mathcal T:
c\in\mathcal C(P_X,T\kappa_0;\ell,\tau),
$$

with $P_X$, $\ell$, and $\tau$ held fixed.

Every term is load-bearing:

- Without a reference, “latent” has no contrast class.
- Without $\mathcal T$, any arbitrary replacement could count as exposure.
- Without fixed $P_X$, learning or construction can be mistaken for release.
- Without fixed $\ell$ and $\tau$, evaluator relabeling can be mistaken for
  behavior.
- Without a time boundary, reorganization during the intervention can be
  hidden inside the phrase “same substrate.”

This is an operational definition, not a historical explanation. A route can
be latent now because evolution, training, or development built it earlier.

## 3. Exposure, amplification, creation, reinterpretation

For a reference run $r_0$ and intervention run $r_1$, record at least:

$$
\left(
\Delta\mathrm{Trace},
\Delta\mathrm{Process},
\Delta\kappa,
\Delta\ell,
\Delta\mathcal C
\right).
$$

| Diagnosis | Required evidence | Typical confound |
|:---|:---|:---|
| **exposure** | changed behavior under admissible $\kappa$ change; fixed declared process and lens | hidden learning or damage during the intervention |
| **amplification** | graded effect increases with a fixed outcome definition | thresholding a continuous behavior into presence/absence |
| **creation or import** | operative process structure changes and the new structure is necessary | declaring every internal reorganization “the same substrate” |
| **reinterpretation** | trace is unchanged while only $\ell$ changes | a coarse lens hides a real causal difference |

Endpoints alone do not identify the case. The
[Constraint-Release Benchmark](../../lab/benchmarks/constraint-release/README.md)
is deliberately constructed so that exposure and reinterpretation have the
same score increase and different trace signatures.

## 4. What the biological evidence warrants

Several primary results motivate the definition:

- Blackiston and Levin showed that ectopic eyes grafted to Xenopus tadpole
  tails can support light-mediated learning even when the normal eyes are
  absent. A later intervention study found that serotonergic stimulation
  promotes innervation and visual learning through posterior grafts.
- Kriegman, Blackiston, Levin, and Bongard built Xenobots from Xenopus cells;
  later work demonstrated kinematic replication in a designed environment.
- Gumuskaya and collaborators showed that adult human airway epithelial cells
  can self-construct into motile Anthrobots and reported a neural-wound repair
  assay.
- Regeneration and bioelectric-control studies show that multicellular systems
  can restore or redirect large-scale pattern after perturbation.

These are heterogeneous findings. “Novel current configuration” does not mean
“no relevant evolutionary history.” Epithelial cells, cilia, sensory
transduction, wound responses, and developmental plasticity are evolved
systems. The experiments demonstrate behavioral or morphogenetic capacities
under unusual couplings; they do not by themselves locate all explanatory
information or prove a shared cognitive mechanism.

Primary sources and claim-level qualifications are listed in the
[source and integration ledger](../../meta/research-alignment/related-work-map.md#latent-competence-and-diverse-cognition).

## 5. Relations to existing concepts

**Affordance.** An affordance is relational: what an environment offers a
particular embodied system. Constraint release can create a new affordance
without changing the internal process, but not every affordance is a latent
competence. The latter also requires a task and observed capacity.

**Exaptation and spandrels.** A structure selected for one role can support
another. Historical exaptation is one explanation for present latent
competence, not a synonym for the operational definition.

**Degeneracy and redundancy.** Different structures can yield the same
function; one structure can yield different functions across contexts.
Degeneracy can make competence robust under perturbation, while redundancy can
mask which route carried it.

**Emergence.** Weak-emergence language says a macrobehavior follows from local
dynamics but is not transparent from a compact description. Latency asks a
different question: which admissible intervention makes that behavior
reachable and detectable?

**Substrate independence.** A competence preserved across a declared family of
substrates supports an invariance claim. One surprising substrate does not
establish substrate independence.

**Embodiment.** The
[effective-goal quotient](../optimization/embodiment-and-the-non-invariant-decomposition-of-goals.md)
already shows that reachable trajectories and a lens jointly determine which
goals are behaviorally distinct. Latent competence is the forward counterpart:
change reachability and a previously absent task distinction can become
expressed.

**Observer-relative equivalence.** The
[invariance framework](../core/invariance-and-identity.md) requires the test
family and equality notion. A lens-only increase is therefore a valid change
in *reported* competence but not evidence of behavioral exposure.

## 6. Where does the explanatory cost live?

Suppose an intervention with short description $d(T)$ exposes a behavior with
long trace description $d(r)$. It is tempting to infer that the substrate
“contained” the behavior. At most, one can write an encoding-relative
bookkeeping inequality such as

$$
K(r)
\leq
K(P_X)+K(\kappa_0)+K(T)+K(\tau)+K(\ell)+O(1).
$$

Here $K$ is description length under a declared universal machine or practical
code. This inequality does not allocate causal credit uniquely. Shared
regularities can move description length among terms, and a different
factorization can shift the apparent cost.

Candidate explanations include:

- historical selection, training, or development;
- generic state-space geometry or dynamical attractors;
- environmental regularity that does much of the computation;
- an intervention aligned with a pre-existing bottleneck;
- an observer lens fitted to the outcome; and
- hidden complexity in what was called a “simple” substrate.

The scientific task is comparison by intervention and ablation, not choosing a
single term by intuition.

## 7. Minimal protocol

A latent-competence claim should report:

1. the fixed process and what “fixed” excludes;
2. reference coupling $\kappa_0$;
3. admissible transformation family $\mathcal T$;
4. task family $\tau$ and observer lens $\ell$;
5. physical traces before and after intervention;
6. learning, damage, and reorganization during the intervention;
7. lens-only, sham-intervention, and process-edit controls;
8. more than one intervention-cost encoding; and
9. a historical explanation audit.

Without item 7, exposure and reinterpretation remain observationally
confounded.

## 8. Open questions

- What process boundary remains stable during biological reorganization?
- Can exposure and fast construction be separated when the intervention
  triggers learning?
- Which transformations are admissible without trivializing latency?
- Does intervention complexity predict competence gain across graph or
  developmental ensembles?
- Can a transported lens distinguish a robust new capacity from evaluator
  fitting?
- When an altered embodiment exposes preferences or avoidance, what moral
  uncertainty protocol should govern further intervention?

## Related

- [Competence, Constraint, and Verification](../core/competence-constraint-and-verification.md)
- [The Agent Is Not Where the Model Ends](../identity/the-agent-is-not-where-the-model-ends.md)
- [Embodiment and Goal Decomposition](../optimization/embodiment-and-the-non-invariant-decomposition-of-goals.md)
- [Measurement as Weak Intervention](../core/measurement-as-weak-intervention.md)
- [Trace to Generator](trace-to-generator.md) — active typed construction and model-identification question
- [Weak and Strong Emergence](emergence-downward-causation.md)
- [Constraint-Release Benchmark](../../lab/benchmarks/constraint-release/README.md)
