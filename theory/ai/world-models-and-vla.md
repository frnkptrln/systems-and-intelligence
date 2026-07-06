# World Models and VLA: The Spine, Industrialized (Framing Note)

**Status:** Working Note

**Scope:** Reading two current AI research programs through the repository's instruments: world models as trace → generator at industrial scale, and vision-language-action models as the reconstructed generator coupled back to matter. Not a survey, not a capability forecast — a mapping.

**Epistemic status:** `[HYPOTHESIZED]` mapping over well-documented research lines. The individual observations (model exploitation, causal confusion, Moravec's asymmetry) are established in their home literatures; connecting them as instances of this repository's two directions is the note's contribution.

**Related files:**

- llms-as-probabilistic-automata.md
- ../core/the-generator-question.md
- ../../lab/benchmarks/inverse-reconstruction/README.md
- ../../logs/016_the-runtime-is-part-of-the-generator.md
- ../../logs/017_provenance-depth-and-the-verification-economy.md

**Failure conditions:**

- Claiming contributions to robotics or model-based RL. This note reads those fields; it does not advance them.
- Letting the mapping flatten real differences: a learned latent dynamics model is not a CA rule table, and industrial scale changes what the toy results license.

---

## The claim

The two directions of [the Generator Question](../core/the-generator-question.md) have both become industries, and they arrived as a matched pair `[HYPOTHESIZED]`:

> **A world model is the inverse direction at scale** — a generator reconstructed from traces, so that planning can run inside the reconstruction. **A VLA is the construction direction at scale** — a generator coupled to actuators, so that every output is submitted to matter. Together they close the loop the spine describes: observe traces → reconstruct a generator → act through it → let the referee vote.

## World models: the inverse direction as an industry

From Ha & Schmidhuber's *World Models* (2018) through the Dreamer line (Hafner et al.), LeCun's JEPA program, and action-controllable video models (Genie), the recipe is constant: learn a compressed generator of environment dynamics from observation traces, then plan or imagine inside it. This is trace → generator, executed daily at scale — with Sutton's Dyna (1991) as the ancestor that named the move.

Three of this repository's results describe that industry's known pain points, which is the evidence the mapping carries content:

1. **The learned model is one member of the equivalence class.** A world model consistent with all training traces may still be the wrong generator out of distribution. Model-based RL knows the consequence intimately as **model exploitation**: the policy, optimizing inside the learned model, systematically discovers and exploits the regions where the reconstruction diverges from reality. In this repo's terms: *the policy is an adversarial divergence-query generator running against its own world model* — Total-Rickall logic, with the agent as the interrogator and its own model as the impostor.
2. **Passive traces hit the passive ceiling.** The [intervention experiment](../../lab/benchmarks/inverse-reconstruction/README.md) showed the consistent-generator class does not collapse under watching — only under queries. The industrial instance: world models trained on passive video inherit exactly this underdetermination (imitation learning's **causal confusion** — de Haan et al. 2019 — is the documented case: passive traces cannot distinguish causes from correlates). Action-conditioned data is the intervention protocol; embodiment is not a luxury but the class-collapsing query channel.
3. **The runtime is part of the generator** ([Log 016](../../logs/016_the-runtime-is-part-of-the-generator.md)): a world model's validity is indexed to the embodiment and regime it was trained in — a provenance question ([Log 017](../../logs/017_provenance-depth-and-the-verification-economy.md)'s reference-class field, applied to dynamics models).

## VLA: where the antenna meets the referee

A vision-language-action model couples a corpus-trained core — in the [antenna reading](../identity/psychedelics-as-perturbation.md), a compressed *receiver of the cultural field* — to a physical actuator (RT-2, OpenVLA, π0). Two things happen at that coupling, and both are this repository's themes:

- **The referee changes.** A language model's outputs face a soft referee — plausibility, consensus, resonance. A gripper faces matter. Every VLA action is a performance node: **d = 0 verification at every timestep**, unpurchaseable by fluency. Moravec's paradox, in verification-economy terms: the tasks that look hard (deduction-shaped, corpus-covered) have cheap referees, and the tasks that look trivial (pouring water) have the expensive one. VLAs are where a deduction-shaped intelligence is finally billed at the hard rate.
- **The budgets turn hard by physics.** Entry 14's catastrophe was a dissipation budget left as a sentence in a config file. An embodied agent's torque limits, battery, and breakable environment are budgets *poured in concrete by default* — which cuts both ways: the substrate constraint binds honestly, and the cost of the impostor-generator failure mode (acting on a wrong world model) is paid in atoms, not tokens.

## What follows (and what doesn't)

The pair sharpens the repo's open real-model question: world models *are* learned searchers in generator space, operating far above the [family-search floor](../../lab/benchmarks/inverse-reconstruction/README.md) — and their documented failure modes (exploitation, causal confusion) are exactly what the toy results predict for reconstruction under passive data and open families. Two questions this suggests, both honest extensions rather than claims: does model-exploitation rate track equivalence-class size in controlled settings (a measurable bridge from the benchmark to model-based RL)? And do VLAs exhibit the P8 pattern — capability gains loading physical constraint axes faster than their safety architecture scales?

What does *not* follow: any forecast about robotics timelines, any claim that the toy results transfer quantitatively, any suggestion that this repository's vocabulary improves on the fields' own. The mapping earns its keep only as long as it keeps predicting which failure modes those fields will report next.

> **Related work.** Ha & Schmidhuber (2018), *World Models*; Hafner et al., Dreamer/DreamerV3 (2019–2023); LeCun (2022), *A Path Towards Autonomous Machine Intelligence* (JEPA); Bruce et al. (2024), Genie; Sutton (1991), Dyna; de Haan et al. (2019), *Causal Confusion in Imitation Learning*; Brohan et al. (2023), RT-2; Kim et al. (2024), OpenVLA; Physical Intelligence (2024), π0; Moravec (1988). Mapping in the [Related Work Map](../../meta/research-alignment/related-work-map.md).
