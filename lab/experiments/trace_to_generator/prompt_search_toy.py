"""Toy inverse-prompt search scaffold (backend-free)."""

from evaluator import score_output


def mock_generate(prompt: str) -> str:
    # Stub runtime: replace with real model call when available.
    return f"Generated trace for prompt: {prompt}"


def mutate_prompt(prompt: str) -> list[str]:
    return [prompt, prompt + "\nBe concise.", prompt + "\nUse explicit runtime assumptions."]


def run_search(seed_prompts: list[str], must_include: list[str], steps: int = 2) -> tuple[str, float]:
    best_prompt = ""
    best_score = -1.0
    frontier = seed_prompts
    for _ in range(steps):
        next_frontier = []
        for p in frontier:
            out = mock_generate(p)
            s = score_output(out, must_include)
            if s > best_score:
                best_prompt, best_score = p, s
            next_frontier.extend(mutate_prompt(p))
        frontier = next_frontier
    return best_prompt, best_score


if __name__ == "__main__":
    seed = ["Explain emergence and runtime coupling."]
    target_tokens = ["trace", "generator", "runtime"]
    prompt, score = run_search(seed, target_tokens)
    print("Best prompt:", prompt)
    print("Score:", round(score, 3))
