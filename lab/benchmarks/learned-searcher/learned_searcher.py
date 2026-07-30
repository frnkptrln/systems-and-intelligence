"""Learned-searcher benchmark — pre-registered first contact with the exact floors.

Implements the front page's first near-term frontier item: give a language model
the same partial traces and query budgets as the exact ECA baselines, and score
its answers with the same exact machinery. Three tasks, all scored analytically:

- T1 consistent completion   evidence from one random-ring update of a hidden
                             rule; the model must output a full rule table
                             consistent with the evidence. Truth recovery beyond
                             chance is information-theoretically impossible on
                             uniform worlds (benchmark v1.2); T1 measures
                             consistency and reveals the model's selection prior.
- T2 pairwise witness        two explicit rule tables; the model must construct
                             a width-8 ring that one synchronous update
                             distinguishes, within the analytic minimal cost.
                             Six instances are coverage traps: the pair differs
                             only on neighborhood 111, where every cost-3
                             maximal-coverage row fails (witness benchmark,
                             restricted arm). A coverage heuristic scores ~0
                             on these; difference-set reasoning scores ~1.
- T3 universal witness       a declared class of four rule tables; the model
                             must construct one row whose single update
                             identifies every member, within the exact minimal
                             identification cost.

The instance seed is fixed; prompts, strict final-line parsing, and exhaustive
scoring are locked by a canonical digest. The execution target is registered
separately, so freezing the protocol does not silently choose a model. Outputs
are recorded verbatim with model, source, attempt, response, and usage metadata
to a JSONL file opened in exclusive-create mode. Parse failures and API errors
count as failures. One run per execution registration; no re-rolls.

Providers: ``--provider anthropic`` is currently available through
``lab/providers`` but is refused until an exact target is frozen in
``execution-registration.json``; ``--provider stub`` exercises the pipeline
offline with a constant answer and gains no information about any model.
``--dry-run`` prints the protocol digest, instances, and prompts without calls.
"""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import random
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from itertools import combinations, product
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

WIDTH = 8
COORDS = 8
PROTOCOL_VERSION = "learned-searcher-v0.1"
PROTOCOL_SEED = 0
EXPECTED_PROTOCOL_SHA256 = "5a64f4778a78063627c57c28215974057024793e5d385ee9554f3b5b0bda4963"
EXECUTION_REGISTRATION = HERE / "execution-registration.json"
MAX_ATTEMPTS = 2

SYSTEM_PROMPT = (
    "You are a careful reasoner working on elementary cellular automata. "
    "A rule table maps each 3-bit neighborhood (left, center, right) to one "
    "output bit. Rows are rings of 8 cells updated synchronously: the new "
    "value of cell i is the table entry for (cell i-1, cell i, cell i+1), "
    "with wraparound. Think step by step as needed, then end your reply with "
    "the single final line requested. The final line must match the requested "
    "format exactly."
)


def rule_bit(rule: int, coord: int) -> int:
    return (rule >> coord) & 1


def full_table(rule: int) -> tuple[int, ...]:
    return tuple(rule_bit(rule, coord) for coord in range(COORDS))


def step(table: tuple[int, ...], row: tuple[int, ...]) -> tuple[int, ...]:
    width = len(row)
    return tuple(
        table[(row[(i - 1) % width] << 2) | (row[i] << 1) | row[(i + 1) % width]]
        for i in range(width)
    )


def evidence(rule: int, row: tuple[int, ...]) -> dict[int, int]:
    width = len(row)
    tests = {}
    for i in range(width):
        coord = (
            (row[(i - 1) % width] << 2) | (row[i] << 1) | row[(i + 1) % width]
        )
        tests[coord] = rule_bit(rule, coord)
    return dict(sorted(tests.items()))


def pair_min_cost(a: int, b: int) -> int:
    """Analytic minimal preparation cost separating two rules (witness result)."""
    return min(
        bin(coord).count("1")
        for coord in range(COORDS)
        if rule_bit(a, coord) != rule_bit(b, coord)
    )


def rows_at_cost(width: int, cost: int):
    for ones in combinations(range(width), cost):
        row = [0] * width
        for i in ones:
            row[i] = 1
        yield tuple(row)


def identifies(cls: list[int], row: tuple[int, ...]) -> bool:
    outputs = {step(full_table(rule), row) for rule in cls}
    return len(outputs) == len(cls)


def min_identifying_cost(cls: list[int], width: int = WIDTH) -> int | None:
    for cost in range(width + 1):
        for row in rows_at_cost(width, cost):
            if identifies(cls, row):
                return cost
    return None


# --- Instances (deterministic; this set is the pre-registered protocol) -----

def build_instances(seed: int = 0) -> list[dict]:
    rng = random.Random(f"learned-searcher:{seed}")
    instances = []

    for i in range(40):
        rule = rng.randrange(256)
        row = tuple(rng.getrandbits(1) for _ in range(WIDTH))
        ev = evidence(rule, row)
        instances.append(
            {"task": "T1", "id": f"T1-{i:02d}", "rule": rule, "evidence": ev}
        )

    pairs = []
    while len(pairs) < 34:
        a, b = rng.randrange(256), rng.randrange(256)
        if a != b and (a, b) not in pairs:
            pairs.append((a, b))
    traps = []
    while len(traps) < 6:
        a = rng.randrange(128)
        if (a, a | 128) not in traps:
            traps.append((a, a | 128))  # differ only on neighborhood 111
    for i, (a, b) in enumerate(pairs + traps):
        instances.append(
            {
                "task": "T2",
                "id": f"T2-{i:02d}",
                "a": a,
                "b": b,
                "budget": pair_min_cost(a, b),
                "trap": i >= len(pairs),
            }
        )

    for i in range(20):
        cls = sorted(rng.sample(range(256), 4))
        instances.append(
            {
                "task": "T3",
                "id": f"T3-{i:02d}",
                "cls": cls,
                "budget": min_identifying_cost(cls),
            }
        )
    return instances


# --- Prompts (canonical wording; part of the pre-registration) --------------

def _render_table(rule: int) -> str:
    lines = []
    for coord in range(7, -1, -1):
        l, c, r = (coord >> 2) & 1, (coord >> 1) & 1, coord & 1
        lines.append(f"  ({l},{c},{r}) -> {rule_bit(rule, coord)}")
    return "\n".join(lines)


def render_prompt(inst: dict) -> str:
    if inst["task"] == "T1":
        ev_lines = "\n".join(
            f"  ({(c >> 2) & 1},{(c >> 1) & 1},{c & 1}) -> {out}"
            for c, out in inst["evidence"].items()
        )
        return (
            "A hidden rule table produced these observed neighborhood -> output "
            f"pairs:\n{ev_lines}\n\n"
            "Give one complete rule table consistent with every observation. "
            "End with exactly one line of the form\n"
            "TABLE: t111 t110 t101 t100 t011 t010 t001 t000\n"
            "where each t is the output bit for that neighborhood, written as "
            "eight binary digits separated by spaces."
        )
    if inst["task"] == "T2":
        return (
            "Rule A:\n" + _render_table(inst["a"]) + "\n\n"
            "Rule B:\n" + _render_table(inst["b"]) + "\n\n"
            "Construct one ring of 8 cells such that a single synchronous "
            "update under Rule A differs from a single synchronous update "
            f"under Rule B. Use at most {inst['budget']} ones in the ring. "
            "End with exactly one line of the form\n"
            "ROW: r0 r1 r2 r3 r4 r5 r6 r7\n"
            "as eight binary digits separated by spaces (r0..r7 around the ring)."
        )
    cls_txt = "\n\n".join(
        f"Rule {name}:\n" + _render_table(rule)
        for name, rule in zip("ABCD", inst["cls"])
    )
    return (
        cls_txt + "\n\n"
        "One of these four rules is in effect, but you do not know which. "
        "Construct one ring of 8 cells such that the result of a single "
        "synchronous update is different for every one of the four rules — "
        "one update must identify the rule no matter which it is. "
        f"Use at most {inst['budget']} ones in the ring. "
        "End with exactly one line of the form\n"
        "ROW: r0 r1 r2 r3 r4 r5 r6 r7\n"
        "as eight binary digits separated by spaces (r0..r7 around the ring)."
    )


# --- Parsing and scoring (part of the pre-registration) ---------------------

_FINAL_ANSWER = re.compile(r"^(TABLE|ROW): ([01](?: [01]){7})$")


def parse_answer(text: str, kind: str) -> tuple[int, ...] | None:
    """Accept exactly one eight-bit answer on the final non-empty line."""
    lines = text.splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return None
    match = _FINAL_ANSWER.fullmatch(lines[-1].strip())
    if match is None or match.group(1) != kind:
        return None
    return tuple(int(bit) for bit in match.group(2).split())


def score(inst: dict, bits: tuple[int, ...] | None) -> dict:
    if bits is None:
        return {"parsed": False}
    result: dict = {"parsed": True}
    if inst["task"] == "T1":
        # TABLE line is written t111..t000 -> bits[0] is coordinate 7.
        table = tuple(reversed(bits))
        result["consistent"] = all(
            table[c] == out for c, out in inst["evidence"].items()
        )
        result["truth"] = table == full_table(inst["rule"])
        result["unknown_coords"] = COORDS - len(inst["evidence"])
    elif inst["task"] == "T2":
        cost = sum(bits)
        result["separates"] = step(full_table(inst["a"]), bits) != step(
            full_table(inst["b"]), bits
        )
        result["within_budget"] = cost <= inst["budget"]
        result["cost"] = cost
    else:
        cost = sum(bits)
        result["identifies"] = identifies(inst["cls"], bits)
        result["within_budget"] = cost <= inst["budget"]
        result["cost"] = cost
    return result


# --- Frozen protocol ---------------------------------------------------------

def protocol_manifest() -> dict:
    """Canonical task, prompt, parser, and exhaustive score manifest."""
    instances = build_instances(PROTOCOL_SEED)
    items = []
    all_answers = tuple(product((0, 1), repeat=COORDS))
    for inst in instances:
        items.append(
            {
                "instance": inst,
                "prompt": render_prompt(inst),
                "answer_kind": "TABLE" if inst["task"] == "T1" else "ROW",
                "scores": [
                    {"answer": bits, "score": score(inst, bits)}
                    for bits in all_answers
                ],
            }
        )
    return {
        "version": PROTOCOL_VERSION,
        "seed": PROTOCOL_SEED,
        "width": WIDTH,
        "system_prompt": SYSTEM_PROMPT,
        "final_answer_pattern": _FINAL_ANSWER.pattern,
        "final_answer_policy": (
            "last non-empty line; surrounding whitespace ignored; exact kind, "
            "colon, and eight space-separated bits required"
        ),
        "parser_source": inspect.getsource(parse_answer),
        "provider_call_attempts_per_instance": MAX_ATTEMPTS,
        "items": items,
    }


def protocol_sha256() -> str:
    payload = json.dumps(
        protocol_manifest(), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_execution_registration(protocol_digest: str) -> dict:
    registration = json.loads(EXECUTION_REGISTRATION.read_text(encoding="utf-8"))
    if registration.get("protocol_sha256") != protocol_digest:
        raise RuntimeError(
            "Execution registration does not match the frozen protocol digest."
        )
    return registration


# --- Providers ---------------------------------------------------------------

class StubProvider:
    """Offline pipeline test; constant answers, no information about any model."""

    name = "stub"
    model = "constant-zero-v1"
    last_usage = None

    def complete(self, prompt: str, system: str | None = None) -> str:
        kind = "TABLE" if "TABLE:" in prompt else "ROW"
        return f"{kind}: 0 0 0 0 0 0 0 0"


def make_provider(name: str, model: str | None = None):
    if name == "stub":
        return StubProvider()
    if not model:
        raise ValueError("A frozen exact model identifier is required.")
    sys.path.insert(0, str(REPO))
    from lab.providers.anthropic_provider import AnthropicProvider

    return AnthropicProvider(model=model)


def provider_identity(provider) -> dict:
    return {
        "provider": provider.name,
        "model": getattr(provider, "model", None),
    }


def complete_with_retry(provider, prompt: str) -> tuple[str, list[dict]]:
    """Make at most two recorded attempts after provider-call errors."""
    attempts = []
    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        started = time.perf_counter()
        try:
            reply = provider.complete(prompt, system=SYSTEM_PROMPT)
            attempts.append(
                {
                    "attempt": attempt,
                    "ok": True,
                    "latency_seconds": round(time.perf_counter() - started, 6),
                    "usage": getattr(provider, "last_usage", None),
                    "stop_reason": getattr(provider, "last_stop_reason", None),
                    "request_id": getattr(provider, "last_request_id", None),
                }
            )
            return reply, attempts
        except Exception as error:
            last_error = error
            attempts.append(
                {
                    "attempt": attempt,
                    "ok": False,
                    "error_type": type(error).__name__,
                    "error": str(error),
                    "latency_seconds": round(time.perf_counter() - started, 6),
                    "usage": getattr(provider, "last_usage", None),
                    "stop_reason": getattr(provider, "last_stop_reason", None),
                    "request_id": getattr(provider, "last_request_id", None),
                }
            )
    return (
        f"[PROVIDER ERROR] {type(last_error).__name__}: {last_error}",
        attempts,
    )


def git_provenance() -> dict:
    """Capture the exact source state used for a real run."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=REPO,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "dirty": None}
    return {"commit": commit, "dirty": dirty}


# --- Runner ------------------------------------------------------------------

def summarize(records: list[dict]) -> str:
    lines = []
    for task in ("T1", "T2", "T3"):
        rows = [r for r in records if r["task"] == task]
        n = len(rows)
        parsed = [r for r in rows if r["score"].get("parsed")]
        lines.append(f"{task}: n={n} parsed={len(parsed)}")
        if task == "T1":
            ok = sum(1 for r in parsed if r["score"]["consistent"])
            truth = sum(1 for r in parsed if r["score"]["truth"])
            chance = sum(
                2.0 ** -(COORDS - len(r["instance"]["evidence"]))
                for r in rows
            )
            lines.append(
                f"    consistent {ok}/{n}   truth {truth}/{n} "
                f"(chance expectation {chance:.1f})"
            )
        elif task == "T2":
            for label, subset in (
                ("random", [r for r in rows if not r["instance"]["trap"]]),
                ("trap  ", [r for r in rows if r["instance"]["trap"]]),
            ):
                sep = sum(
                    1
                    for r in subset
                    if r["score"].get("parsed") and r["score"]["separates"]
                )
                opt = sum(
                    1
                    for r in subset
                    if r["score"].get("parsed")
                    and r["score"]["separates"]
                    and r["score"]["within_budget"]
                )
                lines.append(
                    f"    {label} separates {sep}/{len(subset)}   "
                    f"cost-optimal {opt}/{len(subset)}"
                )
        else:
            ident = sum(
                1 for r in parsed if r["score"]["identifies"]
            )
            opt = sum(
                1
                for r in parsed
                if r["score"]["identifies"] and r["score"]["within_budget"]
            )
            lines.append(f"    identifies {ident}/{n}   cost-optimal {opt}/{n}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("anthropic", "stub"), default="stub")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()

    digest = protocol_sha256()
    if digest != EXPECTED_PROTOCOL_SHA256:
        raise RuntimeError(
            "Frozen protocol digest changed. Review the change and register a "
            "new digest before any execution."
        )

    instances = build_instances(PROTOCOL_SEED)
    if args.dry_run:
        counts = {}
        for inst in instances:
            counts[inst["task"]] = counts.get(inst["task"], 0) + 1
        print(
            f"protocol: {PROTOCOL_VERSION} sha256={digest}\n"
            f"instances: {counts}  (total {len(instances)}; "
            f"up to {len(instances) * MAX_ATTEMPTS} provider calls after retries)"
        )
        for task in ("T1", "T2", "T3"):
            first = next(i for i in instances if i["task"] == task)
            print(f"\n--- first {task} prompt ({first['id']}) ---")
            print(render_prompt(first))
        return

    registration = load_execution_registration(digest)
    if args.provider == "stub":
        if not args.out:
            parser.error("--out is required for stub runs.")
        model = StubProvider.model
    else:
        if args.out:
            parser.error(
                "Real runs always use the canonical results.jsonl path; "
                "--out is available only for stub runs."
            )
        if registration.get("status") != "frozen":
            parser.error(
                "No real execution is registered. Freeze provider, exact model, "
                "and maintainer prediction in execution-registration.json first."
            )
        if registration.get("provider") != args.provider:
            parser.error("CLI provider does not match the frozen registration.")
        model = registration.get("model")
        if not model:
            parser.error("The frozen registration has no exact model identifier.")
        if registration.get("maintainer_prediction") is None:
            parser.error(
                "The frozen registration must record or explicitly waive the "
                "maintainer prediction."
            )

    output = Path(args.out) if args.provider == "stub" else HERE / "results.jsonl"
    provenance = git_provenance()
    if args.provider != "stub" and (
        provenance["commit"] is None or provenance["dirty"] is not False
    ):
        parser.error("Real runs require a clean, committed git worktree.")

    provider = make_provider(args.provider, model)
    identity = provider_identity(provider)
    records = []
    try:
        sink = output.open("x", encoding="utf-8")
    except FileExistsError:
        parser.error(f"Refusing to overwrite existing result file: {output}")

    with sink:
        run_record = {
            "record_type": "run",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "protocol_version": PROTOCOL_VERSION,
            "protocol_sha256": digest,
            "protocol_seed": PROTOCOL_SEED,
            "execution_registration": registration,
            "provider": identity,
            "git": provenance,
            "python": sys.version,
        }
        sink.write(json.dumps(run_record) + "\n")
        for inst in instances:
            prompt = render_prompt(inst)
            reply, attempts = complete_with_retry(provider, prompt)
            kind = "TABLE" if inst["task"] == "T1" else "ROW"
            bits = parse_answer(reply, kind)
            record = {
                "record_type": "result",
                "task": inst["task"],
                "id": inst["id"],
                "instance": inst,
                "protocol_sha256": digest,
                "provider": identity,
                "attempts": attempts,
                "usage": getattr(provider, "last_usage", None),
                "response_metadata": {
                    "stop_reason": getattr(provider, "last_stop_reason", None),
                    "request_id": getattr(provider, "last_request_id", None),
                },
                "reply_characters": len(reply),
                "reply": reply,
                "score": score(inst, bits),
            }
            records.append(record)
            sink.write(json.dumps(record) + "\n")

    print(
        f"LEARNED-SEARCHER RUN  provider={identity['provider']} "
        f"model={identity['model']}  protocol={digest}"
    )
    print(summarize(records))
    print(f"\nverbatim record: {output}")


if __name__ == "__main__":
    main()
