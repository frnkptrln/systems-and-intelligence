#!/usr/bin/env python3
"""
Meta-Learning Regime Shift
--------------------------

A two-state Markov system whose transition probability changes abruptly
every N steps (regime shift).  Two agents learn side by side:

  1. FIXED-RATE agent  – constant learning rate η
  2. META-LEARNING agent – a meta-learner adjusts η based on smoothed
     prediction error: high surprise → raise η, low surprise → lower η

The comparison shows how adaptive capacity (dimension A of the
System Intelligence Index) gives an agent faster re-convergence after
regime shifts while remaining stable during calm phases.

Usage:
    python3 meta_regime_shift.py
"""

import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────
NUM_STEPS           = 8000
REGIME_LENGTH       = 2000          # steps between regime shifts
P_VALUES            = [0.15, 0.50, 0.80, 0.30]  # cycling transition probs

FIXED_LR            = 0.005         # constant learning rate for baseline
META_LR_INIT        = 0.005         # initial learning rate for meta agent
META_LR_MIN         = 0.001
META_LR_MAX         = 0.10
META_SMOOTH         = 0.02          # EMA smoothing for error signal
META_UP_FACTOR      = 1.04          # multiplicative increase on surprise
META_DOWN_FACTOR    = 0.98          # multiplicative decrease on low error
SURPRISE_THRESHOLD  = 0.25          # error above this → increase LR

SEED = 17

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def current_p_change(step):
    """Return the true transition probability for the current regime."""
    regime_idx = (step // REGIME_LENGTH) % len(P_VALUES)
    return P_VALUES[regime_idx]


def learn_step(M, state, next_state, lr):
    """
    Update a 2×2 transition matrix M given observed transition.
    Returns updated M and squared error.
    """
    prediction = M[state, :]
    target = np.array([1.0, 0.0] if next_state == 0 else [0.0, 1.0])
    error = target - prediction

    M[state, :] += lr * error
    M = np.clip(M, 1e-4, 1.0)
    M = M / M.sum(axis=1, keepdims=True)

    sq_error = np.sum(error ** 2)
    return M, sq_error


# ─────────────────────────────────────────────
# Simulation
# ─────────────────────────────────────────────

def run():
    rng = np.random.default_rng(SEED)

    # Shared system state
    system_state = 0

    # Agent 1: fixed learning rate
    M_fixed = rng.random((2, 2))
    M_fixed = M_fixed / M_fixed.sum(axis=1, keepdims=True)

    # Agent 2: meta-learning
    M_meta = M_fixed.copy()
    meta_lr = META_LR_INIT
    smoothed_error = 0.0

    # Logging
    err_fixed_log  = []
    err_meta_log   = []
    lr_log         = []
    p_true_log     = []
    learned_p_fixed = []
    learned_p_meta  = []

    for t in range(NUM_STEPS):
        p_change = current_p_change(t)
        current = system_state

        # System dynamics
        if rng.random() < p_change:
            system_state = 1 - system_state
        next_s = system_state

        # ── Agent 1: fixed LR ──
        M_fixed, e_fix = learn_step(M_fixed, current, next_s, FIXED_LR)

        # ── Agent 2: meta-learning ──
        M_meta, e_meta = learn_step(M_meta, current, next_s, meta_lr)

        # Meta-learner: adjust learning rate based on surprise
        smoothed_error = (1 - META_SMOOTH) * smoothed_error + META_SMOOTH * e_meta
        if smoothed_error > SURPRISE_THRESHOLD:
            meta_lr = min(META_LR_MAX, meta_lr * META_UP_FACTOR)
        else:
            meta_lr = max(META_LR_MIN, meta_lr * META_DOWN_FACTOR)

        # Log
        err_fixed_log.append(e_fix)
        err_meta_log.append(e_meta)
        lr_log.append(meta_lr)
        p_true_log.append(p_change)
        learned_p_fixed.append(M_fixed[0, 1])
        learned_p_meta.append(M_meta[0, 1])

    # ─────────────────────────────────────────
    # Visualisation
    # ─────────────────────────────────────────
    win = 80
    smooth = lambda v: np.convolve(v, np.ones(win)/win, mode="valid")

    fig, axes = plt.subplots(3, 1, figsize=(13, 9), sharex=True)

    # Panel 1 – Prediction error
    ax = axes[0]
    ax.plot(smooth(err_fixed_log), label="Fixed LR", alpha=0.8, linewidth=0.9)
    ax.plot(smooth(err_meta_log),  label="Meta-Learning", alpha=0.8, linewidth=0.9)
    for i in range(1, len(P_VALUES)):
        x = i * REGIME_LENGTH
        if x < NUM_STEPS:
            ax.axvline(x, color="gray", linestyle=":", alpha=0.5)
    ax.set_ylabel("Smoothed Squared Error")
    ax.set_title("Prediction Error  –  Fixed LR vs. Meta-Learning Agent")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)

    # Panel 2 – Learning rate
    ax = axes[1]
    ax.plot(lr_log, color="darkorange", linewidth=0.8)
    ax.axhline(FIXED_LR, color="steelblue", linestyle="--", alpha=0.6,
               label=f"Fixed LR = {FIXED_LR}")
    for i in range(1, len(P_VALUES)):
        x = i * REGIME_LENGTH
        if x < NUM_STEPS:
            ax.axvline(x, color="gray", linestyle=":", alpha=0.5)
    ax.set_ylabel("Learning Rate η")
    ax.set_title("Adaptive Learning Rate (Meta-Learner)")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_yscale("log")

    # Panel 3 – Learned vs. true transition probability
    ax = axes[2]
    ax.plot(learned_p_fixed, alpha=0.5, linewidth=0.7, label="Fixed LR  P(1|0)")
    ax.plot(learned_p_meta,  alpha=0.5, linewidth=0.7, label="Meta-LR   P(1|0)")
    ax.step(range(NUM_STEPS), p_true_log, where="post", color="red",
            linestyle="--", linewidth=1.2, label="True P(switch)")
    for i in range(1, len(P_VALUES)):
        x = i * REGIME_LENGTH
        if x < NUM_STEPS:
            ax.axvline(x, color="gray", linestyle=":", alpha=0.5)
    ax.set_ylabel("P(state change)")
    ax.set_xlabel("Time Step")
    ax.set_title("Learned vs. True Transition Probability")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.suptitle("Meta-Learning Under Regime Shifts", fontsize=13, y=0.99)
    fig.tight_layout()
    plt.show()

    # ── Summary ──
    half = NUM_STEPS // 2
    print("\n─── Results ───")
    print(f"Mean error (2nd half) – Fixed LR:      {np.mean(err_fixed_log[half:]):.4f}")
    print(f"Mean error (2nd half) – Meta-Learning:  {np.mean(err_meta_log[half:]):.4f}")
    print(f"Final learning rate (meta):             {meta_lr:.5f}")


if __name__ == "__main__":
    run()
