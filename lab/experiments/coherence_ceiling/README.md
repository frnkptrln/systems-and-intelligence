# A Ceiling on Coupling: Survival in a Moving Environment

**Status:** Sketch, 2026-11-21. A toy model with its predictions fixed before it ran. The first commit of this directory contains this text through "Reading rules" and no code; the history is the record of the order. Results follow below once they exist.

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

Not yet run.
