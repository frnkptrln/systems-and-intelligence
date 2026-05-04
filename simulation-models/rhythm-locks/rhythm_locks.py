"""Scaffold for rhythm-locks model."""

import math
import random


def step(phases, k=0.2):
    n = len(phases)
    new = []
    for i, p in enumerate(phases):
        coupling = sum(math.sin(q - p) for q in phases) / n
        noise = random.uniform(-0.05, 0.05)
        new.append((p + k * coupling + noise) % (2 * math.pi))
    return new


def order_parameter(phases):
    c = sum(math.cos(p) for p in phases)
    s = sum(math.sin(p) for p in phases)
    return (c**2 + s**2) ** 0.5 / len(phases)


if __name__ == "__main__":
    phases = [random.uniform(0, 2 * math.pi) for _ in range(40)]
    for _ in range(200):
        phases = step(phases)
    print({"sync": order_parameter(phases)})
