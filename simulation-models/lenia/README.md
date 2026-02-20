# 🌌 Lenia – Continuous Cellular Automata

Lenia (Bert Chan, 2019) generalises Conway's Game of Life from
**discrete** to **continuous** in every dimension: continuous space,
continuous time, continuous state. The result: cell-like "creatures"
that move, pulse, grow, and interact – emerging from nothing but a
convolution kernel and a smooth growth function.

> *"Lenia is probably the most beautiful demonstration that complex
> life-like behaviour can arise from simple continuous rules."*

---

## 🧠 How It Works

The system follows a single update equation:

```
A(t + dt) = clip[ A(t) + dt · G(K ∗ A(t)) ]
```

| Symbol | Meaning |
|:-------|:--------|
| **A** | Activity field ∈ [0, 1] – how "alive" each cell is |
| **K** | Ring-shaped convolution kernel – "how alive is my neighbourhood?" |
| **K ∗ A** | Spatial convolution (computed via FFT) |
| **G** | Growth function: G(u) = 2·exp(−(u−μ)²/2σ²) − 1 |
| **dt** | Time step (< 1 for smooth, continuous dynamics) |
| **clip** | Clamp result to [0, 1] |

Key insight: the growth function creates a **Goldilocks zone**. Too
little neighbourhood activity → decay. Too much → also decay. Just right
(u ≈ μ) → growth. This is the same principle behind biological morphogenesis.

---

## 🎨 Parameter Presets

| Preset | μ | σ | R | Pattern |
|:-------|:--|:--|:--|:--------|
| **Orbium** (default) | 0.15 | 0.017 | 13 | Gliding, pulsing organisms |
| Geminium | 0.14 | 0.014 | 10 | Self-replicating cells |
| Smooth Life | 0.30 | 0.050 | 15 | Amoeba-like blobs |

Change `MU`, `SIGMA`, and `KERNEL_R` at the top of the script.

---

## 🖼 Visualisation

The window displays the activity field A as a heatmap with a custom
colourmap (black → electric blue → white). The dynamics are mesmerising:
structures appear, move, collide, and evolve.

Press `ESC` to exit.

---

## 🔗 Connection to System Intelligence

Lenia challenges our categories:

- **Predictive Power (P):** The "organisms" behave predictably once
  formed – they follow trajectories, respond to collisions
- **Regulation (R):** Each creature maintains its form through
  the Goldilocks growth function – a kind of homeostasis
- **Adaptive Capacity (A):** Creatures can deform, merge, and reform
  under perturbation

The philosophical question: are Lenia creatures *alive*? They satisfy
several criteria of life (metabolism, self-maintenance, sensitivity to
environment) – raising the question of where "life" begins.

---

## 📚 References

- Chan, B. W.-C. (2019). *Lenia – Biology of Artificial Life*.
  Complex Systems, 28(3).
- Chan, B. W.-C. (2020). *Lenia and Expanded Universe*.
  ALIFE 2020 Conference.

---

## ▶ Run

```bash
cd simulation-models/lenia
python3 lenia.py
```

Requires: `numpy`, `scipy`, `matplotlib`

### Experiment ideas

- Try `MU=0.14, SIGMA=0.014, KERNEL_R=10` for self-replicating cells
- Increase `GRID_SIZE` to 512 for higher resolution (slower)
- Modify the kernel shape in `make_kernel()` for entirely new physics
