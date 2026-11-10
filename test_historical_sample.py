import unittest
from historical_sample import CASES,summarize
class CaseRegisterTests(unittest.TestCase):
 def test_count(self):self.assertEqual(summarize()['records'],6)
 def test_dated(self):self.assertEqual(summarize()['dated_records'],5)
 def test_no_coordinates(self):self.assertEqual(summarize()['historical_dc_identified'],0);self.assertEqual(summarize()['historical_qc_identified'],0)
 def test_negative_not_episode(self):self.assertEqual(summarize()['individual_or_pair_cases'],5)
 def test_no_false_failed_claim(self):self.assertIn('not a verified failed',next(x['outcome'] for x in CASES if x['id']=='LVT151012'))
 def test_no_rediscovery_claim(self):self.assertEqual(summarize()['verified_rediscoveries'],0)
 def test_not_representative(self):self.assertFalse(summarize()['is_representative_sample'])
 def test_unique_ids(self):self.assertEqual(len({x['id'] for x in CASES}),6)
 def test_no_impact_selection(self):self.assertTrue(all('citation' not in x for x in CASES))
if __name__=='__main__':unittest.main()
