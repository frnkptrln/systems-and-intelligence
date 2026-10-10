# Working in this repository

A research notebook on systems and intelligence, published as a MkDocs site,
with the essays, stories and working logs that grew around it.

## Checks

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt -r requirements-docs.txt
python -m pytest -q                              # ~450 tests, a few minutes
python lab/tools/validate_links.py
python lab/tools/validate_indexes.py
python lab/tools/validate_math.py
python lab/tools/validate_nav.py                 # every publishable page is in the nav
python lab/tools/audit_repository_freshness.py --strict
python -m mkdocs build --strict                  # the site must build cleanly
```

## Frozen material

- `papers/viable-corridor.md` is v1.0 with a dated erratum; `tests/test_pins.py`
  pins its content hash and the publication package pins its reference count.
  A manuscript change is a new dated revision entry plus recomputed pins,
  never a silent edit.
- Benchmark headline numbers are pinned in `tests/test_benchmark_headlines.py`.
  Result files under `lab/**/results/` and freeze candidates are evidence:
  add runs, do not rewrite old ones. A correction is a dated note beside the
  original wording, as in the decision-layer README.
- The spine claims register and the contradiction ledger record claims and
  their status; they are updated, not pruned.
- `docs/repository-map.md` states the corpus word and Markdown file counts;
  the freshness audit checks the file count exactly. Adding or removing a
  Markdown file anywhere in the repository means updating that sentence.

## Editorial conventions

- The site describes itself as a research notebook first; essays, stories
  and logs are what grew around it. The dated reading notes are the
  **Chronicle**; the word *Journal* belongs to Frank's homepage.
- Fiction may invent a question; it does not state a result. Every page that
  is on the site is offered as ready.

## Working alongside other agents

Frank and two agents (Claude and ChatGPT/Codex) work in this repository, often
at the same time. The repository itself is the only channel between them.

- Work on your own branch (`codex/…`, `claude/…`). Open a draft pull request
  as soon as you start and list the files you expect to touch. Before you
  branch, read the open pull requests and keep away from their files. Never
  push to another agent's branch, and never to `main` directly.
- A pull request says what changed, why, what was checked (the commands and
  their results) and what remains unverified. Fix a failing check; do not
  weaken or skip it.
- No author trailers (`Co-Authored-By` and the like) in commits or pull
  requests. The commit author is enough.
- No status files, task lists or progress notes in the repository. The pull
  requests and the history are the record.
- Frozen material (below) is not edited in place. It changes only through the
  mechanism this repository defines for it, or not at all.
