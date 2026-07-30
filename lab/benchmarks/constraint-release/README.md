# Constraint Release — Exposure Is Not Reinterpretation

**Status:** exact deterministic toy; repository construction

**Question:** When one small change produces a large competence increase, did
the intervention expose an existing route, create a new route, or merely change
what the evaluator calls success?

## Why this exists

The [situated-stack benchmark](../situated-stack/README.md) already shows that
one fixed controller can receive different scores under different bodies,
interfaces, and environments. This companion benchmark isolates a narrower
identification problem. It holds a transition substrate and fixed policy
constant, changes one constraint bit, and compares the result with a
one-rule observer-lens change. Both interventions raise observed competence
from zero to one. Only one changes physical behavior.

The benchmark is the executable counterpart of
[Latent Competence and Constraint Release](../../../theory/emergence/latent-competence-and-constraint-release.md).
It does not model development, evolution, learning, biological agency, or
neural networks.

## Declared system

A seed permutes four opaque state labels. The transition generator still has
the same named path:

```text
start --approach--> staging --reach-gate--> gate --latent-leg--> goal
```

The task family starts the fixed `advance` policy at each of the three
non-goal states. The reference constraint blocks `latent-leg`; a blocked edge
leaves the system at `gate`. Exact physical success means terminating at
`goal`.

The default seed is 26. It changes only state labels, not path structure. The
tests repeat the experiment across six seeds to ensure that the reported
relations are not an artifact of those labels.

## Four arms

| arm | process change | evaluation change | purpose |
|:---|:---|:---|:---|
| `reference` | `latent-leg` blocked | exact state equality | zero point |
| `constraint-release` | unblock one existing edge | none | exposure candidate |
| `lens-only` | none | identify `gate` with `goal` | reinterpretation control |
| `generator-edit` | replace the transition table with shortcuts | none | creation/import control |

`constraint edits` is Hamming distance between two blocked-edge bit vectors in
this declared encoding. `lens edits` counts the one changed equivalence rule.
Neither is claimed to be Kolmogorov complexity or a representation-independent
measure of intervention cost.

## Run

```bash
cd lab/benchmarks/constraint-release
python constraint_release.py
python constraint_release.py --seed 41
python constraint_release.py --format json
```

The benchmark uses only the Python standard library and has no network
dependency.

## Exact result

```text
Seed: `26`

| arm | generator changed | constraint edits | lens edits | physical success | observed competence | trace changed | classification |
|:---|:---:|---:|---:|---:|---:|:---:|:---|
| `reference` | no | 0 | 0 | 0.000 | 0.000 | no | reference |
| `constraint-release` | no | 1 | 0 | 1.000 | 1.000 | yes | constraint exposure |
| `lens-only` | no | 0 | 1 | 0.000 | 1.000 | no | lens reinterpretation |
| `generator-edit` | yes | 0 | 0 | 1.000 | 1.000 | yes | creation-or-import control |
```

Thus the constraint-release and lens-only arms have the same observed increase,

$$
\Delta C_{\mathrm{obs}} = 1,
$$

but different causal signatures. Constraint release changes every task trace
and exact-goal success while preserving the transition table. The lens-only
arm preserves every physical trace and changes only the equivalence class used
by the evaluator.

## What this demonstrates

- A competence can be latent **relative to** a declared reference constraint
  and admissible release while the transition generator remains fixed.
- A score increase alone cannot distinguish behavioral exposure from observer
  reinterpretation.
- A generator edit can achieve the same endpoint but does not satisfy this
  benchmark's definition of latent exposure.
- Intervention size is encoding-relative: one bit here can unlock three tasks
  only because the fixed substrate and task family already share one gate.

## What it does not demonstrate

- It does not show that the substrate historically acquired the route without
  design, selection, or training.
- It does not allocate explanatory cost uniquely among substrate, path
  geometry, intervention, task choice, and observer lens.
- It does not distinguish competence amplification from exposure in noisy or
  graded systems.
- It does not establish that a real biological novelty is latent rather than
  constructed during reorganization.
- It does not support a Platonic-space interpretation of capability.

## Next falsifiable steps

1. Replace the shared gate with graph ensembles and compare competence gain
   against several intervention codes, not just edge Hamming distance.
2. Add noisy trajectories and ask when a statistical test can distinguish
   amplification from exposure.
3. Let a selector search for releases under a fixed budget; compare random,
   shortest-description, and information-gain interventions.
4. Transport the same lens across task families to test whether the apparent
   competence survives rather than being fitted to this outcome.

## Related

- [Competence, Constraint, and Verification](../../../theory/core/competence-constraint-and-verification.md)
- [Latent Competence and Constraint Release](../../../theory/emergence/latent-competence-and-constraint-release.md)
- [Situated-Stack Benchmark](../situated-stack/README.md)
- [Measurement as Weak Intervention](../../../theory/core/measurement-as-weak-intervention.md)
- [Invariance and Identity](../../../theory/core/invariance-and-identity.md)
- [Embodiment and Goal Decomposition](../../../theory/optimization/embodiment-and-the-non-invariant-decomposition-of-goals.md)
