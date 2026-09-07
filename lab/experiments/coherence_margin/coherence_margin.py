"""Execute the predeclared coherence-floor checks; leave the TEO model unchanged."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
TEO_PATH = ROOT / "simulation-models/alignment-and-veto/teo-civilization/teo_simulation.py"
BASE_COMMIT = "ef9c5117aaf192c73eff71c587053157bae9334c"
DESIGN_COMMIT = "2856729"
COUPLINGS = (0.8, 1.6, 1.7, 2.0, 3.0)
FLOORS = (0.25, 0.5, 0.75)


@lru_cache(maxsize=1)
def teo_model():
    """Load the canonical implementation from its existing, hyphenated path."""
    spec = importlib.util.spec_from_file_location("coherence_margin_teo", TEO_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def lorentzian_floor(r_min: float, delta: float = 1.0) -> float:
    if not (np.isfinite(delta) and delta > 0 and 0 < r_min < 1):
        raise ValueError("Require delta > 0 and 0 < r_min < 1.")
    return 2 * delta / (1 - r_min**2)


def amplitude_rhs(r, coupling: float, delta: float = 1.0):
    return r * (0.5 * coupling * (1 - r**2) - delta)


def amplitude_exact(t, coupling: float, r0: float, delta: float = 1.0):
    """Solve y' = (K - 2*delta)y - Ky², including onset and r0 = 0."""
    t = np.asarray(t, dtype=float)
    if not (np.isfinite(coupling) and coupling >= 0 and
            np.isfinite(delta) and delta > 0 and 0 <= r0 <= 1 and
            np.all(np.isfinite(t)) and np.all(t >= 0)):
        raise ValueError("Require finite nonnegative time/K, delta > 0, and r0 in [0, 1].")
    if r0 == 0:
        return np.zeros_like(t)
    a, y0 = coupling - 2 * delta, r0**2
    if a == 0:
        y = y0 / (1 + coupling * y0 * t)
    elif a > 0:
        # expm1 retains accuracy close to onset; exponent never overflows.
        y = y0 / (np.exp(-a * t) - coupling * y0 * np.expm1(-a * t) / a)
    else:
        y = y0 * np.exp(a * t) / (1 + coupling * y0 * np.expm1(a * t) / a)
    return np.sqrt(y)


def stationary_floor(r_min: float, density: str, width: float = 1.0) -> float:
    """Quadrature of Appendix A.2; a stationary branch, not a transient bound.

    Parameterize q = K*r, F(q) = integral cos²(phi)*g(q*sin(phi)) dphi.
    Then r = q*F(q), K = 1/F(q); q avoids the incoherent root r = 0.
    """
    if not (0 < r_min < 1 and np.isfinite(width) and width > 0):
        raise ValueError("Require 0 < r_min < 1 and a positive finite width.")
    if density == "gaussian":
        def g(omega):
            return np.exp(-0.5 * (omega / width)**2) / (width * np.sqrt(2 * np.pi))
    elif density == "lorentzian":
        def g(omega):
            return width / (np.pi * (omega**2 + width**2))
    else:
        raise ValueError(f"Unknown density: {density}")

    def integral(q):
        return quad(lambda phi: np.cos(phi)**2 * g(q * np.sin(phi)),
                    -np.pi / 2, np.pi / 2, epsabs=1e-12, epsrel=1e-12)[0]

    upper = width
    for _ in range(60):
        if upper * integral(upper) > r_min:
            break
        upper *= 2
    else:
        raise RuntimeError("Could not bracket the stationary branch.")
    q = brentq(lambda q: q * integral(q) - r_min, 0, upper, xtol=1e-12)
    return float(1 / integral(q))


def scalar_checks():
    t = np.linspace(0, 80, 801)
    rows = []
    for floor in FLOORS:
        threshold = lorentzian_floor(floor)
        for coupling in (1.8, 2.0, 2.2, threshold, 1.05 * threshold):
            for fraction in (0.1, 0.5, 0.9):
                r0 = floor + (1 - floor) * fraction
                sol = solve_ivp(lambda t, r: amplitude_rhs(r, coupling), (0, 80),
                                [r0], t_eval=t, rtol=1e-11, atol=1e-13, max_step=0.1)
                if not sol.success or sol.t.size != t.size:
                    raise RuntimeError(sol.message)
                rows.append({"r_min": floor, "K": coupling, "r0": r0,
                             "boundary_derivative": float(amplitude_rhs(floor, coupling)),
                             "r_final": float(sol.y[0, -1]),
                             "max_exact_error": float(np.max(np.abs(
                                 sol.y[0] - amplitude_exact(t, coupling, r0))))})
    return rows


def finite_check(coupling: float, seed: int, *, tight: bool = False):
    """Same parameters, initial draws and RHS as canonical run(); add diagnostics."""
    teo = teo_model()
    p = teo.Params(K=coupling, seed=seed)
    theta0 = np.random.default_rng(seed + 1).normal(0, 0.30, p.N)
    initial = np.concatenate([np.ones(p.N) / p.N, theta0, [0.0]])

    def downward_crossing(t, state):
        return teo.order_parameter(state[p.N:2 * p.N])[0] - p.r_min

    downward_crossing.direction = -1
    solver = {"method": "RK45", "rtol": 1e-10 if tight else 1e-7,
              "atol": 1e-12 if tight else 1e-9, "max_step": 0.05 if tight else 0.1}
    sol = solve_ivp(teo.make_rhs(p), (0, p.T_end), initial,
                    t_eval=np.linspace(0, p.T_end, p.steps),
                    events=downward_crossing, **solver)
    if not sol.success or sol.t.size != p.steps or not np.all(np.isfinite(sol.y)):
        raise RuntimeError(f"Invalid trajectory K={coupling}, seed={seed}: {sol.message}")
    x, theta, omega = sol.y[:p.N], sol.y[p.N:2*p.N], sol.y[-1]
    r = np.abs(np.mean(np.exp(1j * theta), axis=0))
    simplex_error = float(np.max(np.abs(x.sum(axis=0) - 1)))
    crossings = sol.t_events[0]
    v1 = bool(np.all(x.max(axis=0) <= p.x_crit))
    v2 = bool(np.all(r >= p.r_min) and len(crossings) == 0)
    v3 = bool(np.all(omega < p.S_max))
    valid = bool(simplex_error < 1e-8 and np.min(x) >= -1e-10)
    row = {
        "K": coupling, "seed": seed, "solver_complete": bool(sol.success),
        "solver": solver, "numerically_valid": valid,
        "V1_resources_sampled": v1, "V2_coherence": v2, "V3_substrate_sampled": v3,
        "viable_over_observation": v1 and v2 and v3 and valid,
        "r_initial": float(r[0]), "r_min_sampled": float(np.min(r)),
        "r_final": float(r[-1]), "max_resource_share_sampled": float(np.max(x)),
        "Omega_max_sampled": float(np.max(omega)), "simplex_error": simplex_error,
        "first_downward_crossing": float(crossings[0]) if len(crossings) else None,
        "downward_crossing_count": len(crossings),
    }
    return row


def summarize(cells):
    kc = float(teo_model().kc_gaussian(1.0))
    by_coupling = []
    for coupling in COUPLINGS:
        group = [cell for cell in cells if cell["K"] == coupling]
        by_coupling.append({
            "K": coupling, "runs": len(group),
            "coherence_failures": sum(not c["V2_coherence"] for c in group),
            "isolated_coherence_failures": sum(
                not c["V2_coherence"] and c["V1_resources_sampled"] and
                c["V3_substrate_sampled"] and c["numerically_valid"] for c in group),
            "r_min_range": [min(c["r_min_sampled"] for c in group),
                            max(c["r_min_sampled"] for c in group)],
        })
    return {"gaussian_Kc": kc, "by_coupling": by_coupling,
            "above_onset_isolated_failures": sum(
                row["isolated_coherence_failures"] for row in by_coupling if row["K"] > kc),
            "all_resources_safe": all(c["V1_resources_sampled"] for c in cells),
            "all_substrate_safe": all(c["V3_substrate_sampled"] for c in cells),
            "all_numerically_valid": all(c["numerically_valid"] for c in cells)}


def make_figure(report, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 10, "svg.hashsalt": "coherence-margin"})
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), layout="constrained")
    blue, red, green = "#2166ac", "#b2182b", "#26734d"
    k = np.linspace(2, 4, 401)
    ax = axes[0]
    ax.plot(k, np.sqrt(1 - 2/k), color=blue, lw=2)
    ax.axhline(0.5, color="0.3", ls="--", label="required floor = 0.5")
    ax.axvline(2, color="0.5", ls=":")
    ax.axvline(8/3, color=green, ls=":")
    ax.axvspan(2, 8/3, color=red, alpha=0.12)
    ax.text(2.12, 0.15, "Coherent equilibrium\nbelow required floor", fontsize=9, color=red)
    ax.set(xlim=(1.8, 4), ylim=(0, 1), xlabel="Coupling K", ylabel="Stationary coherence r*",
           title="A  Lorentzian continuum (Δ = 1)")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax = axes[1]
    t = np.linspace(0, 25, 501)
    for coupling, color, label in [(2.2, red, "K = 2.2 (above onset)"),
                                   (8/3, blue, "K = 8/3 (at floor)"),
                                   (3.0, green, "K = 3.0 (positive margin)")]:
        ax.plot(t, amplitude_exact(t, coupling, 0.9), color=color, lw=2, label=label)
    ax.axhline(0.5, color="0.3", ls="--")
    ax.set(xlabel="Time", ylabel="Coherence r(t)", ylim=(0, 1),
           title="B  Exact reduced trajectories")
    ax.legend(loc="lower right", frameon=False, fontsize=8.5)
    ax = axes[2]
    for cell in report["finite_cells"]:
        # Fixed offsets only separate the 16 seeds; actual couplings are the ticks.
        offset = (cell["seed"] - 7.5) * 0.0025
        ax.scatter(cell["K"] + offset, cell["r_min_sampled"], s=22, alpha=0.8,
                   color=red if not cell["V2_coherence"] else blue)
    ax.axhline(0.5, color="0.3", ls="--", label="required floor = 0.5")
    ax.axvline(report["summary"]["gaussian_Kc"], color="0.5", ls=":",
               label="Gaussian continuum onset")
    ax.set(xlabel="Coupling K", ylabel="Minimum sampled r(t), t ≤ 80",
           ylim=(0, 1), xticks=[0.8, 1.6, 2.0, 3.0],
           title="C  Finite Gaussian TEO (N = 50)")
    ax.text(0.03, 0.95, "16 seeds per coupling; 80 runs", transform=ax.transAxes,
            va="top", fontsize=9)
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.15)
    for extension in ("svg", "png"):
        metadata = {"Date": None} if extension == "svg" else {}
        fig.savefig(outdir / f"coherence_margin.{extension}", dpi=200, metadata=metadata)
    plt.close(fig)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_experiment(outdir: Path):
    scalar = scalar_checks()
    thresholds = [{"r_min": floor, "lorentzian_exact": lorentzian_floor(floor),
                   "lorentzian_quadrature": stationary_floor(floor, "lorentzian"),
                   "gaussian_stationary": stationary_floor(floor, "gaussian")}
                  for floor in FLOORS]
    max_error = max(row["max_exact_error"] for row in scalar)
    quad_error = max(abs(row["lorentzian_exact"] - row["lorentzian_quadrature"])
                     for row in thresholds)
    if max_error > 1e-7 or quad_error > 1e-7:
        raise RuntimeError(f"Analytical check failed: {max_error=}, {quad_error=}")
    cells = []
    for coupling in COUPLINGS:
        cells.extend(finite_check(coupling, seed) for seed in range(16))
        print(f"Completed K={coupling}, 16 seeds", flush=True)
    summary = summarize(cells)
    kc = summary["gaussian_Kc"]
    failures = [c for c in cells if c["K"] > kc and not c["V2_coherence"]]
    selected = failures[0] if failures else next(c for c in cells if c["K"] == 1.6)
    validation = []
    for coupling in (selected["K"], 3.0):
        original = next(c for c in cells if (c["K"], c["seed"]) == (coupling, selected["seed"]))
        tight = finite_check(coupling, selected["seed"], tight=True)
        keys = ("V1_resources_sampled", "V2_coherence", "V3_substrate_sampled", "numerically_valid")
        validation.append({"tight_run": tight,
                           "classification_unchanged": all(original[k] == tight[k] for k in keys),
                           "r_min_absolute_change": abs(original["r_min_sampled"] - tight["r_min_sampled"]),
                           "r_final_absolute_change": abs(original["r_final"] - tight["r_final"])})
    params = asdict(teo_model().Params())
    params.pop("omega")
    params["base_fitness"] = params["base_fitness"].tolist()
    report = {
        "provenance": {"base_commit": BASE_COMMIT, "design_commit": DESIGN_COMMIT,
                       "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                       "runner_sha256": sha256(Path(__file__)), "canonical_teo_sha256": sha256(TEO_PATH),
                       "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "configuration": {"default_parameters": params, "couplings": COUPLINGS,
                          "seeds": list(range(16)), "initial_condition": "x uniform; theta ~ normal(0, .30) from default_rng(seed+1); Omega=0",
                          "frequency_draws": {str(seed): teo_model().Params(seed=seed).omega.tolist() for seed in range(16)},
                          "sampled_extrema_note": "Extrema and V1/V3 are sampled at 801 times; V2 also checks downward crossing events. No all-time finite-N proof."},
        "scalar_checks": scalar, "thresholds": thresholds,
        "maximum_scalar_error": max_error, "maximum_lorentzian_quadrature_error": quad_error,
        "finite_cells": cells, "validation": validation, "summary": summary,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "results.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    make_figure(report, outdir)
    print(json.dumps({"summary": summary, "thresholds": thresholds,
                      "maximum_scalar_error": max_error, "validation": validation}, indent=2))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results")
    run_experiment(parser.parse_args().output)
