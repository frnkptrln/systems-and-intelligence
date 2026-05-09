"""
L-systems: parallel rewriting as generative morphology.

Run:
    python3 l_systems.py --preset plant --iterations 5
"""

from __future__ import annotations

import argparse
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class LSystem:
    axiom: str
    rules: dict[str, str]
    angle_degrees: float
    step: float
    draw_symbols: frozenset[str]


PRESETS: dict[str, LSystem] = {
    "plant": LSystem(
        axiom="X",
        rules={"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"},
        angle_degrees=25.0,
        step=1.0,
        draw_symbols=frozenset({"F"}),
    ),
    "koch": LSystem(
        axiom="F",
        rules={"F": "F+F-F-F+F"},
        angle_degrees=90.0,
        step=1.0,
        draw_symbols=frozenset({"F"}),
    ),
    "sierpinski": LSystem(
        axiom="A",
        rules={"A": "B-A-B", "B": "A+B+A"},
        angle_degrees=60.0,
        step=1.0,
        draw_symbols=frozenset({"A", "B"}),
    ),
}


def expand(system: LSystem, iterations: int) -> str:
    state = system.axiom
    for _ in range(iterations):
        state = "".join(system.rules.get(symbol, symbol) for symbol in state)
    return state


def interpret(system: LSystem, state: str) -> np.ndarray:
    x = 0.0
    y = 0.0
    heading = math.pi / 2.0
    angle = math.radians(system.angle_degrees)
    stack: list[tuple[float, float, float]] = []
    segments: list[tuple[float, float, float, float]] = []

    for symbol in state:
        if symbol in system.draw_symbols:
            nx = x + math.cos(heading) * system.step
            ny = y + math.sin(heading) * system.step
            segments.append((x, y, nx, ny))
            x, y = nx, ny
        elif symbol == "f":
            x += math.cos(heading) * system.step
            y += math.sin(heading) * system.step
        elif symbol == "+":
            heading += angle
        elif symbol == "-":
            heading -= angle
        elif symbol == "[":
            stack.append((x, y, heading))
        elif symbol == "]" and stack:
            x, y, heading = stack.pop()

    return np.array(segments, dtype=float)


def metrics(state: str) -> dict[str, float]:
    counts = Counter(state)
    total = sum(counts.values())
    probabilities = np.array([count / total for count in counts.values()], dtype=float)
    entropy = float(-(probabilities * np.log2(probabilities)).sum())

    depth = 0
    max_depth = 0
    for symbol in state:
        if symbol == "[":
            depth += 1
            max_depth = max(max_depth, depth)
        elif symbol == "]":
            depth = max(0, depth - 1)

    return {
        "symbols": float(total),
        "unique_symbols": float(len(counts)),
        "branch_events": float(counts.get("[", 0)),
        "max_branch_depth": float(max_depth),
        "symbol_entropy_bits": entropy,
    }


def plot_segments(segments: np.ndarray, preset: str, iterations: int, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="#0a0d12")
    ax.set_facecolor("#0a0d12")

    if len(segments):
        for x1, y1, x2, y2 in segments:
            ax.plot([x1, x2], [y1, y2], color="#7fe0a1", linewidth=0.45, alpha=0.9)
        ax.set_aspect("equal", adjustable="box")
        margin = 2.0
        ax.set_xlim(float(segments[:, [0, 2]].min()) - margin, float(segments[:, [0, 2]].max()) + margin)
        ax.set_ylim(float(segments[:, [1, 3]].min()) - margin, float(segments[:, [1, 3]].max()) + margin)

    ax.set_title(f"{preset} L-system | {iterations} iterations", color="#e7eef8")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout(pad=0)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and render simple L-systems.")
    parser.add_argument("--preset", choices=sorted(PRESETS), default="plant")
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--output", type=Path, default=Path("l_system.png"))
    args = parser.parse_args()

    system = PRESETS[args.preset]
    state = expand(system, args.iterations)
    segments = interpret(system, state)
    result = metrics(state)
    plot_segments(segments, args.preset, args.iterations, args.output)

    print(f"preset: {args.preset}")
    print(f"iterations: {args.iterations}")
    print(f"drawn_segments: {len(segments)}")
    for key, value in result.items():
        print(f"{key}: {value:.4f}")
    print(f"output: {args.output}")


if __name__ == "__main__":
    main()

