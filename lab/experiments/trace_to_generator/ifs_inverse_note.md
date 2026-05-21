# Inverse IFS Note

Status: Working Note
Scope: IFS as a constrained toy model for trace-to-generator reconstruction.
Epistemic status: Methodological framing; no claim that all images are fractals.
Related files:
- simulation-models/emergent-dynamics/iterated-function-systems/README.md
- theory/emergence/generative-form-systems.md
- theory/emergence/trace-to-generator.md
Failure conditions:
- Claiming every image has a compact IFS explanation.
- Ignoring approximation error and identifiability limits.

Forward direction is straightforward: choose contractive maps and iterate.
Inverse direction is harder: given an image trace, search for map sets that approximate it under explicit constraints.

This is useful because it isolates a core asymmetry:
- generator → trace is easy to execute,
- trace → generator is typically a constrained, underdetermined search.
