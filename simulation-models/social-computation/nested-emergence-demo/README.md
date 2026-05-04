## Nested Emergence Demo — Cross-Scale Coherence Propagation

This simulation is a **multi-scale coupling** thought experiment:

- **Bottom scale**: a continuous cellular field (Lenia-like) evolves over time.
- **Top scale**: a Boids-style swarm moves through the world.

The two scales **couple bidirectionally**:

- Bottom → Top: boids sample local field coherence; higher coherence increases alignment (order), lower coherence increases exploration/noise.
- Top → Bottom: boids deposit a density/influence field that perturbs the bottom dynamics.

### What to look for

- **Bottom coherence** rises/falls (spatial smoothness / low local variance).
- **Swarm coherence** rises/falls (velocity alignment order parameter).
- **Lag correlation** between the two time series: a crude indicator that structure propagates across scales with delay.

### Run

```bash
cd simulation-models/nested-emergence-demo
python3 nested_emergence_demo.py
```

Press `ESC` in the window to exit.

