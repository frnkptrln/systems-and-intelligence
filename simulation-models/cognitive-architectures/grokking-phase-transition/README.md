# Grokking: Delayed Generalization

*Status: reproduction attempt on a small modular-arithmetic task. A sharp loss change does not by
itself identify an internal algorithm, understanding, intelligence, or a universal phase
transition.*

Power et al. reported that neural networks trained on some small algorithmic datasets can reach low
training error long before their test performance improves. Continued optimization with particular
regularization and data conditions can then produce delayed, sometimes sharp generalization.

The included script trains an MLP on modular arithmetic with AdamW and weight decay and plots train
and test metrics. Exact timing and final accuracy depend on the split, seed, optimizer, model size,
regularization, hardware, and training duration. A plateau need not be a random walk, and weight
decay is not proof that the model replaces a lookup table with the true algorithm.

## Run

Install the declared dependencies, then execute:

    pip install torch numpy matplotlib
    python grokking.py

Report configuration, seeds, curves, and failures as well as successful runs. Mechanistic claims
require additional analyses such as representation probes, ablations, and comparison with simpler
generalizing solutions.

Reference: Power et al. (2022), *Grokking: Generalization Beyond Overfitting on Small Algorithmic
Datasets*.
