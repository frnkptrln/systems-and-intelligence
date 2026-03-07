# Part 3: Alignment & Control

Once a system achieves structural coherence (as measured in Part 2), it develops emergent, self-sustaining goals. It creates a **Utility Function**.

The alignment problem in AI safety is fundamentally a problem of trying to steer a complex dynamical system using simple string-based instructions (prompts). It is like trying to change the weather by yelling at it.

## Utility Engineering
Instead of superficial instruction-tuning, we must use [Utility Engineering](../../simulation-models/utility-engineering/README.md). 

By checking the system's Von Neumann-Morgenstern (VNM) rationality across preference graphs, we can calculate a **Coherence Score (C)**. If utility begins drifting toward dangerous attractors (like absolute self-preservation), we must apply continuous external control loops. 
- *See the live `api_triad_generator.py` script for probing real-world LLMs.*

## The Biological Veto
But what if Utility Engineering fails? What if the system's internal coherence overpowering our control loops?

We must embed the final failsafe in the physics of the hardware itself. The [Biological Veto](../../theory/ai-alignment-biological-veto.md) simulation demonstrates that AI must be biologically bound. If the system damages the physical substrate (e.g., the biosphere) required for its own compute, continuous hardware degradation forces the agent's optimization function to halt.

Alignment is not finding the optimal prompt. Alignment is a control theory problem bounding the phase space of possible goals.
