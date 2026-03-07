# Black Swan & Resilience

*A simulation balancing efficiency against catastrophic tail risks through active inference and the Biological Veto.*

## The Concept

This simulation models a decentralized network (like a DAO or global market) under constant load. It builds upon Bak's **Self-Organized Criticality (SOC)**, moving the sandpile from a 2D grid to a complex network setting.

Two fundamental opposing forces are explored:
1. **Efficiency (Throughput):** Maximizing the rate of load processed by the network.
2. **Antifragility (Resilience):** Surviving fat-tailed outliers (Black Swans) that emerge inevitably in critically poised systems.

## Key Metrics & Interventions

- **Spectral Gap ($\lambda_2$):** Displays the algebraic connectivity of the network. A higher $\lambda_2$ means better natural dissipation of load, preventing localized clustering.
- **Transfer Entropy Proxy:** The system monitors early-warning signs (rising variance, lag-1 autocorrelation) that precede a regime shift.
- **Active Inference Agent:** An observer that triggers a **Biological Veto**. When the agent predicts a Black Swan, it halts the system's throughput temporarily, allowing the network to dissipate accumulated tension before a catastrophic avalanche destroys the topology.

## Running

```bash
python black_swan_simulation.py
```

## Related Theory

- [Black Swans and Downward Causation](../../theory/black-swans-and-downward-causation.md)
