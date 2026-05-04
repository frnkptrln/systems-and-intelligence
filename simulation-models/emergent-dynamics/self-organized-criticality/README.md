# ⚡ Self-Organized Criticality – Bak's Sandpile

This simulation implements the **Bak-Tang-Wiesenfeld sandpile** (1987),
the canonical model of **self-organized criticality (SOC)**: a system
that drives itself to a critical state where perturbations trigger
avalanches of all sizes, following a **power-law distribution**.

---

## 🧠 Idea

1. Drop a grain of sand on a random cell.
2. If any cell has ≥ 4 grains, it **topples**:
   - loses 4 grains
   - each of its 4 neighbours gains 1 grain
3. Toppling can cascade → **avalanches**
4. Grains at the boundary are lost (**open boundaries** = dissipation).

After a transient phase, the system reaches a **critical state** where:

| Property | Value |
|:---------|:------|
| Small avalanches | Very frequent |
| Large avalanches | Rare but inevitable |
| Size distribution | P(s) ~ s^(−τ),  τ ≈ 1.1 – 1.3 |
| Tuning required | **None** – criticality is self-organized |

### Why is this mind-blowing?

Most phase transitions require precise parameter tuning (temperature
at exactly the Curie point, coupling at exactly K_c). The sandpile
tunes **itself** to criticality – no external hand needed. This is why
power laws appear everywhere:

- **Earthquakes** (Gutenberg-Richter law)
- **Forest fires** (fire size distribution)
- **Neural avalanches** (Beggs & Plenz, 2003)
- **Financial crashes** (Mandelbrot)
- **Extinction events** (punctuated equilibrium)

---

## 🖼 Visualisation

Two-panel display:

| Panel | Content |
|:------|:--------|
| **Left** | Current sandpile height map (sand-coloured heatmap) |
| **Right** | Log-log plot of avalanche size distribution with fitted power-law exponent τ |

The power law becomes visible after a few thousand grains, and gets
cleaner with more data. The fitted τ is displayed as a dashed line.

Press `ESC` to exit.

---

## 🔗 Connection to System Intelligence

- **Regulation (R):** The average height self-regulates near 2.0 –
  too much sand → large avalanches dissipate it
- **Predictive Power (P):** While individual avalanches are
  unpredictable, the *distribution* is perfectly lawful
- **The deep point:** In SOC, the system is at the boundary between
  order and chaos – where many theorists believe computation and
  intelligence are maximised

---

## 📚 References

- Bak, P., Tang, C. & Wiesenfeld, K. (1987). *Self-organized
  criticality: An explanation of 1/f noise*. Physical Review Letters.
- Bak, P. (1996). *How Nature Works: The Science of Self-Organized
  Criticality*. Copernicus.
- Beggs, J. M. & Plenz, D. (2003). *Neuronal avalanches in neocortical
  circuits*. Journal of Neuroscience.

---

## ▶ Run

```bash
cd simulation-models/self-organized-criticality
python3 sandpile.py
```

### Experiment ideas

- Increase `NUM_GRAINS` to 200000 for a cleaner power law
- Try `GRID_SIZE = 128` for larger avalanches (slower)
- Drop grains only in the centre: `r = c = GRID_SIZE // 2`
  → beautiful symmetric patterns
