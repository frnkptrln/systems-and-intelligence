# The Witness Principle: Constructing Distinguishing Interventions

**Status:** working hypothesis with one exact finite lemma and benchmark

**Scope:** This note adds a constructive operator to the repository's model-identification
loop. It does not define intelligence in general, establish a new theory of scientific
discovery, or claim novelty over active learning, experimental design, automata learning,
bisimulation, or abstraction refinement.

**Epistemic status:**

- the definitions below are standard finite-model-identification machinery arranged in the
  repository's vocabulary;
- the coverage–distinction lemma and elementary-cellular-automaton result are exact inside
  their declared deterministic lookup-table setting;
- the proposed relevance to learned world models and representation convergence is a
  repository hypothesis;
- “self-falsifying world model” names an architectural direction, not an accomplished
  system.

---

## The missing move

The [Epistemic Loop](from-trace-to-world-binding.md) already contains observation,
candidate process models, intervention, and revision. The
[inverse-reconstruction benchmark](../../lab/benchmarks/inverse-reconstruction/README.md)
also shows that a prepared state can distinguish models that passive traces leave
equivalent.

In those experiments, however, the useful interventions are supplied by the experimenter.
The remaining constructive question is:

> Given a class of candidate process models, an admissible query language, and a cost
> budget, can a system construct a low-cost query under which the candidates disagree?

This is not the same task as predicting the result of a supplied query. It is the inverse
problem over queries.

## Definitions

Let $\Theta_e$ be the candidate process models consistent with current evidence $e$.
For an admissible query $q \in \mathcal Q$, model $\theta$ induces an outcome law
$P_\theta^q$. Let $d$ be a declared discrepancy and $\varepsilon \ge 0$ a declared
tolerance.

A query $q$ is an **$\varepsilon$-witness** separating
$\theta,\theta' \in \Theta_e$ when

$$
d\!\left(P_\theta^q, P_{\theta'}^q\right) > \varepsilon.
$$

In a deterministic system this reduces to different observed outcomes. In a stochastic
system it requires a statistical test and an error budget; a single differing sample is
not a witness.

Every query induces a partition

$$
\Pi_q(\Theta_e) =
\left\lbrace
[\theta]_q : \theta \in \Theta_e
\right\rbrace,
$$

where two candidates share a block when the query does not distinguish their outcome
laws at the declared tolerance. A conservative one-query score is the largest remaining
block,

$$
R_{\max}(q;\Theta_e) =
\max_{B \in \Pi_q(\Theta_e)} |B|.
$$

For a prior $\mu$ over candidates, an expected residual can also be declared. Under a
uniform prior on a finite class,

$$
R_{\mathrm{avg}}(q;\Theta_e) =
\frac{1}{|\Theta_e|}
\sum_{B \in \Pi_q(\Theta_e)} |B|^2.
$$

Given a query cost $c(q)$ and budget $b$, an exact **witness generator** may choose

$$
q_b^\star
\in
\mathop{\mathrm{arg\,min}}\limits_{q \in \mathcal Q,\;c(q)\le b}
\left(
R_{\max}(q;\Theta_e),
R_{\mathrm{avg}}(q;\Theta_e),
c(q)
\right),
$$

with the tuple read lexicographically. Other applications may replace this objective
with information gain, downstream value, risk, or experiment duration. Those choices are
not interchangeable and must be reported.

The companion note [Decision-Relevant Identifiability](decision-relevant-identifiability.md)
makes that non-interchangeability explicit. Candidate-class reduction and information gain
can prefer a query that resolves nuisance distinctions while a lower-information query
changes the justified action. Witness construction should therefore state whether it is
optimizing identification, information, downstream regret, value of information, or a
viability/safety criterion.

## Coverage–distinction duality

There is one exact result beneath the broader hypothesis.

Let each deterministic candidate $\theta \in \Theta$ be a table
$\theta:X\to Y$. An admissible query $q$ exposes a declared coordinate set
$C(q)\subseteq X$. For two candidates define their disagreement set

$$
D(\theta,\theta') =
\left\lbrace
x\in X : \theta(x)\ne\theta'(x)
\right\rbrace.
$$

Then:

> **Coverage–distinction lemma.** A noiseless query $q$ distinguishes
> $\theta$ and $\theta'$ exactly when
> $C(q)\cap D(\theta,\theta')\ne\varnothing$. It identifies the candidate
> class exactly when $C(q)$ intersects every pairwise disagreement set.

The proof is immediate but useful. If the query exposes no coordinate on which two tables
differ, their observed restrictions are equal. If it exposes at least one such coordinate,
their outcomes differ. Universal identification is therefore a hitting condition over all
remaining candidate pairs.

This separates two structures that information gain alone can hide:

- **distinction geometry:** where the remaining candidates differ;
- **access geometry:** which coordinate sets an admissible intervention can expose, and at
  what cost.

For the full table family $Y^X$, every coordinate must be exposed because some candidate
pair differs only there. For a restricted candidate class, a smaller hitting set may
suffice. A minimum-cost identifying query is therefore a constrained hitting-set problem
over the coverage sets realizable by the intervention interface. A minimum-cost
non-adaptive suite of several queries becomes a set-cover problem over candidate pairs.

The same condition defines a useful quotient of the query space. Write

$$
q \sim_\Theta q'
\quad\Longleftrightarrow\quad
\Pi_q(\Theta)=\Pi_{q'}(\Theta).
$$

Equivalent queries may look different while making exactly the same candidate
distinctions. Search and evaluation should therefore operate on
$\mathcal Q/{\sim_\Theta}$ when possible, assigning each query class the cost of its
cheapest admissible representative. For the full table family, two queries are equivalent
exactly when they expose the same coordinate set. For a restricted family, even different
coverage sets may become equivalent because some table distinctions are absent.

This lemma does not transfer unchanged to partial, stochastic, or noisy observations.
There the binary disagreement set must be replaced by a declared statistical
distinguishability condition.

## The principle

> **Witness Principle — repository hypothesis.** In bounded model identification,
> epistemic capability should be evaluated not only by prediction error or the size of a
> remaining candidate class, but also by the cost of constructing an admissible query
> that reduces that class when reduction matters.

Within this frame, two familiar operations become dual:

- **generalization** merges cases that declared tests do not need to distinguish;
- **discovery** constructs a test that separates a previously merged class.

The equivalence is exact only after the model family, query family, outcome map,
tolerance, and cost have been declared. There is no observer-free witness cost.

The stronger sentence — “intelligence is the ability to generate its own
counterexamples” — is a useful research prompt, not a result established here. A system
may construct excellent distinguishing experiments while lacking broad competence,
autonomous goals, sound values, or viable action.

## A dual interface for world models

A predictive world-model interface has the form

$$
(\text{model}, q) \longmapsto P(o \mid q).
$$

The proposed inverse interface has the form

$$
(\Theta_e,\mathcal Q,c,b) \longmapsto q_b^\star.
$$

The first predicts what follows from an intervention. The second constructs an
intervention at which current candidates predict different things. A
**self-falsifying world model** would couple both directions: it would expose a cheap
place where its present abstraction may fail, execute the admissible query through a
world-coupled referee, and revise from the returned trace.

“Self-falsifying” does not mean that the system can validate its own ontology from inside
itself. The query language, sensors, causal access, costs, and candidate family may all be
misspecified. Matter can answer only the experiment that was actually performed.

## Exact finite baseline

The [Witness-Generation
Benchmark](../../lab/benchmarks/witness-generation/README.md) makes the lemma and operator
concrete for the 256 elementary cellular-automaton rules.

- Candidate class: all 256 rule tables.
- Query: prepare one binary row of width eight and observe its successor.
- Cost: Hamming distance from the all-zero row.
- Generator: exhaustive search over every row at the same cost.
- Baseline: the mean over all equal-cost rows, computed exactly rather than sampled.
- Independent check: an analytical coverage calculation.

The exact frontier is:

| preparation cost | neighborhoods exposed by the best query | worst-case class after best query | mean class after an equal-cost unstructured query |
|---:|---:|---:|---:|
| 0 | 1 | 128 | 128.00 |
| 1 | 4 | 16 | 16.00 |
| 2 | 5 | 8 | 11.43 |
| 3 | 7 | 2 | 5.71 |
| 4 | 8 | 1 | 5.71 |

At cost four, the generated row is a cyclic de Bruijn sequence containing every
three-bit neighborhood. One observed update therefore identifies the rule exactly inside
the declared family. Four ones are not intrinsically intelligent; their arrangement is
informative relative to this rule language and observation map.

### Why the frontier has this form

Let $k(q)$ be the number of distinct three-bit neighborhoods in a query row. Observing one
successor reveals exactly those $k(q)$ bits of the eight-bit rule table. For the full
256-rule family, every outcome block consequently has size

$$
2^{8-k(q)}.
$$

Therefore both the worst-case and uniform expected residual are exactly

$$
R_{\max}(q)=R_{\mathrm{avg}}(q)=2^{8-k(q)}.
$$

The exhaustive query search and this analytical route agree for all 256 width-eight
rows.

The same 256 rows collapse to 21 coverage-equivalent query classes. For the full rule
family these 21 classes induce 21 distinct candidate partitions. The frontier can
therefore be searched over structural query classes rather than raw rows; rotations and
other surface variants do not count as separate epistemic solutions. Some rows with the
same coverage have different preparation costs, so the cheapest representative still
matters.

A width-eight ring has exactly eight cyclic three-bit windows. It exposes all eight
neighborhoods if and only if it is a binary de Bruijn cycle of order three. Each possible
three-bit word then appears once. Exactly four of those words have a central one, so every
such row has Hamming cost four. The cost-four result is thus necessary as well as
sufficient, not merely the best row found by enumeration. The exhaustive check returns
16 linear rows: the rotations of the two binary de Bruijn cycles.

### Why the pairwise profile has this form

Two ECA rules differ on a subset of their eight lookup coordinates. The cheapest query
that reaches a coordinate is its three-bit Hamming weight: cost 0 for `000`, cost 1 for
`001`, `010`, and `100`, cost 2 for `011`, `101`, and `110`, and cost 3 for `111`.
The cheapest witness for a rule pair is therefore the lowest-weight coordinate on which
the rules differ.

Starting with all $\binom{256}{2}=32{,}640$ pairs, the unresolved counts after exposing
successive coordinate layers are

$$
2\binom{128}{2}=16{,}256,\qquad
16\binom{16}{2}=1{,}920,\qquad
128\binom{2}{2}=128,\qquad
0.
$$

Taking successive differences yields the measured profile: cost 0 for $16{,}384$ pairs,
cost 1 for $14{,}336$, cost 2 for $1{,}792$, and cost 3 for $128$. The benchmark now
computes the profile both by exhaustive witness search and by this independent analytical
derivation.

This is a finite receipt, not evidence for the same distribution in learned or continuous
systems. It also exposes the limit of the full-family baseline: once coverage is known,
its optimum is combinatorial rather than learned. A meaningful transfer benchmark must
vary the candidate subset, admissible coverage geometry, or both.

## What becomes testable

### H1 — construction advantage

A learned witness generator should reduce a held-out candidate class with fewer
world-coupled queries than random exploration under matched query, compute, and
intervention budgets.

**Required baseline:** exact or approximate information-gain search over the same query
language. Beating random search alone would not establish a useful learned generator.

### H2 — transfer of separation structure

If the generator has learned reusable structure rather than memorized queries, it should
construct useful witnesses for unseen candidate pairs or related process families without
retraining on every pair.

### H3 — anticipatory refinement

A model that represents where its abstraction can break should adapt to selected
distribution shifts before task failure more cheaply than a model that refines only after
a counterexample arrives.

### H4 — convergence by witness profile

Two systems with dissimilar internal coordinates may still converge operationally if they
construct equivalent distinguishing queries under the same task, intervention family,
tolerance, and cost. Comparing their **witness profiles** may therefore separate
world-imposed convergence from similarity introduced by a representation lens.

Query equivalence makes “equivalent” testable in the finite baseline: systems receive
credit for reaching the same partition of the candidate class, not for reproducing the
same surface row.

This is the bridge to the exploratory note [Intelligence as
Convergence](https://github.com/frnkptrln/systems-and-intelligence/blob/main/ideas/2026-07-23-intelligence-as-convergence.md).
It is not yet a validated representation-similarity measure.

## Relation to existing work

The components are not new:

- Moore's experiments on sequential machines and later finite-state-machine testing study
  distinguishing input sequences (Moore
  [1956](https://www.cs.cmu.edu/~cdm/resources/Moore1956-gedanken-experiments.pdf);
  Lee & Yannakakis
  [1994](https://doi.org/10.1109/12.272431)).
- Angluin's active automata learning uses queries and counterexamples to identify regular
  languages ([1987](https://doi.org/10.1016/0890-5401(87)90052-6)).
- Teaching dimension measures how many selected examples uniquely specify a concept
  within a class (Goldman & Kearns
  [1995](https://doi.org/10.1006/jcss.1995.1003)).
- De Bruijn cycles are classical universal cycles containing every fixed-length word
  exactly once (de Bruijn
  [1946](https://research.tue.nl/en/publications/a-combinatorial-problem/)).
- Local and stochastic distinguishing experiments represent partially observable states
  through action-observation experiments (Collins & Shen
  [2017](https://doi.org/10.1016/j.bica.2017.07.005);
  [2018](https://doi.org/10.1016/j.bica.2018.04.005)).
- Counterexample-guided abstraction refinement uses failed abstract checks to refine a
  model (Clarke et al.
  [2000](https://doi.org/10.1007/10722167_15)).
- Bisimulation, state abstraction, active system identification, causal experimental
  design, and Bayesian information gain all formalize neighboring pieces.
- Recent adaptive state-action abstraction work refines resolution when abstraction error
  becomes limiting ([Rosas 2026](https://arxiv.org/abs/2606.06123)).
- Query-conditioned embodied world models argue for the simplest physical abstraction
  sufficient for a supplied intervention query ([Thorpe et al.
  2026](https://arxiv.org/abs/2605.30542)).

The repository-specific move is narrower: put **construction of the distinguishing query**
between candidate-class maintenance and intervention, give it an explicit cost, separate
candidate distinction geometry from intervention access geometry, and ask whether learned
systems can produce that query before failure. The finite lemma and benchmark are a
baseline for that question, not a novelty claim about their ingredients.

## Failure conditions

Retire or narrow the principle if:

- witness generation adds no predictive or adaptation benefit over ordinary experimental
  design under matched budgets;
- a learned generator only memorizes fixed query templates and fails on unseen candidate
  relations;
- the claimed advantage disappears after intervention risk, latency, sensor noise, and
  computation are counted;
- the candidate family has to contain the answer for every reported success while
  misspecification remains untested;
- witness profiles merely reproduce the chosen representation metric;
- “self-falsifying” becomes a rhetorical substitute for external verification.

## Placement in the loop

The refined epistemic movement is:

    Trace -> Candidate Class -> Witness Construction -> World-Coupled Query
          -> Class Refinement or Family Failure -> Revision -> new Trace

The old loop remains a useful reader path. This note names one operator inside it; it does
not add a third research spine.

## Read next

1. [From Trace to World-Binding](from-trace-to-world-binding.md)
2. [Measurement as Weak Intervention](measurement-as-weak-intervention.md)
3. [Witness-Generation Benchmark](../../lab/benchmarks/witness-generation/README.md)
4. [Decision-Relevant Identifiability](decision-relevant-identifiability.md)
5. [World Models and VLA](../ai/world-models-and-vla.md)
6. [Open Problem 14: Learned Witness Construction](../reference/open-problems.md#open-problem-14-learned-witness-construction)
