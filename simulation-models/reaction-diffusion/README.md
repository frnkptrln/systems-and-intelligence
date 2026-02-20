# 🌊 Reaction-Diffusion Morphogenesis – Gray-Scott Model

This simulation implements the **Gray-Scott model**: a two-chemical
reaction-diffusion system that generates **Turing patterns** – spatial
structures (spots, stripes, labyrinths) that emerge from purely local
chemical dynamics.

---

## 🧠 Idea

Two substances **U** (substrate) and **V** (catalyst) diffuse across a
2D grid and react:

- **Reaction:** U + 2V → 3V (autocatalytic growth)
- **Feed:** U is supplied at rate *F*
- **Kill:** V decays at rate *F + k*

The interplay of fast-diffusing U and slow-diffusing V creates
instabilities that grow into stable spatial patterns – exactly the
mechanism Alan Turing proposed in 1952 to explain biological
morphogenesis (zebra stripes, leopard spots, coral structures).

### Gray-Scott equations

```
∂U/∂t = Dᵤ ∇²U − UV² + F(1 − U)
∂V/∂t = Dᵥ ∇²V + UV² − (F + k)V
```

---

## 🎨 Pattern Presets

The pattern type is controlled by the **feed rate F** and **kill rate k**:

| Preset | F | k | Pattern |
|:---|:---|:---|:---|
| **Labyrinthine** (default) | 0.035 | 0.065 | Winding mazes |
| Mitosis | 0.028 | 0.062 | Splitting dots |
| Coral growth | 0.037 | 0.064 | Branching fingers |
| Spots | 0.030 | 0.062 | Stable dot arrays |
| Worms | 0.038 | 0.061 | Wriggling filaments |

Change `F` and `K` at the top of the script to explore.

---

## 🖼 Visualisation

The matplotlib window shows the concentration of substance **V** as a
colour-mapped heatmap. Patterns emerge gradually over the first few
thousand steps and then stabilise into persistent structures.

Press `ESC` to exit.

---

## ▶ Run

```bash
cd simulation-models/reaction-diffusion
python3 reaction_diffusion.py
```

### Experiment ideas

- Compare default labyrinthine patterns with `F=0.028, k=0.062` (mitosis)
- Watch how initial seed placement affects the final pattern
- Increase `GRID_SIZE` to 400 for higher-resolution patterns (slower)
