# Construction vs. Deduction (Framing Note)

Status: Working Note
Scope: The mathematical ancestor of the project's central asymmetry — what a proof *gives you* versus what it *shows you* — and its mapping onto verification/search, trace/generator, and prediction/performance.
Epistemic status: Framing note over well-established mathematics (intuitionism, proof theory, Curry–Howard); the *mapping* onto the repo's spine is this project's contribution and is tagged where it is a claim. Personal origin: a question that has occupied the author since his mathematics studies — this note is where that thread lives and grows.
Related files:
- theory/computation/p-vs-np-as-generator-search.md
- theory/core/the-generator-question.md
- logs/017_provenance-depth-and-the-verification-economy.md
- fiction/15_the_exchange_rate.md
Failure conditions:
- Treating "constructive good, classical bad" as the claim. It is not; the claim is about what you possess after the proof.
- Claiming the repo's asymmetry follows formally from intuitionism. It rhymes; it does not reduce.

---

## The distinction

Mathematics has two ways of knowing that something exists.

**Deduction** moves from premises to conclusions by rules. Given the proof, checking it is mechanical — each step either follows or it doesn't. Crucially, deduction can establish existence *without exhibiting anything*: assume the object does not exist, derive a contradiction, conclude that it must. The law of the excluded middle does the work, and at the end you hold a certainty and no object.

**Construction** exhibits. A constructive existence proof builds the witness — here is the number, the function, the algorithm, and here is why it has the property. At the end you hold the object itself.

The canonical miniature: *there exist irrational numbers $a, b$ with $a^b$ rational.* Classical proof: consider $\sqrt{2}^{\sqrt{2}}$. Either it is rational — done, with $a = b = \sqrt{2}$ — or it is irrational, and then $(\sqrt{2}^{\sqrt{2}})^{\sqrt{2}} = 2$ is rational. Existence is proved, beautifully, in four lines — and you leave the proof *not knowing which pair works*. The proof is a certificate without a specimen.

The same shape at scale: Hilbert's basis theorem proved that certain generating sets exist, by contradiction, exhibiting none — prompting Gordan's famous protest: *"Das ist nicht Mathematik. Das ist Theologie."* The probabilistic method (Erdős) proves combinatorial objects exist by showing a random draw succeeds with positive probability — entire fields of objects whose existence is certain and whose specimens took decades more to construct, where they have been constructed at all. Brouwer's own fixed-point theorem is the standing joke of the foundational fight: its classical proofs guarantee the fixed point and provide no way to find it.

The fight itself — Brouwer's intuitionism against Hilbert's formalism, later Bishop's quieter constructive analysis — ended, sociologically, in Hilbert's favor: working mathematics is classical, and for good reasons (excluded middle buys reach and elegance; most working mathematicians never feel the loss). But the distinction did not die. It migrated — into computer science, where it turned out to be the load-bearing wall.

## Curry–Howard: construction is generation

The Curry–Howard correspondence makes the distinction exact: **propositions are types, proofs are programs**. A constructive proof of "there exists $x$ with property $P$" *is* — literally, not metaphorically — a program that computes the witness, paired with evidence. In this project's vocabulary:

> **A constructive proof is a generator. A non-constructive existence proof is a certificate that a generator exists, with no generator attached.**

That sentence is the bridge, and it is why this note lives next to [P vs NP as Generator Search](p-vs-np-as-generator-search.md). The complexity-theoretic asymmetry (verifying a witness is cheap; finding one may not be) is the *resource-bounded* form of the same divide: deduction-checking is the polynomial side, construction is the search side. Intuitionism asked the question qualitatively — *what do you possess after the proof?* — half a century before complexity theory asked it quantitatively — *what does it cost to come to possess it?*

## The mapping onto the spine `[HYPOTHESIZED]`

The project's organizing asymmetry now has four faces, and they align:

| Cheap / certificate side | Expensive / artifact side | Where it lives |
|---|---|---|
| Deduction (checking; existence w/o witness) | Construction (exhibiting the witness) | this note |
| Verification of a candidate | Search for the candidate | [P vs NP note](p-vs-np-as-generator-search.md) |
| Trace (running the generator forward) | Generator recovery (inverse direction) | [The Generator Question](../core/the-generator-question.md) |
| Prediction / model consensus | Performance (matter votes) | [Log 017](../../logs/017_provenance-depth-and-the-verification-economy.md), [Entry 15](../../fiction/15_the_exchange_rate.md) |

The alignment is structural, not formal — none of these reduces to another, and the table should be read as four instances of one *shape*: in each row, the left column can be held without possessing what the right column possesses, and the right column is where the scarcity lives.

Two consequences worth stating:

1. **Nature is a non-constructive prover.** Every observed phenomenon is an existence proof of a generator — the world is running it, so it exists. What observation hands you is exactly what the classical proof hands you: certainty *that*, with no access to *what*. The inverse problem of the spine is the demand for constructive content; science, on this reading, is the project of upgrading nature's existence proofs to constructions. The [inverse-reconstruction benchmark](../../lab/benchmarks/inverse-reconstruction/README.md) measures the cost of that upgrade in toy regimes — including the regime where the upgrade is impossible in principle (the equivalence class: many constructions consistent with the certificate).

2. **Proof-theoretic provenance.** In Log 017's vocabulary, a non-constructive existence proof is a claim with high *provenance depth* relative to its witness: the certificate is impeccable and the object is $n$ hops away, where $n$ may be infinite. Mathematics tolerates this gladly (its referent is the formal system, and the formal system has voted). Engineering cannot: you do not build the bridge out of the theorem that good alloys exist. The verification economy of Entry 15 is what happens to a civilization that forgets which of the two games it is playing.

## The honest counterweight

Deduction is not the lesser member of the pair, and this note must not be read as constructivist evangelism. Proof-checking is what makes mathematics *cumulative* — the one human enterprise where verification is genuinely cheap, which is precisely why formal methods (machine-checked proof, from Lean's mathlib outward) can industrialize it. Classical mathematics' non-constructive reach is a feature: it lets you know where to dig before you can dig. The asymmetry claim is narrower and, for that, harder to dismiss:

> The two activities produce different possessions. A deduction yields certainty relative to axioms. A construction yields an artifact that runs. Systems — economies, sciences, agents — that price these possessions identically will, under generation pressure, accumulate certificates and lose artifacts.

That last clause is the repo's claim, not mathematics'. It is tagged `[HYPOTHESIZED]`, it is dramatized in Entry 15, given a schema in Log 017, and measured in miniature by the benchmark.

## Open threads (where this note grows)

- **AI and the two games.** Current models are strongest at the deduction-shaped game (interpolation within a corpus of certificates) and weakest at construction in open spaces — or is that backwards, given program synthesis? This is empirically explorable with the benchmark's planned family-search testbed (v1).
- **Formal substrate as performance.** A machine-checked proof is d = 0 *for formal referents* (Log 017's domain note). Does the deduction/construction divide reappear *inside* formal verification, between checking a proof term and synthesizing one? (It does — that is proof search — and the divide's recursion deserves its own note.)
- **The author's thread.** What made the distinction feel load-bearing in the original mathematics — the experience of holding a proof and not holding the object — is the seed of this note, and worth writing down as such: which theorems, which courses, which moment. *(Deliberately left open for first-person expansion.)*

> **Related work.** Brouwer (1908 ff., intuitionism); Hilbert's program and the Grundlagenstreit; Bishop, *Foundations of Constructive Analysis* (1967); Howard, *The Formulae-as-Types Notion of Construction* (1980, circulating from 1969) and Martin-Löf's intuitionistic type theory (1984) for the proofs-as-programs correspondence; Erdős's probabilistic method as the canonical industrial-scale non-constructive technique. Concept-by-concept mapping in the [Related Work Map](../../meta/research-alignment/related-work-map.md).
