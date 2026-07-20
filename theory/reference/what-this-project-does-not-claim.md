# What This Project Does NOT Claim

**Status:** Reference — maintained alongside the claims themselves.

**Scope:** The explicit negative space of the repository. Trust in the positive claims is earned by keeping this page accurate; if you find an assertion anywhere in the repo that exceeds these boundaries, that is a defect — please file it.

---

This repository does not claim a theory of everything. Its current foundation is deliberately
smaller: typed classical stochastic processes compose; states, dynamics, observations, information,
and prediction can be defined from them; stronger concepts require declared additions. The project
then studies bounded questions about model identification and viability. The earlier unqualified
“generator” spine is research history, not a mathematical primitive or universal law.

The specific non-claims, each with the place where the boundary is stated:

1. **We do not claim that “generator” is a primitive or a new mathematical object.** The
   [Foundations Reconstruction](../core/mathematical-axioms.md) removes the unqualified term. A
   transition kernel, initial state, runtime, environment, observation map, history, model bundle,
   and model class are distinct objects. Qualified terms such as *infinitesimal generator*,
   *generating set*, and *generative model* retain their established meanings.

2. **We do not claim a universal law that forward execution is cheap and inverse recovery is
   hard.** Either direction can be easy, expensive, uncomputable, or statistically unidentified,
   depending on the model family, target equivalence, evidence, intervention access, encoding, and
   cost measure. The older [Generator Question](../core/the-generator-question.md) is retained as a
   superseded spine so this correction remains auditable.

3. **We do not assume P $\ne$ NP as a project foundation.** P versus NP concerns precisely encoded
   decision problems with particular verification conditions. It does not establish generic model-
   identification hardness. Kolmogorov uncomputability and Gödel incompleteness likewise have
   narrower scopes than the former spine assigned them. [Foundations Reconstruction §9.3](../core/mathematical-axioms.md#93-problems-in-the-former-generator-spine).

4. **We do not claim inversion is uniformly hard.** Our own benchmark shows the opposite: with a
   known model family, full observability, and clean data, recovery is cheap. Family search, noise,
   partial observability, missing coverage, and interventions must be reported separately.
   [Inverse-reconstruction benchmark](../../lab/benchmarks/inverse-reconstruction/README.md).

5. **We do not claim that traces identify a unique hidden process.** Predictively equivalent models
   can differ in latent organization. Identifiability requires declared restrictions, interventions,
   or minimality criteria. Perfect prediction does not by itself recover mechanism.
   [Hidden-extension proposition](../core/mathematical-axioms.md#7-a-result-the-foundation-forces-non-identifiability).

6. **We do not claim an absolute mathematical identity predicate for persons, AI systems,
   organizations, or cultures.** Identity is an equivalence relative to declared tests,
   interventions, horizons, tolerances, and levels of description. Predictive identity is one useful
   special case; it does not imply sameness of mechanism, substrate, history, embodiment, or
   perspective. [Foundations Reconstruction §5.1](../core/mathematical-axioms.md#51-identity).

7. **We do not derive learning or intelligence from information, prediction, recurrence, or
   adaptation alone.** Learning requires a data regime, class, loss, baseline, and resource criterion.
   Intelligence requires tasks, objectives, agent/environment interfaces, task weighting, and
   resources. The System Intelligence Index is a selected instrument, not a universal scalar.
   [Foundations Reconstruction §§5.2–5.3](../core/mathematical-axioms.md#52-learning).

8. **We do not claim that any current system is conscious, or that the proposed architectures are
   sufficient for experience.** Global availability, binding, self-model influence, and perturbation
   response are functional properties. Moving from them to phenomenal experience requires an
   independent bridge axiom that this repository does not possess.
   [Foundations Reconstruction §5.4](../core/mathematical-axioms.md#54-consciousness);
   [Consciousness as Global Availability](../identity/consciousness-as-global-availability.md).

9. **We do not claim that positive Shannon entropy guarantees life, novelty, adaptability, or an
   “edge of chaos.”** Entropy depends on a selected distribution and coarse-graining. High-entropy
   noise can be unorganized; deterministic systems can have intricate coarse-grained dynamics.

10. **We do not claim that active inference supplies an unbreakable biological veto.** Preferences,
    generative models, precision, action channels, and free-energy objectives are model additions.
    No general theorem maps suffering to infinite surprise or forces a particular protective action.

11. **We do not claim the Viable Corridor necessity theorem is deep.** Taken alone it is close to
    definitional because the viable region is defined by the three constraints. The substantive
    in-model content is capability loading and single-axis insufficiency.
    [The Viable Corridor, §7.1](../../papers/viable-corridor.md).

12. **We do not claim sufficiency.** That the three constraints jointly suffice for viability is a
    `[CONJECTURE]`, expected to require $\gamma > \gamma_c$; it is unproven, and the numerical
    evidence is single-trajectory, not open-set. [Paper §3.4, Appendix C.5](../../papers/viable-corridor.md).

13. **We do not claim civilization has been measured.** The AI ↔ civilization mapping is a
    `[HEURISTIC]` regime assignment with stated failure conditions, not a calibration. $K_c$ for real
    societies is not currently operationalized. [Paper §4, §5.4, §6.3](../../papers/viable-corridor.md).

14. **We do not claim results about real AI-agent ecologies.** The hard/soft-budget and capability-
    loading evidence comes from synthetic models. Identity experiments test different claims and
    cannot be substituted for real ecology tests. [Paper §5.3 and Appendix D](../../papers/viable-corridor.md).

15. **We do not claim elegance finds truth or that benchmark results generalize beyond their toys.**
    Occam selection pays only under a world bias toward simplicity. The benchmark results are floors
    and existence demonstrations in small, controlled systems.
    [Benchmark](../../lab/benchmarks/inverse-reconstruction/README.md).

16. **We do not treat fiction as evidence or claim external validation.** Fiction can stress-test or
    originate a concept; resonance does not confirm it. The project has not yet received the external
    domain review needed to stabilize its broader claims; the claims we most want checked, and what
    would refute each, are listed in the [Review Request](../../meta/research-alignment/review-request.md). [Narrative as Cognitive
    Technology](../narrative/narrative-as-cognitive-technology.md); [Log 017](../../logs/017_provenance-depth-and-the-verification-economy.md).

---

*The pattern behind this page: the repository's credibility strategy is not to claim more, but to make what is claimed checkable — status tags on claims, external anchors on concepts, "what it does NOT show" on simulations, and this page on the whole. If the positive documents ever drift above these lines, this page wins.*
