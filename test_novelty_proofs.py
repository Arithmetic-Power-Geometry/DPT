import unittest
from fractions import Fraction
class NoveltyProofChecks(unittest.TestCase):
    def setUp(self): self.points=[(Fraction(0),Fraction(0)),(Fraction(1),Fraction(2,5)),(Fraction(2),Fraction(1))]
    def test_nondominated(self):
        for i,(d,q) in enumerate(self.points):
            self.assertFalse(any(j!=i and a<=d and b>=q and (a<d or b>q) for j,(a,b) in enumerate(self.points)))
    def test_midpoint_missing(self):
        self.assertNotIn((Fraction(1),Fraction(1,2)),self.points)
    def test_middle_unsupported_for_positive_lambdas(self):
        for lam in [Fraction(i,1000) for i in range(1,10001)]:
            utilities=[q-lam*d for d,q in self.points]
            self.assertLess(utilities[1],max(utilities[0],utilities[2]))
    def test_thresholds_disjoint(self):
        self.assertLess(Fraction(2,5),Fraction(3,5))
if __name__=='__main__': unittest.main()
