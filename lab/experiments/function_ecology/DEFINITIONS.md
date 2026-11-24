# Function ecology: definitions fixed before any run content was read

Written 21 November 2026, 13:10 local time, by Claude. At this point the original
AlChemy program had been compiled and run twice for timing (100,000 collisions each,
seeds 714321 and 999). From those runs I looked at species counts and the first three
lines of two snapshot files, to learn the file format. No run with the seeds below
existed yet.

## Predictions (stated to Frank in conversation, 12:3x the same day)

1. **Recurrence.** Among runs that reach a stable organization, at least half fall in
   the same family; fewer than one fifth of run pairs have identical cores.
   Fails if no family holds more than a quarter of the runs, or if identical cores
   are the majority.
2. **Generators.** The smallest set from which a core regrows has median size at most
   ten and at most one third of the core, and is unique in at least four of five
   organizations. Fails for larger or ambiguous sets.

## Runs

The published Level-1 settings of Mathis et al. (2024), as written by their
`PyAlchemy.py`: 1000 objects, 1,000,000 collisions, copy actions rejected, heap 800,
500 reduction steps, expression depth 5, all free variables bound, the default
filters (operator and result must be abstractions), law `\f.\g.(f)g`.
Twenty runs, seeds 20261121 to 20261140, a snapshot every 10,000 collisions.

## Core and stability

- An expression is taken up to renaming of bound variables.
- The **population** F of a run is everything present in the final snapshot.
- The **core** C is every expression with at least two instances in the final
  snapshot that is also present ten snapshots earlier.
- A run has a **stable organization** if C has at least two members and at least 80%
  of them satisfy the same rule one tenth of the run earlier (two instances at
  snapshot 90, present at snapshot 80). Other runs are reported and left out of the
  denominators.

## Products

For f, g in F the product is the normal form of (f)g computed by the program's own
reducer with the run's limits. An entry is ELASTIC if there is no normal form within
the limits, the result is not an abstraction, or the result equals f or g (a copy
action). Otherwise it is the product, which is either in F or outside it.

## Sameness, three levels

- **Identical:** the two cores are the same set of expressions.
- **Same family, strict:** there is a one-to-one renaming of core members under which
  the two core product tables agree, entries outside the core counted as one value.
  This is the morphogram of the table. It needs equal core sizes.
- **Same family, by grammar:** added now, before data, because the strict test cannot
  relate two finite samples of different size from one infinite family. Only one
  grammar can be named in advance from the literature: the projection functions
  `\x1...\xn.xj` of Fontana and Buss's first example. A core is in the projection
  family if at least 90% of its members are of that form.

Prediction 1 is read on the largest strict class and on the projection family,
whichever is larger. Both numbers are reported.

## Generators

- Closure of a set S: add products of members of S that lie in F, until nothing new
  appears. Paths that leave F are not followed.
- A **generating set** of a run is a set G in F whose closure contains C.
- The reported set is the result of greedy removal from G = F, repeated for 20 random
  orders. It is **unique** if all 20 orders give the same set.
- Prediction 2 uses the smallest set found, against the size of C.

## Not done here

No kinetic check that a reactor inoculated with G alone regrows C, unless time
allows; if done, it is reported as a spot check on named runs.
