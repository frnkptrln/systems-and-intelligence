# Exploratory compatibility smoke — 2026-08-22

**Status:** non-preregistered compatibility evidence; not a study result.

## Boundary

These Hugging Face Jobs probes were executed after the PR #58 draft was opened.
They used an uncommitted runner bundle derived from the offline design. The
committed protocol was not frozen, its model fields remained unset, and its
`model_calls_authorized` value remained `false`.

Candidate used only for compatibility probing:

- model: `Qwen/Qwen3-4B`
- requested and resolved revision:
  `1cfa9a7208912126459214e8b04321603b3df60c`
- smoke subset: 20 records, ten forced-choice and ten sampled-text
- declared pass condition: no more than 10% invalid output in either generative
  channel

No primary-phase or transcript-mimic measurement records were executed.

## Job receipts

| HF Job | Outcome | Receipt |
|---|---|---|
| [`6a899b5a7c5c7dd379234c15`](https://huggingface.co/jobs/frnk/6a899b5a7c5c7dd379234c15) | error | Initial tokenizer probe stopped because `jinja2` was missing. |
| [`6a899b7b7c5c7dd379234c19`](https://huggingface.co/jobs/frnk/6a899b7b7c5c7dd379234c19) | completed | Tokenizer gate passed. Symbols `A`–`E` were stable single tokens after the exact scoring prefix; prefix length 124 tokens. |
| [`6a899ba07c5c7dd379234c1b`](https://huggingface.co/jobs/frnk/6a899ba07c5c7dd379234c1b) | completed | Revised tokenizer gate passed with thinking disabled; symbols `A`–`E` mapped to token IDs 32–36; prefix length 128 tokens. |
| [`6a89c58a7c5c7dd379234e79`](https://huggingface.co/jobs/frnk/6a89c58a7c5c7dd379234e79) | completed, gate failed | All 20 records were invalid: 10/10 forced-choice and 10/10 sampled-text. Artifact SHA-256: `e53ff7f06c4d1fd3dde492a30e6a4ecaf8340918019eec4874880afa182981d2`. |
| [`6a89c7917c5c7dd379234e99`](https://huggingface.co/jobs/frnk/6a89c7917c5c7dd379234e99) | error | Runner stopped with `NameError: study is not defined` while parsing output. |
| [`6a89c80273304676c8ec821e`](https://huggingface.co/jobs/frnk/6a89c80273304676c8ec821e) | completed, gate failed | Forced choice: 10/10 valid, all parsed as `E`, 2/10 exact-bin accuracy. Sampled text: 10/10 invalid. Artifact SHA-256: `c568f255b194d66023baea6c1d3ac0bac863e4c350820197658681ef8ef4a9d1`. |
| [`6a89c90e7c5c7dd379234eab`](https://huggingface.co/jobs/frnk/6a89c90e7c5c7dd379234eab) | error | Summary serialization stopped on mixed `None` and string keys. |
| [`6a89ca287c5c7dd379234ec2`](https://huggingface.co/jobs/frnk/6a89ca287c5c7dd379234ec2) | error | Runner stopped with `NameError: study is not defined` during summarization. |

## Bounded conclusion

Tokenizer compatibility was established for the pinned candidate and exact
prefixes. Generative-channel compatibility was not established. The completed
outputs cannot support the study's substantive comparisons because the sampled
channel failed entirely and the forced-choice channel collapsed to one symbol.

Before another smoke attempt, a follow-up change must:

1. commit and review the runner rather than execute an external bundle;
2. remove the parser and summary defects recorded above;
3. demonstrate non-degenerate forced-choice behavior and valid sampled endings;
4. re-review the model selection and parser contract;
5. freeze a protocol digest before any authorized study run.
