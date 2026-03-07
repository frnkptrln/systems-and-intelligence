# 🔄 Meta-Learning Regime Shift

This simulation extends the [nested-learning two-state model](../nested-learning-two-state/README.md)
by adding **regime shifts** and a **meta-learner** that adapts the learning
rate in response to prediction error.

---

## 🧠 Idea

A two-state Markov system changes its transition probability abruptly every
N steps (regime shift). Two agents learn the system dynamics side by side:

| Agent | Learning Rate |
|:---|:---|
| **Fixed-LR** | Constant η – good baseline |
| **Meta-Learning** | η is adjusted dynamically: high surprise → raise η, low surprise → lower η |

The meta-learner demonstrates **Adaptive Capacity (A)** from the
[System Intelligence Index](../../theory/system-intelligence-index.md):
the ability to change one's own learning behaviour when conditions change.

---

## 🖼 Visualisation

A 3-panel matplotlib figure:

1. **Prediction error** over time – both agents, with regime-shift markers
2. **Learning rate η** of the meta-learner (log scale)
3. **Learned vs. true transition probability** – convergence tracking

---

## ▶ Run

```bash
cd simulation-models/meta-learning-regime-shift
python3 meta_regime_shift.py
```
