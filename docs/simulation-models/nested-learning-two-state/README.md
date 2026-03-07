# Nested Learning: Two-State World & Observer

This demo shows a minimal nested-learning setup:

- Level 0: A two-state Markov world with fixed switch probability `P_CHANGE`.
- Level 1: An observer that learns a transition matrix `M` to predict the world's next state.

The observer updates its internal model using prediction error between
its probabilistic forecast and the actually observed next state.

This is a tiny illustration of *nested learning*:  
a learning process about another process.

