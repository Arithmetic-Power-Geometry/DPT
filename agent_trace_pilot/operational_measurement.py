"""Reproduce instrumented operational metrics from frozen upstream records.
Not historical Discovery Complexity or Question Compression. Standard library only.
"""
import json,csv,gzip,hashlib
from pathlib import Path
from datetime import datetime
P=Path(__file__).resolve().parent
def measure(r):
 p,c=r["prompt"],r["final_claim"]
 pb,cb=len(p.encode("utf-8")),len(c.encode("utf-8"))
 z=lambda s:len(gzip.compress(s.encode("utf-8"),mtime=0))
 ts=lambda s:datetime.fromisoformat(s.replace("Z","+00:00"))
 return dict(model=r["model"],estimated_tokens=r["total_tokens_est"],wall_time_s=r["wall_time_seconds"],steps=r["steps"],tool_calls=r["tool_calls"],prompt_utf8_bytes=pb,claim_utf8_bytes=cb,naive_signed_change_bits=8*(pb-cb),gzip_signed_change_bits=8*(z(p)-z(c)),timestamp_span_s=(ts(r["collection_timestamp"])-ts(r["first_timestamp"])).total_seconds(),verification_method=r["verification_method"],verified_outcome=r["verification_result"] is not None,historical_DC=None,historical_QC=None)
def run():
 source=json.loads((P/"frozen_trajectory_extract.json").read_text(encoding="utf-8"))
 records=source["records"];assert len(records)==3 and len({r["prompt"] for r in records})==1
 rows=[measure(r) for r in records]
 assert all(not r["verified_outcome"] and r["historical_DC"] is None and r["historical_QC"] is None for r in rows)
 for r,a in zip(records,rows):
  changed=measure({**r,"final_claim":r["final_claim"]+" "*20})
  assert changed["naive_signed_change_bits"]-a["naive_signed_change_bits"]==-160
 out={"task_id":"dd_e01","n_trajectories":3,"n_independent_tasks":1,"n_verified_outcomes":0,"historical_DC_QC_pairs":0,"rows":rows,"warning":"Operational effort and prompt/answer lengths are not theoretical DC/QC"}
 (P/"operational_results.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 with (P/"operational_results.csv").open("w",newline="") as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 return out
if __name__=="__main__":print(json.dumps(run(),indent=2))
