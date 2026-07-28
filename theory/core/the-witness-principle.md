# The Witness Principle: Constructing Distinguishing Interventions

**Status:** working hypothesis with one exact finite baseline

**Scope:** This note adds a constructive operator to the repository's model-identification
loop. It does not define intelligence in general, establish a new theory of scientific
discovery, or claim novelty over active learning, experimental design, automata learning,
bisimulation, or abstraction refinement.

**Epistemic status:**

- the definitions below are standard finite-model-identification machinery arranged in the
  repository's vocabulary;
- the elementary-cellular-automaton result is exact inside its declared family and query
  language;
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
\left\{
[\theta]_q : \theta \in \Theta_e
\right\},
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
\operatorname*{arg\,min}_{q \in \mathcal Q,\;c(q)\le b}
\left(
R_{\max}(q;\Theta_e),
R_{\mathrm{avg}}(q;\Theta_e),
c(q)
\right),
$$

with the tuple read lexicographically. Other applications may replace this objective
with information gain, downstream value, risk, or experiment duration. Those choices are
not interchangeable and must be reported.

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
Benchmark](../../lab/benchmarks/witness-generation/README.md) makes the operator concrete
for the 256 elementary cellular-automaton rules.

- Candidate class: all 256 rule tables.
- Query: prepare one binary row of width eight and observe its successor.
- Cost: Hamming distance from the all-zero row.
- Generator: exhaustive search over every row at the same cost.
- Baseline: the mean over all equal-cost rows, computed exactly rather than sampled.

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

The pairwise witness profile is also exact. Among all $32{,}640$ unordered pairs of
distinct rules, the cheapest separating row has cost 0 for $16{,}384$ pairs, cost 1 for
$14{,}336$, cost 2 for $1{,}792$, and cost 3 for $128$. This is a finite receipt,
not evidence for the same distribution in learned or continuous systems.

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

This is the bridge to the exploratory note [Intelligence as
Convergence](https://github.com/frnkptrln/systems-and-intelligence/blob/main/ideas/2026-07-23-intelligence-as-convergence.md).
It is not yet a validated representation-similarity measure.

## Relation to existing work

The components are not new:

- Angluin's active automata learning uses queries and counterexamples to identify regular
  languages ([1987](https://doi.org/10.1016/0890-5401(87)90052-6)).
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
between candidate-class maintenance and intervention, give it an explicit cost, and ask
whether learned systems can produce that query before failure. The finite benchmark is a
baseline for that question, not a novelty claim about its ingredients.

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
4. [World Models and VLA](../ai/world-models-and-vla.md)
5. [Open Problem 14: Learned Witness Construction](../reference/open-problems.md#open-problem-14-learned-witness-construction)
