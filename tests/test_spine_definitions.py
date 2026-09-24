"""Pin the two exact statements of theory/core/spine-formal-definitions.md.

D10 states the effective-goal-space monotonicity lemma (R1 subset of R2
implies the equivalence under R2 is contained in the equivalence under R1).
D12 states a proposition about component-irreducibility and lumpability and
proves it with the parity control's three update rules. Both are elementary;
this suite exists so that the note's figures are recomputed, not remembered.
"""

import importlib.util
import itertools
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "lab" / "experiments" / "collective-agency-control" / "run_control.py"
SPEC = importlib.util.spec_from_file_location("collective_agency_control_for_spine", CONTROL)
CONTROL_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTROL_MODULE)


# --- D10: the monotonicity lemma on a small instance ------------------------

def goal_classes(goals, reachable, lens):
    """Partition ``goals`` by equality of ``g(lens(gamma))`` over ``reachable``."""
    classes = {}
    for name, goal in goals.items():
        signature = tuple(goal(lens(gamma)) for gamma in reachable)
        classes.setdefault(signature, set()).add(name)
    return {frozenset(members) for members in classes.values()}


def refines(fine, coarse):
    """Every block of ``fine`` lies inside some block of ``coarse``."""
    return all(any(block <= other for other in coarse) for block in fine)


def test_monotonicity_lemma_on_a_finite_instance():
    # Trajectories are words over {a, b}; the lens records the letter counts.
    lens = lambda gamma: (gamma.count("a"), gamma.count("b"))
    goals = {
        "count_a": lambda rec: rec[0],
        "count_b": lambda rec: rec[1],
        "total": lambda rec: rec[0] + rec[1],
        "parity_a": lambda rec: rec[0] % 2,
        "twice_a": lambda rec: 2 * rec[0],
    }
    # Under the restricted body every reachable trajectory has as many a's as
    # b's, so 'count_a' and 'count_b' coincide, as do 'total' and 'twice_a'.
    r1 = ["ab", "aabb"]
    r2 = r1 + ["a", "abb"]               # a released constraint: strictly more reachable
    assert set(r1) <= set(r2)

    classes_1 = goal_classes(goals, r1, lens)
    classes_2 = goal_classes(goals, r2, lens)

    # Relation containment: goals equivalent under R2 are equivalent under R1,
    # so the R2 partition refines the R1 partition and has at least as many blocks.
    for block in classes_2:
        assert any(block <= other for other in classes_1)
    assert refines(classes_2, classes_1)
    assert len(classes_1) <= len(classes_2)

    # The instance is chosen so the refinement is strict: 3 classes become 5.
    assert classes_1 == {
        frozenset({"count_a", "count_b"}),
        frozenset({"total", "twice_a"}),
        frozenset({"parity_a"}),
    }
    assert len(classes_2) == 5


# --- D12: irreducibility and lumpability on the parity control ---------------

STATES = list(itertools.product((0, 1), repeat=6))


def is_first_integral(reading, update):
    return sum(reading(update(s)) == reading(s) for s in STATES)


def is_lumping(reading, update):
    """``reading(update(s))`` is a function of ``reading(s)`` alone."""
    table = {}
    for state in STATES:
        current, successor = reading(state), reading(update(state))
        if table.setdefault(current, successor) != successor:
            return False
    return True


EXPECTED = {
    # update: (off-diagonal edges, largest SCC, maj conserved, rep conserved, image size)
    "uncoupled_toggle": (0, 1, 64, 64, 64),
    "local_repair": (12, 3, 64, 40, 4),
    "cross_group_repair": (18, 6, 64, 40, 4),
}


@pytest.mark.parametrize("name", sorted(EXPECTED))
def test_worked_example_table(name):
    update = CONTROL_MODULE.UPDATES[name]
    majority = CONTROL_MODULE.READINGS["majority_parity"]
    representative = CONTROL_MODULE.READINGS["representative_parity"]
    edges, component, maj_conserved, rep_conserved, image = EXPECTED[name]

    graph = CONTROL_MODULE.causal_graph(update)
    assert graph["off_diagonal_edges"] == edges
    assert graph["largest_strongly_connected_component"] == component
    assert is_first_integral(majority, update) == maj_conserved
    assert is_first_integral(representative, update) == rep_conserved
    assert len({update(s) for s in STATES}) == image


def test_proposition_parts_a_b_c():
    cross = CONTROL_MODULE.UPDATES["cross_group_repair"]
    toggle = CONTROL_MODULE.UPDATES["uncoupled_toggle"]
    local = CONTROL_MODULE.UPDATES["local_repair"]
    majority = CONTROL_MODULE.READINGS["majority_parity"]
    representative = CONTROL_MODULE.READINGS["representative_parity"]

    # (a) component-irreducible with a non-constant first integral
    assert CONTROL_MODULE.causal_graph(cross)["largest_strongly_connected_component"] == 6
    assert is_first_integral(majority, cross) == 64
    assert len({majority(s) for s in STATES}) == 2
    assert is_lumping(majority, cross)

    # (b) the same first integral on a system with no causal edges
    assert CONTROL_MODULE.causal_graph(toggle)["off_diagonal_edges"] == 0
    assert is_first_integral(majority, toggle) == 64

    # (c) conserved on the codewords, not on X, and not a lumping
    for update in (cross, local):
        assert all(representative(update(s)) == representative(s) for s in CONTROL_MODULE.HEALTHY)
        assert is_first_integral(representative, update) == 40
        assert not is_lumping(representative, update)
