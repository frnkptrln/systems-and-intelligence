# Exact control: predictive parity does not identify organization

**Status:** exploratory constructive control, specified 2026-09-05 before execution.

Can perfect joint prediction and macro persistence distinguish uncoupled,
locally repairing, and globally coupled dynamics? This small control examines
the sufficiency of those measurements. It does not implement or freeze the
separate [Collective Agency Benchmark](../../benchmarks/collective-agency/README.md).

## Setting and measures

There are six Boolean components, split into two triplets. The initial ensemble
is uniform on the four codewords `(a,a,a,b,b,b)`, with independent unbiased
`a,b`. This preparation correlates components within each triplet; uncoupled
updates do not mean statistically independent initial states.

Three deterministic updates use the same state space:

- **Uncoupled toggle:** each component flips its own bit.
- **Local repair:** each triplet becomes three copies of its own complemented
  majority bit.
- **Cross-group repair:** each triplet becomes three copies of the other
  triplet's complemented majority bit.

Both macro readings are declared here: representative parity `x[0] XOR x[3]`
and majority parity `majority(x[:3]) XOR majority(x[3:])`. They agree on the
initial ensemble and all its unperturbed successors.

For each update and reading, enumerate the ensemble to compute next-macro
entropy, mutual information from each current triplet and their joint state,
and macro temporal mutual information, all in bits. Also report the mean
conditional entropy of a component's next bit given its own current bit.
The information is measured across the uniform ensemble. Macro parity is
constant within each unperturbed trajectory; its entropy along any one such
trajectory would be zero.

These are exact-distribution information calculations, not fitted predictors,
held-out scores, a general PID estimator, or an NTIC estimate.

For each of the four initial states, flip each of the six bits once, apply one
update, and compare with the unperturbed successor: 24 interventions per model.
Record full-state restoration and preservation of each macro reading. These
are transient bit errors, not membership removal or general viability tests.
Enumerate all 64 states separately to identify which input components can
causally change each output and the largest strongly connected component.

## Prediction and failure condition

The predicted result is identical unperturbed joint predictive information
(1 bit), individual-triplet information (0 bits), and macro persistence
(1 bit) for all three updates and both readings. After a bit error, uncoupled
toggle should restore 0/24 full states and preserve representative parity in
16/24 cases, while preserving majority parity in 24/24. Both repairing updates
should restore 24/24 full states and preserve both macro readings in 24/24.

The causal graphs should have respectively 0, 12, and 18 off-diagonal edges,
with largest strongly connected components of size 1, 3, and 6. If exhaustive
enumeration disagrees with any of these predictions, the proposed witness
fails and the discrepancy must be resolved before drawing its conclusion.

## Run

From the repository root, using only Python's standard library:

```bash
python lab/experiments/collective-agency-control/run_control.py \
  --output lab/experiments/collective-agency-control/result.json
python tests/test_collective_agency_control.py
```

The definitions use familiar parity and repetition-code constructions. This
is a deliberately transparent measurement control, not a mathematical novelty
claim. Identical state spaces do not imply equal computational or communication
budgets. A centralized implementation can reproduce every transition here;
there is no demonstrated macro-intervention advantage or agency verdict.

## Observed result — 2026-09-05

Exhaustive enumeration matches every prediction; the pinning test passes.
The machine-readable output is in [`result.json`](result.json).

| Update | Off-diagonal causal edges | Largest coupled component | Full state restored | Representative parity preserved | Majority parity preserved |
| --- | ---: | ---: | ---: | ---: | ---: |
| Uncoupled toggle | 0 | 1 | 0/24 | 16/24 | 24/24 |
| Local repair | 12 | 3 | 24/24 | 24/24 | 24/24 |
| Cross-group repair | 18 | 6 | 24/24 | 24/24 | 24/24 |

All three systems have the predicted 1 bit of joint information and macro
temporal information, with 0 bits from either triplet alone. Those measurements
cannot identify their different causal organizations. Even perfect macro
preservation under these errors can come from a robust observation rule over
a system that repairs none of its component errors. Local own-bit prediction
separates cross-group repair (1 bit of uncertainty) from the other two (0 bits),
so the indistinguishability applies to the stated macro measurements, not all
possible observations.

For subsequent agency experiments, include this uncoupled control and report
component recovery alongside macro persistence. Robust coarse-graining can be
useful; it should not be counted as evidence of internal repair or agency.

## Information distribution and known erasures

**Status:** companion static calibration, first executed locally on 2026-09-05
and subsequently integrated here. This is not an additional preregistered run.
The original parity code, result and pre-execution predictions above are unchanged.

[`information_distribution.py`](information_distribution.py) enumerates four
encodings over GF(5). The target `S` and random symbols `R,Q` are independent
and uniform. Each of three components stores one field symbol. All arithmetic
in this table is modulo 5.

| Case | Stored symbols `(X1,X2,X3)` | Equiprobable configurations |
| --- | --- | ---: |
| Broadcast | `(S,S,S)` | 5 |
| Essential first component | `(R,S-R,S-R)` | 25 |
| Any two suffice | `(S+R,S+2R,S+3R)` | 25 |
| All three required | `(S+R+Q,S+2R+4Q,S+3R+9Q)` | 125 |

These are 180 exhaustively enumerated configurations, not sampled trials.
Probabilities are exact counts; logarithms are floating-point, in bits.
`H(S) = log2(5)`. The essential-component and two-of-three cases match component
count, local alphabets and entropies, target distribution, random-symbol budget,
and joint component entropy `2*log2(5)`. Broadcast and three-of-three are
calibration controls, not joint-entropy-matched comparisons. Encoding, decoding
and communication costs are not measured.

The normalized joint-over-best-single gain is
`G = [I(X1,X2,X3;S) - max_i I(Xi;S)] / H(S)`. It is **not** a PID synergy
measure and does not compare against an equally informed centralized observer.
Separately, the script computes the two-source Williams–Beer `I_min` PID for
each of the three source pairs, using target-averaged minimum specific
information for redundancy. Its mean synergy is divided by `H(S)`. This is
not a three-source PID or the proposed temporal estimator on adjacent pairs.

A coalition is any subset of the three stored symbols, including the empty
set. The decoder knows the encoding and the identity of every available
symbol. Its optimal success probability is obtained by choosing the most
frequent target conditional on each observed tuple. A minimal reconstructing
coalition succeeds with probability one and has no strictly smaller subset
that does so. The output reports all eight subset accuracies, every minimal
coalition, all three known single-erasure positions, their mean, and their
worst case rather than hiding the essential component in an average.

### Static result

The complete output is in
[`information-distribution-result.json`](information-distribution-result.json).

| Case | G | Mean pair synergy / H(S) | Minimal reconstructing coalitions | Worst known single-erasure accuracy |
| --- | ---: | ---: | --- | ---: |
| Broadcast | 0 | 0 | `{1}`, `{2}`, `{3}` | 100% |
| Essential first component | 1 | 2/3 | `{1,2}`, `{1,3}` | 20% |
| Any two suffice | 1 | 1 | `{1,2}`, `{1,3}`, `{2,3}` | 100% |
| All three required | 1 | 0 | `{1,2,3}` | 20% |

All four intact encodings reconstruct perfectly. The 20% cases leave `S`
uniform over five values; no decoder can do better from the surviving symbols.
For the essential-component case, losing components 1, 2 and 3 yields 20%, 100%
and 100% respectively (73.333...% under uniform single erasure). For two-of-three,
every pair determines the intercept of `f(x)=S+R*x`; for three-of-three, three
points determine the intercept of `f(x)=S+R*x+Q*x^2`, while two leave it uniform.
The script checks these statements with explicit interpolation as well as
conditional counts.

Thus maximal `G` can coexist with either single-erasure fragility or tolerance.
Zero synergy in **every pair** can coexist with full reconstruction from the
triple. In the latter control even each pair's entire target mutual information
is zero: the blind spot is source order, not just a choice of PID redundancy.
This does not turn the joint-over-single gain into a general higher-order PID.

### Reproduce the static control

The script uses Python 3.10+ and only the standard library. It runs the original
seven calibration tests before writing the result. The repository test module
also pins the saved output and all coalition and erasure-location values.

```bash
python lab/experiments/collective-agency-control/information_distribution.py \
  --output lab/experiments/collective-agency-control/information-distribution-result.json
python -m pytest tests/test_collective_agency_control.py \
  tests/test_collective_information_distribution.py -q
```

## Reading the controls together

| Question | Witness | Consequence for the benchmark |
| --- | --- | --- |
| Does joint information identify causal coupling? | Parity dynamics: equal joint information, different causal graphs. | Inspect interventions or causal dependencies separately; statistical dependence is not dynamical coupling. |
| Does joint information identify erasure tolerance? | Essential-component versus two-of-three encodings: equal G, different loss profiles. | Report which subsets reconstruct and which loss locations defeat reconstruction. |
| Does a pairwise null exclude joint information? | Three-of-three: all pair target information is zero, full-group information is H(S). | Declare source order; pair-only tests cannot exclude higher-order dependence. |
| Does macro persistence establish repair? | Uncoupled toggle with majority readout: 24/24 macro preservation, 0/24 full-state restoration. | Report observable retention and physical component recovery separately. |

The two controls do not use the same target, source partition, perturbation,
or information measure: one predicts a next macrostate under a known dynamical
rule and tests bit errors, the other decodes a statically encoded target under
known erasures. Their scores are not pooled or ranked on one common scale.
They jointly reject the substitution of one measurement axis for another;
they do not establish a collective agent or confirm the full benchmark's H1–H5.

Static decoding supplies no time evolution or active repair. The encoder and
ideal observer are assumed available; decoder failure, unknown error positions,
incorrect shares, resources, goals and agency are outside its scope. Likewise,
the parity control does not establish general viability or a budget-matched
macro-intervention advantage. Passive robustness can be useful without being
self-maintenance. The benchmark's freeze candidate and execution permissions
are unchanged.

## References for the static constructions

- Adi Shamir (1979), [*How to share a secret*](https://doi.org/10.1145/359168.359176),
  Communications of the ACM 22(11):612–613. Polynomial threshold construction;
  the small instances used here are explicitly enumerated and decoded.
- Paul L. Williams & Randall D. Beer (2010),
  [*Nonnegative Decomposition of Multivariate Information*](https://arxiv.org/abs/1004.2515).
  Two-source PID with minimum-specific-information redundancy. No claim that
  this estimator is a uniquely correct decomposition.

These familiar constructions are measurement controls, not mathematical novelty claims.
