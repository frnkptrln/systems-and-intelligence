## Continuous Thought Machines (CTM)

This folder contains a CTM-inspired "thought experiment" model: a recurrent system that computes over an internal time axis ("thought ticks") instead of solving inputs one-shot.

### Why CTM fits this repository

- **Dynamical systems lens**: CTM treats inference as a trajectory, consistent with many simulations here (e.g. relaxation in Hopfield memory, CA evolution, active inference loops).
- **Synchronization as representation**: measuring pairwise temporal alignment echoes the repo's recurring theme that *relations over time* can be more informative than instantaneous state.
- **Adaptive compute as self-regulation**: variable numbers of internal ticks is a computational analogue of homeostasis / regulation under complexity.

### Install

Base dependencies:

```bash
pip install -r requirements.txt
```

Optional (for CTM / PyTorch-based simulations):

```bash
pip install -r requirements-ml.txt
```

### Contents

- `ctm/`: small reusable building blocks (starting with Neuron-Level Models / NLMs).

