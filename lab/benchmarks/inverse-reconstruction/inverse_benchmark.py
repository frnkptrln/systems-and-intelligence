"""
inverse_benchmark.py

Trace → candidate process models: inverse-reconstruction benchmark (v0).

WHY THIS EXISTS.  Each task gives the reconstructor N steps of trace and asks
for compatible parameters or rules inside a declared model family. Three
dials — observation noise, partial observability, and trace length / coverage
— make the bounded identification problem measurable. No universal claim that
forward execution is cheap or inverse reconstruction is hard is assumed.

WHAT v0 DELIBERATELY CONCEDES.  In all three testbeds the *model family is
known* to the reconstructor (it knows it is looking at a Kuramoto system, an
elementary CA, a Boids flock — it only lacks the parameters / rule bits).
This is the standard setting of system identification and SINDy-style sparse
regression (Ljung 1999; Brunton, Proctor & Kutz 2016). Recovery in this
setting is cheap at full observability and low noise. Cost and identifiability
change with the model family, observation process, noise, algorithm, and
coverage. A trace that never exercises part of a rule leaves a
CONSISTENT-MODEL CLASS relative to those choices.

TESTBEDS

  1. KURAMOTO (continuous ODE, mean-field).  Forward: N oscillators,
     dθ_i/dt = ω_i + K·r·sin(ψ−θ_i).  Inverse: finite-difference dθ/dt from
     the (noisy) trace, then least squares on the known feature library
     {1, r·sin(ψ−θ_i)} → recovers all ω_i and the shared K.  Dials: angle
     observation noise; observed fraction (the mean field r,ψ is then computed
     from the observed subset only — a biased field, the realistic case).

  2. ELEMENTARY CA (discrete rule table).  Forward: one of the 256 Wolfram
     rules on a ring.  Inverse: tabulate neighborhood→successor with majority
     vote (exact recovery is trivial *given coverage*).  Dials: bit-flip noise;
     initial-condition entropy (a single-seed IC may never exercise some
     neighborhoods → the unseen bits are unidentifiable under this
     observation process, and the consistent-model class has size 2^unseen).
     This testbed measures
     identifiability, not cleverness.

  3. BOIDS (agent-based, position-only observation).  Forward: cohesion/
     alignment/separation with weights (w_c, w_a, w_s).  Inverse: velocities
     and accelerations estimated by differencing the (noisy) positions, the
     three steering features recomputed from the noisy state, least squares →
     weights.  Dial: position noise.  Double differencing amplifies noise by
     ~1/dt², so this curve degrades fastest — the honest cost of observing
     state instead of derivatives.

METRICS.  Parameter recovery: relative error on K / rule-bit accuracy /
weight relative error.  Identifiability: observed-neighborhood fraction and
log2 of the consistent-model class size.  (v1 may add re-simulation
divergence as a behavioral metric.)

Usage::

    python inverse_benchmark.py            # console summary, all testbeds
    python inverse_benchmark.py --save     # also write the benchmark figure
    python inverse_benchmark.py --save -o DIR   # figure into DIR (default lab/tools/)

Related:
- theory/core/the-generator-question.md       (legacy motivation)
- theory/core/mathematical-axioms.md          (current process foundation)
- theory/reference/open-problems.md           (Open Problem 11: bounded inverse reconstruction)
- meta/research-alignment/related-work-map.md (SINDy / system identification / program induction anchors)
- lab/experiments/trace_to_generator/         (the earlier inverse-prompting scaffold)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

TWO_PI = 2.0 * np.pi


# ════════════════════════ Testbed 1: Kuramoto ═══════════════════════
def kuramoto_forward(N: int = 20, K: float = 1.5, T: float = 40.0,
                     dt: float = 0.02, sigma_omega: float = 1.0,
                     seed: int = 0) -> tuple[np.ndarray, np.ndarray, float, float]:
    """Integrate the all-to-all mean-field Kuramoto model (RK4).

    Returns (theta[steps, N], omega[N], K, dt). Incoherent random IC — for
    identification, richer phase coverage is *better* (the regression sees
    more of the feature space).
    """
    rng = np.random.default_rng(seed)
    omega = rng.normal(0.0, sigma_omega, N)
    theta = rng.uniform(0.0, TWO_PI, N)
    steps = int(T / dt)

    def rhs(th):
        z = np.mean(np.exp(1j * th))
        r, psi = np.abs(z), np.angle(z)
        return omega + K * r * np.sin(psi - th)

    out = np.empty((steps, N))
    for t in range(steps):
        out[t] = theta
        k1 = rhs(theta)
        k2 = rhs(theta + 0.5 * dt * k1)
        k3 = rhs(theta + 0.5 * dt * k2)
        k4 = rhs(theta + dt * k3)
        theta = theta + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return out, omega, K, dt


def kuramoto_inverse(theta: np.ndarray, dt: float, noise: float = 0.0,
                     observed_frac: float = 1.0, seed: int = 0
                     ) -> tuple[float, np.ndarray, np.ndarray]:
    """Recover (K, omega) from a (noisy, possibly partially observed) trace.

    Least squares on the known mean-field library: for each observed i,
    dθ_i/dt = ω_i + K · r_obs · sin(ψ_obs − θ_i), with (r_obs, ψ_obs) computed
    from the OBSERVED subset only. Returns (K_hat, omega_hat, observed_idx).
    """
    rng = np.random.default_rng(seed + 1)
    steps, N = theta.shape
    M = max(2, int(round(observed_frac * N)))
    idx = rng.choice(N, size=M, replace=False)

    th = theta[:, idx] + noise * rng.standard_normal((steps, M))
    th_unw = np.unwrap(th, axis=0)
    # central differences (drop first/last sample)
    dth = (th_unw[2:] - th_unw[:-2]) / (2.0 * dt)
    th_mid = th[1:-1]

    z = np.mean(np.exp(1j * th_mid), axis=1)
    r, psi = np.abs(z), np.angle(z)
    feat = r[:, None] * np.sin(psi[:, None] - th_mid)     # (steps-2, M)

    # design: unknowns [omega_1..omega_M, K]
    Tm = dth.shape[0]
    A = np.zeros((Tm * M, M + 1))
    y = np.empty(Tm * M)
    for j in range(M):
        rows = slice(j * Tm, (j + 1) * Tm)
        A[rows, j] = 1.0
        A[rows, M] = feat[:, j]
        y[rows] = dth[:, j]
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return float(coef[M]), coef[:M], idx


# ════════════════════════ Testbed 2: Elementary CA ══════════════════
def ca_forward(rule: int = 110, W: int = 200, T: int = 200,
               ic: str = "random", seed: int = 0) -> np.ndarray:
    """Run an elementary CA on a ring. Returns grid[T, W] of {0,1}."""
    rng = np.random.default_rng(seed)
    bits = np.array([(rule >> k) & 1 for k in range(8)], dtype=np.uint8)
    if ic == "random":
        row = (rng.random(W) < 0.5).astype(np.uint8)
    else:                                  # "single": one seed cell
        row = np.zeros(W, dtype=np.uint8)
        row[W // 2] = 1
    grid = np.empty((T, W), dtype=np.uint8)
    for t in range(T):
        grid[t] = row
        nb = (np.roll(row, 1).astype(int) << 2) | (row.astype(int) << 1) \
             | np.roll(row, -1).astype(int)
        row = bits[nb]
    return grid


def ca_inverse(grid: np.ndarray, flip_p: float = 0.0, seed: int = 0
               ) -> tuple[np.ndarray, np.ndarray, int]:
    """Infer the rule table from a (noisy) space-time trace by majority vote.

    Returns (rule_bits_hat[8] with -1 for never-observed neighborhoods,
    seen_mask[8], equivalence_class_size = 2**unseen).
    """
    rng = np.random.default_rng(seed + 2)
    g = grid.copy()
    if flip_p > 0:
        flips = rng.random(g.shape) < flip_p
        g = (g ^ flips.astype(np.uint8))
    counts = np.zeros((8, 2), dtype=np.int64)
    for t in range(g.shape[0] - 1):
        row, nxt = g[t].astype(int), g[t + 1].astype(int)
        nb = (np.roll(row, 1) << 2) | (row << 1) | np.roll(row, -1)
        for pat in range(8):
            m = nb == pat
            if m.any():
                counts[pat, 1] += int(nxt[m].sum())
                counts[pat, 0] += int(m.sum() - nxt[m].sum())
    seen = counts.sum(axis=1) > 0
    bits = np.where(seen, np.argmax(counts, axis=1), -1)
    return bits, seen, int(2 ** int((~seen).sum()))


def ca_bit_accuracy(rule: int, bits_hat: np.ndarray, seen: np.ndarray) -> float:
    """Accuracy on the OBSERVED bits (unseen bits are unidentifiable, not wrong)."""
    true_bits = np.array([(rule >> k) & 1 for k in range(8)])
    if not seen.any():
        return float("nan")
    return float((bits_hat[seen] == true_bits[seen]).mean())


# ════════════════════════ Testbed 3: Boids ══════════════════════════
def _boids_features(x: np.ndarray, v: np.ndarray, R: float = 6.0,
                    r_sep: float = 1.5) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Cohesion / alignment / separation steering vectors for every boid.

    x, v: (N, 2). Returns three (N, 2) arrays. This is the KNOWN feature
    library of the inverse problem.
    """
    N = x.shape[0]
    d = x[:, None, :] - x[None, :, :]              # d[i,j] = x_i - x_j
    dist = np.linalg.norm(d, axis=2)
    np.fill_diagonal(dist, np.inf)
    nb = dist < R

    coh = np.zeros_like(x)
    ali = np.zeros_like(x)
    sep = np.zeros_like(x)
    for i in range(N):
        j = nb[i]
        if j.any():
            coh[i] = x[j].mean(axis=0) - x[i]
            ali[i] = v[j].mean(axis=0) - v[i]
        close = dist[i] < r_sep
        if close.any():
            w = d[i, close] / (dist[i, close][:, None] ** 2)
            sep[i] = w.sum(axis=0)
    return coh, ali, sep


def boids_forward(N: int = 30, T: int = 400, dt: float = 0.05,
                  w: tuple[float, float, float] = (0.8, 1.2, 2.0),
                  seed: int = 0) -> tuple[np.ndarray, float]:
    """Open-space Boids. Returns positions[T, N, 2] and dt."""
    rng = np.random.default_rng(seed)
    x = rng.uniform(-5, 5, (N, 2))
    v = rng.uniform(-1, 1, (N, 2))
    wc, wa, ws = w
    X = np.empty((T, N, 2))
    for t in range(T):
        X[t] = x
        coh, ali, sep = _boids_features(x, v)
        a = wc * coh + wa * ali + ws * sep
        v = v + dt * a
        speed = np.linalg.norm(v, axis=1, keepdims=True)
        v = np.where(speed > 4.0, v * (4.0 / speed), v)   # speed cap
        x = x + dt * v
    return X, dt


def boids_inverse(X: np.ndarray, dt: float, noise: float = 0.0,
                  seed: int = 0) -> np.ndarray:
    """Recover (w_c, w_a, w_s) from (noisy) POSITION traces only.

    Velocities and accelerations are estimated by central differencing the
    noisy positions; the feature library is recomputed from the noisy state.
    Steps where the speed cap was active are excluded (the cap is outside the
    linear model — the inverse method is told only that much).
    """
    rng = np.random.default_rng(seed + 3)
    Xn = X + noise * rng.standard_normal(X.shape)
    V = (Xn[2:] - Xn[:-2]) / (2.0 * dt)                  # (T-2, N, 2)
    A = (Xn[2:] - 2 * Xn[1:-1] + Xn[:-2]) / (dt ** 2)    # (T-2, N, 2)
    Xm = Xn[1:-1]

    rows_F, rows_y = [], []
    for t in range(0, V.shape[0], 2):                    # thin for speed
        speed = np.linalg.norm(V[t], axis=1)
        ok = speed < 3.9                                 # away from the cap
        if not ok.any():
            continue
        coh, ali, sep = _boids_features(Xm[t], V[t])
        F = np.stack([coh[ok], ali[ok], sep[ok]], axis=-1)  # (n_ok, 2, 3)
        rows_F.append(F.reshape(-1, 3))
        rows_y.append(A[t][ok].reshape(-1))
    Fm = np.concatenate(rows_F)
    ym = np.concatenate(rows_y)
    w_hat, *_ = np.linalg.lstsq(Fm, ym, rcond=None)
    return w_hat


# ════════════════════════ Benchmark driver ══════════════════════════
def run_kuramoto_suite(n_seeds: int = 6) -> dict:
    noises = [0.0, 0.01, 0.03, 0.1, 0.3]
    fracs = [1.0, 0.6, 0.3, 0.15]
    K_err_noise, K_err_frac = [], []
    for nz in noises:
        errs = []
        for s in range(n_seeds):
            th, om, K, dt = kuramoto_forward(seed=s)
            K_hat, om_hat, idx = kuramoto_inverse(th, dt, noise=nz, seed=s)
            errs.append(abs(K_hat - K) / K)
        K_err_noise.append(float(np.mean(errs)))
    for fr in fracs:
        errs = []
        for s in range(n_seeds):
            th, om, K, dt = kuramoto_forward(seed=s)
            K_hat, om_hat, idx = kuramoto_inverse(th, dt, noise=0.03,
                                                  observed_frac=fr, seed=s)
            errs.append(abs(K_hat - K) / K)
        K_err_frac.append(float(np.mean(errs)))
    return {"noises": noises, "K_err_noise": K_err_noise,
            "fracs": fracs, "K_err_frac": K_err_frac}


def run_ca_suite(n_seeds: int = 3) -> dict:
    rules = [110, 30, 90]
    flips = [0.0, 0.01, 0.03, 0.1, 0.2, 0.3]
    acc = []
    for p in flips:
        a = []
        for rule in rules:
            for s in range(n_seeds):
                g = ca_forward(rule=rule, seed=s)
                bits, seen, _ = ca_inverse(g, flip_p=p, seed=s)
                a.append(ca_bit_accuracy(rule, bits, seen))
        acc.append(float(np.nanmean(a)))
    # identifiability: single-seed IC (low-entropy trace)
    ident = {}
    for rule in rules:
        g = ca_forward(rule=rule, ic="single", seed=0)
        bits, seen, eq = ca_inverse(g)
        ident[rule] = {"seen": int(seen.sum()), "class_size": eq}
    return {"flips": flips, "acc": acc, "ident": ident}


def run_boids_suite(n_seeds: int = 3) -> dict:
    w_true = (0.8, 1.2, 2.0)
    noises = [0.0, 0.001, 0.003, 0.01, 0.03]
    w_err = []
    for nz in noises:
        errs = []
        for s in range(n_seeds):
            X, dt = boids_forward(w=w_true, seed=s)
            w_hat = boids_inverse(X, dt, noise=nz, seed=s)
            errs.append(float(np.linalg.norm(w_hat - np.array(w_true))
                              / np.linalg.norm(w_true)))
        w_err.append(float(np.mean(errs)))
    return {"noises": noises, "w_err": w_err, "w_true": w_true}


def print_summary(kur: dict, ca: dict, boi: dict) -> None:
    print("=" * 70)
    print("  INVERSE-RECONSTRUCTION BENCHMARK v0 — bounded model recovery")
    print("=" * 70)
    print("\n[1] KURAMOTO — relative error on K (known family, least squares)")
    print(f"    vs noise (full observability): " +
          "  ".join(f"σ={n:g}:{e:.1%}" for n, e in
                    zip(kur['noises'], kur['K_err_noise'])))
    print(f"    vs observed fraction (σ=0.03): " +
          "  ".join(f"f={f:g}:{e:.1%}" for f, e in
                    zip(kur['fracs'], kur['K_err_frac'])))
    print("\n[2] ELEMENTARY CA — rule-bit accuracy on observed neighborhoods")
    print(f"    vs flip noise (random IC):     " +
          "  ".join(f"p={p:g}:{a:.0%}" for p, a in zip(ca['flips'], ca['acc'])))
    print("    identifiability under single-seed IC (coverage, not noise):")
    for rule, d in ca["ident"].items():
        print(f"      rule {rule:>3}: {d['seen']}/8 neighborhoods observed → "
              f"consistent-model class size {d['class_size']}")
    print("\n[3] BOIDS — relative error on (w_c, w_a, w_s) from positions only")
    print(f"    vs position noise:             " +
          "  ".join(f"σ={n:g}:{e:.1%}" for n, e in
                    zip(boi['noises'], boi['w_err'])))
    print("\nReading: with a KNOWN family, full observability and clean data,")
    print("recovery is cheap (the SINDy/system-identification regime). The")
    print("difficulty enters measurably through noise×differentiation (Boids),")
    print("partial observability (Kuramoto), and coverage (CA equivalence")
    print("classes) — and, beyond v0, through search over model families.")


# ════════════════════════ Figure ════════════════════════════════════
def _repo_lab_tools() -> Path:
    return Path(__file__).resolve().parents[2] / "tools"


def figure(kur: dict, ca: dict, boi: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(12, 8.5))

    ax = axes[0, 0]
    ax.semilogy(kur["noises"], np.maximum(kur["K_err_noise"], 1e-5),
                "o-", color="#1f77b4", lw=2)
    ax.set_xlabel("observation noise σ (rad)")
    ax.set_ylabel("relative error on K")
    ax.set_title("(a) Kuramoto: recovery vs noise\n(full observability — cheap)")
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.semilogy(kur["fracs"], np.maximum(kur["K_err_frac"], 1e-5),
                "s-", color="#d62728", lw=2)
    ax.invert_xaxis()
    ax.set_xlabel("observed fraction of oscillators")
    ax.set_ylabel("relative error on K")
    ax.set_title("(b) Kuramoto: partial observability\n(biased mean field — error grows)")
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.plot(ca["flips"], ca["acc"], "o-", color="#2ca02c", lw=2,
            label="bit accuracy (random IC)")
    ax.axhline(1.0, ls=":", color="gray")
    txt = "\n".join(f"rule {r}: {d['seen']}/8 seen → class {d['class_size']}"
                    for r, d in ca["ident"].items())
    ax.text(0.98, 0.05, "single-seed IC (coverage):\n" + txt,
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
            bbox=dict(boxstyle="round", fc="#f0f0f0", ec="gray"))
    ax.set_xlabel("bit-flip probability")
    ax.set_ylabel("rule-bit accuracy (observed bits)")
    ax.set_ylim(0.45, 1.05)
    ax.set_title("(c) Elementary CA: noise vs coverage\n(unseen neighborhoods ⇒ equivalence class)")
    ax.legend(loc="lower left", fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ax.semilogy(boi["noises"], np.maximum(boi["w_err"], 1e-5),
                "^-", color="#9467bd", lw=2)
    ax.set_xlabel("position noise σ")
    ax.set_ylabel("relative error on (w_c, w_a, w_s)")
    ax.set_title("(d) Boids: weights from positions only\n(double differencing amplifies noise)")
    ax.grid(alpha=0.3)

    fig.suptitle("Inverse benchmark v0 — recovery is cheap with a known family; "
                 "hardness enters via observability, noise, and coverage", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = outdir / "inverse_benchmark.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inverse-reconstruction benchmark v0 (bounded model recovery).")
    parser.add_argument("--save", action="store_true",
                        help="write the benchmark figure.")
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="output directory for the figure (default: lab/tools/).")
    args = parser.parse_args()

    kur = run_kuramoto_suite()
    ca = run_ca_suite()
    boi = run_boids_suite()
    print_summary(kur, ca, boi)

    if args.save:
        outdir = Path(args.output) if args.output else _repo_lab_tools()
        outdir.mkdir(parents=True, exist_ok=True)
        print(f"\nWriting figure to {outdir} …")
        print(f"  {figure(kur, ca, boi, outdir)}")


if __name__ == "__main__":
    main()
