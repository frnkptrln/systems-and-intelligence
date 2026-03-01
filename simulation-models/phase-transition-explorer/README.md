# 🔥 Phase Transition Explorer – 2D Ising Model

This simulation demonstrates the most fundamental phenomenon in
statistical physics: a **phase transition** between order and disorder.

---

## 🧠 Idea

A 2D lattice of magnetic spins (each +1 or −1) interacts with its
nearest neighbours. The Hamiltonian is:

```
H = −J Σ s_i · s_j       (J = 1, sum over nearest neighbours)
```

At **low temperature**, spins align spontaneously (ferromagnetic order,
|M| ≈ 1). At **high temperature**, thermal noise destroys correlations
(disorder, |M| ≈ 0).

The transition happens sharply at the **Onsager critical temperature**:

```
T_c = 2 / ln(1 + √2) ≈ 2.269
```

### Why this matters for the repository

| Concept | Connection |
|:--------|:-----------|
| **Edge of Chaos** | At T_c, correlations diverge — the system is maximally sensitive and complex |
| **Repo Axiom 2** | H(X) is neither 0 (frozen) nor maximal (noise) — life happens at the edge |
| **Self-Organized Criticality** | The Ising model shows *why* criticality is special; SOC shows how systems *reach* it |
| **System Intelligence** | Near T_c: P (prediction) is maximal, R (regulation) is fragile, A (adaptation) peaks |

---

## 🎮 Controls

| Key | Action |
|:----|:-------|
| `←` / `→` | Decrease / increase temperature by 0.1 |
| `r` | Reset the spin grid |
| `ESC` | Exit |

---

## 📊 What You See

The display shows four panels:

1. **Spin grid** — Red/blue for ±1 spins. Watch domains form and dissolve.
2. **Magnetisation |M|** — Order parameter. Drops from ~1 to ~0 at T_c.
3. **Energy per spin** — Rises from ~−2 (ordered) towards 0 (disordered).
4. **Phase diagram** — Your current (T, |M|) overlaid on Onsager's exact solution.
5. **Energy fluctuations** — Proxy for specific heat C_v. Peaks at T_c.

---

## ▶ Run

```bash
cd simulation-models/phase-transition-explorer
python3 phase-transition-explorer.py
```

### Experiment ideas

- Start at T = 0.5 (deep order) and slowly sweep to T = 4.0 — watch the transition
- Start above T_c and cool down — observe spontaneous symmetry breaking
- Stay at T_c and watch scale-free fluctuations (large correlated domains appear and disappear)
- Reset the grid at T_c and watch how long it takes to reach equilibrium (critical slowing down)
