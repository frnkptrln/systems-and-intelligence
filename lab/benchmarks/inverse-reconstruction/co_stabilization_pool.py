#!/usr/bin/env python3
"""
co_stabilization_pool.py

Benchmark v1.13 — does relocating the cost off the contributor retain it?

QUESTION
v1.11 found costly support acutely useful and selected downward in all 16
seeds. v1.12 found that making contribution visible sorts the network but
still does not retain the trait. Log 019 named the next discriminating arm:
the cost in both prior versions falls entirely on the individual donor
(`support_i x spare_i`). If who-pays is the problem, moving the cost to the
local group should retain support. If it is still selected down, the problem
is not who pays but that the selection level cannot see the benefit at all.

TWO ARMS, ONE ACCOUNTING
  donor   v1.11 unchanged. A node pays for the support it sends, from its own
          energy, bounded by its unused repair capacity.
  pool    The local group (a connected component of the link graph) funds
          support at a rate set by the group's MEAN support gene. Every member
          pays that same rate on its own spare capacity, regardless of its own
          gene, and damaged members draw by need. An individual's cost is thus
          decoupled from its own generosity and depends on its neighbours'.
          This is "charge the veto to the institution, not the reviewer"
          (Log 019) made mechanical.

The two arms differ in the routing rule, not in a parameter: that relocation
IS the independent variable. Everything else -- resources, shocks, links,
reproduction, mutation, death, transfer loss, the audit -- is identical, and
the donor arm reproduces v1.11 trajectory-for-trajectory, which a test
asserts.

PREREGISTERED PREDICTIONS (fixed before the first full run)
  P1 ACCOUNTING: energy never negative; no member's levy exceeds its unused
     repair capacity; the donor arm reproduces v1.11 exactly.
  P2 RETENTION: if cost relocation is the missing ingredient, the pool arm
     retains group support in a majority of 16 seeds where the donor arm does
     not. Donor baseline to beat: median delta -0.1056, 0% positive seeds.
  P3 INVASION: this is the honest risk. Pooling lets a support~0 mutant pay
     the group-mean rate while contributing almost nothing to that mean, so
     free-riding may become EASIER, not harder. Prediction: the pool arm
     bounds invasion no better than donor, and possibly worse.
  P4 DILUTION: the pool effect, whatever its sign, should scale with how much
     the cost is diluted -- larger groups spread each contributor's cost over
     more members. Retention is reported against mean group size.
  P5 COMMON MODE: the paired benefit is smaller under correlated damage, as in
     v1.10-v1.12: a pool has no healthy contributors when all are damaged.

CANDIDATE CRITERION
Cost relocation receives a bounded positive result only if P1 holds and P2
holds in >50% of seeds. Either outcome is reported plainly. A failure here is
the more consequential result: it would locate the obstruction below the
accounting, in the selection level itself, and the repository's constraint
vocabulary (Log 019) would need a remedy that no budgeting change supplies.
Nothing here establishes metabolism, life, group selection as a general
force, identity, or consciousness.

RESULT (first full run; 16 seeds, 600 steps, 144 sites)
  P1 CONFIRMED: maximum levy / unused repair capacity = 1.000000; minimum
     stored energy = 0.000000. The donor arm reproduces v1.11
     trajectory-for-trajectory (abundance, linked support, link density, link
     counts), so the arms differ only in who bears the cost.
  P2 NOT SUPPORTED, but the loss nearly vanishes. Pool -0.0075 with 44% of
     seeds positive, against donor -0.1056 with 0%. Measured against the
     starting level the pool arm barely decays (-0.0143 versus -0.1277).
     Relocation removes almost all of the selection pressure against support
     without turning it into positive selection: 44% is not a majority, and
     the criterion is not met.
  P3 FALSIFIED IN THE OPPOSITE DIRECTION. The prediction was that pooling
     makes free-riding EASIER, because a mutant could pay the group rate
     while contributing nothing to it. The reverse happened: seeded with
     4.9% cheaters, the donor arm ends at 21.6% while the pool arm ends at
     2.6% -- BELOW its seeded level -- with mean support 0.874 versus 0.713.
     The reason is the same mechanism read the other way: because the levy
     tracks the group mean, a low-support mutant inside a cooperative group
     cannot avoid paying, so defection buys it nothing. Cost relocation does
     not merely dilute the penalty for contributing; it removes the reward
     for defecting.
  P4 DILUTION: the pool arm sustains smaller groups (mean 4.4 versus 7.7)
     and a smaller population (77.8 versus 104.5). Relocation is not free --
     the group pays in size for what it buys in retention.
  P5 CONFIRMED: the pool's paired gain is larger under sparse damage
     (+0.0264) than under correlated damage (+0.0080), and the low-support
     fraction among linked agents halves (20.2% versus 40.4%).

The preregistered candidate criterion is NOT SUPPORTED, and the arm is still
the most informative of the four co-stabilization versions. Moving the cost
from the contributor to the group nearly eliminates selection against costly
support and reverses invasion outcomes, while costing population size. Two
questions the model cannot settle: whether 44% would cross a majority under a
longer horizon or weaker mutation, and whether the retention seen here is
selection or merely the absence of selection -- with the levy set by the group
mean, within-group variation in the gene is nearly cost-neutral, so drift
rather than advantage may be carrying it. Distinguishing those two is the next
discriminating measurement, not a larger version of this one.

Usage:
    python co_stabilization_pool.py
    python co_stabilization_pool.py --save
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

ARMS = ("donor", "pool")
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

    def copy(self) -> "Population":
        return Population(
            self.occupied.copy(), self.health.copy(), self.energy.copy(),
            self.support.copy(), self.link_gene.copy(), self.links.copy(),
        )


@dataclass
class RunResult:
    population: Population
    abundance: np.ndarray
    mean_support: np.ndarray
    linked_support: np.ndarray
    link_density: np.ndarray
    mean_group_size: float
    max_capacity_ratio: float
    min_energy: float
    links_formed: int
    links_broken: int
    births: int
    deaths: int


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
    """Identical to v1.11 initialization."""
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
    return Population(occupied, health, energy, support, link_gene, links)


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


def _components(pop: Population, edge_u: np.ndarray,
                edge_v: np.ndarray) -> list[np.ndarray]:
    """Connected components of the active link graph over occupied nodes."""
    n = len(pop.occupied)
    parent = np.arange(n)

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for u, v in zip(edge_u[pop.links], edge_v[pop.links]):
        ru, rv = find(int(u)), find(int(v))
        if ru != rv:
            parent[ru] = rv
    groups: dict[int, list[int]] = {}
    for i in np.flatnonzero(pop.occupied):
        r = find(int(i))
        groups.setdefault(r, []).append(int(i))
    return [np.asarray(g) for g in groups.values() if len(g) >= 2]


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


def _route_donor(pop: Population, spare: np.ndarray, edge_u: np.ndarray,
                 edge_v: np.ndarray) -> tuple[float, float]:
    """v1.11 routing: each donor pays for what it sends to linked neighbours.

    The adjacency is rebuilt from the ACTIVE links each step, not from the
    lattice: a node may only send along links that currently exist.
    """
    if not pop.links.any():
        return 0.0, 0.0
    incident: list[list[int]] = [[] for _ in range(len(pop.occupied))]
    for u, v in zip(edge_u[pop.links], edge_v[pop.links]):
        incident[int(u)].append(int(v))
        incident[int(v)].append(int(u))

    total_draw = 0.0
    max_ratio = 0.0
    for donor in np.flatnonzero(pop.occupied):
        capacity = float(spare[donor])
        willing = min(capacity * float(pop.support[donor]), float(pop.energy[donor]))
        if willing <= EPS or not incident[donor]:
            continue
        targets = np.asarray(incident[donor], dtype=int)
        targets = targets[pop.occupied[targets]]
        need = np.maximum(0.0, 1.0 - pop.health[targets])
        targets = targets[need > EPS]
        need = need[need > EPS]
        if len(targets) == 0:
            continue
        draw = min(willing, float(need.sum()) / TRANSFER_ETA)
        delivered = TRANSFER_ETA * draw
        weights = need / need.sum()
        pop.health[targets] += np.minimum(need, delivered * weights)
        pop.energy[donor] -= draw
        total_draw += draw
        if capacity > EPS:
            max_ratio = max(max_ratio, draw / capacity)
    return total_draw, max_ratio


def _route_pool(pop: Population, spare: np.ndarray, edge_u: np.ndarray,
                edge_v: np.ndarray) -> tuple[float, float]:
    """Group-funded routing: every member of a component pays the group's mean
    support rate on its own spare capacity; damaged members draw by need. Cost
    tracks the group's generosity, not the individual's."""
    total_draw = 0.0
    max_ratio = 0.0
    for group in _components(pop, edge_u, edge_v):
        rate = float(pop.support[group].mean())
        if rate <= EPS:
            continue
        # Each member's maximum levy: the group rate on its unused capacity,
        # never more energy than it holds.
        levy_cap = np.minimum(rate * spare[group], pop.energy[group])
        levy_cap = np.maximum(levy_cap, 0.0)
        pool_capacity = float(levy_cap.sum())
        need = np.maximum(0.0, 1.0 - pop.health[group])
        if pool_capacity <= EPS or need.sum() <= EPS:
            continue
        # Collect only what the group's damage can absorb (after loss).
        draw_total = min(pool_capacity, float(need.sum()) / TRANSFER_ETA)
        scale = draw_total / pool_capacity
        actual_levy = levy_cap * scale
        pop.energy[group] -= actual_levy
        delivered = TRANSFER_ETA * draw_total
        weights = need / need.sum()
        pop.health[group] += np.minimum(need, delivered * weights)
        total_draw += draw_total
        ratios = np.divide(actual_levy, spare[group],
                           out=np.zeros_like(actual_levy), where=spare[group] > EPS)
        max_ratio = max(max_ratio, float(ratios.max()) if len(ratios) else 0.0)
    return total_draw, max_ratio


def population_step(pop: Population, env: Environment, t: int, regime: str,
                    transfer_enabled: bool, arm: str, neighbors: np.ndarray,
                    edge_u: np.ndarray, edge_v: np.ndarray,
                    reproduce: bool = True,
                    evolve_links: bool = True) -> dict[str, float]:
    """Advance one paid demographic step under the donor or pool arm."""
    pop.energy[pop.occupied] = np.minimum(
        ENERGY_CAP, pop.energy[pop.occupied] + env.resource[t, pop.occupied],
    )

    degree = _linked_degree(pop, edge_u, edge_v)
    required = METABOLISM + LINK_COST * degree
    paid = np.minimum(pop.energy, required) * pop.occupied
    shortfall = (required - paid) * pop.occupied
    pop.energy -= paid
    pop.health -= shortfall

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

    if transfer_enabled:
        if arm == "donor":
            _, transfer_ratio = _route_donor(pop, spare, edge_u, edge_v)
        elif arm == "pool":
            _, transfer_ratio = _route_pool(pop, spare, edge_u, edge_v)
        else:
            raise ValueError(f"unknown arm: {arm}")
    else:
        transfer_ratio = 0.0

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
    invalid = pop.links & (~pop.occupied[edge_u] | ~pop.occupied[edge_v])
    broken = int(invalid.sum())
    pop.links[invalid] = False

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
        break_now = pop.links & ((~valid) | (env.link_break[t] < LINK_BREAK_RATE))
        broken += int(break_now.sum())
        pop.links[break_now] = False
        propensity = np.sqrt(pop.link_gene[edge_u] * pop.link_gene[edge_v])
        form_now = (~pop.links) & valid & (env.link_form[t] < LINK_FORM_RATE * propensity)
        pop.links[form_now] = True
        formed = int(form_now.sum())

    assert np.all(pop.energy >= -1e-10)
    pop.energy = np.maximum(pop.energy, 0.0)
    assert transfer_ratio <= 1.0 + 1e-10
    return {
        "births": float(births), "deaths": float(deaths),
        "formed": float(formed), "broken": float(broken),
        "capacity_ratio": float(transfer_ratio),
        "min_energy": float(pop.energy.min()),
    }


def run_population(seed: int, arm: str = "donor", regime: str = "independent",
                   transfer_enabled: bool = True, steps: int = STEPS,
                   initial: Population | None = None) -> RunResult:
    neighbors, edge_u, edge_v = lattice()
    env = make_environment(seed, steps=steps)
    pop = initialize(seed) if initial is None else initial.copy()
    abundance = np.zeros(steps)
    mean_support = np.zeros(steps)
    linked_support = np.zeros(steps)
    link_density = np.zeros(steps)
    group_sizes: list[float] = []
    max_ratio = 0.0
    min_energy = float("inf")
    formed = broken = births = deaths = 0

    for t in range(steps):
        audit = population_step(
            pop, env, t, regime, transfer_enabled, arm,
            neighbors, edge_u, edge_v,
        )
        abundance[t], mean_support[t], linked_support[t], link_density[t] = _summary(
            pop, edge_u, edge_v
        )
        if t >= steps - 100:
            groups = _components(pop, edge_u, edge_v)
            if groups:
                group_sizes.append(float(np.mean([len(g) for g in groups])))
        max_ratio = max(max_ratio, audit["capacity_ratio"])
        min_energy = min(min_energy, audit["min_energy"])
        formed += int(audit["formed"])
        broken += int(audit["broken"])
        births += int(audit["births"])
        deaths += int(audit["deaths"])

    return RunResult(
        pop, abundance, mean_support, linked_support, link_density,
        float(np.mean(group_sizes)) if group_sizes else 0.0,
        max_ratio, min_energy, formed, broken, births, deaths,
    )


def pulse_assay(evolved: Population, seed: int, regime: str,
                transfer_enabled: bool, arm: str,
                steps: int = ASSAY_STEPS) -> AssayResult:
    """Paired post-evolution assay with demography and link changes frozen."""
    pop = evolved.copy()
    neighbors, edge_u, edge_v = lattice()
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
            pop, env, t, regime="none", transfer_enabled=transfer_enabled, arm=arm,
            neighbors=neighbors, edge_u=edge_u, edge_v=edge_v,
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


def one_seed(seed: int, arm: str) -> dict[str, float]:
    initial = initialize(seed)
    edge_u, edge_v = lattice()[1:]
    ilinked = initial.occupied & (_linked_degree(initial, edge_u, edge_v) > 0)
    init_linked_support = float(initial.support[ilinked].mean()) if ilinked.any() else 0.0
    enabled = run_population(seed, arm, "independent", True, initial=initial)
    disabled = run_population(seed, arm, "independent", False, initial=initial)
    sparse_on = pulse_assay(enabled.population, seed, "independent", True, arm)
    sparse_off = pulse_assay(enabled.population, seed, "independent", False, arm)
    common_on = pulse_assay(enabled.population, seed, "correlated", True, arm)
    common_off = pulse_assay(enabled.population, seed, "correlated", False, arm)

    linked = enabled.population.occupied & (
        _linked_degree(enabled.population, edge_u, edge_v) > 0
    )
    low = (float(np.mean(enabled.population.support[linked] < 0.20))
           if linked.any() else 0.0)

    tail = slice(-100, None)
    return {
        "abundance_on": float(np.median(enabled.abundance[tail])),
        "abundance_off": float(np.median(disabled.abundance[tail])),
        "linked_support_on": float(np.median(enabled.linked_support[tail])),
        "linked_support_off": float(np.median(disabled.linked_support[tail])),
        "selection_delta": float(
            np.median(enabled.linked_support[tail])
            - np.median(disabled.linked_support[tail])
        ),
        "drift_from_initial": float(
            np.median(enabled.linked_support[tail]) - init_linked_support
        ),
        "mean_group_size": enabled.mean_group_size,
        "sparse_survivor_gain": sparse_on.survivors - sparse_off.survivors,
        "sparse_viability_gain": (
            sparse_on.integrated_viability - sparse_off.integrated_viability
        ),
        "common_viability_gain": (
            common_on.integrated_viability - common_off.integrated_viability
        ),
        "max_capacity_ratio": max(
            enabled.max_capacity_ratio, sparse_on.max_capacity_ratio
        ),
        "min_energy": enabled.min_energy,
        "low_support_fraction": low,
    }


def invasion_test(seed: int, arm: str) -> dict[str, float]:
    """P3: can 5% support~0 mutants sweep a cooperator population?"""
    initial = seed_invasion(seed)
    edge_u, edge_v = lattice()[1:]
    start = float(np.mean(initial.support[initial.occupied] < 0.20))
    pop = run_population(seed, arm, "independent", True, initial=initial).population
    if not pop.occupied.any():
        return {"start": start, "end": float("nan"), "mean_support": float("nan")}
    end = float(np.mean(pop.support[pop.occupied] < 0.20))
    return {"start": start, "end": end,
            "mean_support": float(pop.support[pop.occupied].mean())}


def run_experiment(seeds: int = 16) -> dict:
    arms: dict[str, dict] = {}
    for arm in ARMS:
        rows = [one_seed(s, arm) for s in range(seeds)]
        agg = {k: float(np.median([r[k] for r in rows])) for k in rows[0]}
        agg["positive_selection_seeds"] = float(
            np.mean([r["selection_delta"] >= 0.0 for r in rows])
        )
        agg["max_capacity_ratio"] = float(max(r["max_capacity_ratio"] for r in rows))
        agg["min_energy"] = float(min(r["min_energy"] for r in rows))
        arms[arm] = agg
    invasion = {
        arm: {k: float(np.median([invasion_test(s, arm)[k] for s in range(seeds // 2)]))
              for k in ("start", "end", "mean_support")}
        for arm in ARMS
    }
    return {"seeds": seeds, "arms": arms, "invasion": invasion}


def report(res: dict) -> None:
    print()
    print("BENCHMARK v1.13 — does relocating the cost retain the trait?")
    print(f"seeds {res['seeds']}, steps {STEPS}, sites {SIDE * SIDE}")
    print()
    print("  P2 RETENTION (median over seeds; positive = support retained)")
    print(f"  {'arm':<8}{'linked on':>11}{'linked off':>12}{'delta':>10}"
          f"{'pos seeds':>11}{'vs start':>10}{'abundance':>11}{'group sz':>10}")
    for arm in ARMS:
        a = res["arms"][arm]
        print(f"  {arm:<8}{a['linked_support_on']:>11.3f}{a['linked_support_off']:>12.3f}"
              f"{a['selection_delta']:>+10.4f}{a['positive_selection_seeds']:>10.0%}"
              f"{a['drift_from_initial']:>+10.4f}{a['abundance_on']:>11.1f}"
              f"{a['mean_group_size']:>10.1f}")
    print()
    print("  P1 ACCOUNTING")
    wr = max(res["arms"][a]["max_capacity_ratio"] for a in ARMS)
    we = min(res["arms"][a]["min_energy"] for a in ARMS)
    print(f"  max transfer draw / unused capacity : {wr:.6f}")
    print(f"  min stored energy                   : {we:.6f}")
    print()
    print("  P3 INVASION (5% support<0.20 mutants seeded into cooperators)")
    print(f"  {'arm':<8}{'start':>9}{'end':>9}{'mean support':>15}")
    for arm in ARMS:
        v = res["invasion"][arm]
        print(f"  {arm:<8}{v['start']:>9.1%}{v['end']:>9.1%}{v['mean_support']:>15.3f}")
    print()
    print("  P5 COMMON MODE (paired assay gains)")
    print(f"  {'arm':<8}{'sparse viab':>13}{'common viab':>13}{'low support':>13}")
    for arm in ARMS:
        a = res["arms"][arm]
        print(f"  {arm:<8}{a['sparse_viability_gain']:>+13.4f}"
              f"{a['common_viability_gain']:>+13.4f}{a['low_support_fraction']:>13.1%}")
    print()
    pool = res["arms"]["pool"]
    print("  preregistered candidate criterion:", end=" ")
    if pool["positive_selection_seeds"] > 0.5 and pool["selection_delta"] > 0.0:
        print("SUPPORTED for pool")
        print("  Relocating the cost to the group retains support where donor")
        print("  funding does not. Cost-bearing was the obstruction.")
    else:
        print("NOT SUPPORTED")
        print("  Group funding does not retain support either. The obstruction is")
        print("  not who pays but that the selection level cannot see the benefit;")
        print("  no accounting change in this model reaches it.")


def plot(res: dict, path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.0))
    labels = list(ARMS)

    deltas = [res["arms"][a]["selection_delta"] for a in ARMS]
    drifts = [res["arms"][a]["drift_from_initial"] for a in ARMS]
    x = np.arange(len(ARMS))
    axes[0].bar(x - 0.2, deltas, width=0.4, label="vs. matched control",
                color=["#c44e52" if d < 0 else "#55a868" for d in deltas])
    axes[0].bar(x + 0.2, drifts, width=0.4, label="vs. start",
                color=["#e29ca0" if d < 0 else "#a6d0b3" for d in drifts])
    axes[0].axhline(0, color="black", linewidth=1)
    axes[0].set_xticks(x, labels)
    axes[0].set(title="(a) Support selection", ylabel="linked support delta")
    axes[0].legend(fontsize=8)

    starts = [res["invasion"][a]["start"] for a in ARMS]
    ends = [res["invasion"][a]["end"] for a in ARMS]
    axes[1].bar(x - 0.2, starts, width=0.4, label="seeded", color="#8172b2")
    axes[1].bar(x + 0.2, ends, width=0.4, label="final", color="#c44e52")
    axes[1].axhline(0.5, color="black", linestyle=":", linewidth=1)
    axes[1].set_xticks(x, labels)
    axes[1].set(title="(b) Cheater invasion", ylabel="fraction support < 0.20")
    axes[1].legend(fontsize=8)

    sparse = [res["arms"][a]["sparse_viability_gain"] for a in ARMS]
    common = [res["arms"][a]["common_viability_gain"] for a in ARMS]
    axes[2].bar(x - 0.2, sparse, width=0.4, label="sparse", color="#4c72b0")
    axes[2].bar(x + 0.2, common, width=0.4, label="common", color="#dd8452")
    axes[2].axhline(0, color="black", linewidth=1)
    axes[2].set_xticks(x, labels)
    axes[2].set(title="(c) Paired ablation gain", ylabel="integrated viability")
    axes[2].legend(fontsize=8)
    for ax in axes:
        ax.grid(alpha=0.3)

    fig.suptitle("v1.13 — donor-funded vs group-pool-funded support")
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
        path = Path(__file__).resolve().parents[2] / "tools" / "inverse_benchmark_pool.png"
        plot(res, path)


if __name__ == "__main__":
    main()
