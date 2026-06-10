"""
intervention_experiment.py

Does the equivalence class collapse under interventions? (Benchmark v1, part 1)

THE QUESTION.  `theory/computation/construction-vs-deduction.md` ends on an
open thread with an old ontological core — *does the world already exist, or
do we construct it?* — made operational: under passive observation, many
generators may remain consistent with everything we will ever see (the
consistent-generator equivalence class of the v0 benchmark). Experiments,
however, are not traces. They are QUERIES: the observer chooses states and
makes the generator answer. The measurable form of the question is therefore:

    How does the size of the consistent-generator class shrink as a function
    of INTERVENTION budget — and how does that compare, at equal observation
    budget, to merely watching longer?

TWO TESTBEDS.

  1. ELEMENTARY CA (discrete; class size exactly computable).
     Start from the v0 worst case: rule evolved from a single-seed IC, whose
     orbit never exercises some neighborhoods (rule 90: 5/8 seen, class 2^3).
     Three policies, all consuming the SAME budget (observed update-rows):
       - passive : keep watching the orbit.
       - flip    : before observing, flip one random bit of the current row
                   (a minimal local perturbation — a cheap experiment).
       - design  : set the row to a de Bruijn sequence B(2,3) tiling, which
                   contains every 3-neighborhood (a maximally informative
                   prepared state — the designed experiment).
     Expectation: passive PLATEAUS (the orbit's neighborhood distribution is
     exhausted; more time buys nothing); flips collapse the class gradually;
     one designed preparation collapses it to 1.

  2. KURAMOTO (continuous; identifiability instead of a finite class).
     Observe a SYNCHRONIZED system (K > K_c, locked attractor). In the locked
     state the trace satisfies, for every oscillator i,
         Omega = omega_i + K · r · sin(psi - theta_i)
     with all right-hand quantities CONSTANT. For any K' there is an
     omega_i' := Omega - K'·r·sin(psi - theta_i) reproducing the trace
     exactly: a one-parameter family of generators, indistinguishable on the
     attractor. Passive observation of a relaxed system therefore cannot
     identify K — not for lack of data, but in principle. An intervention
     (a phase kick) re-excites a transient and breaks the degeneracy.
     Metric: relative error on K vs. number of kicks, at fixed total
     observation time, against the passive baseline.

READING.  Attractors hide generators. A relaxed system — synchronized,
frozen, converged — is generator-degenerate: its trace is consistent with a
continuum (or a 2^k set) of rules. Only perturbation reveals structure. This
is the first-principles reason the repository's identity instruments
(Δ-Kohärenz, Observer Divergence) are PERTURBATION protocols rather than
passive transcript analyses: you cannot read a generator off an attractor.

Usage::

    python intervention_experiment.py            # console summary
    python intervention_experiment.py --save     # also write the figure

Related:
- inverse_benchmark.py                          (v0: noise/observability/coverage dials)
- theory/computation/construction-vs-deduction.md  (the open thread this answers)
- theory/core/the-generator-question.md         (the spine)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

TWO_PI = 2.0 * np.pi


# ════════════════════════ Testbed 1: Elementary CA ══════════════════
def _rule_bits(rule: int) -> np.ndarray:
    return np.array([(rule >> k) & 1 for k in range(8)], dtype=np.uint8)


def _neighborhoods(row: np.ndarray) -> np.ndarray:
    r = row.astype(int)
    return (np.roll(r, 1) << 2) | (r << 1) | np.roll(r, -1)


def _step(row: np.ndarray, bits: np.ndarray) -> np.ndarray:
    return bits[_neighborhoods(row)]


def _debruijn_row(W: int) -> np.ndarray:
    """A row tiling the de Bruijn sequence B(2,3) = 00010111 — on a ring of
    width divisible by 8 it contains every 3-bit neighborhood."""
    base = np.array([0, 0, 0, 1, 0, 1, 1, 1], dtype=np.uint8)
    reps = int(np.ceil(W / 8))
    return np.tile(base, reps)[:W]


def ca_class_curve(rule: int, policy: str, budget: int, W: int = 200,
                   T0: int = 100, seed: int = 0) -> list[int]:
    """log2(class size) after each budget step, for one policy.

    All policies first watch the single-seed orbit for T0 steps (the v0
    baseline), then spend `budget` additional observed update-rows according
    to the policy. Returns the list of unseen-bit counts (log2 class size),
    one entry per budget step (index 0 = baseline, before any extra budget).
    """
    rng = np.random.default_rng(seed)
    bits = _rule_bits(rule)
    row = np.zeros(W, dtype=np.uint8)
    row[W // 2] = 1

    seen = np.zeros(8, dtype=bool)
    for _ in range(T0):                       # baseline passive trace
        seen[np.unique(_neighborhoods(row))] = True
        row = _step(row, bits)

    curve = [int(8 - seen.sum())]
    for _ in range(budget):
        if policy == "flip":
            row = row.copy()
            row[rng.integers(W)] ^= 1
        elif policy == "design":
            row = _debruijn_row(W)
        # observe one update-row (input neighborhoods + successor)
        seen[np.unique(_neighborhoods(row))] = True
        row = _step(row, bits)
        curve.append(int(8 - seen.sum()))
    return curve


def run_ca_suite(rules=(90, 0, 110), budget: int = 30, n_seeds: int = 5) -> dict:
    out = {}
    for rule in rules:
        per_policy = {}
        for policy in ("passive", "flip", "design"):
            curves = np.array([ca_class_curve(rule, policy, budget, seed=s)
                               for s in range(n_seeds)], dtype=float)
            per_policy[policy] = curves.mean(axis=0)
        out[rule] = per_policy
    return out


# ════════════════════════ Testbed 2: Kuramoto ═══════════════════════
def _kuramoto_rhs(theta, omega, K):
    z = np.mean(np.exp(1j * theta))
    r, psi = np.abs(z), np.angle(z)
    return omega + K * r * np.sin(psi - theta)


def _integrate(theta, omega, K, T, dt):
    steps = int(T / dt)
    out = np.empty((steps, theta.size))
    for t in range(steps):
        out[t] = theta
        k1 = _kuramoto_rhs(theta, omega, K)
        k2 = _kuramoto_rhs(theta + 0.5 * dt * k1, omega, K)
        k3 = _kuramoto_rhs(theta + 0.5 * dt * k2, omega, K)
        k4 = _kuramoto_rhs(theta + dt * k3, omega, K)
        theta = theta + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return out, theta


def _estimate_K(segments: list[np.ndarray], dt: float, noise: float,
                rng: np.random.Generator) -> float:
    """Least squares for (omega_i, K) over a list of trace segments.

    Segments are processed independently (central differences never straddle
    a kick); the unknowns are shared across segments. Same feature library
    as the v0 benchmark (inverse_benchmark.kuramoto_inverse)."""
    feats, dths = [], []
    for seg in segments:
        if seg.shape[0] < 5:
            continue
        th = seg + noise * rng.standard_normal(seg.shape)
        th_unw = np.unwrap(th, axis=0)
        dth = (th_unw[2:] - th_unw[:-2]) / (2.0 * dt)
        th_mid = th[1:-1]
        z = np.mean(np.exp(1j * th_mid), axis=1)
        r, psi = np.abs(z), np.angle(z)
        feats.append(r[:, None] * np.sin(psi[:, None] - th_mid))
        dths.append(dth)
    F = np.concatenate(feats)                 # (T_total, N)
    Y = np.concatenate(dths)
    Tm, N = F.shape
    A = np.zeros((Tm * N, N + 1))
    y = np.empty(Tm * N)
    for j in range(N):
        rows = slice(j * Tm, (j + 1) * Tm)
        A[rows, j] = 1.0
        A[rows, N] = F[:, j]
        y[rows] = Y[:, j]
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return float(coef[N])


def kuramoto_kick_experiment(n_kicks: int, K: float = 3.0, N: int = 20,
                             T_obs: float = 40.0, dt: float = 0.02,
                             kick_sigma: float = 1.0, noise: float = 0.01,
                             seed: int = 0) -> float:
    """Relative error on K from a LOCKED system, with n_kicks interventions.

    The system is first relaxed onto its synchronized attractor (that
    transient is NOT observed — the observer arrives late). Then T_obs of
    observation is spent, interrupted by n_kicks phase kicks; estimation
    uses only the observed window. n_kicks = 0 is the passive baseline.
    """
    rng = np.random.default_rng(seed)
    omega = rng.normal(0.0, 1.0, N)
    theta = rng.uniform(0.0, TWO_PI, N)
    _, theta = _integrate(theta, omega, K, 60.0, dt)   # relax (unobserved)

    n_seg = n_kicks + 1
    T_seg = T_obs / n_seg
    segments = []
    for s in range(n_seg):
        seg, theta = _integrate(theta, omega, K, T_seg, dt)
        segments.append(seg)
        if s < n_kicks:
            theta = theta + kick_sigma * rng.standard_normal(N)   # the query
    K_hat = _estimate_K(segments, dt, noise, rng)
    return abs(K_hat - K) / K


def run_kuramoto_suite(kick_counts=(0, 1, 2, 4, 8), n_seeds: int = 6) -> dict:
    errs = []
    for b in kick_counts:
        e = [kuramoto_kick_experiment(b, seed=s) for s in range(n_seeds)]
        errs.append(float(np.mean(e)))
    return {"kicks": list(kick_counts), "K_err": errs}


# ════════════════════════ Reporting ═════════════════════════════════
def print_summary(ca: dict, kur: dict) -> None:
    print("=" * 70)
    print("  INTERVENTION EXPERIMENT — does the equivalence class collapse?")
    print("=" * 70)
    print("\n[1] ELEMENTARY CA — log2(consistent-generator class size)")
    print("    baseline: single-seed orbit, 100 steps; then 30 budget steps\n")
    for rule, pp in ca.items():
        print(f"    rule {rule:>3}:  start={pp['passive'][0]:.0f} bits unseen "
              f"(class {2**int(pp['passive'][0])})")
        for pol in ("passive", "flip", "design"):
            c = pp[pol]
            print(f"      {pol:>7}: after 1={c[1]:.1f}  5={c[5]:.1f}  "
                  f"15={c[15]:.1f}  30={c[30]:.1f}  (bits unseen, mean)")
    print("\n[2] KURAMOTO — rel. error on K, observing a LOCKED system")
    print("    (T_obs fixed at 40; kicks replace nothing — same budget)\n")
    print("    " + "  ".join(f"kicks={b}: {e:.1%}"
                             for b, e in zip(kur["kicks"], kur["K_err"])))
    print("\nReading: passive observation of a relaxed system plateaus — the")
    print("attractor is generator-degenerate (for locked Kuramoto, provably a")
    print("one-parameter family). Local perturbations collapse the ambiguity")
    print("gradually; one designed preparation collapses it at a stroke.")
    print("Experiments are queries, not traces. Facts about the generator can")
    print("be CREATED by intervention that observation alone cannot reach.")


def _repo_lab_tools() -> Path:
    return Path(__file__).resolve().parents[2] / "tools"


def figure(ca: dict, kur: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.0))

    colors = {"passive": "#7f7f7f", "flip": "#1f77b4", "design": "#d62728"}
    pp = ca[90]
    x = np.arange(len(pp["passive"]))
    for pol in ("passive", "flip", "design"):
        axL.plot(x, pp[pol], "o-", ms=3, lw=2, color=colors[pol],
                 label={"passive": "passive (watch longer)",
                        "flip": "intervene: flip one bit",
                        "design": "intervene: prepared state (de Bruijn)"}[pol])
    axL.set_xlabel("additional observation budget (update-rows)")
    axL.set_ylabel(r"$\log_2$(consistent-generator class size)")
    axL.set_title("(a) CA rule 90, single-seed start:\n"
                  "passive observation plateaus; queries collapse the class")
    axL.text(0.98, 0.55,
             "frozen system (rule 0):\npassive AND one-bit flips stay\n"
             "at class 16 forever — only the\nprepared state collapses it.\n"
             "The deader the dynamics, the\nmore structure the query\n"
             "itself must supply.",
             transform=axL.transAxes, ha="right", va="center", fontsize=8,
             bbox=dict(boxstyle="round", fc="#fff3e6", ec="#d62728"))
    axL.legend(fontsize=9, loc="center left")
    axL.grid(alpha=0.3)

    axR.semilogy(kur["kicks"], np.maximum(kur["K_err"], 1e-4), "s-",
                 color="#9467bd", lw=2)
    axR.set_xlabel("number of phase-kick interventions (fixed total T_obs)")
    axR.set_ylabel("relative error on K")
    axR.set_title("(b) Kuramoto, observed on its locked attractor:\n"
                  "passively unidentifiable — one kick breaks the degeneracy")
    axR.grid(alpha=0.3)

    fig.suptitle("Interventions vs. observation — facts about the generator "
                 "that watching cannot reach, queries can create", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    out = outdir / "inverse_benchmark_interventions.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Intervention experiment (benchmark v1, part 1).")
    parser.add_argument("--save", action="store_true",
                        help="write the figure (to lab/tools/).")
    parser.add_argument("-o", "--output", type=str, default=None)
    args = parser.parse_args()

    ca = run_ca_suite()
    kur = run_kuramoto_suite()
    print_summary(ca, kur)

    if args.save:
        outdir = Path(args.output) if args.output else _repo_lab_tools()
        outdir.mkdir(parents=True, exist_ok=True)
        print(f"\nWriting figure to {outdir} …")
        print(f"  {figure(ca, kur, outdir)}")


if __name__ == "__main__":
    main()
