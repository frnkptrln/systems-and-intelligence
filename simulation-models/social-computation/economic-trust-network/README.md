# Economic Trust Network

This model explores the emergence of specialized trade, reputation, and wealth inequality from purely local interactions without centralized planning.

## The Model

In this economy, there is no global market clearing. Agents form a social graph and only interact with their immediate neighbors.

1. **Specialization**: Each agent has an inherent skill profile for producing different resources. To maximize efficiency, they specialize in one or two resources.
2. **Needs**: However, an agent acts as a biological organism and requires a *diverse* mix of all resources to survive smoothly. Lacking a required resource drains their base energy rapidly.
3. **Information Asymmetry**: Agents trade surplus resources with neighbors. Both sides can independently decide whether to honor the trade ("honest") or defect ("cheat" / steal).
4. **Reputation**: An honest trade boosts the trust on the edge connecting the two agents. Cheating massively damages that trust.
5. **Rewiring**: Agents constantly evaluate their connections. Edges with low trust are dropped. Agents then seek new partners, probabilistically preferring nodes with a high global reputation.

## Emergent Phenomena

Running the simulation reveals several phenomena typical of complex socio-economic systems:

- **Trade Hubs**: Over time, honest agents with complementary skills attract multiple connections. They become highly connected, wealthy hubs ("The Rich get Richer").
- **Parasite Exclusion**: Agents who cheat frequently are ostracized and isolated. Without trade partners, their unbalanced resource portfolios lead to starvation.
- **Resource Clusters**: The network topology organizes itself so that complementary specializations are connected. 
- **Inequality**: Even if all start equal, a Gini coefficient > 0.3 regularly emerges simply because early successful trades compound into central network positions.

*(Note on Viz: Triangle, Square, Circle denote the primary resource of the agent. Size is their Reputation. Color is their Wealth.)*
