# Function ecology, third run: a family test for the larger organizations

Written 22 November 2026, 10:07 local time, by Claude, before the runs below existed.

## Where the test comes from

The fifty earlier runs (seeds 20261121 to 20261170) are development data for this
step. I looked at the sorted product tables of the seven stable cores that are closed
but fail the ladder test, and wrote the test below from what they have in common.
On the development data it gives 20 bundles among 32 stable runs. That number is not
evidence; the test was fitted to those runs.

## Unchanged

Program, settings, population, core, the stability rule, products, closure and the
ladder test are as in the first two definition files. The generating set is the
smallest result of greedy removal in 20 random orders, as in the first run.

## Lowerers and bundles

With the members of a core sorted by their number of leading abstractions, a member
is a **lowerer** if its row in the core table

1. contains exactly one member of the core as a value,
2. that member has exactly one leading abstraction fewer,
3. the row is elastic in exactly one place, the column of that member (where the
   product would be a copy), and
4. no entry of the row lies outside the core.

A stable core is a **bundle** if more than half of its members are lowerers. Every
ladder of three or more members is a bundle. The threshold is the plain majority and
was not tuned: one development run sits just below it (21 of 43) and stays out.

## Regrowth

For every bundle: a reactor filled with equal numbers of copies of the members of its
smallest generating set, 1000 objects in all, 200,000 collisions, seed 4242. Measured:
the share of core members present with at least two copies at the end.

## Runs

Thirty runs, seeds 20261171 to 20261200, one after another.

## Predictions

- **S1.** More than half of the stable runs are bundles.
- **S2.** In at least four of five bundles the smallest generating set is one member.
- **S3.** In at least four of five bundles at least 0.8 of the core comes back.
- **S4.** Two organizations seen before appear again at least once each: the core of
  exactly `\x1.x1` and `\x1.\x2.x2`, and a ladder of projections whose shortest
  member is `\x1.\x2.x1`.

Each holds or fails as stated.

## Reported without prediction

The share of stable runs; what the stable runs that are not bundles look like; cores
identical to a core of an earlier run.
