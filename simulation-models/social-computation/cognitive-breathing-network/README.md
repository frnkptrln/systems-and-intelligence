# Cognitive Breathing Network

*Part of the Symbiotic Organ Hypothesis framework.*

This directory contains a toy model visualizing **Cognitive Fluidity** (Ego-Dissolution and Re-Individuation) in a Multi-Agent System.

## The Premise

In standard Multi-Agent Systems, agents have fixed boundaries (Markov Blankets). They communicate but do not fundamentally merge. This simulation explores what happens when we allow agents to dynamically dissolve their ego-boundaries based on the thermodynamic stress of the environment.

### The Breathing Cycle

1. **Inhalation (Integration/Merging):** When environmental complexity spikes (e.g., a "Black Swan" event), the capacity of individual agents is insufficient. The network undergoes *ego-dissolution*. Agents merge their identity vectors and capacities, forming larger, red "Hive Mind" nodes to pool cognitive resources.
2. **Exhalation (Differentiation/Splitting):** Once the complexity drops, the network *must* exhale. If agents remain merged indefinitely, the system suffers "cognitive suicide" (homogenization/zero entropy). The simulation forces merged nodes to split back into individual blue agents, introducing slight mutations to restore systemic diversity.

## Running the Simulation

Dependencies: `numpy`, `matplotlib`

```bash
python cognitive_breathing.py
```

## What to Observe

- **The Red Line (Stress):** Represents environmental complexity. Watch for the sudden spikes.
- **The Blue Line (Ego Count):** The number of distinct agents. Notice how it drops sharply when stress spikes (agents merge to survive).
- **The Green Line (Diversity):** A proxy for systemic entropy. It drops during merging but recovers as the system "exhales" and agents mutate upon splitting.
- **The Visualization:** Blue dots are distinct individuals. Red dots are merged Hive Nodes. Black lines show the dense local network formed during crisis states.
