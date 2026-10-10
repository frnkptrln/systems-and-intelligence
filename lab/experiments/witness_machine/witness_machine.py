"""Target-free experiment construction and a separately invoked exact ECA referee.

This is an executable interface, not a trained witness generator. All candidate
simulation calls made by the built-in proposer are counted, including filtering
prior evidence. The referee's exhaustive audit is reported separately.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parents[1] / "benchmarks/witness-generation/witness_benchmark.py"
_module = importlib.util.spec_from_file_location("witness_machine_exact_baseline", BASELINE)
wb = importlib.util.module_from_spec(_module)
sys.modules[_module.name] = wb
_module.loader.exec_module(wb)
PROTOCOL = "witness-machine-interface-v0.1"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def integer(value, name, minimum=0, maximum=None):
    if type(value) is not int or value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"invalid {name}")


def row(value, width, name):
    if not isinstance(value, (list, tuple)) or len(value) != width or any(type(b) is not int or b not in (0, 1) for b in value):
        raise ValueError(f"invalid {name}")
    return tuple(value)


@dataclass(frozen=True)
class Observation:
    query: tuple[int, ...]
    outcome: tuple[int, ...]


@dataclass(frozen=True)
class ProblemSpec:
    candidates: tuple[int, ...]
    width: int = 8
    baseline: tuple[int, ...] = (0,) * 8
    writable: tuple[int, ...] = tuple(range(8))
    observed: tuple[int, ...] = tuple(range(8))
    steps: int = 1
    cost_limit: int = 3
    cost_mode: str = "exact"
    proposal_call_budget: int = 100000
    world_cost_budget: int = 3
    world_query_budget: int = 1
    observations: tuple[Observation, ...] = ()
    prior_weights: tuple[int, ...] = ()
    objective: str = "minimax-residual"

    def __post_init__(self):
        integer(self.width, "width", 3, 12)
        integer(self.steps, "steps", 1, 4)
        candidates = tuple(self.candidates)
        if not candidates or len(set(candidates)) != len(candidates):
            raise ValueError("candidate family must be nonempty and unique")
        for rule in candidates:
            integer(rule, "ECA rule", 0, 255)
        object.__setattr__(self, "candidates", candidates)
        object.__setattr__(self, "baseline", row(self.baseline, self.width, "baseline"))
        for name in ("writable", "observed"):
            values = tuple(getattr(self, name))
            if len(set(values)) != len(values):
                raise ValueError(f"duplicate {name} positions")
            for index in values:
                integer(index, name, 0, self.width - 1)
            object.__setattr__(self, name, values)
        for name in ("cost_limit", "proposal_call_budget", "world_cost_budget", "world_query_budget"):
            integer(getattr(self, name), name)
        if self.cost_limit > len(self.writable) or self.cost_mode not in ("exact", "at-most"):
            raise ValueError("invalid query-cost convention")
        if self.objective != "minimax-residual":
            raise ValueError("only the declared minimax-residual objective is implemented")
        weights = tuple(self.prior_weights) or (1,) * len(candidates)
        if len(weights) != len(candidates):
            raise ValueError("one positive integer prior weight per candidate required")
        for weight in weights:
            integer(weight, "prior weight", 1)
        object.__setattr__(self, "prior_weights", weights)
        observations = tuple(self.observations)
        for evidence in observations:
            if not isinstance(evidence, Observation):
                raise ValueError("observations must be Observation records")
            self.validate_query(evidence.query, enforce_cost=False)
            row(evidence.outcome, len(self.observed), "observed outcome")
        object.__setattr__(self, "observations", tuple(Observation(tuple(e.query), tuple(e.outcome)) for e in observations))

    @classmethod
    def from_dict(cls, data):
        data = dict(data)
        if data.pop("protocol", None) != PROTOCOL:
            raise ValueError("wrong problem protocol")
        data["observations"] = tuple(Observation(**e) for e in data.get("observations", []))
        return cls(**data)

    def to_dict(self):
        return {"protocol": PROTOCOL, **asdict(self)}

    def cost(self, query):
        return sum(a != b for a, b in zip(query, self.baseline))

    def validate_query(self, query, enforce_cost=True):
        query = row(query, self.width, "query")
        if any(query[i] != self.baseline[i] for i in range(self.width) if i not in self.writable):
            raise ValueError("query changes a locked cell")
        cost = self.cost(query)
        if enforce_cost and (cost > self.cost_limit or self.cost_mode == "exact" and cost != self.cost_limit):
            raise ValueError("query violates declared cost convention")
        return query

    def queries(self):
        for values in product((0, 1), repeat=len(self.writable)):
            query = list(self.baseline)
            for index, value in zip(self.writable, values):
                query[index] = value
            cost = self.cost(query)
            if cost == self.cost_limit or self.cost_mode == "at-most" and cost < self.cost_limit:
                yield tuple(query)


def simulate(spec, rule, query):
    state = tuple(query)
    for _ in range(spec.steps):
        state = wb.step(rule, state)
    return tuple(state[i] for i in spec.observed)


class BudgetExhausted(Exception):
    pass


class CandidateOracle:
    """Only declared candidates. No hidden-target argument or global world RNG."""

    def __init__(self, spec, limit=None):
        self.spec, self.limit, self.calls = spec, limit, 0

    def predict(self, candidates, query):
        candidates = tuple(candidates)
        if len(set(candidates)) != len(candidates) or any(type(r) is not int or r not in self.spec.candidates for r in candidates):
            raise ValueError("simulator access is restricted to declared candidates")
        query = self.spec.validate_query(query, enforce_cost=False)
        if self.limit is not None and self.calls + len(candidates) > self.limit:
            raise BudgetExhausted("candidate simulation budget exhausted")
        self.calls += len(candidates)
        return {rule: simulate(self.spec, rule, query) for rule in candidates}

    def consistent_candidates(self):
        candidates = self.spec.candidates
        for evidence in self.spec.observations:
            outcomes = self.predict(candidates, evidence.query)
            candidates = tuple(rule for rule in candidates if outcomes[rule] == evidence.outcome)
        return candidates


def partition(predictions):
    blocks = defaultdict(list)
    for rule, outcome in predictions.items():
        blocks[tuple(outcome)].append(rule)
    return tuple(sorted(tuple(sorted(block)) for block in blocks.values()))


def score(spec, query, predictions):
    blocks = partition(predictions)
    if not blocks:
        raise ValueError("cannot score an empty candidate family")
    weights = dict(zip(spec.candidates, spec.prior_weights))
    total = sum(weights[rule] for rule in predictions)
    expected = sum(Fraction(sum(weights[r] for r in block) * len(block), total) for block in blocks)
    return (max(map(len, blocks)), expected, spec.cost(query))


def score_json(value):
    return {"worst_case_remaining": value[0], "expected_remaining": str(value[1]), "cost": value[2]}


def propose(spec, strategy="budgeted", seed=0):
    if strategy not in ("random", "budgeted", "exhaustive"):
        raise ValueError("unknown strategy")
    oracle = CandidateOracle(spec, spec.proposal_call_budget)
    best = None
    examined = 0
    complete = False
    reason = None
    try:
        candidates = oracle.consistent_candidates()
        if not candidates:
            reason = "family_failure_in_prior_evidence"
        else:
            queries = sorted(spec.queries())
            if strategy != "exhaustive":
                random.Random(seed).shuffle(queries)
            if strategy == "random":
                queries = queries[:1]
            for query in queries:
                predictions = oracle.predict(candidates, query)
                examined += 1
                value = score(spec, query, predictions)
                if best is None or (value, query) < (best[0], best[1]):
                    best = (value, query, predictions)
            complete = strategy != "random" or len(list(spec.queries())) == 1
    except BudgetExhausted:
        reason = "proposal_budget_exhausted"
    return {"protocol": PROTOCOL, "problem_sha256": digest(spec.to_dict()),
            "strategy": strategy, "seed": seed, "query": list(best[1]) if best else None,
            "predictions": [[r, list(o)] for r, o in sorted(best[2].items())] if best else [],
            "partition": [list(b) for b in partition(best[2])] if best else [],
            "declared_cost": best[0][2] if best else None,
            "construction_calls": oracle.calls, "examined_queries": examined,
            "enumeration_complete": complete, "stop_reason": reason}


def exact_frontier(spec, candidates, oracle):
    best = None
    count = 0
    for query in sorted(spec.queries()):
        value = score(spec, query, oracle.predict(candidates, query))
        count += 1
        if best is None or (value, query) < best:
            best = (value, query)
    return best, count


def regret(value, optimum):
    for name, actual, best in zip(("worst_case_remaining", "expected_remaining", "cost"), value, optimum):
        if actual != best:
            return {"optimal": False, "first_worse_component": name, "gap": str(actual - best)}
    return {"optimal": True, "first_worse_component": None, "gap": "0"}


class WorldReferee:
    """Episode budgets are enforced here. Separate CLI processes are the handoff.

    This Python object is not a security sandbox against a hostile same-user
    process. The target file must be isolated by the caller for a blind study.
    """

    def __init__(self, spec, target_rule):
        integer(target_rule, "target rule", 0, 255)
        self.spec, self._target = spec, target_rule
        self.spent_cost, self.spent_queries = 0, 0
        if any(simulate(spec, target_rule, e.query) != e.outcome for e in spec.observations):
            raise ValueError("sealed target contradicts the supplied prior observations")

    def evaluate(self, proposal):
        proposal = json.loads(canonical(proposal))
        spec = self.spec
        if proposal.get("protocol") != PROTOCOL or proposal.get("problem_sha256") != digest(spec.to_dict()):
            raise ValueError("proposal belongs to a different problem")
        calls = proposal.get("construction_calls")
        integer(calls, "reported construction calls", 0, spec.proposal_call_budget)
        integer(proposal.get("examined_queries"), "examined queries")
        audit = CandidateOracle(spec)
        candidates = audit.consistent_candidates()
        receipt = {"protocol": PROTOCOL, "problem_sha256": digest(spec.to_dict()),
                   "proposal_sha256": digest(proposal), "proposal": proposal,
                   "construction_calls_reported": calls, "construction_independently_attested": False,
                   "prior_survivors": list(candidates), "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   "baseline_sha256": hashlib.sha256(BASELINE.read_bytes()).hexdigest()}
        if not candidates:
            if proposal.get("query") is not None:
                raise ValueError("cannot propose from an empty candidate family")
            receipt.update(status="family_failure", outcome=None, survivors=[], frontier=None)
        else:
            optimum, count = exact_frontier(spec, candidates, audit)
            receipt["frontier"] = {"best_query": list(optimum[1]), "best_score": score_json(optimum[0]),
                                   "legal_queries": count, "identification_possible": optimum[0][0] == 1,
                                   "informative_query_exists": optimum[0][0] < len(candidates)}
            if proposal.get("query") is None:
                if proposal.get("predictions") or proposal.get("partition") or proposal.get("declared_cost") is not None:
                    raise ValueError("abstention cannot contain a prediction or cost")
                receipt.update(status="abstained", outcome=None, survivors=list(candidates), regret=None)
            else:
                query = spec.validate_query(proposal["query"])
                cost = spec.cost(query)
                if type(proposal.get("declared_cost")) is not int or proposal["declared_cost"] != cost:
                    raise ValueError("misreported query cost")
                predictions = audit.predict(candidates, query)
                # Canonical byte comparison is type-strict (True is not 1).
                expected = [[r, list(o)] for r, o in sorted(predictions.items())]
                if canonical(proposal.get("predictions")) != canonical(expected):
                    raise ValueError("candidate predictions failed independent verification")
                if canonical(proposal.get("partition")) != canonical([list(b) for b in partition(predictions)]):
                    raise ValueError("declared partition failed independent verification")
                if self.spent_queries >= spec.world_query_budget or self.spent_cost + cost > spec.world_cost_budget:
                    raise ValueError("world budget exhausted")
                self.spent_queries += 1
                self.spent_cost += cost
                observed = simulate(spec, self._target, query)
                survivors = [r for r in candidates if predictions[r] == observed]
                value = score(spec, query, predictions)
                receipt.update(status="family_failure" if not survivors else "identified" if len(survivors) == 1 else "unresolved",
                               outcome=list(observed), survivors=survivors, score=score_json(value),
                               regret=regret(value, optimum[0]),
                               next_observation={"query": list(query), "outcome": list(observed)})
        receipt.update(referee_candidate_calls=audit.calls, world_queries_spent=self.spent_queries,
                       world_cost_spent=self.spent_cost)
        return receipt


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_new(path, value):
    # Never replace a frozen proposal, fixture, or prior receipt.
    with Path(path).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("propose", "referee"):
        command = commands.add_parser(name)
        command.add_argument("--spec", type=Path, required=True)
        command.add_argument("--out", type=Path, required=True)
        if name == "propose":
            command.add_argument("--strategy", choices=("random", "budgeted", "exhaustive"), default="budgeted")
            command.add_argument("--seed", type=int, default=0)
        else:
            command.add_argument("--proposal", type=Path, required=True)
            command.add_argument("--target", type=Path, required=True)
    args = parser.parse_args()
    try:
        spec = ProblemSpec.from_dict(load(args.spec))
        if args.command == "propose":
            result = propose(spec, args.strategy, args.seed)
        else:
            target = load(args.target)
            if set(target) != {"rule"}:
                raise ValueError("target file must contain only rule")
            result = WorldReferee(spec, target["rule"]).evaluate(load(args.proposal))
        write_new(args.out, result)
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.exit(2, f"witness-machine: {exc}\n")
    print(args.out)


if __name__ == "__main__":
    main()
