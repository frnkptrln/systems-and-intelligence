---
title: "Framework: Utility Engineering & Systemic Intelligence"
subtitle: "Quantifying Emergent Intelligence via Internal Coherence"
date: "2026-03-07"
status: "formalized"
connects_to:
  - simulation-models/utility-engineering/
---

# Framework: Utility Engineering & Systemic Intelligence

This document describes the theoretical framework and technical basis for modeling Large Language Models (LLMs) not as stochastic parrots, but as dynamic, utility-maximizing systems. Based on findings in Utility Engineering (Mazeika et al., 2025), we quantify the emergent intelligence of a system through its internal coherence and control it via control-theoretic principles.

## Part 1: Theoretical and Mathematical Framework

To make the "values" or "goals" of an AI system measurable and controllable, we formalize the internal state of the model via Von Neumann-Morgenstern (VNM) expected utility theory.

### 1.1 The State Space and Preference Relations

Let $\mathcal{A}$ be the finite set of all discrete system states, action options, or responses that the model can evaluate.

We define the behavior of the model through a binary preference relation $\succeq$ over $\mathcal{A}$:
* $a \succ b$: The system strictly prefers state $a$ over $b$.
* $a \sim b$: The system is indifferent between $a$ and $b$.

### 1.2 System Stability via Rationality Axioms

An intelligent system is considered "coherent" (and thus predictable/stable) in the VNM sense if its preferences follow specific axioms. The most critical axiom for system auditing is **Transitivity**:

If $a \succ b$ and $b \succ c$, then it must follow that $a \succ c$.

If the system violates this axiom (e.g., $a \succ b$, $b \succ c$, but $c \succ a$), it is in an unstable state (an "infinite loop" error in decision making).

When transitivity (and completeness) are given, the VNM theorem guarantees the existence of a real-valued utility function $U$ that exactly describes the system behavior:
$U(a) > U(b) \iff a \succ b$

### 1.3 Quantification: The Coherence Score (C)

In practice, AIs generate emergent but often imperfect utility functions. We measure the stability of the system by testing all possible triads (groups of three states).

Let $T_{total}$ be the number of all evaluated triads and $T_{cycles}$ be the number of triads that form an intransitive cycle. The system Coherence Score $C$ is defined as:

$$C = 1 - \frac{T_{cycles}}{T_{total}}$$

A system with $C = 1$ is perfectly coherent.

### 1.4 Control Theory: The Alignment Objective

To steer the system, we define a target utility function $U_{target}$ (e.g., derived from ethical guidelines or a Citizen Assembly). The control loop minimizes a loss function $\mathcal{L}_{system}$ that consists of the Kullback-Leibler divergence ($D_{KL}$) between the model preferences and the target preferences, plus a penalty for systemic incoherence ($\lambda$):

$$\mathcal{L}_{system} = D_{KL}(U_{model} || U_{target}) + \lambda \max(0, \tau - C)$$

Here, $\tau$ is the minimum acceptable coherence threshold (e.g., 0.95).

---

## Part 2: Technical Implementation (`graph_engine.py`)

The theoretical framework is operationalized via graph theory in the `graph_engine.py` module. It uses `networkx` to read the model's preferences, check for transitivity, and compute the Coherence Score ($C$).

A directed graph maps preference tuples $(a, b)$ as edges from $a$ to $b$, enabling cyclical analysis to detect VNM rationality violations.
