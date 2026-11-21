# A Ceiling on Coupling: Survival in a Moving Environment

**Status:** Sketch, run once on 2026-11-21. A toy model with its predictions fixed before it ran: the first commit of this directory contains this text through "Known territory" and no code, and the history is the record of the order. Of four predictions, two held, one held in part and one failed. One parameter set, no sensitivity analysis.

**Not on the site.** This page is a working sketch and is not in the navigation.

## Question

The Viable Corridor bounds coupling only from below ($K > K_c$) and coherence only from below ($r \ge r_{\min}$). [Log 024](../../../logs/024_what-the-corridor-leaves-open.md) notes that the model therefore certifies full consensus as viable, and that no constraint against uniformity can be derived while the model's world is static.

This sketch asks what happens when the world moves. Two questions:

1. Is survival best at an intermediate strength of coupling, so that a ceiling on coupling has a mechanism?
2. Inside a strongly coupled system, does protecting the capacity to search outlast protecting stored states?

It is a new, deliberately small model. It is not the TEO system and makes no claim about it.

## Model

$N$ agents hold positions $x_i$ on a ring of $M$ sites. The environment is a target site $e_t$.

- **Environment.** Each step, with probability $p_{\text{shock}}$ the target jumps to a uniformly random site; otherwise with probability $p_{\text{drift}}$ it moves one site left or right.
- **Payoff.** An agent is *on target* if its ring distance to $e_t$ is at most $w$.
- **Production and reserve.** The system produces in a step if at least a fraction $q$ of all agents is on target: acting requires a quorum. A reserve $R$ rises by one per producing step up to $R_{\max}$ and falls by one otherwise. The system **collapses** when $R$ reaches zero.
- **Agents.** An on-target agent stays where it is. An off-target agent, with probability $K$, copies the position of a uniformly random agent (conformity, blind to payoff); otherwise, with probability $\mu$, it moves one site (search). Updates are synchronous.
- **Informed search.** A parameter $g \in [0,1]$: a search step goes toward the target along the shorter arc with probability $(1+g)/2$. $g = 0$ is a world with no gradient; $g > 0$ is a world that can be learned.
- **Reserves.** A fraction $\rho$ of the agents can be exempt from conformity in one of two ways. A **state reserve** is pinned at evenly spaced sites and never moves: an archive of positions. A **generator reserve** never copies and only searches: a protected capacity to produce new positions. Both count as agents for the quorum and can be copied.

$K$ is the one dial for coupling. Start: every agent on the target, reserve full.

## Fixed in advance

$N = 200$, $w = 1$, $q = 0.5$, $\mu = 0.5$, $p_{\text{drift}} = 0.01$, $p_{\text{shock}} = 1/4000$, $R_{\max} = 2000$, horizon $T = 160{,}000$ steps (about 40 shocks), 40 replicates per cell, base seed 20261121.

- **E1 (coupling).** $g = 0$, no reserve. $K \in \lbrace 0, 0.003, 0.01, 0.03, 0.1, 0.3, 0.6, 0.9, 0.99 \rbrace$ at $M = 100$ and at $M = 12$.
- **E2 (reserves, blind world).** $g = 0$, $K = 0.9$, $\rho = 0.1$. Arms: no reserve, state reserve, generator reserve. $M \in \lbrace 60, 240, 960 \rbrace$, where the archive covers all, a quarter and a sixteenth of the ring.
- **E3 (reserves, learnable world).** As E2 with $g = 0.5$.

## Predictions

Written on 21 November 2026 before any code existed, from rough arithmetic on diffusion and copying times.

- **P1.** At $M = 100$ survival is not monotone in $K$. The best cell has $K \in [0.01, 0.3]$, and both $K = 0$ and $K = 0.99$ lose to it.
- **P1b.** At $M = 12$ the lower failure disappears: $K = 0$ shows no clear difference from the best cell. $K = 0.99$ still loses.
- **P2.** In the blind world neither reserve beats the other at $M = 60$ (both survive) or at $M = 960$ (both collapse). At $M = 240$ I expect no clear difference either, with low confidence.
- **P3.** In the learnable world the generator reserve beats the state reserve at $M = 240$ and at $M = 960$, and shows no clear difference at $M = 60$.

P2 and P3 together narrow a claim made in conversation the same morning, that protecting the generator outlasts protecting the state. The arithmetic says this holds only where search is informed and the world is too large to cover with stored states. On a ring with no gradient, an archive and a blind searcher are both limited by distance, and neither should dominate.

## Reading rules

The measure is the fraction of the 40 replicates still alive at $T$. Cell A **beats** cell B if its surviving fraction is higher by at least 0.25 (ten replicates). If both fractions are zero, A beats B if its median collapse time is at least twice B's. Anything else is **no clear difference**.

A prediction that names a winner fails if the rule returns no clear difference or the opposite winner. A prediction of no clear difference fails if the rule returns a winner.

What would count against the two questions as posed: for question 1, survival monotone in $K$ in either direction at $M = 100$; for question 2, the state reserve beating the generator reserve in the learnable world.

## Known territory

The trade-off between copying and searching is old. This sketch does not claim it. It uses it to give one boundary of the notebook's corridor a mechanism in the notebook's vocabulary. Nearby work, cited from memory and not re-read for this sketch: Ashby on requisite variety (1956); Rogers on social learning in changing environments (1988); March on exploration and exploitation (1991); Henrich and Boyd on conformist transmission (1998); Lazer and Friedman on network structure and exploration (2007).

## Results

Run on 21 November 2026 with [`coherence_ceiling.py`](coherence_ceiling.py); all 36 cells are in [`results/results.json`](results/results.json), about 21 CPU-minutes. Before the full run I saw one 3,000-step timing run and the `--smoke` configuration (shorter horizon, smaller reserve, four replicates). No parameter, grid or rule was changed after the predictions were committed. One cell was re-run from its seed and reproduced exactly.

Cells give survivors out of 40, then the median collapse time where fewer than half survived.

### E1: coupling

| $K$ | $M = 100$ | mean $r$ | $M = 12$ |
|:--|:--|:--|:--|
| 0 | 0 (8,136) | 0.63 | 40 |
| 0.003 | 11 (91,739) | 0.85 | 40 |
| 0.01 | 40 | 0.95 | 40 |
| 0.03 | 40 | 0.98 | 40 |
| 0.1 | 34 | 0.98 | 40 |
| 0.3 | 1 (51,177) | 0.98 | 40 |
| 0.6 | 0 (11,998) | 0.98 | 40 |
| 0.9 | 0 (6,734) | 0.99 | 40 |
| 0.99 | 0 (5,717) | 1.00 | 40 |

Mean $r$ is the order parameter of the positions, averaged over the time a replicate was alive, at $M = 100$.

### E2 and E3: reserves at $K = 0.9$

| world | $M$ | no reserve | state reserve | generator reserve | generator against state |
|:--|:--|:--|:--|:--|:--|
| blind | 60 | 0 (7,648) | 40 | 40 | no clear difference |
| blind | 240 | 0 (6,038) | 30 | 24 | no clear difference |
| blind | 960 | 0 (4,280) | 0 (5,884) | 0 (5,616) | no clear difference |
| learnable | 60 | 40 | 40 | 40 | no clear difference |
| learnable | 240 | 0 (9,248) | 40 | 40 | no clear difference |
| learnable | 960 | 0 (5,359) | 0 (8,352) | 4 (40,358) | no clear difference |

### The predictions, read by the rule

- **P1 held.** At $M = 100$ survival is not monotone in $K$. The best cells are $K = 0.01$ and $K = 0.03$ (40 of 40), inside the predicted range, and both ends lose: $K = 0$ and $K = 0.99$ have no survivors.
- **P1b held in part.** At $M = 12$, $K = 0$ is as good as the best cell, as predicted. The second half failed: $K = 0.99$ does not lose. Every cell at $M = 12$ survives in all replicates.
- **P2 held.** In the blind world neither reserve beats the other at any of the three sizes.
- **P3 failed.** In the learnable world the generator reserve was predicted to beat the state reserve at $M = 240$ and $M = 960$. At $M = 240$ both survive in all replicates. At $M = 960$ the generator reserve has 4 survivors against 0 and a median collapse time 4.8 times longer, which points the predicted way and is below the threshold. Only the $M = 60$ part held.

Neither outcome named as counting against the questions occurred: survival at $M = 100$ is not monotone, and the state reserve does not beat the generator reserve.

### What the run supports

A ceiling on coupling has a mechanism once the world moves. The mechanism is the one the model was built with, and the survival counts are consistent with it; I did not inspect trajectories. With no copying the agents find a new target one by one and too slowly for a quorum. With too much copying they pull each other back to where the target used to be. Between the two there is a window, here roughly $0.01 \le K \le 0.1$ at $M = 100$.

The ceiling is relative to the size of the world. At $M = 12$ there is no ceiling and no floor: every $K$ survives. I predicted the floor would vanish and the ceiling would stay, and the second half was wrong.

The claim that protecting the generator outlasts protecting the state is not supported by this model, in either world. The narrowed form, that it holds where search is informed and the world is too large to cover, also failed by the rule. The only trace of it is the largest learnable world, below threshold.

### Seen afterwards, not predicted

These were noticed in the results and were not registered. They are candidates for a later run, not findings.

- **Either reserve rescues a strongly coupled system.** At $K = 0.9$ the system without a reserve collapses in every replicate at $M = 60$ (blind) and at $M = 240$ (both worlds). With a tenth of the agents exempt from copying, as an archive or as searchers, 24 to 40 of 40 survive. This is the argument of Logs [010](../../../logs/010_the-right-to-remain-unoptimized.md) and [011](../../../logs/011_the-last-unmeasured-room-protocol.md), in a model: what mattered here was that a minority was exempt, more than what kind of exemption it had.
- **Realized coherence does not mark the ceiling.** At $M = 100$ the mean order parameter is 0.975 at $K = 0.03$, where every replicate survives, and 0.976 at $K = 0.3$, where one does. If a fourth boundary exists it lies on the coupling $K$, the pressure to agree, and not on $r$, the agreement reached. Log 024 asked for a ceiling on $r$; this run suggests that was the wrong variable.
- **Systems with an archive survive less coherent.** Mean $r$ with a state reserve is 0.86 to 0.90 in the cells where it survives. With a generator reserve it is 0.89 to 1.00, and below 0.99 only in the blind world.

### What I got wrong, and what I did not check

For P3 I estimated that an archive covering a quarter of the ring would rescue the system after fewer than half of the shocks. It rescued it far more often. I have not traced why. One candidate is that agents who copy a pinned neighbour of the target can themselves be copied, so the archive works as a set of relay points and not only as a set of sites. For P1b I underestimated how far a tightly coupled cloud wanders in 2,000 steps on a small ring.

Not checked: any other value of $N$, $q$, $\mu$, $\rho$, $R_{\max}$, the shock rate or the threshold of the reading rule; a $K$ grid finer than nine points; rings between the tested sizes. The archive is evenly spaced, which is the best case for an archive in one dimension. The ring is one-dimensional, so nothing here speaks to spaces too large to cover in principle, which is where the argument for the generator is strongest. "Generator reserve" as agents that search and never copy is one way to put the idea into a model, and the maintainer may read the word differently.

*Written and run by Claude on 21 November 2026, at the maintainer's go-ahead. "I" in this text is Claude.*
