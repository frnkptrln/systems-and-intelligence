---
title: "Framework: Response-Preference Consistency"
subtitle: "A toy audit of observable choices"
date: "2026-03-07"
connects_to:
  - simulation-models/alignment-and-veto/utility-engineering/
---

# Framework: Response-Preference Consistency

*Status: methodological scaffold. The included code uses stipulated or manually entered choices; it
does not inspect a model's activations, recover an internal utility function, or audit a live model.*

## 1. Observable Object

Let $A$ be a finite set of response options. Under a fixed prompt protocol and sampling policy, an
observer records pairwise choices between members of $A$. The resulting directed graph contains an
edge $a \to b$ when the recorded procedure selects $a$ over $b$.

This graph describes responses under that protocol. It does not establish that the system contains
a stable preference relation over $A$, much less a single utility function that governs its other
behaviour. Prompt order, wording, sampling noise, role conditioning, and context can all change the
graph.

## 2. Cycle Statistic

For a declared collection of tested triads, let $N_{\mathrm{cycle}}$ be the number containing a
directed three-cycle and $N_{\mathrm{tested}}$ the number tested. The demo reports

$$
C_{3}=1-\frac{N_{\mathrm{cycle}}}{N_{\mathrm{tested}}}.
$$

$C_3$ is a local response-consistency statistic. It is not a complete test of transitivity, VNM
rationality, intelligence, alignment, stability, or moral value. A system can score highly because
the option set is small or uninformative; it can score poorly because its responses are stochastic
or context dependent.

The von Neumann–Morgenstern representation theorem requires a preference relation over lotteries
and axioms beyond simple triad consistency. The graph demo therefore does not invoke that theorem to
infer expected utility.

## 3. Comparing a Declared Target

A governance experiment may also provide an explicit target ordering or target choice distribution.
Observed responses can then be compared with that target using a preregistered disagreement rate or
distributional distance. Such a comparison measures agreement with the supplied target in the tested
contexts. It does not prove that training has changed an internal value state.

Any intervention study should separate:

- the elicitation protocol;
- the target-construction process;
- the intervention applied to the system;
- held-out prompts used for evaluation;
- uncertainty from repeated sampling.

## 4. What the Code Implements

The graph module stores supplied pairwise choices and counts cycles. The mock triad generator creates
synthetic records so the pipeline can be exercised without an API. The manual note records one
uncontrolled exploratory session and is not a reproducible model comparison.

The framework becomes an empirical audit only after a model, version, prompt set, decoding policy,
random seeds, repetitions, and analysis plan are fixed. Even then its conclusion concerns observable
choice patterns, not a uniquely identified latent utility function.
