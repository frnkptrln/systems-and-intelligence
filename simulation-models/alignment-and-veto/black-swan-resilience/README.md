# Black Swan & Resilience

*A toy network-load simulation with an early-warning pause policy.*

## The Concept

This simulation models load accumulation and redistribution on a selected network. It is
inspired by sandpile models; it is not calibrated to a DAO, market, or infrastructure
network.

Two quantities are compared in this implementation:
1. **Efficiency (Throughput):** Maximizing the rate of load processed by the network.
2. **Toy resilience:** avoiding large modeled cascades under the selected load rule.

The code does not establish a universal efficiency–resilience trade-off, antifragility, or
inevitable power-law tails.

## Key Metrics & Interventions

- **Spectral gap ($\lambda_2$):** Reports algebraic connectivity. Any relation to load
  dissipation is a property to test under this code's redistribution rule, not a general
  graph-theoretic identity.
- **Early-warning statistics:** Monitors variance and lag-1 autocorrelation. These are not
  transfer entropy and are not universal precursors.
- **Pause policy:** Temporarily halts throughput when the selected warning crosses a
  threshold. The comparison should report false alarms, missed cascades, and total
  throughput as well as avoided losses.

The current artifact is an exploratory simulation, not evidence that the policy works in a
real system.

## Running

```bash
python black_swan_simulation.py
```

## Related Theory

- [Black Swans and Downward Causation](../../../theory/emergence/black-swans-and-downward-causation.md)
