#!/usr/bin/env python3
"""
co_stabilization_redundancy.py

Benchmark v1.10 — redundancy versus dependency under a matched repair budget.

QUESTION
v1.9 showed that coupling which substitutes for self-sufficiency creates
super-additive knockout cascades and *reduces* noise viability. That is
dependency, not yet co-stabilization. This experiment asks whether coupling
can make a causal, budget-matched contribution to viability rather than merely
move fragility around.

ARCHITECTURES
Every active node owns the same repair budget B per step.

  coexistence  — a node may spend B only on its own deficit; unused capacity
                 is discarded.
  substitution — a fixed fraction c of B is reserved for neighbors and only
                 (1-c)B remains local. Transfer loses (1-eta) in transit.
  redundancy   — a node repairs itself first; only unused capacity may be
                 routed to damaged neighbors. Coupling supplements rather
                 than replaces self-sufficiency. Total capacity remains N*B.

The redundancy mechanism is not guaranteed to help: transfer is lossy, it has
no spare donors under correlated shocks, topology restricts reach, and
permanent knockout removes both a node and its repair capacity.

PROBES AND TWO AXES
  Resilience gain     = viability(redundancy) - viability(coexistence)
                        under the same shocks and total repair capacity.
  Dependency cost     = additional viability lost by surviving nodes after a
                        permanent knockout, relative to the matched no-
                        knockout twin.

A knockout cascade alone is never counted as co-stabilization. The narrow
candidate criterion requires a positive, budget-matched resilience gain under
sparse distributed shocks across the sensitivity grid. Dependency cost is
reported separately; it is a profile, not evidence by itself.

SENSITIVITY
  N in {16, 32, 64}; ring, small-world, connected-random topology;
  viability threshold in {0.60, 0.75}; independent versus correlated shocks;
  single and double knockout in the headline case; transfer efficiency and
  repair-budget sweeps in the representative case.

PREDICTIONS (registered before first run)
  P1 BUDGET: no architecture draws more than B per active node per step.
  P2 REDUNDANCY: under sparse independent shocks, redundancy beats matched
     coexistence in at least 75% of N/topology/threshold cells and has a
     positive median resilience gain.
  P3 CORRELATION LIMIT: redundancy's gain is smaller under correlated shocks,
     where healthy spare donors largely disappear.
  P4 SUBSTITUTION: substitution does not outperform coexistence in the
     majority of independent-shock cells and carries greater knockout
     dependency than coexistence.
  P5 COST: redundancy's benefit weakens as transfer efficiency falls; a
     positive result must not depend on eta=1 or one hand-picked budget.

RESULT (first run; headline 20 seeds, sensitivity 12 seeds per cell)
  P1 CONFIRMED: maximum resource draw / available capacity = 1.000000.
  P2 CONFIRMED: redundancy beats coexistence in 100% of the 18 sensitivity
     cells; median independent-shock gain = +0.0543. In the headline case,
     viability is 0.999 versus 0.933 and localized recovery takes 4.6 versus
     7.0 steps.
  P3 CONFIRMED: median correlated-shock gain = +0.0000. When all nodes are
     damaged together, there is no healthy spare capacity to route.
  P4 FALSIFIED: substitution also beats coexistence under independent shocks
     in every sensitivity cell (headline 0.993 versus 0.933). Pooling alone
     is beneficial when damage is sparse. Its limits remain visible:
     correlated viability is lower (0.981 versus 0.992), and knockout costs
     are higher. Post-run diagnostic: redundancy still beats substitution in
     100% of cells, median +0.0129.
  P5 CONFIRMED: redundancy gain stays positive from eta=0.40 to 1.00
     (+0.0602 to +0.0657) and for B in {0.08, 0.12, 0.16}
     (+0.1343, +0.0652, +0.0377).

The preregistered candidate criterion is SUPPORTED. The measured content is
one budget-matched mechanism: healthy nodes' otherwise-unused capacity
causally improves system viability under sparse shocks. Edge ablation
(eta=0) reduces the architecture exactly to coexistence. Single/double node
knockout costs remain near zero for redundancy (0.000 / 0.001), so the gain
does not require keystone fragility. This is functional mutual support in a
designed repair network, not spontaneous ecology, metabolism, or life.

FAILURE CONDITIONS
The co-stabilization candidate fails if the median independent-shock gain is
non-positive, if fewer than 75% of sensitivity cells improve, if any budget
audit fails, or if gains appear only at lossless transfer / one parameter
choice. A positive result remains a toy mechanism of mutual support, not a
theory of life, metabolism, identity, or consciousness.

Usage:
    python co_stabilization_redundancy.py
    python co_stabilization_redundancy.py --seeds 12
    python co_stabilization_redundancy.py --save
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ARCHITECTURES = ("coexistence", "substitution", "redundancy")
TOPOLOGIES = ("ring", "small_world", "random_connected")
N_VALUES = (16, 32, 64)
THRESHOLDS = (0.60, 0.75)

DEFAULT_BUDGET = 0.12
DEFAULT_ETA = 0.75
SUBSTITUTION_SHARE = 0.70
STEPS = 180
KNOCKOUT_AT = 90
EPS = 1e-12


@dataclass
class SimResult:
    viability: float
    mean_health: float
    max_budget_ratio: float
    viable_trace: np.ndarray
    health_trace: np.ndarray


def _add_edge(adj: np.ndarray, i: int, j: int) -> None:
    if i != j:
        adj[i, j] = True
        adj[j, i] = True


def make_adjacency(n: int, topology: str, seed: int = 0) -> np.ndarray:
    """Connected undirected graphs with no external dependency."""
    rng = np.random.default_rng(seed)
    adj = np.zeros((n, n), dtype=bool)

    if topology == "ring":
        for i in range(n):
            _add_edge(adj, i, (i + 1) % n)

    elif topology == "small_world":
        # Degree-4 ring lattice, then rewire forward edges with p=0.20.
        edges = []
        for i in range(n):
            for d in (1, 2):
                j = (i + d) % n
                if i < j or (i + d) >= n:
                    edges.append((i, j))
        for i, j in edges:
            if rng.random() < 0.20:
                candidates = np.flatnonzero(
                    (np.arange(n) != i) & (~adj[i])
                )
                # Build progressively: avoid self/duplicate; preserve edge count.
                candidates = candidates[candidates != j]
                if len(candidates):
                    j = int(rng.choice(candidates))
            _add_edge(adj, i, j)
        # Connectivity guard: retain a ring backbone.
        for i in range(n):
            _add_edge(adj, i, (i + 1) % n)

    elif topology == "random_connected":
        # Ring backbone guarantees connectivity; add random edges to mean degree 4.
        for i in range(n):
            _add_edge(adj, i, (i + 1) % n)
        target_edges = 2 * n
        while int(adj.sum() // 2) < target_edges:
            i, j = rng.integers(0, n, size=2)
            _add_edge(adj, int(i), int(j))
    else:
        raise ValueError(f"unknown topology: {topology}")

    return adj


def make_damage(seed: int, n: int, regime: str, steps: int = STEPS) -> np.ndarray:
    """Matched damage trace used by every architecture in a comparison."""
    rng = np.random.default_rng(seed)
    damage = np.zeros((steps, n), dtype=float)

    if regime == "independent":
        hit = rng.random((steps, n)) < 0.08
        magnitude = rng.uniform(0.25, 0.55, size=(steps, n))
        damage = hit * magnitude

    elif regime == "correlated":
        event = rng.random(steps) < 0.07
        magnitude = rng.uniform(0.18, 0.42, size=steps)
        damage = event[:, None] * magnitude[:, None] * np.ones((1, n))

    else:
        raise ValueError(f"unknown damage regime: {regime}")

    return damage


def _route(
    donor_amount: np.ndarray,
    need: np.ndarray,
    adj: np.ndarray,
    active: np.ndarray,
    eta: float,
) -> tuple[np.ndarray, float]:
    """Route donor budgets to currently damaged active neighbors.

    Returns delivered repair (after transfer loss and need caps) plus resource
    drawn at donors (before transfer loss). Oversupply is counted as spent,
    which prevents hidden free capacity.
    """
    n = len(need)
    received = np.zeros(n, dtype=float)
    drawn = 0.0

    for i in range(n):
        amount = float(donor_amount[i])
        if not active[i] or amount <= EPS:
            continue
        targets = np.flatnonzero(adj[i] & active & (need > EPS))
        if len(targets) == 0:
            continue
        weights = need[targets]
        weights = weights / weights.sum()
        received[targets] += eta * amount * weights
        drawn += amount

    return np.minimum(received, need), drawn


def repair_step(
    h_after_damage: np.ndarray,
    adj: np.ndarray,
    architecture: str,
    active: np.ndarray,
    budget: float,
    eta: float,
    substitution_share: float = SUBSTITUTION_SHARE,
) -> tuple[np.ndarray, float, float]:
    """Apply one repair step and return (new health, resource draw, capacity)."""
    need = np.maximum(0.0, 1.0 - h_after_damage)
    n_active = int(active.sum())
    capacity = budget * n_active
    repair = np.zeros_like(h_after_damage)

    if architecture == "coexistence":
        local = np.minimum(need, budget) * active
        repair += local
        drawn = float(local.sum())

    elif architecture == "substitution":
        local_cap = budget * (1.0 - substitution_share)
        local = np.minimum(need, local_cap) * active
        repair += local
        remaining_need = np.maximum(0.0, need - repair)
        donor = np.full(len(need), budget * substitution_share) * active
        delivered, sent = _route(donor, remaining_need, adj, active, eta)
        repair += delivered
        drawn = float(local.sum()) + sent

    elif architecture == "redundancy":
        # Local priority: coupling can use only capacity that the donor did
        # not need for itself. This is pooled spare capacity, not added energy.
        local = np.minimum(need, budget) * active
        repair += local
        remaining_need = np.maximum(0.0, need - repair)
        donor = np.maximum(0.0, budget - local) * active
        delivered, sent = _route(donor, remaining_need, adj, active, eta)
        repair += delivered
        drawn = float(local.sum()) + sent

    else:
        raise ValueError(f"unknown architecture: {architecture}")

    if drawn > capacity + 1e-9:
        raise AssertionError(
            f"budget violation: draw={drawn:.6f} capacity={capacity:.6f}"
        )

    out = np.clip(h_after_damage + repair, 0.0, 1.0)
    out[~active] = 0.0
    return out, drawn, capacity


def simulate(
    architecture: str,
    adj: np.ndarray,
    damage: np.ndarray,
    threshold: float,
    budget: float = DEFAULT_BUDGET,
    eta: float = DEFAULT_ETA,
    frozen_targets: tuple[int, ...] = (),
    knockout_at: int | None = None,
) -> SimResult:
    """Run one matched world. Frozen targets lose health and repair capacity."""
    steps, n = damage.shape
    h = np.ones(n, dtype=float)
    active = np.ones(n, dtype=bool)
    viable_trace = np.empty((steps, n), dtype=bool)
    health_trace = np.empty((steps, n), dtype=float)
    budget_ratios = []

    for t in range(steps):
        if knockout_at is not None and t >= knockout_at:
            active[list(frozen_targets)] = False
            h[~active] = 0.0

        h = np.clip(h - damage[t], 0.0, 1.0)
        h[~active] = 0.0
        h, drawn, capacity = repair_step(
            h, adj, architecture, active, budget, eta
        )
        budget_ratios.append(drawn / capacity if capacity > 0 else 0.0)
        viable_trace[t] = h >= threshold
        health_trace[t] = h

    return SimResult(
        viability=float(viable_trace.mean()),
        mean_health=float(health_trace.mean()),
        max_budget_ratio=float(max(budget_ratios, default=0.0)),
        viable_trace=viable_trace,
        health_trace=health_trace,
    )


def knockout_dependency(
    architecture: str,
    adj: np.ndarray,
    damage: np.ndarray,
    threshold: float,
    targets: tuple[int, ...],
    budget: float = DEFAULT_BUDGET,
    eta: float = DEFAULT_ETA,
) -> float:
    """Counterfactual loss among survivors caused by permanent knockout."""
    base = simulate(architecture, adj, damage, threshold, budget, eta)
    ko = simulate(
        architecture, adj, damage, threshold, budget, eta,
        frozen_targets=targets, knockout_at=KNOCKOUT_AT,
    )
    keep = np.ones(adj.shape[0], dtype=bool)
    keep[list(targets)] = False
    base_v = base.viable_trace[KNOCKOUT_AT:, keep].mean()
    ko_v = ko.viable_trace[KNOCKOUT_AT:, keep].mean()
    return float(base_v - ko_v)


def localized_recovery_steps(
    architecture: str,
    adj: np.ndarray,
    threshold: float = 0.95,
    budget: float = DEFAULT_BUDGET,
    eta: float = DEFAULT_ETA,
) -> int:
    """Steps for a node plus its neighbors to recover from a one-off shock."""
    n = adj.shape[0]
    target = int(np.argmax(adj.sum(axis=1)))
    damaged = np.flatnonzero(adj[target])
    damaged = np.unique(np.concatenate(([target], damaged)))
    h = np.ones(n)
    h[damaged] = 0.20
    active = np.ones(n, dtype=bool)

    for t in range(1, 101):
        h, _, _ = repair_step(h, adj, architecture, active, budget, eta)
        if np.all(h >= threshold):
            return t
    return 101


def _top_targets(adj: np.ndarray, count: int) -> tuple[int, ...]:
    order = np.argsort(-adj.sum(axis=1), kind="stable")
    return tuple(int(x) for x in order[:count])


def headline_suite(seeds: int = 30) -> dict:
    """Representative N=32 small-world case, including one/two knockouts."""
    n = 32
    threshold = 0.70
    viability = {
        regime: {a: [] for a in ARCHITECTURES}
        for regime in ("independent", "correlated")
    }
    ko1 = {a: [] for a in ARCHITECTURES}
    ko2 = {a: [] for a in ARCHITECTURES}
    budget_max = {a: 0.0 for a in ARCHITECTURES}
    recovery = {a: [] for a in ARCHITECTURES}

    for seed in range(seeds):
        adj = make_adjacency(n, "small_world", seed)
        damage_ind = make_damage(seed, n, "independent")
        damage_cor = make_damage(seed, n, "correlated")
        for a in ARCHITECTURES:
            ri = simulate(a, adj, damage_ind, threshold)
            rc = simulate(a, adj, damage_cor, threshold)
            viability["independent"][a].append(ri.viability)
            viability["correlated"][a].append(rc.viability)
            budget_max[a] = max(
                budget_max[a], ri.max_budget_ratio, rc.max_budget_ratio
            )
            ko1[a].append(
                knockout_dependency(
                    a, adj, damage_ind, threshold, _top_targets(adj, 1)
                )
            )
            ko2[a].append(
                knockout_dependency(
                    a, adj, damage_ind, threshold, _top_targets(adj, 2)
                )
            )
            recovery[a].append(localized_recovery_steps(a, adj))

    return {
        "viability": {
            r: {a: float(np.mean(v)) for a, v in by_a.items()}
            for r, by_a in viability.items()
        },
        "ko1": {a: float(np.mean(v)) for a, v in ko1.items()},
        "ko2": {a: float(np.mean(v)) for a, v in ko2.items()},
        "budget_max": budget_max,
        "recovery": {a: float(np.mean(v)) for a, v in recovery.items()},
        "seeds": seeds,
    }


def sensitivity_grid(seeds: int = 8) -> list[dict]:
    """N/topology/threshold grid; one matched trace per seed and regime."""
    cells = []
    for n in N_VALUES:
        for topology in TOPOLOGIES:
            for threshold in THRESHOLDS:
                vals = {
                    regime: {a: [] for a in ARCHITECTURES}
                    for regime in ("independent", "correlated")
                }
                max_budget = 0.0
                for seed in range(seeds):
                    adj = make_adjacency(n, topology, seed)
                    for regime in ("independent", "correlated"):
                        damage = make_damage(seed, n, regime)
                        for a in ARCHITECTURES:
                            res = simulate(a, adj, damage, threshold)
                            vals[regime][a].append(res.viability)
                            max_budget = max(max_budget, res.max_budget_ratio)

                means = {
                    regime: {a: float(np.mean(v)) for a, v in by_a.items()}
                    for regime, by_a in vals.items()
                }
                cells.append({
                    "n": n,
                    "topology": topology,
                    "threshold": threshold,
                    "ind_gain": (
                        means["independent"]["redundancy"]
                        - means["independent"]["coexistence"]
                    ),
                    "corr_gain": (
                        means["correlated"]["redundancy"]
                        - means["correlated"]["coexistence"]
                    ),
                    "sub_gap": (
                        means["independent"]["substitution"]
                        - means["independent"]["coexistence"]
                    ),
                    # Post-run diagnostic prompted by P4's falsification.
                    # Not part of the preregistered pass criterion.
                    "red_vs_sub": (
                        means["independent"]["redundancy"]
                        - means["independent"]["substitution"]
                    ),
                    "max_budget_ratio": max_budget,
                })
    return cells


def parameter_sweep(seeds: int = 12) -> dict:
    """Representative sensitivity to transfer loss and total repair budget."""
    n = 32
    topology = "small_world"
    threshold = 0.70
    etas = (0.40, 0.60, 0.75, 1.00)
    budgets = (0.08, 0.12, 0.16)
    eta_gain = {}
    budget_gain = {}

    for eta in etas:
        gains = []
        for seed in range(seeds):
            adj = make_adjacency(n, topology, seed)
            damage = make_damage(seed, n, "independent")
            co = simulate("coexistence", adj, damage, threshold, eta=eta)
            re = simulate("redundancy", adj, damage, threshold, eta=eta)
            gains.append(re.viability - co.viability)
        eta_gain[eta] = float(np.mean(gains))

    for budget in budgets:
        gains = []
        for seed in range(seeds):
            adj = make_adjacency(n, topology, seed)
            damage = make_damage(seed, n, "independent")
            co = simulate(
                "coexistence", adj, damage, threshold, budget=budget
            )
            re = simulate(
                "redundancy", adj, damage, threshold, budget=budget
            )
            gains.append(re.viability - co.viability)
        budget_gain[budget] = float(np.mean(gains))

    return {"eta_gain": eta_gain, "budget_gain": budget_gain}


def summarize(head: dict, cells: list[dict], sweep: dict) -> dict:
    ind = np.array([c["ind_gain"] for c in cells])
    corr = np.array([c["corr_gain"] for c in cells])
    sub = np.array([c["sub_gap"] for c in cells])
    red_vs_sub = np.array([c["red_vs_sub"] for c in cells])
    budget = np.array([c["max_budget_ratio"] for c in cells])
    return {
        "ind_median": float(np.median(ind)),
        "ind_positive_fraction": float(np.mean(ind > 0.0)),
        "corr_median": float(np.median(corr)),
        "sub_nonpositive_fraction": float(np.mean(sub <= 0.0)),
        "red_vs_sub_median": float(np.median(red_vs_sub)),
        "red_over_sub_fraction": float(np.mean(red_vs_sub > 0.0)),
        "max_budget_ratio": float(max(budget.max(), max(head["budget_max"].values()))),
        "eta_all_positive": bool(all(v > 0.0 for v in sweep["eta_gain"].values())),
        "budget_all_positive": bool(
            all(v > 0.0 for v in sweep["budget_gain"].values())
        ),
        "candidate_supported": bool(
            np.median(ind) > 0.0
            and np.mean(ind > 0.0) >= 0.75
            and np.median(corr) < np.median(ind)
            and budget.max() <= 1.0 + 1e-9
            and all(v > 0.0 for v in sweep["eta_gain"].values())
            and all(v > 0.0 for v in sweep["budget_gain"].values())
        ),
    }


def print_summary(head: dict, cells: list[dict], sweep: dict, summary: dict) -> None:
    print("=" * 78)
    print("  BENCHMARK v1.10 — redundancy vs dependency (matched repair budget)")
    print("=" * 78)
    print(f"  headline: N=32 small-world, threshold=.70, seeds={head['seeds']}")
    print("\n  viability after repair")
    print(f"  {'architecture':15s} {'independent':>12s} {'correlated':>12s} "
          f"{'KO-1 cost':>10s} {'KO-2 cost':>10s} {'recovery':>10s}")
    for a in ARCHITECTURES:
        print(
            f"  {a:15s} "
            f"{head['viability']['independent'][a]:12.3f} "
            f"{head['viability']['correlated'][a]:12.3f} "
            f"{head['ko1'][a]:10.3f} "
            f"{head['ko2'][a]:10.3f} "
            f"{head['recovery'][a]:10.1f}"
        )

    print("\n  grid sensitivity (18 cells: N x topology x threshold)")
    print(f"  median redundancy gain, independent : {summary['ind_median']:+.4f}")
    print(f"  cells with positive gain             : "
          f"{summary['ind_positive_fraction']:.1%}")
    print(f"  median redundancy gain, correlated  : {summary['corr_median']:+.4f}")
    print(f"  substitution non-positive cells      : "
          f"{summary['sub_nonpositive_fraction']:.1%}")
    print(f"  redundancy advantage vs substitution: "
          f"{summary['red_vs_sub_median']:+.4f} median, "
          f"{summary['red_over_sub_fraction']:.1%} cells")
    print(f"  maximum budget draw / capacity       : "
          f"{summary['max_budget_ratio']:.6f}")

    print("\n  transfer-efficiency sweep (redundancy gain)")
    for eta, gain in sweep["eta_gain"].items():
        print(f"    eta={eta:4.2f}: {gain:+.4f}")
    print("  repair-budget sweep (redundancy gain)")
    for budget, gain in sweep["budget_gain"].items():
        print(f"    B={budget:4.2f}: {gain:+.4f}")

    print("\n  preregistered candidate criterion: "
          f"{'SUPPORTED' if summary['candidate_supported'] else 'NOT SUPPORTED'}")
    print("  A positive result supports one budget-matched mechanism of mutual")
    print("  support under sparse shocks. It is not a theory of life or consciousness.")


def figure(cells: list[dict], sweep: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7))

    labels = [f"{c['topology']}\nN={c['n']}, v={c['threshold']:.2f}" for c in cells]
    x = np.arange(len(cells))
    axes[0].bar(x - 0.18, [c["ind_gain"] for c in cells], 0.36,
                label="independent shocks")
    axes[0].bar(x + 0.18, [c["corr_gain"] for c in cells], 0.36,
                label="correlated shocks")
    axes[0].axhline(0, color="black", lw=0.8)
    axes[0].set_xticks(x, labels, rotation=90, fontsize=6)
    axes[0].set_ylabel("redundancy viability gain vs coexistence")
    axes[0].set_title("(a) Sensitivity: gain must survive more than one cell")
    axes[0].legend(fontsize=8)

    etas = list(sweep["eta_gain"])
    budgets = list(sweep["budget_gain"])
    axes[1].plot(etas, [sweep["eta_gain"][x] for x in etas], "o-",
                 label="transfer efficiency eta")
    axes[1].plot(budgets, [sweep["budget_gain"][x] for x in budgets], "s-",
                 label="repair budget B")
    axes[1].axhline(0, color="black", lw=0.8)
    axes[1].set_xlabel("eta or B (separate sweeps)")
    axes[1].set_ylabel("redundancy viability gain")
    axes[1].set_title("(b) Cost sensitivity")
    axes[1].legend(fontsize=8)
    axes[1].grid(alpha=0.3)

    fig.suptitle("Benchmark v1.10 — budget-matched redundant support")
    fig.tight_layout()
    out = outdir / "inverse_benchmark_redundancy.png"
    fig.savefig(out, dpi=120)
    return out


def run(seeds: int = 12) -> tuple[dict, list[dict], dict, dict]:
    head = headline_suite(seeds=max(seeds, 20))
    cells = sensitivity_grid(seeds=seeds)
    sweep = parameter_sweep(seeds=max(seeds, 12))
    summary = summarize(head, cells, sweep)
    return head, cells, sweep, summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--save", action="store_true")
    args = ap.parse_args()

    head, cells, sweep, summary = run(args.seeds)
    print_summary(head, cells, sweep, summary)
    if args.save:
        outdir = Path(__file__).resolve().parents[2] / "tools"
        print(f"\n  figure -> {figure(cells, sweep, outdir)}")


if __name__ == "__main__":
    main()
