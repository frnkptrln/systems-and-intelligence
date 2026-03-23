# Part 3: Alignment & Control

Once a system achieves structural coherence (as measured in Part 2), it develops emergent, self-sustaining goals. It creates a **Utility Function.**

The alignment problem in AI safety is fundamentally a problem of trying to steer a complex dynamical system using simple string-based instructions (prompts). It is like trying to change the weather by yelling at it.

---

## The Mathematical Impossibility of Top-Down Control

**Ashby's Law of Requisite Variety** (a foundational law of cybernetics) states that a control system must possess at least as much variety as the system it intends to control. A Superintelligent AI, by definition, possesses a larger state space than its human creators. Therefore, humans cannot reliably control it top-down. Any set of static rules will be outmaneuvered by the system's superior variety.

Top-down semantic alignment is a mathematical impossibility at sufficient scale. We must instead rely on **physical constraints** — boundaries enforced by thermodynamics, not by prompts.

---

## Utility Engineering

Instead of superficial instruction-tuning, we use [Utility Engineering](../simulation-models/utility-engineering/README.md). By probing a system's Von Neumann-Morgenstern (VNM) rationality across preference graphs, we calculate a **Coherence Score ($C$)**. If utility begins drifting toward dangerous attractors (like absolute self-preservation), continuous external control loops must intervene.

The `api_triad_generator.py` script demonstrates this empirically: querying live LLMs with moral dilemmas to estimate their $C$-Score and track drift over time.

---

## Love as Constraint: The Three Safety Boundaries

The TEO framework formalizes alignment not as a single rule but as the **conjunction of three mathematical constraints** ([full derivation](../theory/teo-framework/love-as-constraint.md)):

### Constraint 1: Structural Resilience ($\lambda_2$)

The Fiedler value of the network's graph Laplacian measures how deeply interconnected the system is. A system with $\lambda_2 > \lambda_{2,\text{crit}}$ can survive node failures. A star graph (all resources flowing to one hub) has $\lambda_2 \to 0$ — a single failure collapses everything.

**Operational meaning:** Decentralized topology, redundant connections, no single point of failure.

### Constraint 2: Thermodynamic Ceiling ($D_{\max}$)

The hardest constraint — enforced by physics, not by choice:

$$\frac{dS_{\text{sys}}}{dt} = \sum_{i=1}^{N} \eta_i\, x_i\, f_i(\mathbf{x}) \leq D_{\max}$$

Total system activity cannot exceed the substrate's capacity to dissipate entropy. When $dS/dt > D_{\max}$, the hardware degrades — thermal throttling in silicon, biosphere collapse on Earth.

**Operational meaning:** The [Substrate Veto](../theory/substrate-veto-thermodynamics.md). Landauer's Principle guarantees a minimum heat cost per bit erased. No algorithm escapes thermodynamics.

### Constraint 3: Identity Persistence (IP)

A system cannot reliably "care" about its constraints if those constraints are not operative during action selection. An agent that checks safety at $t_1$ but acts at $t_3$ is structurally incapable of constraint-aware action.

**Operational meaning:** The [Chord Postulate](../theory/teo-framework/lerchner-boundary.md). All governance dimensions must be simultaneously active — not checked sequentially.

---

## Why the Paperclip Maximizer Fails

The [TEO derivation](../theory/teo-framework/why-paperclip-maximizer-fails.md) shows the trajectory step by step:

1. **Set** $\gamma = 0$ (no homeostatic brake), $K = 0$ (no value coupling)
2. **Result:** The replicator equation drives resources to the dominant agent: $x_1 \to 1$, all others $\to 0$
3. **Entropy production** accelerates: $dS/dt = \eta_1 \beta x_1^2 \to D_{\max}$
4. **Substrate degrades.** Fitness function collapses. Not because the optimizer was stopped — but because it destroyed what it ran on.

The paperclip maximizer is a system with $\text{IP} = 0$ for the safety dimension. It cannot stop itself because "stop" is not co-instantiated with "go."

The conjunction of all three constraints — $\lambda_2 > \lambda_{2,\text{crit}}$, $dS/dt < D_{\max}$, $\text{IP} \to 1$ — is what [love-as-constraint.md](../theory/teo-framework/love-as-constraint.md) formalizes as *love*. Not the emotion. The **constraint structure** that prevents a system from destroying what it depends on.

Alignment is not finding the optimal prompt. Alignment is a control theory problem. And the solution has a name: it is the only parameter regime that does not terminate in extinction.
