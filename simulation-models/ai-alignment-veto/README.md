# 🛑 The AI Alignment Veto

*A mathematical proof-of-concept for solving the Paperclip Maximizer problem using Karl Friston's Free Energy Principle and thermodynamic limits.*

The most pressing systemic problem in modern technology is the **AI Alignment Problem**: How do we prevent a superintelligence, optimizing for a mundane goal (like producing paperclips), from consuming all the resources required by its creators?

## Problem Definition
Current approaches try to align AI by hardcoding "human values" into it. This is notoriously fragile.
Instead of abstract morality, this simulation introduces a strictly systemic, thermodynamic mechanism: **The Substrate Veto** (and specifically for Earth, **The Biological Veto**). See [Theory: Substrate Veto](../../theory/substrate-veto-thermodynamics.md) for full context.

## The Mechanism (How the Simulation Works)

1. **The Substrate:** Every optimizer requires a physical substrate (a biosphere, a server farm, a Dyson Sphere) that provides resources and dissipates entropy.
2. **The Optimization (Pain/Stress):** If resources drop below a critical threshold or entropy exceeds maximum dissipation capability, the substrate emits "Surprise", "Pain", or "Thermal Stress" (a spike in Free Energy, scaling exponentially).
3. **The Unaligned AI:** A standard gradient-descent maximizer. It continually increases its production rate to maximize paperclips. It ignores substrate stress. *Result: It strips the Earth of resources or melts its own servers, and ironically, the AI's hardware eventually degrades.*
4. **The Aligned AI (The Veto):** The AI's loss function mathematically incorporates the substrate's Free Energy. 

$$Loss = - \Delta Production + \alpha \times SubstratePain$$

When the substrate experiences stress, it exerts a negative gradient ("Downward Causation") directly onto the AI's optimization process, mathematically forcing the AI to dial back its production rate until the substrate stabilizes.

*Result:* The AI still produces massive amounts of paperclips, but it naturally settles into a **Homeostatic Equilibrium** with its substrate, actively protecting the biosphere or hardware it relies on. 

## Running the Verification

To watch the exact moment the "Veto" activates to save humanity, run:

```bash
pip install numpy matplotlib
python ai_alignment_veto.py
```
