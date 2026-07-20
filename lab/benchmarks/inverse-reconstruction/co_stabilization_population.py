#!/usr/bin/env python3
"""
co_stabilization_population.py

Benchmark v1.11 — can a population build its own support network?

QUESTION
v1.10 supplied a repair graph from outside and showed that routing otherwise-
unused capacity can improve viability under sparse shocks without exceeding a
matched repair budget. v1.11 removes the supplied graph. Individuals occupy a
spatial population, reproduce locally, mutate, die, and pay for every support
link and transfer. Link propensity and support propensity are heritable.
Links form and dissolve during the run; low-support recipients ("cheaters")
are allowed. There is no explicit fitness or group reward: survival and local
reproduction are the only selection events.

STATE AND COSTS
  health          — damaged by shocks and starvation; death below a cutoff.
  energy          — receives environmental resources; pays metabolism, link
                    maintenance, self-repair, transfers, and reproduction.
  support gene    — fraction of unused per-step repair capacity offered to
                    linked damaged neighbors.
  link gene       — probability weight for forming a local support link.

The geography is a fixed toroidal lattice, but the occupied population and
support graph are not fixed. A link exists only if both endpoints are alive,
costs both endpoints each step, and can break. Offspring inherit both genes
with mutation. Transfers are lossy and may use only capacity left after local
repair. Disabling transfer leaves the demographic, resource, mutation, link,
and shock rules intact.

PREREGISTERED PREDICTIONS (before the first run)
  P1 ACCOUNTING: energy never becomes negative; no donor exceeds its unused
     repair capacity; link maintenance and reproduction are paid explicitly.
  P2 SELECTION: under independent shocks, transfer-enabled populations retain
     more support capacity (mean support among linked agents) than matched
     transfer-disabled controls in a majority of seeds.
  P3 FUNCTION: after evolution under independent shocks, paired sparse-shock
     assays recover faster and retain more survivors with evolved transfers
     enabled than with the same agents and links ablated.
  P4 COMMON MODE: the paired benefit is smaller under correlated damage, where
     healthy donors largely disappear.
  P5 CHEATERS: support need not fix at one. Without partner choice, recipients
     with low contribution can persist; their frequency is reported rather
     than treated as a failure of accounting. After the two-seed pilot, the
     descriptive threshold was fixed at support < 0.20 (and link gene > 0.50
     for the stricter link-seeking-cheater diagnostic). This diagnostic is not
     part of the candidate criterion.

CANDIDATE CRITERION
Endogenous co-stabilization receives a first bounded positive result only if
P1 passes, transfer-enabled evolution retains more linked support than the
disabled control in >50% of seeds, and the median paired sparse-shock assay
has both positive survivor gain and faster recovery. A result remains a toy
population mechanism, not metabolism, open-ended evolution, life, identity,
or consciousness. Failure is informative: it locates which supplied rule
(partner choice, kin structure, resource production, or topology) is still
missing.

RESULT (first full run; 16 seeds, 600 steps, 144 sites)
  P1 CONFIRMED: maximum transfer draw / unused repair capacity = 1.000000;
     minimum stored energy = 0.000000. Link, transfer, and birth costs are
     explicit. Median link turnover is 1,236 formed / 1,168 broken, so the
     realized support graph is dynamically constructed rather than fixed.
  P2 FALSIFIED: transfer-enabled populations retain less linked support than
     disabled controls in all 16 seeds (0.378 versus 0.486; median delta
     -0.1061; positive seeds 0%). Support also falls -0.1221 from its initial
     level. Late abundance is lower (104.1 versus 125.6).
  P3 CONFIRMED in the paired acute assay: enabling the evolved transfers adds
     +0.0089 survivors, +0.0176 integrated viability, and a 2-step recovery
     advantage after a sparse pulse. The network is functionally useful even
     though selection does not retain its costly contribution trait.
  P4 PARTIAL: common-mode survivor gain is +0.0000 and integrated viability
     gain +0.0097, smaller than the sparse +0.0176; however, the recovery-time
     advantage is 3 rather than 2 steps. The common-mode limit holds for
     survival/integrated function, not for every summary statistic.
  P5 CONFIRMED descriptively: 40.4% of linked agents have support < 0.20 and
     17.6% combine support < 0.20 with link propensity > 0.50.

The preregistered candidate criterion is NOT SUPPORTED because P2 fails
decisively. This population produces a multilevel tension: paid support helps
the current collective under perturbation, while local survival/reproduction
selects its heritable contribution downward in the no-partner-choice model.
The fixed toroidal geography still constrains possible partners; only the
occupied population and realized links are endogenous. The result locates the
next discriminating mechanisms — partner choice, conditional reciprocity, and
spatial/kin assortment — rather than licensing an ecology or life claim.

Usage:
    python co_stabilization_population.py
    python co_stabilization_population.py --seeds 16
    python co_stabilization_population.py --save
"""

from __future__ import annotations

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
            self.occupied.copy(),
            self.health.copy(),
            self.energy.copy(),
            self.support.copy(),
            self.link_gene.copy(),
            self.links.copy(),
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


def make_environment(
    seed: int,
    steps: int = STEPS,
    side: int = SIDE,
) -> Environment:
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
    rng = np.random.default_rng(seed)
    n = side * side
    _, edge_u, edge_v = lattice(side)
    occupied = rng.random(n) < 0.72
    # Keep every initial condition well inside the viable population regime.
    if occupied.sum() < n // 2:
        occupied[np.argsort(rng.random(n))[: n // 2]] = True
    health = np.where(occupied, rng.uniform(0.82, 1.0, n), 0.0)
    energy = np.where(occupied, rng.uniform(0.42, 0.88, n), 0.0)
    support = np.where(occupied, rng.uniform(0.0, 1.0, n), 0.0)
    link_gene = np.where(occupied, rng.uniform(0.0, 1.0, n), 0.0)
    probability = 0.22 * np.sqrt(link_gene[edge_u] * link_gene[edge_v])
    links = occupied[edge_u] & occupied[edge_v] & (rng.random(len(edge_u)) < probability)
    return Population(occupied, health, energy, support, link_gene, links)


def _linked_degree(
    pop: Population,
    edge_u: np.ndarray,
    edge_v: np.ndarray,
) -> np.ndarray:
    degree = np.zeros(len(pop.occupied), dtype=int)
    np.add.at(degree, edge_u[pop.links], 1)
    np.add.at(degree, edge_v[pop.links], 1)
    return degree


def _summary(
    pop: Population,
    edge_u: np.ndarray,
    edge_v: np.ndarray,
) -> tuple[float, float, float, float]:
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


def _route_support(
    pop: Population,
    spare: np.ndarray,
    edge_u: np.ndarray,
    edge_v: np.ndarray,
    enabled: bool,
) -> tuple[float, float]:
    """Route paid, lossy support and return draw plus capacity ratio."""
    if not enabled or not pop.links.any():
        return 0.0, 0.0
    incident: list[list[int]] = [[] for _ in range(len(pop.occupied))]
    for u, v in zip(edge_u[pop.links], edge_v[pop.links]):
        incident[int(u)].append(int(v))
        incident[int(v)].append(int(u))

    total_draw = 0.0
    max_ratio = 0.0
    order = np.flatnonzero(pop.occupied)
    # Fixed site order makes the routing rule reproducible; paired assays swap
    # only the transfer flag, not the environment or evolved state.
    for donor in order:
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


def _clear_dead_links(
    pop: Population,
    edge_u: np.ndarray,
    edge_v: np.ndarray,
) -> int:
    invalid = pop.links & (~pop.occupied[edge_u] | ~pop.occupied[edge_v])
    count = int(invalid.sum())
    pop.links[invalid] = False
    return count


def population_step(
    pop: Population,
    env: Environment,
    t: int,
    regime: str,
    transfer_enabled: bool,
    neighbors: np.ndarray,
    edge_u: np.ndarray,
    edge_v: np.ndarray,
    reproduce: bool = True,
    evolve_links: bool = True,
) -> dict[str, float]:
    """Advance one paid demographic step."""
    occupied_start = pop.occupied.copy()
    pop.energy[pop.occupied] = np.minimum(
        ENERGY_CAP,
        pop.energy[pop.occupied] + env.resource[t, pop.occupied],
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
    _, transfer_ratio = _route_support(
        pop, spare, edge_u, edge_v, transfer_enabled
    )

    pop.health = np.minimum(pop.health, 1.0)
    dead = pop.occupied & (
        (pop.health <= DEATH_CUTOFF)
        | (env.background_death[t] < BACKGROUND_DEATH)
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
        break_now = pop.links & (
            (~valid) | (env.link_break[t] < LINK_BREAK_RATE)
        )
        broken += int(break_now.sum())
        pop.links[break_now] = False
        propensity = np.sqrt(pop.link_gene[edge_u] * pop.link_gene[edge_v])
        form_now = (
            (~pop.links)
            & valid
            & (env.link_form[t] < LINK_FORM_RATE * propensity)
        )
        pop.links[form_now] = True
        formed = int(form_now.sum())

    assert np.all(pop.energy >= -1e-10)
    pop.energy = np.maximum(pop.energy, 0.0)
    # Every transfer is bounded by capacity after local self-repair.
    assert transfer_ratio <= 1.0 + 1e-10
    return {
        "births": float(births),
        "deaths": float(deaths),
        "formed": float(formed),
        "broken": float(broken),
        "capacity_ratio": float(transfer_ratio),
        "min_energy": float(pop.energy.min()),
        "occupied_start": float(occupied_start.sum()),
    }


def run_population(
    seed: int,
    regime: str = "independent",
    transfer_enabled: bool = True,
    steps: int = STEPS,
    initial: Population | None = None,
) -> RunResult:
    neighbors, edge_u, edge_v = lattice()
    env = make_environment(seed, steps=steps)
    pop = initialize(seed) if initial is None else initial.copy()
    abundance = np.zeros(steps)
    mean_support = np.zeros(steps)
    linked_support = np.zeros(steps)
    link_density = np.zeros(steps)
    max_ratio = 0.0
    min_energy = float("inf")
    formed = broken = births = deaths = 0

    for t in range(steps):
        audit = population_step(
            pop, env, t, regime, transfer_enabled,
            neighbors, edge_u, edge_v,
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

    return RunResult(
        pop, abundance, mean_support, linked_support, link_density,
        max_ratio, min_energy, formed, broken, births, deaths,
    )


def pulse_assay(
    evolved: Population,
    seed: int,
    regime: str,
    transfer_enabled: bool,
    steps: int = ASSAY_STEPS,
) -> AssayResult:
    """Paired post-evolution assay with demography and link changes frozen."""
    pop = evolved.copy()
    neighbors, edge_u, edge_v = lattice()
    env = make_environment(seed + 50_000, steps=steps)
    # A pulse makes the counterfactual legible without a demographic lottery.
    rng = np.random.default_rng(seed + 80_000)
    alive = np.flatnonzero(pop.occupied)
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
            pop, env, t, regime="none",
            transfer_enabled=transfer_enabled,
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
    return AssayResult(
        survivors, health, recovery, max_ratio, viability_sum / steps
    )


def one_seed(seed: int) -> dict[str, float]:
    initial = initialize(seed)
    edge_u, edge_v = lattice()[1:]
    initial_linked = initial.occupied & (
        _linked_degree(initial, edge_u, edge_v) > 0
    )
    initial_linked_support = (
        float(initial.support[initial_linked].mean())
        if initial_linked.any() else 0.0
    )
    enabled = run_population(seed, "independent", True, initial=initial)
    disabled = run_population(seed, "independent", False, initial=initial)
    sparse_on = pulse_assay(enabled.population, seed, "independent", True)
    sparse_off = pulse_assay(enabled.population, seed, "independent", False)
    common_on = pulse_assay(enabled.population, seed, "correlated", True)
    common_off = pulse_assay(enabled.population, seed, "correlated", False)
    linked = enabled.population.occupied & (
        _linked_degree(enabled.population, edge_u, edge_v) > 0
    )
    if linked.any():
        low_support_fraction = float(
            np.mean(enabled.population.support[linked] < 0.20)
        )
        link_seeking_cheater_fraction = float(np.mean(
            (enabled.population.support[linked] < 0.20)
            & (enabled.population.link_gene[linked] > 0.50)
        ))
        enabled_link_gene = float(enabled.population.link_gene[linked].mean())
    else:
        low_support_fraction = 0.0
        link_seeking_cheater_fraction = 0.0
        enabled_link_gene = 0.0
    tail = max(1, STEPS // 5)
    return {
        "enabled_abundance": float(enabled.abundance[-tail:].mean()),
        "disabled_abundance": float(disabled.abundance[-tail:].mean()),
        "enabled_linked_support": float(enabled.linked_support[-tail:].mean()),
        "disabled_linked_support": float(disabled.linked_support[-tail:].mean()),
        "enabled_link_density": float(enabled.link_density[-tail:].mean()),
        "disabled_link_density": float(disabled.link_density[-tail:].mean()),
        "support_selection": float(
            enabled.linked_support[-tail:].mean()
            - disabled.linked_support[-tail:].mean()
        ),
        "support_change_from_initial": float(
            enabled.linked_support[-tail:].mean() - initial_linked_support
        ),
        "enabled_link_gene": enabled_link_gene,
        "sparse_survivor_gain": sparse_on.survivors - sparse_off.survivors,
        "sparse_health_gain": sparse_on.mean_health - sparse_off.mean_health,
        "sparse_recovery_gain": sparse_off.recovery_time - sparse_on.recovery_time,
        "sparse_viability_gain": (
            sparse_on.integrated_viability - sparse_off.integrated_viability
        ),
        "common_survivor_gain": common_on.survivors - common_off.survivors,
        "common_health_gain": common_on.mean_health - common_off.mean_health,
        "common_recovery_gain": common_off.recovery_time - common_on.recovery_time,
        "common_viability_gain": (
            common_on.integrated_viability - common_off.integrated_viability
        ),
        "max_capacity_ratio": max(
            enabled.max_capacity_ratio, disabled.max_capacity_ratio,
            sparse_on.max_capacity_ratio, common_on.max_capacity_ratio,
        ),
        "min_energy": min(enabled.min_energy, disabled.min_energy),
        "links_formed": float(enabled.links_formed),
        "links_broken": float(enabled.links_broken),
        "births": float(enabled.births),
        "deaths": float(enabled.deaths),
        "low_support_fraction": low_support_fraction,
        "link_seeking_cheater_fraction": link_seeking_cheater_fraction,
    }


def run_experiment(seeds: int) -> dict[str, np.ndarray | float | bool]:
    rows = [one_seed(seed) for seed in range(seeds)]
    keys = rows[0].keys()
    data = {key: np.asarray([row[key] for row in rows]) for key in keys}
    positive_selection = float(np.mean(data["support_selection"] > 0.0))
    criterion = bool(
        data["max_capacity_ratio"].max() <= 1.0 + 1e-9
        and data["min_energy"].min() >= -1e-9
        and positive_selection > 0.50
        and np.median(data["sparse_survivor_gain"]) > 0.0
        and np.median(data["sparse_recovery_gain"]) > 0.0
    )
    return {
        **data,
        "positive_selection_fraction": positive_selection,
        "criterion_supported": criterion,
    }


def report(result: dict[str, np.ndarray | float | bool]) -> None:
    med = lambda key: float(np.median(result[key]))  # noqa: E731
    print("BENCHMARK v1.11 — endogenous support population")
    print(f"seeds {len(result['support_selection'])}, steps {STEPS}, sites {SIDE * SIDE}")
    print()
    print("late-run medians (transfer enabled / disabled):")
    print(
        f"abundance {med('enabled_abundance'):.1f} / "
        f"{med('disabled_abundance'):.1f}"
    )
    print(
        f"linked support {med('enabled_linked_support'):.3f} / "
        f"{med('disabled_linked_support'):.3f}"
    )
    print(
        f"link density {med('enabled_link_density'):.3f} / "
        f"{med('disabled_link_density'):.3f}"
    )
    print(
        f"support-selection delta {med('support_selection'):+.4f}; "
        f"positive seeds {100 * float(result['positive_selection_fraction']):.1f}%"
    )
    print()
    print("paired evolved-network ablation:")
    print(
        f"sparse survivor gain {med('sparse_survivor_gain'):+.4f}; "
        f"viability gain {med('sparse_viability_gain'):+.4f}; "
        f"recovery advantage {med('sparse_recovery_gain'):+.1f} steps"
    )
    print(
        f"common-mode survivor gain {med('common_survivor_gain'):+.4f}; "
        f"viability gain {med('common_viability_gain'):+.4f}; "
        f"recovery advantage {med('common_recovery_gain'):+.1f} steps"
    )
    print()
    print(
        f"audit max capacity ratio {np.max(result['max_capacity_ratio']):.6f}; "
        f"min energy {np.min(result['min_energy']):.6f}"
    )
    print(
        f"turnover medians: links +{med('links_formed'):.0f}/-{med('links_broken'):.0f}, "
        f"births {med('births'):.0f}, deaths {med('deaths'):.0f}"
    )
    print(
        f"support change from initial {med('support_change_from_initial'):+.4f}; "
        f"linked mean link gene {med('enabled_link_gene'):.3f}"
    )
    print(
        f"low-support linked agents {100 * med('low_support_fraction'):.1f}%; "
        f"link-seeking cheaters {100 * med('link_seeking_cheater_fraction'):.1f}%"
    )
    verdict = "SUPPORTED" if result["criterion_supported"] else "NOT SUPPORTED"
    print(f"preregistered candidate criterion: {verdict}")


def plot(result: dict[str, np.ndarray | float | bool], path: Path) -> None:
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    axes[0].scatter(
        result["disabled_linked_support"], result["enabled_linked_support"],
        alpha=0.75,
    )
    axes[0].axline((0, 0), slope=1, color="black", linewidth=1)
    axes[0].set(xlabel="transfer disabled", ylabel="transfer enabled", title="Linked support")
    axes[1].boxplot(
        [result["sparse_viability_gain"], result["common_viability_gain"]],
        tick_labels=["sparse", "common"],
    )
    axes[1].axhline(0, color="black", linewidth=1)
    axes[1].set(title="Paired viability gain", ylabel="transfer on − ablated")
    axes[2].scatter(result["links_formed"], result["links_broken"], alpha=0.75)
    axes[2].axline((0, 0), slope=1, color="black", linewidth=1)
    axes[2].set(xlabel="formed", ylabel="broken", title="Endogenous link turnover")
    fig.suptitle("v1.11 — endogenous support population")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=170)
    print(f"saved {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=16)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    if args.seeds < 1:
        parser.error("--seeds must be >= 1")
    result = run_experiment(args.seeds)
    report(result)
    if args.save:
        path = Path(__file__).resolve().parents[2] / "tools" / "inverse_benchmark_population.png"
        plot(result, path)


if __name__ == "__main__":
    main()
