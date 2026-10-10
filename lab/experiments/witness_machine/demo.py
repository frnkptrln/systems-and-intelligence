"""Run open, model-free controls with proposer/referee in separate processes."""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys

from witness_machine import ProblemSpec, Observation, write_new


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).with_name('witness_machine.py')
    pair = ProblemSpec((0,128))
    cases = [
        ('pair', pair, 128),
        ('pair-budget-two', replace(pair,cost_limit=2,world_cost_budget=2),128),
        ('four',replace(pair,candidates=(0,64,128,192),prior_weights=(1,1,1,1)),192),
        ('full-family',replace(pair,candidates=tuple(range(256)),prior_weights=(1,)*256,cost_limit=4,world_cost_budget=4),110),
        ('masked',replace(pair,observed=()),128),
        ('zero-cost',replace(pair,candidates=(0,1),cost_limit=0,world_cost_budget=0),1),
        ('family-failure',replace(pair,cost_limit=0,world_cost_budget=0),1),
        ('prior-family-failure',replace(pair,observations=(Observation((0,)*8,(1,)*8),)),1),
        ('limited-compute',replace(pair,proposal_call_budget=2),128),
        ('shifted-access',ProblemSpec((0,30,90,128,255),width=5,baseline=(1,0,1,0,1),writable=(1,3),observed=(4,1),steps=2,cost_mode='at-most',cost_limit=2),90),
    ]
    summaries = []
    for name,spec,target in cases:
        folder = output/name;folder.mkdir()
        public,sealed = folder/'problem.json',folder/'open-demo-target.json'
        write_new(public,spec.to_dict());write_new(sealed,{'rule':target})
        for strategy in ('random','budgeted','exhaustive'):
            proposal,receipt = folder/f'{strategy}-proposal.json',folder/f'{strategy}-receipt.json'
            subprocess.run([sys.executable,str(source),'propose','--spec',str(public),'--out',str(proposal),'--strategy',strategy],check=True,capture_output=True)
            subprocess.run([sys.executable,str(source),'referee','--spec',str(public),'--proposal',str(proposal),'--target',str(sealed),'--out',str(receipt)],check=True,capture_output=True)
            result = json.loads(receipt.read_text())
            summaries.append({'case':name,'strategy':strategy,'status':result['status'],
                              'score':result.get('score'),'regret':result.get('regret'),
                              'construction_calls':result['construction_calls_reported'],
                              'referee_calls':result['referee_candidate_calls'],
                              'world_queries':result['world_queries_spent']})
    report = {'kind':'open-deterministic-controls','trained_model':False,'blind_evaluation':False,
              'source_sha256':result['source_sha256'],'baseline_sha256':result['baseline_sha256'],
              'runs':summaries}
    write_new(output/'summary.json',report)
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    run(parser.parse_args().output)
