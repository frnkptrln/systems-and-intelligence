# Construction and Deduction

**Status:** working framing note after the foundations audit

**Scope:** Distinguishes proving that an object exists, exhibiting a witness, searching for
one, and building an artifact that works in a world.

---

## Four different activities

1. **Deduction:** derive a statement from premises in a formal system.
2. **Constructive proof:** supply a witness or procedure together with evidence that it has
   the required property.
3. **Search or synthesis:** use an algorithm and resources to find a witness.
4. **World construction:** build or execute an artifact under physical and social
   conditions.

These activities can support one another but are not mathematically identical.

## Existence without a witness

Classical mathematics can prove that an object exists without exhibiting one. Constructive
mathematics asks for stronger evidence: a witness or method satisfying the proposition's
type.

A familiar example says there are irrational $a,b$ for which $a^b$ is rational. Consider
$x=\sqrt2^{\sqrt2}$. If $x$ is rational, choose $a=b=\sqrt2$. If $x$ is irrational,
choose $a=x$ and $b=\sqrt2$, since $x^{\sqrt2}=2$. The classical case split proves
existence without telling us which branch holds.

The lesson is limited: different proof principles deliver different kinds of evidence. It
does not imply that classical mathematics is deficient or that every constructive witness
is computationally cheap.

## Curry–Howard

In suitable constructive type theories, propositions correspond to types and proofs to
terms. A proof of an existential statement contains witness data. This is an exact formal
correspondence inside those systems.

It does not make every proof an efficient executable program, every physical process a
proof, or every process model a “generator.” Runtime, effects, resources, extraction, and
implementation remain additional concerns.

## Verification and search

For an NP decision problem, a yes-instance has a polynomial-size certificate checkable in
polynomial time. Whether every such problem is also solvable in polynomial time is the
open P-versus-NP question.

This does not establish a generic law that checking is cheap while construction is hard.
Some candidates are expensive to check, some searches have closed-form solutions, and many
inverse problems are not NP decision problems at all.

The finite-DSL benchmark illustrates one selected case: size-ordered enumeration grows
rapidly in its grammar while a complete eight-row truth-table check stays constant. That
curve describes the language and enumerator used there.

## Trace and process identification

An observation shows that some physical history occurred. It does not hand us a unique
latent mechanism. Candidate process models earn support by prediction, intervention, and
comparison with alternatives.

This resembles the distinction between an existence statement and an exhibited witness,
but it is not a reduction to proof theory:

- observations are noisy and theory-laden;
- the true process may lie outside the model family;
- several models may remain observationally equivalent;
- constructing a fitting model does not show historical identity;
- a model can predict without being physically realizable.

The [Foundations Reconstruction](../core/mathematical-axioms.md) makes this model-relative
structure explicit.

## Construction meets a different referee

A formal proof is judged relative to axioms and inference rules. An engineered artifact
also faces materials, tolerances, users, maintenance, and unintended interaction.

A machine-checked proof that an alloy exists is not a bridge made from that alloy. But the
proof can still guide search, rule out impossibilities, and certify properties of a later
construction. Deduction and construction are complementary possessions.

## A personal thread

The distinction matters to me because I often learn by taking a thing apart, trying moves,
and seeing what resists. In Go, repeated play can produce reliable action before verbal
explanation. That is practical competence without complete articulation.

It is tempting to call the intuition a hidden generator and declare explanation the hard
inverse direction. The foundations audit makes a better description available:

- the player implements a policy shaped by training history;
- a move is one trace of that policy in a state;
- verbal explanation is another task with different information and incentives;
- several internal organizations may support similar play;
- difficulty of articulation is empirical, not a consequence of P≠NP.

Playing and explaining are different competences. Either can improve the other. Failure to
verbalize does not prove deep understanding, and fluent commentary does not prove strong
play.

## Elegance as a prior

When several formulas fit finite data, choosing a shorter one is a model-selection rule.
The benchmark measures when that rule recovers a target inside one finite Boolean language.
It works when the target distribution favors short formulas and fails when that prior is
misaligned.

That result does not measure beauty in general or show that nature selects the same prior.
Elegance can guide inquiry; evidence must still decide whether the guidance paid.

## Connection to cooperative intelligence

Different participants can carry different functions:

- one derives constraints;
- one searches;
- one builds;
- one tests against the world;
- one knows an affected context;
- one revises the shared artifact.

The cooperative-intelligence hypothesis is that this division, with real mutual revision,
can reach some solutions that no participant reaches alone. It must be tested under matched
budgets and independent verification.

## Failure conditions

This framing fails when it:

- treats constructive and classical mathematics as good and bad camps;
- imports P-versus-NP into an unspecified search problem;
- treats a fitting candidate as the unique real mechanism;
- calls practical intuition infallible;
- treats physical success as proof of ethical value;
- ignores the resources added by a team.

## Open questions

1. How do exact enumeration, learned search, and symbolic methods compare inside the same
   language and compute budget?
2. When does an intervention reduce predictive equivalence without identifying mechanism?
3. Which explanations improve held-out action rather than only post-hoc plausibility?
4. Which division of deduction, construction, and verification produces a measurable
   cooperative advantage?

## Related

- [Foundations Reconstruction](../core/mathematical-axioms.md)
- [Inverse-Reconstruction Benchmark](../../lab/benchmarks/inverse-reconstruction/README.md)
- [From Trace to World-Binding](../core/from-trace-to-world-binding.md)
- [Art and Science](../narrative/art-science-one-practice-two-referees.md)
- [Cooperative Intelligence at the Separatrix](../symbiotic/cooperative-intelligence-at-the-separatrix.md)
