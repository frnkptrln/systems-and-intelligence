# ⚡ The Grokking Phase Transition

This module provides a visual, real-time simulation of the "Grokking" phenomenon, representing a critical breakthrough in our understanding of how Artificial Intelligence develops generalized knowledge.

Inspired by the landmark ArXiv paper: **[Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets (Power et al., 2022)](https://arxiv.org/abs/2201.02177)**.

## The Phenomenon

In standard machine learning wisdom, if a model perfectly memorizes its training data but fails on test data, it has severely **overfitted**, and training should be stopped. 

However, OpenAI researchers discovered a bizarre phase transition. If you train a small neural network on an algorithmic task (like modular addition $a + b \mod P$) and keep training it *long after* it has perfectly memorized the training set, something magical happens. The test accuracy suddenly spikes from random guessing to 100%. 

The network abandons its internal "lookup table" (memorization) and collapses its weights into a structured, generalizing graph (understanding/intelligence). It "groks" the underlying rules of the universe.

## The Simulation

The included script `grokking.py` trains a simple Multi-Layer Perceptron (MLP) on modular arithmetic ($P = 97$). It visualizes this thermodynamic-like phase transition in real-time.

1. **Phase 1 (Memorization):** Train Loss plunges to near zero. Train accuracy hits 100%. Test loss remains high and test accuracy stays flat.
2. **Phase 2 (The Plateau):** The model spends thousands of epochs changing its internal weight representations without altering its external accuracy (the "Random Walk" phase). **Weight Decay** slowly acts as Occam's Razor, punishing complex memory tables.
3. **Phase 3 (Grokking):** Test loss abruptly collapses. Test accuracy rockets to 100%. Intelligence has emerged.

## Running the Simulation

You will need PyTorch to run this model. It heavily relies on the optimization process (`AdamW` + `weight_decay`). 
*Note: Depending on your hardware (CPU vs GPU), the phase transition usually occurs between epoch 3,000 and 10,000.*

```bash
pip install torch numpy matplotlib
python grokking.py
```
