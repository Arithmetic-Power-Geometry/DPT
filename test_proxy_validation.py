import unittest,os
from proxy_validation import load,run
PATH=os.environ.get('DPT_BENCHMARK_ZIP','')
@unittest.skipUnless(PATH and os.path.isfile(PATH), 'Separate generated-question benchmark archive not supplied')
class ProxyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run(PATH)
 def test_shape(self):self.assertEqual((self.r['n_questions'],self.r['n_seed_clusters'],self.r['n_conditions']),(1000,100,10))
 def test_counts(self):self.assertEqual((self.r['regionIV_count'],self.r['frontier_candidates']),(541,6))
 def test_arithmetic(self):self.assertEqual(self.r['score_formula_checks']['max_abs_dc_residual'],0);self.assertEqual(self.r['score_formula_checks']['max_abs_qc_residual'],0)
 def test_expected_sign(self):self.assertGreater(self.r['pairs']['DC_vs_novelty']['rho'],0);self.assertLess(self.r['pairs']['QC_vs_usefulness']['rho'],0)
 def test_deterministic(self):
  r2=run(PATH)
  self.assertEqual(self.r['pairs'],r2['pairs'])
if __name__=='__main__':unittest.main()
