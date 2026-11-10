"""Deterministic, source-attributed *task resolution* experiment.

Outcomes are benchmark agreement diagnostics, NOT independent discovery events;
measured path effort is NOT historical DPT discovery complexity. The frozen
before/after task-state length is NOT historical Question Compression.
"""
from __future__ import annotations
import csv
import hashlib
import json
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from rdkit import Chem, rdBase
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors, FilterCatalog

ROOT=Path(__file__).resolve().parent
PAINS_PARAMS=FilterCatalog.FilterCatalogParams()
PAINS_PARAMS.AddCatalog(FilterCatalog.FilterCatalogParams.FilterCatalogs.PAINS)
PAINS=FilterCatalog.FilterCatalog(PAINS_PARAMS)

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',',':'), ensure_ascii=False)

def sha(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()

def resolve(task, audit=None):
    """Run a frozen task with optional timestamped RDKit-call auditing."""
    def call(name,fn,*args):
        started=datetime.now(timezone.utc).isoformat()
        ns=time.perf_counter_ns()
        value=fn(*args)
        duration=time.perf_counter_ns()-ns
        if audit is not None:audit.append({'operation':name,'started_utc':started,'elapsed_ns':duration})
        return value
    mol=call('MolFromSmiles',Chem.MolFromSmiles,task['smiles'])
    if mol is None:raise ValueError('Invalid frozen SMILES: '+task['task_id'])
    op=task['operation']
    if op=='mw_logp_hbd':
        return {'MW':round(call('MolWt',Descriptors.MolWt,mol),2),'RDKit_LogP':round(call('MolLogP',Crippen.MolLogP,mol),3),'HBD':call('CalcNumHBD',rdMolDescriptors.CalcNumHBD,mol)}
    if op=='smiles_tpsa':
        return {'canonical_SMILES':call('MolToSmiles',Chem.MolToSmiles,mol),'TPSA':round(call('CalcTPSA',rdMolDescriptors.CalcTPSA,mol),2)}
    if op=='lipinski':
        vals={'MW':round(call('MolWt',Descriptors.MolWt,mol),2),'RDKit_LogP':round(call('MolLogP',Crippen.MolLogP,mol),3),'HBD':call('CalcNumHBD',rdMolDescriptors.CalcNumHBD,mol),'HBA':call('CalcNumHBA',rdMolDescriptors.CalcNumHBA,mol)}
        return {**vals,'passes_all_thresholds':vals['MW']<500 and vals['RDKit_LogP']<5 and vals['HBD']<=5 and vals['HBA']<=10}
    if op=='pains':
        n=len(call('PAINS_GetMatches',PAINS.GetMatches,mol))
        return {'PAINS_alert_count':n,'passes_PAINS':n==0}
    if op=='rot_formula':
        return {'rotatable_bonds':call('CalcNumRotatableBonds',rdMolDescriptors.CalcNumRotatableBonds,mol),'formula':call('CalcMolFormula',rdMolDescriptors.CalcMolFormula,mol)}
    if op=='aromatic_rings':return {'aromatic_rings':call('CalcNumAromaticRings',rdMolDescriptors.CalcNumAromaticRings,mol)}
    raise ValueError('Unsupported operation '+op)

def independent_benchmark_agreement(t,out):
    """Sealed benchmark target is read ONLY here, after resolve returned."""
    t_id=t['task_id']
    if t_id=='dd_e01':
        return {'status':'partial','exact_match':False,'checks':{'MW':abs(out['MW']-180.16)<=0.02,'HBD':out['HBD']==1,'LogP_exact':abs(out['RDKit_LogP']-1.24)<=0.01},'reason':'LogP is method-dependent; RDKit differs from benchmark point target'}
    if t_id=='dd_e02':
        benchmark_smiles='CC(C)Cc1ccc(cc1)C(C)C(=O)O'
        same=Chem.MolToSmiles(Chem.MolFromSmiles(benchmark_smiles))==out['canonical_SMILES']
        return {'status':'pass' if same and abs(out['TPSA']-37.3)<=0.05 else 'fail','exact_match':bool(same and abs(out['TPSA']-37.3)<=0.05),'checks':{'graph_equivalence':same,'TPSA':abs(out['TPSA']-37.3)<=0.05}}
    if t_id=='dd_e03':
        return {'status':'partial','exact_match':False,'checks':{'pass_thresholds':out['passes_all_thresholds'],'MW':abs(out['MW']-129.16)<=0.02,'HBD_numeric':out['HBD']==2,'HBA_numeric':out['HBA']==4},'reason':'Benchmark HBD/HBA (2/4) conflict with RDKit and PubChem (3/1)'}
    if t_id=='dd_e07':return {'status':'pass' if out['PAINS_alert_count']==0 else 'fail','exact_match':out['PAINS_alert_count']==0,'checks':{'PAINS_zero':out['PAINS_alert_count']==0}}
    if t_id=='dd_e08':
        ok=out['rotatable_bonds']==12 and out['formula']=='C33H35FN2O5'
        return {'status':'pass' if ok else 'fail','exact_match':ok,'checks':{'rotatable_bonds':out['rotatable_bonds']==12,'formula':out['formula']=='C33H35FN2O5'}}
    if t_id=='dd_e10':
        return {'status':'mismatch','exact_match':False,'checks':{'aromatic_rings':out['aromatic_rings']==4},'reason':'Benchmark claims four; RDKit structure-based ring count is three'}
    raise ValueError('No sealed validator for '+t_id)

def run(n_repeats=30):
    tasks=json.loads((ROOT/'frozen_tasks.json').read_text())['tasks']
    traces=[];summaries=[];all_output={}
    for task in tasks:
        before={'molecule':task['smiles'],'question_id':task['task_id'],'property_request':task['operation'],'measurements':None}
        effort=[];outs=[]
        for run_index in range(n_repeats):
            started=datetime.now(timezone.utc).isoformat()
            audited_calls=[];s=time.perf_counter_ns();out=resolve(task,audited_calls);elapsed_ns=time.perf_counter_ns()-s
            completed=datetime.now(timezone.utc).isoformat()
            effort.append(elapsed_ns);outs.append(out)
            traces.append({'task_id':task['task_id'],'repetition':run_index,'started_utc':started,'completed_utc':completed,'elapsed_ns':elapsed_ns,'rdkit_operation_calls':len(audited_calls),'rdkit_operations':audited_calls,'input_state_sha256':sha(canonical(before)),'output_sha256':sha(canonical(out))})
        assert all(o==outs[0] for o in outs)
        out=outs[0];all_output[task['task_id']]=out
        after={**before,'measurements':out}
        bb=len(canonical(before).encode());ab=len(canonical(after).encode())
        agreement=independent_benchmark_agreement(task,out)
        summaries.append({'task_id':task['task_id'],'operation':task['operation'],'rdkit_calls':len(audited_calls),'outcome_status':agreement['status'],'strict_target_match':agreement['exact_match'],'elapsed_median_ms':statistics.median(effort)/1e6,'elapsed_p05_ms':sorted(effort)[round(0.05*(len(effort)-1))]/1e6,'elapsed_p95_ms':sorted(effort)[round(0.95*(len(effort)-1))]/1e6,'state_before_bytes':bb,'state_after_bytes':ab,'signed_change_bits':8*(bb-ab),'state_before_sha256':sha(canonical(before)),'state_after_sha256':sha(canonical(after)),'result_sha256':sha(canonical(out)),'verification_details':canonical(agreement)})
    assert len(summaries)==6 and len(traces)==6*n_repeats
    with (ROOT/'execution_traces.jsonl').open('w') as f:
        for tr in traces:f.write(canonical(tr)+'\n')
    with (ROOT/'summary.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(summaries[0]));w.writeheader();w.writerows(summaries)
    report={'schema':'dpt-prospective-rdkit-v1','python':platform.python_version(),'rdkit_version':rdBase.rdkitVersion,'n_tasks':len(tasks),'n_repetitions_each':n_repeats,'n_traces':len(traces),'outcomes':{s['task_id']:s['outcome_status'] for s in summaries},'strict_target_matches':sum(int(s['strict_target_match']) for s in summaries),'outputs':all_output,'limitations':['Tasks are solutions of prewritten questions, not question discovery','Operating-time quantiles measure execution jitter, not scientific population variation','Frozen task-state signed length differences are not DPT QC','RDKit descriptor implementation and benchmark targets may differ','Benchmark answer labels are not independently adjudicated historical discovery outcomes']}
    (ROOT/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
if __name__=='__main__':print(json.dumps(run(),indent=2))
