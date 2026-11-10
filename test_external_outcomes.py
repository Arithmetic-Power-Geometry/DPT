import unittest
from external_outcomes import audit,RECORDS
class DocumentaryAudit(unittest.TestCase):
 def test_three_distinct_cases(self):self.assertEqual(audit()['episode_count'],3)
 def test_no_paired_coordinates(self):self.assertEqual(audit()['paired_historical_dc_outcomes'],0);self.assertEqual(audit()['paired_historical_qc_outcomes'],0)
 def test_outcome_not_proxy(self):self.assertTrue(all(r['independent_of_dpt_scoring'] for r in RECORDS))
 def test_ligo_background_not_cost(self):self.assertIn('not total discovery cost',RECORDS[1]['cost_components']['verification']['scope'])
 def test_kepler_no_invented_rate(self):self.assertIsNone(RECORDS[2]['secondary']['recovery_rate'])
 def test_negative_control_leakage(self):
  r=[dict(x) for x in RECORDS];r[0]['historical_dc']=1
  with self.assertRaises(AssertionError):audit(r)
 def test_falsification_outcome_missing(self):
  r=[dict(x) for x in RECORDS];r[0]['outcome_value']=None
  with self.assertRaises(AssertionError):audit(r)
 def test_sensitivity_missing_case(self):
  r=RECORDS[:2];self.assertEqual(audit(r)['episode_count'],2);self.assertFalse(audit(r)['predictive_validation_permitted'])
if __name__=='__main__':unittest.main()
