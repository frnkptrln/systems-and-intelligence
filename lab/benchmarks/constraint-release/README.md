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

## Graph ensemble calibration — 19 October 2026

The original four-arm result above is unchanged. This extension takes a small,
finite step toward the first open experiment below: does the size of a release
determine its competence gain once the shared-gate construction is replaced?
It enumerates a declared graph family rather than sampling more labelings of
the original path.

**Setting.** States `0, 1, 2` each have one outgoing `advance` edge, whose
target can be any of `0, 1, 2, 3`; goal `3` is absorbing. Thus there are
`4^3 = 64` labeled functional graphs, including self-loops and cycles. Every
comparison fixes the graph, policy, three equally weighted starts, and exact
goal lens. A reference mask `B` blocks source edges; a nonempty subset `R` of
`B` is released. A blocked edge stalls permanently. Success means reaching
`3` within three steps. That horizon is sufficient by construction: a longer
path would repeat a non-goal state and remain in a deterministic cycle.

All eight reference masks are considered; the empty mask admits no nonempty
release. There are `3^3 - 2^3 = 19` admissible `(B, R)` pairs per graph and
**1,216 paired cases** in total. Gain is the number of additional successful
starts divided by three. Previously successful starts cannot be lost in this
static, one-action family; nonnegative gain is a structural property here.

**Three conditional costs.** Source labels address the edges to release.

| cost | definition | what is counted |
|:---|:---|:---|
| Hamming edits | `k = size(R)` | changed constraint bits |
| fixed-address payload | `2k` bits | two bits per released source |
| prefix-address payload | sum of codeword lengths | source `0/1/2` uses `0/10/11` |

The graph, reference, codebook, and number `k` are free side information;
framing and the work of choosing a release are excluded. These are declared
payloads and an edit metric, not minimum message lengths, full intervention
costs, or Kolmogorov complexity. Fixed-address cost only rescales Hamming
count, so their identical rankings supply no independent robustness evidence.

**Exact enumeration.** Counts below classify each case by its competence gain.

| released edges `k` | cases | gain `0` | gain `1/3` | gain `2/3` | gain `1` | mean gain | zero-gain fraction |
|:---|---:|---:|---:|---:|---:|:---|:---|
| 1 | 768 | 522 | 195 | 42 | 9 | `17/128` | `87/128` |
| 2 | 384 | 201 | 84 | 75 | 24 | `17/64` | `67/128` |
| 3 | 64 | 27 | 12 | 9 | 16 | `13/32` | `27/64` |

These are exact counts under the counting measure on `(graph, B, R)`, not
estimates from independent observations. References admitting more release
subsets receive more weight; the three `k` rows contain different populations.
Their increasing means do not isolate a causal dose response to release size.
Labeled graphs also count separately when related by an isomorphism.

Equal costs do not determine equal gains even within one graph and reference.
For the chain `g = (1, 2, 3)`, with `B = {1, 2}`, releasing `{1}` gives gain
`0`, whereas releasing `{2}` gives gain `1/3`. Both interventions cost one
Hamming edit, two fixed-address bits, and two prefix-address bits. The position
of the remaining blockage matters as well as the release size.

**Transported recodings.** All six permutations of the non-goal states carry
the graph, blocked edges, released edges, and starts together, keeping goal
`3` fixed. Across **7,296 transported cases**, gain is invariant, while prefix
payload cost changes in **3,072**. For example, the same chain with
`B = R = {2}` has full gain `1`; swapping labels `0` and `2` preserves that
gain but changes prefix cost from two bits to one. The physical intervention
is the same under transport; the shorter codeword belongs to another label.
Pooled cost/gain histograms remain invariant because each permutation maps
the complete ensemble bijectively onto itself. This aggregate symmetry does
not make an individual intervention's code length invariant, and the six
recodings are not independent replications.

The extension therefore gives a finite calibration and explicit witnesses:
release count alone does not determine gain, and one concrete payload code
changes under relabeling of the same physical release. It does not allocate
causal credit uniquely or establish a general complexity–competence law.
Only the constraint varies within each pair; the original lens-only and
process-edit controls remain the separate identification demonstration above.
There is no learning, historical selection model, biological system, or LLM.
Other graph families, task weights, codes, noise, and adaptation remain open.

Run from this directory using only the Python standard library:

```bash
python graph_ensemble.py
python graph_ensemble.py --format json
```

The dated [enumeration record](results/graph-ensemble-2026-10-19.json) preserves
the exact aggregate output, inspectable witnesses, and reproduction metadata.

## Next falsifiable steps

1. Extend the finite graph calibration above to other transition families,
   task distributions, and intervention codes; the four-state enumeration
   addresses a bounded instance, leaving the broader comparison open.
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
