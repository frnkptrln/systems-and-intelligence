"""
Iterated Function Systems: small transformation sets, stable global form.

Run:
    python3 ifs_attractors.py --preset barnsley --points 120000
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class AffineMap:
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float
    p: float

    def apply(self, x: float, y: float) -> tuple[float, float]:
        return (
            self.a * x + self.b * y + self.e,
            self.c * x + self.d * y + self.f,
        )


PRESETS: dict[str, list[AffineMap]] = {
    "barnsley": [
        AffineMap(0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01),
        AffineMap(0.85, 0.04, -0.04, 0.85, 0.0, 1.60, 0.85),
        AffineMap(0.20, -0.26, 0.23, 0.22, 0.0, 1.60, 0.07),
        AffineMap(-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07),
    ],
    "sierpinski": [
        AffineMap(0.5, 0.0, 0.0, 0.5, 0.0, 0.0, 1.0),
        AffineMap(0.5, 0.0, 0.0, 0.5, 1.0, 0.0, 1.0),
        AffineMap(0.5, 0.0, 0.0, 0.5, 0.5, 0.8660254, 1.0),
    ],
    "dragon": [
        AffineMap(0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 1.0),
        AffineMap(-0.5, -0.5, 0.5, -0.5, 1.0, 0.0, 1.0),
    ],
}


def generate_points(
    maps: list[AffineMap],
    points: int,
    seed: int,
    discard: int = 50,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    probabilities = np.array([m.p for m in maps], dtype=float)
    probabilities = probabilities / probabilities.sum()
    choices = rng.choice(len(maps), size=points + discard, p=probabilities)

    x = 0.0
    y = 0.0
    data = np.zeros((points, 2), dtype=float)
    out_index = 0

    for i, choice in enumerate(choices):
        x, y = maps[int(choice)].apply(x, y)
        if i >= discard:
            data[out_index] = (x, y)
            out_index += 1

    return data


def estimate_box_dimension(data: np.ndarray, min_power: int = 3, max_power: int = 8) -> tuple[float, list[tuple[int, int]]]:
    mins = data.min(axis=0)
    spans = data.max(axis=0) - mins
    spans[spans == 0] = 1.0
    normalized = (data - mins) / spans

    counts: list[tuple[int, int]] = []
    for power in range(min_power, max_power + 1):
        grid_size = 2**power
        cells = np.floor(normalized * grid_size).astype(int)
        cells = np.clip(cells, 0, grid_size - 1)
        occupied = np.unique(cells, axis=0).shape[0]
        counts.append((grid_size, occupied))

    x = np.log([grid for grid, _ in counts])
    y = np.log([count for _, count in counts])
    slope, _ = np.polyfit(x, y, 1)
    return float(slope), counts


def plot_points(data: np.ndarray, preset: str, dimension: float, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 9), facecolor="#080b10")
    ax.set_facecolor("#080b10")
    ax.scatter(data[:, 0], data[:, 1], s=0.05, c=data[:, 1], cmap="viridis", linewidths=0)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(f"{preset} IFS attractor | box dimension ~ {dimension:.3f}", color="#e7eef8")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout(pad=0)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate IFS attractors and estimate box-counting dimension.")
    parser.add_argument("--preset", choices=sorted(PRESETS), default="barnsley")
    parser.add_argument("--points", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output", type=Path, default=Path("ifs_attractor.png"))
    args = parser.parse_args()

    data = generate_points(PRESETS[args.preset], args.points, args.seed)
    dimension, counts = estimate_box_dimension(data)
    plot_points(data, args.preset, dimension, args.output)

    print(f"preset: {args.preset}")
    print(f"points: {args.points}")
    print(f"box_dimension_estimate: {dimension:.4f}")
    print("occupied_boxes:")
    for grid_size, occupied in counts:
        print(f"  {grid_size:4d} -> {occupied}")
    print(f"output: {args.output}")


if __name__ == "__main__":
    main()

