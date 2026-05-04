# 🐦 Boids – Emergent Collective Motion

This simulation implements **Craig Reynolds' Boids model** (1987):
each agent follows three simple local rules, and complex flock-like
motion emerges without any central control.

---

## 🧠 Idea

Every boid perceives only its nearby neighbours and applies three
steering forces:

| Rule | Effect |
|:-----|:-------|
| **Separation** | Steer away from neighbours that are too close |
| **Alignment** | Match heading with nearby neighbours |
| **Cohesion** | Steer toward the average position of nearby neighbours |

No boid knows the shape of the flock. Yet the swarm self-organises
into coherent, fluid formations – splitting around obstacles, merging
again, and flowing like a living organism.

### Comparison with Stigmergy Swarm

| | Stigmergy (ants) | Boids (flocking) |
|:---|:---|:---|
| Communication | **Indirect** (pheromone) | **Direct** (local sensing) |
| Goal | Path optimisation | Collective motion |
| Memory | External (environment) | None (stateless) |
| Structure | Trails and networks | Dynamic formations |

Both models produce global order from local rules – but via
fundamentally different coordination mechanisms.

---

## 🖼 Visualisation

The matplotlib window shows:

- **Coloured dots** – each boid, colour-coded by heading (HSV hue =
  flight angle) so aligned sub-flocks share a colour
- **Faint trails** – recent trajectory of each boid
- **Dark background** – simulates a night-sky aesthetic

The world is toroidal (wrap-around edges).

Press `ESC` to exit.

---

## 🔗 Connection to System Intelligence

- **Regulation (R):** The flock maintains cohesion (a target variable)
  without any explicit set-point
- **Adaptive Capacity (A):** When the flock is disrupted, it reforms
  dynamically – no recovery plan needed
- **Emergent structure:** Global formations are not prescribed by any
  individual rule

---

## ▶ Run

```bash
cd simulation-models/boids-flocking
python3 boids.py
```

### Experiment ideas

- Increase `W_SEPARATION` to 4.0 → the flock dissolves into loose gas
- Decrease `R_COHESION` to 5.0 → many small sub-flocks instead of one
- Set `NUM_BOIDS = 500` for dramatic large-flock dynamics (slower)
- Try `MAX_SPEED = 4.0` for fast, chaotic motion
