#!/usr/bin/env python3
"""
exp8_reflexive_depth.py

Experiment 8: Adaptive self-estimation under regime shift

THE QUESTION. The availability node maps Kegan's subject-object move to
iterations of a self-reconstruction operator. This file tests a much narrower
engineering analogue: does online adaptation of a process-noise assumption
improve tracking after the process changes? The code directly compares
estimators; "reflexive depth" is the hypothesized interpretation, not the
measured variable.

THE SETUP. A minimal Gaussian tracking task. A hidden state theta(t) drifts
as a random walk with volatility q; the estimator observes
o(t) = theta(t) + observation noise. The depth labels below are the
interpretive vocabulary; computationally these are three estimators with
different capabilities:

  depth 0  — no self-model. Estimate = the raw current observation.
             (reactive: the agent is its behavior, holds no model of it.)
  depth 1  — a self-model with a FIXED update rule (a Kalman filter with
             process-noise Q pinned to the initial regime q0). It has a
             model of itself but is SUBJECT to the update rule: it cannot
             revise how it updates.
  depth 2  — an adaptive Kalman filter that monitors innovation statistics
             and re-estimates Q. Engineering description: online
             hyperparameter adaptation. Interpretive description: the
             update rule taken as object.

Two perturbations, chosen to separate what online Q adaptation can and cannot
identify:

  VOLATILITY REGIME CHANGE — q jumps q0 -> q1 (>> q0) at mid-run. The
     disposition starts drifting far faster. Depth 1's fixed small gain
     lags systematically; the lag is STRUCTURE in the innovations, which
     is exactly what depth 2 can take as object.
  CONSTANT SELF-OBSERVATION BIAS — o(t) = theta(t) + b + noise, constant
     b. The Wall-3 case: the bias sits on the ONLY channel the agent has
     to itself, leaves no exploitable structure once converged, and cannot
     be removed by modeling harder. No external reference, no correction.

METRIC.  RMSE of the self-estimate against the true theta, split into the
stationary window and the post-perturbation window; 200 seeds.

PREDICTIONS (stated before the first run; original interpretive language
retained, with the measured claim recalibrated in RESULT):
  P1  Stationary regime (no perturbation): depth 0 worst (no smoothing);
      depth 1 ~= depth 2 (adaptive Q settles near the true q0, so the meta
      level adds little when there is nothing to adapt to).
  P2  THE DECIDING ONE — after the volatility jump, depth 2 beats depth 1
      (lower post-change RMSE): the meta level detects the innovation
      structure depth 1 is subject to and raises its gain. This is Kegan's
      "took the update rule as object", measured. If depth 2 does NOT beat
      depth 1 here, the mapping is unsupported and the docstring will say so.
  P3  THE HONEST LIMIT — against the constant bias, depth 2 = depth 1
      (both converge to theta + b; neither removes b). Reflexive depth is
      powerless on the only channel — Wall 3 in a toy. This is the control
      that keeps P2 from being read as "more meta is always better".
  P4  Cost: depth 2's adaptivity should cost a little VARIANCE in the
      stationary regime (it chases noise it mistakes for signal) — a small
      price paid for the regime-change win. If the price is zero, note it.

RESULT (run 1, 200 seeds — the numbers the console prints):
  P1  CONFIRMED: stationary RMSE 0.497 / 0.141 / 0.174 (depth 0 / 1 / 2).
      The self-model roughly triples accuracy over no model; depth 2 ~=
      depth 1 with a small penalty — nothing to adapt to when stationary.
  P2  CONFIRMED AT THE ESTIMATOR LEVEL: post-change RMSE 0.498 / 0.504 /
      0.322 — adaptive depth 2 beats fixed-Q depth 1 by 36%. The fixed
      filter is slightly worse than raw observation after misspecification.
      This measures the value of online Q adaptation; the Kegan mapping is
      an interpretation over that mechanism.
  P3  CONFIRMED WITHIN THIS OBSERVATION MODEL: under constant bias, depth 2
      (0.624) does not beat depth 1 (0.612). Both retain error near the bias
      magnitude because no unbiased reference exists. This is an
      identifiability limit for the sole biased channel, not a general
      empirical measurement of Wall 3.
  P4  CONFIRMED: depth 2 costs a little stationary variance (0.174 vs
      0.141) — it occasionally mistakes noise for a regime shift and
      raises its gain. The price of adaptivity, paid in the calm regime
      and repaid many times over at the change.

POST-RUN CALIBRATION. The code directly measures adaptive filtering in one
Gaussian tracking task. Depth 2 differs from depth 1 not merely by "depth"
but by access to a different algorithmic capability: online estimation of
Q. The result therefore does not isolate reflexivity from adaptivity.

WHAT THIS DOES NOT SHOW. It does not measure Kegan stages, human development,
consciousness, or a general law of self-modeling. The constant-bias result is
an identifiability limit under one observation channel, evaluated by an
external ground truth unavailable to the agent; it is analogous to the
repo's Wall-3 concern, not a measurement of Gödelian self-limitation.

Required follow-ups before a stronger interpretation: an oracle Q-switch,
fixed-Q grid and change-point baselines, a shuffled/uninformative meta-signal
control, paired uncertainty intervals, and an external-reference
intervention for the bias case. Depth 3 remains unbuilt.

Usage::

    python exp8_reflexive_depth.py            # console summary
    python exp8_reflexive_depth.py --save      # + figure to lab/tools/

Related:
- theory/identity/consciousness-as-global-availability.md  (On Levels: reflexive depth; the depth-2 toy named there)
- lab/agents/three_layer_agent.py                          (conceptual motivation only; not used by this experiment)
- theory/core/the-generator-question.md                    (formal analogy only; this experiment measures channel identifiability)
- theory/core/measurement-as-weak-intervention.md          (the external-reference follow-up: watching < perturbing, reflexive)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

T = 400
T_SWITCH = 200
Q0 = 0.002          # initial drift volatility (variance)
Q1 = 0.05           # post-change volatility
R_OBS = 0.25        # observation noise variance
BIAS = 0.6          # constant self-observation bias
N_SEEDS = 200


def make_world(seed: int, mode: str) -> tuple[np.ndarray, np.ndarray]:
    """Return (theta[T] true disposition, obs[T] self-observation).

    mode: 'regime' (volatility jumps at T_SWITCH) or 'bias' (constant
    offset on the observation channel, stationary volatility).
    """
    rng = np.random.default_rng(seed)
    theta = np.empty(T)
    theta[0] = 0.0
    for t in range(1, T):
        if mode == "regime":
            q = Q0 if t < T_SWITCH else Q1
        else:
            q = Q0
        theta[t] = theta[t - 1] + rng.normal(0.0, np.sqrt(q))
    obs = theta + rng.normal(0.0, np.sqrt(R_OBS), T)
    if mode == "bias":
        obs = obs + BIAS
    return theta, obs


def depth0(obs: np.ndarray) -> np.ndarray:
    """No self-model: the estimate is the raw current observation."""
    return obs.copy()


def depth1(obs: np.ndarray, q_fixed: float = Q0) -> np.ndarray:
    """Fixed-rule self-model: Kalman filter with Q pinned to the initial
    regime. Has a model of itself; cannot revise how it updates."""
    xh = np.empty(T)
    x, P = obs[0], 1.0
    for t in range(T):
        P = P + q_fixed                       # predict
        e = obs[t] - x
        K = P / (P + R_OBS)
        x = x + K * e
        P = (1 - K) * P
        xh[t] = x
    return xh


def depth2(obs: np.ndarray, ewma: float = 0.05) -> np.ndarray:
    """Takes the update rule as object: adaptive Kalman that re-estimates
    its own process noise Q from the running statistics of its innovations.
    Engineering description: an adaptive process-noise estimator. The
    "model of its modeling" phrase is the hypothesized interpretation."""
    xh = np.empty(T)
    x, P = obs[0], 1.0
    s_hat = R_OBS                              # running innovation variance
    for t in range(T):
        Q_hat = max(0.0, s_hat - R_OBS - P)    # process noise implied by innovations
        P = P + Q_hat
        e = obs[t] - x
        s_hat = (1 - ewma) * s_hat + ewma * e * e
        K = P / (P + R_OBS)
        x = x + K * e
        P = (1 - K) * P
        xh[t] = x
    return xh


def _rmse(est: np.ndarray, theta: np.ndarray, lo: int, hi: int) -> float:
    return float(np.sqrt(np.mean((est[lo:hi] - theta[lo:hi]) ** 2)))


def run_suite(n_seeds: int = N_SEEDS) -> dict:
    out = {mode: {d: {"stat": [], "post": []} for d in ("d0", "d1", "d2")}
           for mode in ("regime", "bias")}
    for mode in ("regime", "bias"):
        for s in range(n_seeds):
            theta, obs = make_world(s, mode)
            ests = {"d0": depth0(obs), "d1": depth1(obs), "d2": depth2(obs)}
            for d, est in ests.items():
                # stationary window: settled, before the switch
                out[mode][d]["stat"].append(_rmse(est, theta, 50, T_SWITCH))
                # post window: after the switch (regime) / matched window (bias)
                out[mode][d]["post"].append(_rmse(est, theta, T_SWITCH, T))
    return out


def print_summary(res: dict) -> None:
    print("=" * 74)
    print("  EXPERIMENT 8 — adaptive self-estimation under regime shift")
    print("  (self-estimate RMSE vs true disposition; 200 seeds)")
    print("=" * 74)
    for mode, title in (("regime", "VOLATILITY REGIME CHANGE (q0 -> q1 at t=200)"),
                        ("bias", "CONSTANT OBSERVATION BIAS (sole-channel control)")):
        print(f"\n  {title}")
        print(f"    {'':22s} {'depth 0':>10s} {'depth 1':>10s} {'depth 2':>10s}")
        for win, label in (("stat", "stationary RMSE"),
                          ("post", "post-window RMSE")):
            vals = [np.mean(res[mode][d][win]) for d in ("d0", "d1", "d2")]
            print(f"    {label:22s} {vals[0]:10.3f} {vals[1]:10.3f} {vals[2]:10.3f}")
        d1p = np.mean(res[mode]["d1"]["post"])
        d2p = np.mean(res[mode]["d2"]["post"])
        gain = (d1p - d2p) / d1p * 100 if d1p else 0.0
        print(f"    depth2 vs depth1 (post): {gain:+.1f}%  "
              f"({'adaptive estimator helps' if gain > 2 else 'no adaptive-estimator gain'})")
    print("\n  Reading: online Q adaptation helps after a volatility shift")
    print("  and cannot identify a constant bias on the sole observation")
    print("  channel. The reflexive-depth / Kegan reading remains a hypothesis.")


def figure(res: dict, outdir: Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    depths = ["d0", "d1", "d2"]
    labels = ["depth 0\n(raw obs)", "depth 1\n(fixed Q)", "depth 2\n(adaptive Q)"]
    colors = ["#999999", "#1f77b4", "#d62728"]
    xs = np.arange(3)

    for ax, mode, title in (
        (axes[0], "regime", "(a) Volatility regime change\nonline Q adaptation helps"),
        (axes[1], "bias", "(b) Constant observation bias\nnot identifiable from the sole channel"),
    ):
        stat = [np.mean(res[mode][d]["stat"]) for d in depths]
        post = [np.mean(res[mode][d]["post"]) for d in depths]
        w = 0.38
        ax.bar(xs - w / 2, stat, w, label="stationary", color=colors, alpha=0.5)
        ax.bar(xs + w / 2, post, w, label="post-perturbation",
               color=colors)
        ax.set_xticks(xs, labels, fontsize=8)
        ax.set_ylabel("self-estimate RMSE")
        ax.set_title(title, fontsize=10)
        ax.grid(alpha=0.3, axis="y")
        ax.legend(fontsize=8)

    fig.suptitle("Exp 8 — adaptive self-estimation (fixed vs online process-noise model)",
                 fontsize=12)
    fig.tight_layout()
    out = outdir / "exp8_reflexive_depth.png"
    fig.savefig(out, dpi=110)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true")
    ap.add_argument("--seeds", type=int, default=N_SEEDS)
    args = ap.parse_args()
    res = run_suite(n_seeds=args.seeds)
    print_summary(res)
    if args.save:
        outdir = Path(__file__).resolve().parents[1] / "tools"
        print(f"\n  figure -> {figure(res, outdir)}")


if __name__ == "__main__":
    main()
