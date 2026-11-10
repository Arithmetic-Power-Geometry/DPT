"""Source-anchored documentary outcomes, deliberately NOT DPT coordinate validation."""
import json
from pathlib import Path

RECORDS = [
 {"id":"HARTLEY1928_SHANNON1948","domain":"information theory","source_date":"1948-07","source":"https://doi.org/10.1002/j.1538-7305.1948.tb01338.x","outcome":"published_mathematical_generalization","outcome_value":1,"outcome_unit":"documented_publication_transition","cost_components":{},"matched_representation":False,"independent_of_dpt_scoring":True,"historical_dc":None,"historical_qc":None,"reason":"No dated historical labor-cost register or matched encoding"},
 {"id":"GW150914","domain":"gravitational wave astronomy","source_date":"2015-09-14","source":"https://gwosc.org/events/GW150914/","outcome":"matched_filter_snr","outcome_value":24,"outcome_unit":"dimensionless","secondary":{"false_alarm_upper_per_year":1/203000,"false_alarm_inequality":"strictly less than","coincident_background_days":16,"hanford_veto_pct":4,"livingston_veto_pct":1},"cost_components":{"verification":{"value":16,"unit":"coincident detector days used for background analysis","scope":"post-detection analysis, not total discovery cost"}},"matched_representation":False,"independent_of_dpt_scoring":True,"historical_dc":None,"historical_qc":None,"reason":"Measured verification exposure is not a full six-component search cost or a minimum"},
 {"id":"KEPLER_DR25_PLTI","domain":"exoplanet astronomy","source_date":"2017-06-01","source":"https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20170009553.pdf","outcome":"transit_injection_recovery_experiment_documented","outcome_value":1,"outcome_unit":"documented_pipeline_experiment","secondary":{"pipeline_version":"SOC 9.3","data_release":"DR25","injection_unit":"one simulated transit signal per target","recovery_rate":None},"cost_components":{},"matched_representation":False,"independent_of_dpt_scoring":True,"historical_dc":None,"historical_qc":None,"reason":"No independently retrieved target-level injection/recovery file or historical search-cost register"}
]

def audit(records=RECORDS):
 assert len({r['id'] for r in records})==len(records)
 for r in records:
  assert r['independent_of_dpt_scoring'] is True
  assert r['historical_dc'] is None and r['historical_qc'] is None
  assert r['source'].startswith('https://')
  assert r['outcome_value'] is not None
 assert records[1]['secondary']['false_alarm_upper_per_year'] < 0.000005
 return {"episode_count":len(records),"externally_documented_outcomes":len(records),"paired_historical_dc_outcomes":sum(r['historical_dc'] is not None for r in records),"paired_historical_qc_outcomes":sum(r['historical_qc'] is not None for r in records),"predictive_validation_permitted":False,"records":records}

if __name__=='__main__':
 Path('external_outcomes.json').write_text(json.dumps(audit(),indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({k:v for k,v in audit().items() if k!='records'},indent=2))
