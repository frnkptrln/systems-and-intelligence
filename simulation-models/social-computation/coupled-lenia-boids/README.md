# Coupled Dynamics: Lenia ↔ Boids

This directory contains a simulation demonstrating multi-model coupling, specifically illustrating bidirectional causality across fundamentally different substrate models.

## The Models

1. **Continuous Cellular Automaton (Lenia)**: Represents the "environment" or "caloric mass". It has its own intrinsic dynamics of growth, propagation, and decay based on a continuous convolution kernel.
2. **Agent-Based Swarm (Boids)**: Represents foraging agents traversing the continuous environment.

## Bidirectional Causality

The experiment explores what happens when two separate chaotic/complex systems become mutually dependent:

*   **Upward Causation (Environment $\to$ Agents):**
    *   **Attraction:** The Boids' acceleration vector is modified by a "Foraging Force" that points up the gradient of the Lenia density. They actively hunt high-density zones.
    *   **Survival:** Boids must consume Lenia mass to maintain energy. If they fail to find dense Lenia patches, they stave and die.

*   **Downward Causation (Agents $\to$ Environment):**
    *   **Consumption:** When a Boid feeds, it reduces the Lenia mass in that specific grid cell, suppressing the continuous CA's growth at that node.
    *   **Fertilization:** When Boids migrate, they leave a trace amount of "fertilizer" (waste) that minimally boosts Lenia. More importantly, when a Boid dies, its body undergoes catastrophic decay, massively boosting the localized Lenia density and triggering a new "bloom" of CA growth.

## Emergent Dynamics

Observing this coupled system, you can see patterns reminiscent of macroscopic ecology:
- **Boom and Bust Cycles**: If the Boid population explodes due to high Lenia density, they rapidly overgraze the environment, causing mass starvation. The resultant die-off fertilizes the ground, allowing Lenia to recover and restart the cycle.
- **Herding**: The swarm follows moving Lenia blobs (gliders).
- **Substrate Symbiosis**: Without the Boids dying and fertilizing the ground, the Lenia simulation might collapse to zero due to its volatile growth parameters. Without Lenia, the Boids starve.
