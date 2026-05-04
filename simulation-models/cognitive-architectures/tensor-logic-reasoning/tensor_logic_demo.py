#!/usr/bin/env python3
"""
tensor_logic_demo.py

Small demonstration script inspired by Pedro Domingos' "Tensor Logic":
- Facts (Parent)
- Rule (Ancestor)
- Logical inference
- Embeddings & reasoning in embedding space

Part of the "systems-and-intelligence" repository under:
simulation-models/tensor-logic-reasoning/
"""

import numpy as np


# ---------------------------------------------------------
# 1. Entities & Parent Relation
# ---------------------------------------------------------

def build_entities():
    """
    Creates a mapping from names to integer indices.
    """
    entities = ["Alice", "Bob", "Charlie", "David"]
    name_to_idx = {name: i for i, name in enumerate(entities)}
    return entities, name_to_idx


def build_parent_matrix(name_to_idx):
    """
    Creates a Parent adjacency matrix P[x, y],
    where P[i, j] = 1 means: Parent(entity_i, entity_j).
    """
    n = len(name_to_idx)
    P = np.zeros((n, n), dtype=np.float32)

    parent_pairs = [
        ("Alice", "Bob"),
        ("Bob", "Charlie"),
        ("Charlie", "David"),
    ]

    for p, c in parent_pairs:
        i = name_to_idx[p]
        j = name_to_idx[c]
        P[i, j] = 1.0

    return P


# ---------------------------------------------------------
# 2. Logical Inference: Ancestor as Transitive Closure
# ---------------------------------------------------------

def compute_ancestor_closure(parent_matrix):
    """
    Computes Ancestor[x, z] as the transitive closure of Parent.

    Ancestor(x, z) is true if there is a chain of Parent edges
    from x to z (including direct Parent relationships).
    """
    n = parent_matrix.shape[0]
    ancestor = parent_matrix.copy()

    # Transitive closure: repeated path extension
    for _ in range(n):
        new_paths = ancestor @ parent_matrix
        new_paths = (new_paths > 0).astype(np.float32)
        ancestor = np.maximum(ancestor, new_paths)

    return ancestor



def print_relation_matrix(matrix, entities, title):
    """
    Nicely formatted matrix table:
    - Column width dynamically adjusted to longest name
    - Uniform spacing
    - Clean horizontal lines
    """
    print(f"\n{title}")

    # Dynamically determine longest name
    max_name_len = max(len(name) for name in entities)
    col_width = max(max_name_len, 7) + 2  # +2 for spacing

    # Line width
    total_width = col_width + len(entities) * col_width + 3
    print("-" * total_width)

    # Header
    header = " " * col_width + "| " + "".join(
        f"{name:>{col_width}}" for name in entities
    )
    print(header)
    print("-" * total_width)

    # Rows
    for i, row_name in enumerate(entities):
        row = f"{row_name:<{col_width}}| " + "".join(
            f"{int(matrix[i, j] > 0.5):>{col_width}}"
            for j in range(len(entities))
        )
        print(row)

    print("-" * total_width)

# ---------------------------------------------------------
# 3. Embeddings & Relation Tensor
# ---------------------------------------------------------

def build_embeddings(name_to_idx, dim=16, seed=42):
    """
    Creates random, normalized embeddings Emb[x, d]
    for each entity.
    """
    rng = np.random.default_rng(seed)
    n = len(name_to_idx)
    emb = rng.normal(0.0, 1.0, size=(n, dim)).astype(np.float32)

    # Normalize to unit vectors
    norms = np.linalg.norm(emb, axis=1, keepdims=True) + 1e-8
    emb = emb / norms
    return emb


def build_relation_tensor_parent(parent_matrix, emb):
    """
    EmbParent[i, j] = Sum_{(x,y) in Parent} Emb[x,i] * Emb[y,j]

    This is the construction from Domingos' paper:
    superposition of tensor products of argument embeddings.
    """
    n, dim = emb.shape
    R = np.zeros((dim, dim), dtype=np.float32)

    for x in range(n):
        for y in range(n):
            if parent_matrix[x, y] > 0.5:
                R += np.outer(emb[x], emb[y])

    return R


def compute_score_baseline(emb, R):
    """
    Computes a baseline score over all (a,b) pairs.
    This baseline is subtracted later so that the
    sigmoid output is better centered around 0.5.
    """
    n = emb.shape[0]
    scores = []
    for i in range(n):
        for j in range(n):
            va = emb[i]
            vb = emb[j]
            s = np.einsum("i,ij,j->", va, R, vb)
            scores.append(s)
    return float(np.mean(scores))


# ---------------------------------------------------------
# 4. Reasoning in Embedding Space
# ---------------------------------------------------------

def logistic(x):
    return 1.0 / (1.0 + np.exp(-x))


def query_parent_logical(parent_matrix, name_to_idx, a, b):
    """
    Logical truth of Parent(a,b) based on the matrix.
    """
    i = name_to_idx[a]
    j = name_to_idx[b]
    return int(parent_matrix[i, j] > 0.5)


def query_parent_embedding(emb, R, name_to_idx, a, b,
                           temperature=1.0, baseline=None):
    """
    Reasoning in embedding space following Domingos:

    Score(a,b) = Emb[a]^T * R * Emb[b]

    With optional baseline centering and temperature T:
    p = sigmoid((score - baseline) / T)
    """
    i = name_to_idx[a]
    j = name_to_idx[b]

    va = emb[i]  # [dim]
    vb = emb[j]  # [dim]

    score = np.einsum("i,ij,j->", va, R, vb)

    if baseline is not None:
        score_centered = score - baseline
    else:
        score_centered = score

    p = logistic(score_centered / max(temperature, 1e-8))
    return float(score), float(p), float(score_centered)


# ---------------------------------------------------------
# 5. Demo
# ---------------------------------------------------------

def main():
    entities, name_to_idx = build_entities()
    P = build_parent_matrix(name_to_idx)
    A = compute_ancestor_closure(P)

    print_relation_matrix(P, entities, "Parent Relation (logical)")
    print_relation_matrix(A, entities, "Ancestor Relation (logical, transitive)")

    # Embeddings + relation tensor
    emb = build_embeddings(name_to_idx, dim=16, seed=42)
    R_parent = build_relation_tensor_parent(P, emb)
    baseline = compute_score_baseline(emb, R_parent)

    print("\nBaseline score (over all pairs): {:.4f}".format(baseline))

    print("\nEmbedding-based Parent Queries")
    print("=".ljust(47, "="))

    test_pairs = [
        ("Alice", "Bob"),      # true
        ("Bob", "Charlie"),    # true
        ("Alice", "Charlie"),  # Ancestor only
        ("Alice", "David"),    # Ancestor
        ("Bob", "David"),      # Ancestor
        ("Charlie", "Alice"),  # false
    ]

    for a, b in test_pairs:
        logical_val = query_parent_logical(P, name_to_idx, a, b)

        score_tight, p_tight, centered_tight = query_parent_embedding(
            emb, R_parent, name_to_idx, a, b,
            temperature=0.1, baseline=baseline
        )
        score_soft, p_soft, centered_soft = query_parent_embedding(
            emb, R_parent, name_to_idx, a, b,
            temperature=1.0, baseline=baseline
        )

        print("\n-----------------------------------------------")
        print(f"Query: Parent({a}, {b})")
        print(f"  Logical:           {logical_val}")
        print(f"  Score (raw):       {score_soft:.4f}")
        print(f"  Score (centered):  {centered_soft:.4f}")
        print(f"  p(T=0.1):          {p_tight:.3f}")
        print(f"  p(T=1.0):          {p_soft:.3f}")

    print("\n-----------------------------------------------")
    print("Note:")
    print(" - The logical view uses only the binary Parent matrix.")
    print(" - Embeddings + relation tensor produce soft scores.")
    print(" - Baseline centering brings typical pairs near p≈0.5.")
    print(" - Temperature T controls how 'strictly logical' vs. analog the interpretation is.")


if __name__ == "__main__":
    main()
