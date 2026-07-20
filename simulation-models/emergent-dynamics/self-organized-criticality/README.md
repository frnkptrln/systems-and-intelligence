# ⚡ Self-Organized Criticality – Bak's Sandpile

This simulation implements the **Bak-Tang-Wiesenfeld sandpile** (1987),
the canonical model of **self-organized criticality (SOC)**. The script
lets a finite open-boundary pile approach a stationary regime and plots
the observed avalanche-size distribution. A power-law claim requires a
fit comparison and finite-size analysis beyond the visual included here.

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
| Large avalanches | Possible and less frequent in typical runs |
| Size distribution | Estimated from the run; model- and size-dependent |
| Tuning required | Slow drive and open-boundary dissipation are built in |

### Why is this mind-blowing?

Many familiar phase transitions are studied by varying a control parameter
through a critical region. The sandpile is a precise example in which slow
driving and dissipation produce scale-rich cascades without tuning such a
parameter to a single value. It motivated comparisons with many empirical
systems, but their power laws and mechanisms must be established separately:

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

The log-log plot and fitted slope are exploratory diagnostics. Establishing a
power law requires testing alternative heavy-tailed distributions, a fitting
range, goodness of fit, uncertainty, and finite-size effects.

Press `ESC` to exit.

---

## 🔗 Connection to System Intelligence

- **Regulation (R):** The average height self-regulates near 2.0 –
  too much sand → large avalanches dissipate it
- **Predictive Power (P):** Individual avalanches vary while aggregate
  distributions can be estimated with uncertainty.
- **Research connection:** Critical regimes are candidates for studying
  information propagation and computation; this simulation does not show
  that intelligence is maximized there.

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
cd simulation-models/emergent-dynamics/self-organized-criticality
python3 sandpile.py
```

### Experiment ideas

- Increase `NUM_GRAINS` to 200000 for a cleaner power law
- Try `GRID_SIZE = 128` for larger avalanches (slower)
- Drop grains only in the centre: `r = c = GRID_SIZE // 2`
  → beautiful symmetric patterns
