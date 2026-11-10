#!/usr/bin/env python3
"""Reproducible, seed-clustered diagnostics for the deterministic generated-question proxy benchmark.
Not historical DC/QC validation; proxy rubric ratings may be mechanically dependent.
"""
import csv,io,json,zipfile,sys,hashlib
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr

SEED=20261110
FIELDS=['question_id','problem_id','field','condition_id','DC_normalized','QC_normalized','novelty_proxy','usefulness_proxy','feasibility_proxy','regionIV','frontier_candidate']

def load(path):
 with zipfile.ZipFile(path) as z:
  names=[n for n in z.namelist() if n.endswith('/data/question_coordinates_proxy_1000.csv')]
  assert len(names)==1
  data=z.read(names[0]); rows=list(csv.DictReader(io.StringIO(data.decode('utf-8-sig'))))
 return rows,hashlib.sha256(data).hexdigest()

def rho(a,b): return float(spearmanr(a,b).statistic)

def run(path):
 rows,digest=load(path)
 assert len(rows)==1000
 ids=[r['question_id'] for r in rows];assert len(set(ids))==1000
 groups=sorted(set(r['problem_id'] for r in rows));assert len(groups)==100
 for g in groups: assert sum(r['problem_id']==g for r in rows)==10
 for k in ('DC_normalized','QC_normalized','novelty_proxy','usefulness_proxy','feasibility_proxy'):
  assert all(np.isfinite(float(r[k])) for r in rows)
 rng=np.random.default_rng(SEED)
 dc=np.array([float(r['DC_normalized']) for r in rows]);qc=np.array([float(r['QC_normalized']) for r in rows]);nov=np.array([float(r['novelty_proxy']) for r in rows]);use=np.array([float(r['usefulness_proxy']) for r in rows]);fea=np.array([float(r['feasibility_proxy']) for r in rows]);grp=np.array([r['problem_id'] for r in rows]);field=np.array([r['field'] for r in rows]);cond=np.array([r['condition_id'] for r in rows]);
 idxs={g:np.where(grp==g)[0] for g in groups}
 pairs={'DC_vs_novelty':(dc,nov),'QC_vs_usefulness':(qc,use),'DC_vs_feasibility':(dc,fea),'QC_vs_novelty':(qc,nov),'DC_vs_QC':(dc,qc)}
 result={'scope':'deterministic proxy score diagnostics only; no independently measured discovery coordinates','source_sha256':digest,'n_questions':len(rows),'n_seed_clusters':len(groups),'n_conditions':len(set(cond)),'fields':{f:int(np.sum(field==f)) for f in sorted(set(field))},'seed':SEED,'cluster_bootstrap_draws':1200,'within_seed_permutation_draws':1200,'pairs':{},'negative_controls':{},'condition_descriptives':{}}
 B=1200
 # Cluster bootstrap is used to avoid treating 10 generated questions per seed as independent.
 bootidx=[np.concatenate([idxs[g] for g in rng.choice(groups,size=len(groups),replace=True)]) for _ in range(B)]
 for label,(x,y) in pairs.items():
  observed=rho(x,y)
  bs=np.array([rho(x[i],y[i]) for i in bootidx]);bs=bs[np.isfinite(bs)]
  # Within-seed permutation preserves seed effects; only within-problem alignment is broken.
  perms=[]
  for _ in range(B):
   yperm=y.copy()
   for g in groups: yperm[idxs[g]]=y[rng.permutation(idxs[g])]
   perms.append(rho(x,yperm))
  perms=np.array(perms)
  # Residualized by seed mean (descriptive, not causal adjustment).
  xc=np.array([x[i]-x[idxs[grp[i]]].mean() for i in range(len(x))]);yc=np.array([y[i]-y[idxs[grp[i]]].mean() for i in range(len(y))])
  result['pairs'][label]={'rho':observed,'cluster_bootstrap_95pct':[float(np.quantile(bs,.025)),float(np.quantile(bs,.975))],'within_seed_centered_rho':rho(xc,yc),'within_seed_permutation_null_95pct':[float(np.quantile(perms,.025)),float(np.quantile(perms,.975))],'within_seed_permutation_p_centered_on_null':float((1+np.sum(np.abs(perms-np.mean(perms))>=abs(observed-np.mean(perms))))/(B+1))}
 # mechanically linked scores? exact deterministic mean from rubric
 cost_cols=['C_time','C_concept','C_search','C_experiment','C_compute','C_coordination'];qcols=['QC_description','QC_graph','QC_scope','QC_parsimony']
 cost=np.array([[float(r[k]) for k in cost_cols] for r in rows]); q=np.array([[float(r[k]) for k in qcols] for r in rows]);
 result['score_formula_checks']={'max_abs_dc_residual':float(np.max(np.abs(dc-cost.mean(axis=1)/4))),'max_abs_qc_residual':float(np.max(np.abs(qc-q.mean(axis=1)/4)))}
 result['negative_controls']['shuffle_novelty_across_seed_clusters']='see within_seed_permutation_null for DC_vs_novelty';result['negative_controls']['shuffle_usefulness_across_seed_clusters']='see within_seed_permutation_null for QC_vs_usefulness'
 for c in sorted(set(cond)):
  ii=np.where(cond==c)[0]
  result['condition_descriptives'][c]={'n':len(ii),'mean_dc_proxy':float(np.mean(dc[ii])),'mean_qc_proxy':float(np.mean(qc[ii])),'mean_novelty_proxy':float(np.mean(nov[ii])),'mean_usefulness_proxy':float(np.mean(use[ii]))}
 result['regionIV_count']=sum(r['regionIV']=='1' for r in rows)
 result['frontier_candidates']=sum(r['frontier_candidate'].strip().lower()=='true' for r in rows)
 return result
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python proxy_validation.py QuestionBenchmark.zip')
 out=run(sys.argv[1]);Path('P07_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['n_questions','n_seed_clusters','regionIV_count','frontier_candidates','pairs','score_formula_checks']},indent=2))
