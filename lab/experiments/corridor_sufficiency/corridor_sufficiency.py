"""Closed-form thresholds for the finite-N viable corridor, with numerical controls.

Companion to lab/experiments/corridor_sufficiency/README.md. The functions in
the first half are the formulas of that note; the second half checks them
against the unchanged canonical TEO right-hand side.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, replace
from functools import lru_cache
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parents[3]
TEO_PATH = ROOT / "simulation-models/alignment-and-veto/teo-civilization/teo_simulation.py"


@lru_cache(maxsize=1)
def teo_model():
    """Load the canonical implementation from its existing, hyphenated path."""
    spec = importlib.util.spec_from_file_location("corridor_sufficiency_teo", TEO_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# ───────────────────── Resource axis (Propositions 2–4) ─────────────────────
def gamma_low(delta, N, x_reg, x_crit):
    """Brake strength below which the dominant share must cross x_crit (H = 1)."""
    return x_crit * (1 - x_crit) * delta / ((x_crit - x_reg) * (1 - 1 / N))


def excess_max(c, x_reg):
    """Largest total excess sum_j (x_j - x_reg)_+ on the simplex with max_j x_j = c.

    A convex function on the capped simplex is maximal at a vertex: floor(1/c)
    shares equal to c, one share holding the remainder. Assumes N > floor(1/c).
    """
    k = math.floor(1 / c + 1e-12)
    return k * (c - x_reg) + max(0.0, 1 - k * c - x_reg)


def gamma_full(spread, N, x_reg, x_crit):
    """Brake strength above which the whole pluralism region {max x < x_crit} is invariant."""
    return x_crit * (1 - x_crit) * spread / ((x_crit - x_reg) - excess_max(x_crit, x_reg) / N)


def gamma_up(spread, N, x_reg, x_crit):
    """Closed-form over-estimate of gamma_full, from excess_max(c) <= (c - x_reg)/c."""
    return x_crit * (1 - x_crit) * spread / ((x_crit - x_reg) * (1 - 1 / (N * x_crit)))


def y_star(gamma, delta, N, x_reg, health=1.0):
    """Equilibrium dominant share: health*delta*y(1-y) = gamma(1-1/N)(y - x_reg)."""
    g, d = gamma * (1 - 1 / N), health * delta
    if g == 0:
        return 1.0
    return ((d - g) + math.sqrt((g - d) ** 2 + 4 * d * g * x_reg)) / (2 * d)


def d_low(gamma, delta, N, x_reg, eta=1.0, f_base=1.0):
    """Smallest ceiling that leaves the substrate untouched: throughput at y_star."""
    return eta * (f_base + delta * y_star(gamma, delta, N, x_reg))


def d_floor(delta, x_reg, eta=1.0, f_base=1.0):
    """Ceiling below which the veto is unavoidable in the two-level family."""
    return eta * (f_base + delta * x_reg)


def health_limit(D_max, gamma, delta, N, x_reg, eta=1.0, f_base=1.0):
    """Substrate health at the damage-stabilised equilibrium (printed model).

    Throughput equals D_max at y_D; the unscaled brake balances the scaled
    drift there at H = gamma(1-1/N)(y_D - x_reg) / (delta*y_D*(1-y_D)).
    """
    y_d = (D_max / eta - f_base) / delta
    return gamma * (1 - 1 / N) * (y_d - x_reg) / (delta * y_d * (1 - y_d))


def delta_concentration(gamma, N, x_reg, x_crit):
    """Capability at which gamma_low(delta) reaches gamma."""
    return gamma * (1 - 1 / N) * (x_crit - x_reg) / (x_crit * (1 - x_crit))


def delta_substrate(gamma, D_max, N, x_reg, eta=1.0, f_base=1.0):
    """Capability at which d_low(gamma, delta) reaches D_max."""
    a, g = D_max / eta - f_base, gamma * (1 - 1 / N)
    return a * (a + g) / (a + g * x_reg)


# ───────────────────── Coherence axis (Propositions 5–6) ────────────────────
def centred(omega):
    omega = np.asarray(omega, dtype=float)
    return omega - omega.mean()


def coupling_of_u(nu, u):
    """K(u) = N u / sum_i sqrt(1 - nu_i²/u²): the coupling whose locked state has K r = u."""
    return len(nu) * u / np.sum(np.sqrt(np.clip(1 - (nu / u) ** 2, 0, None)))


def stability_sum(nu, u):
    """S(u) = sum_i (1 - 2 s_i²)/sqrt(1 - s_i²), s_i = nu_i/u; positive iff the state is a minimum."""
    s2 = (nu / u) ** 2
    return float(np.sum((1 - 2 * s2) / np.sqrt(1 - s2)))


def lock_threshold(omega):
    """Exact finite-N locking threshold K_lock = min_u K(u), attained where S(u_s) = 0."""
    nu = centred(omega)
    nu_max = float(np.abs(nu).max())
    if nu_max == 0:
        return {"K_lock": 0.0, "u_s": 0.0, "r_at_threshold": 1.0}
    lo, hi = nu_max * (1 + 1e-12), 2 * nu_max
    while stability_sum(nu, hi) <= 0:
        hi *= 2
    u_s = brentq(lambda u: stability_sum(nu, u), lo, hi, xtol=1e-14, rtol=1e-14)
    k_lock = float(coupling_of_u(nu, u_s))
    return {"K_lock": k_lock, "u_s": float(u_s), "r_at_threshold": float(u_s / k_lock)}


def locked_state(omega, K):
    """The stable locked state at coupling K > K_lock: (u, r, phases in the co-rotating frame)."""
    nu = centred(omega)
    thr = lock_threshold(omega)
    if K <= thr["K_lock"]:
        raise ValueError("No stable locked state at or below K_lock.")
    hi = max(2 * thr["u_s"], 1.0)
    while coupling_of_u(nu, hi) < K:
        hi *= 2
    u = brentq(lambda v: coupling_of_u(nu, v) - K, thr["u_s"], hi, xtol=1e-14, rtol=1e-14)
    return float(u), float(u / K), np.arcsin(nu / u)


def floor_coupling(omega, r_min):
    """Smallest coupling whose stable locked state has r >= r_min (>= K_lock)."""
    nu = centred(omega)
    thr = lock_threshold(omega)
    if thr["r_at_threshold"] >= r_min:
        return thr["K_lock"]
    coherence = lambda u: np.mean(np.sqrt(1 - (nu / u) ** 2)) - r_min
    hi = 2 * thr["u_s"]
    while coherence(hi) < 0:
        hi *= 2
    return float(coupling_of_u(nu, brentq(coherence, thr["u_s"], hi, xtol=1e-14)))


def potential_hessian(phi, K):
    """Hessian of U(phi) = -sum nu_i phi_i - (K/2N) sum_ij cos(phi_i - phi_j)."""
    c = np.cos(phi[:, None] - phi[None, :]) * K / len(phi)
    np.fill_diagonal(c, 0)
    return np.diag(c.sum(axis=1)) - c


def _arc_optimum(p, r_min):
    """Half-arc a maximising G(a) = 2 sin a (p cos a - q) under p cos a - q >= r_min."""
    q = 1 - p
    if p - q < r_min or p - q <= 0:
        return None
    a_opt = math.acos((q + math.sqrt(q * q + 8 * p * p)) / (4 * p))
    a = min(a_opt, math.acos(min(1.0, (r_min + q) / p)))
    gain = 2 * math.sin(a) * (p * math.cos(a) - q)
    return (a, gain) if gain > 0 else None


def arc_threshold(omega, r_min):
    """Smallest K certified by the cluster-arc condition for a realised frequency vector."""
    w = np.sort(np.asarray(omega, dtype=float))
    n, best = len(w), None
    for m in range(1, n + 1):
        opt = _arc_optimum(m / n, r_min)
        if opt is None:
            continue
        widths = w[m - 1:] - w[:n - m + 1]
        start = int(np.argmin(widths))
        k = float(widths[start] / opt[1])
        if best is None or k < best["K_arc"]:
            best = {"K_arc": k, "cluster_size": m, "cluster_start": start,
                    "half_arc": opt[0], "width": float(widths[start]),
                    "coherence_bound": m / n * math.cos(opt[0]) - (1 - m / n)}
    return best


def arc_threshold_density(mass, r_min, c_max=60.0):
    """Population version: mass(c) = P(|omega| <= c) for a symmetric density."""
    def needed(c):
        opt = _arc_optimum(mass(c), r_min)
        return math.inf if opt is None else 2 * c / opt[1]
    grid = np.linspace(1e-3, c_max, 6000)
    values = [needed(c) for c in grid]
    i = int(np.argmin(values))
    res = minimize_scalar(needed, bounds=(grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]),
                          method="bounded", options={"xatol": 1e-10})
    return float(min(res.fun, values[i]))


# ───────────────────────────── Numerical controls ───────────────────────────
def integrate(p, x0, theta0, t_end, rtol=1e-9, atol=1e-11, max_step=0.05):
    """Integrate the canonical right-hand side from an arbitrary initial condition."""
    sol = solve_ivp(teo_model().make_rhs(p), (0.0, t_end),
                    np.concatenate([x0, theta0, [0.0]]),
                    method="RK45", rtol=rtol, atol=atol, max_step=max_step)
    if not sol.success:
        raise RuntimeError(sol.message)
    n = p.N
    x, theta, overshoot = sol.y[:n], sol.y[n:2 * n], sol.y[2 * n]
    return {"t": sol.t, "x": x, "theta": theta, "Omega": overshoot,
            "r": np.abs(np.exp(1j * theta).mean(axis=0))}


def closed_form_rows():
    """Closed forms against the canonical runner, on the paper's own parameter rows."""
    teo = teo_model()
    rows = []
    for label, gamma, delta, d_max in (("C.1 (a) in-corridor", 1.5, 0.3, 1.5),
                                       ("C.4 baseline, delta=2", 1.5, 2.0, 1e9),
                                       ("C.4 regulation only", 6.0, 2.0, 1e9),
                                       ("C.2 gamma=0.6", 0.6, 0.3, 1.5)):
        p = replace(teo.Params(), gamma=gamma, delta=delta, D_max=d_max, T_end=200.0, steps=2001)
        res = teo.run(p)
        _, r_lock, _ = locked_state(p.omega, p.K)
        rows.append({"row": label, "gamma": gamma, "delta": delta,
                     "y_star": y_star(gamma, delta, p.N, p.x_reg),
                     "max_x_simulated": float(res.max_x[-1]),
                     "throughput_formula": d_low(gamma, delta, p.N, p.x_reg, p.eta),
                     "throughput_simulated": float(res.S_dot[-1]),
                     "r_lock": r_lock, "r_simulated": float(res.r[-1])})
    return rows


def resource_threshold_rows():
    """Symmetric starts bracket gamma_low; two-leader starts bracket gamma_full."""
    teo = teo_model()
    base = teo.Params()
    n, x_reg, x_crit = base.N, base.x_reg, base.x_crit
    low = gamma_low(base.delta, n, x_reg, x_crit)
    full = gamma_full(base.delta, n, x_reg, x_crit)
    rows = []
    for factor in (0.99, 0.999, 1.001, 1.01):
        p = replace(base, gamma=low * factor)
        out = integrate(p, np.ones(n) / n, np.zeros(n), 400.0, rtol=1e-8, atol=1e-10, max_step=0.1)
        rows.append({"start": "uniform shares", "gamma": p.gamma, "gamma_over_gamma_low": factor,
                     "sup_max_x_minus_x_crit": float(out["x"].max() - x_crit)})
    eps = 1e-7
    for factor in (0.985, 0.998, 1.002, 1.01):
        p = replace(base, gamma=full * factor)
        x0 = np.full(n, (1 - 2 * (x_crit - eps)) / (n - 2))
        x0[:2] = x_crit - eps
        out = integrate(p, x0, np.zeros(n), 60.0, rtol=1e-11, atol=1e-13)
        rows.append({"start": "two shares at x_crit - 1e-7", "gamma": p.gamma,
                     "gamma_over_gamma_full": factor,
                     "sup_max_x_minus_x_crit": float(out["x"].max() - x_crit)})
    return rows


def _sample_pluralism(rng, n, x_crit):
    """Shares with max < x_crit, from spread-out to two-leader configurations."""
    while True:
        kind = rng.integers(3)
        if kind == 0:
            x = rng.dirichlet(np.full(n, rng.choice([0.05, 0.3, 1.0, 5.0])))
        elif kind == 1:
            x = rng.dirichlet(np.ones(n)) * 0.2
            leaders = rng.choice(n, size=2, replace=False)
            x[leaders] += 0.4
            x /= x.sum()
        else:
            x = np.full(n, 1e-3)
            x[rng.choice(n, size=3, replace=False)] = rng.uniform(0.2, x_crit, 3)
            x /= x.sum()
        if x.max() < x_crit and x.min() > 0:
            return x


def open_set_rows(samples=200):
    """Sample each invariant set of the note and record the worst margins."""
    teo = teo_model()
    base = teo.Params()
    n, rng = base.N, np.random.default_rng(20261115)
    rows = []

    # Theorem 2 with the locked-state clause, canonical parameters.
    _, r_lock, phi = locked_state(base.omega, base.K)
    worst = {"max_x": 0.0, "r": 1.0, "Omega": 0.0}
    for _ in range(samples):
        out = integrate(base, _sample_pluralism(rng, n, base.x_crit),
                        phi + rng.normal(0, 0.2, n), 60.0, rtol=1e-8, atol=1e-10, max_step=0.1)
        worst = {"max_x": max(worst["max_x"], float(out["x"].max())),
                 "r": min(worst["r"], float(out["r"].min())),
                 "Omega": max(worst["Omega"], float(out["Omega"].max()))}
    rows.append({"set": "Theorem 2, locked-state clause", "gamma": base.gamma, "K": base.K,
                 "samples": samples, "phase_perturbation_sd": 0.2, "r_lock": r_lock,
                 "sup_max_x": worst["max_x"], "inf_r": worst["r"], "sup_Omega": worst["Omega"],
                 "violations": int(worst["max_x"] >= base.x_crit or worst["r"] < base.r_min
                                   or worst["Omega"] > 0)})

    # Theorem 2 with the cluster-arc clause: cluster on an arc, the rest anywhere.
    arc = arc_threshold(base.omega, base.r_min)
    p = replace(base, K=1.03 * arc["K_arc"])
    order = np.argsort(base.omega)
    cluster = order[arc["cluster_start"]:arc["cluster_start"] + arc["cluster_size"]]
    outside = np.setdiff1d(np.arange(n), cluster)
    worst = {"max_x": 0.0, "r": 1.0, "arc": 0.0, "Omega": 0.0}
    for k in range(samples):
        theta0 = np.empty(n)
        centre = rng.uniform(0, 2 * np.pi)
        theta0[cluster] = centre + rng.uniform(-1, 1, cluster.size) * arc["half_arc"] * 0.999
        if k % 2:      # worst case of the proof: the cluster on the arc's ends, the rest opposite
            theta0[cluster] = centre + rng.choice([-1, 1], cluster.size) * arc["half_arc"] * 0.999
            theta0[outside] = centre + np.pi
        else:
            theta0[outside] = rng.uniform(0, 2 * np.pi, outside.size)
        out = integrate(p, _sample_pluralism(rng, n, base.x_crit), theta0, 60.0,
                        rtol=1e-8, atol=1e-10, max_step=0.1)
        worst = {"max_x": max(worst["max_x"], float(out["x"].max())),
                 "r": min(worst["r"], float(out["r"].min())),
                 "arc": max(worst["arc"], float(np.ptp(out["theta"][cluster], axis=0).max())),
                 "Omega": max(worst["Omega"], float(out["Omega"].max()))}
    rows.append({"set": "Theorem 2, cluster-arc clause", "gamma": p.gamma, "K": p.K,
                 "samples": samples, "cluster_size": arc["cluster_size"],
                 "arc_limit": 2 * arc["half_arc"], "coherence_bound": arc["coherence_bound"],
                 "sup_max_x": worst["max_x"], "inf_r": worst["r"], "sup_arc": worst["arc"],
                 "sup_Omega": worst["Omega"],
                 "violations": int(worst["max_x"] >= base.x_crit or worst["Omega"] > 0
                                   or worst["r"] < arc["coherence_bound"]
                                   or worst["arc"] >= 2 * arc["half_arc"])})

    # Theorem 3: just above gamma_low the smaller set {x_1 < y*, others < x_reg} is invariant.
    p = replace(base, gamma=1.002 * gamma_low(base.delta, n, base.x_reg, base.x_crit))
    target = y_star(p.gamma, p.delta, n, p.x_reg)
    worst = {"x_1": 0.0, "others": 0.0, "Omega": 0.0}
    for _ in range(samples):
        while True:
            x0 = rng.dirichlet(np.full(n - 1, rng.choice([0.2, 1.0, 5.0])))
            lead = rng.uniform(0.0, target) * rng.choice([1.0, 0.999999])
            x0 = np.concatenate([[lead], (1 - lead) * x0])
            if x0[1:].max() < p.x_reg and x0.min() > 0:
                break
        out = integrate(p, x0, phi.copy(), 300.0, rtol=1e-8, atol=1e-10, max_step=0.1)
        worst = {"x_1": max(worst["x_1"], float(out["x"][0].max())),
                 "others": max(worst["others"], float(out["x"][1:].max())),
                 "Omega": max(worst["Omega"], float(out["Omega"].max()))}
    rows.append({"set": "Theorem 3, {x_1 < y*, others < x_reg}", "gamma": p.gamma, "K": p.K,
                 "samples": samples, "y_star": target, "sup_x_1": worst["x_1"],
                 "sup_other_share": worst["others"], "sup_Omega": worst["Omega"],
                 # x_1 approaches y* from below and meets it only in floating point.
                 "violations": int(worst["x_1"] > target + 1e-9 or worst["others"] >= p.x_reg
                                   or worst["Omega"] > 0)})
    return rows


def classify(p, t_end=1500.0):
    """Run the paper's standard start and report what the substrate did."""
    res = teo_model().run(replace(p, T_end=t_end, steps=int(t_end) + 1))
    tail = res.Omega[-1] - res.Omega[int(0.8 * len(res.Omega))]
    pluralism = bool(np.all(res.max_x <= p.x_crit))
    if not pluralism:
        outcome = "concentration"
    elif res.Omega[-1] == 0:
        outcome = "untouched"
    elif res.H[-1] > 0 and tail < 1e-3 * p.S_max:
        outcome = "damage-stabilised"
    elif res.H[-1] == 0:
        outcome = "veto"
    else:
        outcome = "unsettled"
    return {"outcome": outcome, "H_final": float(res.H[-1]), "max_x_final": float(res.max_x[-1]),
            "sup_max_x": float(res.max_x.max()), "r_min_sampled": float(res.r.min()),
            "throughput_final": float(res.S_dot[-1])}


def damage_rows():
    """The damage-stabilised window of the printed model, and its closure when the brake scales."""
    teo = teo_model()
    rows = []
    for gamma, delta, d_max in ((6.0, 2.0, 1.70), (6.0, 2.0, 1.65), (6.0, 2.0, 1.61),
                                (6.0, 2.0, 1.59), (1.5, 0.3, 1.100), (1.5, 0.3, 1.085)):
        base = replace(teo.Params(), gamma=gamma, delta=delta, D_max=d_max)
        printed = classify(base, 3000.0)
        scaled = classify(replace(base, brake_couples_to_H=True), 3000.0)
        inside = d_floor(delta, base.x_reg) < d_max < d_low(gamma, delta, base.N, base.x_reg)
        rows.append({"gamma": gamma, "delta": delta, "D_max": d_max,
                     "D_floor": d_floor(delta, base.x_reg),
                     "D_low": d_low(gamma, delta, base.N, base.x_reg), "inside_window": inside,
                     "H_predicted": health_limit(d_max, gamma, delta, base.N, base.x_reg) if inside else 0.0,
                     "printed_model": printed, "brake_scaled_by_H": scaled})
    return rows


def plane_rows(delta=2.0):
    """(gamma, D_max) grid at fixed capability, against what the note proves for each cell."""
    teo = teo_model()
    base = replace(teo.Params(), delta=delta)
    n, x_reg, x_crit = base.N, base.x_reg, base.x_crit
    low = gamma_low(delta, n, x_reg, x_crit)
    rows = []
    for gamma in np.round(np.linspace(1.0, 9.0, 9), 6):
        for d_max in np.round(np.linspace(1.45, 2.25, 9), 6):
            if gamma >= low and d_max >= d_low(gamma, delta, n, x_reg):
                claim = "viable, substrate untouched"       # Theorem 3
            elif d_max < d_floor(delta, x_reg):
                claim = "not viable"                        # Proposition 4
            elif gamma < low and d_max >= base.eta * (1 + delta * x_crit):
                claim = "not viable"                        # Proposition 3
            else:
                claim = "none"                              # between D_floor and D_low: computed only
            cell = classify(replace(base, gamma=float(gamma), D_max=float(d_max)))
            cell["viable"] = cell["outcome"] in ("untouched", "damage-stabilised")
            agrees = {"viable, substrate untouched": cell["outcome"] == "untouched",
                      "not viable": not cell["viable"], "none": None}[claim]
            rows.append({"gamma": float(gamma), "D_max": float(d_max), "proved": claim,
                         "simulation_agrees": agrees, **cell})
    return rows


def coherence_rows():
    """Finite-N coherence thresholds across frequency draws, beside the continuum references."""
    teo = teo_model()
    rows = []
    for population in (50, 200, 1000):
        for seed in range(16):
            omega = teo.Params(seed=seed, N=population).omega
            lock, arc = lock_threshold(omega), arc_threshold(omega, 0.5)
            rows.append({"N": population, "seed": seed, "K_lock": lock["K_lock"],
                         "r_at_threshold": lock["r_at_threshold"],
                         "K_floor_0.5": floor_coupling(omega, 0.5), "K_arc_0.5": arc["K_arc"],
                         "arc_cluster_fraction": arc["cluster_size"] / population})
    return rows


def coherence_scan(seed=7):
    """Minimum sampled coherence from the paper's standard start, across K (illustration)."""
    teo = teo_model()
    rows = []
    for coupling in np.round(np.arange(1.4, 4.01, 0.2), 6):
        res = teo.run(replace(teo.Params(seed=seed), K=float(coupling), T_end=300.0, steps=3001))
        rows.append({"K": float(coupling), "r_min_sampled": float(res.r.min()),
                     "r_final": float(res.r[-1])})
    return rows


def thresholds():
    teo = teo_model()
    p = teo.Params()
    n = p.N
    gauss = lambda c: math.erf(c / math.sqrt(2))
    lorentz = lambda c: 2 / math.pi * math.atan(c)
    return {
        "gamma_low": gamma_low(p.delta, n, p.x_reg, p.x_crit),
        "gamma_full": gamma_full(p.delta, n, p.x_reg, p.x_crit),
        "gamma_up": gamma_up(p.delta, n, p.x_reg, p.x_crit),
        "eq9_estimate": p.x_crit * (1 - p.x_crit) * p.delta / (p.x_crit - p.x_reg),
        "y_star_canonical": y_star(p.gamma, p.delta, n, p.x_reg),
        "D_low_canonical": d_low(p.gamma, p.delta, n, p.x_reg, p.eta),
        "D_floor_canonical": d_floor(p.delta, p.x_reg, p.eta),
        "delta_concentration": delta_concentration(p.gamma, n, p.x_reg, p.x_crit),
        "delta_substrate": delta_substrate(p.gamma, p.D_max, n, p.x_reg, p.eta),
        "rescue_quartet_delta_2": {
            "baseline_share": y_star(1.5, 2.0, n, p.x_reg),
            "gamma_low": gamma_low(2.0, n, p.x_reg, p.x_crit),
            "share_at_gamma_6": y_star(6.0, 2.0, n, p.x_reg),
            "throughput_at_gamma_6": d_low(6.0, 2.0, n, p.x_reg, p.eta),
            "D_floor": d_floor(2.0, p.x_reg, p.eta)},
        "seed_7": {"lock": lock_threshold(p.omega), "arc_r_min_0.5": arc_threshold(p.omega, 0.5),
                   "r_lock_at_K_3": locked_state(p.omega, 3.0)[1]},
        "K_arc_density": {"gaussian_sigma_1": {str(f): arc_threshold_density(gauss, f) for f in (0.25, 0.5, 0.75)},
                          "lorentzian_Delta_1": {str(f): arc_threshold_density(lorentz, f) for f in (0.25, 0.5, 0.75)}},
    }


def make_figure(report, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    teo = teo_model()
    base = teo.Params()
    n, x_reg, x_crit = base.N, base.x_reg, base.x_crit
    fig, (left, right) = plt.subplots(1, 2, figsize=(11.5, 5.4))

    delta = 2.0
    gammas = np.linspace(0.6, 9.4, 400)
    left.plot(gammas, [d_low(g, delta, n, x_reg) for g in gammas], color="black", lw=1.6,
              label=r"$D_{\rm low}(\gamma)$: throughput at $y^*$")
    left.axhline(d_floor(delta, x_reg), color="black", ls=":", lw=1.2, label=r"$D_{\rm floor}$")
    left.axvline(gamma_low(delta, n, x_reg, x_crit), color="black", ls="--", lw=1.2,
                 label=r"$\gamma_{\rm low}$")
    style = {"untouched": ("o", "#1b7837"), "damage-stabilised": ("s", "#c98b1f"),
             "veto": ("x", "#b2182b"), "concentration": ("^", "#762a83"), "unsettled": ("d", "grey")}
    for outcome, (marker, colour) in style.items():
        cells = [c for c in report["plane"] if c["outcome"] == outcome]
        if cells:
            left.scatter([c["gamma"] for c in cells], [c["D_max"] for c in cells], marker=marker,
                         color=colour, s=34, label=f"simulated: {outcome}")
    left.set_xlabel(r"brake strength $\gamma$")
    left.set_ylabel(r"dissipation ceiling $D_{\max}$")
    left.set_title(r"Resource–substrate plane at capability $\delta = 2$")
    left.set_ylim(1.4, 2.3)
    left.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, frameon=False)

    omega = base.omega
    lock = lock_threshold(omega)
    ks = np.linspace(lock["K_lock"] * 1.0005, 4.0, 200)
    right.plot(ks, [locked_state(omega, k)[1] for k in ks], color="black", lw=1.6,
               label=r"$r_{\rm lock}(K)$, stable locked state")
    scan = report["coherence_scan"]
    right.plot([s["K"] for s in scan], [s["r_min_sampled"] for s in scan], "o", color="#2166ac",
               ms=4, label="simulated: minimum $r$ over $t \\leq 300$")
    right.axvline(lock["K_lock"], color="black", ls="--", lw=1.2, label=r"$K_{\rm lock}(\omega)$")
    right.axvline(report["thresholds"]["seed_7"]["arc_r_min_0.5"]["K_arc"], color="black", ls="-.",
                  lw=1.2, label=r"$K_{\rm arc}(\omega)$")
    right.axvline(teo.kc_gaussian(1.0), color="grey", ls=":", lw=1.2, label=r"$K_c$ (continuum onset)")
    right.axhline(base.r_min, color="grey", lw=0.8)
    right.set_xlabel(r"coupling $K$")
    right.set_ylabel(r"coherence $r$")
    right.set_title(r"Coherence axis, canonical frequencies ($N = 50$, seed 7)")
    right.set_ylim(0, 1.02)
    right.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, frameon=False)
    fig.tight_layout()
    fig.savefig(outdir / "corridor_sufficiency.png", dpi=200)
    plt.close(fig)


def source_info():
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    return {"runner_sha256": sha(Path(__file__)), "canonical_teo_sha256": sha(TEO_PATH),
            "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__}


def write_report(report, path):
    """One record per line inside each list, so that diffs stay readable."""
    lines = ["{"]
    keys = list(report)
    for k, key in enumerate(keys):
        value, comma = report[key], "," if k < len(keys) - 1 else ""
        if isinstance(value, list):
            lines.append(f' {json.dumps(key)}: [')
            lines.extend("  " + json.dumps(row) + ("," if i < len(value) - 1 else "")
                         for i, row in enumerate(value))
            lines.append(" ]" + comma)
        else:
            lines.append(f" {json.dumps(key)}: {json.dumps(value)}{comma}")
    lines.append("}")
    path.write_text("\n".join(lines) + "\n")


def run_experiment(outdir, samples=200):
    params = asdict(teo_model().Params())
    params.pop("omega")
    params.pop("base_fitness")
    report = {"provenance": source_info(),
              "configuration": {"default_parameters": params,
                                "solver_note": "Canonical run(): RK45, rtol 1e-7, atol 1e-9, max_step 0.1. "
                                               "Arbitrary starts: RK45 at the tolerances given in the runner.",
                                "sampling_seed": 20261115, "samples_per_set": samples},
              "thresholds": thresholds()}
    for name, build in (("closed_forms", closed_form_rows), ("resource_thresholds", resource_threshold_rows),
                        ("open_sets", lambda: open_set_rows(samples)), ("damage_window", damage_rows),
                        ("plane", plane_rows), ("coherence_thresholds", coherence_rows),
                        ("coherence_scan", coherence_scan)):
        report[name] = build()
        print(f"Completed {name}", flush=True)
    outdir.mkdir(parents=True, exist_ok=True)
    write_report(report, outdir / "results.json")
    make_figure(report, outdir)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results")
    parser.add_argument("--samples", type=int, default=200, help="Initial conditions per invariant set.")
    args = parser.parse_args()
    run_experiment(args.output, args.samples)
