---
title: "Decision-Relevant Identifiability — When Uncertainty Matters"
date: "2026-08-10"
status: "Working Note"
scope: >
  Separates model identification from decision sufficiency. Defines access-relative
  indistinguishability, a decision-regret radius over a remaining candidate class, and the
  distinction between information gain and value of information.
epistemic_status: >
  Conceptual synthesis built from standard statistical decision theory and finite model
  identification. The finite examples below are exact receipts, not claims of novel mathematics.
related:
  - theory/core/mathematical-axioms.md
  - theory/core/the-witness-principle.md
  - theory/core/measurement-as-weak-intervention.md
  - theory/core/from-trace-to-world-binding.md
  - theory/reference/open-problems.md
  - lab/benchmarks/inverse-reconstruction/README.md
  - lab/benchmarks/witness-generation/README.md
failure_conditions:
  - Treating class size as a universal proxy for decision quality after this note distinguishes them.
  - Treating information gain, identification, and decision value as interchangeable objectives.
  - Claiming that a zero decision-regret radius identifies the true hidden model.
  - Ignoring the declared query, action, task, loss, prior, tolerance, or access geometry.
---

# Decision-Relevant Identifiability

*When does unresolved model uncertainty actually matter for action?*

## Result in one page

The repository's process-identification programme asks which candidate process models remain
consistent with evidence and which observations or interventions can distinguish them. The
[Witness Principle](the-witness-principle.md) adds the constructive question: which admissible query
should be generated to refine the remaining class?

This note adds a prior question:

> **Does the remaining ambiguity matter for the decision we are about to make?**

A large candidate class can be decision-trivial if every remaining model supports the same action.
A two-model class can be decision-critical if the models recommend incompatible actions. Therefore
candidate-class size, posterior entropy, information gain, and downstream decision value are not
interchangeable objectives.

The resulting loop is not simply

$$
\text{trace}\to\Theta_e\to\text{witness}\to\Theta_{e'}.
$$

For task-directed action it is more accurately

$$
\text{trace}
\to \Theta_e
\to \text{decision relevance}
\to \text{witness if needed}
\to \Theta_{e'}.
$$

The useful target is not complete hidden-state recovery. It is enough information to choose an
acceptable action under the declared task, loss, and risk criterion.

---

## 1. Access-relative identifiability

Let $\Theta$ be a declared class of candidate process models and $\mathcal Q$ the complete set of
queries available to an observer. A query may represent passive observation, a prepared state,
an intervention, or an adaptive experiment, provided its causal and observational interface is
explicit.

For each model $\theta$ and query $q$, let $P_\theta^q$ be the induced outcome law. Define

$$
\theta\sim_{\mathcal Q}\theta'
\quad\Longleftrightarrow\quad
P_\theta^q=P_{\theta'}^q
\qquad\text{for every }q\in\mathcal Q.
$$

Two models related by $\sim_{\mathcal Q}$ are indistinguishable under the observer's entire declared
access geometry. This is stronger than saying that they fit the evidence collected so far. It says
that no admissible query in the declared interface separates them.

If access expands from $\mathcal Q$ to $\mathcal Q'$ with

$$
\mathcal Q\subseteq\mathcal Q',
$$

then the induced partition can only stay the same or become finer. More access may distinguish more
models; it cannot erase a distinction that was already available.

The hidden-extension proposition in the
[Foundations Reconstruction](mathematical-axioms.md#7-a-result-the-foundation-forces-non-identifiability)
is a limiting case. If a hidden component $Z$ is independent, observations discard it, and the
permitted interventions act only through the visible $X$ component, then changing the hidden
transition on $Z$ need not change any accessible outcome law. The hidden dynamics are not merely
hard to infer: they lie outside the distinguishing power of that interface.

A finite controlled-system check on 2026-08-10 made this explicit. Two models were given different
hidden-state dynamics while actions and sensors touched only the visible state. Across all 16 action
sequences of length four, every visible outcome distribution was identical. The residuals were
exactly zero for every query sequence.

The operational rule is therefore:

> **No witness exists outside the access geometry.**

Intervention breaks observational equivalence only where the intervention-and-observation interface
reaches a difference between the remaining candidates.

---

## 2. Identification is not yet decision sufficiency

Let $B\subseteq\Theta_e$ be the candidate class remaining after current evidence. Let $A$ be the
available action set for a declared task. For model $\theta$ and action $a$, let $V_\theta(a)$ be the
expected task value, and let

$$
V_\theta^*=\max_{a\in A}V_\theta(a).
$$

Define the **decision-regret radius** of the class by

$$
\rho_D(B)=
\min_{a\in A}
\max_{\theta\in B}
\left[V_\theta^*-V_\theta(a)\right].
$$

This quantity asks for the smallest worst-case regret achievable without resolving which member of
$B$ is the true model.

A particularly important case is

$$
\rho_D(B)=0.
$$

Then at least one available action is optimal under every model in the remaining class. The hidden
model remains unidentified, but the ambiguity is irrelevant to this decision.

This does **not** imply that the models are equivalent for another task, horizon, action set, loss,
or affected party. Decision sufficiency is task-relative in exactly the same sense that
identifiability is access-relative.

### Exact finite counterexample: class size is not decision risk

Two finite examples make the separation unavoidable.

**Case A — large class, harmless ambiguity.** Eight distinct candidate models remain. Every model
assigns value 1 to action $a_1$ and value 0 to action $a_2$:

$$
V_\theta(a_1)=1,\qquad V_\theta(a_2)=0
\qquad\forall\theta\in B.
$$

Then

$$
|B|=8,
\qquad
\rho_D(B)=0.
$$

Under a uniform prior, perfect model identification has zero value for this choice because the same
action is optimal before and after identification.

**Case B — tiny class, critical ambiguity.** Only two models remain:

$$
V_{\theta_1}=(10,0),
\qquad
V_{\theta_2}=(0,10).
$$

Then

$$
|B|=2,
\qquad
\rho_D(B)=10.
$$

Under a uniform prior the best action before more evidence has expected value 5, while perfect
identification gives expected value 10. The value of perfect information is therefore 5.

Hence

$$
\boxed{|B|\text{ is not a monotone proxy for decision risk.}}
$$

A larger epistemic equivalence class can be safer to act under than a much smaller one.

---

## 3. Information gain is not value of information

The same distinction applies to query selection.

Suppose eight candidate models differ in three binary coordinates

$$
(d,n_1,n_2).
$$

The coordinate $d$ determines which of two actions is correct. The nuisance coordinates $n_1,n_2$
do not affect the decision.

Consider two exact queries under a uniform prior.

### Query N — identify nuisance structure

The query reveals $(n_1,n_2)$ but not $d$. It returns two bits of information about the model:

$$
I(\Theta;Q_N)=2\text{ bits}.
$$

It shrinks each posterior block from eight candidates to two. Nevertheless both values of $d$ remain
possible in every block, so the best achievable decision value is unchanged. Its decision value of
information is

$$
\mathrm{VOI}_D(Q_N)=0.
$$

### Query D — identify the decision boundary

The second query reveals only $d$. It returns one bit:

$$
I(\Theta;Q_D)=1\text{ bit}.
$$

The posterior class remains size four, larger than under Query N. But the correct action is now
known. In the symmetric unit-reward example, expected decision value rises from $1/2$ to 1:

$$
\mathrm{VOI}_D(Q_D)=\frac12.
$$

Therefore a query can have **more information gain, produce a smaller candidate class, and still be
less useful for action** than another query.

The objectives

- candidate-class reduction,
- posterior entropy reduction,
- information gain,
- worst-case regret reduction,
- expected value of information,
- viability or safety value,

must therefore be reported separately unless an explicit theorem or assumption makes them coincide.

---

## 4. Decision-relevant witnesses

The [Witness Principle](the-witness-principle.md) defines a witness as a query under which remaining
candidate models predict distinguishable outcomes. Its current objective can minimize residual
class size, but it already permits downstream value or risk as alternative objectives.

The present note sharpens why that choice matters.

A **decision-relevant witness** is an admissible query whose possible outcomes refine the candidate
class in a way that reduces a declared decision criterion, for example expected regret or
worst-case regret. A query that separates models only along nuisance dimensions is an identifying
witness but not a decision-relevant witness for that task.

One possible robust objective is

$$
q_D^*
\in
\mathop{\mathrm{arg\,min}}_{q\in\mathcal Q,\,c(q)\le b}
\mathbb E_{o\sim P^q}
\left[
\rho_D(B_{q,o})
\right],
$$

where $B_{q,o}$ is the candidate class remaining after observing outcome $o$. A Bayesian version
would maximize ordinary expected value of information. A safety-critical version could use a
viability loss or constraint-violation risk instead.

These objectives are not interchangeable. Which one is appropriate is part of the task definition,
not a consequence of the process foundation.

This suggests a discipline for active model refinement:

> **Do not resolve uncertainty merely because it is resolvable. Resolve the uncertainty whose
> resolution changes the justified action, risk, or viability assessment.**

---

## 5. Relation to the repository's existing results

### Process-model identification

The inverse-reconstruction benchmark measures where candidate classes remain broad because of noise,
partial observability, missing coverage, family uncertainty, or misspecification. Those are
identification results. This note adds a downstream question: which distinctions inside the class
matter to the action being optimized?

### Model exploitation and uncertainty marking

The v1.3–v1.7 benchmark sequence shows that committing to an unmarked class member can produce an
optimizer's-curse wedge and that class-aware planning or ensembles reduce self-deception. The
present result does not replace those findings. It says that **class size alone is insufficient to
predict the downstream cost of uncertainty**. The relevant geometry is how remaining model
disagreements intersect the action-value landscape.

### Weakness and commitment

Holding an equivalence class open is epistemically honest, but not every open distinction deserves
equal resources. A weak representation can remain intentionally unresolved when all supported
models induce the same acceptable action. Conversely, even a nearly collapsed class deserves a
witness when the last surviving distinction crosses a decision or viability boundary.

### Viable Corridor

For viability-sensitive systems the natural question may be narrower than reward optimality:

> Do all remaining models agree that this action stays inside the declared viable region?

If yes, complete identification may be unnecessary for that action. If not, a distinguishing query
can have high safety value even when its Shannon information gain is small.

---

## 6. What this note does not claim

- It does **not** propose a new theory of decision making. Regret and value of information are
  standard decision-theoretic constructions.
- It does **not** say that model identification is unimportant. Identification may matter for future
  tasks, explanation, science, transfer, audit, or safety even when the present action is unchanged.
- It does **not** make truth task-relative. The model that generated the world is whatever it is;
  only the sufficiency of our distinctions for a chosen decision is task-relative.
- It does **not** equate robust action with intelligence. A fixed reflex may have zero regret in a
  tiny task while lacking broad competence.
- It does **not** justify ignorance when unmodeled harms, affected parties, distribution shift, or
  misspecification could change the action ranking.
- It does **not** imply that low information gain means low value. The finite example shows exactly
  the opposite can occur.

---

## 7. Immediate empirical consequence

The smallest useful next experiment is already defined by the distinction above.

Extend the finite Witness-Generation Benchmark with a task/value layer and compare, under matched
query cost:

1. a query selected for candidate-class reduction or information gain;
2. a query selected for expected decision value or regret reduction.

Construct cases with nuisance coordinates and decision coordinates so that the objectives disagree.
Measure class size, information gain, regret, value of information, and realized reward separately.

The finite example in this note predicts that an information-maximizing query can dominate in bits
and class reduction while losing decisively on downstream value.

If the two selectors always coincide under the tested structures, the proposed distinction adds no
empirical leverage there. If they diverge as the exact example predicts, the benchmark gains a new
axis: **epistemic resolution versus decision-relevant resolution**.

---

## Rule

The Witness Principle asks whether the system can construct a query that separates its candidate
models. This note adds the prior accounting question:

> **Before buying a distinction, state what decision that distinction can change.**

Or, more compactly:

> **Not every uncertainty must be resolved. The important uncertainty is the uncertainty that can
> change the justified action.**
