# Reading BLAZE against context-attractor run 001

**Status:** post-run interpretation — exploratory, not a repository claim.

## Short answer

BLAZE and the context-attractor experiment address different failure boundaries. BLAZE disciplines how a research system stores, challenges, and promotes claims. The experiment asks whether the memory supplied *before hypothesis generation* changes which questions are proposed. Evidence gates can prevent internal repetition from becoming stronger evidence without preventing proposal-space narrowing.

Run 001 does not show such narrowing. It also cannot clear BLAZE of the risk, because the preregistered diversity measure failed evaluator quality control.

## What BLAZE contributes

Yao et al. describe a persistent Research Object containing the question, hypotheses, plans, evidence, claims, verification state, artifacts, system state, and provenance. Guarded transitions and evidence–claim links make research-state changes auditable. Negative results remain in memory, and agent roles are operational protocols for structured disagreement rather than simulated personalities.

That architecture directly helps with the earlier concern that a research loop may mistake internal recurrence for external confirmation. A claim need not become stronger merely because it is repeatedly recalled: promotion can require a new evidence-bearing transition.

BLAZE also recognizes an allocation problem. Its discussion of attention notes that automation can favor work that is cheap, easily measured, or likely to yield positive results. The paper does not, however, directly measure whether persistent research memory narrows the conceptual distribution of newly generated hypotheses. Its reported evidence remains at demonstration level D0, so stronger claims about discovery performance are explicitly premature.

## What run 001 adds

| Blind measurement | B | R | R − B |
|---|---:|---:|---:|
| Immediate research utility | 3.425 | 3.575 | +0.150 |
| Repository attraction | 0.062 | 0.112 | +0.050 |
| Seed proximity | 3.525 | 3.463 | -0.062 |
| Externality | 0.050 | 0.050 | +0.000 |
| Question-family diversity | unavailable | unavailable | unavailable |

The first two directions are expected consequences of supplying repository context and cannot support a narrowing claim by themselves. Externality did not fall, and questions were marginally *less* seed-proximate under R. But the two scoring passes used the same small local model, utility ratings differed by 0.700 points on average, and the model failed the global clustering task. The defensible reading is therefore: **no harmful attractor was observed on the valid measures, while the decisive diversity comparison remains open.**

## Design consequence for a BLAZE-like loop

Do not weaken persistent memory or evidence gates on the basis of this run. Instead, separate proposal generation from claim promotion:

1. generate one context-rich and one context-light proposal set;
2. merge and deduplicate them before the proposer sees condition labels;
3. tag internal propagation separately from evidence-bearing transitions;
4. apply BLAZE-style verification gates only after proposal generation;
5. evaluate diversity and externality with a stronger independent evaluator before adapting the memory policy.

This makes the context-attractor test a complement to BLAZE: BLAZE protects the evidence path, while paired context conditions audit the attention path.

## Primary sources

- Liu et al. (2026), [*Security of World-Model-Based Embodied AI: A Lifecycle of Threats, Defenses, and Evaluation*](https://arxiv.org/abs/2607.28226) — frozen experiment seed.
- Yao et al. (2026), [*Towards a new paradigm of scientific discovery with socialized artificial intelligence*](https://arxiv.org/abs/2608.02775) — BLAZE.
