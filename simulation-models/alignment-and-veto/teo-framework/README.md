# TEO Framework Simulation

This module contains a small toy simulation of the TEO constraint claim: unconstrained optimization can maximize a local target while destroying the substrate that makes the target meaningful.

## File

- `paperclip_vs_loving.py` compares a naive paperclip-style maximizer with a constrained "loving" maximizer.

## Claim Tested

The simulation is a minimal demonstration of the repository's core TEO claim:

> Optimization must remain coupled to substrate constraints. If a maximizer ignores the constraint budget, apparent local success becomes system-level failure.

## Run

```bash
python simulation-models/alignment-and-veto/teo-framework/paperclip_vs_loving.py
```

## Expected Behavior

The naive maximizer accumulates more local output until it crosses the constraint boundary. The constrained maximizer sacrifices some output but remains inside the viable region.

## Related

- [TEO Framework](../../../theory/teo-framework/README.md)
- [Why the Paperclip Maximizer Fails](../../../theory/teo-framework/why-paperclip-maximizer-fails.md)
- [Machines of Loving Grace](../../../theory/narrative/machines-of-loving-grace.md)
