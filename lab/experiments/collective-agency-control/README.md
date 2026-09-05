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
