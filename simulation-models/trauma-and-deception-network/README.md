# Trauma & Deception Network

*Part of the Scar Tissue and Epistemic Firewalls framework.*

This simulation demonstrates two deeply counter-intuitive principles of complex systems:
1. **Deception is structurally necessary:** Perfect transparency leads to catastrophic synchronization (fragility).
2. **Forgetting must be catastrophic to be useful:** Survival mechanisms crystallize into permanent "Scars" that reduce efficiency but prevent future death.

## The Mechanics

- **Epistemic Firewalls (Orange):** When local nodes become too synchronized (i.e., they all agree too much), they instinctively deploy firewalls. They stop broadcasting their true state and broadcast noise/lies instead. This acts as a firebreak, preserving network diversity.
- **Black Swan Events (Red Background):** Periodically, the environment shocks the system.
- **Scar Tissue (Black):** If a node is caught in a Black Swan event while highly synchronized (i.e., it failed to deploy a firewall and had no local diversity), it suffers "trauma." Its state permanently crystallizes. It becomes a Scar. Elastic nodes must now route their learning around these dead, rigid monuments to past crises.

## Running the Simulation

Dependencies: `numpy`, `matplotlib`

```bash
python trauma_network.py
```

## What to Observe

Watch how the Global Synchronization line (blue) climbs, triggering the deployment of Active Firewalls (orange). When the red Black Swan zones hit, any parts of the network that failed to deploy firewalls will instantly turn black (Scar Tissue). Over time, the network becomes a topographical history of the traumas it has survived.
