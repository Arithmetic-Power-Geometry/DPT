"""Alternative deterministic encodings of frozen pre/post task states.
These are diagnostics, not historical QC or semantic compression.
"""
from pathlib import Path
import json,gzip,csv
from instrumented_rdkit import canonical,resolve,ROOT

def length(text,method):
 b=text.encode('utf-8')
 if method=='utf8':return len(b)
 if method=='pretty_json':return len(json.dumps(json.loads(text),indent=2,sort_keys=True,ensure_ascii=False).encode('utf-8'))
 if method=='gzip':return len(gzip.compress(b,mtime=0))
 raise KeyError(method)

def run():
 tasks=json.loads((ROOT/'frozen_tasks.json').read_text())['tasks']
 rows=[]
 for t in tasks:
  state={'molecule':t['smiles'],'question_id':t['task_id'],'property_request':t['operation'],'measurements':None}
  before=canonical(state);state['measurements']=resolve(t);after=canonical(state)
  row={'task_id':t['task_id']}
  for method in ('utf8','pretty_json','gzip'):
   row[f'{method}_signed_bits']=8*(length(before,method)-length(after,method))
  rows.append(row)
 with (ROOT/'representation_sensitivity.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 return rows
if __name__=='__main__':
 for r in run():print(r)
