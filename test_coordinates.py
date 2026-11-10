import unittest
from coordinates import coordinate,sensitivity
class CoordinateTests(unittest.TestCase):
    def test_compression(self):
        x=coordinate([1,3],[.5,.5],8,5)
        self.assertEqual((x.dc,x.signed_change,x.qc,x.expansion),(2,3,3,0))
    def test_expansion(self):
        x=coordinate([1,3],[.5,.5],5,8)
        self.assertEqual((x.signed_change,x.qc,x.expansion),(-3,0,3))
    def test_zero_edge(self):
        self.assertEqual(coordinate([0],[1],0,0).dc,0)
    def test_invalid(self):
        for args in [([1],[.8],3,2),([-1],[1],3,2),([1],[1],-1,2),([float('nan')],[1],3,2),([],[],3,2)]:
            with self.subTest(args=args),self.assertRaises(ValueError):coordinate(*args)
    def test_sensitivity(self):
        x=sensitivity([1,3],[[.5,.5],[.25,.75]],[7,8],[5,9])
        self.assertEqual(x['scenario_count'],8)
        self.assertEqual(x['dc_interval'],[2,2.5])
        self.assertEqual(x['signed_interval'],[-2,3])
        self.assertEqual(x['qc_interval'],[0,3])
        self.assertEqual(x['expansion_interval'],[0,2])
if __name__=='__main__':unittest.main()
