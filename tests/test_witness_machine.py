"""Exact controls and boundary tests for the target-free Witness Machine slice."""
from dataclasses import replace
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "lab/experiments/witness_machine/witness_machine.py"
spec = importlib.util.spec_from_file_location("witness_machine", SOURCE)
wm = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = wm
spec.loader.exec_module(wm)


@pytest.mark.parametrize("cost,remaining", [(0,128),(1,16),(2,8),(3,2),(4,1)])
def test_original_full_family_frontier(cost, remaining):
    problem = wm.ProblemSpec(tuple(range(256)), cost_limit=cost, world_cost_budget=cost)
    proposal = wm.propose(problem, "exhaustive")
    old = wm.wb.best_query_at_cost(width=8, cost=cost)
    assert tuple(proposal["query"]) == old.row
    predictions = {r:tuple(o) for r,o in proposal["predictions"]}
    assert wm.score(problem, proposal["query"], predictions)[0] == remaining
    assert proposal["construction_calls"] == len(list(problem.queries())) * 256
    assert proposal["enumeration_complete"]


@pytest.mark.parametrize("candidates", [(0,128),(0,64,128,192)])
def test_known_traps_and_equal_objective_referee(candidates):
    problem = wm.ProblemSpec(candidates)
    proposal = wm.propose(problem, "exhaustive")
    assert proposal["query"] == [0,0,0,0,0,1,1,1]
    receipt = wm.WorldReferee(problem, candidates[-1]).evaluate(proposal)
    assert receipt["status"] == "identified"
    assert receipt["regret"]["optimal"]
    assert receipt["world_cost_spent"] == 3
    assert receipt["world_queries_spent"] == 1
    assert "target_rule" not in json.dumps(receipt)


def test_unreachable_is_certified_only_by_referee_frontier():
    problem = wm.ProblemSpec((0,128), cost_limit=2, world_cost_budget=2, proposal_call_budget=2)
    proposal = wm.propose(problem, "budgeted")
    assert not proposal["enumeration_complete"]
    assert proposal["stop_reason"] == "proposal_budget_exhausted"
    receipt = wm.WorldReferee(problem, 128).evaluate(proposal)
    assert receipt["status"] == "unresolved"
    assert not receipt["frontier"]["informative_query_exists"]
    assert not receipt["frontier"]["identification_possible"]
    assert receipt["frontier"]["legal_queries"] == 28
    assert receipt["construction_calls_reported"] == 2
    assert receipt["referee_candidate_calls"] == 58


def test_budget_abstention_does_not_consume_world():
    problem = wm.ProblemSpec((0,128), proposal_call_budget=1)
    proposal = wm.propose(problem)
    assert proposal["query"] is None
    result = wm.WorldReferee(problem, 128).evaluate(proposal)
    assert result["status"] == "abstained"
    assert result["world_queries_spent"] == 0
    assert result["frontier"]["identification_possible"]


def test_zero_cost_still_consumes_a_world_query():
    problem = wm.ProblemSpec((0,1), cost_limit=0, world_cost_budget=0)
    proposal = wm.propose(problem)
    referee = wm.WorldReferee(problem, 1)
    result = referee.evaluate(proposal)
    assert result["status"] == "identified"
    assert result["world_cost_spent"] == 0
    assert result["world_queries_spent"] == 1
    with pytest.raises(ValueError, match="world budget"):
        referee.evaluate(proposal)


def test_receipt_freezes_proposal_and_simulator_enforces_declared_access():
    problem = wm.ProblemSpec((0,128))
    proposal = wm.propose(problem,"exhaustive")
    receipt = wm.WorldReferee(problem,128).evaluate(proposal)
    proposal['query'][0] = 1
    assert receipt['proposal_sha256'] == wm.digest(receipt['proposal'])
    oracle = wm.CandidateOracle(problem,100)
    with pytest.raises(ValueError,match='declared'):
        oracle.predict((30,),(0,)*8)
    assert oracle.calls == 0


def test_at_most_uses_cheapest_tied_query():
    problem = wm.ProblemSpec((0,1), cost_mode="at-most", cost_limit=3)
    proposal = wm.propose(problem, "exhaustive")
    assert proposal["query"] == [0]*8
    assert proposal["declared_cost"] == 0
    assert wm.WorldReferee(problem, 0).evaluate(proposal)["regret"]["optimal"]


def test_geometry_matches_independent_string_update():
    problem = wm.ProblemSpec((0,30,90,128,255), width=5, baseline=(1,0,1,0,1), writable=(1,3), observed=(4,1), steps=2, cost_limit=2, cost_mode="at-most")
    proposal = wm.propose(problem, "exhaustive")
    assert proposal["examined_queries"] == 4
    for query in problem.queries():
        assert all(query[i] == problem.baseline[i] for i in (0,2,4))
        for rule in problem.candidates:
            state=''.join(map(str,query))
            for _ in range(2):
                state=''.join(str((rule >> int(state[(i-1)%5]+state[i]+state[(i+1)%5],2)) & 1) for i in range(5))
            assert wm.simulate(problem,rule,query) == tuple(int(state[i]) for i in (4,1))


def test_empty_observation_map_cannot_distinguish():
    problem = wm.ProblemSpec((0,128), observed=())
    result = wm.WorldReferee(problem, 128).evaluate(wm.propose(problem, "exhaustive"))
    assert result["outcome"] == []
    assert result["survivors"] == [0,128]
    assert not result["frontier"]["informative_query_exists"]


def test_prior_filter_is_charged_and_conditioned():
    evidence = wm.Observation((0,)*8,(0,)*8)
    problem = wm.ProblemSpec((0,1,128), observations=(evidence,), proposal_call_budget=5)
    proposal = wm.propose(problem)
    assert proposal["construction_calls"] == 5  # three old predictions, two new
    assert [r for r,_ in proposal["predictions"]] == [0,128]
    assert wm.WorldReferee(problem,128).evaluate(proposal)["prior_survivors"] == [0,128]
    with pytest.raises(ValueError, match="contradicts"):
        wm.WorldReferee(problem,1)


def test_family_failure_is_not_identification():
    problem = wm.ProblemSpec((0,128), cost_limit=0, world_cost_budget=0)
    receipt = wm.WorldReferee(problem,1).evaluate(wm.propose(problem))
    assert receipt["status"] == "family_failure"
    assert receipt["survivors"] == []
    missing = replace(problem, observations=(wm.Observation((0,)*8,(1,)*8),))
    result = wm.WorldReferee(missing,1).evaluate(wm.propose(missing))
    assert result["status"] == "family_failure"
    assert result["world_queries_spent"] == 0
    assert result["frontier"] is None


def test_positive_prior_weights_are_conditioned_exactly():
    problem = wm.ProblemSpec((0,1,128), prior_weights=(1,7,2), cost_limit=0)
    predictions = {0:(0,),1:(1,),128:(0,)}
    assert wm.score(problem,(0,)*8,predictions) == (2,Fraction(13,10),0)


@pytest.mark.parametrize("field,value", [("declared_cost",0),("declared_cost",True),("predictions",[]),("partition",[]),("problem_sha256","bad"),("construction_calls",100001)])
def test_forged_proposal_rejected_before_world_call(field,value):
    problem = wm.ProblemSpec((0,128))
    proposal = wm.propose(problem,"exhaustive");proposal[field]=value
    referee = wm.WorldReferee(problem,128)
    with pytest.raises(ValueError):
        referee.evaluate(proposal)
    assert referee.spent_queries == 0


def test_illegal_query_and_world_budget_are_separate():
    problem = wm.ProblemSpec((0,128), world_cost_budget=2)
    proposal = wm.propose(problem,"exhaustive")
    with pytest.raises(ValueError, match="world budget"):
        wm.WorldReferee(problem,128).evaluate(proposal)
    proposal["query"] = [False]*8
    with pytest.raises(ValueError, match="query"):
        wm.WorldReferee(problem,128).evaluate(proposal)


@pytest.mark.parametrize("change", [{"candidates":(0,0)},{"candidates":(False,1)},{"observed":(8,)},{"writable":(1,1)},{"cost_limit":True},{"prior_weights":(0,1)},{"objective":"IG"},{"width":13}])
def test_invalid_problem_is_rejected(change):
    with pytest.raises(ValueError):
        wm.ProblemSpec(**({"candidates":(0,128)}|change))


def test_cli_handoff_is_target_independent_and_no_overwrite(tmp_path):
    problem = wm.ProblemSpec((0,128))
    public = tmp_path/'problem.json'; public.write_text(json.dumps(problem.to_dict()))
    proposal = tmp_path/'proposal.json'
    command = [sys.executable,str(SOURCE),'propose','--spec',str(public),'--out',str(proposal),'--strategy','exhaustive']
    subprocess.run(command,check=True,capture_output=True)
    original = proposal.read_bytes()
    assert subprocess.run(command,capture_output=True).returncode == 2
    assert proposal.read_bytes() == original
    for target in (0,128):
        sealed = tmp_path/f'target-{target}.json'; sealed.write_text(json.dumps({"rule":target}))
        output = tmp_path/f'receipt-{target}.json'
        subprocess.run([sys.executable,str(SOURCE),'referee','--spec',str(public),'--proposal',str(proposal),'--target',str(sealed),'--out',str(output)],check=True,capture_output=True)
        receipt = json.loads(output.read_text())
        assert receipt['survivors'] == [target]
        assert receipt['proposal_sha256'] == wm.digest(json.loads(original))
    assert proposal.read_bytes() == original
    assert 'target' not in public.read_text()
