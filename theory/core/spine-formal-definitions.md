# The Spine as a Discrete Object — Formal Definitions

**Status:** Working Note — one shared finite setting and twelve definitions, each carrying its own tag. Tags used: `[established]` (textbook mathematics restated), `[formalized]` (a definition whose objects exist in this repository), `[operationalized]` (an exact instance is computed and test-pinned), `[hypothesis]` (a falsifiable repository claim without a decisive instrument), `[speculative]` (a reading the setting cannot express; entertained, not committed).
**Lane:** Theory — synthesis layer, model-identification arc, with one definition (D12) proposed for the collective-agency work.
**Created:** 2026-09-21
**Last reviewed:** 2026-09-21
**Review trigger:** a change to any home file named below, a new pinned number in a cited test, or a maintainer decision on which definitions are load-bearing.
**Provenance:** Drafted 2026-09-21 in an agent session working from the maintainer's Second Founding brief. Every definition tightens a sentence that already exists in the named home file; no home file was rewritten. Every number is quoted from a frozen README result or from the named pinning test; the worked example of D12 and the lemma of D10 are pinned by [`tests/test_spine_definitions.py`](../../tests/test_spine_definitions.py). No external material was introduced.

**Scope.** The [Foundations Reconstruction](mathematical-axioms.md) gives the repository its process language: standard Borel interfaces and Markov kernels. That language is right for the general case and wrong for reading a spine element at a glance, because most spine elements are statements about *finite* families, *finite* traces, and *finite* query sets, and the repository's exact results (the rule-90 class, the de Bruijn frontier, the parity control) live in that finite world. This note restates each spine element in the finite-set instance of the same foundation, which the reconstruction itself names ([§1.3](mathematical-axioms.md#13-why-begin-with-stochastic-rather-than-deterministic-processes): "A finite-state version could use finite sets and stochastic matrices"). Nothing here replaces a home file. Where an element does not fit the setting, the note says so and tags the remainder `[speculative]` instead of dressing it up.

---

## 0. The shared setting `[established]`

A **finite process** (a candidate process model in the reconstruction's sense) is a tuple

$$
\theta = (X, U, Y, \delta, \omega, X_0)
$$

with a finite state set $X$, a finite input alphabet $U$ (a singleton $\lbrace \epsilon \rbrace$ for an autonomous system), a finite readout alphabet $Y$, a transition function $\delta : X \times U \to X$, a readout $\omega : X \to Y$, and a set $X_0 \subseteq X$ of admissible initial states. A **trajectory** under input word $u = u_0 \cdots u_{n-1} \in U^*$ from $x_0 \in X_0$ is $x_{0:n}$ with $x_{t+1} = \delta(x_t, u_t)$; its **trace** is $\omega(x_0)\,\omega(x_1) \cdots \omega(x_n) \in Y^{n+1}$. Write $\tau_\theta(x_0, u)$ for that trace.

A **query** is a pair $q = (x_0, u) \in X \times U^*$; the **admissible query set** $Q$ is a declared subset. A **model class** $\Theta$ is a finite set of processes over one $(U, Y)$. **Evidence** $e$ is a finite set of pairs $(q, y)$ with $y \in Y^*$. An **observer** is any function $\phi : Y^* \to Z$ into a finite set of verdicts, scores, or partitions. A **cost** is $c : Q \to \mathbb N$ and a **budget** is $b \in \mathbb N$.

Two relations recur in every definition:

$$
\Theta_e = \lbrace \theta \in \Theta : \tau_\theta(q) = y \ \text{ for every } (q, y) \in e \rbrace
\qquad\text{(the consistent class)}
$$

$$
\theta \sim_{Q} \theta' \iff \tau_\theta(q) = \tau_{\theta'}(q) \ \text{ for every } q \in Q
\qquad\text{(access-relative equivalence)}
$$

**Stochastic reading.** Replace $\delta$ by a stochastic matrix $X \times U \to \Delta(X)$ and read "trace" as "trace law" throughout; every definition below lifts by that substitution, and the reconstruction's Markov-kernel language is the general form. The deterministic case is stated because every exact result in the repository is deterministic.

**Complexity classes.** They apply below only where a problem is precisely encoded (D1). No other definition uses them.

---

## D1 — Construction and deduction `[established]`; the repository's claim `[operationalized]` for one language

*Home:* [Construction and Deduction](../computation/construction-vs-deduction.md).

Fix a binary relation $R \subseteq A \times W$ over finite words. **Verification** is the decision problem "is $(a, w) \in R$?" **Construction** (search) is the function problem "given $a$, return some $w$ with $(a, w) \in R$, or report that none exists." **Deduction** is derivability $\Gamma \vdash \varphi$ in a fixed proof system; a constructive proof of an existential is a derivation from which a $w$ can be extracted. Verification, construction, and deduction are three different problems with three different cost functions, and no theorem relates them in general.

The spine's former sentence "verification is cheap, construction is hard" is, in these terms, the conjunction "$R \in \mathrm{P}$" and "search-$R \notin \mathrm{FP}$." For $R$ an NP relation that is the P versus NP question. The repository does not assume it ([Foundations §9.3](mathematical-axioms.md#93-problems-in-the-former-generator-spine); [non-claim 3](../reference/what-this-project-does-not-claim.md)).

What is measured: in the finite Boolean DSL of benchmark v1.2, verifying a candidate costs a constant eight bit-comparisons, while the size-ordered enumerator reaches rule 90 (minimal size 3) within at most 36 candidates, rule 30 (size 5) within at most 771, and rule 110 (size 8) within at most 116,232 ([benchmark README, v1.2](../../lab/benchmarks/inverse-reconstruction/README.md#v1-part-2-family-search-the-wall-measured-run), frozen result; the enumeration figures are not test-pinned, the Occam-is-chance identity of the same section is, by [`tests/test_benchmark_v1_headlines.py`](../../tests/test_benchmark_v1_headlines.py)). That is a property of one enumerator over one language, not a lower bound.

---

## D2 — Forward map and fiber (Trace → Generator, Generator → Trace) `[formalized]` `[operationalized]`

*Home:* [From Trace to Generator](../emergence/trace-to-generator.md), [The Generator Question](the-generator-question.md).

The **forward map** is

$$
F : \Theta \times Q \to Y^*, \qquad F(\theta, q) = \tau_\theta(q).
$$

"Generator → Trace" is evaluation of $F$. "Trace → Generator" is the **fiber**: given evidence $e$, the set $\Theta_e$ above, which is exactly $\bigcap_{(q,y)\in e} F(\cdot, q)^{-1}(y)$. Relative to a declared target equivalence $\equiv$ on $\Theta$, the evidence **identifies** the process when $\Theta_e / {\equiv}$ has one element; "many-to-one" means the fiber contains more than one $\equiv$-class. The measure of underdetermination is $|\Theta_e / {\equiv}|$, a number; the cost of computing it is a separate number.

**Hidden extension in finite form.** For any finite $Z$ and $h : Z \to Z$, the process $\theta' = (X \times Z, U, Y, \delta \times h, \omega \circ \pi_X, X_0 \times Z)$ satisfies $F(\theta', q) = F(\theta, q)$ for every query $q$ whose input does not act on $Z$. So a model class closed under extension never has a singleton fiber; identifiability is always relative to a class ([Foundations §7](mathematical-axioms.md#7-a-result-the-foundation-forces-non-identifiability)).

Exact instance: the 256 elementary cellular-automaton rules with a single-seed initial row expose five of the eight neighborhoods of rule 90, so $|\Theta_e| = 2^3 = 8$ however long the orbit is watched ([`tests/test_benchmark_headlines.py`](../../tests/test_benchmark_headlines.py), `test_rule90_single_seed_equivalence_class`).

---

## D3 — Bounded inverse system `[formalized]`; exact instance `[operationalized]`

*Home:* [The Generator Question](the-generator-question.md) ("model family, evidence regime, intervention access, target equivalence, cost measure"); [The Witness Principle](the-witness-principle.md).

A **bounded inverse system** is the six-tuple

$$
\mathcal B = (\Theta, Q, \omega, \equiv, c, b)
$$

with $\Theta$ finite. "Bounded" means all six are declared; every question of the model-identification arc is a question about some $\mathcal B$. For a query $q$ let $\Pi_q(\Theta_e)$ be the partition of $\Theta_e$ into blocks with equal trace $F(\cdot, q)$, and let $R_{\max}(q) = \max_{B \in \Pi_q} |B|$ be the worst-case residual. The **bounded inverse problem** is: given $e$, choose $q \in Q$ with $c(q) \le b$ minimizing $R_{\max}(q; \Theta_e/{\equiv})$. For deterministic lookup-table families the coverage–distinction lemma of the Witness Principle turns this into a hitting-set problem over the coordinates the query exposes.

Exact instance: 256 ECA rules, one prepared row of width eight, Hamming cost from the all-zero row. Worst-case residual after the best query at costs 0 to 4: 128, 16, 8, 2, 1; the cost-four universal queries are exactly the 16 rotations of the two binary de Bruijn cycles; the 256 rows fall into 21 coverage-equivalent query classes; the pairwise witness profile is 16,384 / 14,336 / 1,792 / 128 rule pairs at minimal costs 0 to 3 ([`tests/test_witness_benchmark.py`](../../tests/test_witness_benchmark.py)).

---

## D4 — Measurement, intervention, footprint `[formalized]`; regimes 1–3 `[operationalized]`; regime 4 `[speculative]` as an institutional claim

*Home:* [Measurement as Weak Intervention](measurement-as-weak-intervention.md).

Classify queries by what the observer supplies. A query is **passive** when $x_0$ is the process's own initial state and $u$ is the neutral word; **perturbing** when $u$ contains a non-neutral symbol; **preparing** when $x_0$ is chosen by the observer. The **footprint** of a query is its cost $d(q) = c(q)$ (Hamming distance of the prepared state from the reference state, plus the number of non-neutral input symbols). Its **identifying power** is $R_{\max}(q)$ from D3. The note's "two axes" are the coordinates $(d(q), R_{\max}(q))$, and "coupling is not identification" is the statement that neither coordinate determines the other. Witnesses, all frozen results of benchmark v1.1 ([README](../../lab/benchmarks/inverse-reconstruction/README.md#v1-part-1-the-intervention-experiment-run); the rule-90 hierarchy is pinned by `test_ca_hierarchy_watching_perturbing_preparing` in [`tests/test_benchmark_v1_headlines.py`](../../tests/test_benchmark_v1_headlines.py)):

| query | $d(q)$ | $R_{\max}$ | reading |
|:---|---:|---:|:---|
| rule 90, single seed, any horizon | 0 | 8 | large trace, no identification |
| rule 0, one-bit flip | 1 | 16 | positive footprint, no identification |
| rule 90, de Bruijn row | 4 | 1 | one step identifies |

**Regime 4 (reflexive measurement).** The observer's verdict enters the process's input: $u_t = \psi(\phi(y_{0:t}))$ for some $\psi : Z \to U$. Then the object under identification is the closed loop $\theta \circ \phi$, not $\theta$, and changing $\phi$ changes $\Theta$. This is the finite form of "the metric enters the generator." The definition is exact; the claim that institutions behave this way is [pre-registered and untested](../../logs/018_the-city-panel-protocol.md) and stays speculative here.

Conditioning versus intervention: restricting $e$ to traces the process happened to produce is conditioning; choosing $(x_0, u)$ is intervention. In the finite setting the distinction is the distinction between passive and non-passive $q$; it needs no further primitive.

---

## D5 — World model, replay, exploitation `[formalized]`; toy `[operationalized]`; transfer `[hypothesis]`

*Home:* [World Models and VLA Systems](../ai/world-models-and-vla.md), [Verification as Reverse Pressure](verification-as-reverse-pressure.md).

A **world model** is a candidate $\hat\theta \in \Theta$ together with a **policy** $\pi : Y^* \to U$. A **recorded history** is $H = \langle (y_i, u_i, y_{i+1}) \rangle_{i < n}$. Under a test family $\mathcal Q$ with equivalence $\sim_{\mathcal Q}$ on $Y$, the model **passes replay** of $H$ when

$$
\omega_{\hat\theta}\bigl(\delta_{\hat\theta}(\hat x_i, u_i)\bigr) \sim_{\mathcal Q} y_{i+1}
\quad\text{for every } i < n,
$$

where $\hat x_i$ is the model's state after replaying the prefix. Byte equality, predictive equivalence, and policy-preserving equivalence are three choices of $\sim_{\mathcal Q}$ (Open Problem 18). Passing replay is consistency with those tests, not identification (D2).

**Exploitation.** For a value $V_\theta(u)$ of input word $u$ under process $\theta$, the planner chooses $u^\star \in \arg\max_u V_{\hat\theta}(u)$ and the **wedge** is $V_{\hat\theta}(u^\star) - V_\theta(u^\star)$. In the v1.3 toy the model is one member of a class of size $2^u$ treated as fact; the wedge is $0$ at $u = 0$ and positive at $u = 5$ (pinned by `test_wedge_is_zero_at_u0_and_positive_at_u5` in [`tests/test_benchmark_v1_headlines.py`](../../tests/test_benchmark_v1_headlines.py)); the frozen monotone sequence $0 \to 0.034 \to 0.053 \to 0.068 \to 0.076 \to 0.081$ is in the [README](../../lab/benchmarks/inverse-reconstruction/README.md#v13-model-exploitation-the-world-models-bridge-run). That learned world models or VLA systems exhibit the same wedge is a hypothesis; the mapping is structural, not quantitative.

---

## D6 — Invariance and test-relative identity `[established]`; the identity reading `[hypothesis]`

*Home:* [Invariance and Identity](invariance-and-identity.md), [Foundations §4.5 and §5.1](mathematical-axioms.md#45-symmetry-and-invariance).

An **invariance claim** has three declared parts: a transformation family $S$ (any set of functions on $X$, on $Y^*$, or on $\Theta$; a group is sufficient, not required), a represented quantity $f$ with finite codomain, and an equality notion $=_\varepsilon$. Then $f$ is **$S$-invariant** when $f \circ s =_\varepsilon f$ for every $s \in S$. A **test family** $\mathcal Q$ induces

$$
x \sim_{\mathcal Q} x' \iff q(x) = q(x') \ \text{ for every } q \in \mathcal Q,
$$

and $X / {\sim_{\mathcal Q}}$ contains exactly the distinctions the tests can make. Adding tests refines the partition; removing tests coarsens it.

**The finite TCS anchor.** Let $\mathcal Q$ be all future traces: $x \sim x'$ iff $\tau_\theta(x, u) = \tau_\theta(x', u)$ for every $u \in U^*$. This is Moore-machine equivalence; the quotient $X / {\sim}$ is the minimal Moore machine, computable by partition refinement (Moore 1956; Hopcroft 1971). The reconstruction's *predictive identity* (causal states, [§5.1](mathematical-axioms.md#51-identity)) is this construction in the finite deterministic case. The repository's rule "never claim an invariant without naming the transformation family, the represented quantity, and the equality notion" is the statement that $S$, $f$, and $=_\varepsilon$ are three free parameters, none of which the mathematics fixes.

What the setting does not decide: *which* $\mathcal Q$ individuates an agent, a person, or a culture. That choice is a model supplement (hypothesis), and the Chord/Arpeggio and practice-based identity proposals are two candidates for it (D7, D9).

---

## D7 — Commit-time composition; "coherence work" `[formalized]` `[operationalized]` in toys; the consciousness reading `[speculative]`, explicitly not derived

*Home:* [Machine Consciousness as Generator Coherence](../identity/machine-consciousness-as-generator-coherence.md), [Chord vs. Arpeggio](../identity/chord-vs-arpeggio-identity.md), [Consciousness as Global Availability](../identity/consciousness-as-global-availability.md).

Let $C_1(x), \ldots, C_k(x) \subseteq U$ be constraint sets active at state $x$ (goals, vetoes, role commitments), with an **active set** $\mathrm{act}(x) \subseteq \lbrace 1, \ldots, k \rbrace$. A committed action $a$ satisfies the **Chord property** at $x$ when

$$
a \in \bigcap_{i \in \mathrm{act}(x)} C_i(x),
$$

and an architecture is an **Arpeggio** when each step selects $a$ from one $C_{i_t}(x)$ in turn without the intersection being guaranteed at commitment. **Coherence work** is whatever process keeps $\bigcap_{i \in \mathrm{act}(x)} C_i(x) \neq \varnothing$ under perturbation of $x$, that is, resolves conflicts between partial constraints before commitment. The measured instance is Exp5: veto-violation rates 0.74 / 0.59 / 0.03 for private / broadcast / chord bindings under one perturbation schedule (pinned by [`tests/test_agentic_headlines.py`](../../tests/test_agentic_headlines.py)); Exp7 shows the fractional IP score is satisfied by consultation without composition, so IP does not certify the Chord property.

What resists formalization: any statement that this organization is, or entails, consciousness. The setting has no object for phenomenal experience, and the reconstruction adopts no bridge axiom ([§5.4](mathematical-axioms.md#54-consciousness)). The home file's title keeps the legacy word "generator"; its content is the Chord property under perturbation, and that is all this definition claims.

---

## D8 — Convergence `[formalized]` as lens-relative equivalence; the convergence claim `[hypothesis]`, in its strong form `[speculative]`

*Home:* [Intelligence as Convergence](../../ideas/2026-07-23-intelligence-as-convergence.md) (ideas note), [The Witness Principle, H4](the-witness-principle.md#h4-convergence-by-witness-profile).

Two processes **converge relative to a lens and a task family** $(\ell, T)$, $\ell : Y^* \to L$ and $T \subseteq Q$, when

$$
\theta \equiv_{\ell, T} \theta' \iff \ell(F(\theta, q)) = \ell(F(\theta', q)) \ \text{ for every } q \in T .
$$

This is D6 with $S$ trivial and the test family $\lbrace \ell \circ F(\cdot, q) : q \in T \rbrace$; it adds no object. Two facts follow immediately: coarsening $\ell$ (replacing it by $\pi \circ \ell$) or shrinking $T$ can only merge classes, and any two processes are convergent under a constant lens. The ideas note's warning is exactly this monotonicity read backwards: a shared bottleneck, selector, or evaluator is a coarse $(\ell, T)$, and convergence under it says nothing about convergence under a finer one. **Witness-profile convergence** (Witness Principle H4) is the special case $\ell = $ "the partition $\Pi_q(\Theta)$ the system constructs," which is testable in the finite baseline.

The strong reading, that different substrates converge on shared structure "imposed by the world," would require the classes of $\equiv_{\ell,T}$ to stay large as $\ell$ is refined toward the identity. Nothing in the repository measures that, and the setting offers no reason to expect it. The definition is kept; the claim is not promoted.

---

## D9 — Recurrent practice and the return path `[formalized]` as a definition without an instrument; the cultural reading `[speculative]` beyond it

*Home:* [From Action to Culture](../emergence/from-action-to-culture.md); Open Problem 12.

A **practice** is a language $L \subseteq Y^*$ of recognizable performances. Under a declared transformation family $S$ on processes (change of context, personnel, tool), the practice is **reproduced** across $S$ when $\tau_{s\theta}(q) \in L$ for every $s \in S$ and every admissible $q$; it is reproduced *with variation* when the traces differ but stay in $L$. A **return path** is a process whose transition rule is updated by its own record,

$$
\delta_{t+1} = \rho(\delta_t, y_{0:t}),
$$

a higher-order finite process (a learning automaton over a finite rule space). A **practice network** is a directed graph $G = (V, E)$ with practices as vertices and an edge $i \to j$ when performances in $L_i$ change $\rho$ for $L_j$; the network is **recursive** when $G$ has a directed cycle. The essay's "culture is a recursive network of such generators" is, in this vocabulary, "$G$ is cyclic and its vertices are reproduced across $S$." The essay's identity proposal, "identity is the invariant pattern across the rituals a system reproduces, revises, and refuses," is $S$-invariance of $G$ itself (D6 with $f = G$).

This captures reproduction and the return path. It does not capture meaning, normativity, or power, which the essay's §2 correctly separates and for which the setting has no object. The definition is offered so that Open Problem 12 has a target; no instrument exists, and the essay's own status (`[HYPOTHESIZED]`, unmeasured) is unchanged.

---

## D10 — Effective goal space and the monotonicity lemma `[proved]`; orthogonality theses `[hypothesis]`, no theorem

*Home:* [Embodiment and the Non-Invariant Decomposition of Goals](../optimization/embodiment-and-the-non-invariant-decomposition-of-goals.md); [The Agent Is Not Where the Model Ends, §4](../identity/the-agent-is-not-where-the-model-ends.md#4-the-situated-stack-and-orthogonality).

Let $\mathcal G$ be a finite set of goals $g : L \to \mathbb R$ defined on lens records, let $R_e \subseteq Y^*$ be the set of trajectories reachable under coupling $e$, and let $\ell : Y^* \to L$ be the evaluation lens. The home file's relation is

$$
g \sim_{e,\ell} h \iff g(\ell(\gamma)) = h(\ell(\gamma)) \ \text{ for every } \gamma \in R_e ,
$$

and $\mathcal G / {\sim_{e,\ell}}$ is the **effective goal space**.

**Lemma (monotonicity in reachability).** If $R_1 \subseteq R_2$ then ${\sim_2} \subseteq {\sim_1}$ as relations on $\mathcal G$; hence $\mathcal G / {\sim_2}$ refines $\mathcal G / {\sim_1}$ and $|\mathcal G / {\sim_1}| \le |\mathcal G / {\sim_2}|$.

*Proof.* Let $g \sim_2 h$. Then $g(\ell(\gamma)) = h(\ell(\gamma))$ for every $\gamma \in R_2$, in particular for every $\gamma \in R_1 \subseteq R_2$, so $g \sim_1 h$. The refinement and cardinality statements are the standard consequences of one equivalence relation being contained in another. $\square$

*Consequences.* Enlarging reachability (releasing a constraint, adding an actuator, lengthening the horizon) can split goal classes and never merge them; restricting it can merge and never split. Coarsening the lens acts the same way on goals pulled back through the coarsening. The lemma is elementary and is stated because the home file's central claim, that embodiment can change *which goal distinctions are behaviorally real*, is exactly the claim that $R_e$ varies with the body, and the lemma says in which direction. A small instance is pinned by [`tests/test_spine_definitions.py`](../../tests/test_spine_definitions.py).

**Orthogonality.** For a situated system $\Sigma$, lens $\ell$, and task family $\tau$, write $J_{\ell,\tau}(\Sigma)$ for the selected capability score. *Strong representation-invariant orthogonality* is the existence of functions $I$, $\Phi$ with $J_{\ell,\tau}(\Sigma) = \Phi(I(P), g)$ for every admissible transformation of the stack around the controller $P$; *fixed-stack orthogonality* asserts the same for a single declared stack; *local goal independence* asserts only that changing $g$ moves $J$ little within a declared class. All three are existence statements over a transformation class, hence claims of the D6 kind with $S$ = the admitted stack transformations. The situated-stack toy gives one controller scoring from $0$ to $1$ as stack components change, and a coordinated sensor–actuator mirror preserving every physical trace ([`tests/test_situated_stack.py`](../../tests/test_situated_stack.py)); that is a finite existence demonstration against the strong thesis under that class, not a theorem about any other.

---

## D11 — No view from nowhere `[formalized]` as an indexing rule; anything further `[speculative]`

*Home:* [The Agent Is Not Where the Model Ends](../identity/the-agent-is-not-where-the-model-ends.md) (the opening formulation), [Polycontextural Observation](../identity/polycontextural-observation.md).

Every statement about a process in this setting is a function of the tuple $(F, \omega, Q, \ell)$: which traces exist, which readout produced them, which queries were admissible, which lens scored them. A "view from nowhere" would be the tuple with $\omega = \mathrm{id}_X$ and $Q$ the set of all queries. That tuple is not an admissible bounded inverse system for any declared $\mathcal B$ (D3), and even granting it, the hidden-extension construction (D2) shows that components outside the declared $X$ stay invisible. The formal content of the slogan is therefore an **indexing rule**: a capability, identity, or convergence claim is well-formed only once its $(\omega, Q, \ell)$ is stated, and two observers with different tuples are not in disagreement until a translation between their tuples is declared (the polycontextural note's "translation rule," of which the [representation experiment](../../lab/experiments/representation_reconstruction/README.md) gives one exact instance: under an invertible re-encoding the conjugate rule is the translation, class size the preserved invariant).

Any reading beyond indexing, about perspective or subjectivity, has no object here and is tagged speculative.

---

## D12 — Invariants over irreducible internal trajectories (the multi-agent reframing) `[established]` definitions; proposition `[proved]` by an exact control; the reframed research question `[hypothesis]`

*Home:* the four 2026-09-03 ideas notes ([When Does a Collection Become an Agent?](../../ideas/2026-09-03-when-does-a-collection-become-an-agent.md), [Macro Agency Needs Downward Control](../../ideas/2026-09-03-macro-agency-needs-downward-control.md), [Collective Self-Knowledge May Require Synergy](../../ideas/2026-09-03-collective-self-knowledge-may-require-synergy.md), [Closure Can Open a New Possibility Space](../../ideas/2026-09-03-closure-can-open-a-new-possibility-space.md)); [Collective Agency benchmark](../../lab/benchmarks/collective-agency/README.md) (preregistration draft); [exact control](../../lab/experiments/collective-agency-control/README.md).

**The reframing.** The question is not whether a multi-component system is irreducible. It is which of its properties stay invariant across its internal trajectories when those trajectories are irreducible. Internally irreducible and externally compressible are compatible, and the definitions below make both words exact.

Let $X = X_1 \times \cdots \times X_N$ be a product of finite component state sets with an autonomous transition $\delta : X \to X$.

**Causal dependency graph.** $G_\delta$ has vertices $1, \ldots, N$ and an edge $j \to i$ whenever there exist $x, x' \in X$ differing only in coordinate $j$ with $\delta(x)_i \neq \delta(x')_i$.

**Internally irreducible.** $\delta$ is *component-irreducible* when $G_\delta$ is strongly connected. (Strong connectivity implies that $\delta$ is not a product $\delta_A \times \delta_B$ over any partition of the components; the converse fails, so the weaker "not a product" is a different, weaker notion.)

**Externally compressible.** A readout $\omega : X \to Y$ with $|Y| < |X|$, not constant, is a **lumping** of $\delta$ when there is $\bar\delta : Y \to Y$ with

$$
\omega \circ \delta = \bar\delta \circ \omega ,
$$

that is, the macro-state has its own closed dynamics. This is a substitution-property partition in the sense of Hartmanis and Stearns (1966) and, in the stochastic reading, Kemeny–Snell lumpability. An **invariant of the dynamics** (a first integral) is the case $\bar\delta = \mathrm{id}_Y$: $\omega \circ \delta = \omega$.

**Proposition.** Component-irreducibility and lumpability are independent properties: (a) there is a component-irreducible $\delta$ with a non-constant first integral; (b) the same readout is a first integral of a $\delta$ whose causal graph has no edges at all; (c) a readout can be conserved on an invariant subset of $X$ without being a lumping of $\delta$.

*Proof (worked example).* Take the parity control's six Boolean components ([exact control](../../lab/experiments/collective-agency-control/README.md); all figures below are enumerated over all 64 states by [`tests/test_spine_definitions.py`](../../tests/test_spine_definitions.py), and the causal-graph figures also by [`tests/test_collective_agency_control.py`](../../tests/test_collective_agency_control.py)). Write $\mathrm{maj}$ for the majority of a triplet, $\omega_{\mathrm{maj}}(x) = \mathrm{maj}(x_{1:3}) \oplus \mathrm{maj}(x_{4:6})$ (majority parity) and $\omega_{\mathrm{rep}}(x) = x_1 \oplus x_4$ (representative parity).

| update $\delta$ | off-diagonal edges of $G_\delta$ | largest strongly connected component | $\omega_{\mathrm{maj}}$ conserved on | $\omega_{\mathrm{rep}}$ conserved on | image size |
|:---|---:|---:|---:|---:|---:|
| uncoupled toggle: every bit flips | 0 | 1 | 64 / 64 | 64 / 64 | 64 |
| local repair: each triplet becomes three copies of its own complemented majority | 12 | 3 | 64 / 64 | 40 / 64 | 4 |
| cross-group repair: each triplet becomes three copies of the *other* triplet's complemented majority | 18 | 6 | 64 / 64 | 40 / 64 | 4 |

(a) Cross-group repair is component-irreducible (strongly connected on all six components) and $\omega_{\mathrm{maj}}$ is a first integral on all 64 states: $\mathrm{maj}$ of the new first triplet is $1 - \mathrm{maj}(x_{4:6})$ and of the new second triplet $1 - \mathrm{maj}(x_{1:3})$, and the two complements cancel in the parity. The internal trajectory is irreducible; the one-bit macro-state is closed with $\bar\delta = \mathrm{id}$.
(b) The uncoupled toggle has no causal edges and $\omega_{\mathrm{maj}}$ is a first integral of it too (both majorities flip). So the invariant does not detect irreducibility, which is the control's own finding restated: predictive parity does not identify organization.
(c) $\omega_{\mathrm{rep}}$ is conserved on the four codewords $(a,a,a,b,b,b)$ under both repair rules, but on only 40 of 64 states, and it is not a lumping of either repair rule (its next value is not a function of its current value). Conservation on an invariant subset is weaker than lumpability on $X$. $\square$

**What the reframing asks.** For a declared decomposition of $X$ and a declared perturbation family $S$ (bit errors, membership replacement, budget changes), the question becomes: which lumpings $\omega$ of $\delta$ exist (the lattice of substitution-property partitions), which of them are $S$-invariant (D6), and which of them add control rather than compression (the ideas note's macro-intervention criterion: an intervention on $\omega$'s value that changes later local trajectories beyond matched micro-perturbations). Irreducibility of $G_\delta$ is one coordinate of the answer, not the question. The proposition settles only the compatibility claim; whether the invariant lumpings of a system are what collective-agency measurement should target is the hypothesis the benchmark draft is written to test, and it remains unrun.

---

## What resists formalization here

| element | what the setting expresses | what it does not, and the tag for the remainder |
|:---|:---|:---|
| D7 coherence work | the Chord property and its persistence under perturbation | that it is or entails experience — `[speculative]`, not derived |
| D8 convergence | lens-relative equivalence and its monotonicity | that convergence is world-imposed rather than lens-imposed — `[speculative]` in the strong form |
| D9 recurrent practice | reproduction across $S$, return path, cyclic practice graph | meaning, normativity, power — `[speculative]`, outside the setting |
| D11 no view from nowhere | the indexing rule | perspective, subjectivity — `[speculative]` |
| D12 multi-agent | causal graph, lumping, first integral | that invariant lumpings are the right target for agency — `[hypothesis]`, unrun |

## Relation to the rest of the repository

The claims that these definitions make precise, with their five-valued status and their falsifiers, are tabulated in the [Spine Claims Register](spine-claims-register.md). The definitions do not enter the [Concept Registry](../../meta/repository-meta/concept-registry.md) as new terms; each tightens a term already registered, and the registry rows point here. Nothing in this note changes the status of any home file.
