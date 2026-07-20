#!/usr/bin/env python3
"""
co_stabilization_selection.py

Benchmark v1.12 — can any partner rule make costly support retainable?

QUESTION
v1.11 built an endogenous support network and found it functionally useful
and evolutionarily doomed: contribution was selected downward in all 16 seeds.
The cause is structural rather than mysterious. In v1.11 a link forms with
probability proportional to sqrt(link_gene[u] * link_gene[v]); the support
gene never enters. A recipient that contributes nothing is exactly as
attractive a partner as one that contributes everything, so paying for
support is a pure loss. v1.12 asks the follow-up the roadmap named: does
making contribution VISIBLE to partner formation change the selection
outcome, and what does that visibility cost?

FOUR ARMS, ONE ACCOUNTING
  blind            v1.11 unchanged. Partner formation ignores support.
  partner_choice   Both endpoints weight formation by the other's support,
                   and links to low contributors break faster. This is
                   "legitimate refusal" as a link rule.
  reciprocity      Formation is blind, but a donor scales its offer to each
                   neighbour by what that neighbour has given back. Per-edge,
                   directional, decaying memory.
  assortment       Formation favours genetically similar partners
                   (greenbeard-style), independent of absolute contribution.

THE MATCHED-COST CONTROL
v1.10's lesson was that a gain must come from reallocation, not from a larger
budget. The information analogue applies here: partner_choice, reciprocity,
and assortment all need knowledge about a partner that the blind arm never
buys. Each therefore pays ASSESS_COST per assessed incident edge per step,
from the same energy pool as metabolism, links, repair, and reproduction.
Free information would rig the comparison.

PREREGISTERED PREDICTIONS (fixed before the first full run)
  P1 ACCOUNTING: energy never negative; no donor exceeds its unused repair
     capacity; link, transfer, assessment, and birth costs paid explicitly.
     The blind arm must reproduce v1.11 exactly, making "identical
     accounting" a checked fact rather than a claim.
  P2 RETENTION: at least one of partner_choice / reciprocity / assortment
     reverses the sign of support selection — linked support under enabled
     transfer >= its matched disabled control in a majority of 16 seeds.
     The v1.11 baseline to beat is median delta -0.1061 with 0% positive
     seeds.
  P3 INVASION: a mechanism passing P2 also bounds invasion. Seeded with a
     cooperator population and 5% support~0 mutants, cheater frequency stays
     below fixation rather than sweeping.
  P4 COST BOUNDARY: the advantage disappears at a high enough assessment
     cost. A mechanism whose benefit survives every cost is more likely
     mis-accounted than powerful.
  P5 COMMON MODE: the paired benefit is smaller under correlated damage than
     under sparse damage, as in v1.10 and v1.11. A mechanism that abolishes
     this limit is suspect.

CANDIDATE CRITERION
A mechanism receives a first bounded positive result only if P1 holds, P2
holds in >50% of seeds, P3 bounds invasion, and P4 exhibits a real cost
boundary. If no arm satisfies all four, the result is reported as a
falsification in the v1.11 manner: informative, and locating the next
missing ingredient rather than hiding it. Nothing here would establish
metabolism, life, open-ended evolution, identity, or consciousness.

RESULT (first full run; 16 seeds, 600 steps, 144 sites)
  P1 CONFIRMED: maximum transfer draw / unused repair capacity = 1.000000;
     minimum stored energy = 0.000000 across all four arms. The blind arm
     reproduces v1.11 trajectory-for-trajectory (abundance, linked support,
     link density, and link counts identical), so the arms differ only in
     the partner rule and its paid information.
  P2 NOT SUPPORTED: no arm reversed the sign in a majority of seeds.
     blind -0.1056 (0% of seeds positive), partner_choice -0.0287 (19%),
     reciprocity -0.0999 (0%), assortment -0.0956 (0%). partner_choice
     weakens the loss by roughly a factor of four but does not invert it.
  P3 CONFIRMED for partner_choice, with an important qualification. Seeded
     with 5% cheaters, the fraction of LINKED agents below support 0.20
     ends at 1.2% under partner_choice versus 22.0% under blind. But the
     cheater fraction in the population as a whole still rises to 27.1%.
     Partner choice protects the network, not the population: cheaters are
     excluded rather than eliminated, and persist unlinked.
  P4 NOT AS PREDICTED: partner_choice's delta moves toward zero as
     assessment cost rises (-0.0351 at zero cost to -0.0012 at 0.0100)
     instead of losing its advantage. The mechanism is a rewiring rule, so
     a higher price suppresses link formation in both treatment and control
     rather than taxing a benefit. The predicted cost boundary does not
     apply to a rule of this shape; reciprocity and assortment show no
     advantage to bound at any price.
  P5 CONFIRMED: every arm shows a smaller paired gain under correlated than
     under sparse damage (partner_choice +0.0035 vs +0.0088).

  Post-hoc diagnostic, not part of the criterion: measured against the
  starting level rather than the matched control, partner_choice is the
  only arm that does not decay -- +0.0657 versus -0.1277 (blind), -0.0875
  (reciprocity), -0.0835 (assortment). Under a rule that rewards support
  even when transfer is off, the matched control rises too, so the
  preregistered on-off delta understates absolute retention. Which of the
  two comparisons is the right question is now itself an open problem;
  the preregistered one is reported as the verdict.

The preregistered candidate criterion is NOT SUPPORTED. Making contribution
visible to partner formation is not sufficient to make it evolutionarily
retainable in this model. It does sort the network: costly support survives
where partners can refuse, while non-contributors persist outside it.

Usage:
    python co_stabilization_selection.py
    python co_stabilization_selection.py --save
"""

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np

SIDE = 12
STEPS = 600
ASSAY_STEPS = 36

RESOURCE_MEAN = 0.074
METABOLISM = 0.055
ENERGY_CAP = 2.0
REPAIR_BUDGET = 0.10
TRANSFER_ETA = 0.75
LINK_COST = 0.0025
LINK_FORM_RATE = 0.075
LINK_BREAK_RATE = 0.020
DEATH_CUTOFF = 0.045
BACKGROUND_DEATH = 0.0008

BIRTH_THRESHOLD = 1.10
BIRTH_COST = 0.58
CHILD_ENERGY = 0.34
CHILD_HEALTH = 0.82
BIRTH_RATE = 0.12
MUTATION_SIGMA = 0.035

# v1.12 additions. ASSESS_COST is the price of partner information; the
# sweep in P4 varies it. CHOICE_STRENGTH scales how strongly a low
# contributor loses links. MEMORY_DECAY governs reciprocity's forgetting.
ASSESS_COST = 0.0012
CHOICE_STRENGTH = 0.10
MEMORY_DECAY = 0.92
MEMORY_GAIN = 6.0

MECHANISMS = ("blind", "partner_choice", "reciprocity", "assortment")
INFORMED = ("partner_choice", "reciprocity", "assortment")

EPS = 1e-12


@dataclass
class Environment:
    resource: np.ndarray
    local_hit: np.ndarray
    local_magnitude: np.ndarray
    global_hit: np.ndarray
    global_magnitude: np.ndarray
    background_death: np.ndarray
    birth_gate: np.ndarray
    birth_choice: np.ndarray
    birth_priority: np.ndarray
    mutation_support: np.ndarray
    mutation_link: np.ndarray
    link_form: np.ndarray
    link_break: np.ndarray


@dataclass
class Population:
    occupied: np.ndarray
    health: np.ndarray
    energy: np.ndarray
    support: np.ndarray
    link_gene: np.ndarray
    links: np.ndarray
    # Directional per-edge memory: recv_u[e] is what edge_u[e] received from
    # edge_v[e]. Only reciprocity reads it; every arm carries it so that the
    # state shape stays identical across mechanisms.
    recv_u: np.ndarray
    recv_v: np.ndarray

    def copy(self) -> "Population":
        return Population(
            self.occupied.copy(), self.health.copy(), self.energy.copy(),
            self.support.copy(), self.link_gene.copy(), self.links.copy(),
            self.recv_u.copy(), self.recv_v.copy(),
        )


@dataclass
class RunResult:
    population: Population
    abundance: np.ndarray
    mean_support: np.ndarray
    linked_support: np.ndarray
    link_density: np.ndarray
    max_capacity_ratio: float
    min_energy: float
    links_formed: int
    links_broken: int
    births: int
    deaths: int
    assessment_paid: float


@dataclass
class AssayResult:
    survivors: float
    mean_health: float
    recovery_time: float
    max_capacity_ratio: float
    integrated_viability: float


def lattice(side: int = SIDE) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return von-Neumann neighbors and each undirected torus edge once."""
    n = side * side
    neighbors = np.empty((n, 4), dtype=int)
    edge_u: list[int] = []
    edge_v: list[int] = []
    for row in range(side):
        for col in range(side):
            i = row * side + col
            up = ((row - 1) % side) * side + col
            down = ((row + 1) % side) * side + col
            left = row * side + (col - 1) % side
            right = row * side + (col + 1) % side
            neighbors[i] = (up, down, left, right)
            edge_u.extend((i, i))
            edge_v.extend((right, down))
    return neighbors, np.asarray(edge_u), np.asarray(edge_v)


def incidence(edge_u: np.ndarray, edge_v: np.ndarray, n: int) -> list[list[tuple[int, int, bool]]]:
    """For each node: (neighbour, edge index, node_is_u) triples."""
    table: list[list[tuple[int, int, bool]]] = [[] for _ in range(n)]
    for e, (u, v) in enumerate(zip(edge_u, edge_v)):
        table[int(u)].append((int(v), e, True))
        table[int(v)].append((int(u), e, False))
    return table


def make_environment(seed: int, steps: int = STEPS, side: int = SIDE) -> Environment:
    """Counter-based arrays keep treatment environments paired by site/time."""
    rng = np.random.default_rng(seed + 10_000)
    n = side * side
    _, edge_u, _ = lattice(side)
    e = len(edge_u)
    resource = RESOURCE_MEAN * rng.lognormal(0.0, 0.18, size=(steps, n))
    return Environment(
        resource=resource,
        local_hit=rng.random((steps, n)) < 0.038,
        local_magnitude=rng.uniform(0.26, 0.52, size=(steps, n)),
        global_hit=rng.random(steps) < 0.028,
        global_magnitude=rng.uniform(0.18, 0.34, size=steps),
        background_death=rng.random((steps, n)),
        birth_gate=rng.random((steps, n)),
        birth_choice=rng.integers(0, 4, size=(steps, n)),
        birth_priority=rng.random((steps, n)),
        mutation_support=rng.normal(0.0, MUTATION_SIGMA, size=(steps, n)),
        mutation_link=rng.normal(0.0, MUTATION_SIGMA, size=(steps, n)),
        link_form=rng.random((steps, e)),
        link_break=rng.random((steps, e)),
    )


def initialize(seed: int, side: int = SIDE) -> Population:
    """Identical to v1.11 initialization, plus zeroed reciprocity memory."""
    rng = np.random.default_rng(seed)
    n = side * side
    _, edge_u, edge_v = lattice(side)
    occupied = rng.random(n) < 0.72
    if occupied.sum() < n // 2:
        occupied[np.argsort(rng.random(n))[: n // 2]] = True
    health = np.where(occupied, rng.uniform(0.82, 1.0, n), 0.0)
    energy = np.where(occupied, rng.uniform(0.42, 0.88, n), 0.0)
    support = np.where(occupied, rng.uniform(0.0, 1.0, n), 0.0)
    link_gene = np.where(occupied, rng.uniform(0.0, 1.0, n), 0.0)
    probability = 0.22 * np.sqrt(link_gene[edge_u] * link_gene[edge_v])
    links = occupied[edge_u] & occupied[edge_v] & (rng.random(len(edge_u)) < probability)
    e = len(edge_u)
    return Population(
        occupied, health, energy, support, link_gene, links,
        np.zeros(e), np.zeros(e),
    )


def seed_invasion(seed: int, cheater_fraction: float = 0.05,
                  side: int = SIDE) -> Population:
    """Cooperator population with a small support~0 mutant cohort (P3)."""
    pop = initialize(seed, side)
    rng = np.random.default_rng(seed + 90_000)
    alive = np.flatnonzero(pop.occupied)
    pop.support[alive] = rng.uniform(0.80, 1.0, len(alive))
    pop.link_gene[alive] = rng.uniform(0.50, 0.90, len(alive))
    n_cheat = max(1, int(round(cheater_fraction * len(alive))))
    cheaters = rng.choice(alive, size=n_cheat, replace=False)
    pop.support[cheaters] = rng.uniform(0.0, 0.02, n_cheat)
    return pop


def _linked_degree(pop: Population, edge_u: np.ndarray,
                   edge_v: np.ndarray) -> np.ndarray:
    degree = np.zeros(len(pop.occupied), dtype=int)
    np.add.at(degree, edge_u[pop.links], 1)
    np.add.at(degree, edge_v[pop.links], 1)
    return degree


def _summary(pop: Population, edge_u: np.ndarray,
             edge_v: np.ndarray) -> tuple[float, float, float, float]:
    count = int(pop.occupied.sum())
    if count == 0:
        return 0.0, 0.0, 0.0, 0.0
    degree = _linked_degree(pop, edge_u, edge_v)
    linked = pop.occupied & (degree > 0)
    mean_support = float(pop.support[pop.occupied].mean())
    linked_support = float(pop.support[linked].mean()) if linked.any() else 0.0
    possible = max(1, int(np.sum(pop.occupied[edge_u] & pop.occupied[edge_v])))
    density = float(pop.links.sum() / possible)
    return float(count), mean_support, linked_support, density


def _route_support(pop: Population, spare: np.ndarray, edge_u: np.ndarray,
                   edge_v: np.ndarray, enabled: bool, mechanism: str,
                   incident: list[list[tuple[int, int, bool]]]) -> tuple[float, float]:
    """Route paid, lossy support and return draw plus capacity ratio.

    Identical to v1.11 except that reciprocity scales the per-neighbour offer
    by decaying memory of what that neighbour returned. Every arm keeps the
    same capacity bound: a donor may spend only repair budget left unused
    after its own repair, and never more energy than it holds.
    """
    if not enabled or not pop.links.any():
        return 0.0, 0.0

    total_draw = 0.0
    max_ratio = 0.0
    order = np.flatnonzero(pop.occupied)
    for donor in order:
        capacity = float(spare[donor])
        willing = min(capacity * float(pop.support[donor]), float(pop.energy[donor]))
        if willing <= EPS:
            continue
        entries = [
            (nb, e, is_u) for (nb, e, is_u) in incident[donor]
            if pop.links[e] and pop.occupied[nb]
        ]
        if not entries:
            continue
        targets = np.array([nb for (nb, _, _) in entries], dtype=int)
        need = np.maximum(0.0, 1.0 - pop.health[targets])

        if mechanism == "reciprocity":
            # What this donor received from each neighbour, saturating.
            memory = np.array([
                pop.recv_u[e] if is_u else pop.recv_v[e]
                for (_, e, is_u) in entries
            ])
            trust = np.clip(MEMORY_GAIN * memory, 0.0, 1.0)
            # A donor still opens with a baseline offer, otherwise no first
            # move is possible and reciprocity can never bootstrap.
            weight = 0.25 + 0.75 * trust
            need = need * weight

        keep = need > EPS
        if not keep.any():
            continue
        entries = [entries[i] for i in np.flatnonzero(keep)]
        targets = targets[keep]
        need = need[keep]

        draw = min(willing, float(need.sum()) / TRANSFER_ETA)
        delivered = TRANSFER_ETA * draw
        weights = need / need.sum()
        given = np.minimum(need, delivered * weights)
        pop.health[targets] += given
        pop.energy[donor] -= draw
        total_draw += draw
        # Record the gift in the recipient's directional memory slot.
        for (_, e, is_u), amount in zip(entries, given):
            if is_u:
                pop.recv_v[e] += float(amount)
            else:
                pop.recv_u[e] += float(amount)
        if capacity > EPS:
            max_ratio = max(max_ratio, draw / capacity)
    return total_draw, max_ratio


def _clear_dead_links(pop: Population, edge_u: np.ndarray,
                      edge_v: np.ndarray) -> int:
    invalid = pop.links & (~pop.occupied[edge_u] | ~pop.occupied[edge_v])
    count = int(invalid.sum())
    pop.links[invalid] = False
    pop.recv_u[invalid] = 0.0
    pop.recv_v[invalid] = 0.0
    return count


def population_step(pop: Population, env: Environment, t: int, regime: str,
                    transfer_enabled: bool, neighbors: np.ndarray,
                    edge_u: np.ndarray, edge_v: np.ndarray,
                    incident: list[list[tuple[int, int, bool]]],
                    mechanism: str = "blind",
                    assess_cost: float = ASSESS_COST,
                    reproduce: bool = True,
                    evolve_links: bool = True) -> dict[str, float]:
    """Advance one paid demographic step under the given partner mechanism."""
    pop.energy[pop.occupied] = np.minimum(
        ENERGY_CAP, pop.energy[pop.occupied] + env.resource[t, pop.occupied],
    )

    degree = _linked_degree(pop, edge_u, edge_v)
    # Informed mechanisms pay for partner information, per assessed edge.
    per_edge = assess_cost if mechanism in INFORMED else 0.0
    required = METABOLISM + (LINK_COST + per_edge) * degree
    paid = np.minimum(pop.energy, required) * pop.occupied
    shortfall = (required - paid) * pop.occupied
    pop.energy -= paid
    pop.health -= shortfall
    assessment_paid = float(per_edge * degree[pop.occupied].sum())

    if regime == "independent":
        damage = env.local_hit[t] * env.local_magnitude[t]
    elif regime == "correlated":
        damage = np.full(len(pop.occupied), env.global_hit[t] * env.global_magnitude[t])
    elif regime == "none":
        damage = np.zeros(len(pop.occupied))
    else:
        raise ValueError(f"unknown regime: {regime}")
    pop.health[pop.occupied] -= damage[pop.occupied]

    need = np.maximum(0.0, 1.0 - pop.health)
    self_draw = np.minimum(np.minimum(need, REPAIR_BUDGET), pop.energy) * pop.occupied
    pop.health += self_draw
    pop.energy -= self_draw
    spare = np.where(pop.occupied, REPAIR_BUDGET - self_draw, 0.0)

    pop.recv_u *= MEMORY_DECAY
    pop.recv_v *= MEMORY_DECAY
    _, transfer_ratio = _route_support(
        pop, spare, edge_u, edge_v, transfer_enabled, mechanism, incident
    )

    pop.health = np.minimum(pop.health, 1.0)
    dead = pop.occupied & (
        (pop.health <= DEATH_CUTOFF) | (env.background_death[t] < BACKGROUND_DEATH)
    )
    deaths = int(dead.sum())
    pop.occupied[dead] = False
    pop.health[dead] = 0.0
    pop.energy[dead] = 0.0
    pop.support[dead] = 0.0
    pop.link_gene[dead] = 0.0
    broken = _clear_dead_links(pop, edge_u, edge_v)

    births = 0
    if reproduce and pop.occupied.any() and (~pop.occupied).any():
        eligible = np.flatnonzero(
            pop.occupied
            & (pop.energy >= BIRTH_THRESHOLD)
            & (pop.health >= 0.78)
            & (env.birth_gate[t] < BIRTH_RATE)
        )
        eligible = eligible[np.argsort(env.birth_priority[t, eligible])]
        for parent in eligible:
            if not pop.occupied[parent] or pop.energy[parent] < BIRTH_THRESHOLD:
                continue
            target = int(neighbors[parent, env.birth_choice[t, parent]])
            if pop.occupied[target]:
                continue
            pop.energy[parent] -= BIRTH_COST
            pop.occupied[target] = True
            pop.health[target] = CHILD_HEALTH
            pop.energy[target] = CHILD_ENERGY
            pop.support[target] = np.clip(
                pop.support[parent] + env.mutation_support[t, target], 0.0, 1.0
            )
            pop.link_gene[target] = np.clip(
                pop.link_gene[parent] + env.mutation_link[t, target], 0.0, 1.0
            )
            births += 1

    formed = 0
    if evolve_links:
        valid = pop.occupied[edge_u] & pop.occupied[edge_v]
        break_extra = np.zeros(len(edge_u))
        if mechanism == "partner_choice":
            # A link to a low contributor is dropped faster. Both endpoints
            # judge, so the weaker contributor sets the risk.
            weakest = np.minimum(pop.support[edge_u], pop.support[edge_v])
            break_extra = CHOICE_STRENGTH * (1.0 - weakest)
        break_now = pop.links & (
            (~valid) | (env.link_break[t] < LINK_BREAK_RATE + break_extra)
        )
        broken += int(break_now.sum())
        pop.links[break_now] = False
        pop.recv_u[break_now] = 0.0
        pop.recv_v[break_now] = 0.0

        propensity = np.sqrt(pop.link_gene[edge_u] * pop.link_gene[edge_v])
        if mechanism == "partner_choice":
            # Both endpoints prefer contributors.
            propensity = propensity * np.sqrt(
                pop.support[edge_u] * pop.support[edge_v]
            )
        elif mechanism == "assortment":
            # Similarity, not level: a greenbeard tag rather than a rating.
            propensity = propensity * (
                1.0 - np.abs(pop.support[edge_u] - pop.support[edge_v])
            )
        form_now = (
            (~pop.links) & valid & (env.link_form[t] < LINK_FORM_RATE * propensity)
        )
        pop.links[form_now] = True
        pop.recv_u[form_now] = 0.0
        pop.recv_v[form_now] = 0.0
        formed = int(form_now.sum())

    assert np.all(pop.energy >= -1e-10)
    pop.energy = np.maximum(pop.energy, 0.0)
    assert transfer_ratio <= 1.0 + 1e-10
    return {
        "births": float(births),
        "deaths": float(deaths),
        "formed": float(formed),
        "broken": float(broken),
        "capacity_ratio": float(transfer_ratio),
        "min_energy": float(pop.energy.min()),
        "assessment_paid": assessment_paid,
    }


def run_population(seed: int, mechanism: str = "blind",
                   regime: str = "independent", transfer_enabled: bool = True,
                   steps: int = STEPS, initial: Population | None = None,
                   assess_cost: float = ASSESS_COST) -> RunResult:
    neighbors, edge_u, edge_v = lattice()
    incident = incidence(edge_u, edge_v, len(neighbors))
    env = make_environment(seed, steps=steps)
    pop = initialize(seed) if initial is None else initial.copy()
    abundance = np.zeros(steps)
    mean_support = np.zeros(steps)
    linked_support = np.zeros(steps)
    link_density = np.zeros(steps)
    max_ratio = 0.0
    min_energy = float("inf")
    formed = broken = births = deaths = 0
    assessment = 0.0

    for t in range(steps):
        audit = population_step(
            pop, env, t, regime, transfer_enabled, neighbors, edge_u, edge_v,
            incident, mechanism=mechanism, assess_cost=assess_cost,
        )
        abundance[t], mean_support[t], linked_support[t], link_density[t] = _summary(
            pop, edge_u, edge_v
        )
        max_ratio = max(max_ratio, audit["capacity_ratio"])
        min_energy = min(min_energy, audit["min_energy"])
        formed += int(audit["formed"])
        broken += int(audit["broken"])
        births += int(audit["births"])
        deaths += int(audit["deaths"])
        assessment += audit["assessment_paid"]

    return RunResult(
        pop, abundance, mean_support, linked_support, link_density,
        max_ratio, min_energy, formed, broken, births, deaths, assessment,
    )


def pulse_assay(evolved: Population, seed: int, regime: str,
                transfer_enabled: bool, mechanism: str,
                steps: int = ASSAY_STEPS) -> AssayResult:
    """Paired post-evolution assay with demography and link changes frozen."""
    pop = evolved.copy()
    neighbors, edge_u, edge_v = lattice()
    incident = incidence(edge_u, edge_v, len(neighbors))
    env = make_environment(seed + 50_000, steps=steps)
    rng = np.random.default_rng(seed + 80_000)
    alive = np.flatnonzero(pop.occupied)
    if len(alive) == 0:
        return AssayResult(0.0, 0.0, float(steps + 1), 0.0, 0.0)
    if regime == "independent":
        targets = rng.choice(alive, size=max(1, len(alive) // 8), replace=False)
        pop.health[targets] -= 0.98
    elif regime == "correlated":
        pop.health[alive] -= 0.28
    else:
        raise ValueError(f"unknown regime: {regime}")
    pop.health = np.maximum(pop.health, 0.0)

    initial_count = max(1, int(pop.occupied.sum()))
    recovery = float(steps + 1)
    max_ratio = 0.0
    viability_sum = 0.0
    for t in range(steps):
        audit = population_step(
            pop, env, t, regime="none", transfer_enabled=transfer_enabled,
            neighbors=neighbors, edge_u=edge_u, edge_v=edge_v,
            incident=incident, mechanism=mechanism,
            reproduce=False, evolve_links=False,
        )
        max_ratio = max(max_ratio, audit["capacity_ratio"])
        viability_sum += float(pop.health[pop.occupied].sum() / initial_count)
        if recovery > steps and pop.occupied.any():
            if float(pop.health[pop.occupied].mean()) >= 0.94:
                recovery = float(t + 1)
    survivors = float(pop.occupied.sum() / initial_count)
    health = float(pop.health[pop.occupied].mean()) if pop.occupied.any() else 0.0
    return AssayResult(survivors, health, recovery, max_ratio, viability_sum / steps)


def one_seed(seed: int, mechanism: str,
             assess_cost: float = ASSESS_COST) -> dict[str, float]:
    initial = initialize(seed)
    edge_u, edge_v = lattice()[1:]
    initial_linked = initial.occupied & (
        _linked_degree(initial, edge_u, edge_v) > 0
    )
    initial_linked_support = (
        float(initial.support[initial_linked].mean())
        if initial_linked.any() else 0.0
    )
    enabled = run_population(seed, mechanism, "independent", True,
                             initial=initial, assess_cost=assess_cost)
    disabled = run_population(seed, mechanism, "independent", False,
                              initial=initial, assess_cost=assess_cost)
    sparse_on = pulse_assay(enabled.population, seed, "independent", True, mechanism)
    sparse_off = pulse_assay(enabled.population, seed, "independent", False, mechanism)
    common_on = pulse_assay(enabled.population, seed, "correlated", True, mechanism)
    common_off = pulse_assay(enabled.population, seed, "correlated", False, mechanism)

    linked = enabled.population.occupied & (
        _linked_degree(enabled.population, edge_u, edge_v) > 0
    )
    if linked.any():
        low_support = float(np.mean(enabled.population.support[linked] < 0.20))
        cheaters = float(np.mean(
            (enabled.population.support[linked] < 0.20)
            & (enabled.population.link_gene[linked] > 0.50)
        ))
    else:
        low_support = 0.0
        cheaters = 0.0

    tail = slice(-100, None)
    return {
        "abundance_on": float(np.median(enabled.abundance[tail])),
        "abundance_off": float(np.median(disabled.abundance[tail])),
        "linked_support_on": float(np.median(enabled.linked_support[tail])),
        "linked_support_off": float(np.median(disabled.linked_support[tail])),
        "link_density_on": float(np.median(enabled.link_density[tail])),
        "selection_delta": float(
            np.median(enabled.linked_support[tail])
            - np.median(disabled.linked_support[tail])
        ),
        # Post-hoc diagnostic, not part of the preregistered criterion:
        # the v1.11 comparison against the starting level. Under a rule that
        # also rewards support when transfer is off, the matched control
        # rises too, so the on-off delta understates absolute retention.
        "drift_from_initial": float(
            np.median(enabled.linked_support[tail]) - initial_linked_support
        ),
        "sparse_survivor_gain": sparse_on.survivors - sparse_off.survivors,
        "sparse_viability_gain": (
            sparse_on.integrated_viability - sparse_off.integrated_viability
        ),
        "sparse_recovery_gain": sparse_off.recovery_time - sparse_on.recovery_time,
        "common_survivor_gain": common_on.survivors - common_off.survivors,
        "common_viability_gain": (
            common_on.integrated_viability - common_off.integrated_viability
        ),
        "max_capacity_ratio": max(
            enabled.max_capacity_ratio, sparse_on.max_capacity_ratio
        ),
        "min_energy": enabled.min_energy,
        "low_support_fraction": low_support,
        "cheater_fraction": cheaters,
        "assessment_paid": enabled.assessment_paid,
        "links_formed": float(enabled.links_formed),
        "links_broken": float(enabled.links_broken),
    }


def invasion_test(seed: int, mechanism: str) -> dict[str, float]:
    """P3: can 5% support~0 mutants sweep a cooperator population?"""
    initial = seed_invasion(seed)
    edge_u, edge_v = lattice()[1:]
    start = float(np.mean(initial.support[initial.occupied] < 0.20))
    result = run_population(seed, mechanism, "independent", True, initial=initial)
    pop = result.population
    if not pop.occupied.any():
        return {"start": start, "end": float("nan"), "extinct": 1.0}
    end = float(np.mean(pop.support[pop.occupied] < 0.20))
    linked = pop.occupied & (_linked_degree(pop, edge_u, edge_v) > 0)
    end_linked = float(np.mean(pop.support[linked] < 0.20)) if linked.any() else 0.0
    return {
        "start": start, "end": end, "end_linked": end_linked,
        "mean_support": float(pop.support[pop.occupied].mean()), "extinct": 0.0,
    }


def run_experiment(seeds: int = 16) -> dict:
    arms: dict[str, dict] = {}
    for mechanism in MECHANISMS:
        rows = [one_seed(s, mechanism) for s in range(seeds)]
        agg = {k: float(np.median([r[k] for r in rows])) for k in rows[0]}
        agg["positive_selection_seeds"] = float(
            np.mean([r["selection_delta"] >= 0.0 for r in rows])
        )
        agg["max_capacity_ratio"] = float(max(r["max_capacity_ratio"] for r in rows))
        agg["min_energy"] = float(min(r["min_energy"] for r in rows))
        arms[mechanism] = agg

    invasion = {
        m: {k: float(np.median([invasion_test(s, m)[k] for s in range(seeds // 2)]))
            for k in ("start", "end", "end_linked", "mean_support")}
        for m in MECHANISMS
    }

    # P4: does a higher information price remove any advantage?
    costs = (0.0, ASSESS_COST, 0.004, 0.010)
    sweep: dict[str, list[float]] = {}
    for mechanism in INFORMED:
        deltas = []
        for cost in costs:
            rows = [one_seed(s, mechanism, assess_cost=cost) for s in range(seeds // 2)]
            deltas.append(float(np.median([r["selection_delta"] for r in rows])))
        sweep[mechanism] = deltas

    return {"seeds": seeds, "arms": arms, "invasion": invasion,
            "costs": list(costs), "sweep": sweep}


def report(res: dict) -> None:
    print()
    print("BENCHMARK v1.12 — partner rules and the retention of costly support")
    print(f"seeds {res['seeds']}, steps {STEPS}, sites {SIDE * SIDE}")
    print()
    print("  P2 SELECTION (median over seeds; positive = support retained)")
    print(f"  {'mechanism':<16}{'linked on':>11}{'linked off':>12}"
          f"{'delta':>10}{'pos seeds':>11}{'abundance':>11}")
    for m in MECHANISMS:
        a = res["arms"][m]
        print(f"  {m:<16}{a['linked_support_on']:>11.3f}"
              f"{a['linked_support_off']:>12.3f}{a['selection_delta']:>+10.4f}"
              f"{a['positive_selection_seeds']:>10.0%}{a['abundance_on']:>11.1f}")
    print()
    print("  post-hoc diagnostic (NOT part of the criterion): drift from the")
    print("  starting level, the v1.11 comparison. Where a rule rewards support")
    print("  even with transfer off, the matched control rises too.")
    for m in MECHANISMS:
        print(f"  {m:<16}{res['arms'][m]['drift_from_initial']:>+11.4f}")
    print()
    print("  P1 ACCOUNTING")
    worst_ratio = max(res["arms"][m]["max_capacity_ratio"] for m in MECHANISMS)
    worst_energy = min(res["arms"][m]["min_energy"] for m in MECHANISMS)
    print(f"  max transfer draw / unused capacity : {worst_ratio:.6f}")
    print(f"  min stored energy                   : {worst_energy:.6f}")
    for m in INFORMED:
        print(f"  assessment paid ({m:<14}): {res['arms'][m]['assessment_paid']:.1f}")
    print()
    print("  P3 INVASION (5% support<0.20 mutants seeded into cooperators)")
    print(f"  {'mechanism':<16}{'start':>9}{'end':>9}{'end linked':>13}{'mean sup':>11}")
    for m in MECHANISMS:
        v = res["invasion"][m]
        print(f"  {m:<16}{v['start']:>9.1%}{v['end']:>9.1%}"
              f"{v['end_linked']:>13.1%}{v['mean_support']:>11.3f}")
    print()
    print("  P4 COST BOUNDARY (median selection delta by assessment cost)")
    header = "".join(f"{c:>11.4f}" for c in res["costs"])
    print(f"  {'mechanism':<16}{header}")
    for m in INFORMED:
        row = "".join(f"{d:>+11.4f}" for d in res["sweep"][m])
        print(f"  {m:<16}{row}")
    print()
    print("  P5 COMMON MODE (paired assay gains)")
    print(f"  {'mechanism':<16}{'sparse viab':>13}{'common viab':>13}"
          f"{'sparse surv':>13}{'cheaters':>10}")
    for m in MECHANISMS:
        a = res["arms"][m]
        print(f"  {m:<16}{a['sparse_viability_gain']:>+13.4f}"
              f"{a['common_viability_gain']:>+13.4f}"
              f"{a['sparse_survivor_gain']:>+13.4f}"
              f"{a['cheater_fraction']:>10.1%}")
    print()
    verdict(res)


def verdict(res: dict) -> None:
    winners = [
        m for m in INFORMED
        if res["arms"][m]["positive_selection_seeds"] > 0.5
        and res["arms"][m]["selection_delta"] > 0.0
    ]
    print("  preregistered candidate criterion:", end=" ")
    if not winners:
        print("NOT SUPPORTED")
        print("  No partner rule reversed the sign of support selection.")
        print("  Visibility of contribution is not by itself sufficient;")
        print("  the missing ingredient lies elsewhere.")
    else:
        bounded = [
            m for m in winners
            if res["invasion"][m]["end"] < 0.5
            and min(res["sweep"][m]) < 0.0
        ]
        if bounded:
            print("SUPPORTED for " + ", ".join(bounded))
            print("  Retention, bounded invasion, and a real cost boundary all hold.")
            print("  This is a toy population mechanism, not metabolism, life,")
            print("  identity, or consciousness.")
        else:
            print("PARTIAL for " + ", ".join(winners))
            print("  Retention holds but invasion or the cost boundary does not.")


def plot(res: dict, path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.0))
    labels = [m.replace("_", "\n") for m in MECHANISMS]

    deltas = [res["arms"][m]["selection_delta"] for m in MECHANISMS]
    colors = ["#c44e52" if d < 0 else "#55a868" for d in deltas]
    axes[0].bar(labels, deltas, color=colors)
    axes[0].axhline(0, color="black", linewidth=1)
    axes[0].set(title="(a) Support selection\n(positive = contribution retained)",
                ylabel="linked support: transfer on − off")

    starts = [res["invasion"][m]["start"] for m in MECHANISMS]
    ends = [res["invasion"][m]["end"] for m in MECHANISMS]
    x = np.arange(len(MECHANISMS))
    axes[1].bar(x - 0.2, starts, width=0.4, label="seeded", color="#8172b2")
    axes[1].bar(x + 0.2, ends, width=0.4, label="final", color="#c44e52")
    axes[1].axhline(0.5, color="black", linestyle=":", linewidth=1)
    axes[1].set_xticks(x, labels)
    axes[1].set(title="(b) Cheater invasion", ylabel="fraction support < 0.20")
    axes[1].legend(fontsize=8)

    for m in INFORMED:
        axes[2].plot(res["costs"], res["sweep"][m], marker="o", label=m)
    axes[2].axhline(0, color="black", linewidth=1)
    axes[2].set(title="(c) Price of partner information",
                xlabel="assessment cost per edge per step",
                ylabel="selection delta")
    axes[2].legend(fontsize=8)
    for ax in axes:
        ax.grid(alpha=0.3)

    fig.suptitle("v1.12 — partner rules and the retention of costly support")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=170)
    print(f"saved {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=16)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    if args.seeds < 2:
        parser.error("--seeds must be >= 2")
    res = run_experiment(args.seeds)
    report(res)
    if args.save:
        path = Path(__file__).resolve().parents[2] / "tools" / "inverse_benchmark_selection.png"
        plot(res, path)


if __name__ == "__main__":
    main()
