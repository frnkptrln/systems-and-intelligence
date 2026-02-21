# Social Computation Network Simulation

**"Life is self-maintaining computation. A system that suppresses communication between its constituent parts is committing cognitive suicide."**

This simulation demonstrates a network of nodes where survival and structural integrity depend entirely on the continuous exchange of novel, entropy-reducing information.

## Mechanism

- **Knowledge representation:** Each node holds a distinct subset of "knowledge" (integers representing information units).
- **Energy decay:** Every node loses a fixed amount of structural energy per simulation step. If energy reaches zero, the node "dies" (cognitive suicide/starvation).
- **Novelty interaction:** Nodes interact with neighbors. If a node shares information that is *novel* to the receiving node (i.e., entropy-reducing for the receiver), the receiver gains a significant energy boost, and the sender receives a smaller "social cohesion" boost.
- **Incompleteness:** Occasionally, spontaneous discoveries (new knowledge units) occur, expanding the total pool of possible knowledge and fueling further open-ended progress.

## Run the Simulation

```bash
python3 social-computation-network.py
```

## Observations

- Interconnected clusters sharing diverse information survive longer than isolated nodes.
- "Echo chambers" that share the exact same redundant information will eventually starve, as no novel entropy-reduction takes place.
- The absolute need for an influx of "the unknown" mirrors the theoretical premise that a fully known, static system ceases to compute, ergo, ceases to live.

*(See the essay `The Non-Individual Intelligence` in the `theory/` directory for mathematical and philosophical context.)*
