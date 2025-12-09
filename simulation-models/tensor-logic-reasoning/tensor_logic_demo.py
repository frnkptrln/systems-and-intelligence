#!/usr/bin/env python3
"""
tensor_logic_demo.py

Kleines Demonstrationsscript inspiriert von Pedro Domingos' "Tensor Logic":
- Fakten (Parent)
- Regel (Ancestor)
- logische Inferenz
- Embeddings & Reasoning im Embedding-Space

Einbettbar in das Repo "systems-and-intelligence" unter:
simulation-models/tensor-logic-reasoning/
"""

import numpy as np


# ---------------------------------------------------------
# 1. Entities & Parent-Relation
# ---------------------------------------------------------

def build_entities():
    """
    Erzeugt ein Mapping von Namen auf Integer-Indizes.
    """
    entities = ["Alice", "Bob", "Charlie", "David"]
    name_to_idx = {name: i for i, name in enumerate(entities)}
    return entities, name_to_idx


def build_parent_matrix(name_to_idx):
    """
    Erzeugt eine Parent-Adjazenzmatrix P[x, y],
    wobei P[i, j] = 1 bedeutet: Parent(entity_i, entity_j).
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
# 2. Logische Inferenz: Ancestor als transitiver Abschluss
# ---------------------------------------------------------

def compute_ancestor_closure(parent_matrix):
    """
    Berechnet Ancestor[x, z] als transitiven Abschluss von Parent.

    Ancestor(x, z) ist wahr, wenn es eine Kette von Parent-Kanten
    von x nach z gibt (inklusive direkter Parent-Beziehung).
    """
    n = parent_matrix.shape[0]
    ancestor = parent_matrix.copy()

    # Transitiver Abschluss: wiederholt Pfadverlängerung
    for _ in range(n):
        new_paths = ancestor @ parent_matrix
        new_paths = (new_paths > 0).astype(np.float32)
        ancestor = np.maximum(ancestor, new_paths)

    return ancestor



def print_relation_matrix(matrix, entities, title):
    """
    Schön formatierte Matrix-Tabelle:
    - Spaltenbreite wird dynamisch an längsten Namen angepasst
    - Einheitliche Abstände
    - Saubere horizontale Linien
    """
    print(f"\n{title}")

    # Dynamisch längster Name
    max_name_len = max(len(name) for name in entities)
    col_width = max(max_name_len, 7) + 2  # +2 für Abstand

    # Linienbreite
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
# 3. Embeddings & Relationstensor
# ---------------------------------------------------------

def build_embeddings(name_to_idx, dim=16, seed=42):
    """
    Erzeugt zufällige, normierte Embeddings Emb[x, d]
    für jede Entität.
    """
    rng = np.random.default_rng(seed)
    n = len(name_to_idx)
    emb = rng.normal(0.0, 1.0, size=(n, dim)).astype(np.float32)

    # Normierung auf Einheitsvektoren
    norms = np.linalg.norm(emb, axis=1, keepdims=True) + 1e-8
    emb = emb / norms
    return emb


def build_relation_tensor_parent(parent_matrix, emb):
    """
    EmbParent[i, j] = Sum_{(x,y) in Parent} Emb[x,i] * Emb[y,j]

    Das ist die Konstruktion aus Domingos' Paper:
    Superposition der Tensor-Produkte der Argument-Embeddings.
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
    Berechnet einen Baseline-Score über alle (a,b)-Paare.
    Diese Baseline ziehen wir später ab, damit der
    Sigmoid-Output besser um 0.5 herum zentriert ist.
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
# 4. Reasoning im Embedding-Space
# ---------------------------------------------------------

def logistic(x):
    return 1.0 / (1.0 + np.exp(-x))


def query_parent_logical(parent_matrix, name_to_idx, a, b):
    """
    Logische Wahrheit von Parent(a,b) anhand der Matrix.
    """
    i = name_to_idx[a]
    j = name_to_idx[b]
    return int(parent_matrix[i, j] > 0.5)


def query_parent_embedding(emb, R, name_to_idx, a, b,
                           temperature=1.0, baseline=None):
    """
    Reasoning im Embedding-Space nach Domingos:

    Score(a,b) = Emb[a]^T * R * Emb[b]

    Mit optionaler Baseline-Zentrierung und Temperatur T:
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

    print_relation_matrix(P, entities, "Parent-Relation (logisch)")
    print_relation_matrix(A, entities, "Ancestor-Relation (logisch, transitiv)")

    # Embeddings + Relationstensor
    emb = build_embeddings(name_to_idx, dim=16, seed=42)
    R_parent = build_relation_tensor_parent(P, emb)
    baseline = compute_score_baseline(emb, R_parent)

    print("\nBaseline-Score (über alle Paare): {:.4f}".format(baseline))

    print("\nEmbedding-basierte Parent-Queries")
    print("=".ljust(47, "="))

    test_pairs = [
        ("Alice", "Bob"),      # wahr
        ("Bob", "Charlie"),    # wahr
        ("Alice", "Charlie"),  # nur Ancestor
        ("Alice", "David"),    # Ancestor
        ("Bob", "David"),      # Ancestor
        ("Charlie", "Alice"),  # falsch
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
        print(f"  Logisch:           {logical_val}")
        print(f"  Score (roh):       {score_soft:.4f}")
        print(f"  Score (zentriert): {centered_soft:.4f}")
        print(f"  p(T=0.1):          {p_tight:.3f}")
        print(f"  p(T=1.0):          {p_soft:.3f}")

    print("\n-----------------------------------------------")
    print("Hinweis:")
    print(" - Die logische Sicht nutzt nur die binäre Parent-Matrix.")
    print(" - Embeddings + Relationstensor erzeugen weiche Scores.")
    print(" - Die Baseline-Zentrierung bringt typische Paare in die Nähe von p≈0.5.")
    print(" - Die Temperatur T steuert, wie 'streng logisch' vs. analog die Interpretation ist.")


if __name__ == "__main__":
    main()
