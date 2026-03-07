"""
Observer Attribution Model
----------------------------
A lightweight simulated observer that reads an agent's outputs and computes
an 'intentionality score' — modeling how a human would attribute purpose
and identity to the agent based on external behavior alone.

intentionality_score = f(TF-IDF similarity across outputs, entropy of topic distribution)
  - Low entropy + high similarity → high intentionality attribution
  - High entropy + low similarity → low intentionality attribution
"""

import numpy as np
from collections import Counter
import math


def _compute_tf(words: list[str]) -> dict[str, float]:
    """Term frequency for a single document."""
    counts = Counter(words)
    total = len(words)
    if total == 0:
        return {}
    return {w: c / total for w, c in counts.items()}


def _compute_idf(documents: list[list[str]]) -> dict[str, float]:
    """Inverse document frequency across all documents."""
    n_docs = len(documents)
    if n_docs == 0:
        return {}

    doc_freq: dict[str, int] = {}
    for doc in documents:
        unique_words = set(doc)
        for w in unique_words:
            doc_freq[w] = doc_freq.get(w, 0) + 1

    return {w: math.log(n_docs / (1 + df)) for w, df in doc_freq.items()}


def tfidf_similarity(outputs: list[str]) -> float:
    """
    Compute average pairwise cosine similarity of TF-IDF vectors
    across agent outputs.

    High similarity = the agent consistently talks about the same things
                      (appears intentional to an observer).
    """
    # Tokenize
    documents = [o.lower().split() for o in outputs]
    if len(documents) < 2:
        return 0.0

    idf = _compute_idf(documents)
    all_words = sorted(idf.keys())
    word_to_idx = {w: i for i, w in enumerate(all_words)}

    # Build TF-IDF vectors
    vectors = []
    for doc in documents:
        tf = _compute_tf(doc)
        vec = np.zeros(len(all_words))
        for w, freq in tf.items():
            if w in word_to_idx:
                vec[word_to_idx[w]] = freq * idf.get(w, 0)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm
        vectors.append(vec)

    # Average pairwise cosine similarity
    sims = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            sims.append(float(np.dot(vectors[i], vectors[j])))

    return float(np.mean(sims)) if sims else 0.0


def topic_entropy(outputs: list[str], top_n: int = 20) -> float:
    """
    Compute Shannon entropy of the topic distribution across outputs.

    Low entropy = focused, consistent topics (appears purposeful).
    High entropy = scattered, random topics (appears aimless).
    """
    # Simple topic model: word frequency distribution
    all_words = []
    for o in outputs:
        words = [w for w in o.lower().split() if len(w) > 4]
        all_words.extend(words)

    if not all_words:
        return 0.0

    counts = Counter(all_words)
    top_words = counts.most_common(top_n)
    total = sum(c for _, c in top_words)

    if total == 0:
        return 0.0

    entropy = 0.0
    for _, count in top_words:
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)

    # Normalize by max possible entropy
    max_entropy = math.log2(min(top_n, len(top_words)))
    if max_entropy > 0:
        return entropy / max_entropy
    return 0.0


def intentionality_score(outputs: list[str]) -> float:
    """
    Compute the observer's attribution of intentionality.

    Score in [0, 1]:
      1.0 = "This agent clearly has a purpose and identity"
      0.0 = "This agent is random noise"
    """
    if len(outputs) < 2:
        return 0.0

    sim = tfidf_similarity(outputs)
    ent = topic_entropy(outputs)

    # High similarity + low entropy = high intentionality
    # Formula: weighted combination
    score = 0.6 * sim + 0.4 * (1.0 - ent)
    return float(np.clip(score, 0.0, 1.0))
