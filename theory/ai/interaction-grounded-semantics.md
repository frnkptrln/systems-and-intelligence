---
title: Interaction-Grounded Semantics
date: 2026-07-30
status: working formalization over preliminary evidence
---

# Interaction-Grounded Semantics

**Status:** Working formalization over Georgeon, Marrel, and Cook's
[published 2026 proof-of-concept](https://doi.org/10.1007/978-3-032-33010-9_16)
and earlier enactive-decision-process work. It defines functional
interchangeability inside declared interaction tests, not meaning in every
linguistic, phenomenological, or social sense.

**Why this page exists:** The repository treated observation as a process and
measurement as intervention, but did not yet formalize the claim that a signal
can acquire a stable role from action–feedback history without first being
specified as a description of an external world state.

## 1. Observation token versus interaction event

A conventional observation model writes

$$
o_t=O(s_t),
$$

where $s_t$ is a world state and $O$ maps it to an observation. This need not be
passive—the observation process may include a sensor action—but the token is
usually interpreted as information about $s_t$.

An interaction-first model instead takes

$$
i_t=I(a_t,s_t,s_{t+1})
$$

as primitive. The token records a sensorimotor loop: an attempted action and
the feedback or transition that followed. Georgeon and collaborators' Enactive
Markov Decision Process (EMDP) makes this distinction explicit. In one finite
version, an EMDP has state space $S$, decision set $D$, interaction set $I$,
an interaction kernel $q(i_t\mid s_t,d_t)$, and a successor kernel
$p(s_{t+1}\mid s_t,i_t)$.

The agent need not receive a symbol labeled “wall on the left.” It can receive
a token whose regular role is: after a left-feeling action in this history,
continuing forward tends to fail. Spatial interpretation is then a model the
agent may construct from temporal regularity; it is not built into the token
name.

## 2. History and continuation

Let

$$
H_t=(i_0,i_1,\ldots,i_{t-1})
$$

be the interaction history retained for prediction or control. A current
state can be insufficient when the system adapts, consumes resources, or
builds schemas; two equal present observations with different $H_t$ can imply
different continuation laws.

Fix:

- a set $\mathcal H_{x,y}$ of admissible histories in which tokens $x$ and
  $y$ can be compared;
- a policy family $\Pi_\ell$;
- continuation horizons $\mathcal K_\ell$;
- a set $\mathcal Q_\ell$ of probes over conditional future-interaction
  distributions; and
- an equality or tolerance relation $=_{\ell}$.

For policy $\pi$, write

$$
\Pr_\pi(I_{t:t+k}\mid h\mathbin{\|}x)
$$

for the distribution of the next $k+1$ interaction tokens after history $h$
extended by $x$.

**Definition — functional semantic equivalence.**

$$
x\sim^{\mathrm{sem}}_{\ell}y
$$

when, for every $h\in\mathcal H_{x,y}$, $\pi\in\Pi_\ell$,
$k\in\mathcal K_\ell$, and $Q\in\mathcal Q_\ell$,

$$
Q\!\left(
\Pr_\pi(I_{t:t+k}\mid h\mathbin{\|}x)
\right)
=_{\ell}
Q\!\left(
\Pr_\pi(I_{t:t+k}\mid h\mathbin{\|}y)
\right).
$$

This definition is deliberately indexed by $\ell$. It says that $x$ and $y$
play the same declared continuation role. It does not claim that an
all-purpose, observer-independent meaning has been recovered.

## 3. What the probes decide

The choice of $\mathcal Q_\ell$ determines which kind of role is preserved:

| Probe family | Preserved distinction | Failure if omitted |
|:---|:---|:---|
| next-token prediction | local sequential regularity | long-horizon roles may collapse |
| multi-step prediction | temporal consequences | action alternatives may still differ |
| policy-value probes | consequences under selected policies | semantics becomes policy-family relative |
| affordance probes | actions that remain available or successful | equal predictions can hide control differences |
| valence probes | preferred and avoided continuations | pragmatic desirability can disappear |
| resource/safety probes | energy, damage, or viability consequences | “same role” can hide mortal cost |

Valence is therefore not automatically part of token identity. A scalar
$v(i)$ can be innate or learned, but it contributes to meaning only when the
declared probes preserve it or when it causally changes policy.

The relation is policy-relative unless $\Pi_\ell$ is rich enough to cover all
relevant policies. This is analogous to the repository's general
test-relative identity:

$$
x\sim_{\mathcal Q}y
\quad\Longleftrightarrow\quad
Q(x)\overset{d}{=}Q(y)
\text{ for every declared }Q.
$$

## 4. Schemas and composition

A schema can treat a recurring token sequence as a higher-level token:

$$
\sigma=(i_j,\ldots,i_{j+m})
\longmapsto
[\sigma].
$$

Recursive compression alone does not guarantee compositional semantics. For a
replacement relation to compose, it should be a congruence for the schema
operations being used. If $x\sim^{\mathrm{sem}}_\ell y$, then for every
admissible schema context $K[-]$ the stronger requirement is

$$
K[x]\sim^{\mathrm{sem}}_\ell K[y].
$$

This can fail. Two tokens may be interchangeable in short predictions but
different inside a longer action sequence, just as equal aggregate scores can
hide different physical traces in the
[situated-stack benchmark](../../lab/benchmarks/situated-stack/README.md).

The right empirical object is therefore not an embedding picture by itself.
It is a replacement or intervention test: substitute tokens or schemas and
measure whether the declared future roles remain invariant.

## 5. What has been demonstrated

Georgeon, Marrel, and Cook's 2026 paper reports an agent whose
experience is a stream of sensorimotor-loop tokens. A schema mechanism learns
token sequences and assigns pragmatic roles according to their place in the
stream; the authors analyze a small Transformer's attention matrix as evidence
of semantic organization. Their official tutorial repository supplies a
related maze-like demonstration in which the agent receives binary feedback
from actions such as moving, turning, or feeling a direction.

This is **preliminary empirical evidence** for learned interaction-role
structure. It does not yet demonstrate:

- invariance across seeds, architectures, bodies, or task families;
- causal necessity of the reported attention structure;
- human-like spatial concepts;
- policy-independent semantic equivalence;
- logical abstraction from schemas; or
- convergence on a shared semantics across agents.

The earlier EMDP and artificial-enactive-inference papers provide a clearer
formal basis for action-dependent interaction tokens than the short 2026 paper
alone.

Primary sources and the official implementation are in the
[claim-level source audit](../../meta/research-alignment/agi-26-day-2-source-map.md#interaction-grounded-semantics).

## 6. Developmental ordering as a hypothesis

A research sequence suggested by this programme is

$$
\text{interaction regularities}
\rightarrow
\text{schemas}
\rightarrow
\text{body/displacement model}
\rightarrow
\text{spatial world model}
\rightarrow
\text{logical abstraction}.
$$

Each arrow needs a criterion:

1. **Regularity to schema:** compressed sequence predicts held-out
   continuations better than token-frequency controls.
2. **Schema to body model:** the agent predicts how its own action changes the
   frame of later interactions.
3. **Body to spatial model:** learned displacement compositions generalize to
   novel routes and coordinate relabelings.
4. **Spatial to logical abstraction:** relational operations transfer outside
   the original sensorimotor domain.

The sequence is an architecture hypothesis. Biological cognition may use
parallel, recurrent, socially mediated, or genetically scaffolded routes.

## 7. Active perception and measurement

An interaction token is a record of intervention. This connects directly to
[Measurement as Weak Intervention](../core/measurement-as-weak-intervention.md):

- an action can have a large dynamical footprint but little identifying power;
- repeated interactions can remain inside one observational equivalence class;
- a selected interaction can act as a
  [distinguishing witness](../core/the-witness-principle.md); and
- if the agent models the metric or signal, observation becomes part of the
  process being identified.

The slogan “meaning comes from action” is therefore too broad. Some actions
repeat an uninformative loop. A sharper proposal is:

> Meaning becomes operationally stable when interaction history supports
> counterfactual replacement classes that preserve declared predictions,
> affordances, and values.

## 8. Semantic convergence across agents

Agents $A$ and $B$ can use different token alphabets. A translation
$\phi:I_A\to I_B$ supports lens-relative convergence when corresponding token
replacements preserve a shared probe family after transporting histories and
policies:

$$
x\sim^{A,B}_{\ell}\phi(x).
$$

This is stronger than embedding similarity and weaker than identical inner
meaning. It requires:

- a shared or translated task and policy family;
- comparable embodiment and action effects;
- agreed probe outcomes and tolerances; and
- held-out interaction tests.

If those conditions are absent, apparent semantic convergence can be a shared
evaluator artifact.

## 9. Next experiment

A useful repository extension would construct a small grid or graph world in
which tokens encode only action–feedback events. It should compare:

1. next-token clusters;
2. continuation-role equivalence;
3. affordance-preserving equivalence; and
4. transported equivalence after sensor and action relabeling.

The key falsifier is a token pair that looks equivalent in learned embeddings
but fails a held-out replacement test. That result would show why semantics
cannot be inferred from representation geometry alone.

## Related

- [Competence, Constraint, and Verification](../core/competence-constraint-and-verification.md)
- [The Agent Is Not Where the Model Ends](../identity/the-agent-is-not-where-the-model-ends.md)
- [From Trace to World-Binding](../core/from-trace-to-world-binding.md)
- [World Models and VLA Systems](world-models-and-vla.md)
- [Measurement as Weak Intervention](../core/measurement-as-weak-intervention.md)
- [Invariance and Identity](../core/invariance-and-identity.md)
- [Situated-Stack Benchmark](../../lab/benchmarks/situated-stack/README.md)
