"""Held-out grouped seed-level diagnostics of deterministic rubric proxies, not external validity or actual MDL."""
import csv, io, json, zipfile, sys
import numpy as np
from scipy.stats import spearmanr
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error

def run(archive, seed=20261110, permutations=80):
 with zipfile.ZipFile(archive) as z:
  n=next(x for x in z.namelist() if x.endswith('/data/question_coordinates_proxy_1000.csv'))
  r=list(csv.DictReader(io.StringIO(z.read(n).decode('utf-8-sig'))))
 assert len(r)==1000
 col=lambda s:np.array([float(v[s]) for v in r])
 dc,qc=col('DC_normalized'),col('QC_normalized')
 # Length of observed generated question is only a text-length proxy, NOT MDL.
 length=np.array([len(v['normalized_question'].encode('utf-8')) for v in r],dtype=float)
 # Pareto rank: dominance in the two observed rubric coordinates, descriptive, not a new independent metric.
 # Nonnegative min-max normalized coordinates; cost lower and compression higher.
 rank=np.array([np.sum((dc<=dc[i]) & (qc>=qc[i]) & ((dc<dc[i]) | (qc>qc[i]))) for i in range(len(r))],float)
 groups=np.array([v['problem_id'] for v in r]); folds=list(GroupKFold(5).split(dc,groups=groups))
 xdict={'intercept':np.zeros((len(r),1)),'cost_only':dc[:,None], 'compression_only':qc[:,None], 'two_coordinates':np.column_stack([dc,qc]), 'two_plus_interaction':np.column_stack([dc,qc,dc*qc]),'text_length_proxy':length[:,None], 'pareto_dominance_count':rank[:,None], 'two_plus_length':np.column_stack([dc,qc,length])}
 rng=np.random.default_rng(seed)
 results={'scope':'generated-question deterministic rubric proxy evaluation; NOT historical DC/QC or MDL','n':len(r),'seed_groups':len(set(groups)),'folds':5,'permutations':permutations,'seed':seed,'models':{},'negative_controls':{}}
 for outcome in ['novelty_proxy','usefulness_proxy','feasibility_proxy']:
  y=col(outcome); results['models'][outcome]={}
  predictions={}
  for name,x in xdict.items():
   pred=np.empty(len(y))
   for train,test in folds:
    if name=='intercept': pred[test]=np.mean(y[train])
    else: pred[test]=make_pipeline(StandardScaler(),Ridge(alpha=10)).fit(x[train],y[train]).predict(x[test])
   predictions[name]=pred
   results['models'][outcome][name]={'rmse':float(np.sqrt(mean_squared_error(y,pred))),'spearman_pred_outcome':float(spearmanr(y,pred).statistic)}
  # Group bootstrap paired delta for two coordinates vs cost-only (positive means improvement).
  seeds=sorted(set(groups)); idx={g:np.where(groups==g)[0] for g in seeds}; deltas=[]
  for _ in range(600):
   ii=np.concatenate([idx[g] for g in rng.choice(seeds,size=len(seeds),replace=True)])
   a=np.mean((y[ii]-predictions['cost_only'][ii])**2)
   b=np.mean((y[ii]-predictions['two_coordinates'][ii])**2)
   deltas.append(np.sqrt(a)-np.sqrt(b))
  results['models'][outcome]['two_vs_cost_delta_rmse']={'observed':results['models'][outcome]['cost_only']['rmse']-results['models'][outcome]['two_coordinates']['rmse'],'cluster95':np.quantile(deltas,[.025,.975]).tolist()}
  # Shuffle outcome across entire seed clusters (preserves within-seed vectors, breaks seed-predictor alignment).
  null=[]; ys=np.array([y[idx[g]] for g in seeds]); assert ys.shape==(100,10)
  for _ in range(permutations):
   shuffled=ys[rng.permutation(len(seeds))]; yp=y.copy()
   for g,values in zip(seeds,shuffled):yp[idx[g]]=values
   pred=np.empty(len(y))
   x=xdict['two_coordinates']
   for train,test in folds:pred[test]=make_pipeline(StandardScaler(),Ridge(alpha=10)).fit(x[train],yp[train]).predict(x[test])
   null.append(float(np.sqrt(mean_squared_error(yp,pred))))
  results['negative_controls'][outcome]={'seed_permutation_rmse_95':np.quantile(null,[.025,.975]).tolist(),'observed_two_coord_rmse':results['models'][outcome]['two_coordinates']['rmse']}
 return results
if __name__=='__main__':
 res=run(sys.argv[1]);open('P08_results.json','w').write(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
