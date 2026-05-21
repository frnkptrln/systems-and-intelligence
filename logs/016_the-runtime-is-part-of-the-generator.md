# The Runtime Is Part of the Generator

Status: Applied Architecture Log
Scope: Practical implications of treating runtime as part of behavior-generating systems.
Epistemic status: Design guidance drawn from software/ML deployment patterns; not universal law.
Related files:
- logs/013_the-coupling-first-sequence.md
- logs/010_the-right-to-remain-unoptimized.md
- theory/emergence/trace-to-generator.md
- theory/ai/llms-as-probabilistic-automata.md
Failure conditions:
- Reducing runtime to an afterthought in reproducibility claims.
- Assuming artifact equivalence implies behavioral equivalence.

If runtime is part of the generator, engineering practice changes:

1. **Infrastructure as runtime**
   - Build pipelines, container layers, drivers, and schedulers are generator components.
   - “Same code, different stack” is often “different generator.”

2. **Organizations as interpreters**
   - Policy, incentives, and escalation paths shape execution trajectories.
   - A specification run by two institutions can yield different system behavior.

3. **LLM applications**
   - Behavior depends on more than model weights: system prompt, tool access, retrieval corpus, memory policy, and sampling.

4. **Reproducibility failures**
   - Most incident retrospectives should include runtime-diff audits, not just code diffs.

5. **Governance**
   - Compliance and safety should target coupled systems, not isolated artifacts.

Applied rule: document generator bundles as **artifact + runtime + policy + history assumptions**.
