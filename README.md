# 🧠 systems-and-intelligence

This repository is a collection of projects focusing on **Complex Adaptive Systems (CAS)**, **Emergent Intelligence**, and **Self-Regulation** in software and simulation models. The goal is to explore how simple, local rules can lead to complex, intelligent, or stable global behavior.

## 📂 Repository Structure

| Folder | Description | Focus |
| :--- | :--- | :--- |
| `simulation-models/` | Code implementing specific models of self-organization (e.g., Cellular Automata, Agent-Based Systems). | **Practical Work** |
| `neural-networks/` | Code and notebooks for AI/ML projects exploring learning and pattern recognition. | **AI/ML** |
| `data-analysis/` | Scripts and utilities for processing, plotting, and statistical evaluation of simulation results. | **Metrics & Validation** |
| `tools/` | Helper scripts, visualization libraries, and general utilities used across projects. | **Utilities** |
| `theory/` | Conceptual write-ups, white papers, and essays detailing the underlying philosophical and mathematical concepts. | **Concepts & Essays** |
| `meta/` | Foundational documents concerning ethics, epistemology, and the fundamental limits of intelligence/computation. | **Philosophy & Ethics** |

---

## 🔬 Featured Project: Ecosystem Regulation

**Path:** `simulation-models/ecosystem-regulation/`

This project demonstrates **Homeostasis** in a cellular automaton. It extends the classic *Game of Life* with a global feedback mechanism that keeps the system's population at a predefined target density while preserving complex local dynamics (pattern growth and decay). 

[Image of the Homeostasis negative feedback loop]


### 📜 The Model: Robust Dynamics (B3/S234 Mod.)

The script `homeostatic_life.py` uses a modified rule set to enforce long-lasting, controlled activity, mimicking a stable ecosystem under constant localized pressure.

#### Rules Summary

| State | Neighbor Count | Outcome (Next Generation) | Rule Type |
| :---: | :---: | :---: | :---: |
| **Live Cell** (`#`) | 2 or 3 | Survives (100% chance) | Survival (S23) |
| **Live Cell** (`#`) | 4 | Survives with **50% probability** | Modified Survival (S4) |
| **Live Cell** (`#`) | $<2$ or $>4$ | Dies (Under/Overpopulation) | |
| **Empty Cell** (` `) | 3 | Birth, **with dynamic probability** ($P_{Birth}$) | Birth (B3) |

#### Homeostasis Mechanism

The birth probability ($P_{Birth}$) is dynamically adjusted in every generation, acting as a negative feedback loop based on the deviation from the target fill ratio ($F_{Target}$):

* If the **Fill Ratio is too low**, $P_{Birth}$ increases.
* If the **Fill Ratio is too high**, $P_{Birth}$ decreases.

---

## 🚀 Installation & Execution

### Prerequisites
Ensure you have Python 3 installed. No external libraries are required.

### Running the Homeostasis Simulation

```bash
# Navigate to the project directory
cd simulation-models/ecosystem-regulation

# Run the simulation
python3 homeostatic_life.py
