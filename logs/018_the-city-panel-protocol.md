# Log 018: The City Panel Protocol — a Pre-Registered Design for the Corridor's First Field Test

**Mode:** Applied Architecture / Pre-registration

**Status:** PROTOCOL — frozen before data contact

**Date:** 2026-07-06

**Scope:** Operationalizes the Viable Corridor's three constraint axes at city scale and pre-registers directional hypotheses, per [the-city-as-deployed-intelligence](../theory/human-organism-silicon-age/the-city-as-deployed-intelligence.md) and paper §5.4. **No data has been examined against these hypotheses.** The git commit introducing this file is the protocol's timestamp — the pre-registration is enforced by the repository's own provenance mechanism ([Log 017](017_provenance-depth-and-the-verification-economy.md), eating its own dogfood).

**Depends on:** `papers/viable-corridor.md` (§4, §5.4, P8), `theory/human-organism-silicon-age/the-city-as-deployed-intelligence.md`, `017_provenance-depth-and-the-verification-economy.md`

---

## Why pre-register

The corridor's Class B claims (real-world systems) carry a measurement debt the paper states openly: $\gamma_{\text{eff}}$, $K_{\text{eff}}$, and substrate headroom are barely operationalizable for a civilization ($N = 1$). At city scale they are measured municipal quantities across thousands of comparable instances. But observational urban data offers endless researcher degrees of freedom — proxy choice, panel choice, outcome choice — and a framework this flexible could be "confirmed" by accident. The registered-report discipline (Chambers, 2013) is the honest instrument: freeze the choices *before* touching the data, publish the freeze, and let the commit hash prove the order of events. What follows is the freeze.

## Constructs and primary proxies

Each proxy is named with its known threat to validity; alternates are listed for robustness, not for post-hoc substitution.

| Corridor construct | Primary proxy (US panel) | Threat to validity |
|:---|:---|:---|
| $\gamma_{\text{eff}}$ — regulation strength | Land-use regulation stringency (Wharton Residential Land Use Regulatory Index; Gyourko et al. 2008/2021) | regulation ≠ *homeostatic* regulation; stringency can encode incumbent protection rather than anti-concentration |
| $K_{\text{eff}}$ — coherence / coupling | Economic connectedness & civic engagement (Social Capital Atlas, Chetty et al. 2022, county level) | social capital is an outcome as well as an input; reverse causation with prosperity |
| Substrate headroom | Infrastructure utilization margins: water-system capacity vs. demand; grid reserve margin where published | municipal capacity data is patchy and heterogeneous; missing-not-at-random |
| Viability outcome (**primary**) | **Shock-recovery half-life**: years for employment and population to return to pre-shock trend after a FEMA-declared major disaster or a documented major plant closure | trend estimation choices; shock severity varies — severity controls required |
| Vital-floor breaches (secondary) | Boil-water advisories, blackout-hours, homelessness rate changes | reporting heterogeneity across municipalities |

The outcome choice is deliberate: the corridor predicts *robust viability* — return after perturbation — **not growth**. City-IP, so to speak: identity persistence of vital function under a kick. This is the intervention logic of the benchmark, found in the wild: shocks are the divergence queries that reveal which cities had the constraint architecture and which had eleven green quarters.

## Pre-registered hypotheses

- **H1 (the conjunction).** Recovery is predicted by the *minimum* of the three standardized constraint scores better than by any single score or by their mean. Model comparison: min-model vs. best-single-axis vs. additive, by out-of-sample fit. *Falsifier:* a single axis or the additive model matches or beats the min-model — the conjunction claim fails at city scale.
- **H2 (capability loading).** Pre-shock growth rate interacts with substrate headroom: high growth on low headroom predicts slow recovery and more floor breaches; growth with headroom does not. *Falsifier:* growth uniformly aids recovery regardless of headroom — capability would not load the substrate axis in the field.
- **H3 (the unwatched axis).** Instrumentation proxies (smart-city technology adoption indices) predict recovery only conditional on the coherence score; the main effect alone is ≈ 0. *Falsifier:* instrumentation alone robustly predicts recovery — the Meridian warning would be wrong where it matters.

## Panel and analysis plan (frozen)

US metropolitan areas / counties; shocks 2000–2020 with ≥ 3 post-shock years observed; target $N \geq 100$ shocked units. Pre-specified form: recovery half-life regressed on the three standardized constraint scores, their minimum, the H2 interaction, shock-severity controls (FEMA damage class), region and year fixed effects, clustered errors. Robustness: the listed alternate proxies, substituted one at a time and reported *all*, not selectively. Multiple comparisons: three hypotheses, stated once, no garden of forking paths beyond the listed robustness set.

## What this protocol does NOT claim

- **No causal identification.** Observational panel; associations only. Corridor-consistent associations would be *survival of a falsification attempt*, not proof; their absence would be genuinely damaging (that is the point).
- **No proxy = construct identity.** Every row of the proxy table is contestable; that is why it is frozen and public rather than chosen after seeing residuals.
- **No commitment that we run it ourselves next week.** The protocol is also an invitation: any group with panel-data experience can execute it, and the commit hash guarantees they would be testing our predictions, not our postdictions.

## Failure conditions for the protocol itself

- Any analysis of these hypotheses on these data before this file's commit — there was none; the hash is the warrant.
- Proxy substitution after data contact presented as the primary result.
- Reporting only the robustness variants that flatter H1–H3.

> **Anchors.** Chambers (2013), registered reports; Gyourko, Saiz & Summers (2008) and Gyourko, Hartley & Krimmel (2021), the Wharton index; Chetty et al. (2022), *Social Capital I/II* (Nature); West (2017), *Scale*. Internal: paper §5.4 (the measurement debt this addresses at its tractable scale), [the city node](../theory/human-organism-silicon-age/the-city-as-deployed-intelligence.md), [Log 017](017_provenance-depth-and-the-verification-economy.md) (the provenance mechanism doing the timestamping).
