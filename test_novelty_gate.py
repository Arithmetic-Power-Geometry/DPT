import unittest
from novelty_gate import read,evaluate,dominates
class GateTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.rows=read();cls.r=evaluate(cls.rows)
 def test_n(self):self.assertEqual(self.r['n_records'],9)
 def test_three_tasks(self):self.assertEqual(self.r['n_tasks'],3)
 def test_one_domain(self):self.assertEqual(self.r['n_domains'],1)
 def test_no_verified_outcome(self):self.assertEqual(self.r['verified_outcomes'],0)
 def test_no_predictive_baseline(self):self.assertIsNone(self.r['outcome_based_baseline_comparisons'])
 def test_no_historical_dc(self):self.assertIsNone(self.r['independent_historical_dc'])
 def test_no_historical_qc(self):self.assertIsNone(self.r['independent_historical_qc'])
 def test_folds(self):self.assertEqual(self.r['negative_controls']['task_holdout_folds'],3)
 def test_no_label_permutation(self):self.assertFalse(self.r['negative_controls']['label_permutation_defined'])
 def test_whitespace_control(self):self.assertEqual(self.r['negative_controls']['whitespace_20_spaces_signed_bit_change'],-160)
 def test_no_self_dominance(self):self.assertTrue(all(not dominates(x,x) for x in self.rows))
 def test_frontier_nonempty(self):self.assertTrue(all(x['pareto_models'] for x in self.r['per_task']))
 def test_no_duplicate_task_model(self):self.assertEqual(len({(r['task'],r['model']) for r in self.rows}),9)
 def test_gemini_token_min(self):self.assertTrue(all(x['minimum_token_model']=='gemini-3.1-pro' for x in self.r['per_task']))
 def test_gpt_easy_time_min(self):self.assertEqual(next(x for x in self.r['per_task'] if x['task']=='dd_e01')['minimum_time_model'],'gpt-5.4')
if __name__=='__main__':unittest.main()
