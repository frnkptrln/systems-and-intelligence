# Identification Claims — Model-Identification Arc

**Lane:** Repository Meta  
**Status:** Draft — a synthesis index proposed on 2026-09-02; which entries are load-bearing is a maintainer decision  
**Scope:** A minimal claim set for the model-identification arc, derived only from what four existing artifacts already assert: the [Inverse-Reconstruction Benchmark](../../lab/benchmarks/inverse-reconstruction/README.md), [The Witness Principle](../../theory/core/the-witness-principle.md), [Decision-Relevant Identifiability](../../theory/core/decision-relevant-identifiability.md), and [Active Identifiability](../../lab/experiments/active_identifiability/README.md). Companion to [Core Claims](core-claims.md), which covers the viability arc and the identity branch.  
**Purpose:** Keep the arc's measured and exact results precise, challengeable, and linked to artifacts, in the same shape as the viability register.  
**Created:** 2026-09-02  
**Last reviewed:** 2026-09-02  
**Review trigger:** a new benchmark version, a change to any cited artifact's own status line, or a maintainer decision on this register's status.

---

## Relation to the Project

The [Foundations Reconstruction](../../theory/core/mathematical-axioms.md) supplies the shared
process language. The model-identification arc then asks, under declared model families, evidence,
intervention access, target equivalence, and cost, which candidate process models an observer can
distinguish. The claims below are what the arc's artifacts already establish inside their declared
testbeds. None is a universal law. Each names the testbed it was measured in, and each is narrower
than the earlier [Generator Question](../../theory/core/the-generator-question.md)'s universal
framing, which the reconstruction superseded and which that document retains as research history.

Evidence kinds used below:

- *measured* — a run with frozen numbers, guarded by a regression test where one is named;
- *exact lemma* — a proof or exact finite computation inside a declared setting;
- *argument* — a stated rule or interpretation without a decisive measurement;
- *design draft* — a protocol that exists but has not run.

These extend the kinds used in [Core Claims](core-claims.md) for the reason that register gives:
reading the bullets should be enough to tell the artifacts apart.

---

## Claim 1: Known-Family Inversion Is Cheap; Hardness Belongs to Named Dials

**Claim:** With a known model family, full observability, and clean data, inversion is cheap in the
benchmark's three testbeds: exact rule tables, sub-percent Kuramoto parameter error, and Boids
weights within 3%. The benchmark therefore does not support a uniform "inverse is hard" reading.
Where hardness appears, it is attributed to a named dial — noise amplified by differentiation,
partial observability, coverage, or family search — not to inversion as such.

**Not obvious because:** The repository's earlier spine treated the forward/inverse asymmetry as a
universal law. The measurement demoted it to "hard exactly here" ([Feynman Mode](feynman-mode.md),
receipt 2). Standard system identification already knew that the known-family case is cheap; what
this claim adds is the relocation of the repository's own hardness talk onto dials the benchmark can
turn.

**Artifacts:**

- *measured* — [Inverse-Reconstruction Benchmark, "The honest finding"](../../lab/benchmarks/inverse-reconstruction/README.md#the-honest-finding)
  (v0, Kuramoto / elementary CA / Boids; the near-exact and blow-up bands are guarded by
  [`tests/test_benchmark_headlines.py`](../../tests/test_benchmark_headlines.py); the exact figures
  are the README's frozen results)
- *measured* — [Benchmark v1.2, family search](../../lab/benchmarks/inverse-reconstruction/README.md#v1-part-2-family-search-the-wall-measured-run)
  (the family-search dial: enumeration cost grows with description size in one declared DSL while
  verification stays flat; the enumeration-cost figures are frozen in the README without a named
  regression test, while v1.2's Occam-is-chance identity is pinned by
  [`tests/test_benchmark_v1_headlines.py`](../../tests/test_benchmark_v1_headlines.py))
- *argument* — [The Generator Question](../../theory/core/the-generator-question.md), "Current
  status (2026-07-30)" banner, and [Foundations Reconstruction §10.2](../../theory/core/mathematical-axioms.md#102-revise),
  which require the asymmetry to state its conditions

**Current status:** v0 results are frozen: Kuramoto error on $K$ is 0.0% at $\sigma = 0$ with full
observation; CA rule-bit accuracy is 100% for flip probability $p \le 0.2$; Boids weights are
recovered within 3% at $\sigma = 0$. Family search is measured for one DSL and one size-ordered
enumerator, and the README limits the reading itself: "a measured property of this DSL and
enumerator, not a P-vs-NP result or a lower bound for other search algorithms." None of the four
source artifacts disagrees. [What This Project Does NOT Claim](../../theory/reference/what-this-project-does-not-claim.md),
items 2 and 4, state the same boundary from the negative side.

**Failure condition:** Weakened if a testbed in the repository's own families shows known-family,
fully observed, clean-data recovery failing for a reason not attributable to one of the named dials;
or if the benchmark's effects disappear under its own preregistered controls, the strict failure the
[Related Work Map](../research-alignment/related-work-map.md) names for this row. Restating the
claim as a universal cheapness law would be a failure of the claim, not a strengthening.

---

## Claim 2: Noise × Differentiation and Partial Observability Are Separately Measured

**Claim:** Noise amplified by differentiation and partial observability are distinct degradation
sources with separately measured curves. Inferring velocities and accelerations by differencing
noisy Boids positions degrades weight recovery from 3% to 789% relative error within
$\sigma = 0.03$. Unobserved Kuramoto oscillators bias the reconstructed mean field, and the error on
$K$ grows monotonically as the observed fraction shrinks (0.5% at $f = 1$, 13% at $f = 0.6$, 21% at
$f = 0.3$, 41% at $f = 0.15$, all at the sweep's fixed angle noise $\sigma = 0.03$), while angle
noise under full observation is a separate curve (0.0% at $\sigma = 0$ to 27% at $\sigma = 0.3$).

**Not obvious because:** One label, "noisy and partial data," would hide that the two sources enter
through different mechanisms — a differencing operator that amplifies noise by roughly $1/dt^2$,
versus a biased field computed from an observed subset — and therefore call for different
remedies. Coverage is a third source with its own signature and is carried by Claim 3.

**Artifacts:**

- *measured* — [Inverse-Reconstruction Benchmark, results (v0)](../../lab/benchmarks/inverse-reconstruction/README.md#results-v0-seeds-averaged)
  (seeds averaged; the bands are guarded by
  [`tests/test_benchmark_headlines.py`](../../tests/test_benchmark_headlines.py); the exact figures
  are the README's frozen results)

**Current status:** frozen v0 results. The README states its own scope: it measures finite search
and identification problems, with hand-rolled least squares in v0; a cross-method comparison
against SINDy and PySR is listed in the benchmark's open roadmap and has not been run.

**Failure condition:** Weakened if, in the same testbeds, the two curves collapse to one under a
shared explanation, or if the monotone dependence on observed fraction fails to replicate under the
benchmark's own seeds.

---

## Claim 3: Identifiability Is Relative to a Candidate Family and an Intervention Set

**Claim:** What can be identified is relative to the declared candidate family and the admissible
intervention set. Passive observation of a declared family can plateau permanently: rule 90 from a
single seed leaves a consistent-model class of size 8 however long the orbit is watched, while
one-bit flips collapse the class within about ten queries and one prepared de Bruijn row collapses
it in one step (watching < perturbing < preparing). Two generators with the same observational
covariance are separated by $do(X = x)$ and by nothing observational. Agreement at one observable
does not establish shared mechanism. Disagreement at one readout does not establish different
underlying states.

**Not obvious because:** "More data" is the default remedy for underdetermination, and it is the
remedy that buys nothing here. The formal reason is the hidden-extension proposition in
[Foundations Reconstruction §7](../../theory/core/mathematical-axioms.md#7-a-result-the-foundation-forces-non-identifiability):
a discarded independent component preserves every observed trace law, so trace agreement can never
by itself select a mechanism, and intervening only on the visible component cannot reveal it
either, so access assumptions must be stated as well. The readout half turns the same point onto
the measurement channel: a difference in one channel may be a property of that channel.

**Artifacts:**

- *measured* — [Benchmark v1.1, the intervention experiment](../../lab/benchmarks/inverse-reconstruction/README.md#v1-part-1-the-intervention-experiment-run)
  (CA rule 90: class 8 under passive observation, collapse under flips and preparation; rule 0: the
  frozen exception, where single-bit flips never collapse the class; Kuramoto on its locked
  attractor: passive error on $K$ about 83%, one phase kick 3%, eight kicks 0.3%)
- *measured* — [Active Identifiability, Track A causal witness](../../lab/experiments/active_identifiability/causal_witness.py)
  (two linear-Gaussian generators with identical covariance; expected information gain about
  generator identity 0.0397 bit at $do(X=0)$ rising to 0.6338 bit at $do(X=3)$; cost-adjusted
  optimum approximately $x = 2.5504$; the committed reference is reproduced by
  [`tests/test_active_identifiability.py`](../../tests/test_active_identifiability.py))
- *exact lemma* — the hidden-extension proposition, which
  [Decision-Relevant Identifiability §1](../../theory/core/decision-relevant-identifiability.md)
  cites as its limiting case, and that note's finite controlled check of 2026-08-10: two models with
  different hidden-state dynamics, actions and sensors touching only the visible state, identical
  visible outcome distributions across all 16 action sequences of length four, residuals exactly
  zero. From these the note states the operational rule "No witness exists outside the access
  geometry" (*argument*)
- *argument* — [Active Identifiability README](../../lab/experiments/active_identifiability/README.md),
  whose opening statement of relativity to a candidate family and an admissible intervention set is
  quoted in the last two sentences of the claim; its "Interpretation boundary" section adds the
  per-channel rules
- *design draft* — [Active Identifiability, Track B multi-readout study](../../lab/experiments/active_identifiability/README.md)
  (720 primary and 240 extension records; protocol `0.1-draft`, `model_calls_authorized: false`;
  the exploratory compatibility probes of 2026-08-22 did not pass the smoke gate)

**Current status:** The family-and-intervention half is measured in the CA and Kuramoto testbeds
and exact for the linear-Gaussian pair. The benchmark limits its own reading: "This supports
perturbation as a method in these testbeds; it does not by itself validate the repository's identity
instruments or establish a general hierarchy for every causal system." The readout half is stated as
an interpretation boundary and imports five controls from an external precursor result, in which
persona framing was "measurable but not dominant or measurement-invariant"; nothing in this
repository has measured that half, because Track B has not run and its protocol authorizes no model
calls. The artifacts do not disagree. They carry different evidence levels for the two halves of the
claim, and this register records the split rather than averaging it.

**Failure condition:** Weakened if a passive readout in a declared family reliably collapses a
class that the declared intervention set cannot, which would contradict the access-geometry rule;
if the intervention hierarchy reverses in one of the benchmark's own testbeds under its declared
interfaces; or if Track B, run under a frozen protocol, finds single-channel differences predicting
cross-channel differences so reliably that factorizing the readout adds nothing. The proposition
itself is elementary and cannot fail; its relevance would narrow if a declared family together with
a minimality criterion made trace agreement sufficient for that family.

---

## Claim 4: The Coverage–Distinction Lemma, at Its Own Scope

**Claim:** For a deterministic lookup-table candidate family with noiseless queries, a query
distinguishes two candidates exactly when the coordinate set it exposes intersects their
disagreement set, and identifies the class exactly when it hits every pairwise disagreement set.
For the 256 elementary cellular-automaton rules with one prepared row of width eight and Hamming
cost from the all-zero row, the exact frontier is a worst-case class of 128, 16, 8, 2, and 1 at costs
0 to 4; the cost-4 universal queries are exactly the 16 rotations of the two binary de Bruijn cycles,
so cost 4 is necessary and sufficient; the 256 rows form 21 coverage-equivalent query classes; and
the pairwise witness profile is 16,384, 14,336, 1,792, and 128 rule pairs at minimal costs 0 to 3.
The lemma does not transfer unchanged to partial, stochastic, or noisy observation.

**Not obvious because:** Information gain alone hides the separation between where candidates
differ (distinction geometry) and what an admissible intervention can expose (access geometry). The
exact frontier also bounds what a learned witness generator could claim: for the full family the
optimum is combinatorial, so a learned system earns interest only on varied candidate subsets or
access geometries.

**Artifacts:**

- *exact lemma* — [The Witness Principle](../../theory/core/the-witness-principle.md), section
  "Coverage–distinction duality"
- *measured* — [Witness-Generation Benchmark](../../lab/benchmarks/witness-generation/README.md)
  (exhaustive enumeration with an independent analytical cross-check; pinned by
  [`tests/test_witness_benchmark.py`](../../tests/test_witness_benchmark.py))
- *argument* — [The Witness Principle](../../theory/core/the-witness-principle.md) as a repository
  hypothesis, with its four testable hypotheses H1–H4
- *design draft* — [Learned-Searcher Benchmark](../../lab/benchmarks/learned-searcher/README.md)
  (protocol frozen by digest; execution target unregistered; not run; reached through Open
  Problem 14, which the Witness Principle cites)

**Current status:** The lemma and the ECA frontier are exact and cross-checked by two independent
routes. The Witness Principle's own status line is "working hypothesis with one exact finite lemma
and benchmark"; its hypotheses on construction advantage, transfer, anticipatory refinement, and
convergence by witness profile are untested, and
[Open Problem 14](../../theory/reference/open-problems.md#open-problem-14-learned-witness-construction)
holds the learned-construction question. The [Concept Registry](concept-registry.md) row
"Witness / distinguishing query" carries the same split.

**Failure condition:** For the lemma, only a disagreement between the enumerated and analytical
routes inside the declared setting. For the wider principle, the note's own conditions: no benefit
over ordinary experimental design under matched budgets; a learned generator that only memorizes
fixed query templates; an advantage that disappears once intervention risk, latency, sensor noise,
and computation are counted; success that requires the candidate family to contain the answer
while misspecification remains untested; witness profiles that merely reproduce the chosen
representation metric; and "self-falsifying" used as a rhetorical substitute for external
verification.

---


---

## What This Register Does Not Do

- It adds no experiment and re-runs nothing; every number above is a frozen result of the cited
  artifact.
- It does not rank the claims or decide which are load-bearing. That decision belongs to the
  maintainer, who on 2026-09-02 chose a separate file over a second part of
  [Core Claims](core-claims.md) (decision D1).
- It does not extend any claim beyond the testbed its artifact declares. The open questions the
  four sources point to are [Open Problems 11 and 14](../../theory/reference/open-problems.md) and
  the benchmark's own roadmap; Problems 15 and 18 are adjacent, and whether they belong to this arc
  is a maintainer decision.
- It adds one Concept Registry row, for *readout*, because the statement of Claim 3 uses the term
  (maintainer decision D3, 2026-09-02). *Access geometry* appears only in a failure condition and a
  rationale; it resolves to the Witness Principle and Decision-Relevant Identifiability and has no
  row of its own, and whether it needs one is left to the maintainer.
- It does not promote any exploratory note in `ideas/`.

## Maintenance Rule

The rule from [Core Claims](core-claims.md) applies unchanged: a precise statement, a non-obvious
implication, at least one artifact link marked with its evidential kind, a current-status line
saying what the artifacts establish, and a failure condition. A claim with no artifact does not
enter this register. If two artifacts disagree, the disagreement is recorded as the current status
rather than resolved here.

---

## Candidates (Not Yet Claims)

Entries whose home artifact is a working note without a pinned measurement or a test-guarded
lemma. They keep the claim shape so that promotion is a status decision, not a rewrite. The
placement follows maintainer decision D2 of 2026-09-02: the home document of the entry below,
[Decision-Relevant Identifiability](../../theory/core/decision-relevant-identifiability.md), carries
the status "Working Note"; its finite receipts are exact but no benchmark or regression test pins
them, unlike the lemma behind Claim 4.

### Candidate C1: Class Size Is Not Decision Risk; Information Gain Is Not Value of Information

**Claim:** Candidate-class size is not a monotone proxy for decision risk, and information gain is
not value of information. Exact finite receipts: eight remaining candidates with decision-regret
radius 0, against two remaining candidates with radius 10; a query that returns two bits and
shrinks the posterior class to two candidates with zero decision value, against a query that
returns one bit, leaves four candidates, and fixes the correct action. Candidate-class reduction,
posterior entropy reduction, information gain, worst-case regret reduction, expected value of
information, and viability or safety value must therefore be reported separately unless an explicit
theorem or assumption makes them coincide.

**Not obvious because:** The benchmark's v1.3–v1.7 results price unmarked uncertainty by class
size: the optimizer's-curse wedge grows with the class. This candidate adds that class size alone does
not predict the downstream cost of uncertainty; what matters is how the remaining disagreements
intersect the action-value landscape.

**Artifacts:**

- *exact lemma* — [Decision-Relevant Identifiability §2–§3](../../theory/core/decision-relevant-identifiability.md)
  (the two finite counterexamples)
- *argument* — the same note's rule, "Before buying a distinction, state what decision that
  distinction can change"
- *design draft* — the same note's §7, a task/value layer on the witness benchmark comparing a
  class-reduction selector with a decision-value selector under matched query cost (unrun)
- *argument* — [Open Problem 11](../../theory/reference/open-problems.md#open-problem-11-trace-to-generator-reconstruction),
  the decision-relevance constraint that recoverable class size and decision sufficiency be
  reported separately

**Current status:** The note's own status is "Working Note"; the [Concept Registry](concept-registry.md)
records it as formalized from standard decision theory with exact finite receipts and no novel
mathematics claimed. The proposed task/value layer is unrun. The note states what it does not
claim: it does not make truth task-relative, and it does not justify ignorance when unmodeled harms,
affected parties, distribution shift, or misspecification could change the action ranking.

**Failure condition:** From the note itself: if the class-reduction selector and the decision-value
selector always coincide under the tested structures, the distinction adds no empirical leverage
there. Treating a zero regret radius as identification of the true model, or class size as a
universal proxy, would be a misuse of the claim rather than a refutation of it.
