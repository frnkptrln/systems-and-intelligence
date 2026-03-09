# 🧠 Cognitive Division of Labor (Latent vs. Introspective Agents)

This simulation demonstrates the architectural implications of the [Asimov / Anthropic Parodox](../../theory/agentic-society-principles.md) in Multi-Agent Systems.

It posits that an efficient agentic society cannot consist solely of "omniscient, hyper-reflective" agents, nor solely of "blind, reactive" agents. Total omniscience causes cognitive paralysis (The Last Answer), while total reactivity causes chaotic inefficiency.

## The Simulation

The simulation runs three isolated resource-gathering societies in parallel:

1. **Pure Latent (Intuition Only):**
   10 agents that move every single tick. They have $R \approx 0$ (no reflectivity). They only see 1 step ahead. They are fast but often wander aimlessly or loop around local minima.
   
2. **Pure Introspective (Reflexion Only):**
   10 agents that calculate the absolute perfect path (A* distance mapping) to the nearest resource. They have $R \approx 1$ (high reflectivity). However, computing this "god-mode" vision takes time. They only move every 5 ticks.

3. **Symbiotic (Action + Reflexion):**
   A mix of 7 Latent and 3 Introspective agents. 
   - The *Introspective* agents act as the slow-moving "consciousness" of the system. While computing their perfect paths, they leave strong gradients ("meaning"/pheromones) in the environment.
   - The *Latent* agents act as the fast-moving "body". They still only see 1 step ahead, but their instincts drive them up the gradients left by the Introspectives.
   
*Result:* The Symbiotic society typically outperforms the others in this toy environment, suggesting that a “division of cognitive labor” (slow reflection shaping fast action through environmental memory) can outperform homogeneous swarms under some conditions.

## Running the Simulation

```bash
pip install numpy matplotlib
python latent_introspective_society.py
```
