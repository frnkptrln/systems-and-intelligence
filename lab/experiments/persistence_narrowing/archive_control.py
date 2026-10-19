"""Post-hoc controls for the persistence experiment's proposal archives.

Compare no recall, fitted prior-world artifacts, uniformly drawn artifacts,
and a common XOR translation of the fitted archive. The existing loop and
referee are reused unchanged. All archive arms use the same 16 entry indices,
recall schedule and downstream proposal budget. Preparation work is not matched.

This is a fixed-grid mechanical control, not an LLM or semantic-memory study.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "archive_control_persistence", HERE / "persistence_narrowing.py"
)
assert SPEC and SPEC.loader
pn = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = pn
SPEC.loader.exec_module(pn)

ARMS = ("none", "fitted", "uniform", "translated")
METRICS = ("observed", "heldout", "distinct_proposals", "distinct_accepted", "accepted", "recalls")
Archive = tuple[tuple[int, ...], ...]


def build_archives(family: str, seed: int) -> tuple[dict[str, Archive], tuple[int, ...]]:
    """Build fixed, target-independent banks; preserve order and duplicates."""

    if family not in pn.FAMILIES:
        raise ValueError(f"unknown family: {family}")
    size = pn._state_size(family)
    fitted = pn.build_memory(family, seed)
    uniform_rng = random.Random(f"archive-control:uniform:{family}:{seed}")
    uniform = tuple(
        tuple(uniform_rng.getrandbits(1) for _ in range(size))
        for _ in range(pn.MEMORY_WORLDS)
    )
    shift_rng = random.Random(f"archive-control:xor:{family}:{seed}")
    shift = shift_rng.randrange(1, 1 << size)
    mask = tuple((shift >> bit) & 1 for bit in range(size))
    translated = tuple(tuple(a ^ b for a, b in zip(state, mask)) for state in fitted)
    return {"fitted": fitted, "uniform": uniform, "translated": translated}, mask


def archive_audit(family: str, archive: Archive) -> dict:
    """Expose multiplicities, internal geometry and distance to the zero start."""

    tables = tuple(pn._to_table(family)(state) for state in archive)

    def pair_distances(entries):
        return dict(sorted(Counter(
            pn.hamming(a, b)
            for i, a in enumerate(entries)
            for b in entries[i + 1:]
        ).items()))

    return {
        "entries": ["".join(map(str, state)) for state in archive],
        "multiplicities": dict(sorted(Counter("".join(map(str, s)) for s in archive).items())),
        "unique_states": len(set(archive)),
        "parameter_pair_distances": pair_distances(archive),
        "table_pair_distances": pair_distances(tables),
        "parameter_distance_from_zero": dict(sorted(Counter(sum(s) for s in archive).items())),
    }
