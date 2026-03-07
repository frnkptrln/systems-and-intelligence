# System Intelligence Index (SII)

*Exploratory notes on how to think about "intelligence" as a property of systems.*

---

## 1. Motivation

When we talk about *intelligence*, we often think of agents: humans, animals,
machines. But many of the phenomena that interest us in complex systems
look "intelligent" without any explicit agent:

- ecosystems that regulate themselves  
- markets that react to shocks  
- infrastructures that re-route around failures  
- technical systems that maintain service under changing load  

Instead of asking *"Is this system intelligent, yes or no?"*, it can be more
useful to ask:

> **"To what degree does this system behave intelligently?"**

The **System Intelligence Index (SII)** is a tentative way to structure that
question.

It is not meant as a precise metric, but as a **conceptual scaffold**:
a way to decompose "intelligence" into dimensions that can be observed,
simulated, and eventually quantified.

---

## 2. Intelligence as a System Property

In this context, a *system* is any configuration of interacting components:

- cells in a cellular automaton  
- services in a software architecture  
- species in an ecosystem  
- agents in an economy  

We call a system *intelligent* (in a weak sense) if it exhibits:

1. **Predictive structure** – it encodes regularities of its environment or of
   its own dynamics.
2. **Regulatory capacity** – it can maintain some internal variables within
   viable bounds.
3. **Adaptive flexibility** – it can change its own behaviour or structure in
   response to perturbations.

The **System Intelligence Index** is meant to reflect these three aspects.

---

## 3. Three Core Dimensions

We can think of the SII as a product (or composition) of three factors:

\[
\text{SII} \approx P \times R \times A
\]

where:

- \( P \) = **Predictive Power**  
- \( R \) = **Regulation Ability**  
- \( A \) = **Adaptive Capacity**

Each factor can be explored separately in simulations and models.

### 3.1 Predictive Power (P)

**Question:**  
How well does the system anticipate what will happen next?

In many models, "prediction" appears as:

- internal transition matrices that match the world's dynamics  
- low prediction error over time  
- internal representations that compress regularities in the environment  

Possible operationalisations:

- inverse of long-term prediction error  
- mutual information between internal state and future environment state  
- convergence of internal models to external dynamics  

In your nested-learning demos, \( P \) is high when the observer's internal
transition matrix closely matches the true Markov process.

### 3.2 Regulation Ability (R)

**Question:**  
How well does the system keep key variables within viable ranges?

Examples:

- homeostatic cellular automata maintaining target density  
- control systems keeping temperature, load, or latency stable  
- organisms maintaining internal variables (pH, glucose, temperature)  

Possible operationalisations:

- inverse of variance around a target value  
- time spent within a defined "viability corridor"  
- robustness under perturbations (how quickly it returns to viable ranges)  

In your ecosystem-regulation models, \( R \) increases when the system can
compensate for shocks (e.g. random deaths) without collapsing or exploding.

### 3.3 Adaptive Capacity (A)

**Question:**  
How capable is the system of changing its own behaviour or structure when
conditions change?

This includes:

- updating internal models when the environment shifts  
- changing parameters (learning rates, thresholds)  
- reconfiguring topology (who interacts with whom)  

Possible operationalisations:

- speed of re-convergence after a regime change  
- capacity to maintain performance across multiple environments  
- diversity of internal models or strategies  

In nested-learning setups, \( A \) shows up when a meta-learner adjusts the
learning rate or strategy of a lower-level learner in response to non-stationary
dynamics.

---

## 4. A Simple Conceptual Formula

For many exploratory simulations, a simple multiplicative structure is enough:

\[
\text{SII} = f(P, R, A) \approx P \times R \times A
\]

Why multiplicative?

- if any factor is **near zero**, the overall intelligence feels low  
  - a system that predicts well but cannot regulate anything  
  - a system that regulates well but never learns  
- if all three are moderately high, the system feels "intelligent" in a
  systems sense, even without consciousness or explicit goals

In practice, each of \( P, R, A \) could be normalised to \([0, 1]\)
or to some bounded interval, and the resulting SII would also live in a
bounded range.

This is not a final definition, but a **working model** to connect:

- predictive models (nested learning)  
- regulatory structures (homeostasis)  
- adaptation mechanisms (meta-learning, plasticity)  

---

## 5. Examples Across Models

To make SII less abstract, here are some informal sketches:

### 5.1 Simple Homeostatic CA

- Predictive Power (P):  
  None in the internal sense – it just applies a rule, no explicit model.  
  → \( P \) ≈ low

- Regulation Ability (R):  
  High, if density hovers around a target with low variance.  
  → \( R \) ≈ high

- Adaptive Capacity (A):  
  Low, if the rule set is fully fixed.  
  → \( A \) ≈ low

Result:  
SII is non-zero (the system is "smart" in regulating density),  
but not very high (no learning, no internal modelling).

### 5.2 Nested Learning Two-State Model

- Predictive Power (P):  
  High, if the learned transition matrix converges to the true dynamics.  
  → \( P \) ≈ high

- Regulation Ability (R):  
  Minimal – the model doesn't regulate a target variable, it only predicts.  
  → \( R \) ≈ low

- Adaptive Capacity (A):  
  Medium – it can adapt its model if the environment changes, but only via
  a simple learning rule.  
  → \( A \) ≈ medium

Result:  
SII is driven by prediction and some adaptation, but lacks explicit
regulation.

### 5.3 Meta-Learning System (Future Work)

A model where:

- a lower-level learner predicts the world  
- a meta-learner tunes the learner (e.g. learning rate, prior assumptions)  
- a regulatory loop keeps performance or error within bounds

could exhibit:

- high \( P \) (accurate internal model)  
- medium to high \( R \) (stable performance under noise)  
- high \( A \) (robust under shifting regimes)

Such systems are good candidates for high SII in simulations.

---

## 6. Limitations and Open Questions

The **System Intelligence Index** is intentionally incomplete.  
Open issues include:

- **Metric choice**  
  How exactly should \( P, R, A \) be measured in different models?

- **Non-multiplicative combinations**  
  In some systems, a weighted sum or more complex function might reflect
  "intelligence" better than a product.

- **Scale and scope**  
  Intelligence at the component level vs. subsystem vs. whole system –
  SII might need to be defined at multiple scales.

- **Goal ambiguity**  
  Regulation requires choosing "what matters". Who or what defines the
  target variables in a given model?

- **Relation to human notions of intelligence**  
  SII says nothing about consciousness, experience, or meaning – it is a
  systems-level view, not a psychological one.

---

## 7. Why Bother?

Even if SII never becomes a "standard metric", it is useful as a **lens**:

- it encourages thinking about **prediction, regulation, and adaptation**
  as separable dimensions  
- it helps compare very different systems (ecosystems, automata, networks)
  along a common conceptual axis  
- it creates a bridge between your **code experiments** and your
  **philosophical questions** about intelligence and systems

Future work in this repository can:

- implement concrete estimators for \( P, R, A \) in specific models  
- explore how changes in architecture or feedback affect SII  
- connect SII to ideas from control theory, information theory, and
  active inference

For now, the **System Intelligence Index** is a **thinking tool** –
a way to structure intuitions and guide the design of new experiments.

---

