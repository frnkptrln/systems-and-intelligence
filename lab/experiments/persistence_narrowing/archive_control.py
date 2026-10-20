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


@dataclass
class Totals:
    runs: int = 0
    sums: dict[str, Fraction] = field(default_factory=lambda: {key: Fraction(0) for key in METRICS})

    def add(self, result) -> None:
        self.runs += 1
        for key in METRICS:
            self.sums[key] += getattr(result, key)

    def report(self) -> dict:
        return {
            "runs": self.runs,
            "means": {key: str(value / self.runs) for key, value in self.sums.items()},
        }


def contrasts(totals: dict[str, Totals]) -> dict:
    comparisons = (("fitted", "uniform"), ("fitted", "translated"),
                   ("fitted", "none"), ("uniform", "none"), ("translated", "none"))
    return {
        f"{left}_minus_{right}": {
            key: str(totals[left].sums[key] / totals[left].runs
                     - totals[right].sums[key] / totals[right].runs)
            for key in METRICS
        }
        for left, right in comparisons
    }


def check_block(blocks: dict[str, list]) -> dict:
    """Separate information invariance from visible optimization success.

    Enumerating all targets gives an unbiased half on every unobserved bit.
    Therefore 2H = 2P + 256*8 - T even when visible tests are not saturated.
    The older ceiling identity additionally needs P == T.
    """

    recalls = blocks["fitted"][0].recalls
    paired_recalls = all(
        run.recalls == recalls
        for arm in ("fitted", "uniform", "translated") for run in blocks[arm]
    )
    if not paired_recalls:
        raise AssertionError("archive arms have different realized recall counts")
    checks = {}
    for arm, runs in blocks.items():
        h = sum(run.heldout_correct for run in runs)
        p = sum(run.observed_passed for run in runs)
        t = sum(run.observed_total for run in runs)
        invariant = 2 * h == 2 * p + len(runs) * pn.COORDS - t
        if not invariant:
            raise AssertionError(f"target-independence check failed: {arm}")
        checks[arm] = {
            "information_identity": invariant,
            "visible_saturation": p == t,
            "heldout_correct_sum": h,
            "visible_passed_sum": p,
            "visible_total_sum": t,
        }
    return {"paired_recalls": paired_recalls, "recalls_per_archive_run": recalls, "arms": checks}


def aggregate(seeds: int = 2, rows: int = 8, *, budget: int = pn.BUDGET) -> dict:
    if seeds < 1 or rows < 1 or budget < 0:
        raise ValueError("seeds and rows must be positive; budget must be nonnegative")
    families = {}
    for family in pn.FAMILIES:
        totals = {arm: Totals() for arm in ARMS}
        by_seed = []
        for seed in range(seeds):
            archives, mask = build_archives(family, seed)
            seed_totals = {arm: Totals() for arm in ARMS}
            row_checks = []
            for row in range(rows):
                blocks = {
                    arm: [
                        pn.run_loop(
                            rule, seed, family=family,
                            condition="none" if arm == "none" else "memory",
                            memory=archives["fitted" if arm == "none" else arm],
                            row_index=row, budget=budget,
                        )
                        for rule in range(256)
                    ]
                    for arm in ARMS
                }
                row_checks.append({"row": row, **check_block(blocks)})
                for arm, runs in blocks.items():
                    for run in runs:
                        totals[arm].add(run)
                        seed_totals[arm].add(run)
            audits = {arm: archive_audit(family, bank) for arm, bank in archives.items()}
            by_seed.append({
                "seed": seed,
                "xor_mask": "".join(map(str, mask)),
                "xor_multiset_unchanged": Counter(archives["fitted"]) == Counter(archives["translated"]),
                "archives": audits,
                "arms": {arm: value.report() for arm, value in seed_totals.items()},
                "contrasts": contrasts(seed_totals),
                "row_checks": row_checks,
            })
        families[family] = {
            "arms": {arm: value.report() for arm, value in totals.items()},
            "contrasts": contrasts(totals),
            "by_seed": by_seed,
        }

    source_paths = (Path(__file__), HERE / "persistence_narrowing.py", pn._RB_PATH)
    return {
        "schema": "persistence-archive-control/1",
        "status": "post-hoc fixed-grid control",
        "sources_sha256": {
            path.relative_to(pn.REPO).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in source_paths
        },
        "parameters": {
            "seeds": seeds, "rows": rows, "rules": 256,
            "evaluation_budget": budget, "memory_worlds": pn.MEMORY_WORLDS,
            "p_recall": str(pn.P_RECALL), "families": pn.FAMILIES, "arms": ARMS,
            "evaluation_runs": len(pn.FAMILIES) * len(ARMS) * seeds * rows * 256,
            "prior_fit_proposals_per_fitted_archive": pn.MEMORY_WORLDS * pn.BUDGET,
            "uniform_stream": "archive-control:uniform:{family}:{seed}",
            "xor_stream": "archive-control:xor:{family}:{seed}",
            "uniform_sampling": "independent bits with replacement; order and duplicates retained",
            "translation": "one uniformly drawn nonzero state-space XOR mask per family/seed",
            "pull_reported": False,
        },
        "families": families,
    }


def render_markdown(report: dict) -> str:
    lines = ["# Post-hoc archive controls", "", "| family | arm | observed | heldout | distinct proposals | distinct accepted |",
             "|:---|:---|---:|---:|---:|---:|"]
    for family, results in report["families"].items():
        for arm, result in results["arms"].items():
            means = result["means"]
            values = [f"{float(Fraction(means[key])):.6f}" for key in METRICS[:4]]
            lines.append(f"| {family} | {arm} | " + " | ".join(values) + " |")
    lines.extend(["", "Exact fractional means, per-seed contrasts, archive geometry and row checks are in JSON.",
                  "This fixed grid has only two archive seeds by default. Preparation cost is not matched.",
                  "XOR changes archive location relative to the unchanged zero start and test values."])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=2)
    parser.add_argument("--rows", type=int, default=8)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()
    if args.seeds < 1 or args.rows < 1:
        parser.error("seeds and rows must be positive")
    report = aggregate(args.seeds, args.rows)
    print(json.dumps(report, indent=2, sort_keys=True) if args.format == "json" else render_markdown(report))


if __name__ == "__main__":
    main()
