# GameNGen: From Traces to an Interactive Surrogate

**Status:** Working Note — external case study for the model-identification arc

**Scope:** Uses GameNGen as a bounded example of learning an action-conditioned interactive surrogate from traces. It does **not** claim that GameNGen recovers DOOM's original program, causal decomposition, or latent state.

**Primary source:** Dani Valevski, Yaniv Leviathan, Moab Arar, and Shlomi Fruchter, *Diffusion Models Are Real-Time Game Engines*, ICLR 2025. [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/b71ecea210f7159f31e46631fe5c838f-Abstract-Conference.html) · [project page](https://gamengen.github.io/) · [arXiv:2408.14837](https://arxiv.org/abs/2408.14837)

**Related repository work:**

- [From Trace to Generator](trace-to-generator.md)
- [The Generator Question](../core/the-generator-question.md)
- [From Trace to World-Binding](../core/from-trace-to-world-binding.md)
- [Inverse-Reconstruction Benchmark](../../lab/benchmarks/inverse-reconstruction/README.md)
- [The Agent Is Not Where the Model Ends](../identity/the-agent-is-not-where-the-model-ends.md)
- [The Witness Principle](../core/the-witness-principle.md)

**Failure conditions for this reading:**

- treating visual similarity as recovery of the original mechanism;
- ignoring that the training corpus is selected by a policy;
- treating persistence over long rollouts as evidence of a complete internal world state;
- using one successful game simulator as evidence for a general law of world-model learning.

---

## 1. Why this case belongs here

GameNGen is easy to summarize too strongly: an AI model learns to "run DOOM" from gameplay. The more useful reading is narrower.

DOOM gives us an unusual model-identification case because the hidden productive process is not mysterious. There really is a conventional software system with program state, hand-written transition logic, and a renderer. We can therefore distinguish three targets that are often blurred together:

1. **mechanism recovery** — reconstruct the original state variables, update rules, and rendering logic;
2. **predictive reconstruction** — construct a model that predicts future observations under actions;
3. **interactive equivalence** — construct a process whose rollouts are sufficiently similar under a declared policy, horizon, and observation metric.

GameNGen is evidence for the second and third targets. It is not evidence for the first.

That distinction is exactly the correction the repository's current model-identification arc requires: a successful reconstruction need not be *the* source mechanism. It may be one member of a test-relative equivalence class.

---

## 2. The original engine and the learned simulator are differently factored

Write a conventional interactive environment as

$$
E=(S,A,O,T,V),
$$

where \(S\) is latent state, \(A\) actions, \(O\) observations, \(T(s_{t+1}\mid s_t,a_t)\) the state transition law, and \(V(o_t\mid s_t)\) the observation or rendering channel.

A classical game loop has the approximate causal form

$$
s_t \xrightarrow{a_t} s_{t+1} \xrightarrow{V} o_{t+1}.
$$

GameNGen instead learns an action-conditioned observation process of the form

$$
q_\theta(o_{t+1}\mid o_{\le t},a_{\le t+1}),
$$

implemented as an autoregressive diffusion model over rendered frames.

The learned model therefore does not inherit the engine's explicit ontology. It is not handed a canonical object table, map state, health variable, enemy state machine, collision system, or renderer. It receives observations and actions and is optimized to continue the observable process.

This gives a concrete example of a point that is otherwise easy to leave philosophical:

> **Two processes can be behaviorally close under a test while having different internal factorizations.**

The reconstruction target must therefore state which equivalence relation matters.

---

## 3. A policy-relative notion of success

The GameNGen paper explicitly defines simulation quality relative to a policy, an initial-state distribution, episode lengths, and an observation distance. That is more important for this repository than the headline frame rate.

Let \(\pi\) be the policy that chooses actions, \(\mu_0\) an initial-state distribution, \(H\) a horizon distribution, and \(d\) a distance on observations. A repository-style adequacy statement can be written schematically as

$$
\hat E \approx_{\pi,\mu_0,H,d,\varepsilon} E
$$

when rollouts from the learned simulator and the source environment remain within a declared tolerance \(\varepsilon\) under those tests.

This is deliberately weaker than

$$
\hat E \equiv E
$$

as mechanisms.

It also makes a usually hidden variable explicit: **the policy is part of the evidence regime**.

GameNGen collects its corpus by first training an RL agent to play DOOM and recording that agent's actions and observations. The diffusion model then learns from those trajectories. The authors note that the agent does not explore every location and interaction, and that these coverage gaps become limitations of the learned simulator.

So the effective reconstruction pipeline is not simply

$$
E \rightarrow \text{traces} \rightarrow \hat E.
$$

It is

$$
E \xrightarrow{\pi_{\mathrm{data}}} \mathcal T_\pi
\xrightarrow{\text{learning}} \hat E.
$$

The learned surrogate is therefore a reconstruction of **the environment as encountered under a particular data-collection policy**.

This is the large-scale analogue of the coverage effect already measured in the repository's [Inverse-Reconstruction Benchmark](../../lab/benchmarks/inverse-reconstruction/README.md): if a trace never exercises part of a rule, that part is not identifiable from the trace. More data from the same narrow orbit need not repair the missing information.

---

## 4. The screen is also a state channel

GameNGen's context is short: the authors report a little over three seconds of history. Yet gameplay can remain coherent for much longer rollouts.

Part of the explanation is visible in the observation itself. DOOM's screen contains state-bearing features: health, ammunition, available weapons, room geometry, and other cues. The paper notes that the model can use these visible quantities and learned heuristics to infer facts such as approximate location or whether an area has probably already been traversed.

This means the observation is not merely an output to be rendered. It is also an input channel through which earlier state is repeatedly re-presented.

A useful decomposition is therefore

$$
\text{effective predictive state}
=
\text{model parameters}
+
\text{recent trace}
+
\text{state re-encoded in the current observation}.
$$

That does **not** mean the pixels constitute a complete Markov state. The model can fail when relevant information is neither visible nor contained in its short context. But it does show why "memory inside the network" is the wrong boundary for some functional questions.

This connects directly to [The Agent Is Not Where the Model Ends](../identity/the-agent-is-not-where-the-model-ends.md): persistent or recurrently available environmental structure can belong inside the effective control or prediction model even when it is outside the controller's private hidden state.

---

## 5. Where predictive equivalence breaks

The paper's most revealing limitation is not a blurry frame. It is a causal mistake.

The authors note that if the player repeatedly shoots, GameNGen can infer that an enemy should be present and may generate one. In the training distribution, shooting is strongly associated with enemies. But the causal direction in the source game is not "shooting creates enemies."

Schematically, the source process often contains

$$
\text{enemy present} \rightarrow \text{shooting},
$$

while a learned conditional regularity can behave as though

$$
\text{shooting} \Rightarrow \text{enemy likely}.
$$

This is a compact example of the gap between **predictive fit** and **causal recovery**.

Under familiar trajectories, both models may produce similar observations. Under a deliberately chosen intervention, the equivalence can break. Repeatedly firing in a context where no enemy should exist acts as a crude distinguishing query.

That places GameNGen naturally beside [The Witness Principle](../core/the-witness-principle.md): a passive corpus may leave candidate explanations behaviorally equivalent, while an intervention selected to separate them can expose a difference.

---

## 6. What GameNGen does and does not show

| Observation | Supported reading | Unsupported reading |
|:---|:---|:---|
| Interactive DOOM-like rollouts at real-time rates | an action-conditioned generative model can approximate a complex interactive observation process | the original DOOM program has been recovered |
| Long rollouts despite a short context | observations plus learned heuristics can carry enough state for substantial local continuity | the model contains a complete persistent world state |
| Strong visual fidelity | selected observation distributions are close under the reported metrics and human judgments | causal structure is correct |
| Failures outside agent coverage | the data-collection policy constrains what can be identified | more passive samples from the same policy necessarily recover missing transitions |
| Action-conditioned generation | actions can be incorporated into a learned transition surrogate | action correlations reveal the source system's causal graph |

The case therefore strengthens the bounded Generator Question while weakening any older, stronger slogan that equates understanding with recovery of the original hidden mechanism.

A system may construct a **useful generator** without reconstructing **the historical generator**.

---

## 7. A later architectural turn: explicit memory returns

A useful follow-up is Po et al., *MultiGen: Level-Design for Editable Multiplayer Worlds in Diffusion Game Engines* (2026), [arXiv:2603.06679](https://arxiv.org/abs/2603.06679).

MultiGen introduces a persistent external state independent of the model's context window and decomposes generation into **Memory, Observation, and Dynamics** modules. The motivation is not that GameNGen failed as a visual simulator. It is that editable, reproducible, shared worlds demand stronger persistence and controllability than a pure next-frame predictor naturally provides.

There is a revealing architectural loop here:

$$
\text{explicit engine state + dynamics + renderer}
$$

$$
\Downarrow
$$

$$
\text{history + action} \rightarrow \text{next observation}
\qquad \text{(GameNGen)}
$$

$$
\Downarrow
$$

$$
\text{memory + dynamics + observation}
\qquad \text{(MultiGen-style decomposition)}.
$$

The lesson is not that explicit state is always necessary. It is that the required factorization depends on the tests the system must survive. Visual continuation, editable level structure, multiplayer consistency, and causal intervention are different equivalence targets.

---

## 8. What this changes in the repository's model-identification arc

GameNGen suggests four refinements that should remain explicit in future reconstruction work.

### 8.1 Name the reconstruction target

Ask separately whether the goal is:

- parameter recovery inside a known family;
- source-mechanism recovery;
- predictive sufficiency;
- interactive behavioral equivalence;
- causal equivalence under interventions; or
- safety-preserving equivalence for a declared task.

Success under one target does not imply success under the others.

### 8.2 Treat the sampling policy as part of the model-identification problem

A trace corpus is not neutral. The policy determines which transitions become visible. Coverage is therefore not only a dataset statistic; it is a property of the coupling between observer and process.

### 8.3 Include the observation channel in the state audit

If the world repeatedly exposes state through HUDs, landmarks, files, logs, tool outputs, or other persistent traces, then the effective predictive system may use those structures as recurrent memory. Removing them is an intervention on the system, not merely a cosmetic UI change.

### 8.4 Test surrogates with distinguishing interventions

A model that reproduces passive or policy-typical trajectories should be challenged with actions chosen specifically because candidate mechanisms disagree about their consequences.

The relevant question becomes:

> **Where does an observationally adequate surrogate stop being interventionally adequate?**

That is a direct bridge from GameNGen to the repository's witness-generation programme.

---

## 9. A bounded experiment suggested by the case

A useful local benchmark would reproduce the GameNGen distinction without requiring a neural video model.

Take a small environment with an explicit latent state and renderer. Generate training traces under a deliberately biased policy. Fit two surrogate classes:

1. an **observation-only autoregressive predictor** conditioned on recent observations and actions;
2. an **explicit-state model** with a declared latent transition structure.

Then evaluate both on:

- in-policy passive rollouts;
- held-out regions of state-action space;
- longer horizons than the training context;
- interventions selected to separate plausible causal models; and
- observation ablations that remove state-bearing cues.

Measure at least three different relations:

$$
\text{prediction error},
\qquad
\text{rollout equivalence},
\qquad
\text{intervention divergence}.
$$

The expected result is not that the explicit-state model always wins. The useful outcome would be a map of **which test family requires which representation**.

That would extend the existing inverse-reconstruction work from

> *Can a generator be identified from traces?*

into

> *When is a surrogate generator sufficient, and which interventions reveal that it is not the source mechanism?*

---

## 10. Working conclusion

GameNGen is valuable here precisely because it resists a simple story about "understanding the game."

It shows that a model can acquire enough regularity from action-conditioned traces to become an interactive generator in its own right. It also shows that this generator can remain policy-bound, memory-limited, and causally wrong in ways that ordinary rollout quality does not immediately reveal.

The strongest repository-compatible reading is therefore:

> **Trace reconstruction can produce an adequate interactive surrogate without recovering the source mechanism.**

And the corresponding research question is:

> **Adequate under which policy, horizon, observation channel, intervention family, and equivalence relation?**

That is not a retreat from the Generator Question. It is the typed version of it.
