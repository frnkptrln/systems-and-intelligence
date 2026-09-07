"""Check the coherence floor and finite-size effects using the unchanged TEO model."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
from scipy.special import ndtr

ROOT = Path(__file__).resolve().parents[3]
TEO_PATH = ROOT / "simulation-models/alignment-and-veto/teo-civilization/teo_simulation.py"
BASE_COMMIT = "ef9c5117aaf192c73eff71c587053157bae9334c"
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


def frequency_diagnostics(omega):
    centered = np.sort(omega - np.mean(omega))
    cdf = ndtr(centered)
    n = len(omega)
    return {"frequency_std": float(np.std(omega)),
            "centered_gaussian_cdf_distance": float(max(
                np.max(np.arange(1, n+1)/n - cdf),
                np.max(cdf - np.arange(n)/n)))}


def finite_check(coupling: float, seed: int, *, population: int = 50, tight: bool = False):
    """Same parameters, initial draws and RHS as canonical run(); add diagnostics."""
    teo = teo_model()
    p = teo.Params(K=coupling, seed=seed, N=population)
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
        "N": population, "K": coupling, "seed": seed, "solver_complete": bool(sol.success),
        "solver": solver, "numerically_valid": valid,
        "V1_resources_sampled": v1, "V2_coherence": v2, "V3_substrate_sampled": v3,
        "viable_over_observation": v1 and v2 and v3 and valid,
        "r_initial": float(r[0]), "r_min_sampled": float(np.min(r)),
        "r_final": float(r[-1]), "max_resource_share_sampled": float(np.max(x)),
        "Omega_max_sampled": float(np.max(omega)), "simplex_error": simplex_error,
        "first_downward_crossing": float(crossings[0]) if len(crossings) else None,
        "downward_crossing_count": len(crossings),
    }
    row.update(frequency_diagnostics(p.omega))
    return row


def size_sweep_cells(report):
    return [c for c in report["finite_cells"] if c["K"] == 2.0] + report["larger_N_cells"]


def summarize_sizes(cells):
    rows = []
    for n in (50, 200, 1000):
        group = [c for c in cells if c["N"] == n]
        rows.append({"N": n, "runs": len(group),
                     "coherence_failures": sum(not c["V2_coherence"] for c in group),
                     "r_min_range": [min(c["r_min_sampled"] for c in group),
                                     max(c["r_min_sampled"] for c in group)],
                     "frequency_std_range": [min(c["frequency_std"] for c in group),
                                             max(c["frequency_std"] for c in group)]})
    return rows


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

    plt.rcParams.update({"font.size": 10})
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
    for cell in size_sweep_cells(report):
        # Fixed offsets separate seeds; population sizes are the three ticks.
        position = cell["N"] * np.exp((cell["seed"] - 7.5) * 0.008)
        ax.scatter(position, cell["r_min_sampled"], s=22, alpha=0.8,
                   color=red if not cell["V2_coherence"] else blue)
    ax.axhline(0.5, color="0.3", ls="--", label="required floor = 0.5")
    ax.set(xlabel="Population N (log scale)", ylabel="Minimum sampled r(t), t ≤ 80",
           ylim=(0, 1), xscale="log", xticks=[50, 200, 1000],
           title="C  Gaussian TEO size check (K = 2)")
    ax.set_xticklabels(["50", "200", "1000"])
    ax.minorticks_off()
    ax.text(0.03, 0.95, "Same 16 seeds at each size", transform=ax.transAxes,
            va="top", fontsize=9)
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.15)
    fig.savefig(outdir / "coherence_margin.png", dpi=200)
    plt.close(fig)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_info():
    return {"base_commit": BASE_COMMIT, "runner_sha256": sha256(Path(__file__)),
            "canonical_teo_sha256": sha256(TEO_PATH), "python": platform.python_version(),
            "numpy": np.__version__, "scipy": scipy.__version__}


def write_report(report, path):
    """One row per numerical record; keep metadata indented for inspection."""
    sections = []
    for key, value in report.items():
        if isinstance(value, list):
            body = "[\n" + ",\n".join("    " + json.dumps(row, allow_nan=False)
                                      for row in value) + "\n  ]"
        else:
            body = json.dumps(value, indent=2, allow_nan=False).replace("\n", "\n  ")
        sections.append("  " + json.dumps(key) + ": " + body)
    path.write_text("{\n" + ",\n".join(sections) + "\n}\n")


def run_experiment(outdir: Path, baseline: Path | None = None):
    if baseline is not None:
        report = json.loads(baseline.read_text())
        if sha256(TEO_PATH) != report["provenance"]["canonical_teo_sha256"]:
            raise RuntimeError("Baseline was produced by a different canonical TEO model.")
        report["provenance"] = {"baseline": report["provenance"], "size_sweep": source_info()}
        return add_size_sweep(report, outdir)
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
    params.pop("base_fitness")
    report = {
        "provenance": {"baseline": source_info(), "size_sweep": source_info()},
        "configuration": {"default_parameters": params, "couplings": COUPLINGS,
                          "seeds": list(range(16)), "initial_condition": "x uniform; theta ~ normal(0, .30) from default_rng(seed+1); Omega=0",
                          "sampled_extrema_note": "Extrema and V1/V3 are sampled at 801 times; V2 also checks downward crossing events. No all-time finite-N proof."},
        "scalar_checks": scalar, "thresholds": thresholds,
        "maximum_scalar_error": max_error, "maximum_lorentzian_quadrature_error": quad_error,
        "finite_cells": cells, "validation": validation, "summary": summary,
    }
    return add_size_sweep(report, outdir)


def add_size_sweep(report, outdir):
    configuration = report["configuration"]
    configuration.pop("frequency_draws", None)
    configuration["default_parameters"].pop("base_fitness", None)
    configuration["frequency_generation"] = "default_rng(seed).normal(0, sigma, N); increasing N extends the same draw sequence"
    configuration["size_sweep"] = {"K": 2.0, "populations": [50, 200, 1000], "seeds": list(range(16))}
    configuration["solver"] = {"method": "RK45", "rtol": 1e-7, "atol": 1e-9, "max_step": 0.1}
    configuration["tight_solver"] = {"method": "RK45", "rtol": 1e-10, "atol": 1e-12, "max_step": 0.05}
    for row in report["finite_cells"]:
        row["N"] = 50
        row.update(frequency_diagnostics(teo_model().Params(seed=row["seed"]).omega))
        row.pop("solver", None)
    for validation in report["validation"]:
        validation["tight_run"]["N"] = 50
        validation["tight_run"].pop("solver", None)
    report["larger_N_cells"] = []
    for population in (200, 1000):
        for seed in range(16):
            cell = finite_check(2.0, seed, population=population)
            cell.pop("solver")
            report["larger_N_cells"].append(cell)
        print(f"Completed K=2.0, N={population}, 16 seeds", flush=True)
    report["size_summary"] = summarize_sizes(size_sweep_cells(report))
    # Check the trajectory closest to the floor at each new size under tighter
    # integration; report the selection and the measured differences explicitly.
    report["size_validation"] = []
    for population in (200, 1000):
        original = min((c for c in report["larger_N_cells"] if c["N"] == population),
                       key=lambda c: (abs(c["r_min_sampled"] - 0.5), c["seed"]))
        tight = finite_check(2.0, original["seed"], population=population, tight=True)
        tight.pop("solver")
        report["size_validation"].append({"tight_run": tight,
            "classification_unchanged": original["V2_coherence"] == tight["V2_coherence"],
            "r_min_absolute_change": abs(original["r_min_sampled"] - tight["r_min_sampled"]),
            "r_final_absolute_change": abs(original["r_final"] - tight["r_final"])})
    outdir.mkdir(parents=True, exist_ok=True)
    write_report(report, outdir / "results.json")
    make_figure(report, outdir)
    print(json.dumps({"size_summary": report["size_summary"],
                      "size_validation": report["size_validation"]}, indent=2))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results")
    parser.add_argument("--extend-baseline", type=Path,
                        help="Reuse an original N=50 report and run only the new size checks.")
    args = parser.parse_args()
    run_experiment(args.output, args.extend_baseline)
