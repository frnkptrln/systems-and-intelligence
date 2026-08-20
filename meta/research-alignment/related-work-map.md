# Related Work Map: Research Alignment Layer

## 1) Purpose

This document maps repository-internal concepts to external research across AI agents, complex systems, active inference, alignment, memory, multi-agent systems, human oversight, and AI consciousness.

It is intended to:
- separate **established results** from **adjacent research**, **repo hypotheses**, **speculative analogies**, and **open problems**;
- identify where repository claims should be strengthened, softened, or tested;
- provide concrete empirical next steps.

The AGI-26 primary-source audit and inclusion decisions for the
situated-competence extension are kept in
[section 7](#7-agi-26-source-audit-and-integration-ledger) below.

## 2) Concept-to-literature matrix

| Concept | Canonical repo file | External anchor papers | Support/challenge from external work | What repo adds | What would weaken repo claim | Suggested next empirical test |
|---|---|---|---|---|---|---|
| Foundations Reconstruction | `theory/core/mathematical-axioms.md` | Eilenberg & Mac Lane (1945); Shannon (1948); Fritz (2020) on Markov categories; Crutchfield & Young (1989) / Shalizi & Crutchfield (2001); Valiant (1984); Wolpert & Macready (1997); Pearl (1995) | **Strong established substrate:** standard Borel spaces and Markov kernels already supply a classical compositional probability theory; computational mechanics already supplies predictive equivalence; learning and decision theory already require tasks and losses. **Challenge:** standard Borel/Markov structure is a scope choice, not an absolutely irreducible foundation, and it excludes quantum and some higher-order processes. | A repository-specific dependency audit: removes the unqualified generator from the primitive basis; separates derived concepts from model supplements and a phenomenal bridge axiom; proves an elementary hidden-extension non-identifiability proposition; identifies which former axioms fail. No novel mathematics claimed. | A strictly weaker basis deriving the same quantitative concepts over the same classical continuous models; an undeclared premise in a derivation; or a required target phenomenon that cannot be represented without a third primitive. | Proof-level work first: attempt a weaker relational/finite basis, test coarse-graining dependence, and identify the smallest causal supplement. Empirical tests begin only after a concrete process model is instantiated. |
| Fractal Architecture of Emergence | `theory/emergence/fractal-architecture-of-emergence.md` | Kim et al. (2025); Park et al. (2023); Beckenbauer et al. (2025) | **Adjacent research:** scaling and multi-agent phase behavior suggest hierarchical structure appears useful, but not proven “fractal” in a strict mathematical sense. | Cross-scale framing linking micro cognition to macro governance and orchestration constraints. | Treating metaphorical self-similarity as universal law without quantitative scale invariance evidence. | Run multi-scale simulations and fit power-law / renormalization-style diagnostics for repeated motifs across levels. |
| Generative Form Systems | `theory/emergence/generative-form-systems.md` | Hutchinson (1981); Barnsley (1986/1988); Lindenmayer (1968); Erdős & Rényi (1960); Wilson (1971) | **Strong formal anchor:** IFS, rewriting systems, random graph thresholds, and renormalization provide real mathematical operators for generated form. **Challenge:** these formalisms do not imply consciousness or agency by themselves. | A disciplined intake spine: operator → iteration → attractor/threshold → measurement → failure condition. | Treating visual or metaphorical similarity as evidence without identifying an operator or measurable invariant. | Compare IFS box dimension, L-system growth metrics, graph thresholds, and coherence transitions as separate generative regimes before claiming cross-scale unity. |
| Consciousness as Global Availability | `theory/identity/consciousness-as-global-availability.md` | Dehaene et al. (1998); Oizumi et al. (2014); Friston/active inference; Markov blanket literature; Gurnee, Sofroniew, Pearce et al. (2026) *Verbalizable Representations Form a Global Workspace in Language Models* — reported internal-inspection evidence of a bounded workspace layer in production LLMs, mapped in `theory/ai/j-space-and-global-availability.md` | **Mixed support:** global workspace, integration, and boundary-maintenance theories provide architectural anchors. **Challenge:** none gives a settled consciousness test, and introspective language remains weak evidence. | Narrows consciousness-adjacent claims to broadcast, integration, boundary maintenance, and perturbation response. | Reducing consciousness to fluent self-report, one metric, or broad network size. | Compare private-module, broadcast-module, and chord-architecture agents under perturbation using Δ-Kohärenz and Identity Persistence. |
| Functional coherence-work hypothesis | `theory/identity/machine-consciousness-as-generator-coherence.md` (legacy title) | Bach & Sorensen (2025/26) *The Machine Consciousness Hypothesis*; von der Malsburg (1997); Graziano (2013); Block (1995) | **Position paper, not evidence.** Limited behaviour can underdetermine internal organization, but neither the source nor this repository proves that every behavioural test is impossible. Functional architecture and phenomenal experience remain distinct. | Translates the proposal into a candidate internal process architecture: conflict detection and commit-time binding under perturbation, with no phenomenal bridge. | Coherence work adds no held-out prediction beyond capacity, memory, or ordinary control; or the effect disappears under matched interventions. | Compare private, broadcast, and commit-time-binding architectures under matched compute; add internal interventions and simpler baselines. |
| Substrate Veto / Biological Veto | `theory/veto/ai-alignment-biological-veto.md` | Wagner et al. (2025); Carichon et al. (2025); Butlin & Lappas (2025) | **Support:** human-in-the-loop and governance literature supports oversight layers. **Challenge:** “veto” can bottleneck safety if operators are overloaded or captured. | Explicit constitutional interface where biological actors can halt optimization trajectories. | Assuming availability, competence, or incorruptibility of human vetoers under adversarial pressure. | Red-team veto latency, false-positive/false-negative rates, and capture resistance in stress-test scenarios. |
| Impedance Matching / Latency as Mercy | `logs/012_latency-as-mercy.md` | Shanahan et al. (2023); Carichon et al. (2025); Wagner et al. (2025) | **Adjacent support:** role/interaction framing and oversight research imply pacing affects controllability. **Challenge:** latency can reduce responsiveness in emergencies. | Reframes delay as a governance affordance, not only a performance defect. | Claiming latency is generally beneficial without context-dependent tradeoff curves. | A/B test policy outcomes vs inserted delay under fast-attack vs deliberative-task regimes. |
| Identity Persistence | `lab/metrics/identity_persistence.py` | Park et al. (2023); Packer et al. (2023); Zhang et al. (2025) | **Support:** long-horizon agent behavior depends on persistent memory and self-model continuity. | A computable metric layer for persistence under perturbation in controlled experiments. | Equating behavioral consistency with stable “identity” without disentangling prompt artifacts. | Benchmark persistence under memory corruption, role swaps, and context-window truncation. |
| Chord vs Arpeggio | `theory/core/thermodynamics-of-orchestration.md` | Beckenbauer et al. (2025); Kim et al. (2025) | **Adjacent research:** synchronization vs sequential coordination tradeoffs are visible in multi-agent orchestration. | Intuitive compositional metaphor linking simultaneity/sequencing to coordination quality and cost. | Overextending metaphor without operational definitions of “chord-like” states. | Define measurable synchrony index and compare collective task performance at matched compute budgets. |
| Mirror Problem | `lab/experiments/mirror_problem.py` | Chalmers (2023); Shanahan et al. (2023); Butlin & Lappas (2025) | **Challenge:** anthropomorphic interpretation of fluent self-description is known risk. **Support:** role-play and self-modeling dynamics are empirically tractable. | Bridges phenomenology-like claims with benchmarkable observer divergence experiments. | Treating introspective language as direct evidence of consciousness or selfhood. | Blind human-evaluator study separating introspective fluency from causal self-model robustness. |
| Three-Layer Memory | `lab/agents/three_layer_agent.py` | Packer et al. (2023); Wei et al. (2025); Zhang et al. (2025) | **Support:** memory tiering and retrieval control are strongly supported design patterns. | Integration with coherence and identity metrics rather than memory alone. | Claiming architecture sufficiency for robust agency without retrieval-quality and conflict-resolution evidence. | Ablation across short/mid/long layers; evaluate coherence, utility drift, and recovery after perturbation. |
| Δ-Kohärenz | `lab/metrics/delta_coherence.py` | Kim et al. (2025); Zhang et al. (2025); Park et al. (2023) | **Adjacent support:** system-level scaling work motivates coherence metrics; direct standardization remains open. | Named metric for temporal coherence shifts under interventions. | Using single metric as proxy for alignment, capability, and safety simultaneously. | Correlate Δ-Kohärenz with independent safety, truthfulness, and coordination benchmarks. |
| Generative Surprise | `theory/core/system-intelligence-index.md` | Park et al. (2023); Shanahan et al. (2023) | **Adjacent support:** creative recombination emerges in agent simulations and role-based generation. | Positions surprise as a monitored signal in system intelligence rather than pure novelty. | Rewarding surprise without guardrails, inducing deceptive or incoherent novelty-seeking. | Controlled novelty-pressure sweeps measuring utility, truthfulness, and harm rates jointly. |
| Utility Engineering / TEO | `papers/quantifying-emergent-utility-in-llms.md` (archived 2026-08-20 — historical early synthesis, not citation-ready) | Mazeika et al. (2025); Carichon et al. (2025) | **Strong support:** explicit utility analysis/control aligns with emergent-value-system literature. **Challenge:** objective misspecification and cross-agent divergence persist. | Connects utility shaping to thermodynamic/economic constraints and constitutional controls. | Presenting utility controls as stable in deployment without distribution-shift validation. | Long-horizon drift tests with adversarial preference perturbations and multi-agent conflict tasks. |
| Epistemic Firewalls | `theory/veto/implementation-patterns-biological-veto.md` | Carichon et al. (2025); Wagner et al. (2025); Butlin & Lappas (2025) | **Support:** isolation boundaries and escalation pathways are common in safety governance. | Treats epistemic compartmentalization as systems architecture, not only policy language. | Excessive compartmentalization causing blind spots and degraded situational awareness. | Simulate cascading-failure scenarios with and without cross-firewall diagnostic channels. |
| Cognitive Breathing | `simulation-models/social-computation/cognitive-breathing-network/README.md` | Beckenbauer et al. (2025); Kim et al. (2025); Park et al. (2023) | **Adjacent support:** periodic exploration/exploitation rhythms are plausible in adaptive coordination. | Formal social-computation simulation motif for contraction/expansion cycles. | Claiming biological analogy implies optimality in digital collectives. | Parameter sweep for inhale/exhale cadence vs resilience, adaptation speed, and instability onset. |
| Human Vital Systems Control Plane | `logs/005_human-vital-systems-control-plane.md` | Wagner et al. (2025); Carichon et al. (2025); Butlin & Lappas (2025) | **Support:** safety-critical sectors require human accountability and layered controls. **Challenge:** centralized control planes may create single points of failure. | Cross-domain proposal connecting infrastructure governance with agentic oversight primitives. | Assuming governance centralization improves robustness without fault-tolerance evidence. | Tabletop + simulation exercises on healthcare/energy/water scenarios with failure injection. |
| Process-model identification (active repository question: Trace → Generator) | `theory/core/mathematical-axioms.md`; `theory/core/the-generator-question.md` | Ljung (1999) *System Identification*; Brunton, Proctor & Kutz (2016) *SINDy*; Schmidt & Lipson (2009); Cranmer (2023) *PySR*; Solomonoff (1964); Pearl (1995) | **Strong established fields and a decisive correction:** known-family identification can be cheap; latent representations can be observationally non-identifiable; causal recovery requires structural and intervention assumptions. P $\ne$ NP does not establish a generic inverse law. | A bounded programme that reports model family, evidence, intervention access, target equivalence, uncertainty, and cost together; measured equivalence classes and intervention effects in controlled cellular-automaton cases. | Any universal hardness or unique-mechanism language; or recovery claims that omit the family and equivalence relation. A strict failure would be the benchmark's effects disappearing under its own preregistered controls. | Continue benchmark comparisons against exact enumeration, SINDy/PySR, learned searchers, and intervention policies under matched budgets; report nulls and non-identifiability separately from compute cost. |
| Witness construction / self-falsifying world models | `theory/core/the-witness-principle.md`; `lab/benchmarks/witness-generation/` | Moore (1956) and Lee & Yannakakis (1994) distinguishing sequences; Goldman & Kearns (1995) teaching dimension; Angluin (1987) active automata learning; de Bruijn (1946) universal cycles; Collins & Shen (2017, 2018) distinguishing experiments; Clarke et al. (2000) CEGAR; active system identification and optimal experimental design; Rosas (2026) adaptive state-action abstraction; Thorpe et al. (2026) query-conditioned embodied world models | **Strong adjacent foundation:** distinguishing tests, selected examples, universal cycles, counterexamples, information gain, and abstraction refinement are established. **Challenge:** generating a useful query is not new by itself, and a fixed full lookup-table family collapses to coordinate coverage. | Inserts an explicit, costed witness-construction operator between candidate-class maintenance and world-coupled intervention; separates candidate distinction geometry from intervention access geometry; derives and exhaustively checks the ECA frontier; proposes witness profiles as an instrument-relative convergence object. No novelty claim for the ingredients. | No benefit over information-gain or rollout search under matched budgets; memorization of fixed query templates; advantage vanishing under noise, intervention risk, compute accounting, or family misspecification. | Vary candidate subsets and access geometries across disjoint finite process families; compare random queries, exact/bounded information-gain search, predictive rollout search, and direct witness generation on unseen cases. |
| Referee boundary in self-revision loops | `lab/benchmarks/recursive-workbench/`; note `ideas/2026-07-24-self-improvement-needs-a-referee.md` | Goodhart (1975) via Manheim & Garrabrant (2018); Campbell (1979) Campbell's law; Mitchell (1982) version spaces — the evidence ceiling is version-space identifiability; Angluin (1987) membership queries — the referee query is a query with the budget moved to the evaluator's side, as in audit sampling; Amodei et al. (2016) reward hacking; Krakovna et al. (2020) specification gaming; Ring & Orseau (2011) delusion box; Everitt et al. (2021) reward tampering; Schmidhuber (2006) Gödel machine; Zelikman et al. (2024) self-taught optimizer (STOP); holdout discipline in ML evaluation and separation of duties in audit practice | **Strong adjacent foundation:** every qualitative effect measured here is established — version-space saturation, active-learning gains, and proxy-gaming are all textbook; holdout sets and separation of duties are standard defense. **Challenge:** the direction of all three effects was predictable in advance; the toy proposer is not an optimized adversary; no claim survives contact with this row except the exact instantiation. | A paired exact toy in which the referee boundary is varied one property at a time: measured saturation at an analytically computed evidence ceiling (10x budget does not move performance beyond it), measured held-out gain from referee-side witness queries, and measured tripling of the observed-vs-held-out gap under a declared capture policy. Connects the equivalence-class floor and the witness operator to self-improvement claims. | An internal referee (no write-protection, no independent evidence) sufficing against optimized proposers in a natural setting; a capture policy under which held-out performance rises; the ceiling formula mispricing the class floor. | Vary referee properties independently against proposers of increasing strength up to score-optimizing ones; report whether observed score remains a calibrated predictor of held-out score per configuration (Open Problem 15). |
| Situated competence and constraint release | `theory/core/competence-constraint-and-verification.md`; `theory/emergence/latent-competence-and-constraint-release.md` | Blackiston & Levin (2013); Blackiston, Vien & Levin (2017); Kriegman et al. (2020, 2021) on Xenobots; Gumuskaya et al. (2023) on Anthrobots; Fields & Levin (2022); Pezzulo & Levin (2026) | **Empirical support with a strict boundary:** living material can exhibit robust behavior in unusual configurations, consistent with a larger reachable repertoire than the reference embodiment displays. The studies do not identify a Platonic source of competence or isolate explanatory cost among evolution, substrate, coupling, and intervention. | A reference-relative definition that holds process, task, and lens fixed; separates exposure from creation, amplification, and reinterpretation; and supplies an exact lens-only control. | Constraint release ceasing to change physical traces under fixed tests; the result vanishing when intervention cost and hidden process edits are counted; or biological cases being fully predicted by a narrower ordinary model. | Extend the finite benchmark to many graph families and matched-description interventions; in biological cases, preregister fixed lenses and compare embodiment, learning-history, and observer-only controls. |
| Random substrate plus low-rank selector | `theory/core/competence-constraint-and-verification.md#6-rich-process-small-selector-the-lottalora-constraint` | Hazan, Zhang, Hartl & Levin (2026), *LottaLoRA* | **Preprint evidence:** frozen seeded random backbones plus trained low-rank adapters recover high relative performance on nine reported benchmarks. **Challenge:** the result does not distinguish random-feature coverage, lottery-like directions, optimization geometry, implicit regularization, or an inefficient basis carrying little task information. | Makes minimum selector rank conditional on architecture, optimizer, budget, data, seed distribution, tolerance, reliability, and metric; refuses to identify it with task complexity. | Performance collapsing across seeds or matched baselines; task information being concentrated entirely in adapter/head; or the threshold moving arbitrarily with architecture and training protocol. | Replicate with seed distributions, shuffled/trivial controls, matched trainable-parameter budgets, and rank sweeps; report threshold distributions rather than one minimum rank. |
| Interaction-grounded semantics | `theory/ai/interaction-grounded-semantics.md` | Georgeon, Marrel & Cook (2026); Georgeon, Lurie & Robertson (2024); Georgeon & Ritter (2012); official `schema_mechanism` implementation | **Preliminary empirical and architectural support:** action-dependent interaction tokens and learned schemas can organize future behavior without predefined world-state labels. **Challenge:** one small architecture does not establish general semantics, biological developmental order, or cross-agent convergence. | Defines a policy-, history-, horizon-, probe-, and lens-relative equivalence over continuation roles; separates functional role, affordance preservation, and valence. | Token classes failing to predict held-out continuations or policies; equivalent roles collapsing under mild policy shifts; or world-state labels explaining the same behavior more simply. | Train on action-feedback histories, then test held-out continuation prediction, intervention on token classes, displacement composition, and cross-policy/cross-agent transfer. |
| Replay and proof as corrective feedback | `theory/core/verification-as-reverse-pressure.md`; `theory/ai/world-models-and-vla.md` | Rodionov (2026) ARC-AGI-3 agent and ablation; Urban (2026); Bryant et al. (2026) on proof-producing autoformalization | **Mixed demonstrated support:** executable replay catches contradictions; machine-checked proof exposes malformed definitions and assumptions. ARC ablations also show executable representation is not uniformly best, verification is costly, and held-out transfer is unresolved. Proof and replay have different semantics and are only structurally analogous. | A typed correction loop in which failed verification can revise definitions, interfaces, constraints, or model families; exact replay is replaced by a declared test equivalence when justified. | Verification improving audit scores without held-out accuracy; revision overfitting the replay corpus; or the empirical/formal analogy hiding distinct failure modes. | Compare exact and equivalence-class replay under display nuisance shifts; classify proof/replay failures by whether they revise a candidate, definition, interface, or test. |
| Identity under self-modification | `theory/core/invariance-and-identity.md#self-modification-and-the-projector-audit` | Perrier (2026), *Self-Modification and the Evolution of Identity in Intelligent Systems* | **Formal proposal with philosophical extrapolation:** a projector compatible with the relevant operators can express weak preservation of an identity-bearing subspace. The paper's stronger liar/diagonalization interpretation is not a general impossibility theorem for self-modifying agents. | Integrates the projector test with observer-relative identity, separates six continuity criteria, and treats provenance/succession as alternatives when the criterion itself changes. | The selected projector lacking causal relevance; continuity judgments being stable without it; or the commutation condition proving too strong or too weak for real update systems. | Instrument an autonomous loop with frozen external tests, editable internal criteria, and provenance; compare sameness, functional continuity, and succession judgments under controlled criterion edits. |
| Grokking as inverse-direction transition | `theory/emergence/grokking-phase-transition.md` | Power et al. (2022); Nanda et al. (2023) *Progress Measures*; Liu, Michaud & Tegmark (2023) *Omnigrok* | **Strong support:** mechanistic interpretability has reverse-engineered the post-grokking algorithm (modular arithmetic via Fourier features) — the inverse direction partially *executed on the network itself*. **Challenge:** results are task-specific; no general trace→generator method follows. | Reads grokking as the trace-memorization → generator-approximation transition inside a learning system, connecting it to the spine. | Evidence that grokking is an optimization artifact (e.g. weight-decay dynamics) with no recoverable "generator" content beyond narrow task families. | Replicate progress-measure analysis on the repo's grokking simulation; test whether transition timing predicts out-of-distribution generalization. |
| Program induction and finite model search | `theory/computation/p-vs-np-as-generator-search.md` (legacy framing) | Lake, Salakhutdinov & Tenenbaum (2015) *BPL*; Ellis et al. (2021) *DreamCoder*; Levin (1973) universal search; Ljung (1999) | Program induction can recover useful programs inside selected languages with strong priors. Cost and identifiability depend on the language, evidence, prior, target equivalence, and algorithm; no uniform P-versus-NP conclusion follows. | The v1.2 benchmark reports exact enumeration cost and prior/world-bias curves inside a finite declared language. | Results disappear under matched search budgets, or claims omit the model language and out-of-family controls. | Compare exact enumeration, learned searchers, and symbolic methods under the same DSL, compute budget, noise, and held-out targets. |
| Narrative as cognitive technology | `theory/narrative/narrative-as-cognitive-technology.md` | Dennett (2013) *Intuition Pumps*; Lakoff & Johnson (1980) *Metaphors We Live By* | **Adjacent support:** intuition pumps and conceptual metaphor are established accounts of how framing devices shape available thought. **Challenge:** "installed primitives become available hypotheses" is plausible but not quantified; media-effects research is methodologically contested. | Two-directional claim grounded in an internal datum: the repo's fiction layer both stress-tests theory (existing rule) and *generates* concepts that become architecture (Entry 15 → Log 017, provenance depth). | Evidence that narrative exposure does not measurably change hypothesis generation; or that the Entry-15→Log-017 sequence was incidental rather than generative. | Track future fiction→formalism sequences in this repo as they occur; treat each as one observation, not proof. |
| Art–science: one practice, two referees | `theory/narrative/art-science-one-practice-two-referees.md` | Ginzburg (1979/1986) *Clues: Roots of an Evidential Paradigm*; Morelli (1880s) attribution method | **Support:** the evidential paradigm documents a centuries-old trace-based-inference tradition in the humanities, and the art market's attribution grades (*by / studio of / school of / after*) are a working provenance economy predating Log 017's schema. **Challenge:** the shared-generator claim is untested outside friendly cases, and "resonance" has no measurement comparable to physical verification. | A mechanism for the art–science connection (one generative practice, two verification regimes) plus a *measured* instance of aesthetics doing epistemic work (the elegance/Occam curves). | A domain where generative practice and aesthetic selection fully dissociate; or the provenance analogy breaking at an essential joint. | Track further fiction→formalism sequences as they occur; attempt a structural comparison of the two referees (matter vs. resonance) honest enough to show where it fails. |
| Invariance and identity | `theory/core/invariance-and-identity.md`; `theory/core/mathematical-axioms.md` | Klein (1872) Erlangen Program; Noether (1918); Nozick (2001) *Invariances*; Crutchfield & Young (1989) | **Strong formal anchor with a correction:** group invariance and symmetry–conservation results are established, but invariance can also be defined under semigroups, individual interventions, and stochastic kernels. Predictive equivalence is established in computational mechanics. **Challenge:** agent identity still requires a justified test family; no absolute persistence predicate follows. | Recasts identity explicitly as an equivalence relative to tests, horizons, tolerances, and equality notions; corrects the former no-group-no-invariant rule. | A claimed identity distinction that changes arbitrarily with an unreported test set or coarse-graining; or no domain justification for the selected transformations. | Reorganize Identity Suite metrics as reports of property + transformation family + test protocol + tolerance; compare predictive, mechanistic, historical, and embodied equivalences rather than collapsing them. |
| Psychedelics as perturbation | `theory/identity/psychedelics-as-perturbation.md` | Carhart-Harris & Friston (2019) *REBUS*; Carhart-Harris et al. (2014) *The entropic brain*; Huxley (1954); James (1898) | **Strong support:** REBUS is published mainstream neuroscience and maps cleanly onto precision-weighted priors; the filter lineage (James/Bergson/Huxley) anticipates the defensible half. **Challenge:** perturbed-state phenomenology resists controlled verification; the resonance-as-evidence risk is maximal here. | The perturbation/invariance reading: chemical self-intervention on an attractor; integration as invariant extraction; the sober basis as referee. | Evidence that relaxed-prior states yield no basis-invariant content beyond control conditions. | Specify a sober-basis verification protocol: what would count, operationally, as a basis-invariant insight. |
| Animism as generator prior | `theory/emergence/animism-as-generator-prior.md` | Barrett (2004) HADD; Guthrie (1993) *Faces in the Clouds*; Dennett (1987) *The Intentional Stance* | **Support:** hyperactive agency detection, anthropomorphism-as-strategy, and the intentional stance are established cognitive science. **Challenge:** unifying them as 'a prior over generator equivalence classes' is the repo's own move. | Connects the agent prior to a *measured* sibling (the Occam curves): priors over generators pay world-dependently; divergence queries as the calibration instrument. | Agent-attribution failing to behave like a prior (e.g., insensitivity to base rates under controlled traces). | A toy: agent-prior vs. simplicity-prior competing on traces from agentic vs. blind generators; measure the payoff crossover. |
| World models & VLA | `theory/ai/world-models-and-vla.md` | Ha & Schmidhuber (2018); Hafner et al., Dreamer (2019–2023); LeCun (2022) JEPA; Sutton (1991) Dyna; de Haan et al. (2019) causal confusion; RT-2 (2023), OpenVLA (2024), π0 (2024); Moravec (1988) | **Strong support:** model exploitation and causal confusion are documented failure modes that match the repo's equivalence-class and passive-ceiling results; Moravec's asymmetry matches the two-referees reading. **Challenge:** the toy results license qualitative reading only; industrial scale changes the quantities. | Reads both programs as the spine's two directions industrialized; the policy-as-adversarial-divergence-query framing; VLA as d=0-per-timestep verification. | The predicted failure modes ceasing to appear as the fields scale (e.g., passive video models achieving intervention-grade causal identification). | **Done** (benchmark v1.3): the optimizer's-curse wedge grows monotonically with class size while the candidate-average gap stays ≈0; exploitation is selection over guesses, not navigation toward them. Next: the closed-loop version. |
| Cooperative intelligence at the separatrix | `theory/symbiotic/cooperative-intelligence-at-the-separatrix.md` | Hutchins (1995) *Cognition in the Wild*; Ostrom (1990) *Governing the Commons*; Woolley et al. (2010) collective-intelligence factor; Dellermann et al. (2019) hybrid intelligence | **Adjacent support:** cognition can be distributed across people and artifacts; institutions can sustain cooperation; group performance and human–machine complementarity can be studied empirically. **Challenge:** none of these results establishes that heterogeneous cooperation improves transitions across a dynamical separatrix, and the participant categories are not equivalent kinds of agents. | Distributes the repo's trace→generator→construction→world-coupling→intervention→revision loop across heterogeneous contributors and connects it to the Transition Problem while keeping authority, veto, and responsibility located. | Equivalent verified performance from the strongest isolated participant; human rubber-stamping; cultural knowledge reduced to decoration; or coordination gains disappearing when review, verification, substrate, and displaced-harm costs are counted. | Compare isolated human, isolated model, unstructured human–AI pairing, and a structured shared-workspace condition on bounded construction tasks; pre-register complementarity, revision, authority, and viability measures. |
| Practice–culture feedback | `theory/emergence/from-action-to-culture.md` | Gollwitzer (1999); Sheeran & Webb (2016); Wood & Rünger (2016); Reckwitz (2002); Shove, Pantzar & Watson (2012); Feldman & Pentland (2003); Giddens (1984); Swidler (1986); Bell (1992/2009) | **Strong adjacent foundation:** intention–behavior gaps, cue-linked action, habits, socially organized practices, recursive structure, cultural repertoires, routine performance, and ritualization are established research programmes. **Challenge:** they use different units and mechanisms; individual habit cannot simply be scaled into organizational or cultural reproduction, and ritual is not a synonym for repetition. | Treats the passage from represented knowledge to durable collective action as a generator-and-return-path problem: traces require a runtime; recurrent practices are bundles of enactment, competence, materials, norms, transmission, feedback, and history; active culture alters the next action field. This is an integration, not a novelty claim about the component mechanisms. | Represented knowledge predicting persistence as well as the full bundle; no measurable distinction between a preserved trace and an active practice; failure to generalize under actor turnover; or recurrence being explained entirely by coercion or infrastructure ignored by the account. | On one bounded practice, compare information alone, a cue-linked plan, a workflow scaffold, and recurrent enactment with feedback; track event-level performance, variation, newcomer transmission, independently measured effects, and persistence under actor/tool turnover. |
| The city as deployed intelligence | `theory/human-organism-silicon-age/the-city-as-deployed-intelligence.md` | Jacobs (1961); Alexander (1965) *A City is Not a Tree*; West (2017) *Scale*; Batty (2013) | **Strong support:** urban scaling laws are quantitative and replicated; Jacobs/Moses is a documented natural experiment in single-axis optimization; Alexander's semilattice/tree distinction is a real topological claim. **Challenge:** the organism framing must stay bounded by the scaling data; 'city as intelligence' is a reading, not an established result. | The corridor's field site: superlinear-output-on-sublinear-substrate as measured capability loading; vital floors as breakers (Log 005); the tractable Class B measurement program (N=thousands of cities vs N=1 civilization). | Urban data failing to show corridor structure (e.g., no relation between constraint architecture and viability outcomes across cities). | **Pre-registered** as [Log 018](../../logs/018_the-city-panel-protocol.md): constructs, proxies (Wharton index, Social Capital Atlas, infrastructure margins), three falsifiable hypotheses, analysis plan — frozen before data contact. Execution open. |
| Measurement as weak intervention | `theory/core/measurement-as-weak-intervention.md` | Goodhart (1975) / Strathern (1997); Campbell (1979); Lucas (1976); MacKenzie (2006) *An Engine, Not a Camera*; Pearl (2009) *Causality*; Landsberger (1958) on the Hawthorne record | **Strong support:** reflexive-metric failure is established independently in economics, sociology, and science studies; Pearl's seeing/doing distinction formally grounds the watching/perturbing split. **Challenge:** the Hawthorne record is itself contested; the four-regime typology and the footprint×identification plane are the repo's own arrangement. | Wires the reflexivity literature into the equivalence-class formalism: coupling ≠ identification (measured for toy generators); metrics as inputs to the generator (a non-stationary identification target); the negative-yield limit (surveillance destroying the coherence axis it reads). | A demonstrated regime where high-stakes public metrics do not induce adaptation; or passive traces reliably collapsing generator classes in reflexive systems. | Log 018 H3 is the pre-registered field instance (instrumentation predicts recovery only conditional on coherence); toy option: a benchmark variant whose cells adapt to being read. |
| Construction vs. Deduction | `theory/computation/construction-vs-deduction.md` | Brouwer (1908 ff.); Hilbert program / Grundlagenstreit; Bishop (1967) *Foundations of Constructive Analysis*; Howard (1980) *Formulae-as-Types*; Martin-Löf (1984); Erdős (probabilistic method) | **Strong formal anchor:** intuitionism, constructive analysis, and Curry–Howard are settled mathematics; "constructive proof = program" is a theorem-grade correspondence, not an analogy. **Challenge:** the repo's *mapping* of this divide onto trace/generator and prediction/performance is structural rhyme, not formal reduction — and must not be presented as one. | Aligns the proof-theoretic divide with the project's asymmetry (verification/search, trace/generator, prediction/performance) as four instances of one shape; "nature as non-constructive prover" framing. | Demonstration that the four faces diverge in a load-bearing case — e.g. a regime where deduction-side abundance does *not* produce construction-side scarcity. | Benchmark v1 family-search testbed: measure whether AI systems are stronger at the deduction-shaped game (interpolation over certificates) or at open-space construction. |
| Weakness principle & the self hierarchy (Stack Theory) | `lab/benchmarks/inverse-reconstruction/README.md` (Exp-1 counterpart); also `theory/core/measurement-as-weak-intervention.md`, `theory/computation/construction-vs-deduction.md`, `lab/metrics/identity_persistence.py` | Bennett (2023c) *The Optimal Choice of Hypothesis Is the Weakest, Not the Shortest*; Bennett (2026) *No Selves, No Consciousness* (AAAI SSS); Meulemans et al. (2025) *EUPI*; Schelling (1960); Grice (1957) | **Strong independent convergence:** Bennett reaches structurally parallel results by the repo's own method — necessity proofs + randomised Monte-Carlo. Thm 2 (an internal *do-vs-see tag* is unavoidable for causal learning) is the measurement note's core distinction proved as a necessity condition; Exp 2's info-seeking probing is divergence-query logic collapsing a decoder equivalence class; Thm 5 (a binding move restricts the future self) is Identity Persistence / Log-017 commit authority. **Caveat:** weakness-optimality *under a uniform extension prior* is partly definitional; the load-bearing claim is representation-invariance — extension count `w(ℓ)=\|E_ℓ\|` is encoding-free where description length (MDL/AIXI) is not. Bennett explicitly disclaims sufficiency for phenomenology (matches the repo's `[SPECULATIVE]` line on experience). | The **cost side** of Bennett's prescription: `family_search` measured that *simplicity* selection is world-dependent (chance on uniform worlds), and v1.3 measured the optimizer's-curse wedge from committing to one class member — both are the penalty for *not* holding the weakest hypothesis (the uncollapsed class). His proof and our measurements are two faces of one result; three-way convergence with EUPI at the level of formal frameworks. | A weakness selector failing to beat Occam on the CA testbed's held-out neighbourhoods, or collapsing to the same choice — the convergence would be superficial. | **Done (benchmark v1.4, `weakness_selector.py`)**: all three pre-stated predictions confirmed — commitment efficiency +2.7→+1.0 (simple world), 0.00±0.03 (uniform; analytic prediction hit to two decimals), < −7 (complex, Laplace-floored); on complex worlds the elegant guess is worse than a coin at every coverage and lies outside the world's support 100% of the time at k ≤ 5. **Also done (benchmark v1.5, `wmax_planner.py`)**: marking the guesses *eliminates* the v1.3 wedge (wmean wedge ≈ 0 at every class size, vs .085 committed at u=5) and cuts real-reward regret 35–60%; the exact pessimist (wmin) is never disappointed but pays *more* real reward than the committed baseline from u ≥ 3 — worst-case discipline is a safety instrument, not free. **Both follow-ups also done**: v1.6 closed loop (acting is measuring — dense regimes collapse the class in one round; the risky prediction that the argmax explores its own delusions faster than a random policy was *falsified*: optimization is not curiosity, the selection-not-navigation null extends to the closed loop) and v1.7 ensemble sweep (52% of the wedge gone by K=4, 87% by K=16; regret floor is genuine ignorance — ensembles cure delusion, not ignorance). Remaining open: learned world models with correlated ensembles (real-model question; API budget). |
| Viable Corridor / capability loading | `papers/viable-corridor.md` | Aubin (1991) *Viability Theory*; Rockström et al. (2009) / Richardson et al. (2023); Bostrom (2014); Omohundro (2008) *Basic AI Drives* | **Support:** viability theory supplies the formal frame (open-set invariance); the instrumental-convergence literature matches the capability-loading mechanism. **Challenge:** no external work yet validates the specific three-constraint conjunction or the capability-loading result outside this repo's two models. | Capability as a *shared driver* loading several constraints at once, demonstrated in two structurally independent in-repo models; single-axis insufficiency. | External replication failing; or real agent ecologies in which single-axis interventions suffice at high capability. | P7/P8 on real LLM agent populations (the companion-paper programme). |

## 2b) A note on anchor independence

Several rows above cite Elija Perrier and Michael Timothy Bennett, and they appear in the matrix
as separate lines of external support: Perrier on self-modification and the projector criterion,
Bennett on the weakness principle and Stack Theory, and Perrier & Bennett (2026),
*Time, Identity and Consciousness in Language Model Agents* (arXiv:2603.09043), as the source of
the Identity Persistence score.

These are not independent anchors. They are two researchers who also publish together, and the
identity/consciousness cluster in this repository leans on them heavily. That concentration is
worth stating plainly: agreement between these sources is weaker evidence than agreement between
unrelated groups would be, and a critique that lands against their shared framing lands against
several repository rows at once.

The bibliography previously listed the joint paper under a wrong title and initial
("Bennett, C.", *Identity Persistence in Autonomous Agents: The Chord Postulate*), which hid the
overlap — the co-author read as a different person from the Stack Theory author. Corrected
2026-08-11.

The Arpeggio and Chord postulates are **Stack Theory's**, instantiated for language-model agents by
that paper, which also supplies the two persistence scores and a three-axis identity morphospace.
The repository's fractional coverage score and two-axis plot are local adaptations; its substantive
contribution is the Exp5–7 measurement and the commit-time deflation — joint
satisfaction at the commitment boundary rather than physical simultaneity. See the
[glossary](../../theory/reference/glossary.md#chord-postulate-arpeggio-postulate).

This tightens the dependency rather than loosening it: the borrowed identity vocabulary and the
paper's windowed metrics come from the same pairing. The repository's adaptations must therefore
be evaluated as adaptations, not counted as independent confirmation.

## 3) Initial external anchors

Foundation anchors (added with the reconstruction):
- Eilenberg & Mac Lane, *General Theory of Natural Equivalences* (1945)
- Shannon, *A Mathematical Theory of Communication* (1948)
- Fritz, *A Synthetic Approach to Markov Kernels, Conditional Independence and Theorems on Sufficient Statistics* (2020)
- Crutchfield & Young, *Inferring Statistical Complexity* (1989); Shalizi & Crutchfield, *Computational Mechanics* (2001)
- Valiant, *A Theory of the Learnable* (1984); Wolpert & Macready, *No Free Lunch Theorems for Optimization* (1997)
- Pearl, *Causal Diagrams for Empirical Research* (1995)

Core anchors used above:
- Shanahan, McDonell & Reynolds, *Role Play with Large Language Models* (2023)
- Chalmers, *Could a Large Language Model be Conscious?* (2023)
- Park et al., *Generative Agents: Interactive Simulacra of Human Behavior* (2023)
- Packer et al., *MemGPT: Towards LLMs as Operating Systems* (2023)
- Mazeika et al., *Utility Engineering: Analyzing and Controlling Emergent Value Systems in AIs* (2025)
- Butlin & Lappas, *Principles for Responsible AI Consciousness Research* (2025)
- Carichon et al., *The Coming Crisis of Multi-Agent Misalignment* (2025)
- Beckenbauer et al., *Orchestrator: Active Inference for Multi-Agent Systems in Long-Horizon Tasks* (2025)
- Wei et al., *Evo-Memory* (2025)
- Zhang et al., *Agentic Context Engineering* (2025)
- Kim et al., *Towards a Science of Scaling Agent Systems* (2025)
- Wagner et al., *Humans in the Loop* (2025)

Inverse-direction anchors (added with the trace→generator rows):
- Ljung, *System Identification: Theory for the User* (2nd ed., 1999)
- Brunton, Proctor & Kutz, *Discovering Governing Equations from Data: Sparse Identification of Nonlinear Dynamical Systems (SINDy)* (PNAS, 2016)
- Schmidt & Lipson, *Distilling Free-Form Natural Laws from Experimental Data* (Science, 2009)
- Cranmer, *Interpretable Machine Learning for Science with PySR and SymbolicRegression.jl* (2023)
- Solomonoff, *A Formal Theory of Inductive Inference* (1964); Levin, *Universal Sequential Search Problems* (1973)
- Power et al., *Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets* (2022)
- Nanda et al., *Progress Measures for Grokking via Mechanistic Interpretability* (ICLR 2023)
- Liu, Michaud & Tegmark, *Omnigrok: Grokking Beyond Algorithmic Data* (ICLR 2023)
- Lake, Salakhutdinov & Tenenbaum, *Human-Level Concept Learning through Probabilistic Program Induction* (Science, 2015)
- Ellis et al., *DreamCoder: Bootstrapping Inductive Program Synthesis* (PLDI 2021)
- Chollet, *On the Measure of Intelligence* (2019)
- Aubin, *Viability Theory* (1991); Bostrom (2014); Omohundro, *The Basic AI Drives* (2008)

Additional adjacent references to consider in future updates:
- Active inference and free-energy principle literature (for formal grounding of orchestration claims).
- Safety cases from high-reliability engineering (for veto/control-plane fault tolerance).
- Causal discovery (constraint-based and score-based structure learning) — adjacent to trace→generator for graphical generators.

## 4) Cross-links added

Short “Related work” pointers were added to selected canonical files so major theory text remains intact.

A second round (2026-06) anchored the inverse-direction files in place:
- `theory/core/the-generator-question.md` — the "external machinery" note now names the fields that work the inverse problem (system identification, SINDy/symbolic regression, program induction, mechanistic interpretability) and states what the project adds beyond them.
- `theory/emergence/grokking-phase-transition.md` — Power / Nanda / Omnigrok block; the essay's "generator reading" is positioned as a framing on top of that literature, not a competing account.
- `theory/computation/p-vs-np-as-generator-search.md` — Levin search, program induction (BPL, DreamCoder), symbolic regression, Chollet.
- `theory/reference/glossary.md` — header pointer to the Internal Language Anchors table and this map ("no term floats free").

## 5) Claim-status legend

Use this legend when revising repository claims:
- **Established result**: replicated external empirical or theoretical support.
- **Adjacent research**: neighboring evidence, not direct confirmation.
- **Repo hypothesis**: internal claim with partial or no external validation.
- **Speculative analogy**: useful framing metaphor without direct measurement.
- **Open problem**: unresolved, requires targeted experiments.

## 6) Final report

### Files changed
- `meta/research-alignment/related-work-map.md`
- `theory/emergence/fractal-architecture-of-emergence.md` (cross-link)
- `theory/veto/ai-alignment-biological-veto.md` (cross-link)
- `lab/agents/three_layer_agent.py` (cross-link comment)
- `papers/quantifying-emergent-utility-in-llms.md` (cross-link)

### Strongest external support
- Utility Engineering / TEO and Three-Layer Memory have the clearest direct alignment with current literature on emergent utility control and memory architectures.

### Strongest external challenge
- Mirror Problem and consciousness-adjacent claims face the strongest challenge: fluent introspection is not equivalent to consciousness or robust self-modeling.

### Claims that should be softened
- Universal framing of fractality, blanket benefit of latency, and confidence in veto infallibility should be narrowed to context-dependent hypotheses.

### Claims that now look more promising
- Memory-tiered agents with explicit utility/control instrumentation and human oversight pathways appear empirically tractable and high-value for near-term testing.

## 7) AGI-26 source audit and integration ledger

This section preserves the source audit, integration decisions, and claim
status behind
[Competence, Constraint, and Verification](../../theory/core/competence-constraint-and-verification.md)
(audit of 2026-07-30, formerly a standalone file).

**Sourcing rule:** A scientific claim is retained only when it is supported
by an independently citable artifact: a paper, proceedings chapter, official
repository, or author or project page. Conference talks and recordings are
treated only as pointers to such artifacts, not as evidence. Anything without
one remains a lead, is marked unverified, and is not load-bearing in
repository synthesis.

**Conference anchor:** *Artificial General Intelligence: 19th International
Conference, AGI 2026, San Francisco, July 27–30, 2026*, proceedings
[Part I, LNCS 16854](https://doi.org/10.1007/978-3-032-33010-9) and
[Part II, LNCS 16855](https://doi.org/10.1007/978-3-032-33195-3).

### Integration map

| AGI-26 idea | Existing repository concept | Relationship | Required action |
|:---|:---|:---|:---|
| diverse cognition under unusual bodies and constraints | situated stack; embodiment; emergence; invariance | supports and refines | define latent competence; add trace/lens controls |
| Platonic-space ingress | speculative emergence and narrative layer | philosophical interpretation, not empirical consequence | exclude from working science; retain as explicitly speculative source |
| fixed random backbone plus low-rank adapters | typed process models; compression; selector question | challenges controller/weights-only attribution; does not restore generic generator | integrate conditional $r^*$ audit and competing explanations |
| comportment-grounded semantics | measurement as intervention; action-conditioned observation; world binding | fills a formal gap | create interaction-role equivalence note |
| executable world models with replay and simplification | world models; autonomous loops; inverse reconstruction | refines and partially supports | formalize equivalence-class replay; cite later ablation |
| autoformalization as feedback on definitions | construction versus deduction; recursive workbench | supports with an important correction | create verification-as-reverse-pressure bridge |
| identity under self-modification | invariance and test-relative identity | specializes and challenges | add projector audit; reject absolute impossibility reading |
| categorical architecture comparison | [typed process-diagram structure](../../theory/core/mathematical-axioms.md#44-structure); graph-oriented architecture notes | potentially refines; partly duplicates | retain as research seed, no new category-theory foundation |
| implication as algorithmic containment | Kolmogorov complexity; compression; simulation | mostly adjacent/rephrasing, with a formal theorem under assumptions | supporting context only |
| process calculi with interaction, energy, history | coupled processes; mortality; bisimulation | relevant but not verified from an independent public artifact | open seed only |
| one-principle active-inference architecture | existing active-inference notes and simulations | largely duplicate at current evidence level | open implementation lead only |
| reproducible AGI builds and protocol governance | provenance depth; referee boundary | supports engineering governance | link as a preliminary policy proposal |
| PLN compilation to thermodynamic hardware | thermodynamic hardware manifesto; stochastic computation | narrow hardware result, no load-bearing synthesis role | exclude from central theory |

This map preserves competing interpretations. It does not flatten the
repository's older process-identification, viability, or identity programmes
into the new synthesis.

### Status vocabulary used in this ledger

| Label | Meaning in this ledger |
|:---|:---|
| **empirically demonstrated** | reported experiment or benchmark with a described method; scope stays with that setup |
| **formally proved** | theorem inside a declared formal system and assumptions |
| **proposed hypothesis** | testable interpretation not established by the cited result |
| **philosophical interpretation** | conceptual or metaphysical reading without a discriminating empirical result |
| **preliminary result** | preprint, short paper, public-set result, or incompletely validated implementation |
| **conference lead not independently verified** | presented at the conference, but no adequate primary or official artifact was located; not evidence |

### Primary-source ledger

#### Latent competence and diverse cognition

| Source | Verified content | Status | Repository use |
|:---|:---|:---|:---|
| Blackiston & Levin (2013), [*Ectopic eyes outside the head in Xenopus tadpoles provide sensory data for light-mediated learning*](https://doi.org/10.1242/jeb.074963), *Journal of Experimental Biology* 216, 1031–1040 | posterior eye grafts supported a light-mediated learning assay in tadpoles without normal eyes | empirically demonstrated | motivates competence under an unusual sensory coupling |
| Blackiston, Vien & Levin (2017), [*Serotonergic stimulation induces nerve growth and promotes visual learning via posterior eye grafts*](https://doi.org/10.1038/s41536-017-0012-5), *npj Regenerative Medicine* 2, 8 | serotonergic intervention affected innervation and visual learning through posterior grafts | empirically demonstrated | shows that a simple intervention can alter access, while also warning that the biological process changes |
| Kriegman et al. (2020), [*A scalable pipeline for designing reconfigurable organisms*](https://doi.org/10.1073/pnas.1910837117), *PNAS* 117, 1853–1859 | designed Xenopus-cell constructs displayed predicted locomotion and collective behaviors | empirically demonstrated, explicitly design-assisted | prevents describing Xenobots as wholly undesigned competence |
| Blackiston et al. (2021), [*A cellular platform for the development of synthetic living machines*](https://doi.org/10.1126/scirobotics.abf1571), *Science Robotics* 6 | biological construction and behavior of Xenobots | empirically demonstrated | supports unconventional-body evidence |
| Kriegman et al. (2021), [*Kinematic self-replication in reconfigurable organisms*](https://doi.org/10.1073/pnas.2112672118), *PNAS* 118 | kinematic replication in a designed environment | empirically demonstrated in the reported setup | included with design/environment qualifications |
| Gumuskaya et al. (2024), [*Motile Living Biobots Self-Construct from Adult Human Somatic Progenitor Seed Cells*](https://doi.org/10.1002/advs.202303575), *Advanced Science* 11, e2303575 | adult airway epithelial cells self-constructed into motile Anthrobots; a neural-wound assay was reported | empirically demonstrated | supports reorganization under novel embodiment; does not establish cognition |
| Fields & Levin (2022), [*Competency in Navigating Arbitrary Spaces as an Invariant for Analyzing Cognition in Diverse Embodiments*](https://doi.org/10.3390/e24060819), *Entropy* 24, 819 | proposes competent navigation as a cross-embodiment analytic lens | proposed hypothesis / conceptual framework | supporting vocabulary, not a universal metric |
| Pezzulo & Levin (2026), [*Bootstrapping Life-Inspired Machine Intelligence*](https://arxiv.org/abs/2602.08079) | synthesizes biological design principles involving embodiment, constraints, multiscale control, and plasticity | proposed synthesis / preprint | scientific anchor for the conservative Level B reading |
| Levin (official Thoughtforms essay), [*A Short Argument on Platonic Space*](https://thoughtforms.life/a-short-argument-on-platonic-space-variable-agency-patterns-that-in-form-physics-biology-computer-science-and-cognitive-science/) | explicitly proposes a Platonic-space interpretation and acknowledges uncertainty | philosophical interpretation | excluded from the repository's working scientific commitment |

**Decision:** **integrated** at observational and conservative theoretical
levels; Platonic ingress **excluded as speculative**.

#### Random substrate and low-rank selection

Hazan, Zhang, Hartl & Levin (2026),
[*A Little Rank Goes a Long Way: Random Scaffolds with LoRA Adapters Are All You Need*](https://arxiv.org/abs/2604.08749),
arXiv:2604.08749.

- **Verified result:** frozen seeded random backbones plus trained LoRA paths
  recover 96–100% of fully trained performance on nine reported benchmarks
  while training 0.5–40% of parameters.
- **Verified mechanism evidence:** learned backbone scaling remains positive
  when the scaffold is fixed; when the scaffold is destabilized, optimization
  can suppress it and move task information into the adapter.
- **Author hypothesis:** saturation rank estimates task intrinsic dimension.
  The paper also reports architecture-capacity dependence and calls broader
  invariance an open problem.
- **Artifact status:** a dedicated official implementation repository was not
  located during this audit; reproduction therefore depends on the manuscript
  description and any later author release.

**Decision:** **integrated** as a preliminary empirical constraint. “Noise
contains the answer” and “minimum rank equals task complexity” are rejected.

#### Interaction-grounded semantics

| Source | Verified content | Status |
|:---|:---|:---|
| Georgeon, Marrel & Cook (2026), [*Emergence of Comportment-Grounded Semantics*](https://doi.org/10.1007/978-3-032-33010-9_16), AGI 2026, pp. 253–259 | sensorimotor-loop token stream, learned schemas, pragmatic sequence roles, attention-matrix analysis | preliminary published experiment |
| Georgeon, Lurie & Robertson (2024), [*Artificial Enactive Inference in Three-Dimensional World*](https://doi.org/10.1016/j.cogsys.2024.101234), *Cognitive Systems Research* 86, 101234 | formal EMDP/SEMDP treatment in which interactions depend on decision and state | published formal/modeling proposal |
| Georgeon, Marshall & Gay (2012), [*Interactional Motivation in Artificial Systems*](https://doi.org/10.1109/DevLrn.2012.6400833), ICDL-EPIROB | introduces interactional-motivation framing | published short paper |
| PetiteIA, [Schema Mechanism tutorial](https://github.com/PetiteIA/schema_mechanism) | official runnable tutorial with action-dependent binary feedback and learned schemas | official implementation |

**Decision:** **integrated** with a new continuation-role equivalence. Claims
about universal developmental ordering or full human semantics remain
**open**.

#### World models, proof, and recursive correction

| Source | Verified content | Status | Decision |
|:---|:---|:---|:---|
| Rodionov (2026), [*Executable World Models for ARC-AGI-3 in the Era of Coding Agents*](https://arxiv.org/abs/2605.05138); [official code](https://github.com/astroseger/arc-3-agents-baseline1) | executable model, replay, simplification, and planning loop on 25 public games; private validation untested | preliminary conference/public-set result | integrate architecture, not headline |
| Rodionov (2026), [*Do Coding Agents Need Executable World Models, Simplification, and Verification to Solve ARC-AGI-3?*](https://arxiv.org/abs/2607.15439) | four-way ablation; stronger model/reasoning most robust; textual variant sometimes beats executable-only; verification arm leads four main settings at higher cost; held-out untested | preliminary ablation preprint | integrated as the controlling source |
| Urban (2026), [*130k Lines of Formal Topology in Two Weeks*](https://arxiv.org/abs/2601.03298) | long-running LLM–Megalodon feedback loop and large generated formalization | preliminary autoformalization report | supporting context |
| Bryant, Huerta y Munive, Kaliszyk & Urban (2026), [*Munkres' General Topology Autoformalized in Isabelle/HOL*](https://arxiv.org/abs/2604.07455); [code](https://github.com/JUrban/isa_top_autoform1) | 806 checked results with zero `sorry`; qualitative audit finds weak definitions, redundancy, and integration problems | empirically documented formalization plus machine-checked corpus | integrated as proof/specification correction evidence |

Dramatic conference phrasing was replaced by the numbers and limitations in
the papers.

**Decision:** **integrated** through
[Verification as Reverse Pressure](../../theory/core/verification-as-reverse-pressure.md).

#### Identity and self-modification

Perrier (2026),
[*Deconstructing Superintelligence: Identity, Self-Modification and Différance*](https://arxiv.org/abs/2604.19845);
published in AGI 2026 proceedings,
[Part II chapter](https://doi.org/10.1007/978-3-032-33195-3_14).

- **Formally defined in the paper:** update $\hat U$, discrimination $\hat D$,
  representation $\hat R$, and a nontrivial unifying projector $\Pi$ in the
  intersection of their commutants for weak self-modification.
- **Formally proved in the paper:** commutator identities and restrictions
  inside the proposed associative-operator model.
- **Proposed philosophical interpretation:** liar-paradox, inclosure, and
  Derridean readings of strong self-modification.
- **Not established:** an impossibility theorem for every identity relation or
  every self-modifying system.

**Decision:** **integrated** as a specialized projector audit; universal
identity-collapse reading **excluded**.

#### Architecture comparison and algorithmic containment

| Source | Verified content | Status | Decision |
|:---|:---|:---|:---|
| de los Riscos, Corbacho & Arbib (2026), [*Proposal for an AGI Formal Comparative Framework Based on Category Theory*](https://doi.org/10.1007/978-3-032-33010-9_11); expanded [working paper](https://arxiv.org/abs/2603.28906) | syntax, knowledge, relational, scope, and constraint layers; structure-preserving architecture morphisms; worked RL/causal-RL/schema comparisons | conference position paper plus evolving working paper | **open research seed**; no new category-theory section |
| Franz (2026), [*Grounded Reasoning: Implication as Algorithmic Containment*](https://doi.org/10.1007/978-3-032-33010-9_15), AGI 2026, pp. 238–252 | frames implication through reconstruction/algorithmic containment and proves a result under generated-instance assumptions with logarithmic overhead | formal result under stated assumptions | **supporting context**; overlaps conditional description length and simulation |

The categorical framework earns a future comparison only if its morphisms
predict a distinction that the repository's typed process graphs do not.
Algorithmic containment earns a bridge only where it improves on established
conditional Kolmogorov-complexity language.

#### Interaction, energy, history, and process calculi

Meredith (2026), [*Algorithmic Scientists and the Foundations of Machine
Intelligence*](https://f1r3fly.io/white-papers/algorithmic-scientists.html),
official F1R3FLY white paper.

The white paper proposes graph-structured lambda theories, bisimulation-
preserving morphisms, reactive contexts, and generated behavioral logics. It
is an official project document, not a peer-reviewed proceedings artifact.
The broader energy, stochasticity, history-monad, and mortality cluster
was not located in a citable paper or repository.

**Decision:** **retained as an open research seed**. Bisimulation is relevant
to test-relative functional equivalence; no foundation change.

#### Unified active-inference architecture

Roger Harielson (2026), [*Unified Cognition from a Single Optimization
Principle: Active Inference in MeTTa with Emergent Reasoning, Planning, and
Self-Knowledge*](https://doi.org/10.6084/m9.figshare.31742059), Figshare
preprint, is accompanied by the Project Dagaz
[official repository](https://github.com/Jolnir-Sefir/dagaz) and archived
manuscripts. The artifacts report 23 MeTTa modules and Python executable
specifications; they also report that native Hyperon execution is blocked by
runtime defects. The benchmark claims are author-reported implementation
results, not independent evidence that one objective is sufficient for unified
cognition.

**Decision:** **retained as an open implementation lead**. The abstract-level
claim does not yet add a verified result beyond the repository's existing
active-inference material.

#### Reproducibility and protocol governance

Hatta (2026), [*Reproducibility is the New Copyleft: Defining AGI-oriented
Reproducible Builds*](https://arxiv.org/abs/2606.03019).

The preprint proposes seven requirements covering code, data, weights,
configuration, toolchain/hardware, audit history, and protocol governance. Its
append-only signed self-improvement log is a design proposal; recursive
verifiability remains an explicit research problem.

**Decision:** **linked as supporting engineering context** for
[Provenance Depth](../../logs/017_provenance-depth-and-the-verification-economy.md)
and referee governance, not a settled build standard.

#### Thermodynamic and probabilistic hardware

Ma (2026), [*Compiling PLN to Thermodynamic Hardware*](https://doi.org/10.1007/978-3-032-33195-3_2),
AGI 2026, pp. 16–21.

The paper maps a PLN factor graph to an Ising-style hardware representation
and reports simulator-level validation. That is a narrow compiler/hardware
result. It does not materially constrain the competence, semantics, replay, or
identity synthesis.

**Decision:** **excluded as out of scope**; relevant only to the repository's
explicitly speculative thermodynamic-hardware track.

### Unsupported leads not carried forward

The following were not used as scientific premises:

- exact benchmark numbers not reproduced in a paper or official artifact;
- slide-dependent claims, figures, or demonstrations absent from an
  independently citable artifact;
- the claim that random noise “contains” task solutions;
- minimum adapter rank as an architecture-independent task complexity;
- exact replay as proof of an accurate or general world model;
- machine-checked proof as proof of good definitions or good library design;
- strong self-modification as a universal mathematical impossibility;
- Platonic ingress as an empirical explanation; and
- unverified claims that one active-inference objective already yields unified
  cognition.

### Repository outputs

- [Competence, Constraint, and Verification](../../theory/core/competence-constraint-and-verification.md)
- [Latent Competence and Constraint Release](../../theory/emergence/latent-competence-and-constraint-release.md)
- [Interaction-Grounded Semantics](../../theory/ai/interaction-grounded-semantics.md)
- [Verification as Reverse Pressure](../../theory/core/verification-as-reverse-pressure.md)
- [Constraint-Release Benchmark](../../lab/benchmarks/constraint-release/README.md)
- [Invariance and Identity](../../theory/core/invariance-and-identity.md#self-modification-and-the-projector-audit)
