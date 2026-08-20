---
title: Verification as Reverse Pressure
date: 2026-07-30
status: working bridge between empirical replay and formal proof
---

# Verification as Reverse Pressure

**Status:** Working structural bridge. Replay and formal proof are not
identified; the common correction schema is proposed and its failure modes are
explicit.

**Why this page exists:** The repository distinguished construction from
deduction and argued that self-improvement needs a referee. It had not yet
formalized the reverse direction: a verifier can expose defects in the
definitions, interfaces, and process that generated the candidate.

## 1. Approval is the least interesting output

A verifier is often pictured as a terminal gate:

$$
\text{candidate}\longrightarrow
\lbrace\text{accept},\text{reject}\rbrace.
$$

In a research loop, the useful output is richer:

$$
\mathrm{Verify}_{\mathcal Q}(z,H)
\longrightarrow
(b,e),
$$

where $z$ is a proposal, $H$ is the evidence or obligation history,
$\mathcal Q$ is the test protocol, $b$ is a status, and $e$ is a
counterexample, failed obligation, mismatch trace, or unresolved condition.

The evidence $e$ can update the proposal process itself:

$$
\theta_{t+1}=
\mathrm{Revise}(\theta_t,e_t,H_t).
$$

This is **verification as reverse pressure on construction**. It requires an
informative failure interface. A Boolean rejection without localization may
provide too little pressure; a permissive verifier may provide false
stability.

## 2. Replay as a declared relation

Let a transition hypothesis predict

$$
M_t(o_i,a_i)=\widehat{o}_{i+1}
$$

and let the retained history be

$$
H_t=\langle(o_i,a_i,o_{i+1})\rangle_{i=0}^{t-1}.
$$

For a declared equivalence relation $\sim_{\mathcal Q}$, define replay fit:

$$
\mathrm{Replay}_{\mathcal Q}(M_t,H_t)=1
$$

if and only if

$$
M_t(o_i,a_i)\sim_{\mathcal Q}o_{i+1}
\quad
\text{for every }(o_i,a_i,o_{i+1})\in H_t.
$$

Exact equality is one choice of $\sim_{\mathcal Q}$. It is appropriate when
every encoded difference is causally or operationally relevant. It is harmful
when incidental pixels, serialization details, or nondeterministic order are
forced into the theory. Conversely, a coarse equivalence can erase a
safety-relevant distinction.

A replay report should therefore name:

- observation representation;
- equality or tolerance;
- deterministic and stochastic treatment;
- retained versus forgotten history;
- on-policy versus counterfactual transitions;
- resource budget; and
- the revision action triggered by each failure.

Passing replay means consistency with retained tests, not truth, causal
identification, or transfer.

## 3. The ARC-AGI-3 case

Rodionov's initial 2026 system maintains an executable Python world model,
verifies it against earlier observations, periodically simplifies it, and
plans through it. The later ablation compares four nested agents:

1. textual baseline;
2. executable model without replay;
3. executable model with scheduled simplification; and
4. fixed-interface executable model with simplification and exact replay.

The ablation prevents three overstatements:

- executable representation was not uniformly better than text;
- component effects varied by model and reasoning setting; and
- the verification treatment ranked first in the four main settings but
  consumed substantially more resources.

The strongest reported public-set result used a model released after the games
and had no held-out evaluation. It is evidence of public-set saturation, not a
general ARC-AGI-3 or AGI claim.

The repository extraction is architectural: keep world models revisable,
expose contradictions, price verification, and compare exact with
equivalence-class replay.

## 4. Proof can debug the specification

Let $D_t$ contain definitions, axioms, theorem statements, interfaces, and
translation rules. A prover explores consequences:

$$
D_t
\longrightarrow
\mathrm{Consequences}(D_t).
$$

A failed attempt can have several causes:

| Failure source | Example | Legitimate response |
|:---|:---|:---|
| false target | theorem does not follow | weaken or reject the target |
| missing assumption | intended domain restriction absent | add and justify the assumption |
| weak or wrong definition | definition admits unintended models | repair definition and recheck corpus |
| representation mismatch | library and local concepts do not align | add a proved translation layer |
| search failure | theorem is true but automation cannot find proof | improve tactics, decomposition, or budget |
| implementation defect | parser, elaborator, or kernel interface fails | repair tooling; do not alter mathematics to hide it |

Thus a failed proof is not automatically evidence that the definitions are
wrong. It is a diagnostic that narrows hypotheses only when the prover's
soundness, completeness limits, and resource budget are understood.

Urban's 2026 Megalodon report describes a long-running LLM–proof-assistant
feedback loop that produced roughly 130,000 lines of formal topology in about
two weeks. Bryant, Huerta y Munive, Kaliszyk, and Urban later report a complete
Isabelle/HOL formalization of Munkres' general-topology chapters. Their own
qualitative audit matters here: the proofs check, but definitions are sometimes
weak, assumptions redundant, and integration with Isabelle's existing
topology library awkward.

That result demonstrates both directions:

- machine checking can stabilize a very large generated artifact; and
- successful proof does not remove the need to revise definitions,
  interfaces, organization, and abstraction.

## 5. One correction schema, two semantics

| Empirical agent | Formal mathematics | Relation |
|:---|:---|:---|
| world model | definitions and axioms | analogy |
| observed transition | theorem statement or required property | analogy |
| replay mismatch | countermodel, failed obligation, or proof impasse | correspondence only when diagnostic evidence is available |
| model revision | definition/specification revision | structural correspondence |
| simplification | refactoring or abstraction | analogy |
| regression history | proof corpus | structural correspondence |
| new action in the world | new lemma or tactic | analogy, not identity |

A general proposal-process loop is

$$
P_{\theta_t}
\longrightarrow
z_t
\longrightarrow
\mathrm{Verify}_{\mathcal Q}(z_t,H_t)
\longrightarrow
e_t
\longrightarrow
\theta_{t+1}.
$$

The schema earns its place only if it predicts useful design requirements:

1. the verifier must return localized evidence;
2. counterexamples must be retained as regression obligations;
3. revision must be able to reach definitions and interfaces, not only the
   final output;
4. simplification must rerun the corpus; and
5. the verifier itself must have provenance, scope, and capture resistance.

No gradient, differentiability, or loss surface is assumed. “Proof is
backpropagation” remains a metaphor.

## 6. Simplification is another hypothesis

Let a model-quality report be

$$
\mathbf q(M;H)=
\left(
\mathrm{Fit}_{\mathcal Q}(M,H),
-\mathrm{Complexity}(M),
\mathrm{Transfer}(M),
-\mathrm{RevisionCost}(M)
\right).
$$

This vector avoids pretending that the trade-offs have universal weights.
Simplification improves the report only if it reduces complexity without an
unacceptable loss elsewhere.

Three failure modes matter:

- **premature compression:** a partially correct distinction is deleted before
  enough evidence arrives;
- **regression overfitting:** the simplest model memorizes the replay corpus
  but fails transported tests; and
- **interface compression:** a clean abstraction hides uncertainty or
  provenance needed by downstream users.

Minimum description length is therefore a model-selection principle under a
code and data model, not an automatic truth oracle.

## 7. Multiple views over one verified core

A stable formal object can support several presentation layers:

- a machine-checkable core;
- an implementation interface;
- a research explanation with full assumptions;
- a beginner-oriented derivation; and
- generated domain-specific tactics or translators.

These views are safe only when their relationship to the core is itself
checked or explicitly lossy. A prose explanation can be pedagogically clearer
and still omit a decisive hypothesis. A machine-generated intermediate
representation can improve proof search while becoming a provenance burden.

This is also an information-architecture rule for the repository: one concept
home, typed derivatives, and links that identify which view is authoritative.

## 8. Referee independence and self-modification

The [Recursive Workbench](../../lab/benchmarks/recursive-workbench/README.md)
measures three exact toy regimes:

- revision saturates at the evidence ceiling under a frozen referee;
- new referee-side evidence raises held-out performance; and
- evaluator capture improves the report without improving the artifact.

A verifier can live inside a system, but independence must then be specified
operationally through at least one of:

- evidence the proposer cannot manufacture;
- permissions the proposer cannot silently rewrite;
- a frozen or versioned test corpus;
- external failure authority;
- cryptographic or institutional provenance; or
- an adversarially independent model and budget.

If every criterion and its history are editable, “verified improvement” can
collapse into self-approval.

## 9. Open problems

1. What is the weakest counterexample interface that still improves revision?
2. When should replay use exact equality, predictive equivalence, bisimulation,
   or safety-preserving refinement?
3. How should stochastic histories be replayed without demanding impossible
   sample identity?
4. Can proof obligations and empirical tests share a typed correction API
   without erasing their semantic differences?
5. Which simplification schedule improves transfer under matched compute?
6. How can a verifier be revised without losing the authority to assess the
   revision?
7. When does a generated intermediate representation become the actual
   specification rather than a disposable translation?

## Sources and related work

Primary-source status is recorded in the
[claim-level source ledger](../../meta/research-alignment/related-work-map.md#world-models-proof-and-recursive-correction).

- [Competence, Constraint, and Verification](competence-constraint-and-verification.md)
- [Construction and Deduction](../computation/construction-vs-deduction.md)
- [From Trace to World-Binding](from-trace-to-world-binding.md)
- [World Models and VLA Systems](../ai/world-models-and-vla.md)
- [Self-Improvement Needs a Referee](https://github.com/frnkptrln/systems-and-intelligence/blob/main/ideas/2026-07-24-self-improvement-needs-a-referee.md)
- [Recursive Workbench](../../lab/benchmarks/recursive-workbench/README.md)
- [Provenance Depth](../../logs/017_provenance-depth-and-the-verification-economy.md)
