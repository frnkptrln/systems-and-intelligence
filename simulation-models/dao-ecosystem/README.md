# DAO Ecosystem: The Alignment Problem on the Biological Substrate

This project simulates a Decentralized Autonomous Organization (DAO) – or any other macroeconomic superorganism – whose existence depends on a "biological substrate" (humans, cells). The simulation investigates the effects of different **fitness functions** on the survival of the overall system.

## Background

The model illustrates the so-called **Alignment Problem**:
1. Cells work, consuming energy and accumulating entropy ("pain").
2. They produce resources, which are extracted to the superorganism (the DAO).
3. The DAO must return these resources to the cells to ensure its continued existence. *How* it does this decides the life and death of the system.

### Strategy: Capitalism (Cancerous Growth)
The DAO optimizes for maximum profit. Resources are distributed to the *most productive* cells (ROI). Cells that are already weakened (high pain, low energy) receive nothing and eventually die off. In the short term, this maximizes DAO growth, but inevitably leads to the ecological collapse of the substrate.

### Strategy: Homeostasis (Nervous System)
The DAO optimizes for systemic health. It acts as a survival network and strategically routes resources to the cells with the highest pain/lowest energy levels. This reduces short-term profit, but stabilizes the system indefinitely.

## Usage

The script requires only standard Python (no external dependencies).

```bash
# Simulate collapse through profit maximization
python dao_ecosystem.py --strategy capitalism --steps 100

# Simulate sustainable survival through homeostasis
python dao_ecosystem.py --strategy homeostasis --steps 100
```
