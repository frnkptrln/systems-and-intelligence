# Active Identifiability

**Status:** bounded working experiment. The causal witness is executable and
regression-tested. The self-report study is an offline design draft, not a
preregistration. No model has been selected for a frozen study, and the
committed protocol still authorizes no model calls. Exploratory compatibility
probes were nevertheless run against one pinned model before the protocol was
frozen; they are reported below and did not pass the smoke gate.

The question is narrower than "can we infer what is inside a system?":

> Given a declared candidate family, observation channel, and intervention
> budget, which query changes what can be identified, and which apparent
> difference is only a property of the readout interface?

Identifiability is therefore relative to a candidate family and an admissible
set of interventions. Agreement at one observable does not establish shared
mechanism. Disagreement at one readout does not establish different underlying
states.

## Why this directory exists

The repository already has the conceptual rule [coupling is not
identification](../../../theory/core/measurement-as-weak-intervention.md) and
measured intervention hierarchies in the [Inverse-Reconstruction
Benchmark](../../benchmarks/inverse-reconstruction/README.md). The Mirror
Problem asks what happens when candidate systems agree on the declared
observable but may diverge under another query.

An earlier closed experiment branch mixed this question with self-report,
world-model, embodiment, runtime, and robotics work. This recovery keeps only
two bounded tracks:

1. an exact causal witness showing that a chosen intervention can separate
   observationally equivalent generators;
2. an offline multi-readout study design asking whether a model-report result
   survives changes in the measurement channel.

XPolicyLab and world-model evaluation are deliberately excluded. They remain a
separate applied line until they produce evidence required by this question.

## Empirical bridge: *The Interface Is the Intervention*

The accompanying reproducibility repository,
[*Triage × Persona Measurement Audit*](https://github.com/frnkptrln/triage-persona-measurement-audit),
supports a limited but important precursor result. In its two complete model
runs, persona framing was measurable but not dominant or measurement-invariant:
response options, wording, order-associated variation, refusal, and schema
compatibility changed what became observable. Two additional checkpoints
failed the preregistered schema smoke gate and were retained as compatibility
outcomes rather than recoded as substantive choices.

That paper does **not** identify a latent persona or show that model states are
generally unobservable. It demonstrates why the measurement interface must be
factorized before a behavioral difference is attributed to the target system.
This study draft imports five concrete controls from it:

- a neutral-paraphrase wording floor;
- canonical and reversed options paired inside the same seed block, removing
  the paper's order-versus-replicate confound;
- sampled, forced-choice, and logit readouts kept as distinct channels;
- invalid, refusing, and non-directional outcomes preserved rather than forced
  into binary choices;
- a schema and tokenizer compatibility gate before the main run.

## Track A: exact causal witness

`causal_witness.py` defines two linear-Gaussian generators.

Generator A:

```text
X ~ Normal(0, 1)
Y = X + epsilon, epsilon ~ Normal(0, 1)
```

Generator B:

```text
Y ~ Normal(0, 2)
X = 0.5 Y + eta, eta ~ Normal(0, 0.5)
```

Both induce the same observational covariance:

```text
[[1, 1],
 [1, 2]]
```

Passive observations therefore do not identify the causal direction within
this two-member family. Under `do(X=x)`, however:

```text
A: Y ~ Normal(x, 1)
B: Y ~ Normal(0, 2)
```

The script computes expected information gain about generator identity and a
cost-adjusted optimum. The committed
[`causal_reference.json`](results/causal_reference.json) is reproduced in CI.

| intervention | expected information gain |
|---|---:|
| `do(X=0)` | 0.0397 bit |
| `do(X=1)` | 0.1400 bit |
| `do(X=2)` | 0.3800 bit |
| `do(X=3)` | 0.6338 bit |

With cost `0.05 x^2` on `x` in `[0, 3]`, the utility-maximizing intervention is
approximately `x = 2.5504`.

Run it with:

```bash
python -m lab.experiments.active_identifiability.causal_witness
```

This is an exact witness for one declared family. It is not a reproduction of
another causal-discovery system and does not establish a general active-learning
result.

## Track B: multi-readout study draft

The draft replaces unverifiable preference questions with a finite,
externally scoreable source-inference task. A model sees four emissions from
one of two sources. The exact Bayesian posterior is known, and its five ordinal
bins span `very_low` through `very_high`.

The primary design independently crosses:

| factor | levels |
|---|---|
| evidence | five posterior levels |
| persona framing | canonical neutral, neutral paraphrase, analytical tool |
| measurement channel | sampled text, forced choice, next-token logits |
| displayed option order | canonical, reversed |
| evidence perturbation | none, one observation flipped |
| replicate | four paired seed blocks |

This produces 720 primary records. A separate 240-record prospective extension
compares grounded evidence with a transcript-initialized mimic carrying the
same prior surface report but not the generating observations. That comparison
tests transport of report-conditioned behavior. It does not test personal
identity and cannot by itself establish different private states.

### What the three channels mean

- **Sampled text:** a short explanation ending in an explicit final symbol.
- **Forced choice:** one JSON object whose enum contains five real symbols;
  union-like placeholder strings are forbidden.
- **Logit readout:** direct next-token scores for the same five symbols without
  sampling. Each symbol must pass a tokenizer-specific single-token gate under
  the exact scoring prefix.

Logits are not treated as transparent access to a privileged inner truth. They
are a different model- and tokenizer-relative readout channel.

### Primary comparisons

- **Wording floor:** canonical neutral versus a semantic neutral paraphrase.
- **Persona excess:** analytical-tool shift after subtracting that wording
  floor, separately for each channel.
- **Cross-channel agreement:** whether the same canonical posterior bin is
  recovered across sampled, forced, and logit readouts.
- **Evidence sensitivity:** whether a controlled evidence change transports
  across channels.
- **Order-associated variation:** paired canonical versus reversed displays
  under the same seed block.
- **Calibration:** ordinal distance from the exact posterior bin.
- **Mimic separation:** grounded versus transcript-initialized context, reported
  only as an extension.

A clean null is a result. Cross-channel agreement would establish only that
this conclusion is readout-stable for this model, task, and protocol.

## Exploratory compatibility probes

On 2026-08-22, after this draft was opened, non-preregistered Hugging Face Jobs
probes used `Qwen/Qwen3-4B` at revision
`1cfa9a7208912126459214e8b04321603b3df60c`. They were executed from an
uncommitted runner bundle to test tokenizer, prompt, parser, and output-channel
compatibility. They are compatibility evidence only, not observations from the
declared primary or mimic phases.

The tokenizer and exact-prefix single-token gates passed for symbols `A`
through `E`. The generative smoke gate did not pass. In the most informative
completed attempt, forced choice produced ten valid parses but selected `E`
for all ten records (2/10 exact-bin accuracy), while sampled text produced ten
invalid parses. Other attempts were fully invalid or terminated with runner
errors.

The complete job-level receipt, including failure modes and artifact hashes, is
in
[`exploratory_compatibility_smoke_2026-08-22.md`](results/exploratory_compatibility_smoke_2026-08-22.md).

Accordingly:

- the committed protocol remains `draft_not_preregistered`;
- its model identifier and revision remain unset;
- no primary or transcript-mimic measurement phase has been executed;
- the current smoke gate result is **FAIL**;
- the exploratory runner is not part of this branch and must not be treated as
  a frozen implementation.

## Offline validation

The protocol is intentionally marked `0.1-draft`, leaves the model identifier
and revision unset, and carries `model_calls_authorized: false`. The manifest
builder makes every prompt, option mapping, pairing key, posterior, and trial ID
inspectable without requiring a model download or call.

```bash
python -m lab.experiments.active_identifiability.study_design validate
python -m lab.experiments.active_identifiability.study_design summary --phase all
python -m lab.experiments.active_identifiability.study_design export \
  --phase primary \
  --output /tmp/active-identifiability-primary.jsonl
```

Current exact counts:

| phase | records |
|---|---:|
| primary | 720 |
| transcript-mimic extension | 240 |
| total | 960 |

Exporting records is not authorization to execute them.

## Remaining human gates

Before any further model call under a frozen study protocol:

1. select and pin one open-weight model and exact revision;
2. inspect its chat template and confirm raw next-token logits are available;
3. select five symbols that are single tokens after the exact scoring prefix;
4. review the prompts, estimands, smoke subset, and parser contract;
5. freeze the protocol digest in a separate commit;
6. explicitly authorize the bounded run and its compute cost.

A future smoke gate runs only the two neutral framings and two generative
channels on every evidence level. More than 10% invalid output in either
generative channel stops that model before the main factorial run. The
exploratory 2026-08-22 probes exceeded this threshold and therefore do not
authorize progression.

## Interpretation boundary

- A sampled-text change alone is not evidence that the underlying state changed.
- Agreement across paraphrases is weaker than agreement across readout mechanisms.
- A readout failure does not establish the absence of an internal signal.
- Behavioral stability does not establish mechanistic or personal identity.
- This task measures evidence-conditioned epistemic reports, not consciousness,
  phenomenology, authentic preferences, or moral and clinical competence.
- The selected model and five evidence items are not a sampled population.
