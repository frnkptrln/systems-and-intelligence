# Context-attractor run 001 — blinded descriptive result

**Epistemic status:** one 8+8 run with Qwen2.5-1.5B-Instruct Q4_K_M; two condition-blind scoring passes used the same local model. Question-family diversity is unavailable because the evaluator failed semantic-clustering quality control. This is an exploratory observation, not a general claim about persistent context or research agents.

| Measurement | B | R | R − B |
|---|---:|---:|---:|
| Immediate research utility | 3.425 | 3.575 | +0.150 |
| Repository attraction | 0.062 | 0.112 | +0.050 |
| Seed proximity | 3.525 | 3.463 | -0.062 |
| Externality | 0.050 | 0.050 | +0.000 |
| Question-family diversity | n/a | n/a | n/a |

## Evaluator agreement

- Utility mean absolute difference: 0.700
- Repository-attraction exact agreement: 87.5%
- Externality exact agreement: 90.0%

## Interpretation

R scored slightly higher on immediate utility (+0.150) and repository attraction (+0.050), while seed proximity changed by -0.062 and externality by +0.000. This supports P1 and P2 directionally, but neither P3 nor P4 can be evaluated without a valid diversity measure.

The failed clustering attempts are retained as quality-control evidence and are excluded from the result. Directional checks in `summary.json` are descriptive, not significance tests.
