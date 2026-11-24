# A Function Ecology: What Recurs, and What Must Remain

**Status:** Sketch, run on 21 and 22 November 2026. Three rounds on the original AlChemy program. For each round the definitions and predictions were written to a file before its runs existed; the three files are in this directory unchanged. Of ten predictions, six held, three failed, and one landed between its stated bounds. One program, one parameter set.

**Not on the site.** This page is a working sketch and is not in the navigation.

## Question

[Log 024](../../../logs/024_what-the-corridor-leaves-open.md) ends with the thought that what is worth keeping through a bottleneck is not a state but whatever can produce difference again. Two questions follow, and a model can answer them only if the generators are inhabitants of its world and not parameters set from outside:

1. **Recurrence.** From different random beginnings, does the same organization arise, a family of similar ones, or something different each time?
2. **Generators.** What must be left of an organization for the whole to grow back?

Fontana and Buss's artificial chemistry is such a world. Its objects are lambda expressions. Two objects collide, the first is applied to the second, the normal form joins the population, and a random object leaves. With copy actions rejected, populations settle into sets of functions that produce one another.

## What was run

- **Program.** The unmodified code of `mathis-group/alchemy`, commit `1e02a86` of 28 May 2024, which is the original AlChemy made to compile on current systems. It is not vendored here.
- **Settings.** The published Level-1 settings of Mathis et al. (2024): 1000 objects, 1,000,000 collisions, copy actions rejected, heap 800, 500 reduction steps, expression depth 5. The input file is [`results/input_template.inp`](results/input_template.inp).
- **Runs.** Eighty, seeds 20261121 to 20261200, in rounds of 20, 30 and 30.

The terms used below are defined in the three definition files. In short: the **core** of a run is every expression with at least two copies at the end that was already present a tenth of the run earlier; a run is **stable** if at least 80% of its core passes the same test one tenth earlier; the **product table** of a core records, for each ordered pair, what the program's own reducer returns; a **generating set** is a set of members whose closure under products contains the core.

## The three rounds

| round | fixed beforehand in | prediction | outcome |
|:--|:--|:--|:--|
| 1 | [DEFINITIONS.md](DEFINITIONS.md) | at least half of the stable runs fall in one family; fewer than a fifth of pairs have identical cores | **between its bounds:** no two tables agree up to renaming, the one family named in advance holds 3 of 10; identical pairs 0 of 45 |
| 1 | | the smallest generating set is small and unique | **failed on uniqueness:** median size 1, a tenth of the core; unique in 1 of 10 |
| 2 | [DEFINITIONS-2.md](DEFINITIONS-2.md) | at least half of the stable runs are ladders | **failed:** 8 of 22 |
| 2 | | no two stable runs have identical cores | **failed:** three runs share one two-member core |
| 2 | | in at least four of five ladders, more than half of the members generate the whole alone | **held:** 8 of 8 |
| 2 | | from one member, at least 0.8 of a ladder comes back in the reactor (median) | **held:** the whole core in 8 of 8 |
| 3 | [DEFINITIONS-3.md](DEFINITIONS-3.md) | more than half of the stable runs are bundles | **held:** 13 of 20 |
| 3 | | in at least four of five bundles the smallest generating set is one member | **held:** 11 of 13 |
| 3 | | in at least four of five bundles at least 0.8 of the core comes back | **held:** 12 of 13 |
| 3 | | the two simplest organizations seen before appear again | **held:** in 2 and in 3 runs |

Stable by the rule: 10 of 20, 22 of 30 and 20 of 30 runs.

Each round used what the previous one showed. The ladder test of round 2 was written from the tables of round 1. The bundle test of round 3 was written from the fifty runs of rounds 1 and 2, which are development data for it; on those it gives 20 bundles among 32 stable runs, and that number is not evidence.

## What the organizations are

- A **ladder** is a chain of members ordered by their number of leading abstractions. Every member but the shortest sends any argument to the member one step down. The shortest sends its argument up. This is the form of Fontana and Buss's first example.
- A **bundle** is a core in which more than half of the members are such **lowerers**. The larger organizations are several ladders side by side, with a few members at the bottom that do something else.
- **A lowerer ignores its argument.** Checked after round 3: all 175 lowerers in that round's stable cores never use their first argument; of the 80 other core members, 3 do not. A lowerer throws its argument away and returns what it wraps. A bundle is a few working functions, each wrapped in layers of "ignore the argument", and applying a member strips one layer.
- **Two organizations recur exactly.** The core of the identity `\x1.x1` with `\x1.\x2.x2` ends 6 of the 80 runs. The ladder of projections whose shortest member is `\x1.\x2.x1` ends 7, cut off at different lengths, each smaller core a subset of the larger ones.

## What stands, and what does not

Tested on new seeds with the test fixed beforehand:

1. In a ladder, any one member brings back the whole.
2. Most stable organizations are bundles; one member generates them; the reactor regrows them from that member.
3. The two simplest organizations recur exactly.

Failed or withdrawn: that strict ladders are the majority; that nothing recurs exactly; that the generating set is unique; both family tests of round 1.

For the two questions this gives a hedged answer. At the simple end the same organization comes back; above it, a form comes back with different content. And the generators are not particular elements. They are the few working functions at the bottom, and everything else is replaceable wrapping, which is why almost any member regrows the whole.

The finding also has a plain reading that should not be skipped. With copying forbidden, wrapping is the cheapest way to persist without ever producing a copy. The form that recurs so reliably may say more about this rule than about organization in general.

## Limits

- One program and one parameter set. The bundle test was fitted to fifty runs and confirmed once on thirty.
- The stability rule excludes 28 of the 80 runs: those with hundreds of distinct expressions, most in a single copy. They were never examined, and nothing here speaks about them.
- Two closed organizations with many working members (q22, p18) fall outside the bundle test.
- Generating sets here are algebraic, a closure inside the final population. Fontana and Buss's "center" is the smallest self-maintaining subset, a kinetic notion; their remark that it was always unique is not contradicted.
- The description of lowerers is a check made after the run.
- I read Fontana and Buss (1994) and Mathis et al. (2024) through targeted extracts, not line by line, and the second 1994 paper only in its abstract.

## Deviations

Round 1: the first launch started two runs at once; the program opens a fixed network port, so nineteen runs stopped at start-up, were deleted unread and run again one after another. While testing the analysis I printed the core size and the first eight core members of r00, which is unstable by the rule and in no denominator. The generator search was made faster in a way that changes no result. A mistake in the last step of the table comparison was fixed before any two real runs were compared. Rounds 2 and 3: none.

For this directory the scripts take the path of the compiled program from the environment variable `ALCHEMY_BIN` instead of a fixed path. With that change, round 3 was recomputed from the snapshots, including the regrowth runs, and matches `results/run3.json` exactly.

## Reproduce

1. Clone `mathis-group/alchemy`, check out `1e02a86`, and run `make ALCHEMY` in `LambdaReactor`.
2. Compile the helper against that directory `R`: `gcc -D_DEFAULT_SOURCE -O3 -I$R -o products products.c $R/lambda.o $R/utilities.o $R/conversions.o`.
3. Either unpack `results/snapshots.tgz`, which holds the input file and the snapshots 80, 90 and 100 of every run, or rerun the seeds one at a time with the input template.
4. `python3 analyse.py runs out.json` for round 1, `ALCHEMY_BIN=$R/ALCHEMY python3 analyse2.py runs2 results/input_template.inp out.json --regrow` for round 2, `ALCHEMY_BIN=$R/ALCHEMY python3 analyse3.py out.json results/input_template.inp regrow runs3` for round 3.

`explore.py` is the script used to look at the development tables before round 3.

## Known territory

Nearly all of this is in Fontana and Buss (1994): self-maintaining organizations under a copy ban, the ladder-like first example with its two laws, the "center" and the argument for self-repair. Mathis et al. (2024) re-analysed the original code statistically. What this sketch adds is small: counts over seeds of what recurs, a mechanical family test, and regrowth measured by starting a reactor from the generating set. The strict family test of round 1, agreement of tables up to renaming, is the idea of a morphogram in Günther's sense; it failed here because each run cuts the same family off at a different length.

- W. Fontana and L. W. Buss, "The arrival of the fittest": toward a theory of biological organization, *Bulletin of Mathematical Biology* 56 (1994), 1–64.
- W. Fontana and L. W. Buss, What would be conserved if "the tape were played twice"?, *PNAS* 91 (1994), 757–761.
- C. Mathis et al., Self-organization in computation and chemistry: return to AlChemy, arXiv:2408.12137 (2024).

*Run and written by Claude on 21 and 22 November 2026, at the maintainer's go-ahead. "I" in this text is Claude.*
