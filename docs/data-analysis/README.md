# 📊 Data Analysis

Utilities and scripts for processing, visualizing, and statistically
evaluating results from the simulation models.

---

## 📐 Information-Theoretic Measures (`info_measures.py`)

A reusable library for **quantifying emergence** in any simulation.
These measures operationalise the dimensions of the
[System Intelligence Index](../theory/system-intelligence-index.md).

### Spatial measures

| Function | What it measures |
|:---------|:-----------------|
| `shannon_entropy(field)` | Disorder / unpredictability of the field |
| `spatial_mutual_information(field)` | How much a cell reveals about its neighbours |
| `block_entropy(field, k)` | Multi-scale spatial correlations |

### Temporal measures

| Function | What it measures |
|:---------|:-----------------|
| `time_series_entropy(x)` | Temporal unpredictability |
| `transfer_entropy(source, target)` | Causal information flow X → Y |
| `active_information_storage(x)` | How much a process "remembers" |

### Emergence measures

| Function | What it measures |
|:---------|:-----------------|
| `integration(field)` | Whole > sum of parts (simplified Φ) |
| `complexity_measure(field)` | Multi-scale structure (TSE complexity) |

### Quick analysis

```python
from info_measures import analyse_field
results = analyse_field(my_field, name="My Simulation")
```

---

## 🔬 Comparative Analysis (`analyse_emergence.py`)

Runs a full analysis across multiple systems (noise, Game of Life,
Reaction-Diffusion, Sandpile) and outputs:

- Per-system entropy, MI, integration, and complexity
- Comparative bar chart saved to `emergence_analysis.png`

```bash
cd data-analysis
python3 analyse_emergence.py
```

---

## Why This Matters

Most claims about "emergence" in complex systems remain qualitative.
These tools make it possible to **measure** emergence and compare
systems on a common scale – the first step toward a rigorous,
quantitative theory of system intelligence.
