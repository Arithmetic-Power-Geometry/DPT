import unittest, math
from historical_episode import entropy_binary, diagnostic
class TestHistory(unittest.TestCase):
    def test_uniform(self): self.assertAlmostEqual(entropy_binary(.5),1)
    def test_extremes(self): self.assertEqual(entropy_binary(0),0); self.assertEqual(entropy_binary(1),0)
    def test_asymmetric(self): self.assertAlmostEqual(entropy_binary(.75),.8112781244591328)
    def test_symmetry(self): self.assertAlmostEqual(entropy_binary(.2),entropy_binary(.8))
    def test_invalid(self):
        with self.assertRaises(ValueError): entropy_binary(1.1)
    def test_missing_not_zero(self): self.assertEqual(diagnostic(.75)['historical_DC'],'NA')
if __name__=='__main__':unittest.main()
