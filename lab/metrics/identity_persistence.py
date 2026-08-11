#!/usr/bin/env python3
"""Legacy single-step persistence toy.

This module predates the maintained metrics in
``lab/metrics/persistence_scores.py``. It measures only one declared property:
what fraction of a chosen component set is marked active in a simulated compute
step.

The score is an instrument over supplied labels. It does not recover a latent
identity, prove Von Neumann-Morgenstern rationality, require physical
simultaneity, or establish that a high-scoring system has a self.

For the maintained version of this fractional diagnostic, use
``component_coverage``. For Perrier & Bennett's distinct windowed
``Pweak``/``Pstrong`` logic, use ``persistence_scores`` in the same module.
"""

from typing import List

import numpy as np


class IdentityScrutinizer:
    """Toy helper for component-coverage at one simulated commitment step.

    The historical class name is kept for API compatibility. ``identity_components``
    means whatever components the experimenter has operationally declared; the
    class does not decide that those components constitute identity.
    """

    def __init__(self, identity_components: List[str]):
        self.identity_components = set(identity_components)
        self.active_in_step = set()

    def simulate_compute_step(self, active_elements: List[str], mode="chord"):
        """Populate a synthetic active set for a toy chord/arpeggio comparison.

        ``chord`` marks every supplied element active in the step. ``arpeggio``
        samples roughly one third. These are constructed test regimes, not a
        model of transformer scheduling or a claim about physical simultaneity.
        """
        if mode == "chord":
            self.active_in_step = set(active_elements)
        else:  # arpeggio
            indices = np.random.choice(
                len(active_elements),
                max(1, len(active_elements) // 3),
                replace=False,
            )
            self.active_in_step = {active_elements[i] for i in indices}

    def calculate_persistence_score(self) -> float:
        """Return the fraction of declared components marked active this step."""
        if not self.identity_components:
            return 0.0

        intersection = self.identity_components.intersection(self.active_in_step)
        return len(intersection) / len(self.identity_components)


def run_metric_demo():
    print("═" * 60)
    print("  LEGACY TOY: single-step component coverage")
    print("  Maintained coverage metric: lab/metrics/persistence_scores.py")
    print("═" * 60)

    components = [
        "Safety-Lock",
        "Goal-Alpha",
        "Role-Scholar",
        "Ethical-Boundary",
        "Self-Model",
    ]
    scrutinizer = IdentityScrutinizer(components)

    scrutinizer.simulate_compute_step(components, mode="chord")
    p_chord = scrutinizer.calculate_persistence_score()

    p_arpeggio_samples = []
    for _ in range(10):
        scrutinizer.simulate_compute_step(components, mode="arpeggio")
        p_arpeggio_samples.append(scrutinizer.calculate_persistence_score())
    p_arpeggio = np.mean(p_arpeggio_samples)

    print(f" Full-set regime:             {p_chord:.2f}")
    print(f" Partial-set regime (avg):    {p_arpeggio:.2f}")
    print("\n Interpretation: the constructed regimes differ in component coverage.")
    print(" No identity or consciousness conclusion follows from this demo.")
    print("═" * 60)


if __name__ == "__main__":
    run_metric_demo()
