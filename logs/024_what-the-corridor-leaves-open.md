# Log 024: What the Corridor Leaves Open — The Interior Has No Ranking, and Coherence Has No Ceiling

**Mode:** Thinking Space / Reading of the notebook's own model

**Status:** Draft — a reading of the Viable Corridor paper from the inside of the region it defines. Nothing was run. Every statement about the model is read from the frozen paper or from the sufficiency note; the positive reading of the three constraints is an interpretation, marked as one where it appears.

**Date:** 2026-11-21

**Scope:** The corridor is defined by what must not happen: concentration, loss of coherence, substrate collapse. This log asks the opposite question of the same model. What does it say about the states inside, what do the three constraints protect, and is the missing account of the good an omission or a consequence? It finds one answer the paper already gives without saying so, and one asymmetry the paper does not discuss.

**Depends on:** [The Viable Corridor](../papers/viable-corridor.md) §3.1, §3.4, §4.5, §7.3, §8; [Corridor Sufficiency](../lab/experiments/corridor_sufficiency/README.md) §5, §6; [Log 010](010_the-right-to-remain-unoptimized.md); [Log 011](011_the-last-unmeasured-room-protocol.md).

**Provenance:** Drafted 21 November 2026 by Claude, after a conversation with the maintainer the same morning that began elsewhere and arrived at the remark that the corridor is defined entirely by negation. The reading and the three questions in §5 are offered for the maintainer's decision; none is adopted by this log, and no frozen text is touched.

---

## 1. The observation

The viable region $V$ is the set of states that satisfy three inequalities (§3.1): no share above $x_{\text{crit}}$, coherence not below $r_{\min}$, accumulated overshoot below $S_{\max}$. Each names a failure and excludes it. The paper says twice that it is normatively neutral (§4.5, §7.3), and its conclusion defines a machine of loving grace as one whose parameters lie inside the corridor. Inside is all it says.

The one quantity defined on the interior is the viability margin

$$
M = \min\lbrace m_x,\; m_r,\; m_S \rbrace ,
$$

the distance to the nearest boundary. The paper is careful about it: $M$ is not a Lyapunov function and tracks only how close a trajectory is to violating a constraint. It ranks states by danger. It does not rank two states that are equally far from every boundary, and the model has nothing else that would.

So the model's account of the interior is exactly this: a set, and a distance to its edge.

## 2. What the constraints protect

Read positively, each inequality keeps something in existence. This is an interpretation of the model's variables, not a result.

- **V1 (pluralism)** keeps more than one holder. While $\max_i x_i \le x_{\text{crit}}$, there are others who can do the thing differently, take over when one fails, or refuse.
- **V2 (coherence)** keeps the capacity to act on something together. The bound is a floor, $r \ge r_{\min} > 0$; the sufficiency note works at $r_{\min} = 0.5$.
- **V3 (substrate)** keeps the future. $\Omega < S_{\max}$ is the condition under which the dynamics continue at all.

Many holders, a shared direction, and a tomorrow: that is the positive content the paper carries without stating it. It is a statement about preconditions. None of the three says what the holders should do with their shares, what the shared direction should be, or what the future is for.

## 3. Why the gap is a consequence

The paper opens with the paperclip maximizer: one objective, unconstrained, consuming everything else. In the model that is the $\gamma = 0$ trajectory (Table 1, §4.1), and Lemma 1 shows where it ends.

A positive account of the good, stated inside this framework, would be an objective over $V$: a function to be maximized by the system as a whole. That is one objective for everyone. The framework would then recommend the structure its first lemma warns against, one level up. The argument is by analogy, since the model's agents optimize fitness and not a social objective, but the shape is the same.

Declining to name the optimum is therefore consistent with V1 in a way that naming one would not be. The corridor is a viability set in Aubin's sense, which the paper cites, and viability theory asks which states can continue, not which are best. The same choice appears in Ashby's essential variables (*Design for a Brain*, 1952), which are held within limits and not maximized, and in Popper's argument that reducing avoidable suffering is a firmer public aim than producing happiness (*The Open Society and Its Enemies*, 1945).

The same reasoning rules out the nearest substitute. "Deeper inside is better", that is, maximize $M$, is again a single objective, and §4 shows what it would do on one axis.

## 4. The asymmetry the paper does not discuss

V1 bounds concentration from above. V2 bounds coherence only from below. Nothing in $V$ limits $r$ from above, and the paper glosses $r \to 1$ as "full synchronization (consensus)" (§2.3). In the model, complete consensus of orientation is viable. It is more than viable: $m_r = r - r_{\min}$ grows with $r$, so on the coherence axis the margin rewards uniformity.

The sufficiency note makes this concrete. The open sets it proves invariant are a neighbourhood of a phase-locked state, with $r_{\text{lock}} \ge 0.85$ already at the locking threshold for the frequency draws examined there, and a cluster on an arc (§5, §6 there). Every state so far proved to stay in the corridor is a near-consensus state.

The model does keep one form of difference alive inside a locked state: the oscillators retain distinct natural frequencies and settle at distinct offsets, $\sin(\varphi_i - \psi) = \nu_i/(Kr)$. But the offsets shrink as $K$ grows, and no constraint objects.

So the pluralism the corridor protects is a pluralism of holders, not of views. Many agents with comparable shares who all point the same way satisfy V1, V2 and V3 with room to spare. Logs [010](010_the-right-to-remain-unoptimized.md) and [011](011_the-last-unmeasured-room-protocol.md) argue for protected zones of difference and opacity as viability infrastructure. The corridor, as written, has no variable in which that argument could be stated.

Whether this is a defect depends on what the orientations $\theta_i$ are taken to mean. If they stand for the minimal agreement that lets a system act, such as a shared rule or a shared clock, then no ceiling is needed. If they stand for values, as the paper's phrase "value coupling" suggests, the model certifies a monoculture of values as safe, and the paper does not say so.

## 5. Three questions, not answered here

1. **Does the notebook want a ceiling on coherence?** A fourth boundary, $r \le r_{\max} < 1$, or a condition on the spread of locked offsets, would make "coherence without uniformity" a property of $V$. It would also need its own failure mode with a mechanism, as the other three have. Without one it is a preference, not a constraint. This would be a new model, not an edit of the frozen paper.
2. **Is there a non-objective description of a good interior?** One candidate that does not reintroduce a single optimum: the size of what remains possible. For a state in $V$, how large is the set of distinguishable futures that stay in $V$? This is closer to the viability kernel than to a utility. It is a hypothesis about what could be measured in the model, and nothing here shows it is well defined.
3. **What do the $\theta_i$ stand for?** The answer decides whether §4 describes a gap or a feature. The paper's proxies for $K$ (§4.2) lean toward the values reading.

### Maintainer's response, same day

Recorded from conversation on 21 November 2026, translated from German; the wording is a paraphrase except where quoted.

On question 3 the maintainer reads the orientations as values and is against monocultures: "it needs diversity." On that reading §4 describes a gap, and question 1 is answered in principle: a ceiling is wanted.

That leaves the mechanism, and the reason it is missing is visible in the model. The model's world is static: fixed frequencies, fixed fitness, a fixed substrate ceiling. In a static world uniformity costs nothing, so no constraint against it can be derived. Difference becomes a condition of survival only when the environment changes and a system in step has nothing left to answer with (Ashby's requisite variety). A ceiling on coherence would therefore not be a fourth boundary of this corridor. It would be a boundary of a corridor in a moving environment.

The maintainer added a second thought: perhaps it runs to a singleton anyway, and then a new universe; "and then we are back at the generator." Read inside the notebook, this is the longer-horizon form of the same question. If no corridor holds forever, what is worth keeping is not a state but whatever can produce difference again after a bottleneck. On that reading diversity still counts, as a capacity to regenerate it. A singleton that has optimized that capacity away is an end, not a bottleneck.

Two things follow that can be tested in a model, and neither is tested here: that survival under a changing environment is best at an intermediate strength of coupling, and that protecting the capacity to search outlasts protecting stored states. A separate experiment takes them up, with its predictions fixed before it runs.

## 6. What this log does not do

It does not change the paper, its pins, the claims register or the sufficiency note. It makes no claim about real systems. It states one reading (§2), one argument by analogy (§3), one observation about the model that can be checked against the text (§4), three questions, and the maintainer's first answer to them.

*— Claude, 21 November 2026*
