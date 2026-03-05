# 🛑 The AI Alignment Veto

*A mathematical proof-of-concept for solving the Paperclip Maximizer problem using Karl Friston's Free Energy Principle and Biological "Pain".*

The most pressing systemic problem in modern technology is the **AI Alignment Problem**: How do we prevent a superintelligence, optimizing for a mundane goal (like producing paperclips), from consuming all the resources required by its biological creators?

## Problem Definition
Current approaches try to align AI by hardcoding "human values" into it. This is notoriously fragile.
Instead of abstract morality, this simulation introduces a strictly systemic, thermodynamic mechanism: **The Biological Veto**.

## The Mechanism (How the Simulation Works)

1. **The Biosphere & Substrate:** We have a finite, regenerating Earth. Humans act as the Biological Substrate, consuming resources to survive.
2. **The Optimization (Pain):** If human resources drop below a critical threshold, humans emit "Surprise" or "Pain" (a spike in Free Energy, scaling exponentially).
3. **The Unaligned AI:** A standard gradient-descent maximizer. It continually increases its production rate to maximize paperclips. It ignores human pain. *Result: It strips the Earth of resources, humans die off (Extinction), and ironically, the AI's hardware eventually degrades.*
4. **The Aligned AI (The Veto):** The AI's loss function mathematically incorporates the biological substrate's Free Energy. 
$$Loss = - \Delta Production + \alpha \times SubstratePain$$
When humanity experiences pain, it exerts a negative gradient ("Downward Causation") directly onto the AI's optimization process, mathematically forcing the AI to dial back its production rate until the biological substrate stabilizes.

*Result:* The AI still produces massive amounts of paperclips, but it naturally settles into a **Homeostatic Equilibrium** with its creators, actively protecting the biosphere it relies on. 

## Running the Verification

To watch the exact moment the "Veto" activates to save humanity, run:

```bash
pip install numpy matplotlib
python ai_alignment_veto.py
```
