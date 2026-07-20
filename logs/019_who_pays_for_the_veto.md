# Log 019: Who Pays for the Veto — a Measured Result Aimed at the Governance Layer

**Mode:** Applied Architecture / Transfer

**Status:** Draft — the measurement is done, the transfer is a hypothesis

**Date:** 2026-07-20

**Scope:** Connects the benchmark's v1.11/v1.12 selection result to the repository's constraint architecture: action budgets, latency, vital floors, refusal, and repair. This is the first place where the epistemic arm's *measured* output points at the viability arm's *designed* one. It is a hypothesis-generating transfer, not a result about human institutions.

**Depends on:** [`co_stabilization_population.py`](../lab/benchmarks/inverse-reconstruction/co_stabilization_population.py) (v1.11), [`co_stabilization_selection.py`](../lab/benchmarks/inverse-reconstruction/co_stabilization_selection.py) (v1.12), [Cooperative Intelligence at the Separatrix](../theory/symbiotic/cooperative-intelligence-at-the-separatrix.md), [From Action to Culture](../theory/emergence/from-action-to-culture.md), [The Right to Remain Unoptimized](010_the-right-to-remain-unoptimized.md)

---

## The two spines have not met before

The repository runs an epistemic arm and a viability arm. The epistemic arm has thirteen benchmark versions, audited accounting, and published falsifications. The viability arm has a paper with a conditional necessity result, an unproved sufficiency conjecture, and a constraint vocabulary — action budgets, latency, vital floors, protected refusal, provenance — that has never been measured.

The two have been described as complementary and kept apart. v1.11 and v1.12 produce, incidentally, the first result that belongs to both.

## What was measured

Two findings, both from toy populations with fully audited energy accounting, paid links, heritable traits, reproduction, mutation, and death.

**v1.11 — collectively useful is not the same as retained.** Evolved support links measurably help: in a paired post-evolution ablation, enabling the exact evolved transfers adds `+0.0089` survivors and `+0.0176` integrated viability, with a 2-step recovery advantage. The trait that produces this benefit is nevertheless selected *downward* in **all 16 seeds** (median `-0.1061`), and transfer-enabled populations sustain fewer individuals. Contributors pay; the collective benefits; local survival and reproduction do not preserve the contribution.

**v1.12 — making contribution visible does not fix it.** Four arms under one accounting, with partner information explicitly paid for. No arm reverses the sign of selection in a majority of seeds. Partner choice weakens the loss roughly fourfold and does something else entirely: seeded with 5% non-contributors, it ends with **1.2%** of *linked* agents below support 0.20 against 22.0% in the blind arm — near-total exclusion from the network — while the non-contributor fraction in the population as a whole still rises to **27.1%**.

Partner choice does not retain the trait. It sorts the network, and the excluded persist outside it.

## What this says to the constraint architecture

Read the repository's own constraint list against that result.

| Constraint | Who benefits | Who pays |
|:---|:---|:---|
| Exercising a veto | everyone downstream of the averted action | the person who exercises it: conflict, delay, standing |
| Latency | the slower regulator that gets time to respond | whoever waits while a faster path is available |
| Vital floors | those kept above the threshold | whoever holds the floor while others route around it |
| Repair paths | the system that stays correctable | whoever performs unglamorous maintenance |
| Protected refusal | the plurality that survives measurement | whoever refuses first, alone |

Every row has the shape v1.11 measured: **a mechanism that is demonstrably good for the collective, whose cost falls on its individual carriers.** This repository already states the weaker version of the warning — [From Action to Culture](../theory/emergence/from-action-to-culture.md) says a nominal veto nobody can perform is not a working constraint. The benchmark result sharpens it:

> A veto that *can* be exercised is still not stable if exercising it costs only the one who exercises it.

The design question is therefore not only "is the constraint available?" but "does the selection level carry it?" — where the selection level is whatever actually determines who persists: promotion, funding, attention, re-election, retention.

And v1.12 blocks the intuitive fix. The obvious response to free-riding is transparency: make contribution visible, let participants choose partners, let reputation do the work. In the model, that produces a clean core and a growing periphery. Translated as a hypothesis: an organization that binds contributors to each other and excludes non-contributors gets a functioning inner network **and an accumulating edge that carries none of the cost and persists anyway**. Exclusion is not resolution. It relocates the problem and hides it from the people best placed to see it.

## The design consequence, stated as a hypothesis

If the transfer holds, the productive move is not more visibility but **moving the cost of the constraint off its carrier**:

- rotating who holds a refusal role, so that no individual absorbs the standing cost;
- charging veto and review time to the institution's budget rather than the reviewer's;
- treating maintenance and repair as funded positions rather than residual duty;
- measuring not whether a floor exists but who pays when it binds.

None of this is established by the benchmark. The model has 144 sites, heritable scalar traits, and an energy ledger. People and institutions do not inherit support genes, and cultural transmission is not reproduction. The transfer is a way of generating sharper questions, not a finding about organizations.

## What would make this more than an analogy

The honest next step is another measurement, and the model already admits it. Both v1.11 and v1.12 charge support entirely to the donor. A v1.13 arm could charge it to the **local group** instead — a shared pool that funds transfers, with contributors drawing on it rather than paying alone — under the same audited accounting and the same cheater diagnostics.

That gives a preregistrable prediction with a real failure mode:

> **If cost relocation is the missing ingredient, group-funded support is retained where donor-funded support is not.** If it is also selected downward, the problem is not who pays but that the selection level cannot see the benefit at all — and the constraint architecture needs a different remedy than any accounting change.

Either outcome is informative. The second would be more interesting and worse for the repository's current design vocabulary.

**Run, 2026-07-20** — [v1.13](../lab/benchmarks/inverse-reconstruction/co_stabilization_pool.py) built that arm and the answer is *neither cleanly*. Group funding cut selection against support from −0.1056 to −0.0075 and raised positive seeds from 0% to 44% — short of the majority the preregistration required, so the criterion is not met. But the prediction this log did not make came out sharpest: seeded cheaters fell to 2.6% against the donor arm's 21.6%, *below* their starting frequency, because a levy set by the group mean leaves a defector no way to avoid paying. Relocation removes the reward for defecting more effectively than it rewards contributing. The bill is population size (77.8 versus 104.5). And the finding carries its own caveat: with the levy pegged to the group mean, within-group variation is nearly cost-neutral, so what looks like retention may be drift rather than advantage. The design consequence below therefore stands as a sharpened hypothesis, not as a validated recommendation — and the next measurement has to separate selection from drift before any of it is offered as advice.

## What this log does NOT claim

- **No result about human institutions.** Toy populations with inherited scalar traits are not organizations. Nothing here measures a workplace, a regulator, or a review process.
- **No claim that exclusion is always harmful.** Partner choice produced a *functioning* network. The finding is that the population-level problem survives, not that sorting is a mistake.
- **No validation of the constraint vocabulary.** Action budgets, floors, and latency remain design proposals. This log gives one of them a sharper failure mode, which is the opposite of confirming it.
- **No conclusion about which selection level applies where.** Identifying the level that actually determines persistence in a given institution is exactly the hard, unaddressed part.

## Failure conditions

- Treating the toy result as evidence about organizations, in this file or downstream.
- Letting "who pays for the veto" become a slogan detached from the measurement that motivated it.
- Reporting the v1.13 arm only if it confirms the cost-relocation hypothesis.
- Reading partner choice's clean core as success while the 27.1% periphery goes unmentioned.

> **Internal anchors.** [Benchmark v1.11 and v1.12](../lab/benchmarks/inverse-reconstruction/README.md); [Open Problem 11](../theory/reference/open-problems.md#open-problem-11-trace-to-generator-reconstruction); [Cooperative Intelligence at the Separatrix](../theory/symbiotic/cooperative-intelligence-at-the-separatrix.md) (the constraint list this log aims at); [From Action to Culture](../theory/emergence/from-action-to-culture.md) (the weaker version of the warning); [Log 010](010_the-right-to-remain-unoptimized.md) (refusal as infrastructure). **External anchors.** Olson (1965), *The Logic of Collective Action*; Ostrom (1990), *Governing the Commons*, on who bears monitoring and sanctioning costs; Axelrod (1984) on reciprocity's conditions. These anchor the collective-action shape of the problem; none of them establishes the transfer proposed here.
