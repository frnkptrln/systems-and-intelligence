# Function ecology, second run: definitions fixed before the runs existed

Written 21 November 2026, 14:31 local time, by Claude, after the first run of twenty
(seeds 20261121 to 20261140) had been analysed and reported to Frank. Everything here
was seen in that first run; this run tests whether it comes back on new seeds.

## Runs

Same program and settings as the first run. Thirty runs, seeds 20261141 to 20261170,
one after another.

## Unchanged from the first run

Population, core, the stability rule, products, closure, and "identical cores" are as
in DEFINITIONS.md. The stability rule excluded half of the first run; it is kept so
the two runs can be compared.

## Ladder test, now fixed in advance

A stable core with at least three members is a **ladder** if, with its members
sorted by their number of leading abstractions,

1. those numbers are consecutive, and
2. for every member except the first, every table entry in its row is the member one
   step down, or elastic in the one column where that product would be a copy.

The first member's row is not constrained. A stable core with two members is counted
as not a ladder.

## Single generators

A member x of a core is a **single generator** if the closure of {x} contains the
whole core. This replaces the twenty random orders of the first run.

## Regrowth in the reactor

For every ladder: a reactor of 1000 copies of one single generator (the first in
sorted order), 200,000 collisions, seed 4242, otherwise the run settings. Measured:
the share of core members present with at least two copies at the end.

## Predictions

- **R1, the family recurs.** At least half of the stable runs are ladders.
- **R2, not the same.** No two stable runs have identical cores.
- **R3, generators are interchangeable.** In at least four of five ladders, more than
  half of the members are single generators.
- **R4, one member is enough.** Across the ladders, the median share of the core that
  comes back in the reactor from one member is at least 0.8.

Each prediction holds or fails as stated; there is no middle range this time.

## Reported without prediction

The share of stable runs; the form of each ladder's first row; whether the same
generating expression occurs in more than one run; what the non-ladder stable runs
look like.
