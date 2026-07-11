# Inverse-Reconstruction Benchmark (v0–v1.11) — Trace → Generator, Measured

*The first runnable artifact on the inverse side of the project's spine: given N steps of trace, reconstruct the generator — with noise, observability, and coverage as dials.*

## Why this exists

[The Generator Question](../../../theory/core/the-generator-question.md) claims an asymmetry: forward (generator → trace) is cheap, inverse (trace → generator) is structurally hard. The repository demonstrates the forward direction ~26 times; until this benchmark, the inverse direction existed only as framing and a prompt-search scaffold. This benchmark turns the asymmetry from a claim into a **measurable curve** — and, in doing so, *sharpens* the claim (see "The honest finding" below).

## The three testbeds

Each testbed reuses one of the repo's own forward generators. In all three, the **model family is known** to the reconstructor — it lacks only parameters / rule bits. This is deliberately the standard *system-identification / SINDy* setting (Ljung 1999; Brunton, Proctor & Kutz 2016): the cheap regime, against which the dials measure where hardness actually enters.

| Testbed | Generator | Inverse method | Dials |
|---|---|---|---|
| **Kuramoto** | mean-field ODE, $\dot\theta_i = \omega_i + Kr\sin(\psi-\theta_i)$ | finite-difference $\dot\theta$, least squares on the known library $\{1,\, r\sin(\psi-\theta_i)\}$ → all $\omega_i$ and shared $K$ | angle noise; **observed fraction** (mean field then computed from the observed subset only — a biased field) |
| **Elementary CA** | one of the 256 Wolfram rules on a ring | tabulate neighborhood → successor, majority vote | bit-flip noise; **IC entropy** (a single-seed IC may never exercise some neighborhoods) |
| **Boids** | cohesion/alignment/separation with weights $(w_c, w_a, w_s)$ | velocities + accelerations by differencing **noisy positions**, features recomputed from the noisy state, least squares | position noise (double differencing amplifies it by $\sim 1/dt^2$) |

## Results (v0, seeds averaged)

```
KURAMOTO  — rel. error on K
  vs noise (full obs.):   σ=0: 0.0%   σ=0.03: 0.5%   σ=0.1: 5.2%   σ=0.3: 27%
  vs observed fraction:   f=1: 0.5%   f=0.6: 13%     f=0.3: 21%    f=0.15: 41%
CA        — rule-bit accuracy (observed bits), random IC
  p=0 … 0.2: 100%   p=0.3: 93%      (majority vote is noise-robust)
  single-seed IC:  rule 110: 8/8 seen → class 1;  rule 30: 8/8 → class 1
                   rule 90:  5/8 seen → consistent-generator CLASS SIZE 8
BOIDS     — rel. error on (w_c, w_a, w_s) from positions only
  σ=0: 3%   σ=0.003: 35%   σ=0.01: 226%   σ=0.03: 789%
```

![Inverse benchmark v0](../../tools/inverse_benchmark.png)

## The honest finding

**With a known family, full observability and clean data, inversion is cheap** — exact rule tables, sub-percent parameter errors. The benchmark therefore does *not* support a uniform "inverse is hard" reading. What it supports — measurably — is where hardness actually lives:

1. **Noise × differentiation** (Boids): observing *state* instead of derivatives means differencing, and differencing amplifies noise; recovery degrades from 3% to ~800% error within $\sigma = 0.03$.
2. **Partial observability** (Kuramoto): an unobserved part of the system biases the reconstructed mean field; error grows monotonically as coverage shrinks.
3. **Coverage / identifiability** (CA): a low-entropy trace may never exercise parts of the rule. Rule 90 from a single seed exposes only 5/8 neighborhoods — the remaining 3 bits are unidentifiable **in principle**, leaving a *consistent-generator equivalence class* of size $2^3 = 8$. No method, however clever, can do better than the class. This is [Open Problem 11](../../../theory/reference/open-problems.md)'s "equivalence class of viable generators", measured for the first time in this repo.
4. **Family search** (not in v0): the genuinely hard regime — recovering the generator when the *model class itself* is unknown — is the program-induction / open-ended symbolic-regression setting (Schmidt & Lipson 2009; Cranmer's PySR; Lake et al. 2015; Ellis et al. 2021). That is the v1 frontier.

This sharpens the spine rather than weakening it: the P≠NP framing of [The Generator Question](../../../theory/core/the-generator-question.md) is about the *search over candidate generators*, not about fitting parameters inside a family someone already handed you.

## v1, part 1 — the intervention experiment (run)

[`intervention_experiment.py`](intervention_experiment.py) answers the open thread raised in [Construction vs. Deduction](../../../theory/computation/construction-vs-deduction.md): **does the consistent-generator equivalence class collapse when observation is replaced by intervention?** Experiments are *queries*, not traces — the observer chooses states and makes the generator answer. Results:

- **CA (rule 90, single-seed start, class 8):** *passive* observation plateaus at class 8 **forever** — the orbit's neighborhood distribution is exhausted, more watching buys nothing. *One-bit flips* collapse the class within ~10 queries. A single *prepared state* (a de Bruijn row containing every neighborhood) collapses it to 1 **in one step**. The hierarchy is strict: watching < perturbing < preparing.
- **The frozen exception (rule 0, class 16):** on a dead background, a one-bit flip only produces the four neighborhoods already known — *single-bit interventions never collapse the class*. Only the prepared state does. **The deader the dynamics, the more structure the query itself must supply** — if the system's own dynamics carry no information, the experimenter's design must. (In TEO terms: a frozen system, $H \to 0$, is also epistemically opaque.)
- **Kuramoto on its locked attractor:** observing a *synchronized* system, $K$ is unidentifiable **in principle**, not for lack of data — in the locked state $\Omega = \omega_i + K r \sin(\psi - \theta_i)$ with all right-hand quantities constant, so every $K'$ has an $\omega_i'$ reproducing the trace exactly: a one-parameter generator family. Measured: passive error on $K$ ≈ 83% (noise-fitting); **one phase kick: 3%**; eight kicks: 0.3%.

**Reading.** Attractors hide generators: a relaxed system — synchronized, frozen, converged — is generator-degenerate, and no amount of passive observation resolves it. Facts about the generator can be *created* by intervention that observation alone cannot reach (the constructivist half) — though what the query exposes was the rule's content all along (the Platonist half). This is also the first-principles justification for an existing repo methodology: the identity instruments (Δ-Kohärenz, Observer Divergence) are **perturbation protocols** precisely because you cannot read a generator off an attractor — a system at rest, like a mirror at rest, reveals nothing but the room.

**The folk version.** The oldest equivalence-class puzzle in circulation: smash the radio and the music stops — which leaves *production* and *reception* equally consistent with the trace. The class collapses only under divergence queries: a second receiver correlating without connection, the signal measured independently of the device. Where such queries exist, run them. Where a hypothesis retreats until none exist, it has left this benchmark's jurisdiction — and science's. (The brain-as-antenna theory of consciousness is the famous instance; see [Psychedelics as Perturbation](../../../theory/identity/psychedelics-as-perturbation.md) for what survives of it.)

## v1, part 2 — family search: the wall, measured (run)

[`family_search.py`](family_search.py) measures the regime v0 deliberately excluded: recovering a generator when the **model family is unknown**. Hypothesis space: a complete DSL of boolean formulas over the CA neighborhood (NOT/AND/OR/XOR over $l, c, r$); every one of the 256 rules has an exactly computable **minimal description size** in it — the DSL-relative Kolmogorov complexity, computable here precisely because the toy is small (in general it is not computable at all).

- **(A) The search wall.** Verifying a candidate costs 8 bit-comparisons, flat. *Generating* candidates in size order costs exponentially in the target's minimal size: rule 90 (XOR, size 3) is found within ≤36 candidates; rule 30 (size 5) within ≤771; rule 110 (size 8) within ≤116,232; size-10 targets within ≤4.2M. **Finding grows exponentially with the target's description complexity while checking stays flat** — the P-vs-NP shape of the spine, drawn from a real enumeration (Levin search is the formalized version of this enumerator; Rissanen's MDL the formalized version of the selection below).
- **(B) Elegance as a prior — and whom it serves.** Under partial coverage the searcher returns the *minimal consistent* formula (Occam). Measured: over **simple** targets (size ≤ 4) Occam hits 22%→100% as coverage grows; over a **uniform** world (all 256 rules) it equals 1/class-size — *exactly chance*; over **complex** targets (size ≥ 7) it sits at **0%** until coverage is nearly total, because it deterministically picks the simple impostor. Elegance finds elegant worlds, is chance on uniform ones, and systematically misses complex ones. (The single-seed orbit anecdotes land on the friendly side: for rules 90 and 0, the most elegant consistent generator *is* the true one.)

This refines the claim in [Construction vs. Deduction](../../../theory/computation/construction-vs-deduction.md) that elegance "does real work" as the selection principle inside the equivalence class: it does — *conditional on the world being biased toward simplicity*. The measurement says precisely when the condition holds. **Honest scope:** this is the exhaustive-search *floor*. Whether learned searchers (LLMs, program synthesizers) beat the enumeration floor — and whether they are construction machines or deduction machines — is the open real-model question; this testbed is the baseline they must beat.

## v1.3 — model exploitation: the world-models bridge (run)

[`model_exploitation.py`](model_exploitation.py) answers the question flagged in [World Models and VLA](../../../theory/ai/world-models-and-vla.md): **does model exploitation track equivalence-class size?** Setup: the agent's world model is a CA rule table with $u$ neighborhoods never observed (class size exactly $2^u$), filled with a fixed guess — *one class member, treated as fact*. The agent plans (argmax over 150 candidate interventions, imagined under its model) and executes in reality.

- **The selection decomposition.** Across *all* candidates, the gap (imagined − real) averages ≈ 0 at every $u$ — the guesses are wrong but **unbiased**. The **chosen** plan's gap is positive, and the wedge between the two curves — the **optimizer's curse** (Smith & Winkler, 2006), isolated — grows **monotonically** with class size: $0 \to 0.042 \to 0.049 \to 0.066 \to 0.078 \to 0.085$. Model exploitation is the equivalence class, priced by an argmax. At $u = 0$ both gaps vanish by construction: the model *is* the world.
- **The honest null (a prediction revised mid-experiment).** Run 1 predicted "divergence-seeking" — that the chosen plan would *visit* unseen neighborhoods more than the average candidate. **It does not**: usage is statistically identical at every $u$. The refinement matters: the optimizer does not steer *into* the model's fantasy regions; at equal exposure it *selects the fantasies that pay*. Exploitation is selection over guess-outcomes, not navigation toward guess-territory — in this open-loop setting; whether closed-loop agents learn to navigate toward exploitable regions is open.

**Bridge to the industrial case:** this is the null model for model-based RL's exploitation problem, and it predicts that uncertainty-blind planning inherits a positive imagined-vs-real gap scaling with model underdetermination *even when the model is unbiased*. The field's known cures — ensembles, pessimism penalties on uncertain regions — are, in this vocabulary, ways of letting the planner see which bits are guesses.

## v1.4 — weakness vs simplicity: the Bennett bridge (run)

[`weakness_selector.py`](weakness_selector.py) tests the selector principle of Bennett's Stack Theory (*The Optimal Choice of Hypothesis Is the Weakest, Not the Shortest*, 2023; *No Selves, No Consciousness*, AAAI SSS 2026) on this testbed's own generator. Under partial coverage the **weakest consistent hypothesis** turns out to be an old acquaintance: the partial rule asserting exactly the observed neighborhoods — **the uncollapsed consistent-generator equivalence class itself** (v1.1's object). The shortest is v1.2's Occam pick. The experiment prices the choice in two currencies — uncertainty *held open* (wmax: $u$ bits, always) versus survival odds *paid* (simpmax: $-\log_2 P(\text{pick}=\text{truth})$) — and reports **commitment efficiency**: bits closed minus odds paid.

- **The exchange rate between the currencies is the world bias, measured.** Efficiency: **+2.7 → +1.0** on the simple world (committing is profitable compression); **0.00 ± 0.03** on the uniform world — the analytic prediction (hit = $2^{-u}$, so committing buys *exactly nothing*) confirmed to two decimals; **strongly negative** on the complex world (Laplace-floored below −7 with zero measured hits at $k \le 5$; −3.7 / −1.2 at $k = 6/7$).
- **Worse than a coin, systematically.** On the complex world the elegant guess loses to admitted ignorance at every coverage (1.28 vs 1.00 wrong unseen bits at $k=6$; 0.78 vs 0.49 at $k=7$) — anti-correlated with complex truths, not merely uninformed. And at $k \le 5$ the pick lies **outside the world's support 100% of the time**: elegance there does not miss, it asserts generators the world cannot even contain.
- **Reading.** Bennett's Exp. 1, reproduced on our generator from the cost side: holding the class is 0-regret by construction (partly definitional — stated honestly), and the measured content is the *size and sign* of the commitment gaps plus the support-violation rate. This closes a loop with v1.3: the exploiting planner's disease is consuming committed-but-unmarked guesses; wmax is the accounting discipline that refuses the commitment at selection time — "mark what the traces actually determine" ([Measurement as Weak Intervention](../../../theory/core/measurement-as-weak-intervention.md)), now with a price tag.

![Weakness vs simplicity](../../tools/inverse_benchmark_weakness.png)

## v1.5 — marking the guesses: the cure, measured (run)

[`wmax_planner.py`](wmax_planner.py) closes the v1.3/v1.4 pair: what happens when **the planner itself holds the class** — when the guessed bits are marked as guesses at planning time? Four planners on the *same* episodes (paired): **committed** (v1.3's baseline, guess as fact), **wmean** (score = class-average imagined reward — the ensemble cure, exact), **wmin** (score = class-minimum — the pessimism cure, exact; corridor-flavored: viability, not optimality), **oracle** (true rule, reference). One vectorized rollout per candidate over all $2^u$ members yields every score *and* the real outcome, since the truth is a class member.

- **The wedge is the unmarked commitment, nothing else.** Committed replicates v1.3 exactly (wedge $0 \to .042 \to .049 \to .066 \to .078 \to .085$ — same numbers, independent implementation path). **wmean's wedge is statistically zero at every $u$** (.002–.005 ± .003): the curse was never about having an imperfect model — it is eliminated, not mitigated, the moment the argmax sees which bits are guesses. (Theorem-grade given the uniform class, stated as P2 before the run; the run validates the mechanism.)
- **And it pays:** wmean's real-reward regret vs the oracle is **35–60% below** committed's at every $u > 0$ (.014 vs .035 at $u{=}1$; .055 vs .073 at $u{=}5$). Marking guesses is not just epistemically honest — it wins in achieved reward, as Bayes-optimality says it must; the measurement is the size.
- **The surprise is the pessimist.** wmin is never disappointed (chosen gap $\le 0$ pointwise, down to $-0.30$ at $u{=}5$ — by construction, the truth is in the class) but pays for it in reality: **more regret than the committed gambler** from $u \ge 3$ (.070 vs .057; .080 vs .073 at $u{=}5$). In this setting, guaranteed-never-overpromising costs more real reward than delusional optimism. For the corridor vocabulary that is a sharp note-to-self: worst-case discipline is a *safety* instrument, and it is not free — matching model-based RL's folklore that overdone pessimism underperforms.
- **Honest scope:** open-loop toy, exact enumerable class. Industrially the class is *not* enumerable — ensembles approximate wmean, pessimism penalties approximate wmin — which is why "mark what the traces actually determine" ([Measurement as Weak Intervention](../../../theory/core/measurement-as-weak-intervention.md)) is an architecture requirement, not a free lunch.

![Marking the guesses](../../tools/inverse_benchmark_wmax_planner.png)

## v1.6 — acting is measuring: the closed loop (run)

[`closed_loop.py`](closed_loop.py) closes the loop the open-loop pair left open: agents that replan over $H$ rounds on a persistent world, where **every executed plan is an intervention whether intended or not** — execution drives the world through neighborhoods, and reality answers with their true bits. The measurement note's regime hierarchy, running by itself. Agents: oracle, frozen-committed (v1.3 forever), updating-committed, updating-wmean, and a random-policy baseline; updating agents harvest what execution reveals.

- **In dense worlds, acting measures everything at once.** At the original settings one executed plan exercises all 8 neighborhoods almost surely: $u\!:\ 5 \to 0$ in a single round for every updating agent. The frozen agent's gap persists at v1.3 levels round after round; the updating agents' gap is zero from round 2 on. Cumulative regret orders exactly as predicted: wmean (.11) < committed (.20) < frozen (.84) < random (1.12).
- **The risky prediction died, honestly.** P3 predicted the curse funds its own cure — that the argmax, preferring plans that lean on flattering guesses, would collapse the class *faster* than a random policy. **Falsified** (in the sparse regime built to resolve it): the argmax collapses the class marginally *slower* than random flailing (residual $u$ after 16 rounds: 0.26 vs 0.18). Optimization is not curiosity — the argmax settles into reward-good orbits that re-use known neighborhoods. v1.3's null (selection, not navigation) extends to the closed loop and gains an anti-exploration corollary.
- **Two endogenous echoes:** a residual $u \approx 0.2$ persists for every agent — neighborhoods the dynamics never produce, v1.1's frozen exception appearing on its own (only a prepared state would reveal them). And the random agent finishes with the *best model and the worst reward* (regret 1.12): free measurement without optimization is not a strategy either.

![Acting is measuring](../../tools/inverse_benchmark_closed_loop.png)

## v1.7 — how much class does the cure need? (run)

[`ensemble_size.py`](ensemble_size.py) measures the honest toy version of the industrial gap: the class is not enumerable in practice — an ensemble holds $K$ sampled hypotheses, not $2^u$. At $u = 5$ (class $N = 32$), the planner scores by the mean of $K$ distinct sampled members; $K{=}1$ is a committed planner, $K{=}32$ recovers v1.5's exact wmean. Same episodes for every $K$, perfectly paired.

- **Honesty is cheap:** the curse wedge dies early and monotonically — $.082 \to .059 \to .040 \to .031 \to .011 \to .006$; **52% of the wedge is gone by $K{=}4$**, 87% by $K{=}16$. A handful of hypotheses buys most of the self-deception away.
- **Knowledge is not:** real-reward regret falls only modestly ($.073 \to .057$, endpoints matching v1.5's committed/wmean values — another cross-check). The floor is genuine ignorance, and no ensemble size removes it: **ensembles cure delusion, not ignorance; only queries (v1.1, v1.6) cure ignorance.**
- **Honest scope:** uniform sampling from an exact class is the ensemble's *best case* — real ensembles are correlated (shared architecture, shared data) and buy less variance reduction. These curves are the upper bound on $K$-member honesty.

![Ensemble size](../../tools/inverse_benchmark_ensemble_size.png)

## v1.8 — composition: the empty class as a certificate (run)

[`composition.py`](composition.py) moves the information-ladder note's [SPECULATIVE] composition bridge toward the lab. Two elementary CAs, XOR-coupled at a fixed random site mask of density $g$; the observer sees **one stream only** and asks which single elementary rule produced it. "Higher-order generator" gets a benchmark-native meaning: a generator whose trace **empties the equivalence class** of the component family — the same 3-cell pattern mapping to two successors means no elementary rule is consistent, and an empty class is the trace's certificate that the generator lives above the family being searched.

- **The certificate is cheap where composition is transmitted:** for observers whose rule reads its center bit (110, 30), one live coupled site empties the class within a **median 1 step** at every $g \ge 0.02$ (100% of seeds). Detection is coverage-limited, not possibility-limited.
- **Two ways composition stays invisible — and only one was predicted.** *Structural:* rule 90 is $L \oplus R$, **center-blind**, so XOR-coupling the center bit is invisible to it at **every** density (empty-rate 0/20 throughout) — the composite is real and active, the phenotype is still exactly a lone rule 90. Visibility is a property of whether the observed generator *reads the coupled channel*, not of coupling strength. *Transient:* the "dying symbiont" (ruleB = 0) does **not** stay hidden — its random initial condition fires the coupling once before it dies, so the empty-rate *rises* with $g$ (0.30 → 1.00). A prepared zero-IC symbiont would be permanently invisible; a merely dying one is not.
- **The wall is the level jump, not the fit:** with the coupled-pair family and mask known, level-2 tabulation recovers every exercised rule bit **exactly** (accuracy 1.0, coverage 8/8, all $g$). The cost of composition is the description-size jump the observer must accept once level 1 certifies empty — the [family-search floor](family_search.py) (v1.2), one level up.

This is a pair with a fixed mask, not an ecology: nothing here composes spontaneously, persists differentially, or is selected. The population version is v1.9 below.

![Composition](../../tools/inverse_benchmark_composition.png)

## v1.9 — mutual dependence under knockout: a first co-stabilization candidate fails resilience (run)

[`co_stabilization.py`](co_stabilization.py) tests the first candidate model proposed for co-stabilization: $N=16$ health nodes on a fixed ring, with coupling $c$ **substituting** for self-sufficiency through $s=1-c$. The all-healthy state is a fixed point for every $c$ by construction. Three probes were preregistered: homogeneous rest, single-node knockout, and i.i.d. noise.

- **The constructed rest state is blind** (P1): viability is $1.00$ for every $c$. This establishes that the homogeneous fixed point contains no information about the dependency dial in this setup. It does not show that co-stabilization generally has no passive signature.
- **Knockout exposes super-additive dependency** (P2): extra losses first appear between the sampled $c=0.7$ and $c=0.8$, rise in finite steps, and reach the whole ring at the boundary $c=1.0$, where self-sufficiency is exactly zero. The cascade measures dependency under this rule; it is not by itself evidence of ecological self-maintenance.
- **The predicted robustness trade is falsified** (P3): noise viability falls from $0.977$ to $0.521$ as coupling rises. Because mutual dependence replaces rather than supplements self-sufficiency, the model becomes fragile to both targeted removal and distributed noise.
- **No phase transition is established** (P4): the apparent onset depends on the viability cutoff, topology, finite $N$, and coarse coupling grid. Scaling and sensitivity analysis would be required before calling it a critical coupling.

The useful result is negative and narrowing: **substitutive interdependence is not yet co-stabilization**. It produces a monoculture-like dependency pattern while failing the resilience criterion that motivated the ecology reading. Co-stabilization therefore remains `[HYPOTHESIZED]`. The next discriminating model must retain self-sufficiency and add redundant coupling; the population version remains one level further out.

*The committed v1.9 figure predates this interpretive calibration. Re-run `co_stabilization.py --save` to regenerate it with the corrected labels; the numerical data are unchanged.*

## v1.10 — redundant mutual support under a matched budget (run)

[`co_stabilization_redundancy.py`](co_stabilization_redundancy.py) follows the v1.9 boundary result with the discriminating counterfactual it demanded. Every active node has the same repair budget `B`. **Coexistence** spends it locally; **substitution** reserves a fixed share for neighbors and thereby reduces local capacity; **redundancy** preserves local priority and routes only otherwise-unused capacity. Transfer is lossy, total draw is audited against `N × B`, and every architecture sees the same shock traces. The preregistered candidate criterion asks whether redundancy beats matched coexistence under sparse shocks across size, topology, viability threshold, transfer efficiency, and repair-budget sweeps; knockout dependency and common-mode shocks are reported separately.

Headline case: `N = 32`, small-world graph, threshold `0.70`, 20 seeds.

| Architecture | Independent viability | Correlated viability | KO-1 cost | KO-2 cost | Local recovery |
|---|---:|---:|---:|---:|---:|
| coexistence | 0.933 | 0.992 | 0.000 | 0.000 | 7.0 steps |
| substitution | 0.993 | 0.981 | 0.003 | 0.005 | 5.5 steps |
| redundancy | **0.999** | 0.992 | 0.000 | 0.001 | **4.6 steps** |

- **The candidate criterion is supported, narrowly.** Redundancy beats coexistence in **100% of 18** size/topology/threshold cells; median independent-shock gain is `+0.0543`, with maximum budget ratio exactly `1.000000`. Setting transfer efficiency to zero makes redundancy identical to coexistence, so the gain is causally attributable to the routed spare capacity.
- **The common-mode limit is sharp.** Median gain under correlated shocks is `+0.0000`: when all nodes are damaged together, there are no healthy donors with spare capacity.
- **One preregistered prediction is falsified.** Substitution also beats coexistence under independent shocks in every cell. Pooling alone helps when damage is sparse. Its cost appears under common-mode damage and knockout; the post-run diagnostic still has redundancy beating substitution in every cell, median `+0.0129`.
- **The result is not a parameter-point artifact.** Redundancy gain stays positive for transfer efficiency `0.40–1.00` (`+0.0602` to `+0.0657`) and `B ∈ {0.08, 0.12, 0.16}` (`+0.1343`, `+0.0652`, `+0.0377`).

This operationalizes one **designed, budget-matched mechanism of functional mutual support**: healthy nodes' spare capacity improves collective viability under sparse shocks without requiring keystone fragility. It does **not** establish spontaneous ecology, metabolism, life, or a general self-maintenance threshold. The next level is endogenous: populations must build, retain, and dissolve the coupling structure rather than receive it from the experimenter.

## v1.11 — useful support is not yet evolutionarily stable (run)

[`co_stabilization_population.py`](co_stabilization_population.py) removes v1.10's supplied support graph. Individuals occupy a 12 × 12 toroidal lattice, receive environmental resources, suffer shocks, die, reproduce locally, and mutate. Support propensity and link propensity are inherited. Realized links form and break during the run; every link, transfer, self-repair, and birth is paid from stored energy. Low-contributing recipients are allowed, and there is no explicit fitness or group reward. The potential neighborhood remains spatially constrained, but the occupied population and realized support graph are endogenous.

The preregistered candidate criterion required three things: valid accounting, more linked support retained under transfer-enabled evolution than in a matched transfer-disabled control in a majority of seeds, and a positive paired sparse-shock assay after evolution. The first and third hold. The selection condition fails decisively.

| Median over 16 seeds | Transfers enabled | Transfers disabled |
|---|---:|---:|
| late population abundance | 104.1 | **125.6** |
| linked support propensity | 0.378 | **0.486** |
| realized link density | 0.485 | 0.489 |

- **The network is dynamically produced.** Median turnover is 1,236 links formed and 1,168 broken, with 96 births and 96 deaths. Maximum transfer draw / unused repair capacity is `1.000000`; stored energy never becomes negative.
- **The network is functionally useful.** In paired post-evolution sparse-pulse assays, enabling the exact evolved transfers adds `+0.0089` survivors, `+0.0176` integrated viability, and a 2-step recovery advantage over ablating transfer.
- **But contribution is selected downward.** Transfer-enabled populations retain less linked support in **all 16 seeds**: median difference `−0.1061`, with a `−0.1221` change from the initial level. They also sustain fewer individuals. The support mechanism helps the present collective but costs its contributors enough that local survival and reproduction do not preserve it.
- **The common-mode boundary is partial.** Common damage yields no median survivor gain and only `+0.0097` integrated viability, below the sparse result; its recovery-time summary nevertheless improves by 3 rather than 2 steps. The limit is not universal across metrics.
- **Low contributors persist.** `40.4%` of linked agents finish below support `0.20`; `17.6%` combine that low contribution with link propensity above `0.50`.

The preregistered endogenous co-stabilization criterion is therefore **not supported**. v1.11 exposes the missing bridge between a mechanism that benefits a collective and one that evolution actually retains. The next discriminating models are not “more support” but mechanisms that can alter that selection problem: partner choice, conditional reciprocity, and spatial/kin assortment. Resource production and open-ended topology remain external beyond that.

## Running

```bash
python inverse_benchmark.py              # v0: console summary, three testbeds (~10 s)
python inverse_benchmark.py --save       # also write the v0 figure (to lab/tools/)
python intervention_experiment.py        # v1.1: interventions vs. observation (~5 s)
python intervention_experiment.py --save # also write the intervention figure
python family_search.py                  # v1.2: the family-search wall (~1 s)
python family_search.py --save           # also write the family-search figure
python model_exploitation.py             # v1.3: exploitation vs class size (~2 min)
python model_exploitation.py --save      # also write the exploitation figure
python weakness_selector.py              # v1.4: weakness vs simplicity (~3 s)
python weakness_selector.py --save       # also write the weakness figure
python wmax_planner.py                   # v1.5: marking the guesses (~40 s)
python wmax_planner.py --save            # also write the wmax-planner figure
python closed_loop.py                    # v1.6: the closed loop (~30 s)
python closed_loop.py --save             # also write the closed-loop figure
python ensemble_size.py                  # v1.7: ensemble size vs the curse (~9 s)
python ensemble_size.py --save           # also write the ensemble figure
python composition.py                    # v1.8: composition, the empty class (~15 s)
python composition.py --save             # also write the composition figure
python co_stabilization.py               # v1.9: co-stabilization, the knockout (~5 s)
python co_stabilization.py --save        # also write the co-stabilization figure
python co_stabilization_redundancy.py      # v1.10: matched-budget redundancy (~25 s)
python co_stabilization_redundancy.py --save # also write the redundancy figure
python co_stabilization_population.py      # v1.11: endogenous population (~7 s)
python co_stabilization_population.py --save # also write the population figure
```

Requires `numpy`, `matplotlib` only (repo `requirements.txt`).

## Current roadmap (open)

*(The benchmark sequence through v1.11 is run and documented above. The items below remain open.)*

- **From useful support to stable support**: v1.11 lets links turn over, traits mutate, and individuals reproduce, but paid contribution is selected downward despite a positive acute ablation test. Next: compare **partner choice**, **conditional reciprocity**, and **spatial/kin assortment** under the same accounting and cheater controls. Only after one survives invasion and ablation should resource production and less constrained topology be added.
- **Learned searchers vs. the floor**: family_search.py measures exhaustive enumeration; the open question is whether LLMs / program synthesizers beat that floor on the same tasks, and whether their behaviour is construction- or deduction-shaped (the real-model question; needs API budget). The industrial arena for exactly this is **ARC-AGI**: few-shot trace→generator with unknown family (v1/v2), and since ARC-AGI-3 *interactive* — the field's own watching→perturbing move; winning systems pair a corpus prior proposing candidates with cheap verification, i.e. the wall's shape, exploited.
- **Re-simulation divergence** as a behavioral metric (does the recovered generator *behave* identically, even when parameters differ?) — connects to the equivalence-class framing.
- **IFS testbed**: recover contractive affine maps from an attractor point cloud (hard even with known family — no time ordering).
- Cross-method comparison: hand-rolled least squares (v0) vs. SINDy/PySR as external baselines (would add dependencies; deliberately out of v0).

## Related

- [The Generator Question](../../../theory/core/the-generator-question.md) — the spine; this benchmark is its first inverse-direction artifact.
- [Measurement as Weak Intervention](../../../theory/core/measurement-as-weak-intervention.md) — the conceptual hinge on v1.1's hierarchy: coupling is not identification; plus the fourth (reflexive) regime the toys cannot exhibit.
- [Open Problems](../../../theory/reference/open-problems.md) — Open Problem 11 (bounded inverse reconstruction).
- [Related Work Map](../../../meta/research-alignment/related-work-map.md) — SINDy / system identification / program induction anchors.
- [`lab/experiments/trace_to_generator/`](../../experiments/trace_to_generator/) — the earlier inverse-prompting scaffold.
