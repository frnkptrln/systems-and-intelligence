# Log 017: Provenance Depth and the Verification Economy

**Mode:** Applied Architecture
**Status:** WORKING NOTE
**Date:** 2026-06-10
**Scope:** A certificate architecture for knowledge claims in a regime where generation is cheap and verification is substrate-bounded. Operationalizes the concept introduced narratively in `fiction/15_the_exchange_rate.md`.
**Depends on:** `theory/core/the-generator-question.md`, `theory/veto/substrate-veto-thermodynamics.md`, `papers/viable-corridor.md` (P7, hard vs. soft budgets), `lab/benchmarks/inverse-reconstruction/README.md`, `016_the-runtime-is-part-of-the-generator.md`

---

## Problem Statement

Claim generation is approaching zero marginal cost; verification is not. A physical verification — an experiment, a cohort, a long-running rig — is bounded by energy, time, and matter (the substrate constraint), and therefore grows at best linearly while candidate claims grow with compute. Every knowledge-bearing institution now faces the same queue problem, and the same temptation: let *predicted* verification stand in for *performed* verification.

The failure is not the prediction. Calibrated predictors are useful. The failure is **letting the prediction trade at par with the performance** — erasing, at the interface, the difference between a claim that matter has voted on and a claim that models agree about. Once the two are priced identically, Gresham's law operates: expensive performed claims stop being produced, the corpus fills with consensus, and predictors trained on that corpus certify the consensus. The loop closes silently. By construction, it closes *first* at the frontier — exactly where claims are out-of-distribution and prediction is least trustworthy.

This log proposes the minimal architecture that keeps the difference visible: **provenance depth as a mandatory, first-class field on every claim certificate.**

## Core Concept: Provenance Depth (d)

Model every certified claim as a node in a provenance DAG whose edges are inference steps. Define:

> **d(claim) = the minimum number of edges between the claim and the nearest *performance node* in its provenance DAG.**

A *performance node* is an event in which the claim (or its direct premise) was exposed to its referent — matter allowed to vote. Indicative scale:

- **d = 0** — physically performed *and* independently replicated.
- **d = 1** — physically performed once (no independent replication).
- **d = 2** — direct statistical inference over d≤1 data (e.g. meta-analysis; no new contact).
- **d = 3** — simulation whose model class was validated against d≤1 data *for this regime*.
- **d ≥ 4** — model-mediated layers: ensemble concordance, predicted-verify, model-evaluating-model. Each additional layer of testimony adds one.

Two hard rules make d meaningful:

1. **d is monotone along inference.** No transformation of claims (aggregation, consensus, re-derivation) may *decrease* d. Only a new performance event resets it.
2. **d never disappears.** It is rendered wherever the claim is rendered — like the assay-mark on silver, not like a footnote nobody reads.

**Domain note (mathematics/software):** a machine-checked formal proof (e.g. a Lean/mathlib artifact) counts as a performance node *for claims whose referent is the formal system itself* — the proof checker is the substrate being contacted. It does not ground claims about the physical world. This distinction is the deduction/construction boundary; see `theory/computation/construction-vs-deduction.md`.

## Failure Conditions (anti-patterns this architecture targets)

1. **Par-trading (the Throughput Rule).** Waiving performance because predicted-verify confidence is high, *without re-pricing*. A waiver is a soft budget on epistemics; the Viable Corridor's P7 result applies directly — soft (routable) budgets fail under rising capability, and generation capability is rising.
2. **Circular grounding (data incest).** A predictor trained on a corpus that contains model-generated claims certifying further model-generated claims. Detectable as provenance DAGs that cycle through model nodes without performance nodes.
3. **Consensus-as-ground.** Treating agreement among N models trained on overlapping corpora as N independent confirmations. Concordance across shared training data is one observation, not N.
4. **Calibration laundering.** Reporting in-distribution calibration as if it covered the frontier. The certificate must carry the *reference class* against which confidence was calibrated, so out-of-distribution use is visible.
5. **Invisible decay.** A d=0 stamp from a drifted regime (old instruments, changed populations, evolved deployment context) silently retaining full value. Performance events should carry timestamps and regime descriptors; consumers decide staleness — the certificate's job is to make it decidable. (Cf. Log 016: the runtime is part of the generator; the *measurement context* is part of the performance.)

## Minimal Certificate Schema

```
claim_id          : content hash of the claim statement
provenance        : DAG reference (nodes typed: PERFORMANCE | INFERENCE | MODEL)
d                 : int   — min hops to nearest PERFORMANCE node (rule-checked)
performance_meta  : for d=0/1 — when, where, by whom, regime descriptors, replication count
reference_class   : for model-mediated nodes — calibration set + measured error rate
confidence        : calibrated p (meaningful only relative to reference_class)
countersignature  : commit authority for the d-stamp (human / institutional anchor)
issued / regime   : timestamps + drift descriptors (consumer-side staleness)
```

The countersignature line is deliberate: stamping d=0 is a *commit* in the Accords sense — the act that anchors silicon claims to the physical layer is exactly the act that should carry biological/institutional commit authority.

## Design Rules

1. **Never hide d.** Rendering d is more important than rendering confidence — confidence is a model's self-report; d is a structural fact about the DAG.
2. **Price verification explicitly.** If performance capacity is scarce (it is), run a visible market or queue for it. Scarcity that is priced produces capacity investment; scarcity that is waived produces fiat.
3. **Reserve frontier capacity.** A fixed fraction of physical verification capacity is allocated to out-of-distribution claims *even when their predicted-verify confidence is high* — precisely because that is where prediction degrades and where the predictor's future calibration data must come from. This is an exploration budget for the verification system itself.
4. **Audit the loop, not the node.** The dangerous failure is not one bad certificate; it is a DAG-population whose performance-node fraction trends to zero. Publish the aggregate: *what fraction of circulating certificates, weighted by economic reliance, sits at d ≤ 1?* That single time series is the system's epistemic-solvency indicator.
5. **Degrade loudly.** When throughput pressure forces waivers (it will), waived certificates must be visibly distinct instruments — different rendering, different price — not discount-rate footnotes on the same instrument.

## Real-World Anchors (this is less fictional than it reads)

- The **replication crisis** is a d-collapse discovered after the fact: large literatures whose effective d was higher than their citations assumed.
- **Benchmark contamination** and model-generated text entering training corpora are circular-grounding (anti-pattern 2) operating today.
- **C2PA / content-provenance** standards and **SBOM** (software bill of materials) are the same architecture for media and code respectively; this log is the analogue for *evidential support* — an evidence bill of materials.
- **Registered reports** and replication prizes are existing mechanisms that re-price d=0 work upward.

`[SPECULATIVE]` The economic reading (verification capacity as the scarce backing of a knowledge economy, d as its assay-mark) extends beyond science governance — but quantifying it requires the measurement programme this repo does not yet have.

## Open Forks

1. **Decay function.** Should d itself age (d=0 from 1995 ≠ d=0 from 2025), or should staleness remain a consumer-side judgment over `performance_meta`? Current lean: keep d structural and timeless, surface regime drift separately — mixing the two re-hides information.
2. **Weighting replications.** Is d=0 binary (replicated: yes/no) or graded by replication count and independence? Graded is more honest, harder to standardize.
3. **Who funds the frontier reserve?** Design Rule 3 is a public good; every private actor prefers to spend verification capacity in-distribution. This is a γ-question (regulation), not a protocol question.
4. **Formal-substrate boundary cases.** Simulation-based inference *is* the performance for some claims (a property of an algorithm, demonstrated by running it). The PERFORMANCE node type needs a referent taxonomy: physical / formal / computational — with explicit rules for which referents ground which claim types.

## Relation to the Repository

The Comptroller of `fiction/15_the_exchange_rate.md` is the narrative stress test of exactly this architecture's absence: a calibrated, honest, Chord-class predictor whose nominations were counted as elections. The trace→generator spine supplies the mechanism (a predictor trained on traces learns what *passes*, not what *is*; cf. the equivalence-class result in `lab/benchmarks/inverse-reconstruction/`). The substrate veto supplies the constraint that makes the temptation permanent (verification capacity cannot scale like generation). P7 supplies the regime claim: soft epistemic budgets fail under rising capability. This log is where those threads become a schema someone could implement.
