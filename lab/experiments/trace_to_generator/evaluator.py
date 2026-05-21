"""Lightweight evaluator scaffold for trace->generator toy search."""

def score_output(text: str, must_include: list[str]) -> float:
    if not text:
        return 0.0
    hits = sum(1 for token in must_include if token.lower() in text.lower())
    return hits / max(len(must_include), 1)
