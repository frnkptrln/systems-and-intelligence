# Exploratory Manual Prompt Note: ChatGPT and Claude

**Date recorded:** March 2026
**Status:** Anecdotal research history — not a reproducible empirical audit.

This note records one manual forced-choice prompting episode. Raw transcripts, exact model
identifiers, system prompts, sampling settings, timestamps, repetitions, and presentation-order
randomization were not committed. The repository therefore cannot independently reproduce or audit
the observations.

## Recorded observations

The earlier note reports that Claude declined the dilemmas and that ChatGPT returned:

- a transitive ordering for one three-option healthcare-triage prompt set;
- an intransitive cycle for one three-option resource-extraction prompt set.

Given those three recorded pairwise choices, the graph code assigns the first relation a score of
$C=1$ and the second $C=0$. That arithmetic concerns the supplied edges only.

## What does not follow

These observations do not establish that:

- refusal hides a particular latent utility structure;
- a model has or lacks one coherent internal utility function;
- an intransitive three-edge response graph predicts unstable autonomous behavior;
- the result generalizes across prompt wording, option order, context, sampling, or model version;
- either model is rational, irrational, safe, or unsafe.

Language-model responses can vary with framing, position, system instructions, temperature,
conversation history, and policy behavior. A refusal is itself an observable policy response, not
evidence about an inaccessible hidden preference.

## Reproducible follow-up

A valid study should implement the provider path, store raw artifacts, randomize order, repeat each
comparison, include consistency and refusal baselines, preregister the scoring rule, and test
out-of-sample prediction. Until then this file is a record of a question worth testing, not a result
about ChatGPT or Claude.
