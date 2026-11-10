"""Reproducible descriptive audit of upstream OpenDiscoveryTrace GitHub samples.
The CSV stores source-extracted fields with upstream blob IDs; no outcomes imputed.
"""
import csv, json, itertools, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def load():
    with (ROOT/'records.csv').open(newline='') as f: r=list(csv.DictReader(f))
    for x in r:
        for k in ('tokens','steps','tools','errors','revisions','prompt_bytes','claim_bytes'):x[k]=int(x[k])
        x['wall_s']=float(x['wall_s']);x['signed_prompt_answer_bits']=8*(x['prompt_bytes']-x['claim_bytes'])
    return r

def evaluate():
    r=load();tasks=sorted({x['task'] for x in r});models=sorted({x['model'] for x in r})
    assert len(r)==9 and len(tasks)==3 and len(models)==3
    assert all(x['verification_method']=='pending' and x['verified_outcome']=='' for x in r)
    assert all(len([x for x in r if x['task']==t])==3 for t in tasks)
    # Task-level grouped holdout feasibility: no verified label in train OR test.
    folds=[{'held_out_task':t,'train_n':sum(x['task']!=t for x in r),'test_n':sum(x['task']==t for x in r),'verified_train_n':0,'verified_test_n':0,'predictive_metric':None} for t in tasks]
    model_ranges={m:{k:[min(x[k] for x in r if x['model']==m),max(x[k] for x in r if x['model']==m)] for k in ('tokens','wall_s','signed_prompt_answer_bits')} for m in models}
    task_ranges={t:{k:[min(x[k] for x in r if x['task']==t),max(x[k] for x in r if x['task']==t)] for k in ('tokens','wall_s','signed_prompt_answer_bits')} for t in tasks}
    # Exact sign count for token and time pairwise contrasts (descriptive, no inferential claims).
    pairwise=[]
    for a,b in itertools.combinations(models,2):
        token_diff=[next(x['tokens'] for x in r if x['task']==t and x['model']==a)-next(x['tokens'] for x in r if x['task']==t and x['model']==b) for t in tasks]
        time_diff=[round(next(x['wall_s'] for x in r if x['task']==t and x['model']==a)-next(x['wall_s'] for x in r if x['task']==t and x['model']==b),2) for t in tasks]
        pairwise.append({'a':a,'b':b,'token_differences_by_task':token_diff,'wall_time_differences_by_task_s':time_diff})
    # Task-block permutation negative control: no outcome labels -> predictive permutation undefined.
    negative_controls={'whitespace_20_spaces_raw_length_shift_bits':-160,'outcome_permutation_test':None,'reason':'No independently verified outcome labels; permutation inference undefined','task_label_permutations':6,'task_permutations_not_valid_as_outcome_test':True}
    # MDL would require a specified model class, likelihood and code lengths.
    return {'n_trajectories':len(r),'n_tasks':len(tasks),'n_domains':1,'n_models':len(models),'verified_outcomes':0,'identified_historical_dc':0,'identified_historical_qc':0,'tasks':tasks,'models':models,'folds':folds,'model_ranges':model_ranges,'task_ranges':task_ranges,'paired_descriptive_contrasts':pairwise,'negative_controls':negative_controls,'comparisons':{'cost_only':'descriptive only','description_length_only':'descriptive only','search':'step count is an incomplete proxy','pareto':'descriptive dominance possible, but no outcome predictive test','genuine_MDL':'not computable: no fixed model family, likelihood and universal code','DPT_operational_two_coordinate':'not defined: prompt/answer length is not QC'},'uncertainty':'Observed ranges only; 3 tasks are insufficient for reliable population intervals','conclusion':'No external predictive construct validity can be estimated'}

if __name__=='__main__':
    o=evaluate();(ROOT/'results.json').write_text(json.dumps(o,indent=2)+'\n');print(json.dumps(o,indent=2))
