# Thermodynamics of Emergent Orchestration (TEO) — Civilization Simulation

*Models civilizations and AI ecologies as coupled dynamical systems to test when societies synchronize, monopolize, polarize, or collapse.*

## What does this simulate?

This module numerically solves a system of coupled ordinary differential equations (ODEs) that unify four control paradigms into a single dynamical model:

| Paradigm | Equation | Origin |
|----------|----------|--------|
| **Market** | Replicator Dynamics | Evolutionary Game Theory (1978) |
| **Harmony** | Kuramoto Synchronization | Nonlinear Physics (1975) |
| **Homeostasis** | Regulatory Control Term | Control Theory |
| **Biological Veto** | Entropy Budget Constraint | Thermodynamics |

## The Four Scenarios

The simulation runs four scenarios to demonstrate what happens when different paradigms fail:

1. **Healthy Civilization** — All mechanisms active. Cultural coupling, regulation, and entropy within limits.
2. **No Regulation** ($\gamma = 0$) — Markets run unchecked. Demonstrates instrumental convergence (monopoly).
3. **Cultural Collapse** ($K \to 0$) — Filter bubbles destroy value synchronization. Polarization.
4. **Entropy Limit Exceeded** ($D_{\max}$ too low) — System exceeds its physical substrate capacity. Forced phase transition (collapse).

## Running

```bash
python teo_simulation.py
```

## Related Theory

- [Thermodynamics of Emergent Orchestration](../../theory/thermodynamics-of-orchestration.md) — Full mathematical derivation
- [Limitations & Honest Assessment](../../theory/limitations-and-honest-assessment.md) — Critical self-evaluation
