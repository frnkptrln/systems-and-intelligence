# LLMs as Probabilistic Automata

Status: Working Note
Scope: Operational model for connecting LLM behavior to the trace→generator framework.
Epistemic status: Engineering abstraction; useful for analysis and experiment design, not a claim of complete mechanistic transparency.
Related files:
- theory/emergence/trace-to-generator.md
- theory/emergence/grokking-phase-transition.md
- theory/emergence/generative-compression.md
- logs/013_the-runtime-is-part-of-the-generator.md
Failure conditions:
- Treating prompts as complete generators.
- Treating output similarity as mechanism identity.

A practical abstraction:
context_t → model state update → distribution over next token → sample token → context_{t+1}

Generator decomposition:
- weights
- architecture
- tokenizer
- context window content
- system/developer policy scaffolding
- sampling parameters
- tool/runtime coupling

A prompt is a control surface, not the whole generator.

Inverse prompt problem:
desired output constraints → search over prompts/context/examples/tools to produce acceptable traces.

Underdetermination:
- Many prompts can yield similar outputs.
- Similar outputs do not identify prompt, latent mechanism, or training provenance.

Relation to grokking and generative compression:
- Grokking frames the shift from memorized trace matching toward rule-like generalization.
- Generative compression asks whether internal structure supports robust variants, not just replay.

Safety note: prompt reconstruction is approximate and underdetermined; it should be treated as constrained steering, not reverse-engineering certainty.
