#!/usr/bin/env python3
"""Frozen deterministic metadata-only candidate triage; NOT episode classification."""
import csv,io,zipfile,hashlib,collections,argparse,json,pathlib
ERA=[('pre1980',None,1979),('1980-1999',1980,1999),('2000-2026',2000,2026)]
FIELDS=['Physics','Chemistry','Biology Medicine','Computer Science','Mathematics']
def select(rows,per_cell=3):
    result=[];counts={}; selected_ids=set()
    for field in FIELDS:
        for era,lo,hi in ERA:
            eligible=[]
            for r in rows:
                try: year=int(r['publication_year'])
                except (ValueError,KeyError): continue
                if r['requested_domain']!=field or not (lo is None or year>=lo) or year>hi:continue
                if r.get('is_retracted')=='True':continue
                if not r.get('title') or not r.get('openalex_id'):continue
                eligible.append(r)
            eligible.sort(key=lambda r:(hashlib.sha256(('DPT-JOI-P05-v1|'+r['candidate_id']).encode()).hexdigest(),r['candidate_id']))
            counts[field+'|'+era]={'eligible':len(eligible),'selected':min(per_cell,len(eligible))}
            for r in eligible[:per_cell]:
                assert r['candidate_id'] not in selected_ids
                selected_ids.add(r['candidate_id'])
                result.append({'candidate_id':r['candidate_id'],'field':field,'era':era,'publication_year':r['publication_year'],'subfield':r.get('subfield',''),'title':r['title'],'doi':r.get('doi',''),'openalex_id':r['openalex_id'],'abstract_available':r.get('abstract_available',''),'screening_status':'UNREVIEWED_METADATA_CANDIDATE','episode_type':'UNDETERMINED','historical_cutoff':'','primary_source_verified':'NO','reconstructable':'UNASSESSED','negative_case':'UNASSESSED','reason':'deterministic SHA256 within field-era; no citation/impact ranking'})
    return result,counts
def main():
    p=argparse.ArgumentParser();p.add_argument('zip');p.add_argument('--out',default='P05_candidate_triage.csv');a=p.parse_args()
    with zipfile.ZipFile(a.zip) as z:
        names=[n for n in z.namelist() if n.endswith('data/processed/discoverybench_candidates_1500.csv')]
        assert len(names)==1
        rows=list(csv.DictReader(io.StringIO(z.read(names[0]).decode('utf-8-sig'))))
    assert len(rows)==1500 and len({r['candidate_id'] for r in rows})==1500
    selected,counts=select(rows)
    with open(a.out,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=selected[0].keys());w.writeheader();w.writerows(selected)
    print(json.dumps({'source_records':len(rows),'triage_candidates':len(selected),'cells':counts,'source_abstract_available':collections.Counter(r.get('abstract_available') for r in rows),'source_retracted':collections.Counter(r.get('is_retracted') for r in rows),'triage_is_not_validated_episode_sampling':True},indent=2))
if __name__=='__main__':main()
