import unittest,sys,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from baselines import run
ARCHIVE=os.environ.get('DPT_BENCHMARK_ZIP','')
@unittest.skipUnless(ARCHIVE and os.path.isfile(ARCHIVE), 'Separate generated-question benchmark archive not supplied')
class TestBaselines(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run(ARCHIVE,permutations=4)
 def test_groups(self):self.assertEqual(self.r['seed_groups'],100)
 def test_fold_count(self):self.assertEqual(self.r['folds'],5)
 def test_models(self):self.assertEqual(len(self.r['models']['novelty_proxy']),9)
 def test_improvement(self):self.assertGreater(self.r['models']['novelty_proxy']['two_vs_cost_delta_rmse']['observed'],0)
 def test_limitations(self):self.assertIn('NOT historical',self.r['scope'])
if __name__=='__main__':unittest.main()
