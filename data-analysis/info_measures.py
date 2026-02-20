#!/usr/bin/env python3
"""
Information-Theoretic Measures for Emergent Systems
-----------------------------------------------------

A reusable library of information-theoretic functions for analysing
the simulations in this repository.  These measures make the
System Intelligence Index (SII) **quantitative** rather than conceptual.

Measures provided:

    SPATIAL
    ├── shannon_entropy(field)         – spatial disorder
    ├── spatial_mutual_information()   – local–global coupling
    └── block_entropy(field, k)        – multi-scale complexity

    TEMPORAL
    ├── time_series_entropy(x)         – temporal unpredictability
    ├── transfer_entropy(x, y, lag)    – causal influence X→Y
    └── active_information_storage()   – memory in a process

    EMERGENCE
    ├── integration(field)             – whole > sum of parts
    └── complexity_measure(field)      – TSE complexity (Tononi et al.)

All functions work on numpy arrays and require no special dependencies
beyond numpy and scipy.
"""

import numpy as np
from scipy.special import digamma
from typing import Optional, Tuple


# ═════════════════════════════════════════════
#  1. SPATIAL MEASURES
# ═════════════════════════════════════════════

def shannon_entropy(field: np.ndarray, bins: int = 64) -> float:
    """
    Shannon entropy H of a spatial field (1D or 2D).

    Measures the amount of "surprise" or disorder in the distribution
    of values. Higher H = more disordered.

        H = -Σ p(x) log₂ p(x)

    Parameters
    ----------
    field : array-like
        A 1D or 2D array of values.
    bins : int
        Number of histogram bins for discretisation.

    Returns
    -------
    float
        Shannon entropy in bits.
    """
    values = np.asarray(field).flatten()
    if values.size == 0:
        return 0.0

    counts, _ = np.histogram(values, bins=bins, density=False)
    probs = counts / counts.sum()
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))


def block_entropy(field: np.ndarray, block_size: int = 2) -> float:
    """
    Block entropy: entropy of k×k blocks in a 2D binary/discrete field.

    Measures spatial correlations: if neighbouring cells are correlated,
    block entropy grows slower than k² × single-cell entropy.

    Parameters
    ----------
    field : 2D array (integer or will be discretised)
    block_size : int
        Side length of the block.

    Returns
    -------
    float
        Block entropy in bits.
    """
    field = np.asarray(field)
    if field.ndim != 2:
        raise ValueError("block_entropy requires a 2D array")

    H, W = field.shape
    k = block_size

    # Discretise to integers if needed
    if not np.issubdtype(field.dtype, np.integer):
        field = (field * 8).astype(int).clip(0, 7)

    # Extract all k×k blocks
    blocks = []
    for i in range(0, H - k + 1, k):
        for j in range(0, W - k + 1, k):
            block = field[i:i+k, j:j+k].flatten()
            blocks.append(tuple(block))

    # Count unique block patterns
    from collections import Counter
    counts = Counter(blocks)
    total = sum(counts.values())
    probs = np.array(list(counts.values())) / total
    return -np.sum(probs * np.log2(probs))


def spatial_mutual_information(
    field: np.ndarray,
    offset: Tuple[int, int] = (1, 0),
    bins: int = 32
) -> float:
    """
    Mutual information between each cell and a shifted version of itself.

    Measures how much a cell's value tells you about its neighbour's value.
    High MI = strong spatial correlations (structure).
    Low MI  = spatial independence (noise).

        I(X; Y) = H(X) + H(Y) - H(X, Y)

    Parameters
    ----------
    field : 2D array
    offset : tuple (dy, dx)
        Spatial shift direction.
    bins : int
        Histogram bins per dimension.

    Returns
    -------
    float
        Mutual information in bits.
    """
    field = np.asarray(field, dtype=np.float64)
    dy, dx = offset

    # Original and shifted
    X = field[:field.shape[0]-abs(dy), :field.shape[1]-abs(dx)].flatten()
    Y = np.roll(np.roll(field, -dy, axis=0), -dx, axis=1)
    Y = Y[:field.shape[0]-abs(dy), :field.shape[1]-abs(dx)].flatten()

    # 2D histogram
    hist_2d, _, _ = np.histogram2d(X, Y, bins=bins)
    pxy = hist_2d / hist_2d.sum()
    px = pxy.sum(axis=1)
    py = pxy.sum(axis=0)

    # MI = H(X) + H(Y) - H(X,Y)
    def H(p):
        p = p[p > 0]
        return -np.sum(p * np.log2(p))

    return H(px) + H(py) - H(pxy)


# ═════════════════════════════════════════════
#  2. TEMPORAL MEASURES
# ═════════════════════════════════════════════

def time_series_entropy(x: np.ndarray, bins: int = 32) -> float:
    """
    Shannon entropy of a time series.

    Parameters
    ----------
    x : 1D array
        Time series values.
    bins : int
        Histogram bins.

    Returns
    -------
    float
        Entropy in bits.
    """
    return shannon_entropy(x, bins=bins)


def transfer_entropy(
    source: np.ndarray,
    target: np.ndarray,
    lag: int = 1,
    bins: int = 16
) -> float:
    """
    Transfer entropy from source → target.

    Measures the amount of information that source provides about
    the FUTURE of target, beyond what target's own past provides.

        TE(X→Y) = H(Y_t | Y_{t-lag}) - H(Y_t | Y_{t-lag}, X_{t-lag})

    This is a non-parametric estimator based on histogram binning.

    Parameters
    ----------
    source : 1D array
        Source time series X.
    target : 1D array
        Target time series Y.
    lag : int
        Time lag k.
    bins : int
        Histogram bins per dimension.

    Returns
    -------
    float
        Transfer entropy in bits (≥ 0).
    """
    source = np.asarray(source, dtype=np.float64)
    target = np.asarray(target, dtype=np.float64)

    n = min(len(source), len(target))
    if n <= lag:
        return 0.0

    # Construct lagged variables
    y_future = target[lag:n]
    y_past   = target[:n-lag]
    x_past   = source[:n-lag]

    # Discretise
    def discretise(arr):
        lo, hi = arr.min(), arr.max()
        if hi == lo:
            return np.zeros_like(arr, dtype=int)
        return np.clip(((arr - lo) / (hi - lo) * (bins - 1)).astype(int), 0, bins - 1)

    y_f = discretise(y_future)
    y_p = discretise(y_past)
    x_p = discretise(x_past)

    # Joint histograms
    # TE = H(y_future, y_past) - H(y_future, y_past, x_past)
    #    + H(y_past, x_past)   - H(y_past)

    def count_entropy(*arrays):
        """Entropy of joint distribution from integer arrays."""
        combined = np.column_stack(arrays)
        # Hash rows to unique integers
        _, counts = np.unique(combined, axis=0, return_counts=True)
        probs = counts / counts.sum()
        return -np.sum(probs * np.log2(probs))

    H_yf_yp    = count_entropy(y_f, y_p)
    H_yf_yp_xp = count_entropy(y_f, y_p, x_p)
    H_yp_xp    = count_entropy(y_p, x_p)
    H_yp       = count_entropy(y_p)

    te = H_yf_yp - H_yf_yp_xp + H_yp_xp - H_yp
    return max(0.0, te)  # TE should be non-negative


def active_information_storage(
    x: np.ndarray,
    lag: int = 1,
    bins: int = 32
) -> float:
    """
    Active information storage (AIS): mutual information between
    a time series and its own past.

        AIS = I(X_t ; X_{t-lag})

    Measures how much the process "remembers" of its own history.

    Parameters
    ----------
    x : 1D array
    lag : int
    bins : int

    Returns
    -------
    float
        AIS in bits.
    """
    x = np.asarray(x, dtype=np.float64)
    n = len(x)
    if n <= lag:
        return 0.0

    current = x[lag:]
    past = x[:n-lag]

    hist_2d, _, _ = np.histogram2d(current, past, bins=bins)
    pxy = hist_2d / hist_2d.sum()
    px = pxy.sum(axis=1)
    py = pxy.sum(axis=0)

    def H(p):
        p = p[p > 0]
        return -np.sum(p * np.log2(p))

    return H(px) + H(py) - H(pxy)


# ═════════════════════════════════════════════
#  3. EMERGENCE / INTEGRATION MEASURES
# ═════════════════════════════════════════════

def integration(field: np.ndarray, n_partitions: int = 4, bins: int = 16) -> float:
    """
    Integration (whole-minus-parts): how much information is lost when
    the field is decomposed into independent sub-regions.

        Φ_approx = H(whole) - Σ H(part_i) / n_partitions

    A positive value means the whole carries more information than the
    sum of its parts – a signature of **emergence**.

    This is a simplified approximation of Tononi's Integrated Information.

    Parameters
    ----------
    field : 2D array
    n_partitions : int
        Split into n×n sub-regions.
    bins : int

    Returns
    -------
    float
        Integration in bits. Positive = emergence.
    """
    field = np.asarray(field, dtype=np.float64)
    H_whole = shannon_entropy(field, bins=bins)

    H, W = field.shape
    ph = H // n_partitions
    pw = W // n_partitions

    H_parts_sum = 0.0
    n_parts = 0
    for i in range(n_partitions):
        for j in range(n_partitions):
            part = field[i*ph:(i+1)*ph, j*pw:(j+1)*pw]
            if part.size > 0:
                H_parts_sum += shannon_entropy(part, bins=bins)
                n_parts += 1

    if n_parts == 0:
        return 0.0

    # Normalised: integration per partition
    return H_whole - H_parts_sum / n_parts


def complexity_measure(field: np.ndarray, max_scale: int = 5, bins: int = 32) -> float:
    """
    Tononi-Sporns-Edelman (TSE) complexity: sum of integration values
    across multiple spatial scales.

    High complexity = the system has structure at MANY scales
    (neither purely random nor purely uniform).

        C = Σ_{k=1}^{k_max} |integration(field, k)|

    Parameters
    ----------
    field : 2D array
    max_scale : int
        Maximum number of partitions per axis.
    bins : int

    Returns
    -------
    float
        Multi-scale complexity (arbitrary units, higher = more complex).
    """
    C = 0.0
    for k in range(2, max_scale + 1):
        C += abs(integration(field, n_partitions=k, bins=bins))
    return C


# ═════════════════════════════════════════════
#  4. UTILITY: Pretty-print a full analysis
# ═════════════════════════════════════════════

def analyse_field(
    field: np.ndarray,
    name: str = "Field",
    time_series: Optional[np.ndarray] = None,
) -> dict:
    """
    Run a full information-theoretic analysis on a 2D field and
    optionally a corresponding time series.

    Parameters
    ----------
    field : 2D array
        Current state of the system.
    name : str
        Label for printing.
    time_series : 1D array, optional
        A scalar time series (e.g. order parameter, density).

    Returns
    -------
    dict
        Dictionary of all computed measures.
    """
    results = {}

    print(f"\n{'═' * 60}")
    print(f"  Information-Theoretic Analysis: {name}")
    print(f"{'═' * 60}")

    # Spatial measures
    H = shannon_entropy(field)
    results["shannon_entropy"] = H
    print(f"\n  Spatial entropy H         = {H:.3f} bits")

    MI = spatial_mutual_information(field)
    results["spatial_MI"] = MI
    print(f"  Spatial mutual info MI    = {MI:.3f} bits")

    BE = block_entropy(field, block_size=2)
    results["block_entropy_2x2"] = BE
    print(f"  Block entropy (2×2)       = {BE:.3f} bits")

    I = integration(field)
    results["integration"] = I
    print(f"  Integration Φ (approx)    = {I:+.3f} bits")

    C = complexity_measure(field)
    results["complexity"] = C
    print(f"  Multi-scale complexity C  = {C:.3f}")

    # Temporal measures
    if time_series is not None and len(time_series) > 10:
        ts = np.asarray(time_series, dtype=np.float64)

        H_t = time_series_entropy(ts)
        results["temporal_entropy"] = H_t
        print(f"\n  Temporal entropy H(t)     = {H_t:.3f} bits")

        AIS = active_information_storage(ts)
        results["active_info_storage"] = AIS
        print(f"  Active info storage AIS   = {AIS:.3f} bits")

    # Interpretation
    print(f"\n  {'─' * 40}")
    if MI > 0.5 and I > 0:
        print(f"  → Strong spatial structure + emergence")
    elif MI > 0.5:
        print(f"  → Strong spatial structure, weak emergence")
    elif I > 0:
        print(f"  → Weak structure but whole > sum of parts")
    else:
        print(f"  → Low structure, spatially independent")
    print(f"{'═' * 60}\n")

    return results
