# 🧬 Emergence Explorer – Interactive Web Visualization

A zero-dependency, single-file web application that makes emergence
tangible in the browser.

---

## 🧠 What It Does

Conway's **Game of Life** runs in real time while information-theoretic
measures are computed and displayed live:

| Measure | What it tells you |
|:--------|:------------------|
| **Shannon Entropy H** | How disordered is the field? H=0 → all dead or all alive; H=1 → 50/50 |
| **Spatial MI I(X;Y)** | How correlated are neighbouring cells? High MI → spatial structure |
| **Alive Ratio** | Fraction of alive cells |
| **Population** | Total alive count, updated every frame |

Two scrolling time-series charts show entropy and MI evolving over time.

---

## 🎮 Controls

| Control | Action |
|:--------|:-------|
| Click/drag on grid | Draw cells |
| ⏸ Pause / ▶ Play | Toggle simulation |
| ⏭ Step | Advance one generation |
| 🗑 Clear | Empty the grid |
| 🎲 Random | Randomise 30% fill |
| Speed slider | Adjust frames per second |
| Grid slider | Resize the lattice (32–200) |

## 🧩 Pattern Library

Pre-built patterns you can drop onto the grid:

- **Glider** — the simplest spaceship
- **Blinker** — period-2 oscillator
- **R-Pentomino** — chaos from 5 cells (stabilises after 1103 generations!)
- **Pulsar** — beautiful period-3 oscillator
- **Gosper Glider Gun** — infinite stream of gliders
- **LWSS** — lightweight spaceship

---

## ▶ Run

Simply open the file in any modern browser:

```bash
# Option 1: direct open
open tools/web-explorer/index.html

# Option 2: local server (for strict CORS)
cd tools/web-explorer
python3 -m http.server 8000
# then open http://localhost:8000
```

No build step, no npm, no dependencies.
