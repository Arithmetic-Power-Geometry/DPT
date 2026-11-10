"""Deterministic identifiability and baseline audit on authentic source-derived records.
No outcome prediction, no DPT historical coordinate estimation.
"""
import csv, json
from pathlib import Path
P=Path(__file__).resolve().parent

def read():
    with (P/'records.csv').open(newline='') as f: rows=list(csv.DictReader(f))
    for r in rows:
        for k in ('tokens','steps','tools','errors','revisions','prompt_bytes','claim_bytes'):
            r[k]=int(r[k])
        r['wall_s']=float(r['wall_s'])
        r['signed_prompt_answer_bits']=8*(r['prompt_bytes']-r['claim_bytes'])
    return rows

def dominates(a,b,keys=('tokens','wall_s')):
    return all(a[k]<=b[k] for k in keys) and any(a[k]<b[k] for k in keys)

def evaluate(rows):
    tasks=sorted({r['task'] for r in rows})
    assert len(rows)==9 and len(tasks)==3
    assert all(r['verification_method']=='pending' and not r['verified_outcome'] for r in rows)
    per_task=[]
    for t in tasks:
        subset=[r for r in rows if r['task']==t]
        frontier=[r['model'] for r in subset if not any(dominates(other,r) for other in subset if other is not r)]
        min_tok=min(subset,key=lambda r:r['tokens'])['model']
        min_time=min(subset,key=lambda r:r['wall_s'])['model']
        per_task.append(dict(task=t,models=3,pareto_models=sorted(frontier),minimum_token_model=min_tok,minimum_time_model=min_time))
    return dict(n_records=9,n_tasks=3,n_domains=len({r['domain'] for r in rows}),verified_outcomes=0,
                outcome_based_baseline_comparisons=None,independent_historical_dc=None,independent_historical_qc=None,
                per_task=per_task,
                negative_controls={'whitespace_20_spaces_signed_bit_change':-160,
                                   'pending_as_failure_is_invalid':True,
                                   'task_holdout_folds':3,
                                   'label_permutation_defined':False},
                novelty_gate='not demonstrated: Pareto dominance and rank ordering are standard operations; no independent outcome or coordinate pair')

def main():
    result=evaluate(read())
    (P/'novelty_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
