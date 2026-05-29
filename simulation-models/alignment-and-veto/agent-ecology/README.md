# Agent-Ecology Stress Test (Class C: P7, P8)

*An independent, agent-based stress test of the Viable Corridor paper's
AI-specific predictions — hard vs. soft budgets (P7) and capability vs.
constraint architecture (P8).*

## Why a second model?

`../teo-civilization/teo_simulation.py` tests the three constraints **inside**
the TEO ODE (Class A — model-internal; Appendix C). That cannot, by itself,
tell us whether the regime claims are artifacts of that particular ODE. This
module is a deliberately **different** model — discrete-time, stochastic,
agent-based, with explicit *hard vs. soft (routable) budget* mechanics the ODE
does not have. Agreement across the two is evidence that the P7/P8 regime
behaviour is **structural**, not a quirk of the TEO formulation.

It introduces **no new theoretical concepts**: capability, hard/soft budgets,
monopolistic concentration, and substrate overshoot are all defined in the
paper (§2, §5.3). This file only *operationalises* them in an independent
setting, with each modelling choice tagged in the docstring.

> **Honest scope.** This is a synthetic ABM, not a test on real AI agents. It
> strengthens the *structural-robustness* case for P7/P8; the Class C claim
> about **real** agent ecologies (LLMs) remains open and is the companion
> paper's subject (`papers/quantifying-emergent-utility-in-llms.md`).

## The model (one step)

`N` agents hold resource shares `w_i` (sum 1), each with a fixed capability
`c_i`. Per step:

- **Myopic optimisation** (discrete replicator): `w_i` grows with its capability
  advantage over the mean, scaled by substrate health `H`.
- **Activity / entropy load**: `demand = η · Σ c_i w_i` — *raw* capability-
  weighted throughput, independent of `H` (matching the canonical TEO
  dissipation of §2.5: a non-self-throttling optimiser dumps entropy at a rate
  set by what it does).
- **Budget** (the P7 mechanism):
  - **hard** — realised activity is clipped to `D` (a hardware/protocol limit the
    optimiser cannot exceed); overshoot can never accumulate;
  - **soft** — the optimiser *routes around* the limit (a fraction `evade` of the
    over-budget activity still happens; `evade=1` ⇒ purely advisory).
- **Regulation `γ`**: simplex-preserving redistribution above `x_reg` (the §2.4
  brake) — the only thing that limits concentration.
- **Substrate**: `Ω += max(0, realised − D)`; **collapse** when `Ω ≥ S_max`.

**Outcomes** per run: `monopoly` (`max_i w_i ≥ x_crit`, a V1 failure) and
`collapse` (`Ω ≥ S_max`, a V3 failure). Over many seeds we report the
*frequency* of each — the "runaway frequency" of P7.

## What it shows

- **P7** — under a **hard** budget the substrate-collapse frequency is ≈0 at every
  capability level; under a **soft** budget it rises with capability (here: 0 → 1
  as the capability scale crosses `C = D/η`). Hard budgets prevent the runaway;
  soft (routable) ones do not.
- **P8** — a hard budget addresses **only** the substrate axis. At high capability
  with weak regulation, **monopoly still occurs** under a hard budget
  (≈26% of runs at `C=1.8, γ=0.3`). Only **hard budget *and* adequate `γ`**
  keep both failure modes near zero — the agent-ecology echo of Appendix C.4:
  capability is a shared driver, and single-axis fixes fail.

## Running

```bash
python agent_budget_sim.py            # console: P7 + P8 frequency tables
python agent_budget_sim.py --save      # also write the Appendix-D figure
python agent_budget_sim.py --save -o DIR
```

The figure `teo_p7p8_agent_ecology.png` is consumed by Appendix D of the paper.
Requires `numpy`, `matplotlib` (repo `requirements.txt`).

## Related

- [The Viable Corridor](../../../papers/viable-corridor.md) — §5.3 (P7, P8), Appendix D
- [TEO simulation](../teo-civilization/teo_simulation.py) — Class A evidence (Appendix C)
