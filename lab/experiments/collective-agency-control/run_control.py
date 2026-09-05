"""Enumerate the parity control defined in the adjacent README; no dependencies."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import product
import json
from math import log2
from pathlib import Path


STATES = tuple(product((0, 1), repeat=6))
HEALTHY = tuple((a,) * 3 + (b,) * 3 for a, b in product((0, 1), repeat=2))


def majority(bits):
    return int(sum(bits) >= 2)


def uncoupled_toggle(state):
    return tuple(1 - bit for bit in state)


def local_repair(state):
    return (1 - majority(state[:3]),) * 3 + (1 - majority(state[3:]),) * 3


def cross_group_repair(state):
    return (1 - majority(state[3:]),) * 3 + (1 - majority(state[:3]),) * 3


UPDATES = {
    "uncoupled_toggle": uncoupled_toggle,
    "local_repair": local_repair,
    "cross_group_repair": cross_group_repair,
}
READINGS = {
    "representative_parity": lambda state: state[0] ^ state[3],
    "majority_parity": lambda state: majority(state[:3]) ^ majority(state[3:]),
}


def entropy(values):
    counts = Counter(values)
    total = sum(counts.values())
    return -sum((n / total) * log2(n / total) for n in counts.values())


def mutual_information(left, right):
    return entropy(left) + entropy(right) - entropy(tuple(zip(left, right)))


def flip(state, index):
    return state[:index] + (1 - state[index],) + state[index + 1:]


def causal_graph(update):
    """Input -> output edges: a single-input change matters somewhere in 64 states."""
    transitions = {state: update(state) for state in STATES}
    edges = sorted({
        (source, target)
        for state in STATES
        for source in range(6)
        for target in range(6)
        if transitions[state][target] != transitions[flip(state, source)][target]
    })
    reachable = [[i == j or (i, j) in edges for j in range(6)] for i in range(6)]
    for via in range(6):
        for source in range(6):
            for target in range(6):
                reachable[source][target] |= reachable[source][via] and reachable[via][target]
    largest = max(sum(reachable[i][j] and reachable[j][i] for j in range(6)) for i in range(6))
    return {
        "edges": [list(edge) for edge in edges],
        "off_diagonal_edges": sum(i != j for i, j in edges),
        "largest_strongly_connected_component": largest,
    }


def measure(update):
    successors = tuple(update(state) for state in HEALTHY)
    sources = [tuple(state[part] for state in HEALTHY) for part in (slice(0, 3), slice(3, 6))]
    local_uncertainty = []
    for index in range(6):
        current = tuple(state[index] for state in HEALTHY)
        future = tuple(state[index] for state in successors)
        local_uncertainty.append(entropy(tuple(zip(current, future))) - entropy(current))

    interventions = [
        (update(state), update(flip(state, bit)))
        for state in HEALTHY for bit in range(6)
    ]
    metrics = {}
    for name, reading in READINGS.items():
        current = tuple(map(reading, HEALTHY))
        future = tuple(map(reading, successors))
        metrics[name] = {
            "next_macro_entropy_bits": entropy(future),
            "triplet_information_bits": [mutual_information(source, future) for source in sources],
            "joint_information_bits": mutual_information(HEALTHY, future),
            "macro_temporal_information_bits": mutual_information(current, future),
            "macro_preserved_after_error": sum(reading(clean) == reading(disturbed) for clean, disturbed in interventions),
        }
    return {
        "mean_local_next_bit_conditional_entropy_bits": sum(local_uncertainty) / 6,
        "state_restored_after_error": sum(clean == disturbed for clean, disturbed in interventions),
        "interventions": len(interventions),
        "readings": metrics,
        "causal_graph": causal_graph(update),
    }


def run():
    return {
        "description": "Exact-distribution parity control; constructive example, not an agency benchmark result.",
        "initial_states": [list(state) for state in HEALTHY],
        "initial_state_probability": "1/4",
        "initial_entropy_bits": entropy(HEALTHY),
        "states_enumerated_per_causal_graph": len(STATES),
        "perturbation": "One transient bit flip before one update, compared with the unperturbed successor.",
        "models": {name: measure(update) for name, update in UPDATES.items()},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("model | off-diagonal edges | largest SCC | state repair | representative | majority")
    for name, data in result["models"].items():
        graph = data["causal_graph"]
        readings = data["readings"]
        print(f"{name} | {graph['off_diagonal_edges']} | {graph['largest_strongly_connected_component']} | "
              f"{data['state_restored_after_error']}/24 | "
              f"{readings['representative_parity']['macro_preserved_after_error']}/24 | "
              f"{readings['majority_parity']['macro_preserved_after_error']}/24")


if __name__ == "__main__":
    main()
