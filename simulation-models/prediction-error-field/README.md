# 🔁 Prediction Error Field (Game of Life)

This model implements a 2D **Game of Life** world where each cell is also a
local learner that tries to predict its **own next state** based only on its
8 neighbours.

Over time, the field of learners collectively approximates the underlying
Game-of-Life rule. The prediction error becomes a spatial "surprise field".

---

## 🧠 Idea

- The world is a binary grid (0/1) updated by Conway's Game of Life (B3/S23).
- Each cell:
  - observes its 8 neighbours,
  - forms an input vector `x = [1, N1..N8]`,
  - predicts its own next state with a small weight vector `w` and a sigmoid,
  - sees the *true* next state from the Game-of-Life rule,
  - updates its weights using a simple local error rule.

This creates a **prediction error field** on top of a classic cellular automaton:
a layer of learning dynamics embedded in a layer of physical dynamics.

---

## 🖼 Visualisation

The script shows a live animation with two panels:

- **Left:** current world state (Conway's Game of Life, black/white)  
- **Right:** prediction error per cell (`|prediction − reality|`, heatmap)

Bright regions in the error field indicate where the local models are still
"surprised" by the world's behaviour.

Press `ESC` in the window at any time to stop the simulation.

---

## ▶ Run

From the repository root:

```bash
cd simulation-models/prediction-error-field
python3 prediction_error_field.py

