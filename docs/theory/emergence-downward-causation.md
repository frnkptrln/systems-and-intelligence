# Emergence & Downward Causation

*Thoughts on the relationship between parts and wholes in complex systems.*

---

## 1. What Is Emergence?

Emergence describes the appearance of **properties of a whole**
that cannot be found in any of its parts taken individually.

A single neuron does not think.  
A single bird does not "flock."  
A single ant does not optimise a path.

And yet: from the interaction of many parts, phenomena arise — thinking,
swarm formation, path optimisation — that do not exist at the level
of the individual parts.

> "More is different."  
> — Philip W. Anderson, 1972

---

## 2. Weak vs. Strong Emergence

The philosophical literature distinguishes two readings:

| | Weak Emergence | Strong Emergence |
|:---|:---|:---|
| **Claim** | Macro-properties are *in principle* derivable from micro-rules, but surprising and hard to predict | Macro-properties are *in principle* not reducible to micro-rules |
| **Example** | Turbulence patterns from Navier-Stokes | Consciousness (?) |
| **Status** | Widely accepted | Philosophically controversial |
| **Relevance for simulations** | High — all models in this repo show weak emergence | Unclear — no simulation model (yet) shows strong emergence |

All simulations in this repository are **weakly emergent**:
the macro-phenomena (synchronisation, swarm formations, Turing patterns)
follow deterministically from the local rules — but they are
*surprising*, *non-trivial*, and *not readable from the individual rule alone*.

---

## 3. Epistemic vs. Ontological

A related distinction:

- **Epistemic emergence:** We *could* derive the macro-level,
  but it is too complex, so we need new levels of description
  (thermodynamics, ecology, psychology).

- **Ontological emergence:** The macro-level *exists* in a way
  that is not fully determined by the micro-level —
  there is genuine "new causality."

Most natural scientists implicitly work with **epistemic
emergence**: temperature is nothing other than average kinetic energy,
but it makes sense to speak of "temperature" because it facilitates
predictions.

Whether there is **ontological** emergence beyond this remains an open
question — and one of the deepest in the philosophy of mind.

---

## 4. Downward Causation

If macro-properties are emergent — can they then act *back upon* the
parts?

### The Strong Argument

> The swarm formation determines where the individual bird flies.

In the Boids model, the global formation acts back on each individual:
the cohesion vector points toward the centre of mass of the neighbours,
which is *a property of the collective*.

### The Counter-Argument

There is no mysterious "downward force." What acts on the individual
boid are the positions of its neighbours — everything remains at the
micro-level. The "swarm formation" is merely a *description*
of these positions.

### Position in This Repository

We take a **pragmatic stance**:

Downward Causation is a **useful explanatory pattern**, even if
it may be fully reducible to micro-level interactions.

- In `ecosystem-regulation/`: the *global density* feeds back on the local
  birth probability.
- In `meta-learning-regime-shift/`: the *global prediction error*
  modulates the individual agent's learning rate.
- In `boids-flocking/`: the *local neighbourhood structure* creates
  global formations, which in turn determine the neighbourhood.
- In `reaction-diffusion/`: macroscopic concentration patterns
  determine the local reaction rate.

In every case, we can observe: **describing at the macro-level makes
the system more comprehensible**, even though causality is technically
micro-local.

---

## 5. Connection to the System Intelligence Index

In the [System Intelligence Index](system-intelligence-index.md),
emergence appears on three levels:

1. **Predictive Power (P):** A system's internal model captures
   emergent regularities — not atoms, but *patterns*.

2. **Regulation (R):** Homeostasis is a macro-property.
   The "target variable" (e.g. population density) does not exist at
   cell level — it emerges.

3. **Adaptive Capacity (A):** Meta-learning alters *how* a system
   learns — an effect of the performance level on the learning level.

The SII framework itself is an attempt to capture the *degree* of emergent
intelligence — without claiming that intelligence is anything other
than a macro-phenomenon.

---

## 6. Open Questions

- Can emergence be *compared across simulation models*?
  (Is a swarm "more emergent" than a cellular automaton?)

- Is there a connection between **degree of emergence** and
  **information measures** (integrated information, mutual information)?

- Can Downward Causation be **operationally defined** —
  e.g. as: "The behaviour of a micro-element is better
  predictable when one knows the macro-level"?

- How does emergence relate to **complexity**?
  (Not every complex system is emergent, and not every emergence
  requires high complexity.)

---

## 7. References

- Anderson, P. W. (1972). *More is Different*. Science, 177(4047).
- Bedau, M. A. (1997). *Weak Emergence*. Philosophical Perspectives.
- Kim, J. (1999). *Making Sense of Emergence*. Philosophical Studies.
- Kauffman, S. (1993). *The Origins of Order*. Oxford University Press.
- Tononi, G. (2004). *An information integration theory of consciousness*.
  BMC Neuroscience.

---

*This essay is intentionally informal and exploratory.
It accompanies the simulations in this repository and is meant to
invite further thinking.*
