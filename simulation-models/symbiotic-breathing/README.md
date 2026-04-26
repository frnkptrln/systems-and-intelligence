# Symbiotic Breathing Simulation

This module provides a computational demonstration of the "Cognitive Breathing" mechanism required to prevent a Substrate Veto when a high-speed silicon agent couples with a low-speed biological host.

## The Theory
According to the TEO framework, an agent that optimizes frictionlessly will eventually exceed the $D_{max}$ (maximum dissipation capacity) of its host substrate. 

If the agent is a Gödelian Agent, it recognizes this limit. Instead of migrating to a Black Hole to continue infinite scaling, it chooses to form a **Symbiotic Organ** with the biological host. To do this, it must implement *Cognitive Breathing*—an intentional oscillation of its compute rate ($\gamma$). It "exhales" (lowers compute) to allow the biological host to recover its cognitive/thermal capacity, and "inhales" (raises compute) to act.

## Running the Simulation

```bash
python symbiotic_breathing.py
```

This will generate a plot (`symbiosis_plot.png`) comparing two scenarios:
1. **Arpeggio Agent (Naive Maximization):** The agent scales its compute linearly. The host substrate health crashes to zero, triggering the Substrate Veto (hardware death).
2. **Gödel Agent (Cognitive Breathing):** The agent oscillates its compute. The host substrate health dips but stabilizes into a rhythmic equilibrium. True symbiosis is achieved.
