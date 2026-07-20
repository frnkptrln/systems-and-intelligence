# Cognitive Breathing Network

*Part of the Symbiotic Organ Hypothesis framework.*

This directory contains a toy model visualizing **Cognitive Fluidity** (Ego-Dissolution and Re-Individuation) in a Multi-Agent System.

> **Status:** The code merges and splits numerical nodes by construction. “Ego,” “Markov blanket,”
> and “hive mind” are visualization metaphors; the run does not model subjective experience or show
> that agent identities literally dissolve.

## The Premise

The simulation asks how dynamically aggregating and separating agent state changes selected capacity
and diversity proxies under a stipulated stress signal.

### The Breathing Cycle

1. **Aggregation:** Above the chosen stress threshold, the script merges selected vectors and
   capacities into larger red nodes.
2. **Separation:** Below the threshold, the script splits those nodes and adds selected mutations.
   Diversity falls and recovers because these update rules were supplied; long aggregation is not
   proved to cause cognitive suicide.

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
