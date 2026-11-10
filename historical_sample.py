"""Auditable purposive case register; not a probability sample or historical DPT estimates."""
import csv,json
from pathlib import Path
CASES=[
 dict(id='GW150914',category='landmark_confirmed',date='2015-09-14',source='https://ligo.org/detections/gw150914/',outcome='confirmed gravitational-wave event',snr='24',dc='',qc='',pathway='detector observation; matched filtering; multi-detector verification',status='documented_outcome_partial_pathway'),
 dict(id='GW151226',category='routine_followup_confirmed',date='2015-12-26',source='https://gwosc.org/s/events/GW151226/GW151226.html',outcome='confirmed second gravitational-wave event',snr='13',dc='',qc='',pathway='O1 detector observation; matched filtering; publication',status='documented_outcome_partial_pathway'),
 dict(id='LVT151012',category='marginal_unconfirmed_at_initial_release',date='2015-10-12',source='https://gwosc.org/s/events/LVT151012/LVT151012.html',outcome='initial candidate significance 1.7 sigma; not a verified failed discovery',snr='9.7',dc='',qc='',pathway='O1 candidate search; marginal classification',status='dated_initial_classification_not_permanent_failure'),
 dict(id='CRISPR_MOJICA_POURCEL',category='independent_convergent_work',date='2005',source='https://www.broadinstitute.org/what-broad/areas-focus/project-spotlight/crispr-timeline',outcome='two independently published related spacer findings; not proven rediscovery of identical question',snr='',dc='',qc='',pathway='independent research groups; publications',status='secondary_timeline_primary_article_audit_pending'),
 dict(id='KEPLER_KOI_FALSE_POSITIVE_CLASS',category='negative_case_class_not_individual_episode',date='',source='https://exoplanet.ipac.caltech.edu/docs/API_kepcandidate_columns.html',outcome='false-positive disposition is defined; no specific dated KOI selected',snr='',dc='',qc='',pathway='threshold crossing; diagnostic vetting; classification',status='class_definition_only_not_historical_episode'),
 dict(id='HARTLEY_SHANNON',category='historical_conceptual_transition',date='1948-07',source='https://doi.org/10.1002/j.1538-7305.1948.tb01338.x',outcome='published mathematical generalization',snr='',dc='',qc='',pathway='Hartley 1928 to Shannon 1948 published formalism',status='publication_relation_not_private_search_pathway'),
]
FIELDS=['id','category','date','source','outcome','snr','dc','qc','pathway','status']
def summarize(rows=CASES):
 assert len(rows)==len({r['id'] for r in rows})
 assert all(r['source'].startswith('https://') for r in rows)
 return {'records':len(rows),'dated_records':sum(bool(r['date']) for r in rows),'individual_or_pair_cases':sum(r['category']!='negative_case_class_not_individual_episode' for r in rows),'historical_dc_identified':sum(bool(r['dc']) for r in rows),'historical_qc_identified':sum(bool(r['qc']) for r in rows),'verified_rediscoveries':0,'verified_failed_research_programs':0,'is_representative_sample':False}
def write(path):
 path=Path(path);path.mkdir(exist_ok=True,parents=True)
 with (path/'historical_sample.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,FIELDS);w.writeheader();w.writerows(CASES)
 (path/'historical_sample_summary.json').write_text(json.dumps(summarize(),indent=2)+'\n')
if __name__=='__main__':write(Path(__file__).parent);print(json.dumps(summarize(),indent=2))
