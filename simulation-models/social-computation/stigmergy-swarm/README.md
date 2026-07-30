# 🐜 Stigmergy Swarm – Collective Intelligence Through Pheromone Trails

This simulation demonstrates **stigmergy**: agents that communicate
*indirectly* through modifications of their shared environment.

Ant-like agents search for food on a 2D grid. When an agent finds food it
carries a unit back to the nest, depositing **pheromone** along the way.
Other agents are probabilistically attracted toward higher pheromone
concentrations – so successful paths get reinforced automatically.

No agent has any global knowledge. Yet over time the swarm converges on
efficient routes from nest to food.

**Scope:** This is a forward path-formation demonstration. It does not move the
food after convergence, compare decay policies, or measure recovery from stale
traces. “Collective intelligence” here means selected route efficiency, not a
group mind.

---

## 🧠 Key Concepts

- **Stigmergy** – indirect coordination via environmental traces
- **Self-organization** – global structure from local rules
- **Positive feedback** – successful paths attract more traffic
- **Evaporation** – unused paths decay, which can reduce lock-in at a chosen rate

Positive feedback and persistence create a trade-off. Slow decay can preserve
useful paths and also preserve an obsolete attractor after the world changes;
fast decay can improve adaptation while discarding coordination work. The
AGI-26 [trace-field study](https://doi.org/10.1007/978-3-032-33195-3_7)
measures that trade-off in a separate bounded simulator. This repository's
model has not yet reproduced that result.

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

## Next controlled extension

Move or replace the food source after a frozen convergence time and compare
trace-free, fixed-decay, multiple-timescale, provenance-aware invalidation, and
targeted-reset arms. Report pre-shift reward, coverage, and time to recover
rather than selecting one decay rate after seeing the result. The design
principles and effective-control boundary are in
[Agentic Society Principles](../../../theory/identity/agentic-society-principles.md#stigmergic-memory)
and [The Agent Is Not Where the Model Ends](../../../theory/identity/the-agent-is-not-where-the-model-ends.md#7-memory-outside-the-agent).
