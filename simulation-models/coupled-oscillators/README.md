# 🔗 Coupled Oscillators – Emergent Synchronisation

This simulation implements the **Kuramoto model**: a classic model of
how synchronisation emerges from the interaction of many oscillators
with different natural frequencies.

---

## 🧠 Idea

- N oscillators each have their own natural frequency ω_i.
- They are coupled through pairwise sine interactions:

  **dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j − θ_i)**

- Below a critical coupling K_c: oscillators remain **incoherent** (each
  runs at its own speed).
- Above K_c: oscillators spontaneously **synchronise** – a phase
  transition to collective order.

This is the same mechanism behind synchronising fireflies, pacemaker cells,
and coupled neuronal oscillators.

---

## 📊 Order Parameter

The simulation tracks **r(t) ∈ [0, 1]**:

| r | Meaning |
|:--|:--------|
| ≈ 0 | Fully incoherent, random phases |
| ≈ 1 | Perfectly synchronised, all phases aligned |

---

## 🖼 Visualisation

- **Left panel** – unit circle with oscillator phases as dots; red arrow =
  mean field direction and magnitude r
- **Right panel** – order parameter r(t) over time

Press `ESC` to exit.

---

## ▶ Run

```bash
cd simulation-models/coupled-oscillators
python3 coupled_oscillators.py
```

### Experiment ideas

- Set `K_COUPLING = 0.5` → no synchronisation
- Set `K_COUPLING = 4.0` → fast, strong synchronisation
- Increase `N_OSCILLATORS` for a cleaner phase transition


## 📚 References
- **Kuramoto, Y. (1975).** *Self-entrainment of a population of coupled non-linear oscillators.* International Symposium on Mathematical Problems in Theoretical Physics.
