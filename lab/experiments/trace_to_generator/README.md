# Trace→Generator: Inverse Prompting Toy Scaffold

Status: Scaffold
Scope: Minimal experiment design for searching prompt/control configurations from desired output constraints.
Epistemic status: Engineering prototype template; no claim of full inverse recovery.
Related files:
- theory/emergence/trace-to-generator.md
- theory/ai/llms-as-probabilistic-automata.md
- theory/core/simulation-theory-map.md
Failure conditions:
- Treating prompt search success as proof of unique generator recovery.
- Ignoring runtime and evaluator bias.

## Goal
Given target output constraints, search for prompt candidates that generate outputs scoring well under an explicit evaluator.

## Components
1. Target constraints (style, facts, structure)
2. Candidate prompts
3. Generator interface (stub)
4. Evaluator
5. Mutation/search loop

## Limits
- No API credentials required; generation backend is mocked by default.
- Reconstruction is non-unique.
- Evaluator choices strongly shape recovered candidates.

## Run
```bash
python lab/experiments/trace_to_generator/prompt_search_toy.py
```
