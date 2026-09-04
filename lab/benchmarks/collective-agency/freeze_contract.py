"""Validate the Collective Agency freeze candidate without implementing it."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


EXPECTED_OPTIONS = {
    "system": "1A",
    "macro_state": "2A_with_2B_sweep",
    "prediction": "3A",
    "synergy": "4A_with_4C_correction",
    "intervention": "6A",
    "viability": "7B_with_7A_margin",
}
EXPECTED_CONTROLS = {
    "independent",
    "broadcast",
    "centralized_aggregator",
    "synchronization",
    "random_coupling",
    "capacity_matched",
}
EXPECTED_AXES = {
    "local_prediction",
    "collective_gain",
    "synergy",
    "closure",
    "downward_control",
    "persistence",
    "viability",
}


def load_candidate(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("freeze candidate must be one JSON object")
    return value


def candidate_errors(candidate: dict[str, Any]) -> list[str]:
    """Check that the file faithfully transcribes the documented defaults."""

    errors: list[str] = []
    if candidate.get("version") != "0.1-candidate":
        errors.append("version must be 0.1-candidate")
    if candidate.get("status") != "candidate_requires_pi_decision":
        errors.append("status must remain candidate_requires_pi_decision")
    for section, option in EXPECTED_OPTIONS.items():
        if candidate.get(section, {}).get("option") != option:
            errors.append(f"{section}.option changed from the documented default")
    if candidate.get("closure", {}).get("primary") != "5A_component_versus_rest":
        errors.append("closure primary must be option 5A")
    if candidate.get("closure", {}).get("secondary") != "5B_collective_versus_exogenous_drive":
        errors.append("closure secondary must be option 5B")
    if candidate.get("nulls", {}).get("threshold") != "8A_K_equals_0_max_over_seeds":
        errors.append("null threshold must be option 8A")
    if candidate.get("nulls", {}).get("bias_report") != "8B_surrogate_mean_plus_3sd":
        errors.append("null bias report must be option 8B")
    if set(candidate.get("controls", [])) != EXPECTED_CONTROLS:
        errors.append("required controls changed")
    if set(candidate.get("report_axes", [])) != EXPECTED_AXES:
        errors.append("reporting profile axes changed")
    if candidate.get("nulls", {}).get("seeds_per_cell") != 16:
        errors.append("seed count changed from the documented candidate")
    if candidate.get("nulls", {}).get("base_forward_runs") != 240:
        errors.append("base forward-run count must be 240")
    if candidate.get("implementation_authorized") is not False:
        errors.append("candidate must not authorize implementation")
    if candidate.get("execution_authorized") is not False:
        errors.append("candidate must not authorize execution")
    return errors


def implementation_blockers(candidate: dict[str, Any]) -> list[str]:
    """Return every reason implementation must not start."""

    blockers = candidate_errors(candidate)
    if candidate.get("status") != "frozen_implementation_authorized":
        blockers.append("status is not frozen_implementation_authorized")
    if candidate.get("implementation_authorized") is not True:
        blockers.append("implementation is not authorized")
    if candidate.get("open_questions"):
        blockers.append("maintainer questions remain unresolved")
    if candidate.get("intervention", {}).get("outcome_horizon") in {None, "", "unset"}:
        blockers.append("intervention outcome horizon is unset")
    if candidate.get("viability", {}).get("recovery_epsilon") in {None, "", "unset"}:
        blockers.append("recovery epsilon is unset")
    return blockers
