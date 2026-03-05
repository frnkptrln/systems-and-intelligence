# 🌀 The Self-Reading Universe

*A simulation of intelligence as the substrate of life and the memory of the cosmos.*

This model operationalizes the philosophical synthesis between two recent papers:
1. **Intelligence as the Substrate of Life** (Agüera y Arcas, 2025): Life is computation; "dumb" matter naturally forms Turing-complete structures.
2. **Large Language Models and Emergence** (Krakauer et al., 2025): Intelligence is compression ("less is different"); it is the memory of what worked.

For more theoretical background, see the essay [Emergence and the Origin of Intelligence](../../theory/emergence-origin-intelligence.md).

## How it works

The simulation creates a closed feedback loop between two systems:

1. **The World (Computation / Life):**
   A continuous cellular automaton (CA) representing the raw physical substrate. It generates patterns based on a growth function defined by the parameter `mu` (the physical law).
   
2. **The Memory (Compression / Intelligence):**
   A Neural Network Autoencoder acting as the "Observer". It continually tries to compress the state of the World into a tiny latent space and reconstruct it, producing a *Reconstruction Loss*.
   
3. **Downward Causation (Consciousness):**
   The Universe "wants" to be meaningful. If the loss is too low (the World is dead/static), it is trivial to compress. If the loss is too high (the World is pure noise), it is impossible to compress. 
   
   The simulation dynamically adjusts the physical laws of the CA (`mu`) based on the Autoencoder's error to maintain a "Critical Target Loss". The Universe pulls itself towards the *Edge of Chaos* – becoming complex enough to be interesting, but structured enough to be read.

## Running the Simulation

**Prerequisites:**
```bash
pip install numpy matplotlib torch scipy
```

**Run:**
```bash
python self_reading_universe.py
```

Watch how the "physics" (blue line) adapt as the observer (red line) tries to understand the world.
