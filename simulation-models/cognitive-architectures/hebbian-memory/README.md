# 🧬 Hebbian Memory – Self-Organizing Associative Memory

This simulation implements a **Hopfield network** – a fully connected
network of binary neurons (±1) that stores patterns via **Hebb's rule**
and recalls them from noisy or partial input.

---

## 🧠 Idea

- **Storage:** Each pattern is imprinted into the weight matrix using
  the outer-product (Hebbian) rule:

  **W += p ⊗ p / N**

  No teacher, no backpropagation – just correlation-based learning.

- **Recall:** Given a noisy probe, neurons update asynchronously:

  **sᵢ ← sign(Σⱼ Wᵢⱼ sⱼ)**

  The network descends a well-defined **energy function**:

  **E = −½ sᵀ W s**

  and converges to the nearest stored pattern (attractor).

This is the simplest model of **content-addressable memory**: you give
the system a partial cue and it reconstructs the full memory.

---

## 📊 What You See

The visualisation shows three rows:

| Row | Contents |
|:----|:---------|
| **Top** | The 4 stored patterns (T, X, Checker, Diamond) |
| **Middle** | Noisy probe → animated convergence → final recalled pattern |
| **Bottom** | Energy descent over update sweeps; overlap with all stored patterns |

The network recalls each pattern in turn, animating the convergence
from noisy input to clean attractor.

---

## 🔗 Connection to System Intelligence

- **Predictive Power (P):** The weight matrix encodes the statistical
  structure of the stored patterns – the network "knows" what a valid
  pattern looks like.
- **Adaptive Capacity (A):** New patterns can be stored incrementally
  by adding their outer product to W.
- **Attractor dynamics:** The energy landscape creates basins of
  attraction – a form of self-regulation toward valid states.

---

## ▶ Run

```bash
cd simulation-models/hebbian-memory
python3 hebbian_memory.py
```

### Experiment ideas

- Increase `NOISE_LEVEL` to 0.4 or 0.5 – when does recall fail?
- Store 6 or 7 patterns in 64 neurons – observe capacity limits
  (the theoretical limit is ~0.14 N ≈ 9 patterns for N=64)
- Try replacing hand-crafted patterns with random ones via
  `NUM_PATTERNS` and removing `BUILT_IN_PATTERNS`
