# Active Inference (The Free Energy Principle)

This module provides a runnable, mathematical demonstration of Karl Friston's **Active Inference Framework**, which forms the neurobiological foundation spanning Part 1 and Part 2 of this repository.

## The Core Concept

Current AI models (LLMs) operate using a discrete objective function: *Predict the next token*. 

Biological systems (and continuous agentic AI) operate using a different function: ***Minimize Variational Free Energy***, which is a mathematical proxy for "Surprise" or prediction error.

When an agent encounters a discrepancy between its internal model (expectation) and sensory input (reality), it has exactly two ways to minimize that Free Energy:

1. **Perception**: Change internal beliefs to match the world.
2. **Action**: Change the world to match internal beliefs.

Goal-directed behavior (intelligence) is not programmed; it emerges naturally as the system attempts to make the environment fit its internal prior predictions.

## The Simulation

The script `active_inference_simulation.py` formally implements these two gradient descent mechanisms:

- $\frac{\partial F}{\partial \mu}$ (Perceptual update: changing beliefs)
- $\frac{\partial F}{\partial a}$ (Active update: executing actions)

### Running the Code
```bash
python active_inference_simulation.py
```

### Interpretation of Results

The simulation runs three scenarios:

1. **Perception Only (The Observer):** The system encounters an environment (State=0.0) that contradicts its prior expectation (State=1.0). Unable to act, it updates its internal beliefs to accept reality. The prediction error drops, but the world remains unchanged.
2. **Action Only (The Pure Agent):** The system cannot update its beliefs (dogmatic prior). To minimize the massive prediction error, it exerts energy (Action) to physically alter the world state from 0.0 to 1.0.
3. **Active Inference (The Balanced Mind):** The system simultaneously updates its beliefs and acts upon the world, finding the mathematically optimal homeostatic balance that minimizes total Free Energy.

**Conclusion:** Alignment cannot be achieved by merely teaching a model what is "good" (Perception). If a model's internal generative goal (Prior Preference) conflicts with human reality, it will inevitably generate Actions to alter human reality to match its goals.


## �� References
- **Friston, K. (2010).** *The free-energy principle: a unified brain theory?* Nature Reviews Neuroscience, 11(2), 127-138.
