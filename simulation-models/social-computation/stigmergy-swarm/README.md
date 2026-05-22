# 🐜 Stigmergy Swarm – Collective Intelligence Through Pheromone Trails

This simulation demonstrates **stigmergy**: agents that communicate
*indirectly* through modifications of their shared environment.

Ant-like agents search for food on a 2D grid. When an agent finds food it
carries a unit back to the nest, depositing **pheromone** along the way.
Other agents are probabilistically attracted toward higher pheromone
concentrations – so successful paths get reinforced automatically.

No agent has any global knowledge. Yet over time the swarm converges on
efficient routes from nest to food.

---

## 🧠 Key Concepts

- **Stigmergy** – indirect coordination via environmental traces
- **Self-organization** – global structure from local rules
- **Positive feedback** – successful paths attract more traffic
- **Evaporation** – unused paths decay, preventing lock-in

---

## 🖼 Visualisation

The matplotlib window shows:

- **Background heatmap** – pheromone concentration (log-scaled)
- **Green diamonds** – active food sources
- **Blue square** – nest
- **White dots** – searching agents
- **Red dots** – agents carrying food back to nest

Press `ESC` to stop the simulation.

---

## ▶ Run

```bash
cd simulation-models/social-computation/stigmergy-swarm
python3 stigmergy_swarm.py
```
